"""
Author: Alejandro Valencia
Centrifugal Compressor Preliminary Design
Calculate Coefficient of Friction
Update: October_, 2023

This function uses Newton's method to solve for the Colebrook equation 
in order to calculate the friction coefficient for a specific Reynolds
number and relative roughness

The following are the inputs:

  reynolds_number: Reynolds number
  relative_roughness: relative roughness

The following are the outputs:

    f: coefficient of friction

"""
import numpy as np


def CalculateFrictionCoefficient(
    reynolds_number, relative_roughness, max_iterations=3, tolerance=1e-6, output="no"
) -> float:
    # [A]:Determine Flow Regime
    if reynolds_number <= 2300:
        # Laminar Flow
        return 64 / reynolds_number

    elif reynolds_number < 4000:
        # %% Transitional Phase
        print(
            "WARNING flow is in the transitional phase. Cannot accurately calculate friction coefficient"
        )
        return 0.0
    else:
        # Fully Turbulent
        # [B]:Define Parameters
        A = relative_roughness / 3.7
        B = 2.51 / reynolds_number

        # [C]:Set Initial Guess
        # Newton's method is an iterative one so we need to set an initial
        #  guess. In 1983, S. E. Haaland developed an explicit relationship
        #  to approximate the friction coefficient.
        x0 = -1.8 * np.log10((6.9 / reynolds_number) + A**1.11)

        # [D]:Define Functions
        y = lambda x: x + 2 * np.log10(A + B * x)
        yp = lambda x: 1 + 2 * B / np.log(10) / (A + B * x)

        # [E]:Iterate
        for iteration in range(0, max_iterations):
            iteration += 1
            xn = x0 - y(x0) / yp(x0)
            residual = abs(xn - x0)

            if output == "yes":
                print("Iteration: %d | Residual: %0.6f\n", iteration, residual)

            if residual < tolerance and output == "yes":
                print("\nSolution converged in %d iterations\n", iteration)
                break
            elif residual > 1e6:
                print("WARNING solution diverging\n")
                break

            x0 = xn

        return 1 / x0**2
