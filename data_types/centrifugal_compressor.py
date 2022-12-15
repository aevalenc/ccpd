"""
  Author: Alejandro Valencia
  Update: 11 December, 2022
"""

from ccpd.data_types.thermo_point import ThermoPoint
from ccpd.data_types.velocity_triangle import ThreeDimensionalBlade


class CompressorStage:
    """
    Compressor stage class data type
    """

    def __init__(self) -> None:
        self.thermodynamic_point = ThermoPoint()
        self.blade = ThreeDimensionalBlade()


class CompressorGeometry:
    """
    Compressor geometry class data type:
    """

    def __init__(self) -> None:
        self.number_of_blades = 0
        self.hub_diameter = 0.0
        self.inner_diameter = 0.0
        self.outer_diameter = 0.0


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

        self.inlet = CompressorStage()
        self.outlet = CompressorStage()
        self.diffuser = CompressorStage()

        self.geometry = CompressorGeometry()
