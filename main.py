""" 
 Author: Alejandro Valencia
 
 Main Function
 Update: 24 July, 2020
"""


from utilities.centrifugal_calcs import centrifugal_calcs


def main(design_stage, varargin):
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
        Ds = varargin[1]
        Oms = varargin[2]
        eta_tt = varargin[3]
        fluid = varargin[4]
        mat = varargin[5]

        # [B] Set Loop Parameters
        if len(varargin) > 6:
            itrmx = varargin[6]
            tol = varargin[7]
        else:
            itrmx = 100
            tol = 1e-5

        # [C]:Run Analysis
        # design = CentrifugalCompressor()
        for itr in range(1, itrmx):
            print("Main Iteration: {}\n".format(itr))

            # [D]:Run Centrifugal Preliminary Design Calculations
            design = centrifugal_calcs(Ds, Oms, eta_tt, fluid, mat)

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

    return design
