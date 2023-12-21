"""
Author: Alejandro Valencia
Update: 30 April, 2023
"""


from ccpd.data_types.thermo_point import ThermoPoint
from ccpd.data_types.three_dimensional_blade import ThreeDimensionalBlade
from ccpd.data_types.centrifugal_compressor_geometry import CompressorGeometry
from dataclasses import dataclass, field


@dataclass
class CompressorStage:
    """
    Compressor stage class data type
    """

    _thermodynamic_point: ThermoPoint = field(default_factory=lambda: ThermoPoint())
    _blade: ThreeDimensionalBlade = field(default_factory=lambda: ThreeDimensionalBlade())
    _flow_area: float = 0.0

    @property
    def thermodynamic_point(self) -> ThermoPoint:
        return self._thermodynamic_point

    @property
    def blade(self) -> ThreeDimensionalBlade:
        return self._blade

    @property
    def flow_area(self) -> float:
        return self._flow_area


@dataclass
class CentrifugalCompressor:
    """
    Final centrifugal compressor class data type
    """

    total_efficiency: float = 0.0
    total_compression_ratio: float = 0.0
    impeller_compression_ratio: float = 0.0
    inlet_tip_to_outlet_diameter_ratio: float = 0.0
    inlet_hub_to_tip_diameter_ratio: float = 0.0
    diameter_safety_factor: float = 0.0
    final_eulerian_work: float = 0.0
    net_power: float = 0.0
    diffusion_ratio: float = 0.0
    de_haller_number: float = 0.0
    lieblien_diffusion_factor: float = 0.0
    stage_loading: float = 0.0
    flow_coefficient: float = 0.0
    blade_orientation_ratio: float = 0.0

    inlet: CompressorStage = CompressorStage()
    outlet: CompressorStage = CompressorStage()
    vaneless_diffuser: CompressorStage = CompressorStage()
    diffuser: CompressorStage = CompressorStage()

    geometry = CompressorGeometry()
