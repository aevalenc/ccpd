"""
Author: Alejandro Valencia
Update: 4 February, 2023
"""

import unittest
import ccpd.data_types.centrifugal_compressor as cc
import numpy as np


class TestCalculateMagnitudeWithComponents(unittest.TestCase, cc.CompressorGeometry):
    """
    Compressor Geometry Tests
    """

    def test_GivenValidInputDiameters_ExpectValidRatios(self):
        # Given
        self.inlet_hub_diameter = 0.4
        self.inlet_tip_diameter = 0.6
        self.outer_diameter = 0.9

        # Call
        self.CalculateInletBladeHeightAndRatios()

        # Expect
        self.assertAlmostEqual(self.inlet_blade_ratio, 0.666, delta=0.001)


if __name__ == "__main__":
    unittest.main()
