import sys
machine = 'ubuntu'
if machine == 'ubuntu':
    sys.path.insert(0, '/home/jmc/Documents/pycrash/')
    sys.path.insert(0, '/home/jmc/Documents/pycrash/projects/validation impact momentum/src/')
    report_dir = '/home/jmc/Documents/pycrash/projects/validation impact momentum/reports/'
    input_dir = '/home/jmc/Documents/pycrash/projects/validation impact momentum/data/input'
elif machine == 'biocore':
    sys.path.insert(0, 'D:\\OneDrive\\pycrash\\')
    sys.path.insert(0, 'D:\\OneDrive\\pycrash\\projects\\validation impact momentum\\src')
    report_dir = 'D:\\OneDrive\\pycrash\\projects\\validation impact momentum\\reports\\'

import numpy as np
import pickle
from scipy.optimize import minimize
from scipy.optimize import brute
from scipy.optimize import fmin
from scipy.optimize import Bounds
from pycrash.vehicle import Vehicle
from pycrash.model_calcs.carpenter_momentum import IMPC
from pycrash.visualization.initial_positions import initial_position
from pycrash.model_calcs.position_data import position_data_static
import os

from vehicle_data_collection import vehicle_data
from optimizer_function import function_optimize, print_callback

# load saved data - Brach test matrix
with open(os.path.join(input_dir, 'brachTestData.pkl'), 'rb') as handle:
    test_data = pickle.load(handle)

# load saved data - pycrash inputs / outputs
with open(os.path.join(report_dir, 'all_test_data.pkl'), 'rb') as handle:
    all_test_data = pickle.load(handle)

# Brach Test Data
test_list = list(test_data.keys())
current_test = test_list[20]
test_inputs = test_data[current_test]
print(f'Current Test: {current_test}')
test_inputs['vehicle'] = 'FordFusion'  # run all with Fusion for now


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
test_inputs['barrier_x_pos'] = vehicle_data['barrier']['length'] / 2 + vehicle_data['FordFusion']['lcgf'] + vehicle_data['FordFusion']['f_hang']
test_inputs['barrier_y_pos'] = test_inputs['d_impact'] * np.sin(test_inputs['phi_impact'] * np.pi / 180)

# compiled test data
#all_test_data = {}
all_test_data[current_test] = test_inputs

veh1 = Vehicle('Veh1', veh1_input)
veh2 = Vehicle('Veh2', veh2_input)

#initial_position(position_data_static([veh1, veh2]))

# optimze inputs using brute force method
x0 = np.array([0, 1, -270])   # <- initial guess for cor, cof, normal impact plane vector
bnds = ((0, 0.15), (0, 10), (-360, -1))  # <- bounds for each variable
#res = minimize(function_optimize, x0, args=(test_inputs,), method='L-BFGS-B',
#               options={'disp': True}, bounds=bnds, callback=print_callback)
#res = fmin(function_optimize, bnds, args=(test_inputs,), full_output=True)
res = brute(function_optimize, ranges=bnds, args=(test_inputs,), full_output=True, finish=None)
print(f'{current_test} -> Inputs at global minimum: {res[0]}')
print(f'{current_test} -> Error at global minimum: {res[1]}')

sim_inputs = {'cor': res[0][0],
              'cof': res[0][1],
              'impact_norm_deg': res[0][2]}
print(f'Simulation inputs for {current_test}: {sim_inputs.values()}')

run = IMPC(current_test, veh1, veh2, sim_inputs)
run.results()


all_test_data[current_test]['sim_dvx'] = run.v1_result['dvx']
all_test_data[current_test]['sim_dvy'] = run.v1_result['dvy']
all_test_data[current_test]['sim_pdof'] = np.arctan(run.v1_result['dvy'] / run.v1_result['dvx']) * 180 / np.pi
all_test_data[current_test]['sim_domega'] = run.v1_result['oz_deg']
all_test_data[current_test]['impact_norm_rad'] = sim_inputs['impact_norm_deg'] * np.pi / 180
all_test_data[current_test]['cor_optimized'] = sim_inputs['cor']
all_test_data[current_test]['cof_optimized'] = sim_inputs['cof']

# calculate error for final model
diff_dv_x = run.v1_result['dvx'] - test_inputs['dvx_test']
diff_dv_y = run.v1_result['dvy'] - test_inputs['dvy_test']
diff_omega = run.v1_result['oz_deg'] - test_inputs['domega_test']
omega_scale = 0.23327
all_test_data[current_test]['error'] = np.sqrt(diff_dv_x ** 2 + diff_dv_y ** 2 + (omega_scale * diff_omega) ** 2)

# save
with open(os.path.join(report_dir, 'all_test_data.pkl'), 'wb') as handle:
    pickle.dump(all_test_data, handle, protocol=pickle.HIGHEST_PROTOCOL)
