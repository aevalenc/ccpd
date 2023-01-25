"""
Author: Alejandro Valencia
Update: 24 January, 2022
"""

import unittest
from ccpd.utilities.tip_diameter import ComputeTipDiameter
from scipy.optimize import Bounds


class TestComputeTipDiameter(unittest.TestCase):
    def test_given_valid_inputs_expect_valid_results(self):
        # Given
        rotational_speed = 40.0
        mass_flow_rate = 5.0
        density = 0.125
        hub_diameter = 0.35
        initial_guess = 0.4
        bounds = [0.4, 0.6]

        # Call
        result = ComputeTipDiameter(
            rotational_speed,
            mass_flow_rate,
            density,
            hub_diameter,
            initial_guess,
            bounds,
        )

        # Expect
        self.assertAlmostEqual(result, 0.6, 3)


if __name__ == "__main__":
    unittest.main()
