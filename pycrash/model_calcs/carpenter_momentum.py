"""
class for static impulse momentum model
"""
from pycrash.impc import impc_calcs
import numpy as np
from copy import deepcopy


class IMPC():
    def __init__(self, name, veh1, veh2, sim_inputs):
        self.name = name
        self.type = 'impc_carpenter'  # class type for saving files
        self.veh1 = deepcopy(veh1)
        self.veh2 = deepcopy(veh2)

        impactp_gx = self.veh1.init_x_pos + self.veh1.pimpact_x * np.cos(self.veh1.head_angle * np.pi / 180) - self.veh1.pimpact_y * np.sin(self.veh1.head_angle * np.pi / 180)
        impactp_gy = self.veh1.init_y_pos + self.veh1.pimpact_x * np.sin(self.veh1.head_angle * np.pi / 180) + self.veh1.pimpact_y * np.cos(self.veh1.head_angle * np.pi / 180)
        self.poi_veh2x = ((impactp_gx-self.veh2.init_x_pos) * np.cos(self.veh2.head_angle * np.pi / 180) + (impactp_gy-self.veh2.init_y_pos) * np.sin(self.veh2.head_angle * np.pi / 180))
        self.poi_veh2y = (-1 * (impactp_gx-self.veh2.init_x_pos) * np.sin(self.veh2.head_angle * np.pi / 180) + (impactp_gy-self.veh2.init_y_pos) * np.cos(self.veh2.head_angle * np.pi / 180))

        # convert input speeds to fps
        self.veh1.vx_initial = self.veh1.vx_initial * 1.46667
        self.veh1.vy_initial = self.veh1.vy_initial * 1.46667
        self.veh2.vx_initial = self.veh2.vx_initial * 1.46667
        self.veh2.vy_initial = self.veh2.vy_initial * 1.46667

        self.v1_result, self.v2_result = impc_calcs(self.veh1, self.veh2, self.poi_veh2x, self.poi_veh2y, sim_inputs)

    def results(self):
        print('Vehicle 1:')
        print(self.v1_result)
        print(f"PDOF Veh1: {np.arctan(self.v1_result['dvy'] / self.v1_result['dvx']) * 180 / np.pi}")
        print('')
        print('Vehicle 2:')
        print(self.v2_result)
        print(f"PDOF Veh2: {np.arctan(self.v2_result['dvy'] / self.v2_result['dvx']) * 180 / np.pi}")
