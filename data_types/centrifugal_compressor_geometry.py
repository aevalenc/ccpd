"""
  Author: Alejandro Valencia
  Update: 05 Febraury, 2022
"""

import numpy as np


class CompressorGeometry:
    """
    Compressor geometry class data type:
    """

    # TODO: Consider using slots to preallocate class members
    number_of_blades = 0

    inlet_hub_diameter = 0.0
    inlet_mid_diameter = 0.0
    inlet_tip_diameter = 0.0
    inlet_blade_height = 0.0
    inlet_blade_ratio = 0.0

    outer_diameter = 0.0
    outlet_blade_height = 0.0
    outer_blade_height_ratio = 0.0

    def CalculateInletBladeHeightAndRatios(self):
        assert not np.isclose(
            self.inlet_hub_diameter, 0.0
        ), f"Error: hub diameter not not set"

        assert np.greater(
            self.inlet_tip_diameter, self.inlet_hub_diameter
        ), f"Error: tip diameter not greater than hub diameter"

        assert not np.isclose(
            self.outer_diameter, 0.0
        ), f"Error: outer diameter not set"

        self.inlet_blade_height = (
            self.inlet_tip_diameter - self.inlet_hub_diameter
        ) / 2.0
        self.inlet_mid_diameter = (
            self.inlet_tip_diameter + self.inlet_hub_diameter
        ) / 2.0

        self.inlet_blade_ratio = self.inlet_hub_diameter / self.inlet_tip_diameter
        self.outer_blade_height_ratio = self.inlet_tip_diameter / self.outer_diameter
