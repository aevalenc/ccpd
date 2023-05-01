"""
    Thermo point class data type
"""

from dataclasses import dataclass


@dataclass
class ThermodynamicVariable:
    """
    Thermodynamic variable class data type
    """

    static: float = 0.0
    dynamic: float = 0.0
    total: float = 0.0


@dataclass
class ThermoPoint:
    """
    Thermo point class data type
    """

    pressure: ThermodynamicVariable = ThermodynamicVariable()
    density: ThermodynamicVariable = ThermodynamicVariable()
    temperature: ThermodynamicVariable = ThermodynamicVariable()
    speed_of_sound: float = 0.0

    @property
    def GetTemperature(self) -> ThermodynamicVariable:
        return self.temperature

    @property
    def GetPressure(self) -> ThermodynamicVariable:
        return self.pressure

    @property
    def GetDensity(self) -> ThermodynamicVariable:
        return self.density
