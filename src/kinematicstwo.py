"""
Calculated vehicle premotion
Dependencies = tire model
Inputs - pulled from Vehicle class - initial speed (static), variable - braking / steering
Interpolates braking steering with time / distance
"""

from src.tire import tire_model
from src.functions import vehicle_data, constants, premotion
from src.vehicle import Vehicle
from data.defaults.config import default_dict
import pandas as pd
import numpy as np
from scipy import integrate
from copy import deepcopy
import math
import csv
import os

# load defaults
mu_max = default_dict['mu_max']                 # maximum available friction
dt_motion = default_dict['dt_motion']           # iteration time step
dt_impact = default_dict['dt_impact']           # impact time step

# look for Environment data, load if present
if os.path.isfile(os.path.join(os.getcwd(), "data", "input", "environment.csv")):
    enviro = pd.read_csv(os.path.join(os.getcwd(), "data", "input", "environment.csv"))
    if len(enviro) == 0:
        print('Environment file appears blank - no terrian data used')
        print(f'Constant friction {mu_max} used throughout')
    else:
        print('TODO - process terrain data')
else:
    print('No Environment File Provided')


class KinematicsTwo():
    """
    Generates vehicle motion based on inputs defined within Vehicle class
    No external forces
    Environment slope and bank is optionally defined as a function of X,Y components
    creates independent copy of vehicle at instantiation
    """
    def __init__(self, name, veh1, veh2):
        self.name = name
        self.type = 'twomotion'  # class type for saving files
        self.veh1 = deepcopy(veh1)
        self.veh2 = deepcopy(veh2)
        # check for driver inputs - Vehicle 1
        if isinstance(self.veh1.driver_input, pd.DataFrame):
            print(f"Driver input for {self.veh1.name} of shape = {self.veh1.driver_input.shape}")
        else:
            print(f'Driver input for {self.veh1.name} not provided - no braking or steering applied')
            print(f'Current driver input of type: {type(self.veh1.driver_input)}')
            end_time = int(input('Enter duration for simulation (seconds):'))
            t = list(np.arange(0, end_time+dt_motion, dt_motion))  # create time array from 0 to end time from user
            throttle = [0] * len(t)
            brake = [0] * len(t)
            steer = [0] * len(t)
            driver_input_dict = {'t':t, 'throttle':throttle, 'brake':brake, 'steer':steer}
            self.veh1.driver_input = pd.DataFrame.from_dict(driver_input_dict)
            print(f'Driver inputs for {self.veh1.name} set to zero for {end_time} seconds')
        # check for driver inputs - Vehicle 2
        if isinstance(self.veh2.driver_input, pd.DataFrame):
            print(f"Driver input for {self.veh2.name} of shape = {self.veh2.driver_input.shape}")
        else:
            print(f'Driver input for {self.veh2.name} not provided - no braking or steering applied')
            print(f'Current driver input of type: {type(self.veh2.driver_input)}')
            end_time = int(input('Enter duration for simulation (seconds):'))
            t = list(np.arange(0, end_time+dt_motion, dt_motion))  # create time array from 0 to end time from user
            throttle = [0] * len(t)
            brake = [0] * len(t)
            steer = [0] * len(t)
            driver_input_dict = {'t':t, 'throttle':throttle, 'brake':brake, 'steer':steer}
            self.veh2.driver_input = pd.DataFrame.from_dict(driver_input_dict)
            print(f'Driver inputs for {self.veh2.name} set to zero for {end_time} seconds')

         # run vehicle models iteratively to evaluate for impact
         self.veh_motion = vehicle_model(self.veh)

         # create point data in vehicle and global frame
         self.p_vx, self.p_vy, self.p_gx, self.p_gy = position_data(self.veh_motion)
