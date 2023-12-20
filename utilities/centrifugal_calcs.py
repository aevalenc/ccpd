"""
Author: Alejandro Valencia
Centrifugal Compressor Preliminary Design
Initial Calculations
Update: 30 April, 2023
"""

from ccpd.data_types.centrifugal_compressor import CentrifugalCompressor
from ccpd.data_types.thermo_point import ThermodynamicVariable
from ccpd.data_types.working_fluid import WorkingFluid
from ccpd.data_types.inputs import Inputs
from ccpd.utilities.inlet.inlet_loop_calcs import InletLoop
from ccpd.utilities.inlet.inlet_utils import CalculateRemainingInletQuantities
from ccpd.utilities.outlet.setup_outlet_stage import SetupOutletStage
from ccpd.utilities.outlet.optimize_mass_flow_rate import optimize_mass_flow
from ccpd.utilities.vaneless_diffuser.vaneless_diffuser import vaneless_diffuser_calcs
import json
import sys
import numpy as np
import logging

logger = logging.getLogger(__name__)


def centrifugal_calcs(
    specific_diameter,
    specific_speed,
    end_to_end_efficiency,
    fluid,
    material,
    inputs: Inputs,
) -> CentrifugalCompressor:
    """
    This function takes initial design parameters and calculates the first
    centrifugal design iteration. Velocity triangles and thermodynamic
    properties are calculated as well.

    The following are inputs:

        Ds: Specific diameter
        Oms: Specific rotational speed
        eta: Baseline/guess efficiency
        fluid: Working fluid
        mat: Compressor material

    The following are outputs: In this case the output is collected in one
    single data structure result. This structure contains five main
    sub data structures: inlet, outlet, comp, vldiff, and diff

        inlet: structure containing thermodynamic and velocity conditions
        outlet: same as inlet
        comp: structure containing information regarding the geometry and overall characteristics of the compressor
                (blade heights, No. of blades, etc)
        vldiff: Structure containing the information on the vanless diffuser
        diff: Structure containing the information on the wedge diffuser both thermodynamic and geometrical quantites
    """
    compressor = CentrifugalCompressor()

    try:
        fluid_database_file = open("ccpd/fluids/fluids.json", "r")
    except IOError as io_error:
        print(f"{io_error} Fluid database import failed!")
        sys.exit()

    fluid_database = json.load(fluid_database_file)
    working_fluid = WorkingFluid(fluid_database[fluid])

    # [B]:Initial Calculations
    isentropic_exponent = (working_fluid.specific_ratio - 1.0) / working_fluid.specific_ratio
    inverse_isentropic_exponent = 1.0 / isentropic_exponent

    isentropic_work = (
        working_fluid.specific_heat
        * inputs.inlet_total_temperature
        * ((inputs.compression_ratio**isentropic_exponent) - 1.0)
    )

    # @todo Create a method within the centrifugal compressor class to initialize the inlet with these initial values
    compressor.geometry.inlet_hub_diameter = inputs.hub_diameter
    density = ThermodynamicVariable()
    density.total = inputs.inlet_total_pressure / (working_fluid.specific_gas_constant * inputs.inlet_total_temperature)
    total_volume_flow_rate = inputs.mass_flow_rate / density.total

    compressor.geometry.outer_diameter = specific_diameter * np.sqrt(total_volume_flow_rate) / (isentropic_work**0.25)

    rotational_speed = specific_speed * (isentropic_work**0.75) / np.sqrt(total_volume_flow_rate)
    logger.info(f"Rotational speed: {rotational_speed:8.6} ({rotational_speed * 60/(2*np.pi):6.6} [RPM])")

    # [C]:Calculate Velocities and Eulerian Work
    compressor.outlet.blade.mid.translational.magnitude = rotational_speed * compressor.geometry.outer_diameter / 2.0

    eulerian_work = isentropic_work / end_to_end_efficiency
    logger.info(f"Eulerian work: {eulerian_work}")
    compressor.outlet.blade.mid.absolute.tangential = (
        eulerian_work / compressor.outlet.blade.mid.translational.magnitude
    )

    # [D]:Calculate Flow Perfomance Indicators
    compressor.stage_loading = isentropic_work / np.square(compressor.outlet.blade.mid.absolute.tangential)
    compressor.flow_coefficient = inputs.mass_flow_rate / (
        density.total * (compressor.outlet.blade.mid.absolute.tangential * (compressor.geometry.outer_diameter / 2.0))
    )
    compressor.blade_orientation_ratio = (
        compressor.outlet.blade.mid.absolute.tangential / compressor.outlet.blade.mid.translational.magnitude
    )

    # %% [E]:Hub Diameter
    # % If a hub diameter is specified then it is automatically placed in
    # % 	the inlet diameter structure. Otherwise it is set considering a
    # % 	ratio between itself and the exducer diameter
    # P = l_eul * mdot;
    # if Dhub ~= 0
    #     D1.hub = Dhub;
    #     [~, sf] = max_diameter(".\Materials" + '\' + mat,w,Dhub,D2);   % [m] "Max" tip diameter
    # else
    #     [Dmax,sf] = max_diameter(".\Materials" + '\' + mat,w,Dhub,D2);   % [m] "Max" tip diameter
    #     D1.hub    = 0.2*Dmax;
    # end

    # %% [F]:Setup Inlet Loop
    inlet_loop_max_iterations = 1000
    inlet_loop_tolerance = 1e-3
    inlet = InletLoop(
        inputs,
        working_fluid,
        density.total,
        rotational_speed,
        compressor.geometry,
        inlet_loop_max_iterations,
        inlet_loop_tolerance,
    )

    #  [F.1]:Inlet Geometry
    compressor.geometry.CalculateInletBladeHeightAndRatios()
    inlet.blade.CalculateComponentsViaFreeVortexMethod(compressor.geometry, rotational_speed)
    CalculateRemainingInletQuantities(inlet, working_fluid)
    inlet.thermodynamic_point.density.total = density.total
    inlet.thermodynamic_point.pressure.total = inputs.inlet_total_pressure

    #  [G]:Outlet
    # % This for the moment is a little vague. Since we do not know our
    # % 	outlet blade height we assume an outlet absolute angle and check
    # % 	for stability in the vanless diffuser later
    alpha2 = 65 * (np.pi / 180.0)

    outlet = SetupOutletStage(
        alpha2,
        eulerian_work,
        compressor.outlet.blade.mid.translational,
        inputs,
        working_fluid,
    )
    logger.info(
        f"Reaction: {working_fluid.specific_heat * (outlet.thermodynamic_point.temperature.static - inlet.thermodynamic_point.temperature.static) / eulerian_work}"
    )
    # outlet.D2 = D2;

    #  [G.1]:Loop and Iterate
    max_outlet_loop_iterations = 10
    outlet_loop_tolerance = 1e-3
    optimize_mass_flow(
        inlet,
        outlet,
        compressor.geometry,
        working_fluid,
        inverse_isentropic_exponent,
        eulerian_work,
        inputs,
        max_outlet_loop_iterations,
        outlet_loop_tolerance,
    )
    # [outlet,inlet.beta1_geo,Nb] = outlet_loop(inlet, outlet, l_eul, itrmx, tol);
    compressor.impeller_compression_ratio = (
        outlet.thermodynamic_point.pressure.total / inlet.thermodynamic_point.pressure.total
    )
    logger.debug(f"Impeller compression ratio: {compressor.impeller_compression_ratio:.3}")

    # []:Diffusion & Check For Stall
    # This diffusion factor is based on the Dixon book. Lieblein,
    #   Schwenk, and Broderick (1953) developed a general diffusion
    #   factor to check for stall.
    DR = np.abs(inlet.blade.mid.relative.tangential / outlet.blade.mid.relative.magnitude)
    DH = {
        "hub": outlet.blade.mid.relative.magnitude / inlet.blade.hub.relative.magnitude,
        "mid": outlet.blade.mid.relative.magnitude / inlet.blade.mid.relative.magnitude,
        "tip": outlet.blade.mid.relative.magnitude / inlet.blade.tip.relative.magnitude,
    }
    DF = (1 - outlet.blade.mid.relative.magnitude / inlet.blade.mid.relative.magnitude) + np.abs(
        inlet.blade.mid.relative.tangential - outlet.blade.mid.relative.tangential
    ) / (2 * inlet.blade.mid.relative.magnitude) * 0.4
    logger.debug(f"Diffusion ratios:\nDR: {DR}\nDH: {DH}\nDF: {DF}")

    #  []:Vanless & Vaned Diffuser Calculations
    compressor.vaneless_diffuser = vaneless_diffuser_calcs(
        outlet, compressor.geometry, working_fluid, inputs.mass_flow_rate, 100, 0.001
    )
    # result = diffuser_calcs(result);
    # result = diff_diameter(result);
    # result.comp.eta_tt = result.diff.eta_tt;

    #  []:Post Calculations
    # NDmdot = mdot * sqrt(y * Rh * TT1) / (inlet.S1 * PT1);
    # etap   = k * log(result.diff.Be)/log(result.diff.TT4 / TT1);
    # C      = 1 / (B ^ (1 - (y-1)/(2 * y * etap)));

    # result.comp.NDmdot = NDmdot;    % [] Non-dimensional mass flow rate
    # result.comp.etap   = etap;      % [] Polytropic efficiency
    # result.comp.C      = C;         % [] Operating line constant
    # oo = 0
    return compressor

    #  [I]:Ouput
    # result.inlet      = inlet;      % []      Inlet operating conditions
    # result.inlet.in   = outlet.in;  % []      Inlet incidence angle
    # result.outlet     = outlet;     % []      Outlet operating conditions

    # result.comp.Nb    = Nb;         % []      Number of blades
    # result.comp.Bc    = Bc;         % []      Final impeller compression ratio given Ds,Oms
    # result.comp.b1    = b1;         % [m]     Inlet blade height
    # result.comp.eta   = outlet.eta; % []      Compressor efficiency
    # result.comp.b2    = outlet.b2;  % [m]     Outlet blade height
    # result.comp.w     = w;          % [rad/s] Rotational speed
    # result.comp.wRPM  = wRPM;       % [RPM]         "
    # result.comp.Psi   = Psi;        % []      Stage loading
    # result.comp.Phi   = Phi;        % []      Flow Coefficient
    # result.comp.tau   = tau;        % []      Blade orientation
    # result.comp.D1    = D1;         % []      Inlet diameters
    # result.comp.D2    = D2;         % []      Outlet diameter
    # result.comp.rtd2  = rtd2;       % []      Inlet tip dia. to outlet dia. ratio
    # result.comp.rht   = rht;        % []      Inlet hub dia. to inlet tip dia. ratio
    # result.comp.Ds    = Ds;         % []      Specific diameter
    # result.comp.Oms   = Oms;        % []      Specific rotational speed
    # result.comp.his   = his;        % [J]     Isentropic Work
    # result.comp.Q1    = Q1;         % [m^3/s] Volume flow rate
    # result.comp.sf    = sf;         % []      Diameter safety factor
    # result.comp.l_eul = l_eul;      % [J/kg]  New work
    # result.comp.P     = P;          % [J/s]   Power
    # result.comp.DR    = DR;         % []      Diffusion ratio
    # result.comp.DH    = DH;         % []      De Haller number
    # result.comp.DF    = DF;         % []      Lieblein diffusion factor
