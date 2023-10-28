""" 
  Author: Alejandro Valencia
  Centrifugal Compressor Preliminary Design
  Inlet Iteration Loop
  Update: 1 May, 2023
"""

from ccpd.data_types.centrifugal_compressor import CompressorGeometry, CompressorStage
from ccpd.data_types.three_dimensional_blade import (
    ThreeDimensionalBlade,
    VelocityVector,
    VelocityTriangle,
)
from ccpd.data_types.thermo_point import ThermodynamicVariable, ThermoPoint
from ccpd.data_types.inputs import Inputs
from ccpd.data_types.working_fluid import WorkingFluid
from ccpd.utilities.inlet.tip_diameter import ComputeTipDiameter
from numpy import pi, sqrt, float64
from colorama import Fore

# This function takes initial design parameters and calculates the inlet
# 	tip diameter minimizing the relative velocity function. This comes
# 	from the fact that for a centrifugal compressor we want to minimize
# 	the relative Mach number to avoid shock waves and flow separation.
# 	Once a tip diameter is found the density is caluclated. This is an
# 	iterative process where the goal is to find a tip diameter that
# 	matches the density based on our given inlet operating conditions.
#
#       The following are inputs:
#
#           rho0  : Initial density guess
#           hub_diameter  : Hub diameter
#           itermx: Max iterations
#           tol   : Tolerance
#           monitor_residual: String either 'yes' or 'no'
#
#       The following are outputs:
#
#           result: Structure containing the thermofluid properties at
# 					 the inlet after converging to the inlet density
#
# In order to optimize the tip diameter we begin by choosing a hub
#   diameter. The optimal tip diameter will be found by minimizing the
#   relative velocity function (yet to be defined). Recall our golden
#   vector equation.
#
#       V = U + W                               Eq.(1)
#
# V in this case is assumed to be axial (very typical). Thus resulting in
#   the following velocity diagram and equation assuming clockwise
#   rotation.
#
#                               Utip                             axial
#                            --------->^                           ^
#                            \         |                           |
#                             \        |                           |
#                              \       |                           |------->
#                               \      |                           tangential
#                                \     |
#                       W1tip     \    | V1tip = V1atip = V1
#                                  \   |
#                                   \  |
#                                    \ |
#                                     \|
#
#              W1tip^2 = Utip^2 + V1tip^2      Eq.(2)
#
# We can express the translation velocity at the hub in terms of the tip
#  diameter. The expression for V1tip we obtain through the mass flow rate.
#  The inlet absolute velocity is given by
#
#      V1tip = mdot / (rho * S1)               Eq.(3)
#
# Where S1 is the inlet flow area. This can be expressed in terms of our
#  diameters.
#
#      S1 = pi/4 * (Dtip^2 - Dhub^2)           Eq.(4)
#
# The translational velocity is simply given by
#
#      Utip = w * Dtip / 2                     Eq.(5)
#
# Substituting all these expressions into Eq.(2) we derive our relative
# 	velocity function
#
#      W1tip^2 = w^2 * Dtip^2/4 + (mdot / (rho * pi/4 * (Dtip^2 - Dhub^2)))
#


class InletLoopCollector:
    def __init__(self) -> None:
        self.name = __name__

    def Print(self) -> None:
        for key, value in self.__dict__.items():
            if key == "name":
                print(f"{Fore.YELLOW}INFO: {__name__}{Fore.RESET}")
            elif type(key) == str:
                print(f"\t{key}: {value}")
            else:
                print(f"\t{key}: {value: 4.1f}")


def IsInletLoopConverged(
    density_residual, tolerance, iteration, debug_collector: InletLoopCollector
):
    if density_residual < tolerance:
        setattr(
            debug_collector,
            "converge_message",
            f"Minimization problem converged in {iteration} iterations w/ residual: {density_residual:8.6}\n",
        )
        return True

    elif density_residual > 1e6:
        setattr(
            debug_collector,
            "converge_message",
            f"{Fore.YELLOW}WARNING: solution diverging",
        )
        return False


def InletLoop(
    inputs: Inputs,
    fluid: WorkingFluid,
    static_density_guess: float,
    rotational_speed: float,
    compressor_geometry: CompressorGeometry,
    max_iterations: int,
    tolerance: float,
) -> CompressorStage:
    inlet_loop_collector = InletLoopCollector()

    # Quantities
    T = ThermodynamicVariable()
    P = ThermodynamicVariable()
    rho = ThermodynamicVariable()
    V = VelocityVector()
    inlet_flow_area = 0.0

    T.total = inputs.inlet_total_temperature
    P.total = inputs.inlet_total_pressure

    # []:Optimization Loop
    for iteration in range(0, max_iterations):
        # Minimize Inlet Tip Diameter
        tip_diameter = ComputeTipDiameter(
            float64(rotational_speed),
            inputs.mass_flow_rate,
            float64(static_density_guess),
            inputs.hub_diameter,
            float64(0.2),
            bounds=[
                0.4 * compressor_geometry.outer_diameter,
                0.6 * compressor_geometry.outer_diameter,
            ],
        )

        compressor_geometry.inlet_tip_diameter = float(tip_diameter)
        setattr(inlet_loop_collector, "tip_diameter", tip_diameter)

        inlet_flow_area = pi / 4.0 * (tip_diameter**2 - inputs.hub_diameter**2)  # [m^2]

        V.magnitude = inputs.mass_flow_rate / (static_density_guess * inlet_flow_area)  # [m/s]
        V.angle = 0.0
        V.CalculateComponentsWithMagnitudeAndAngle()

        T.static = T.total - V.magnitude**2 / (2 * fluid.specific_heat)  # [K]
        setattr(inlet_loop_collector, "static temperature", T.static)

        mach_number = V.magnitude / sqrt(
            fluid.specific_ratio * fluid.specific_gas_constant * T.static
        )  # []

        P.static = P.total / (1 + (fluid.specific_ratio - 1) / 2 * mach_number**2) ** (
            fluid.specific_ratio / (fluid.specific_ratio - 1)
        )  # [Pa]
        setattr(inlet_loop_collector, "static pressure", P.static)

        rho.static = P.static / (fluid.specific_gas_constant * T.static)  # [kg/m^3]

        density_residual = abs(rho.static - static_density_guess) / static_density_guess
        setattr(inlet_loop_collector, "density residual", density_residual)

        if IsInletLoopConverged(density_residual, tolerance, iteration, inlet_loop_collector):
            break

        if iteration == max_iterations:
            setattr(
                inlet_loop_collector,
                "converge_message",
                f"{Fore.YELLOW}WARNING: Max iterations reached",
            )

        # Reset Density
        static_density_guess = rho.static

    rho.static = P.static / (fluid.specific_gas_constant * T.static)

    # [I]:Output
    # result.mach_number = M1  # []    Absolute Mach number
    # result.inlet_flow_area = S1  # [m^2] Inlet flow area

    inlet_loop_collector.Print()
    blade = ThreeDimensionalBlade(_mid=VelocityTriangle(_absolute=V))
    inlet_thermo_point = ThermoPoint(pressure=P, density=rho, temperature=T)
    inlet = CompressorStage(
        thermodynamic_point=inlet_thermo_point, blade=blade, flow_area=inlet_flow_area
    )

    return inlet
