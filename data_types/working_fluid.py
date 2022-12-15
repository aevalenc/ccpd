"""
Author: Alejandro Valencia
Update: 9 December, 2022
"""


class WorkingFluid:
    """
    Working fluid of the compressor class
    """

    def __init__(self, working_fluid_dictionary) -> None:
        self.specific_heat = working_fluid_dictionary.get("specific_heat")
        self.specific_ratio = working_fluid_dictionary.get("specific_ratio")
        self.specific_gas_constant = working_fluid_dictionary.get(
            "specific_gas_constant"
        )
        self.kinematic_viscosity = working_fluid_dictionary.get("kinematic_viscosity")
