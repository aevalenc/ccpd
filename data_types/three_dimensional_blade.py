"""
    Author: Alejandro Valencia
    Update: 30 April, 2023
    Blade related classes
"""

from dataclasses import dataclass, field
import numpy as np
from ccpd.data_types.centrifugal_compressor_geometry import CompressorGeometry


@dataclass
class VelocityVector:
    """
    Velocity Triangle class is composed of an axial and tangential
    component along with the vector magnitude and orientation in a global
    reference coordinate frame
    """

    _axial: float = 0.0
    _tangential: float = 0.0
    _magnitude: float = 0.0
    _angle: float = 0.0

    @property
    def axial(self) -> float:
        return self._axial

    @property
    def tangential(self) -> float:
        return self._tangential

    @property
    def magnitude(self) -> float:
        return self._magnitude

    @property
    def angle(self) -> float:
        return self._angle

    @axial.setter
    def axial(self, value) -> None:
        self._axial = value

    @tangential.setter
    def tangential(self, value) -> None:
        self._tangential = value

    @magnitude.setter
    def magnitude(self, value) -> None:
        self._magnitude = value

    @angle.setter
    def angle(self, value) -> None:
        self._angle = value

    def __add__(self, other):
        return VelocityVector(self.axial + other.axial, self.tangential + other.tangential)

    def CalculateMagnitudeWithComponents(self) -> None:
        self.magnitude = np.sqrt(np.square(self.axial) + np.square(self.tangential))
        self.angle = np.arctan2(self.tangential, self.axial)

    def CalculateComponentsWithMagnitudeAndAngle(self) -> None:
        self.axial = self.magnitude * np.cos(self.angle)
        self.tangential = self.magnitude * np.sin(self.angle)

    # def __repr__(self):
    #     return (
    #         f"\nAxial: {self.axial:.6}\n"
    #         + f"Tangential: {self.tangential}\n"
    #         + f"Magnitude: {self.magnitude}\n"
    #         + f"Angle: {self.angle}\n"
    #     )


@dataclass
class VelocityTriangle:
    """
    3D blade geometry
    """

    _absolute: VelocityVector = field(default_factory=lambda: VelocityVector())
    _relative: VelocityVector = field(default_factory=lambda: VelocityVector())
    _translational: VelocityVector = field(default_factory=lambda: VelocityVector())

    @property
    def absolute(self) -> VelocityVector:
        return self._absolute

    @property
    def relative(self) -> VelocityVector:
        return self._relative

    @property
    def translational(self) -> VelocityVector:
        return self._translational

    @absolute.setter
    def absolute(self, value) -> None:
        self._absolute = value

    @relative.setter
    def relative(self, value) -> None:
        self._relative = value

    @translational.setter
    def translational(self, value) -> None:
        self._translational = value

    # def __repr__(self):
    #     return (
    #         f"\nAbsolute: {self.absolute}\n"
    #         + f"Relative: {self.relative}\n"
    #         + f"Translational: {self.translational}\n"
    #     )


@dataclass
class MachTriangle:
    _absolute: float = 0.0
    _relative: float = 0.0
    _translational: float = 0.0

    @property
    def absolute(self) -> float:
        return self._absolute

    @property
    def relative(self) -> float:
        return self._relative

    @property
    def translational(self) -> float:
        return self._translational

    @absolute.setter
    def absolute(self, value) -> None:
        self._absolute = value

    @relative.setter
    def relative(self, value) -> None:
        self._relative = value

    @translational.setter
    def translational(self, value) -> None:
        self._translational = value

    # def __repr__(self):
    #     return (
    #         f"\nAbsolute: {self.absolute:.6}\n"
    #         + f"Relative: {self.relative}\n"
    #         + f"Translational: {self.translational}\n"
    #     )


@dataclass
class ThreeDimensionalBlade:
    _hub: VelocityTriangle = field(default_factory=lambda: VelocityTriangle())
    _mid: VelocityTriangle = field(default_factory=lambda: VelocityTriangle())
    _tip: VelocityTriangle = field(default_factory=lambda: VelocityTriangle())
    _hub_mach_number: MachTriangle = field(default_factory=lambda: MachTriangle())
    _mid_mach_number: MachTriangle = field(default_factory=lambda: MachTriangle())
    _tip_mach_number: MachTriangle = field(default_factory=lambda: MachTriangle())

    @property
    def hub(self) -> VelocityTriangle:
        return self._hub

    @property
    def mid(self) -> VelocityTriangle:
        return self._mid

    @property
    def tip(self) -> VelocityTriangle:
        return self._tip

    @property
    def hub_mach_number(self) -> MachTriangle:
        return self._hub_mach_number

    @property
    def mid_mach_number(self) -> MachTriangle:
        return self._mid_mach_number

    @property
    def tip_mach_number(self) -> MachTriangle:
        return self._tip_mach_number

    def CalculateComponentsViaFreeVortexMethod(
        self, compressor_geometry: CompressorGeometry, rotational_speed: float
    ) -> None:
        """
        We have calculated V1 @ the tip. Then assuming a free vortex
        method, the hub and tip velocity triangles can be
        caluclated.
        """
        assert not self._tip is None, "Tip velocity triangle is not set"
        assert not self._mid is None, "Mid velocity triangle is not set"
        assert not self._hub is None, "Hub velocity triangle is not set"

        # []:Translational Velocity
        self._tip.translational._magnitude = rotational_speed * (
            compressor_geometry.inlet_tip_diameter / 2.0
        )

        self._mid.translational._magnitude = rotational_speed * (
            compressor_geometry.inlet_mid_diameter / 2.0
        )

        self._hub.translational._magnitude = rotational_speed * (
            compressor_geometry.inlet_hub_diameter / 2.0
        )

        # Relative Velocity Components & Magnitude
        self._hub.relative._tangential = (
            self._mid.absolute.tangential - self._hub.translational.magnitude
        )
        self._hub.relative._axial = self._mid.absolute.axial
        self._hub.relative.CalculateMagnitudeWithComponents()

        self._mid.relative._tangential = (
            self._mid.absolute.tangential - self._mid.translational.magnitude
        )
        self._mid.relative._axial = self._mid.absolute.axial
        self._mid.relative.CalculateMagnitudeWithComponents()

        self._tip.relative._tangential = (
            self._mid.absolute.tangential - self._tip.translational.magnitude
        )
        self._tip.relative._axial = self._mid.absolute.axial
        self._tip.relative.CalculateMagnitudeWithComponents()
