""" 
Author: Alejandro Valencia
Centrifugal Compressor Preliminary Design
Remaining Inlet Calculations
Update: October 28, 2023
"""

from ccpd.data_types.centrifugal_compressor import CompressorGeometry, CompressorStage
from ccpd.data_types.three_dimensional_blade import VelocityTriangle
from ccpd.data_types.working_fluid import WorkingFluid
import numpy as np

"""
@brief This function takes initial design parameters and calculates the remaining inlet values.

@param working_fluid_specific_ratio: specific ratio for the fluid
@param working_fluid_specific_gas_constant: specific gas constant for the fluid
@param inlet_total_temperature: total temperature at the inlet midspan of the blade
"""


def SanityChecks(
    working_fluid_specific_ratio: float,
    working_fluid_specific_gas_constant: float,
    working_fluid_specific_heat: float,
    inlet_total_temperature: float,
):
    assert not np.isclose(working_fluid_specific_ratio, 0.0), f"[Error]: Specific ratio not set!"

    assert not np.isclose(
        working_fluid_specific_gas_constant, 0.0
    ), f"[Error]: Specific gas constant not set!"

    assert not np.isclose(working_fluid_specific_heat, 0.0), f"[Error]: Specific heat not set!"

    assert not np.isclose(
        inlet_total_temperature, 0.0
    ), f"[Error]: Inlet total temperature not set!"


def CalculateRemainingInletQuantities(
    inlet: CompressorStage,
    working_fluid: WorkingFluid,
) -> None:
    """
    We have calculated V1 @ the tip. Then assuming a free vortex
      method, the hub and tip velocity triangles can be
      caluclated.
    """

    SanityChecks(
        working_fluid.specific_ratio,
        working_fluid.specific_gas_constant,
        working_fluid.specific_heat,
        inlet.thermodynamic_point.temperature.total,
    )

    # [m/s]: Speed of sound
    speed_of_sound_at_inlet = np.sqrt(
        working_fluid.specific_ratio
        * working_fluid.specific_gas_constant
        * inlet.thermodynamic_point.temperature.total
    )
    inlet.thermodynamic_point.speed_of_sound = speed_of_sound_at_inlet

    # []:Mach Numbers
    mid_absolute_mach_number = inlet.blade.mid.absolute.magnitude / speed_of_sound_at_inlet
    inlet.blade.mid_mach_number.absolute = mid_absolute_mach_number

    # Relative Mach Number
    inlet.blade.hub_mach_number.relative = (
        inlet.blade.hub.relative.magnitude / speed_of_sound_at_inlet
    )
    inlet.blade.mid_mach_number.relative = (
        inlet.blade.mid.relative.magnitude / speed_of_sound_at_inlet
    )
    inlet.blade.tip_mach_number.relative = (
        inlet.blade.tip.relative.magnitude / speed_of_sound_at_inlet
    )

    # []:Static Temperature at Midspan
    inlet.thermodynamic_point.temperature.static = (
        inlet.thermodynamic_point.temperature.total
        - inlet.blade.mid.absolute.magnitude**2 / (2 * working_fluid.specific_heat)
    )
