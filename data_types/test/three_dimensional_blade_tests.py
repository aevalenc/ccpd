"""
Author: Alejandro Valencia
Update: 30 April, 2023
"""

import unittest
from ccpd.data_types.centrifugal_compressor_geometry import CompressorGeometry
import ccpd.data_types.three_dimensional_blade as tdb
import numpy as np


class TestCalculateMagnitudeWithComponents(unittest.TestCase, tdb.VelocityVector):
    def test_given_valid_components_expect_valid_magnitude(self):
        # Given
        self.axial = 3.0
        self.tangential = 4.0

        # Call
        self.CalculateMagnitudeWithComponents()

        # Expect
        self.assertEqual(self.magnitude, 5.0)

    def test_no_two_given_valid_components_expect_valid_magnitude(self):
        # Given
        self.axial = -4.0
        self.tangential = 3.0

        # Call
        self.CalculateMagnitudeWithComponents()

        # Expect
        self.assertEqual(self.magnitude, 5.0)


class TestCalculateComponentsWithMagnitudeAndAngle(
    unittest.TestCase, tdb.VelocityVector
):
    def test_given_valid_magnitude_and_angle_expect_valid_components(self):
        # Given
        self.magnitude = 10.0
        self.angle = 60 * np.pi / 180.0

        # Call
        self.CalculateComponentsWithMagnitudeAndAngle()

        # Expect
        self.assertAlmostEqual(self.axial, 5.0)
        self.assertAlmostEqual(self.tangential, 5.0 * np.sqrt(3))


class TestCalculateComponentsViaFreeVortexMethod(unittest.TestCase):
    def setUp(self) -> None:
        self.blade = tdb.ThreeDimensionalBlade()
        return super().setUp()

    @staticmethod
    def CreateBasicCompressorGeometry() -> CompressorGeometry:
        compressor_geometry = CompressorGeometry()
        compressor_geometry.inlet_hub_diameter = 0.4
        compressor_geometry.inlet_tip_diameter = 0.6
        compressor_geometry.outer_diameter = 0.8
        return compressor_geometry

    @staticmethod
    def CreateBasicVelocityTriangleAtGivenPosition(
        component: str, velocity_vector: tdb.VelocityVector
    ) -> tdb.VelocityTriangle:
        velocity_triangle = tdb.VelocityTriangle()
        velocity_triangle.__setattr__(component, velocity_vector)
        return velocity_triangle

    def test_GivenValidInputs_ExpectBladeProperlyAssigned(self):
        # Given
        basic_compressor_geometry = self.CreateBasicCompressorGeometry()
        rotational_speed = 29.0

        absolute_velocity = tdb.VelocityVector(magnitude=5.0, angle=0.0)
        absolute_velocity.CalculateComponentsWithMagnitudeAndAngle()
        self.blade.__setattr__(
            "mid",
            self.CreateBasicVelocityTriangleAtGivenPosition(
                "absolute", absolute_velocity
            ),
        )

        # Call
        self.blade.CalculateComponentsViaFreeVortexMethod(
            basic_compressor_geometry, rotational_speed
        )

        # Expect
        self.assertAlmostEqual(self.blade.mid.absolute.axial, 5.0, delta=0.001)
        self.assertAlmostEqual(self.blade.hub.relative.axial, 5.0, delta=0.001)


if __name__ == "__main__":
    unittest.main()
