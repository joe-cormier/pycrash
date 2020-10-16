
import numpy as np
from pycrash.vehicle import Vehicle
from pycrash.model_calcs.carpenter_momentum import IMPC


sim_inputs = {'cor': 0.1,
              'cof': 0.3,
              'impact_norm_rad': 0}

vehicle1_input_dict = {"year": 2016,
                       "make": "Subaru",
                       "model": "WRX Sti",
                       "weight": 3200,
                       "steer_ratio": 16.5,
                       "init_x_pos": 0,
                       "init_y_pos": 0,
                       "head_angle": 0 * np.pi / 180,  # <- vehicle heading angle
                       "width": 6,
                       "length": 19.3,
                       "hcg": 1,
                       "lcgf": 4.88,
                       "lcgr": 6.96,
                       "wb": 11.84,
                       "track": 6.6,
                       "f_hang": 3.2,
                       "r_hang": 4.1,
                       "tire_d": 2.716666667,
                       "tire_w": 0.866666667,
                       "izz": 2500,
                       "vx_initial": 15,
                       "vy_initial": 0,
                       "omega_z": 0,
                       "pimpact_x": 8.08,
                       "pimpact_y": 0,
                       "impact_norm_rad": (0 * np.pi / 180)}  # <- normal impact plane angle

vehicle2_input_dict = {"year": 2016,
                       "make": "Subaru",
                       "model": "WRX Sti",
                       "weight": 3200,
                       "steer_ratio": 16.5,
                       "init_x_pos": 11,
                       "init_y_pos": -4,
                       "head_angle": 270 * np.pi / 180,  # <- vehicle heading angle
                       "width": 6,
                       "length": 19.3,
                       "hcg": 1,
                       "lcgf": 4.88,
                       "lcgr": 6.96,
                       "wb": 11.84,
                       "track": 6.6,
                       "f_hang": 3.2,
                       "r_hang": 4.1,
                       "tire_d": 2.716666667,
                       "tire_w": 0.866666667,
                       "izz": 2500,
                       "vx_initial": 15,
                       "vy_initial": 0,
                       "omega_z": 0}

veh1 = Vehicle('Veh1', vehicle1_input_dict)
veh2 = Vehicle('Veh2', vehicle2_input_dict)
name = 'run1'

run = IMPC('run1', veh1, veh2, sim_inputs)

print(run.poi_veh2x)
print(run.poi_veh2y)

run.results()