import sys
sys.path.insert(0, '/home/joemcormier/pycrash/')
import numpy as np
from scipy.optimize import minimize
from scipy.optimize import Bounds
from pycrash.vehicle import Vehicle
from pycrash.model_calcs.carpenter_momentum import IMPC
from pycrash.visualization.initial_positions import initial_position
from pycrash.model_calcs.position_data import position_data_static
import os
os.chdir('/home/joemcormier/pycrash/projects/validation impact momentum/')
import data.input.vehicles as vehicle



veh1_input = vehicle.subaru.copy()
veh1_input['vx_initial'] = 15
veh1_input['pimpact_x'] = 8.08
veh1_input['pimpact_y'] = -2.5
veh1_input['impact_norm_rad'] = (0 * np.pi / 180)  # <- normal impact plane angle


veh2_input = vehicle.barrier.copy()
veh2_input['vx_initial'] = 0
veh2_input['init_x_pos'] = 10.75
veh2_input['init_y_pos'] = -2.5
veh2_input['head_angle'] = 180


veh1 = Vehicle('Veh1', veh1_input)
veh2 = Vehicle('Veh2', veh2_input)


initial_position(position_data_static([veh1, veh2]))


# test inputs to match
dvx_test = 10
dvy_test = 5
dvomega_test = -250

# Create simulation
sim_inputs = {'cor': 0.1,
              'cof': 0.3,
              'impact_norm_rad': 0}

veh1_input['vx_initial'] = 15
veh1_input['pimpact_x'] = 8.08
veh1_input['pimpact_y'] = -2.5
veh1_input['impact_norm_rad'] = (0 * np.pi / 180)  # <- normal impact plane angle
veh1_input['striking'] = True
veh2_input['init_x_pos'] = 10.75
veh2_input['init_y_pos'] = -2.5

veh2_input['striking'] = False

name = 'run1'
run = IMPC('run1', veh1, veh2, sim_inputs)

test_inputs = {}
test_inputs = {'cor': 0.1,
                       'cof': 0.3,
                       'impact_norm_rad': 0 * np.pi / 180,
                       'vehicle':'subaru',
                       'pimpact_x':8.08,
                       'pimpact_y':-2.5,
                       'impact_speed':40,
                       'barrier':'barrier',
                       'barrier_x_pos':10.75,
                       'barrier_y_pos':-2.5,
                       'dvx_test': 10,
                       'dvy_test': 5,
                       'dvomega_test': -250}


def function_optimize(params, test_inputs):
    cor = params[0]
    cof = params[1]
    impact_norm_deg = params[2]
    veh1_input = vehicle.subaru.copy()  # import vehicle
    veh1_input['vx_initial'] = test_inputs['impact_speed']
    veh1_input['pimpact_x'] = test_inputs['pimpact_x']
    veh1_input['pimpact_y'] = test_inputs['pimpact_y']
    veh1_input['impact_norm_rad'] = test_inputs['impact_norm_rad']
    veh1 = Vehicle('Veh1', veh1_input)

    veh2_input = vehicle.barrier.copy()  # import barrier
    veh2_input['init_x_pos'] = test_inputs['barrier_x_pos']
    veh2_input['init_y_pos'] = test_inputs['barrier_y_pos']

    veh1 = Vehicle('Veh1', veh1_input)
    veh2 = Vehicle('Veh2', veh2_input)
    sim_inputs = {'cor': 0.1,
                  'cof': 0.3,
                  'impact_norm_rad': impact_norm_deg * np.pi / 180}

    run = IMPC(name, veh1, veh2, sim_inputs)

    diff_dv_x = run.v1_result['dvx'] - test_inputs['dvx_test']
    diff_dv_y = run.v1_result['dvy'] - test_inputs['dvy_test']
    diff_omega = run.v1_result['oz_rad'] - test_inputs['dvomega_test']
    omega_scale = 2

    return diff_dv_x**2 + diff_dv_y**2 + (omega_scale*diff_omega)**2


x0 = np.array([0.3, 0.3, 0])
#x0 = [0.3, 0.3, 0]
bounds = Bounds([0, 0.4], [0, .6], [0, 360])
res = minimize(function_optimize, x0, args=(test_inputs,), method='nelder-mead',
               options={'disp': True}, bounds=bounds)
