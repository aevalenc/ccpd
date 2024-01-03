""" 
 Author: Alejandro Valencia
 
 Main Function
 Update: 3 January, 2024
"""

from ccpd.data_types.inputs import DesignInputs, DesignParametersII, Inputs, InputsII
from ccpd.data_types.centrifugal_compressor import CentrifugalCompressor
from ccpd.utilities.centrifugal_calcs import centrifugal_calcs
import json
import sys
from colorama import Fore
import logging

logging.basicConfig(filename="log.log", encoding="utf-8", level=logging.DEBUG)
logger = logging.getLogger(__name__)


def load_inputs() -> tuple[DesignInputs, InputsII]:
    try:
        input_file = open("ccpd/neptune_inputs.json", "r")
    except IOError as io_error:
        print(f"Error:{io_error} input parameters import failed!")
        sys.exit()
    loaded_file = json.load(input_file)
    design_inputs = DesignInputs(**(loaded_file))
    logger.info(f"Inputs from neptune created")
    inputsII = InputsII(
        mass_flow_rate=design_inputs.mass_flow_rate,
        inlet_total_temperature=design_inputs.inlet_total_temperature,
        inlet_total_pressure=design_inputs.inlet_total_pressure,
        compression_ratio=design_inputs.compression_ratio,
        surface_roughness=design_inputs.surface_roughness,
        tip_clearance=design_inputs.tip_clearance,
        hub_diameter=design_inputs.hub_diameter,
        outlet_angle_guess=design_inputs.outlet_angle_guess,
    )
    return design_inputs, inputsII


def load_base_inputs() -> tuple[DesignParametersII, InputsII]:
    try:
        design_parameter_file = open("ccpd/design_parameters.json", "r")
    except IOError as io_error:
        print(f"Error:{io_error} Design parameters import failed!")
        sys.exit()
    loaded_file = json.load(design_parameter_file)
    design_parameters = DesignParametersII(**loaded_file)

    try:
        input_file = open("ccpd/inputs.json", "r")
    except IOError as io_error:
        print(f"Error:{io_error} input parameters import failed!")
        sys.exit()
    inputs = InputsII(**(json.load(input_file)))
    return design_parameters, inputs


def main(design_stage: str, caller: str = "cli"):
    """
    This function runs either a preliminary design calculations
     for a centrifugal compressor. Note the inputs must be entered in the
     correct order.

    For the prelimiary design this "main" function runs the
     centrifugal_calcs function for a specified number of iterations or
     until convergence is reached. "main" takes the final end to end
     efficiency and uses it as the new guess value to calculate the
     Eulerian work for the centrifugal compressor.

    The following are inputs for the prelimiary design calculations:
        Ds    : Specific diameter
        Oms   : Specific Speed
        eta_tt: Baseline end to end efficiency
        fluid : Working fluid for the machine
        mat   : Compressor material

    For the post calculations the user has three options; a rotational
           speed analysis, preswirl analysis, or a mass flow analysis. Currently,
       only the mass flow analysis has been verified

    The following are inputs for the mass flow analysis:
             fluid : Working fluid for the machine
             mat   : Compressor material
             design: Base design
             mdot  : Desired mass flow rate
    """

    if design_stage == "Preliminary":
        # [A]:Set Calculation Parameters
        if caller == "cli":
            design_inputs, inputsII = load_base_inputs()
        else:
            design_inputs, inputsII = load_inputs()
            logger.debug(f"Inputs from neptune: {inputsII}")

        # [B] Set Loop Parameters
        max_iterations = 2
        tolerance = 1e-5

        # [C]:Run Analysis
        design = CentrifugalCompressor()
        end_to_end_efficiency = design_inputs.end_to_end_efficiency
        for iteration in range(0, max_iterations):
            iteration += 1
            logger.info(f"Main Iteration: {iteration}")

            # [D]:Run Centrifugal Preliminary Design Calculations
            design = centrifugal_calcs(
                design_inputs.specific_diameter,
                design_inputs.specific_rotational_speed,
                end_to_end_efficiency,
                design_inputs.fluid,
                design_inputs.material,
                inputsII,
            )

            # [E]:Calculate Residual & Check Convergence
            residual = abs(end_to_end_efficiency - design.total_efficiency) / design.total_efficiency
            logger.info(f"Main Residual: {residual:.6}")
            if residual < tolerance:
                logger.info(f"Main converged in {iteration} iterations")
                break
            elif iteration == max_iterations:
                logger.warning("Max iterations reached")

            # [F]:Reset Efficiency & Iterate
            end_to_end_efficiency = design.total_efficiency

        print(f"{Fore.GREEN}[ccpd]: exited successfully{Fore.RESET}")

        return design
    else:
        print("Alternative modes TBD")


if __name__ == "__main__":
    main("Preliminary")
