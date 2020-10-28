import numpy as np
from pycrash.vehicle import Vehicle
from pycrash.model_calcs.carpenter_momentum import IMPC
from vehicle_data_collection import vehicle_data

# function to optimize
def function_optimize(params, test_inputs):
    veh1_input = vehicle_data[test_inputs['vehicle']].copy()  # import vehicle
    veh1_input['vx_initial'] = test_inputs['impact_speed']
    veh1_input['pimpact_x'] = test_inputs['pimpact_x']
    veh1_input['pimpact_y'] = test_inputs['pimpact_y']
    #veh1_input['impact_norm_rad'] = test_inputs['impact_norm_rad']

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
    print(sim_inputs)
    print(f'Sim Error: {sim_error}')

    return sim_error


def print_callback(params):
    print(params)

