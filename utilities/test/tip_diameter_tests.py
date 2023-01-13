"""
Author: Alejandro Valencia
Update: 11 December, 2022
"""

import unittest
from ccpd.utilities.tip_diameter import ComputeTipDiameter


class TestComputeTipDiameter(unittest.TestCase):
    def TestGivenValidFunctionAndValidBounds__ExpectValidSolution(self):
        # Given
        function = lambda x: x * (x - 1)

        # Call
        result = ComputeTipDiameter(function)

        # Expect
        self.assertEqual(result, 0.6)
