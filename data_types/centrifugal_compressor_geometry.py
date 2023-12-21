"""
  Author: Alejandro Valencia
  Update: 05 Febraury, 2022
"""

import numpy as np
from dataclasses import dataclass
from attrs import define


@dataclass
class DiameterStruct:
    hub: float = 0.0
    mid: float = 0.0
    tip: float = 0.0


@define
class CompressorGeometry:
    """
    Compressor geometry class data type:
    """

    # TODO: Consider using slots to preallocate class members
    number_of_blades: int = 0

    inlet_hub_diameter: float = 0.0
    inlet_mid_diameter: float = 0.0
    inlet_tip_diameter: float = 0.0
    inlet_blade_height: float = 0.0
    inlet_blade_ratio: float = 0.0

    outer_diameter: float = 0.0
    outlet_blade_height: float = 0.0
    outer_blade_height_ratio: float = 0.0

    vaneless_diffuser_diameter: float = 0.0
    diffuser_diameter: float = 0.0

    def CalculateInletBladeHeightAndRatios(self):
        assert not np.isclose(self.inlet_hub_diameter, 0.0), f"Error: hub diameter not not set"

        assert np.greater(
            self.inlet_tip_diameter, self.inlet_hub_diameter
        ), f"Error: tip diameter not greater than hub diameter"

        assert not np.isclose(self.outer_diameter, 0.0), f"Error: outer diameter not set"

        self.inlet_blade_height = (self.inlet_tip_diameter - self.inlet_hub_diameter) / 2.0
        self.inlet_mid_diameter = (self.inlet_tip_diameter + self.inlet_hub_diameter) / 2.0

        self.inlet_blade_ratio = self.inlet_hub_diameter / self.inlet_tip_diameter
        self.outer_blade_height_ratio = self.inlet_tip_diameter / self.outer_diameter
