"""
Author: Alejandro Valencia
Update: 1 May, 2023
"""

from dataclasses import dataclass
import unittest
from ccpd.data_types.centrifugal_compressor import CompressorStage
from ccpd.data_types.centrifugal_compressor_geometry import CompressorGeometry
from ccpd.data_types.working_fluid import WorkingFluid
from ccpd.utilities.inlet.inlet_utils import CalculateRemainingInletQuantities


@dataclass
class MockInputs:
    """
    Class to mock inputs class for testing purposes
    """

    mass_flow_rate: float = 5.0
    inlet_total_pressure: float = 100000.0
    inlet_total_temperature: float = 298.0
    compression_ratio: float = 1.25
    surface_roughness: float = 0.003
    tip_clearance: float = 0.0001
    hub_diameter: float = 0.2


@dataclass
class MockWorkingFluid(WorkingFluid):
    """
    Class to mock WorkingFluid class for testing purposes
    """

    specific_heat: float = 1006.0
    specific_ratio: float = 1.4
    specific_gas_constant: float = 287.0
    kinematic_viscosity: float = 18.13e-6


def CreateBasicCompressorGeometry() -> CompressorGeometry:
    compressor_geometry = CompressorGeometry()
    compressor_geometry.inlet_hub_diameter = 0.4
    compressor_geometry.inlet_tip_diameter = 0.6
    compressor_geometry.outer_diameter = 0.8
    return compressor_geometry


class TestInletUtils(unittest.TestCase):

    tolerance = 0.001

    def test_GivenValidInputs_ExpectValidResults(self):
        # Given
        inlet_total_temperature = 303.0
        inlet_mid_blade_velocity = 10.0
        inlet = CompressorStage()
        inlet.thermodynamic_point.temperature.total = inlet_total_temperature
        inlet.blade.mid.absolute.magnitude = inlet_mid_blade_velocity

        fluid = MockWorkingFluid()

        # Call
        CalculateRemainingInletQuantities(inlet, fluid)

        # Expect
        self.assertTrue(inlet.thermodynamic_point.speed_of_sound > 0.0)
        self.assertTrue(inlet.blade.mid_mach_number.absolute > 0.0)
        self.assertTrue(inlet.thermodynamic_point.temperature.static > 0.0)

    def test_GivenInvalidSpecificHeat_ExpectFailedAssertion(self):
        # Given
        inlet_total_temperature = 303.0
        inlet_mid_blade_velocity = 10.0
        inlet = CompressorStage()
        inlet.thermodynamic_point.temperature.total = inlet_total_temperature
        inlet.blade.mid.absolute.magnitude = inlet_mid_blade_velocity

        fluid = MockWorkingFluid()
        fluid.specific_heat = 0.0

        # Expect
        with self.assertRaises(AssertionError):
            CalculateRemainingInletQuantities(inlet, fluid)

    def test_GivenInvalidSpecificGasConstant_ExpectFailedAssertion(self):
        # Given
        inlet_total_temperature = 303.0
        inlet_mid_blade_velocity = 10.0
        inlet = CompressorStage()
        inlet.thermodynamic_point.temperature.total = inlet_total_temperature
        inlet.blade.mid.absolute.magnitude = inlet_mid_blade_velocity

        fluid = MockWorkingFluid()
        fluid.specific_gas_constant = 0.0

        # Expect
        with self.assertRaises(AssertionError):
            CalculateRemainingInletQuantities(inlet, fluid)

    def test_GivenInvalidInletTotalTemperature_ExpectFailedAssertion(self):
        # Given
        inlet_mid_blade_velocity = 10.0
        inlet = CompressorStage()
        inlet.blade.mid.absolute.magnitude = inlet_mid_blade_velocity

        fluid = MockWorkingFluid()

        # Expect
        with self.assertRaises(AssertionError):
            CalculateRemainingInletQuantities(inlet, fluid)


if __name__ == "__main__":
    unittest.main()
