"""
Author: Alejandro Valencia
Update: 4 February, 2023
"""

import unittest
import ccpd.data_types.centrifugal_compressor as cc
import numpy as np


class TestCentrifugalCompressorGeometryClass(unittest.TestCase):
    """
    Compressor Geometry Tests
    """

    def setUp(self) -> None:
        self.compressor_geometry = cc.CompressorGeometry()

    def test_GivenValidInputDiameters_ExpectValidRatios(self):
        # Given
        self.compressor_geometry.inlet_hub_diameter = 0.4
        self.compressor_geometry.inlet_tip_diameter = 0.6
        self.compressor_geometry.outer_diameter = 0.9

        # Call
        self.compressor_geometry.CalculateInletBladeHeightAndRatios()

        # Expect
        self.assertAlmostEqual(
            self.compressor_geometry.inlet_blade_ratio, 0.666, delta=0.001
        )

    def test_GivenInvalidInputHubDiameter_ExpectException(self):
        # Given
        self.compressor_geometry.inlet_tip_diameter = 0.6
        self.compressor_geometry.outer_diameter = 0.9

        # Expect
        with self.assertRaises(AssertionError):
            self.compressor_geometry.CalculateInletBladeHeightAndRatios(), "Error: hub diameter not not set"

    def test_GivenInvalidInputTipDiameter_ExpectException(self):
        # Given
        self.compressor_geometry.inlet_hub_diameter = 0.6
        self.compressor_geometry.outer_diameter = 0.9

        # Expect
        with self.assertRaises(AssertionError):
            self.compressor_geometry.CalculateInletBladeHeightAndRatios(),
            "Error: tip diameter not greater than hub diameter"

    def test_GivenInvalidOuterDiameter_ExpectException(self):
        # Given
        self.compressor_geometry.inlet_hub_diameter = 0.4
        self.compressor_geometry.inlet_tip_diameter = 0.6

        # Expect
        with self.assertRaises(AssertionError):
            self.compressor_geometry.CalculateInletBladeHeightAndRatios(), "Error: outer diameter not set"


if __name__ == "__main__":
    unittest.main()
