"""
Author: Alejandro Valencia
Update: May 1, 2023
"""

import unittest
from ccpd.stages.inlet.tip_diameter import ComputeTipDiameter


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

    def test_given_immaginary_rotational_speed_expect_valid_results(self):
        # Given
        rotational_speed = 40.0j
        mass_flow_rate = 5.0
        density = 0.125
        hub_diameter = 0.35
        initial_guess = 0.4
        bounds = [0.4, 0.6]

        # Expect
        with self.assertRaises(AssertionError):
            ComputeTipDiameter(
                rotational_speed,
                mass_flow_rate,
                density,
                hub_diameter,
                initial_guess,
                bounds,
            )


if __name__ == "__main__":
    unittest.main()
