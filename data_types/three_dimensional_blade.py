"""
    Author: Alejandro Valencia
    Update: 30 April, 2023
    Blade related classes
"""

from dataclasses import dataclass
import numpy as np
from ccpd.data_types.centrifugal_compressor_geometry import CompressorGeometry


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
        self.angle = np.arctan2(self.tangential, self.axial)

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


@dataclass
class ThreeDimensionalBlade:
    hub: VelocityTriangle = VelocityTriangle()
    mid: VelocityTriangle = VelocityTriangle()
    tip: VelocityTriangle = VelocityTriangle()

    def CalculateComponentsViaFreeVortexMethod(
        self, compressor_geometry: CompressorGeometry, rotational_speed: float
    ):
        """
        We have calculated V1 @ the tip. Then assuming a free vortex
        method, the hub and tip velocity triangles can be
        caluclated.
        """
        assert not self.tip is None, "Tip velocity triangle is not set"
        assert not self.mid is None, "Mid velocity triangle is not set"
        assert not self.hub is None, "Hub velocity triangle is not set"

        # []:Translational Velocity
        self.tip.translational.magnitude = rotational_speed * (
            compressor_geometry.inlet_tip_diameter / 2.0
        )

        self.mid.translational.magnitude = rotational_speed * (
            compressor_geometry.inlet_mid_diameter / 2.0
        )

        self.hub.translational.magnitude = rotational_speed * (
            compressor_geometry.inlet_hub_diameter / 2.0
        )

        # Relative Velocity Components & Magnitude
        self.hub.relative.tangential = (
            self.mid.absolute.tangential - self.hub.translational.magnitude
        )
        self.hub.relative.axial = self.mid.absolute.axial
        self.hub.relative.CalculateMagnitudeWithComponents()

        self.mid.relative.tangential = (
            self.mid.absolute.tangential - self.mid.translational.magnitude
        )
        self.mid.relative.axial = self.mid.absolute.axial
        self.mid.relative.CalculateMagnitudeWithComponents()

        self.tip.relative.tangential = (
            self.mid.absolute.tangential - self.tip.translational.magnitude
        )
        self.tip.relative.axial = self.mid.absolute.axial
        self.tip.relative.CalculateMagnitudeWithComponents()
