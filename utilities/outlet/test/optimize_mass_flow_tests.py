"""
Author: Alejandro Valencia
Update: 30 April, 2023
"""

import unittest
from ccpd.data_types.centrifugal_compressor import CompressorStage
from ccpd.data_types.thermo_point import ThermodynamicVariable
from ccpd.data_types.three_dimensional_blade import VelocityVector
from ccpd.data_types.centrifugal_compressor_geometry import CompressorGeometry
from ccpd.data_types.test_utils import MockInputs, MockWorkingFluid
from ccpd.utilities.outlet.optimize_mass_flow_rate import optimize_mass_flow
from ccpd.utilities.outlet.setup_outlet_stage import SetupOutletStage
import numpy as np

TO_RADIANS = np.pi / 180


def CreateBasicCompressorGeometry() -> CompressorGeometry:
    compressor_geometry = CompressorGeometry()
    compressor_geometry.inlet_hub_diameter = 0.4
    compressor_geometry.inlet_mid_diameter = 0.5
    compressor_geometry.inlet_tip_diameter = 0.6
    compressor_geometry.outer_diameter = 0.8
    return compressor_geometry


def CreateBasicInletStage() -> CompressorStage:
    inlet = CompressorStage()

    inlet.thermodynamic_point.pressure.static = 98281.8
    inlet.thermodynamic_point.pressure.total = 100000.0
    inlet.thermodynamic_point.density.total = 1.189
    inlet.thermodynamic_point.density.static = 1.174
    inlet.thermodynamic_point.temperature.total = 293
    inlet.thermodynamic_point.temperature.static = 291.55

    inlet.blade.mid.absolute = VelocityVector(axial=53.9224, magnitude=53.9224)
    inlet.blade.mid.relative = VelocityVector(
        axial=53.9224, tangential=-48.108, magnitude=53.9224, angle=-0.728
    )
    inlet.blade.mid.translational = VelocityVector(magnitude=48.107, angle=-0.728)
    return inlet


class TestOutletLoopCalculations(unittest.TestCase):
    tolerance: float = 0.001
    max_iterations: int = 10
    inputs: MockInputs = MockInputs()
    working_fluid: MockWorkingFluid = MockWorkingFluid()
    density: ThermodynamicVariable = ThermodynamicVariable()
    compressor_geometry: CompressorGeometry = CompressorGeometry()
    eulerian_work: float = 0.0
    tip_clearance = 0.0003

    def setUp(self) -> None:
        self.inputs = MockInputs()
        self.working_fluid = MockWorkingFluid()
        self.density.total = 0.125
        self.compressor_geometry = CreateBasicCompressorGeometry()
        self.eulerian_work = 22404.4
        return super().setUp()

    def test_given_valid_inputs_expect_valid_results(self):
        # Setup
        self.setUp()

        # Given
        inverse_exponent = 3.5
        alpha2 = 65 * (np.pi / 180)
        outlet_velocity = VelocityVector(axial=0.0, tangential=160.9, angle=alpha2)
        outlet_velocity.CalculateMagnitudeWithComponents()
        inlet = CreateBasicInletStage()
        outlet = SetupOutletStage(
            alpha2, self.eulerian_work, outlet_velocity, self.inputs, self.working_fluid
        )

        # Call
        result = optimize_mass_flow(
            inlet,
            outlet,
            self.compressor_geometry,
            self.working_fluid,
            inverse_exponent,
            self.eulerian_work,
            self.inputs,
            self.max_iterations,
            self.tolerance,
        )
        outlet = result[0]

        # Expect
        self.assertAlmostEqual(outlet.blade.mid.absolute.magnitude, 28.695, delta=self.tolerance)


if __name__ == "__main__":
    unittest.main()
