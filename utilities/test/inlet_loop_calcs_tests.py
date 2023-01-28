"""
Author: Alejandro Valencia
Update: 24 January, 2022
"""

from dataclasses import dataclass
import unittest
from ccpd.data_types.inputs import Inputs
from ccpd.data_types.thermo_point import ThermodynamicVariable
from ccpd.data_types.working_fluid import WorkingFluid
from ccpd.utilities.inlet_loop_calcs import inlet_loop
from dataclasses import dataclass


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
class MockWorkingFluid:
    """
    Class to mock WorkingFluid class for testing purposes
    """

    specific_heat: float = 1006.0
    specific_ratio: float = 1.4
    specific_gas_constant: float = 287.0
    kinematic_viscosity: float = 18.13e-6


class TestInletLoopCalculations(unittest.TestCase):
    def test_given_valid_inputs_expect_valid_results(self):
        # Given
        inputs = MockInputs()
        working_fluid = MockWorkingFluid()
        rotational_speed = 35.0
        density = ThermodynamicVariable()
        density.total = 0.125
        outer_diameter = 1.1
        inlet_loop_max_iterations = 10
        inlet_loop_tolerance = 0.001

        # Call
        result = inlet_loop(
            inputs,
            working_fluid,
            density.total,
            rotational_speed,
            outer_diameter,
            inlet_loop_max_iterations,
            inlet_loop_tolerance,
        )

        # Expect
        self.assertAlmostEqual(result.blade.mid.magnitude, 13.77, delta=0.01)


if __name__ == "__main__":
    unittest.main()
