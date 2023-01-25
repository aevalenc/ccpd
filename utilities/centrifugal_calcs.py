"""
Author: Alejandro Valencia
Centrifugal Compressor Preliminary Design
Initial Calculations
Update: 24 July, 2020
"""

from ccpd.data_types.centrifugal_compressor import CentrifugalCompressor
from ccpd.data_types.thermo_point import ThermodynamicVariable
from ccpd.data_types.working_fluid import WorkingFluid
from ccpd.data_types.inputs import Inputs
from ccpd.utilities.inlet_loop_calcs import inlet_loop
import json
import sys
import numpy as np


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
    single MATLAB data structure result. This structure contains five main
    sub data structures: inlet, outlet, comp, vldiff, and diff

              inlet: structure containing thermodynamic and velocity
                    conditions
              outlet: same as inlet
              comp: structure containing information regarding the
              geometry and overall characteristics of the compressor
            (blade heights, No. of blades, etc)
          vldiff: Structure containing the information on the vanless
                diffuser
            diff: Structure containing the information on the wedge
              diffuser both thermodynamic and geometrical quantites
    """
    compressor = CentrifugalCompressor()

    try:
        fluid_database_file = open("ccpd/fluids/fluids.json", "r")
    except IOError as io_error:
        print(f"{io_error} Fluid database import failed!")
        sys.exit()

    fluid_database = json.load(fluid_database_file)
    working_fluid = WorkingFluid(fluid_database[fluid])

    isentropic_exponent = (
        working_fluid.specific_ratio - 1.0
    ) / working_fluid.specific_ratio

    inverse_isentropic_exponent = 1.0 / isentropic_exponent

    # [B]:Initial Calculations
    isentropic_work = (
        working_fluid.specific_heat
        * inputs.inlet_total_temperature
        * ((inputs.compression_ratio**isentropic_exponent) - 1.0)
    )

    # @todo Create a method within the centrifugal compressor class to initialize the inlet with these initial values
    density = ThermodynamicVariable()
    density.total = inputs.inlet_total_pressure / (
        working_fluid.specific_gas_constant * inputs.inlet_total_temperature
    )
    total_volume_flow_rate = inputs.mass_flow_rate / density.total

    compressor.geometry.outer_diameter = (
        specific_diameter * np.sqrt(total_volume_flow_rate) / (isentropic_work**0.25)
    )

    rotational_speed = (
        specific_speed * (isentropic_work**0.75) / np.sqrt(total_volume_flow_rate)
    )
    # wRPM  = w * 60/(2*pi);                  % [RPM]
    #     compressor.inlet.thermodynamic_point.
    # compressor.inlet.thermodynamic_point.
    # compressor.inlet.thermodynamic_point.

    # [C]:Calculate Velocities and Eulerian Work
    compressor.outlet.blade.mid.tangential = (
        rotational_speed * compressor.geometry.outer_diameter / 2.0
    )
    eulerian_work = isentropic_work / end_to_end_efficiency
    compressor.outlet.blade.mid.axial = (
        eulerian_work / compressor.outlet.blade.mid.tangential
    )

    # [D]:Calculate Flow Perfomance Indicators
    compressor.stage_loading = isentropic_work / np.square(
        compressor.outlet.blade.mid.tangential
    )
    compressor.flow_coefficient = inputs.mass_flow_rate / (
        density.total
        * (
            compressor.outlet.blade.mid.tangential
            * (compressor.geometry.outer_diameter / 2.0)
        )
    )
    compressor.blade_orientation_ratio = (
        compressor.outlet.blade.mid.axial / compressor.outlet.blade.mid.tangential
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
    inlet = inlet_loop(
        inputs,
        fluid,
        density.total,
        rotational_speed,
        compressor.geometry.outer_diameter,
        inlet_loop_max_iterations,
        inlet_loop_tolerance,
    )
    inlet_loop()

    # %% [F.1]:Inlet Geometry
    # D1.tip = inlet.Dtip;              	% [m] Tip diameter
    # b1     = (D1.tip - D1.hub) / 2;   	% [m] blade height
    # D1.mid = (D1.tip + D1.hub) / 2;   	% [m] Mean diameter
    # rtd2   = D1.tip / D2;             	% []  Inlet tip dia. to outlet dia. ratio
    # rht    = D1.hub / D1.tip;         	% []  Inlet hub dia. to inlet tip dia. ratio

    # %% [F.2]:Inlet Velocity Triangles
    # % As a recap, our knowns are U2, V2.tan, and V1.mag. With these known
    # %   quantites and the diameters for our machine, we can solve for the
    # %   remaining velocity components.
    # inlet = inlet_calcs(inlet, D1, w);
    # inlet.rho01 = rho01;                % [kg/m^3] Inlet total density

    # %% [G]:Outlet
    # % This for the moment is a little vague. Since we do not know our
    # % 	outlet blade height we assume an outlet absolute angle and check
    # % 	for stability in the vanless diffuser later
    # alpha2 = 65;                                      % [deg]
    # outlet = outlet_calcs(alpha2, l_eul, U2);         % []    Outlet velocity triangle
    # outlet.X2 = cp * (outlet.T2 - inlet.T1) / l_eul;  % []    Reaction
    # outlet.D2 = D2;

    # %% [G.1]:Loop and Iterate
    # itrmx = 10;
    # tol   = 1e-3;
    # [outlet,inlet.beta1_geo,Nb] = outlet_loop(inlet, outlet, l_eul, itrmx, tol);
    # Bc    = outlet.PT2 / PT1; % Impeller compression ratio

    # %% []:Diffusion & Check For Stall
    # % This diffusion factor is based on the Dixon book. Lieblein,
    # %   Schwenk, and Broderick (1953) developed a general diffusion
    # %   factor to check for stall.
    # DR     = abs(inlet.W1.mid.tan / outlet.W2.mag);
    # DH.hub = outlet.W2.mag / inlet.W1.hub.mag;
    # DH.mid = outlet.W2.mag / inlet.W1.mid.mag;
    # DH.tip = outlet.W2.mag / inlet.W1.tip.mag;
    # DF     = (1 - outlet.W2.mag / inlet.W1.mid.mag) + ...
    #           abs(inlet.W1.mid.tan - outlet.W2.tan) / (2 * inlet.W1.mid.mag) * 0.4;

    # %% [I]:Ouput
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

    # %% []:Vanless & Vaned Diffuser Calculations
    # result = vaneless_diffuser_calcs(result, 10, 1e-3);
    # result = diffuser_calcs(result);
    # result = diff_diameter(result);
    # result.comp.eta_tt = result.diff.eta_tt;

    # %% []:Post Calculations
    # NDmdot = mdot * sqrt(y * Rh * TT1) / (inlet.S1 * PT1);
    # etap   = k * log(result.diff.Be)/log(result.diff.TT4 / TT1);
    # C      = 1 / (B ^ (1 - (y-1)/(2 * y * etap)));

    # result.comp.NDmdot = NDmdot;    % [] Non-dimensional mass flow rate
    # result.comp.etap   = etap;      % [] Polytropic efficiency
    # result.comp.C      = C;         % [] Operating line constant
    # oo = 0
    return compressor
