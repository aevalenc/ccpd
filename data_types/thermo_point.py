"""
    Thermo point class data type
"""


class ThermodynamicVariable:
    """
    Thermodynamic variable class data type
    """

    def __init__(self):
        self.static = 0.0
        self.dynamic = 0.0
        self.total = 0.0


class ThermoPoint:
    """
    Thermo point class data type
    """

    # self.__pressure = ThermodynamicVariable()
    # self.__temperature = ThermodynamicVariable()
    # self.__density = ThermodynamicVariable()

    def __init__(
        self,
        pressure=ThermodynamicVariable(),
        density=ThermodynamicVariable(),
        temperature=ThermodynamicVariable(),
    ) -> None:
        self.__pressure = pressure
        self.__density = density
        self.__temperature = temperature

    @property
    def GetPressure(self):
        return self.__pressure

    @property
    def GetDensity(self):
        return self.__density

    @property
    def GetTemperature(self):
        return self.__temperature
