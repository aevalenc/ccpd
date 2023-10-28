"""
    Thermo point class data type
"""

from dataclasses import dataclass, field


@dataclass
class ThermodynamicVariable:
    """
    Thermodynamic variable class data type
    """

    static: float = 0.0
    dynamic: float = 0.0
    total: float = 0.0

    def __repr__(self) -> str:
        return f"\n\tstatic: {self.static}\n\tdynamic: {self.dynamic}\n\ttotal: {self.total}"


@dataclass
class ThermoPoint:
    """
    Thermo point class data type
    """

    pressure: ThermodynamicVariable = field(default_factory=lambda: ThermodynamicVariable())
    density: ThermodynamicVariable = field(default_factory=lambda: ThermodynamicVariable())
    temperature: ThermodynamicVariable = field(default_factory=lambda: ThermodynamicVariable())
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
