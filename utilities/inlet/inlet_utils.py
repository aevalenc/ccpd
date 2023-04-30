""" 
Author: Alejandro Valencia
Centrifugal Compressor Preliminary Design
Remaining Inlet Calculations
Update: 04 February, 2020
"""

from ccpd.data_types.centrifugal_compressor import CompressorGeometry, CompressorStage
from ccpd.data_types.three_dimensional_blade import VelocityTriangle
from ccpd.data_types.working_fluid import WorkingFluid
import numpy as np

"""
  This function takes initial design parameters and calculates the 
  	remaining inlet values.
 
  The following are inputs:
 
            inlet: Structure containing the inlet values after the 
  				   minimization problem
               inner_diameter: Structure containing the diameters (hub, mid, tip) for
                   the inlet 
                w: Rotational Speed
 
  The following are outputs:
 
            result: Structure containing the thermofluid properties at the
                    inlet
"""


def CalculateRemainingInletQuantities(
    inlet: CompressorStage,
    compressor_geometry: CompressorGeometry,
    rotational_speed: float,
    working_fluid: WorkingFluid,
):

    # global y Rh cp TT1 PT1

    # [E]:Remaining Inlet Quantites
    # [E.2]:Velocity Components, Magnitude, & Angle
    # We have calculated V1 @ the tip. Then assuming a free vortex
    #   method, the hub and tip velocity triangles can be
    #   caluclated.

    # []:Mach Numbers
    speed_of_sound_at_inlet = np.sqrt(
        working_fluid.specific_ratio
        * working_fluid.specific_gas_constant
        * inlet.thermodynamic_point.GetTemperature()
    )
    # [m/s]: Speed of sound

    # Absolute Mach Number
    mid_mach_number = inlet.blade.mid.absolute.magnitude / speed_of_sound_at_inlet
    # Relative Mach Number
    # M1w.hub = W1.hub.mag / speed_of_sound_at_inlet
    # M1w.mid = W1.mid.mag / speed_of_sound_at_inlet
    # M1w.tip = W1.tip.mag / speed_of_sound_at_inlet

    # # []:Temperature at Midspan
    # T1 = TT1 - V1.mid.mag ^ 2 / (2 * cp)
