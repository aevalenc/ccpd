"""
    Author: Alejandro Valencia
    Update: 04 February, 2022
    Blade related classes
"""

from dataclasses import dataclass
import numpy as np


@dataclass
class VelocityVector:
    """
    Velocity Triangle class is composed of an axial and tangential
    component along with the vector magnitude and orientation in a global
    reference coordinate frame
    """

    axial: float = 0.0
    tangential: float = 0.0
    magnitude: float = 0.0
    angle: float = 0.0

    def __add__(self, other):
        return VelocityVector(
            self.axial + other.axial, self.tangential + other.tangential
        )

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

    absolute: VelocityVector = VelocityVector()
    relative: VelocityVector = VelocityVector()
    translational: VelocityVector = VelocityVector()

    # def __init__(
    #     self, absolute=VelocityVector(), mid=VelocityVector(), tip=VelocityVector()
    # ) -> None:
    #     self.hub = hub
    #     self.mid = mid
    #     self.tip = tip


@dataclass
class ThreeDimensionalBlade:
    hub: VelocityTriangle = VelocityTriangle()
    mid: VelocityTriangle = VelocityTriangle()
    tip: VelocityTriangle = VelocityTriangle()
