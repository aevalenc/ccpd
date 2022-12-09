"""
Author: Alejandro Valencia
Update: 9 December, 2022
"""


class Material:
    """
    Materal of the compressor class definition
    """

    def __init__(self, material_dictionary) -> None:
        self.specific_heat = material_dictionary.get("specific_heat")
        self.specific_ratio = material_dictionary.get("specific_ratio")
        self.specific_gasconstant = material_dictionary.get("specific_gasconstant")
        self.kinematic_viscosity = material_dictionary.get("kinematic_viscosity")
