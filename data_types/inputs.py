"""
  Input parameters

  The following are inputs for the prelimiary design calculations:
              Ds    : Specific diameter
             Oms   : Specific Speed
             eta_tt: Baseline end to end efficiency
             fluid : Working fluid for the machine
             mat   : Compressor material
"""

from attrs import frozen, field


class DesignParameters:
    """
    design parameters
    """

    def __init__(self, design_parameter_dictionary) -> None:
        self.__dict__.update(design_parameter_dictionary)
        self.specific_diameter = design_parameter_dictionary.get("specific_diameter")
        self.specific_rotational_speed = design_parameter_dictionary.get("specific_rotational_speed")
        self.end_to_end_efficiency = design_parameter_dictionary.get("end_to_end_efficiency")
        self.fluid = design_parameter_dictionary.get("fluid")
        self.material = design_parameter_dictionary.get("material")


class Inputs:
    """
    inputs
    """

    def __init__(self, input_dictionary) -> None:
        self.__dict__.update(input_dictionary)
        self.mass_flow_rate = input_dictionary.get("mass_flow_rate")
        self.inlet_total_pressure = input_dictionary.get("inlet_total_pressure")
        self.inlet_total_temperature = input_dictionary.get("inlet_total_temperature")
        self.compression_ratio = input_dictionary.get("compression_ratio")
        self.surface_roughness = input_dictionary.get("surface_roughness")
        self.tip_clearance = input_dictionary.get("tip_clearance")
        self.hub_diameter = input_dictionary.get("hub_diameter")


@frozen
class InputsII:
    """
    inputs
    """

    mass_flow_rate: float
    inlet_total_pressure: float
    inlet_total_temperature: float
    compression_ratio: float
    surface_roughness: float
    tip_clearance: float
    hub_diameter: float
    outlet_angle_guess: float


@frozen
class DesignParametersII:
    """
    Design Parameters version II
    """

    specific_diameter: float
    specific_rotational_speed: float
    end_to_end_efficiency: float
    fluid: str
    material: str


@frozen
class DesignInputs:
    mass_flow_rate: float = field(converter=float)
    inlet_total_pressure: float = field(converter=float)
    inlet_total_temperature: float = field(converter=float)
    compression_ratio: float = field(converter=float)
    surface_roughness: float = field(converter=float)
    tip_clearance: float = field(converter=float)
    hub_diameter: float = field(converter=float)
    outlet_angle_guess: float = field(converter=float)
    specific_diameter: float = field(converter=float)
    specific_rotational_speed: float = field(converter=float)
    end_to_end_efficiency: float = field(converter=float)
    fluid: str
    material: str
