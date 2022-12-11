"""
  Author: Alejandro Valencia
  Update: 11 December, 2022
"""

from data_types.thermo_point import ThermoPoint
from data_types.velocity_triangle import VelocityTriangle


class CompressorStage:
    """
    Compressor stage class data type
    """

    __thermodynamic_values = ThermoPoint()
    __velocity_triangle = VelocityTriangle()


class CentrifugalCompressor:
    """
    Final centrifugal compressor class data type
    """

    __efficiency = 0.9

    __inlet = CompressorStage()
    __outlet = CompressorStage()
    __diffuser = CompressorStage()
