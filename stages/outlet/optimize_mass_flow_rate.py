"""
Author: Alejandro Valencia
Update: October 14, 2023
"""

from ccpd.data_types.thermo_point import ThermodynamicVariable
from ccpd.data_types.three_dimensional_blade import VelocityTriangle, VelocityVector
from ccpd.data_types.working_fluid import WorkingFluid
from ccpd.data_types.inputs import Inputs
from ccpd.data_types.centrifugal_compressor import CompressorStage, CompressorGeometry
from ccpd.data_types.centrifugal_compressor_geometry import DiameterStruct
from ccpd.stages.outlet.friction_coefficient import CalculateFrictionCoefficient
import numpy as np
from colorama import Fore
import logging

logger = logging.getLogger(__name__)


class OutletLoopCollector:
    def __init__(self) -> None:
        self.name = __name__

    def Print(self) -> None:
        for key, value in self.__dict__.items():
            if key == "name":
                print(f"{Fore.YELLOW}INFO: {__name__}{Fore.RESET}")
            elif type(value) == float:
                print(f"\t{key}: {value: 0.6f}")
            else:
                print(f"\t{key}: {value}")


def calculate_geometric_inlet_angle(
    inlet_diameter: DiameterStruct,
    inlet_relative_velocity_angles_dict: dict,
    number_of_blades: int,
    blade_thickness: float,
) -> dict:
    """
    This function calculates the inlet geometric angle based on zero
        incidence losses.

    The following are inputs:

                inlet: Inlet structure
                   Nb: Number of blades
                   th: Blade thickness

    The following is the output:

                beta_geo: Structure containing the geometric inlet angles
    """
    geometric_inlet_angle_dict = dict()
    for section_name, section_length in inlet_diameter.__dict__.items():
        section_area = np.pi * section_length - number_of_blades * blade_thickness
        optimal_area = np.pi * section_length
        geometric_inlet_angle = np.arctan(
            (section_area / optimal_area) * np.tan(inlet_relative_velocity_angles_dict[section_name].relative.angle)
        )
        geometric_inlet_angle_dict[section_name] = geometric_inlet_angle

    return geometric_inlet_angle_dict


def CalculateDiffusionLosses(
    D1: DiameterStruct,
    D2: DiameterStruct,
    average_inlet_relative_angle: float,
    inlet_relative_velocities: list,
    outlet_absolute_velocity: VelocityVector,
    outlet_relative_velocity: VelocityVector,
    outlet_translational_velocity: VelocityVector,
    number_of_blades: int,
    blade_height: float,
) -> tuple[float, float]:
    hydraulic_length = (D2.mid / 2 - D1.mid / 2) / np.cos(average_inlet_relative_angle)
    average_relative_inlet_velocity = np.mean(inlet_relative_velocities).astype(float)
    diffusion_factor = (
        1
        - outlet_relative_velocity.magnitude / average_relative_inlet_velocity
        + (np.pi * D2.mid * outlet_absolute_velocity.tangential)
        / (2 * number_of_blades * hydraulic_length * average_relative_inlet_velocity)
        + 0.1
        * (D1.tip / 2 - D1.hub / 2 + blade_height)
        / (D2.mid / 2 - D1.tip / 2)
        * (1 + outlet_relative_velocity.magnitude / average_relative_inlet_velocity)
    )
    return (
        0.05 * diffusion_factor**2 * outlet_translational_velocity.magnitude**2,
        hydraulic_length,
    )


def CalculateFrictionalLosses(
    outlet_diameter: float,
    blade_height: float,
    number_of_blades: int,
    pitch: float,
    static_density: float,
    outlet_relative_velocity: VelocityVector,
    slip_factor: float,
    surface_roughness: float,
    hydraulic_length: float,
) -> float:
    """
    We first calculate our outlet perimeter and area. Remember that the
    outlet of a centrifugal machine is rectangular. With these two
    quantities we define our hydraulic diameter which will be used to
    determine our flow regime via Reynolds number.
    """
    outlet_flow_area = np.pi * outlet_diameter * blade_height
    outlet_flow_perimeter = number_of_blades * (2 * blade_height + 2 * pitch)
    hydraulic_diameter = 4 * outlet_flow_area / outlet_flow_perimeter
    reynolds_number = static_density * outlet_relative_velocity.magnitude * hydraulic_diameter / slip_factor

    # Enthalpy increase
    relative_roughness = surface_roughness / hydraulic_diameter
    coefficient_of_friction = CalculateFrictionCoefficient(reynolds_number, relative_roughness)
    adjusted_friction_coefficient = coefficient_of_friction + 0.0015

    return (
        4
        * (adjusted_friction_coefficient * hydraulic_length * outlet_relative_velocity.magnitude**2)
        / (2 * hydraulic_diameter)
    )


def optimize_mass_flow(
    inlet: CompressorStage,
    outlet: CompressorStage,
    compressor_geometry: CompressorGeometry,
    fluid: WorkingFluid,
    inverse_exponent: float,
    eulerian_work: float,
    inputs: Inputs,
    max_iterations: int,
    tolerance: float,
) -> tuple[CompressorStage, dict, int]:
    outlet_debug_collector = OutletLoopCollector()
    # []:Initalize
    # Assume an isentropic process for the rotor to begin the iteration
    #   process. This process is to converge to the real pressure at the
    #   outlet of the compressor.
    eta_0 = 1.0
    D1 = DiameterStruct(
        compressor_geometry.inlet_hub_diameter,
        compressor_geometry.inlet_mid_diameter,
        compressor_geometry.inlet_tip_diameter,
    )
    D2 = DiameterStruct(
        mid=compressor_geometry.outer_diameter,
    )

    U2 = outlet.blade.mid.translational
    V2 = outlet.blade.mid.absolute
    W2 = outlet.blade.mid.relative

    temperature = ThermodynamicVariable()
    pressure = ThermodynamicVariable()
    density = ThermodynamicVariable()

    # Loop
    number_of_blades = 0
    geometric_inlet_angle = {}
    for iteration in range(0, max_iterations):
        iteration += 1
        logger.debug(f"Iteration: {iteration}")

        # [A]:Total & Static Temperature
        temperature.total = inlet.thermodynamic_point.temperature.total + (eulerian_work * eta_0 / fluid.specific_heat)
        temperature.static = temperature.total - (V2.magnitude**2) / (2 * fluid.specific_heat)
        logger.debug(f"Outlet temperature: {temperature}")

        outlet.blade.mid_mach_number.absolute = V2.magnitude / np.sqrt(
            fluid.specific_ratio * fluid.specific_heat * temperature.static
        )

        # [B]:Isentropic Outlet Pressure
        pressure.static = inlet.thermodynamic_point.pressure.static * (
            temperature.static / inlet.thermodynamic_point.temperature.static
        ) ** (inverse_exponent)

        pressure.total = pressure.static * (
            1.0
            + ((fluid.specific_ratio - 1.0) / 2.0) * (outlet.blade.mid_mach_number.absolute**2) ** inverse_exponent
        )
        logger.debug(f"Outlet pressure: {pressure}")

        # [C]:Density & Blade Height
        density.static = pressure.static / (fluid.specific_gas_constant * temperature.static)
        logger.debug(f"Outlet density: {density}")

        compressor_geometry.outlet_blade_height = inputs.mass_flow_rate / (
            density.static * np.pi * compressor_geometry.outer_diameter * V2.axial
        )

        # [D]:Stability Check
        compressor_geometry.outer_blade_height_ratio = compressor_geometry.outlet_blade_height / (
            compressor_geometry.outer_diameter / 2
        )

        # To calculate the average flow deflection use the midspan inlet
        #  relative angle
        average_inlet_relative_angle = (W2.angle + inlet.blade.mid.relative.angle) / 2

        #  [F]:Number of Blades
        #  Before continuing we define the solidity. Theory and practice tell
        #   us to keep 1/solidity = 0.4. For the number of blades we round up
        #   and add 1 blade to minimize the blade loading. The pitch and chord
        #   are also calculated.
        inverse_solidity = 0.4
        number_of_blades = (
            2
            * (np.pi * np.cos(average_inlet_relative_angle))
            / (inverse_solidity * np.log((compressor_geometry.outer_diameter / compressor_geometry.inlet_mid_diameter)))
        )
        number_of_blades = np.ceil(number_of_blades) + 1
        pitch = np.pi * compressor_geometry.outer_diameter / number_of_blades
        chord = pitch / inverse_solidity
        logger.debug(f"Number of blades: {number_of_blades}")

        # [G]:Slip Factor & Freestream Velocity
        slip_factor = 1 - 0.63 * np.pi / number_of_blades
        logger.debug(f"Slip factor: {slip_factor}")

        outlet_free_stream_velocity = (1 - slip_factor) * outlet.blade.mid.translational.magnitude + V2.tangential
        outlet_free_stream_relative_velocity = outlet_free_stream_velocity - U2.magnitude
        geometric_outlet_angle = np.arctan(outlet_free_stream_relative_velocity / W2.axial)

        #  [I]:Calculate Losses
        #  [I.1]:Geometric Inlet Angle
        #  We first analyze the losses due to having a difference in the
        #   geometrical outlet angle and the fluid outlet angle. Here we
        #   need the thickness of our blade that is assumed for now.
        blade_thickness = 0.002
        inlet_relative_velocity_angles = {
            key: value for key, value in zip(D1.__dict__.keys(), inlet.blade.__dict__.values())
        }
        geometric_inlet_angle = calculate_geometric_inlet_angle(
            D1, inlet_relative_velocity_angles, number_of_blades, blade_thickness
        )
        incidence = geometric_inlet_angle["hub"] - inlet.blade.hub.relative.angle
        incidence_losses = ((inlet.blade.hub.relative.magnitude * np.sin(incidence)) ** 2) / 2.0
        logger.debug(f"geometric_relative_velocity_angles: {geometric_inlet_angle}")
        logger.debug(f"incidence_losses: {incidence_losses}")

        # Tip clearance
        # From paper provided by Gaetani we found the following relation to
        #   calculate tip losses. The tip clearance was also found via
        #   other papers to be roughly 2% of the exit blade height
        if inputs.tip_clearance == 0:
            inputs.tip_clearance = 0.02 * blade_thickness

        clearance_losses = (
            0.6
            * inputs.tip_clearance
            / compressor_geometry.outlet_blade_height
            * V2.tangential
            * np.sqrt(
                4
                * np.pi
                / (compressor_geometry.outlet_blade_height * number_of_blades)
                * np.ceil(
                    (D1.tip**2 / 4 - D1.hub**2 / 4)
                    / ((D2.mid / 2 - D1.tip / 2) * (1 + pressure.static / inlet.thermodynamic_point.pressure.static))
                )
                * V2.tangential
                * inlet.blade.mid.absolute.axial
            )
        )
        logger.debug(f"clearance_losses: {clearance_losses}")

        # [I.3]:Blade Losses
        inlet_relative_velocities = [
            inlet.blade.hub.relative.magnitude,
            inlet.blade.mid.relative.magnitude,
            inlet.blade.tip.relative.magnitude,
        ]

        diffusion_losses, hydraulic_length = CalculateDiffusionLosses(
            D1,
            D2,
            average_inlet_relative_angle,
            inlet_relative_velocities,
            V2,
            W2,
            U2,
            number_of_blades,
            compressor_geometry.outlet_blade_height,
        )
        logger.debug(f"diffusion_losses: {diffusion_losses:.3}")

        # Friction Losses
        friction_losses = CalculateFrictionalLosses(
            D2.mid,
            compressor_geometry.outlet_blade_height,
            number_of_blades,
            pitch,
            pressure.static,
            W2,
            slip_factor,
            inputs.surface_roughness,
            hydraulic_length,
        )
        logger.debug(f"friction_losses: {friction_losses:.3}")

        # [J]:Calculate New Efficiency
        sum_of_enthalpy_losses = np.sum([diffusion_losses, friction_losses, clearance_losses, incidence_losses])
        eta_new = (eulerian_work - sum_of_enthalpy_losses) / eulerian_work
        residual = np.abs(eta_new - eta_0) / eta_0

        logger.debug(f"Residual: {residual:0.4f}\n")
        if residual < tolerance:
            logger.info(f"Outlet calculations converged in {iteration} iterations; residual = {residual:0.6f}")
            break

        # [K]:New Total Enthalpy Change & Eulerian Work
        isentropic_work_new = eulerian_work * eta_new
        eta_0 = eta_new
        logger.debug(f"Outlet efficiency: {eta_0}")

        if iteration == max_iterations:
            logger.warning(f"{Fore.YELLOW}WARNING:{Fore.RESET} Max iterations reached")
            break

        outlet.thermodynamic_point.pressure = pressure
        outlet.thermodynamic_point.temperature = temperature
        outlet.thermodynamic_point.density = density

    return (outlet, geometric_inlet_angle, number_of_blades)
