""" 
  Author: Alejandro Valencia
  Centrifugal Compressor Preliminary Design
  Inlet Iteration Loop
  Update: 24 July, 2020
"""

from scipy import optimize

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


def ComputeTipDiameter(function) -> float:
    # function = lambda x: x * (x - 1)
    return optimize.minimize(function, bounds=[0.4, 0.6])
