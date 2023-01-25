""" 
  Author: Alejandro Valencia
  Centrifugal Compressor Preliminary Design
  Inlet Iteration Loop
  Update: 24 July, 2020
"""

from scipy import optimize
import numpy as np

#
# This function takes initial design parameters and calculates the inlet
#  tip diameter minimizing the relative velocity function. This comes
# 	from the fact that for a centrifugal compressor we want to minimize
# 	the relative Mach number. MATLAB's built in optimization function
# 	fmincon is utilized.
#
#      The following are inputs:
#
#          mdot  : The inlet mass flow rate
#          rho   : Inlet density
#          Dhub  : Hub diameter
#          w     : rotational speed
#          Dlimit: Max diameter limit
#
#      The following are outputs:
#
#          Dtip: Inlet tip diameter
#


def ComputeTipDiameter(
    rotational_speed: float,
    mass_flow_rate: float,
    density: float,
    hub_diameter: float,
    initial_guess: float,
    bounds: list,
) -> float:
    # function = lambda x, *args: x * (x - args[0])
    function = lambda tip_diameter, *args: (
        args[0] ** 2 * (tip_diameter**2 / 4.0)
        + (args[1] / (args[2] * np.pi / 4 * (tip_diameter**2 - args[3] ** 2))) ** 2
    )

    Bounds = optimize.Bounds(bounds[0], bounds[1])

    result = optimize.minimize(
        function,
        initial_guess,
        args=(rotational_speed, mass_flow_rate, density, hub_diameter),
        bounds=Bounds,
    )

    return result.x[0]
