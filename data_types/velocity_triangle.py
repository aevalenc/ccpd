"""
    Author: Alejandro Valencia
    Update: 11 December, 2022
    Blade related classes
"""

from dataclasses import dataclass
import numpy as np


class VelocityVector:
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

    def Print(self):
        print(
            f"Axial: {self.axial:.6}\n"
            + f"Tangential: {self.tangential}\n"
            + f"Magnitude: {self.magnitude}\n"
            + f"Angle: {self.angle}\n"
        )


@dataclass
class VelocityTriangle:
    """
    3D blade geometry
    """

    absolute: VelocityVector
    relative: VelocityVector
    translational: VelocityVector

    # def __init__(
    #     self, absolute=VelocityVector(), mid=VelocityVector(), tip=VelocityVector()
    # ) -> None:
    #     self.hub = hub
    #     self.mid = mid
    #     self.tip = tip
