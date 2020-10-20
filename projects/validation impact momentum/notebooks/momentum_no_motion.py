import sys

# sys.path.insert(0, '/home/joemcormier/pycrash/')
sys.path.insert(0, '/home/jmc/Documents/pycrash/')
import numpy as np
import pickle
from scipy.optimize import minimize
from scipy.optimize import Bounds
from pycrash.vehicle import Vehicle
from pycrash.model_calcs.carpenter_momentum import IMPC
from pycrash.visualization.initial_positions import initial_position
from pycrash.model_calcs.position_data import position_data_static
import os

# os.chdir('/home/joemcormier/pycrash/projects/validation impact momentum/')
# os.chdir('/home/jmc/Documents/pycrash/projects/validation impact momentum/')
sys.path.insert(0, '/home/jmc/Documents/pycrash/projects/validation impact momentum/src/')
from vehicle_data import vehicle_data

report_dir = '/home/jmc/Documents/pycrash/projects/validation impact momentum/reports/'
# load saved data
with open(os.path.join(report_dir, 'all_test_data.pkl'), 'rb') as handle:
    all_test_data = pickle.load(handle)
with open(os.path.join(report_dir, 'optimized_inputs.pkl'), 'rb') as handle:
    optimized_inputs = pickle.load(handle)

# Brach Test Data
test_data = {}
current_test = 'CF11002'
test_data = {current_test: {'vehicle': 'FordFusion',
                            'barrier': 'barrier',
                            'impact_speed': 39.95,  # [mph]
                            'd_impact': 4.14,  # <- radius to impact center [ft]
                            'phi_impact': -29,  # <- angle to impact center (ccw [+])
                            'gamma': -74.6,  # crush surface angle
                            'cor_test': 0,
                            'impulse_ratio': 85.18,
                            'dvx_test': -38.49 * 0.681818,  # [mph]
                            'dvy_test': 10.69 * 0.681818,  # [mph]
                            'domega_test': -102.75}}  # [deg/s]
# 4.6
# -23.8

test_inputs = test_data[current_test]

veh1_input = vehicle_data['FordFusion'].copy()
veh1_input['vx_initial'] = test_inputs['impact_speed']
veh1_input['pimpact_x'] = test_inputs['d_impact'] * np.cos(test_inputs['phi_impact'] * np.pi / 180)
veh1_input['pimpact_y'] = test_inputs['d_impact'] * np.sin(test_inputs['phi_impact'] * np.pi / 180)
veh1_input['impact_norm_rad'] = test_inputs['gamma'] * np.pi / 180

veh2_input = vehicle_data['barrier'].copy()
veh2_input['vx_initial'] = 0
veh2_input['init_x_pos'] = vehicle_data['barrier']['length'] / 2 + vehicle_data['FordFusion']['lcgf'] + \
                           vehicle_data['FordFusion']['f_hang']
veh2_input['init_y_pos'] = test_inputs['d_impact'] * np.sin(test_inputs['phi_impact'] * np.pi / 180)
veh2_input['head_angle'] = 180

# append data to test data dictionary
test_inputs['pimpact_x'] = test_inputs['d_impact'] * np.cos(test_inputs['phi_impact'] * np.pi / 180)
test_inputs['pimpact_y'] = test_inputs['d_impact'] * np.sin(test_inputs['phi_impact'] * np.pi / 180)
test_inputs['impact_norm_rad'] = test_inputs['gamma'] * np.pi / 180
test_inputs['barrier_x_pos'] = vehicle_data['barrier']['length'] / 2 + vehicle_data['FordFusion']['lcgf'] + \
                               vehicle_data['FordFusion']['f_hang']
test_inputs['barrier_y_pos'] = test_inputs['d_impact'] * np.sin(test_inputs['phi_impact'] * np.pi / 180)

# compiled test data
all_test_data = {}
all_test_data[current_test] = test_inputs

veh1 = Vehicle('Veh1', veh1_input)
veh2 = Vehicle('Veh2', veh2_input)

initial_position(position_data_static([veh1, veh2]))

sim_inputs = {'cor': 0,
              'cof': 1,
              'impact_norm_deg': current_test_data['gamma']}

name = 'run1'
run = IMPC('run1', veh1, veh2, sim_inputs)
run.results()


# Create simulation for optimization

# function to optimize
def function_optimize(params, test_inputs):
    veh1_input = vehicle_data[test_inputs['vehicle']].copy()  # import vehicle
    veh1_input['vx_initial'] = test_inputs['impact_speed']
    veh1_input['pimpact_x'] = test_inputs['pimpact_x']
    veh1_input['pimpact_y'] = test_inputs['pimpact_y']
    veh1_input['impact_norm_rad'] = test_inputs['impact_norm_rad']

    veh2_input = vehicle_data[test_inputs['barrier']].copy()  # import barrier
    veh2_input['init_x_pos'] = test_inputs['barrier_x_pos']
    veh2_input['init_y_pos'] = test_inputs['barrier_y_pos']

    veh1 = Vehicle('Veh1', veh1_input)
    veh2 = Vehicle('Veh2', veh2_input)

    sim_inputs = {'cor': params[0],
                  'cof': params[1],
                  'impact_norm_deg': params[2]}
    name = 'run1'
    run = IMPC(name, veh1, veh2, sim_inputs)

    diff_dv_x = run.v1_result['dvx'] - test_inputs['dvx_test']
    diff_dv_y = run.v1_result['dvy'] - test_inputs['dvy_test']
    diff_omega = run.v1_result['oz_deg'] - test_inputs['domega_test']

    omega_scale = 0.23327

    sim_error = np.sqrt(diff_dv_x ** 2 + diff_dv_y ** 2 + (omega_scale * diff_omega) ** 2)
    print(f'Error: {sim_error}')

    return sim_error


def print_callback(params):
    print(params)


x0 = np.array([0.3, 0.3, -270])
# x0 = [0.3, 0.3, 0]
bounds = Bounds([0, 0.4], [0, .6], [0, -180])
bnds = ((0, 1), (0, 1), (-270, -1))
res = minimize(function_optimize, x0, args=(test_inputs,), method='Powell',
               options={'disp': True}, bounds=bnds, callback=print_callback)

sim_inputs = {'cor': res.x[0],
              'cof': res.x[1],
              'impact_norm_deg': res.x[2]}

optimized_inputs = {}
optimized_inputs[current_test] = sim_inputs

run = IMPC(current_test, veh1, veh2, sim_inputs)
run.results()

all_test_data[current_test]['impact_norm_rad'] = res.x[2] * np.pi / 180
all_test_data[current_test]['cor_optimized'] = res.x[0]
all_test_data[current_test]['cof_optimized'] = res.x[1]
all_test_data[current_test]['error'] = 3.89547721958819


# save
with open(os.path.join(report_dir, 'optimized_inputs.pkl'), 'wb') as handle:
    pickle.dump(optimized_inputs, handle, protocol=pickle.HIGHEST_PROTOCOL)

with open(os.path.join(report_dir, 'all_test_data.pkl'), 'wb') as handle:
    pickle.dump(all_test_data, handle, protocol=pickle.HIGHEST_PROTOCOL)
