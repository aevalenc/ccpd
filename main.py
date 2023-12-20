""" 
 Author: Alejandro Valencia
 
 Main Function
 Update: 24 July, 2020
"""

from ccpd.data_types.inputs import DesignParameters, Inputs
from ccpd.data_types.centrifugal_compressor import CentrifugalCompressor
from ccpd.utilities.centrifugal_calcs import centrifugal_calcs
import json
import sys
from colorama import Fore
import logging

logging.basicConfig(filename="log.log", encoding="utf-8", level=logging.DEBUG)
logger = logging.getLogger(__name__)


def load_base_inputs() -> tuple[DesignParameters, Inputs]:
    try:
        design_parameter_file = open("ccpd/design_parameters.json", "r")
    except IOError as io_error:
        print(f"Error:{io_error} Design parameters import failed!")
        sys.exit()
    design_parameters = DesignParameters(json.load(design_parameter_file))

    try:
        input_file = open("ccpd/inputs.json", "r")
    except IOError as io_error:
        print(f"Error:{io_error} input parameters import failed!")
        sys.exit()
    inputs = Inputs(json.load(input_file))
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
            design_parameters, inputs = load_base_inputs()
        else:
            # TODO: Load parameters from neptune gui
            design_parameters, inputs = load_base_inputs()

        # [B] Set Loop Parameters
        itrmx = 2
        tol = 1e-5

        # [C]:Run Analysis
        design = CentrifugalCompressor()
        for itr in range(1, itrmx):
            logger.info(f"Main Iteration: {itr}")

            # [D]:Run Centrifugal Preliminary Design Calculations
            design = centrifugal_calcs(
                design_parameters.specific_diameter,
                design_parameters.specific_rotational_speed,
                design_parameters.end_to_end_efficiency,
                design_parameters.fluid,
                design_parameters.material,
                inputs,
            )

            # [E]:Calculate Residual & Check Convergence
            # RES = abs(eta_tt - design.diff.eta_tt) / eta_tt
            # print("Main Residual: {}\n\n".format(RES))
            # if RES < tol:
            #     print("\nMain converged in {} iterations\n".format(itr))
            #     break
            # elif itr == itrmx:
            #     print("\nMax iterations reached\n")

            # # [F]:Reset Efficiency & Iterate
            # eta_tt = design.diff.eta_tt
        print(f"{Fore.GREEN}[ccpd]: exited successfully{Fore.RESET}")

        return design
    else:
        print("Alternative modes TBD")


if __name__ == "__main__":
    main("Preliminary")
