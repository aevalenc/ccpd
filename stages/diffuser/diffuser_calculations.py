"""
Author: Alejandro Valencia
Centrifugal Compressor Preliminary Design
Diffuser Calculations
Update: January 3, 2024
"""
import numpy as np
from ccpd.data_types.centrifugal_compressor import CompressorStage
from ccpd.data_types.thermo_point import ThermoPoint, ThermodynamicVariable
from ccpd.data_types.three_dimensional_blade import (
    MachTriangle,
    ThreeDimensionalBlade,
    VelocityTriangle,
    VelocityVector,
)
from ccpd.data_types.working_fluid import WorkingFluid
import logging

logger = logging.getLogger(__name__)


def diffuser_calcs(
    outlet_temperature_struct: ThermodynamicVariable,
    outlet_pressure_struct: ThermodynamicVariable,
    working_fluid: WorkingFluid,
    inlet_total_temperature: float,
    inlet_total_pressure: float,
    isentropic_exponent: float,
    eulerian_work: float,
) -> tuple[CompressorStage, float, float]:
    """
    This function calculates the thermodynamic quantities of the wedge
    diffuser. Theory tells us that max efficiency occurs at a divergence
    angle (2 times theta) between 8 and 10 degrees.

    The following is the input:

        design: Current design with vanless diffuser

    The following is the output

        result: Final design with wedge diffuser
    """

    ## []:Grab Required Values From Design
    TT3 = outlet_temperature_struct.total
    T3 = outlet_temperature_struct.static
    PT3 = outlet_pressure_struct.total
    P3 = outlet_pressure_struct.static

    ## []:Choose Values
    # We start the diffuser design process by choosing certain geometric
    #   parameters. Aungier, in his book, has a table of various diffuser
    # 	specifications. For packaging's sake, the smallest length to width
    # 	ratio was chosen with a divergence angle between 8 and 10 degrees.
    # 	In addition, the coefficient of pressure recovery is given for
    # 	this diffuser. The aspect ratio was taken to be 1 for simplicity.
    LWR = 8.43  # Length to width ratio for the vaned diffuser
    theta = 9.49 / 2  # [deg] Half total divergence angle
    AS = 1  # Channel aspect ratio
    prc = 0.62  # Pressure recovery coefficient
    diffuser_efficiency = 0.87  # Diffuser efficiency corresponding to a 2theta = 8 [deg]

    ## []:Thermodynamic Values
    # Because the diffuser is a stationary flow passage there is no work
    #   done to the fluid. Thus, the total temperature remains constant
    #   resulting in:
    #
    #       h03 = h04
    #       TT3 = TT4

    T4 = ThermodynamicVariable()
    P4 = ThermodynamicVariable()
    rho4 = ThermodynamicVariable()

    T4.total = TT3  # [K]  Total temperature
    P4.static = prc * (PT3 - P3) + P3  # [Pa] Static pressure
    T4is = T3 * (P4.static / P3) ** isentropic_exponent  # [K]  Isentropic static temperature
    T4.static = T3 + (T4is - T3) / diffuser_efficiency  # [K]  Real static temperature
    rho4.static = P4.static / (working_fluid.specific_gas_constant * T4.static)  # [kg/m^3] Density

    ## [.1]:Losses
    # Looking at a Mollier diagram for points 3 to 4, we notice that the
    #   difference in enthalpy is given by the real value minus the
    #   isentropic one. Thus, our enthalpy loss is given by:
    #
    #       dhloss = h4 - h4is
    # -OR-
    #       dhloss = cp(T4 - T4is)
    dhloss = working_fluid.specific_heat * (T4.static - T4is)  # [J/kg] Enthaply drop
    logger.debug(f"Enthalpy drop: {dhloss:0.6}")

    ## [.2]:Continue with remaining thermodynamic values
    TT4is = T4.total - dhloss / working_fluid.specific_heat  # [K]  Isentropic total temperature
    P4.total = P4.static * (TT4is / T4.static) ** (
        working_fluid.specific_ratio / (working_fluid.specific_ratio - 1)
    )  # [Pa] Total pressure

    ## []:Velocity
    # Velocity at the outlet can be derived from the total temperature. The
    #   total temperature is the sum of the static temperature plus
    #   V^2/(2cp)
    V4 = np.sqrt(2 * working_fluid.specific_heat * (T4.total - T4.static))
    M4 = V4 / (working_fluid.specific_ratio * T4.static)
    logger.debug(f"Diffuser velocity magnitude: {V4:0.6}")
    logger.debug(f"Diffuser Mach Number: {M4:0.6}")

    ## []:Final End to End Efficiency
    # Calculate total isentropic enthalpy change [J/kg], then divide by the
    #   Eulerian work of our compressor
    Be = P4.total / inlet_total_pressure
    htis = working_fluid.specific_heat * inlet_total_temperature * (Be**isentropic_exponent - 1)
    eta_tt = htis / eulerian_work

    logger.debug(f"Isentropic enthalpy drop: {htis:0.6}")
    logger.info(f"End to end pressure ratio: {Be:0.3} | End to end efficiency: {eta_tt:0.3f}")

    diffuser = CompressorStage(
        _thermodynamic_point=ThermoPoint(_pressure=P4, _density=rho4, _temperature=T4),
        _blade=ThreeDimensionalBlade(_mid=VelocityTriangle(_absolute=VelocityVector(_magnitude=V4))),
    )

    ## []:Output
    # design.diff.T4     = T4;            # [K]      Real static temperature
    # design.diff.T4is   = T4is;          # [K]      Isentropic static temperature
    # design.diff.TT4    = TT4;           # [K]      Real total temperature
    # design.diff.TT4is  = TT4is;         # [K]      Isentropic total tempertature
    # design.diff.P4     = P4;            # [Pa]     Static pressure
    # design.diff.PT4    = PT4;           # [Pa]     Total pressure
    # design.diff.V4     = V4;            # [m/s]    Outlet velocity
    # design.diff.M4     = M4;            # []       Absolute Mach number
    # design.diff.rho4   = rho4;          # [kg/m^3] Density
    # design.diff.Nb     = 6;             # []       Number of diffuser channels
    # design.diff.dhloss = dhloss;        # [J/kg]   Enthalpy loss
    # design.diff.htis   = htis;          # [J/kg]   End to end enthalpy change
    # design.diff.eta_tt = eta_tt;        # []       End to end efficiency
    # design.diff.LWR    = LWR;           # []       Diffuser channel length to width ratio
    # design.diff.dvang  = 2 * theta;     # [deg]    Total divergence angle
    # design.diff.W      = AS * b3;       # [m]      Diffuser channel width
    # design.diff.Be     = Be;            # []       End to end pressure ratio

    return diffuser, Be, eta_tt
