"""
Author: Alejandro Valencia
Update: October 15, 2023
"""

from dataclasses import dataclass
from ccpd.data_types.inputs import Inputs
from ccpd.data_types.working_fluid import WorkingFluid


@dataclass
class MockInputs(Inputs):
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
