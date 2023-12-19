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


@frozen
class DesignParametersII:
    """
    Design Parameters version II
    """

    hub_diameter: float
    specific_diameter: float
    specific_rotational_speed: float
    end_to_end_efficiency: float
    fluid: float
    material: float


@frozen
class DesignInputs:
    mass_flow_rate = field(converter=float)  # type: ignore
    inlet_total_pressure = field(converter=float)  # type: ignore
    inlet_total_temperature = field(converter=float)  # type: ignore
    compression_ratio = field(converter=float)  # type: ignore
    surface_roughness = field(converter=float)  # type: ignore
    tip_clearance = field(converter=float)  # type: ignore
    hub_diameter = field(converter=float)  # type: ignore
    outlet_angle_guess = field(converter=float)  # type: ignore
    specific_diameter = field(converter=float)  # type: ignore
    specific_rotational_speed = field(converter=float)  # type: ignore
    end_to_end_efficiency = field(converter=float)  # type: ignore
    fluid = field(type=str)  # type: ignore
    material = field(type=str)  # type: ignore
