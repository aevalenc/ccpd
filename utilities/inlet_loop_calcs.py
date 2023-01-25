""" 
  Author: Alejandro Valencia
  Centrifugal Compressor Preliminary Design
  Inlet Iteration Loop
  Update: 24 January, 2023
"""

from ccpd.data_types.centrifugal_compressor import CompressorStage
from ccpd.data_types.velocity_triangle import VelocityTriangle, ThreeDimensionalBlade
from ccpd.data_types.thermo_point import ThermodynamicVariable, ThermoPoint
from ccpd.data_types.inputs import Inputs
from ccpd.data_types.working_fluid import WorkingFluid
from ccpd.utilities.tip_diameter import ComputeTipDiameter
from numpy import pi, sqrt
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


def inlet_loop(
    inputs: Inputs,
    fluid: WorkingFluid,
    static_density_guess: float,
    rotational_speed: float,
    outer_diameter: float,
    max_iterations: int,
    tolerance: float,
) -> CompressorStage:

    # global mdot PT1 TT1 cp Rh y
    # Quantities
    T = ThermodynamicVariable()
    P = ThermodynamicVariable()
    rho = ThermodynamicVariable()

    V = VelocityTriangle()

    # []:Optimization Loop
    for itr in range(0, max_iterations + 1):

        # [A]:Minimize Inlet Tip Diameter
        tip_diameter = ComputeTipDiameter(
            rotational_speed,
            inputs.mass_flow_rate,
            static_density_guess,
            inputs.hub_diameter,
            0.4,
            bounds=[0.4 * outer_diameter, 0.6 * outer_diameter],
        )
        print(f"{Fore.YELLOW}INFO:{Fore.RESET} Mock tip diameter {tip_diameter:.3}")
        # (
        # inputs.mass_flow_rate, static_density_guess, hub_diameter, D2, w
        # )  # [m]

        # [B]:Calculate Flow Inlet Area & Absolute Velocity
        S1 = pi / 4 * (tip_diameter ^ 2 - inputs.hub_diameter ^ 2)  # [m^2]
        V.magnitude = inputs.mass_flow_rate / (static_density_guess * S1)  # [m/s]
        V.angle = 0
        V.axial = V.magnitude
        V.tangential = 0

        # [C]:Static Temperature
        T.static = inputs.inlet_total_temperature - V.magnitude ^ 2 / (
            2 * fluid.specific_heat
        )  # [K]

        # [D]:Mach number
        M1 = V.magnitude / sqrt(
            fluid.specific_ratio * fluid.specific_gas_constant * T.static
        )  # []

        # [E]:Static Pressure
        P.static = P.total / (1 + (fluid.specific_ratio - 1) / 2 * M1 ^ 2) ^ (
            fluid.specific_ratio / (fluid.specific_ratio - 1)
        )  # [Pa]

        # [F]:Recalculate Density
        rho.static = P.static / (fluid.specific_gas_constant * T.static)  # [kg/m^3]

        # [G]:Check for Convergence
        density_residual = abs(rho - static_density_guess) / static_density_guess

        # if strcmp(monitor_residual,'yes') == 1
        #    fprintf('Iteration: d | Residual %0.6f\n', itr, density_residual)
        # end

        if density_residual < tolerance:
            print(
                f"Minimization problem converged in {itr} iterations w/ residual: {density_residual}\n"
            )
            break
        elif density_residual > 1e6:
            print("WARNING solution diverging")
            break

        # [H]:Reset Density
        static_density_guess = rho

    rho.static = P.static / (fluid.specific_gas_constant * T.static)

    # [I]:Output
    # result.tip_diameter = Dtip  # [m]   Tip diameter
    # result.T1 = T1  # [K]   Static Temperature
    # result.M1 = M1  # []    Absolute Mach number
    # result.P1 = P1  # [Pa]  Static Pressure
    # # result.V.mid = V1  # [m/s] Absolute velocity
    # result.S1 = S1  # [m^2] Inlet flow area
    # result.rho1 = rho1

    blade = ThreeDimensionalBlade(mid=V)
    inlet_thermo_point = ThermoPoint(pressure=P, density=rho, temperature=T)
    inlet = CompressorStage(thermodynamic_point=inlet_thermo_point, blade=blade)

    return inlet
