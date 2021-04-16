"""
Calculated vehicle premotion
Dependencies = tire model
Inputs - pulled from Vehicle class - initial speed (static), variable - braking / steering
Interpolates braking steering with time / distance
"""

import matplotlib.pyplot as plt
from .data.defaults.config import default_dict
from copy import deepcopy
from .multi_vehicle_model import multi_vehicle_model
from pycrash.model_calcs.position_data import position_data_motion, position_data_static
from .visualization.vehicle import plot_driver_inputs
from .visualization.model_interval_two_vehicles import plot_motion_interval
from .visualization.initial_positions import initial_position
from .model_calcs.collision_plane import define_impact_plane, define_impact_edge
import pandas as pd
import numpy as np
import os

# load defaults
mu_max = default_dict['mu_max']  # maximum available friction
dt_motion = default_dict['dt_motion']  # iteration time step
dt_impact = default_dict['dt_impact']  # impact time step

figure_size = (16, 9)
xy_ratio = figure_size[0] / figure_size[1]

# TODO: add environmental data inputs (slope, bank, friction)
""" 
if os.path.isfile(os.path.join(os.getcwd(), "data", "input", "environment.csv")):
    enviro = pd.read_csv(os.path.join(os.getcwd(), "data", "input", "environment.csv"))
    if len(enviro) == 0:
        print('Environment file appears blank - no terrian data used')
        print(f'Constant friction {mu_max} used throughout')
    else:
        print('TODO - process terrain data')
else:
    print('No Environment File Provided')
"""

class KinematicsTwo():
    """
    Generates vehicle motion based on inputs defined within Vehicle class
    No external forces
    Environment slope and bank is optionally defined as a function of X,Y components
    creates independent copy of vehicle at instantiation
    """

    def __init__(self, name, impact_type, veh1, veh2, mutual_stiffness=None, vehicle_friction=None, user_sim_defaults=None):
        self.name = name
        self.type = 'multimotion'  # class type for saving files
        self.veh1 = deepcopy(veh1)
        self.veh2 = deepcopy(veh2)

        if (impact_type not in ["SS", "IMPC"]):
            # TODO: add ability to use force-displacement data
            print("Not a valid impact type, choose SS, IMPC")
            impact_type = input("Enter an impact type of SS or IMPC: ")

            if (impact_type not in ["SS", "IMPC"]):
                print("Not a valid impact type - value set to None")
                self.impact_type == None
            else:
                self.impact_type = impact_type
        else:
            self.impact_type = impact_type
            if vehicle_friction:
                self.veh_mu = vehicle_friction
            elif self.impact_type == 'SS':
                print(f"Vehicle friction for {self.name} is empty")
                self.veh_mu = float(input("Enter value for intervehicular friction: "))

        if impact_type == 'SS':
            if mutual_stiffness:
                self.kmutual = mutual_stiffness
            else:
                print(f"Mutual Stiffness for {self.name} is empty")
                self.kmutual = float(input("Enter value for mutual stiffness (lb/ft): "))
            if vehicle_friction:
                self.vehicle_mu = vehicle_friction
            else:
                print(f"Intervehicular friction for {self.name} is empty")
                self.vehicle_mu = float(input("Enter value for sliding friction: "))
        # load defaults
        if user_sim_defaults:
            # TODO: create check for user sim_defaults_input
            self.sim_defaults = user_sim_defaults
        else:
            self.sim_defaults = {'dt_motion': 0.01,
                                 'mu_max': 0.76,
                                 'alpha_max': 0.174533,  # 10 degrees
                                 'vehicle_mu': 0.6,
                                 'cor': 0.1}

        # check for driver inputs - Vehicle 1
        if isinstance(self.veh1.driver_input, pd.DataFrame):
            print(f"Driver input for {self.veh1.name} of shape = {self.veh1.driver_input.shape}")
        else:
            print(f'Driver input for {self.veh1.name} not provided - no braking or steering applied')
            print(f'Current driver input of type: {type(self.veh1.driver_input)}')
            end_time = int(input('Enter duration for simulation (seconds):'))
            t = list(np.arange(0, end_time + dt_motion, dt_motion))  # create time array from 0 to end time from user
            throttle = [0] * len(t)
            brake = [0] * len(t)
            steer = [0] * len(t)
            driver_input_dict = {'t': t, 'throttle': throttle, 'brake': brake, 'steer': steer}
            self.veh1.driver_input = pd.DataFrame.from_dict(driver_input_dict)
            print(f'Driver inputs for {self.veh1.name} set to zero for {end_time} seconds')

        # check for driver inputs - Vehicle 2
        if isinstance(self.veh2.driver_input, pd.DataFrame):
            print(f"Driver input for {self.veh2.name} of shape = {self.veh2.driver_input.shape}")
        else:
            print(f'Driver input for {self.veh2.name} not provided - no braking or steering applied')
            print(f'Current driver input of type: {type(self.veh2.driver_input)}')
            end_time = int(input('Enter duration for simulation (seconds):'))
            t = list(np.arange(0, end_time + dt_motion, dt_motion))  # create time array from 0 to end time from user
            throttle = [0] * len(t)
            brake = [0] * len(t)
            steer = [0] * len(t)
            driver_input_dict = {'t': t, 'throttle': throttle, 'brake': brake, 'steer': steer}
            self.veh2.driver_input = pd.DataFrame.from_dict(driver_input_dict)
            print(f'Driver inputs for {self.veh2.name} set to zero for {end_time} seconds')

        """ impact points and edge detection """
        # TODO: convert sideswipe to lists of tuples like impc
        if self.impact_type == 'SS':
            if all(hasattr(self.veh1, attr) for attr in ["pimpact_x", "pimpact_y"]):
                print(f'Predefined impact point for {self.veh1.name}: x={self.veh1.pimpact_x:.1f}, y={self.veh1.pimpact_y:.1f}')
                if len(self.veh1.pimpact_x) != len(self.veh1.pimpact_x):
                    print(f'Unequal lengths for x ({len(self.veh1.pimpact_x)}) and y ({len(self.veh1.pimpact_y)}) impact points')
                else:
                    self._impactPoints = len(self.veh1.pimpact_x)
            else:
                print(f"Create impact point(s) for {self.veh1.name} = striking vehicle")
                print("")
                self.veh1 = define_impact_plane(veh1, iplane=False)
        else:
            if all(hasattr(self.veh1, attr) for attr in 'impact_points'):  # ["pimpact_x", "pimpact_y", "impact_norm_rad"]
                print(f'Predefined impact points for {self.veh1.name}: (x (ft), y (ft), impact plane angle (deg)) = {self.veh1.impact_points:.1f}')
            else:
                self.veh1.num_impact_points = int(input('Enter number of impact points to define:'))
                print(f"Create impact plane for {self.veh1.name} = striking vehicle")
                print("")
                self.veh1.impactNum = 0    # counter for the number of impacts in simulation
                self.veh1 = define_impact_plane(veh1)

        if all(hasattr(self.veh2, attr) for attr in ["edgeimpact_x1", "edgeimpact_y1", "edgeimpact_x2", "edgeimpact_y2", "edgeimpact"]):
            print(f'Predefined impact edge for {self.veh2.name} x1={self.veh2.edgeimpact_x1:.1f}, y1={self.veh2.edgeimpact_y1}; x2={self.veh2.edgeimpact_x2:.1f}, y2={self.veh2.edgeimpact_y2:.1f}')
        else:
            print(f"Create impacting edge for {self.veh2.name} = struck vehicle")
            print("")
            self.veh2 = define_impact_edge(veh2, iplane=False)

    def plot_inputs(self):
        for veh in [self.veh1, self.veh2]:
            plot_driver_inputs(veh)

    def plot_motion(self):
        for veh in [self.veh1, self.veh2]:
            fig, axs = plt.subplots(3, 2, figsize=figure_size, sharex='col')
            fig.suptitle(f'{veh.name}', fontsize=16)
            axs[0, 0].set_ylabel('Velocity (mph)', color='k')
            axs[0, 0].plot(self.model.t, self.model.Vx / 1.46667, color='k', label='Vx')
            axs[0, 0].plot(self.model.t, self.model.Vy / 1.46667, color='b', label='Vy')
            axs[0, 0].plot(self.model.t, self.model.Vr / 1.46667, color='g', linestyle='dashed', label='V')
            axs[0, 0].tick_params(axis='y', labelcolor='k')
            axs[0, 0].legend(frameon=False)

            axs[0, 1].set_ylabel('Acceleration (g)', color='k')
            axs[0, 1].tick_params(axis='y', labelcolor='k')
            axs[0, 1].plot(self.model.t, self.model.Ax / 32.2, color='k', label='Ax')
            axs[0, 1].plot(self.model.t, self.model.Ay / 32.2, color='b', label='Ay')
            axs[0, 1].plot(self.model.t, self.model.ax / 32.2, color='k', linestyle='dashed', label='ax')
            axs[0, 1].plot(self.model.t, self.model.ay / 32.2, color='b', linestyle='dashed', label='ay')
            axs[0, 1].legend(frameon=False)

            axs[1, 0].set_ylabel('Forward Tire Forces (lb)', color='k')
            axs[1, 0].tick_params(axis='y', labelcolor='k')
            axs[1, 0].plot(self.model.t, self.model.lf_fx, color='b', label='LF')
            axs[1, 0].plot(self.model.t, self.model.rf_fx, color='g', label='RF')
            axs[1, 0].plot(self.model.t, self.model.rr_fx, color='m', label='RR')
            axs[1, 0].plot(self.model.t, self.model.lr_fx, color='orange', label='LR')
            axs[1, 0].legend(frameon=False)

            axs[1, 1].set_ylabel('Rightward Tire Forces (lb)', color='k')
            axs[1, 1].tick_params(axis='y', labelcolor='k')
            axs[1, 1].plot(self.model.t, self.model.lf_fy, color='b', label='LF')
            axs[1, 1].plot(self.model.t, self.model.rf_fy, color='g', label='RF')
            axs[1, 1].plot(self.model.t, self.model.rr_fy, color='m', label='RR')
            axs[1, 1].plot(self.model.t, self.model.lr_fy, color='orange', label='LR')
            axs[1, 1].legend(frameon=False)

            axs[2, 0].set_xlabel('Time (s)')
            axs[2, 0].set_ylabel('Omega (deg/s), Alpha (deg/s/s)', color='k')
            axs[2, 0].tick_params(axis='y', labelcolor='k')
            axs[2, 0].plot(self.model.t, self.model.oz_deg, color='k', label='Omega')
            axs[2, 0].plot(self.model.t, self.model.alphaz_deg, color='r', label='Alpha')
            axs[2, 0].legend(frameon=False)

            axs[2, 1].set_xlabel('Time (s)')
            axs[2, 1].set_ylabel('Heading Angle (deg)', color='k')
            axs[2, 1].tick_params(axis='y', labelcolor='k')
            axs[2, 1].plot(self.veh_motion.t, self.veh_motion.theta_deg, color='k')

            plt.subplots_adjust(wspace=0.2, hspace=.1)
            plt.show()

    # plot initial positions and any motion data to show vehicle paths
    def show_initial_position(self, i=0):
        # TODO: future - can choose a time point
        [self.veh1, self.veh2] = position_data_static([self.veh1, self.veh2])
        initial_position(self.veh1, self.veh2, i)

    # run vehicle models
    def simulate(self, ignore_driver=False):
        if self.impact_type == 'SS':
            [self.veh1, self.veh2], self.crush_data = multi_vehicle_model(vehicle_list=[self.veh1, self.veh2], sim_defaults=self.sim_defaults,
                                                                          impact_type=self.impact_type, ignore_driver=ignore_driver, kmutual=self.kmutual, vehicle_mu=self.vehicle_mu)
        else:
            [self.veh1, self.veh2], self.crush_data = multi_vehicle_model(vehicle_list=[self.veh1, self.veh2], sim_defaults=self.sim_defaults,
                                                                          impact_type=self.impact_type, ignore_driver=ignore_driver)
        # get position data
        self.veh1 = position_data_motion(self.veh1, striking=True)
        self.veh2 = position_data_motion(self.veh2)

    def draw_simulation(self, n_intervals, tire_path=True, show_vector=False):
        plot_motion_interval([self.veh1, self.veh2], n_intervals, tire_path=True, show_vector=False)
