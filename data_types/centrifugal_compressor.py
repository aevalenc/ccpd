"""
  Author: Alejandro Valencia
  Update: 24 January, 2022
"""

from ccpd.data_types.thermo_point import ThermoPoint
from ccpd.data_types.velocity_triangle import ThreeDimensionalBlade
import numpy as np


class CompressorStage:
    """
    Compressor stage class data type
    """

    def __init__(
        self, thermodynamic_point=ThermoPoint(), blade=ThreeDimensionalBlade()
    ) -> None:
        self.thermodynamic_point = thermodynamic_point
        self.blade = blade


class CompressorGeometry:
    """
    Compressor geometry class data type:
    """

    # TODO: Consider using slots to preallocate class members
    def __init__(self) -> None:
        self.number_of_blades = 0

        self.inlet_hub_diameter = 0.0
        self.inlet_mid_diameter = 0.0
        self.inlet_tip_diameter = 0.0
        self.inlet_blade_height = 0.0
        self.inlet_blade_ratio = 0.0

        self.outer_diameter = 0.0
        self.outlet_blade_height = 0.0
        self.outer_blade_height_ratio = 0.0

    def CalculateInletBladeHeightAndRatios(self):
        assert (np.greater(self.inlet_hub_diameter, 0.0)) and (
            np.greater(self.inlet_tip_diameter, self.inlet_hub_diameter)
        ), f"Error: hub diameter not greater than tip diameter"

        assert np.greater(self.outer_diameter, 0.0), f"Error: outer diameter not set"

        self.inlet_blade_height = (
            self.inlet_tip_diameter - self.inlet_hub_diameter
        ) / 2.0
        self.inlet_mid_diameter = (
            self.inlet_tip_diameter + self.inlet_hub_diameter
        ) / 2.0

        self.inlet_blade_ratio = self.inlet_hub_diameter / self.inlet_tip_diameter
        self.outer_blade_height_ratio = self.inlet_tip_diameter / self.outer_diameter


class CentrifugalCompressor:
    """
    Final centrifugal compressor class data type
    """

    def __init__(self) -> None:
        self.total_efficiency = 1.0
        self.total_compression_ratio = 2.0
        self.inlet_tip_to_outlet_diameter_ratio = 0.5
        self.inlet_hub_to_tip_diameter_ratio = 0.5
        self.diameter_safety_factor = 0.5
        self.final_eulerian_work = 0.5
        self.net_power = 0.5
        self.diffusion_ratio = 0.5
        self.de_haller_number = 0.5
        self.lieblien_diffusion_factor = 0.5
        self.stage_loading = 0.5
        self.flow_coefficient = 0.5
        self.blade_orientation_ratio = 0.5

        self.inlet = CompressorStage()
        self.outlet = CompressorStage()
        self.diffuser = CompressorStage()

        self.geometry = CompressorGeometry()
