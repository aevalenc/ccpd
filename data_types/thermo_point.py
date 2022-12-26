"""
    Thermo point class data type
"""


class ThermodynamicVariable:
    """
    Thermodynamic variable class data type
    """

    static = 0.0
    dynamic = 0.0
    total = 0.0


class ThermoPoint:
    """
    Thermo point class data type
    """

    pressure = ThermodynamicVariable()
    temperature = ThermodynamicVariable()
    density = ThermodynamicVariable()
