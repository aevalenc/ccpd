"""
  Input parameters

  The following are inputs for the prelimiary design calculations:
              Ds    : Specific diameter
             Oms   : Specific Speed
             eta_tt: Baseline end to end efficiency
             fluid : Working fluid for the machine
             mat   : Compressor material
"""

import numpy as np


class ThreeDimensionalBlade:
    """
    3D blade geometry
    """

    def __init__(self) -> None:
        self.hub = VelocityTriangle()
        self.mid = VelocityTriangle()
        self.tip = VelocityTriangle()


class VelocityTriangle:
    """
    Velocity Triangle class is composed of an axial and tangential
    component along with the vector magnitude and orientation in a global
    reference coordinate frame
    """

    def __init__(self) -> None:
        self.axial = 0.0
        self.tangential = 0.0
        self.magnitude = 0.0
        self.angle = 0.0

    def CalculateMagnitudeWithComponents(self) -> None:
        self.magnitude = np.sqrt(np.square(self.axial) + np.square(self.tangential))

    def CalculateComponentsWithMagnitudeAndAngle(self) -> None:
        self.axial = self.magnitude * np.cos(self.angle)
        self.tangential = self.magnitude * np.sin(self.angle)
