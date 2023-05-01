""" 
  Author: Alejandro Valencia
  Centrifugal Compressor Preliminary Design
  Minimize tip diameter
  Update: 28 January, 2023
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
    rotational_speed: np.float64,
    mass_flow_rate: np.float64,
    density: np.float64,
    hub_diameter: np.float64,
    initial_guess: np.float64,
    bounds: list,
) -> np.float64:

    assert not isinstance(rotational_speed, complex), (
        f"ERROR: rotational speed is immaginary" + f", is isentropic work positive?"
    )

    function = lambda tip_diameter, *args: (
        args[0] ** 2 * (tip_diameter**2 / 4.0)
        + (args[1] / (args[2] * np.pi / 4 * (tip_diameter**2 - args[3] ** 2))) ** 2
    )

    Bounds = optimize.Bounds(bounds[0], bounds[1])

    # TODO: create a minimization function to reduce the overkill of scipy's optimize.minimize
    result = optimize.minimize(
        function,
        initial_guess,
        args=(rotational_speed, mass_flow_rate, density, hub_diameter),
        bounds=Bounds,
    )

    return result.x[0]
