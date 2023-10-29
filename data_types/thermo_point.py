"""
    Thermo point class data type
"""

from dataclasses import dataclass, field


@dataclass
class ThermodynamicVariable:
    """
    Thermodynamic variable class data type
    """

    _static: float = 0.0
    _dynamic: float = 0.0
    _total: float = 0.0

    @property
    def static(self) -> float:
        return self._static

    @property
    def dynamic(self) -> float:
        return self._dynamic

    @property
    def total(self) -> float:
        return self._total

    @static.setter
    def static(self, value) -> None:
        self._static = value

    @dynamic.setter
    def dynamic(self, value) -> None:
        self._dynamic = value

    @total.setter
    def total(self, value) -> None:
        self._total = value

    # def __repr__(self) -> str:
    #     return f"\n\tstatic: {self.static}\n\tdynamic: {self.dynamic}\n\ttotal: {self.total}"


@dataclass
class ThermoPoint:
    """
    Thermo point class data type
    """

    _pressure: ThermodynamicVariable = field(default_factory=lambda: ThermodynamicVariable())
    _density: ThermodynamicVariable = field(default_factory=lambda: ThermodynamicVariable())
    _temperature: ThermodynamicVariable = field(default_factory=lambda: ThermodynamicVariable())
    _speed_of_sound: float = 0.0

    @property
    def temperature(self) -> ThermodynamicVariable:
        return self._temperature

    @property
    def pressure(self) -> ThermodynamicVariable:
        return self._pressure

    @property
    def density(self) -> ThermodynamicVariable:
        return self._density

    @temperature.setter
    def temperature(self, value) -> None:
        self._temperature = value

    @pressure.setter
    def pressure(self, value) -> None:
        self._pressure = value

    @density.setter
    def density(self, value) -> None:
        self._density = value
