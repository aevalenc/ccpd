"""
Author: Alejandro Valencia
Centrifugal Compressor Preliminary Design
Vaneless Diffuser Calculations
Update: December 20, 2023
"""
import numpy as np
from ccpd.data_types.centrifugal_compressor import CompressorStage
from ccpd.data_types.centrifugal_compressor_geometry import CompressorGeometry
from ccpd.data_types.thermo_point import ThermoPoint, ThermodynamicVariable
from ccpd.data_types.three_dimensional_blade import MachTriangle, ThreeDimensionalBlade, VelocityTriangle
from ccpd.data_types.working_fluid import WorkingFluid
import logging

logger = logging.getLogger(__name__)


def vaneless_diffuser_calcs(
    outlet: CompressorStage,
    compressor_geometry: CompressorGeometry,
    working_fluid: WorkingFluid,
    mass_flow_rate: float,
    max_iterations: int,
    tolerance: float,
) -> tuple[CompressorStage, float]:
    """
    This function takes a current compressor design and calculates the
         necessary quantities for a vanless diffuser. For the purposes of this
         code, point 2 refers to the outlet of the compressor / inlet of the
         vaneless diffuser and point 3 refers to the outlet of the said
         diffuser.

    The following are the inputs:

                 design: Current design structure
                 max_iterations: Max iterations for loop
                 tolerance: Tolerance

    The following is the output

                 result: Design with added vaneless diffuser structure

    """

    # []:Grab Required Values From Design
    outlet_density = outlet.thermodynamic_point.density  # [kg/m^3] Outlet density
    outlet_pressure = outlet.thermodynamic_point.pressure  # [Pa]     Outlet real pressure
    outlet_temperature = outlet.thermodynamic_point.temperature  # [Pa]     Outlet real temperature

    V2 = outlet.blade.mid.absolute  # [m/s]    Outlet velocity
    b2 = compressor_geometry.outlet_blade_height  # [m]      Outlet blade height
    D2 = compressor_geometry.outer_diameter  # [m]      Outlet diameter

    # Initialize Diffuser Values
    density = ThermodynamicVariable()
    temperature = ThermodynamicVariable()
    pressure = ThermodynamicVariable()

    # []:Calculate Vanless Diffuser Diameter
    # We assume a ratio between the outlet diameter and the vaneless
    #   diffuser. In addition, we assume that the blade height will remain
    #   the same, i.e. b3 = b2.
    vaneless_diffuser_to_outlet_diameter_ratio = 1.2
    D3 = vaneless_diffuser_to_outlet_diameter_ratio * D2
    b3 = b2

    # []:Setup Density Loop
    # In this iterative loop, we initialize the average density and the
    #   average velocity with the compressor outlet conditions. As a
    #   result, set rho3 and V3 to outlet_density and V2 respectively to begin the
    #   optimization process. Note that since the diffuser is basically a
    #   stator and no work is done. TT3 will equal TT2.
    temperature.total = outlet_temperature.total  # [K]
    density.static = outlet_density.static  # [kg/m^3]
    V3 = V2  # [m/s]
    M3 = MachTriangle()
    hydraulic_diameter = (4 * np.pi * D3 * b3) / (2 * (np.pi * D3 + b3))  # [m]
    logger.debug(f"Hydraulic diameter: {hydraulic_diameter}")

    for iteration in range(0, max_iterations):
        iteration += 1
        logger.debug(f"Iteration: {iteration}")

        # []:Calculate Average Quantities
        average_density = (outlet_density.static + density.static) / 2  # [kg/m^3]
        average_velocity = (V3.magnitude + V2.magnitude) / 2  # [m/s]
        Re_avg = average_density * hydraulic_diameter * average_velocity / working_fluid.kinematic_viscosity

        # []:Calculate Friction Coefficient
        k = 0.02  # [] Experimental constant
        cf = k * (1.8 * 10**5 / Re_avg)  # [] Friction coefficient
        logger.debug(f"Friction coefficient: {cf}")

        # []:Vanless Diffuser Outlet Velocity
        den = (
            vaneless_diffuser_to_outlet_diameter_ratio
            + cf / 2 * np.pi * outlet_density.static * V2.tangential * D3 * (D3 - D2) / mass_flow_rate
        )
        V3.tangential = V2.tangential / den
        V3.axial = mass_flow_rate / (np.pi * D3 * b3 * density.static)
        V3.CalculateMagnitudeWithComponents()

        # []:Thermodynamic Values
        temperature.static = temperature.total - V3.magnitude**2 / (2 * working_fluid.specific_heat)
        M3.absolute = V3.magnitude / np.sqrt(
            working_fluid.specific_ratio * working_fluid.specific_gas_constant * temperature.static
        )

        # []:Calculate Losses
        num = cf * D2 / 2 * (1 - (1 / vaneless_diffuser_to_outlet_diameter_ratio) ** 1.5) * V2.magnitude**2
        den = 1.5 * b2 * np.cos(V2.angle)
        enthalpy_drop = num / den

        # []:Calculate Isentropic Values
        TT3is = temperature.total - enthalpy_drop / working_fluid.specific_heat
        T3is = TT3is - V3.magnitude**2 / (2 * working_fluid.specific_heat)
        pressure.total = outlet_pressure.static * (TT3is / outlet_temperature.static) ** (
            working_fluid.specific_ratio / (working_fluid.specific_ratio - 1)
        )
        pressure.static = pressure.total / (1 + (working_fluid.specific_ratio - 1) / 2 * M3.absolute**2) ** (
            working_fluid.specific_ratio / (working_fluid.specific_ratio - 1)
        )

        # []:Calculate Outlet Density
        new_density = pressure.static / (working_fluid.specific_gas_constant * temperature.static)
        logger.debug(f"New density: {new_density}")

        # []:Calculate Residual
        residual = abs(density.static - new_density) / density.static
        logger.debug(f"Residual: {residual:0.3f}\n")

        if residual < tolerance:
            logger.info(f"Vanless Diffuser calculations converged in {iteration} iterations")
            break
        elif iteration == max_iterations:
            logger.warning(f"WARNING: Max iterations reached\n")

        density.static = new_density

    vaneless_diffuser = CompressorStage(
        ThermoPoint(pressure, density, temperature),
        ThreeDimensionalBlade(_mid=VelocityTriangle(_absolute=V3), _mid_mach_number=M3),
    )
    logger.debug(f"Vaneless diffuser: {vaneless_diffuser}")

    return vaneless_diffuser, D3
