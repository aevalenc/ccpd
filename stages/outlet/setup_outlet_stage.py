"""
Author: Alejandro Valencia
Update: October 14, 2023
"""

from ccpd.data_types.centrifugal_compressor import CompressorStage
from ccpd.data_types.thermo_point import ThermoPoint, ThermodynamicVariable
from ccpd.data_types.three_dimensional_blade import (
    MachTriangle,
    ThreeDimensionalBlade,
    VelocityTriangle,
    VelocityVector,
)
from ccpd.data_types.inputs import Inputs
from ccpd.data_types.working_fluid import WorkingFluid
import numpy as np


def SetupOutletStage(
    alpha2: float,
    eulerian_work: float,
    outlet_translational_velocity: VelocityVector,
    inputs: Inputs,
    working_fluid: WorkingFluid,
) -> CompressorStage:
    """
    Recall that we do not know any of our flow angles at the exit of the
    impeller. So the outlet absolute flow angle is assumed
    to fix the velocity triangle.

    The following are inputs:

                alpha2: Absolute outlet flow angle
                eulerian_work: Eulerian work
                outlet_translational_velocity: Outer peripheral speed

    The following are outputs

                outlet: Structure containing velocity components and Non-
                    isentropic temperature
    """
    # Velocity Triangles
    outlet_absolute_velocity = VelocityVector()
    outlet_relative_velocity = VelocityVector()

    # Absolute Velocity
    outlet_absolute_velocity.angle = alpha2
    outlet_absolute_velocity.tangential = eulerian_work / outlet_translational_velocity.magnitude
    outlet_absolute_velocity.magnitude = outlet_absolute_velocity.tangential / (np.sin(alpha2))
    outlet_absolute_velocity.axial = outlet_absolute_velocity.magnitude * np.cos(alpha2)

    # Relative Velocity
    outlet_relative_velocity.tangential = (
        outlet_absolute_velocity.tangential - outlet_translational_velocity.magnitude
    )
    outlet_relative_velocity.axial = outlet_absolute_velocity.axial
    outlet_relative_velocity.angle = np.arctan(
        outlet_relative_velocity.tangential / outlet_relative_velocity.axial
    )
    outlet_relative_velocity.magnitude = np.sqrt(
        outlet_relative_velocity.tangential**2 + outlet_relative_velocity.axial**2
    )

    # Total & Static Temperature
    # These are the real values of the temperature considering a non-
    #   isentropic process. The irreversibility is included in the
    #   end to end efficiency assumed at the beginning of the
    #   calculations
    temperature = ThermodynamicVariable()
    temperature.total = inputs.inlet_total_temperature + (
        eulerian_work / working_fluid.specific_heat
    )
    temperature.static = temperature.total - (
        outlet_absolute_velocity.magnitude**2 / (2 * working_fluid.specific_heat)
    )

    # Mach Numbers
    absolute_mach_number = outlet_absolute_velocity.magnitude / np.sqrt(
        temperature.static * working_fluid.specific_ratio * working_fluid.specific_gas_constant
    )
    relative_mach_number = outlet_relative_velocity.magnitude / np.sqrt(
        temperature.static * working_fluid.specific_ratio * working_fluid.specific_gas_constant
    )
    translational_mach_number = outlet_translational_velocity.magnitude / np.sqrt(
        temperature.static * working_fluid.specific_ratio * working_fluid.specific_gas_constant
    )

    # Setup three dimensional blade
    mid_velocity = VelocityTriangle(
        outlet_absolute_velocity,
        outlet_relative_velocity,
        outlet_translational_velocity,
    )
    mid_mach_triangle = MachTriangle(
        absolute_mach_number, relative_mach_number, translational_mach_number
    )
    blade = ThreeDimensionalBlade(_mid=mid_velocity, _mid_mach_number=mid_mach_triangle)

    return CompressorStage(ThermoPoint(_temperature=temperature), blade)
