"""
  Input parameters

  The following are inputs for the prelimiary design calculations:
              Ds    : Specific diameter
             Oms   : Specific Speed
             eta_tt: Baseline end to end efficiency
             fluid : Working fluid for the machine
             mat   : Compressor material
"""


class DesignParameters:
    """
    design parameters
    """

    specific_diameter = 3.85
    specific_rotational_speed = 0.6
    eta_tt = 0.85
    fluid = "air"
    material = "aluminum"


class Inputs:
    """
    inputs
    """

    mass_flow_rate = 5
    inlet_total_pressure = 100000
    total_inlet_temperature = 293
    compression_ratio = 1.25
    surface_roughness = 0.0025
    tip_clearance = 0.001
    hub_diameter = 0.2
