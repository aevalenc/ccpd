"""
Author: Alejandro Valencia
Update: 11 December, 2022
"""

import unittest
import ccpd.data_types.velocity_triangle as vt
import numpy as np


class TestCalculateMagnitudeWithComponents(unittest.TestCase, vt.VelocityTriangle):
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
    unittest.TestCase, vt.VelocityTriangle
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


if __name__ == "__main__":
    unittest.main()
