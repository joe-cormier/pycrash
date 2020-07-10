"""
Calculated vehicle premotion
Dependencies = tire model
Inputs - pulled from Vehicle class - initial speed (static), variable - braking / steering

"""

import pandas as pd
import numpy as np
from scipy import integrate
import matplotlib.pyplot as plt
from copy import deepcopy
from src.vehicle_model import vehicle_model
import math
import csv
import os

# TODO: create inputs for plots
figure_size = (16,9)

# load constants
with open(os.path.join(os.getcwd(), "data", "input", "constants.csv")) as csvfile:
    readCSV = csv.reader(csvfile, delimiter=',')
    cons = {}
    for row in readCSV:
        cons[row[1]] = row[2]

mu_max = float(cons['mu_max'])                  # maximum available friction
dt_motion = float(cons['dt_motion'])           # iteration time step for vehicle motion


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


class SingleMotion():
    """
    Generates vehicle motion based on inputs defined within Vehicle class
    No external forces
    Environment slope and bank is optionally defined as a function of X,Y components
    creates independent copy of vehicle at instantiation
    """
    def __init__(self, name, veh):
        self.name = name
        self.type = 'kinematic'  # class type for saving files
        self.veh = deepcopy(veh)
        # check for driver inputs
        if isinstance(self.veh.driver_input, pd.DataFrame):
            print(f"Driver input for {self.veh.name} of shape = {self.veh.driver_input.shape}")
        else:
            print(f'Driver input for {self.veh.name} not provided - no braking or steering applied')
            print(f'Current driver input of type: {type(self.veh.driver_input)}')
            end_time = int(input('Enter duration for simulation (seconds):'))
            t = list(np.arange(0, end_time+dt_motion, dt_motion))  # create time array from 0 to end time from user
            throttle = [0] * len(t)
            brake = [0] * len(t)
            steer = [0] * len(t)
            driver_input_dict = {'t':t, 'throttle':throttle, 'brake':brake, 'steer':steer}
            self.veh.driver_input = pd.DataFrame.from_dict(driver_input_dict)
            print(f'Driver inputs for {self.veh.name} set to zero for {end_time} seconds')

        # TODO: need to check if time in driver_inputs is the correct dt? 

        # run vehicle model
        self.veh_motion = vehicle_model(self.veh)



    def vehicle_info(self):
        """
        get input on the vehicle used to create Kinematics object
        """
        print(f'Vehicle name is {self.veh.name}')


    def plot_motion(self):
        fig, axs = plt.subplots(3, 2, figsize=figure_size, sharex='col')
        axs[0,0].set_ylabel('Velocity (mph)', color='k')
        axs[0,0].plot(self.veh_motion.t, self.veh_motion.Vx / 1.46667, color='k', label = 'Vx')    
        axs[0,0].plot(self.veh_motion.t, self.veh_motion.Vy / 1.46667, color='b', label = 'Vy')
        axs[0,0].plot(self.veh_motion.t, self.veh_motion.Vr / 1.46667, color = 'g', linestyle='dashed', label = 'V')
        axs[0,0].tick_params(axis='y', labelcolor='k')
        axs[0,0].legend(frameon = False)

        axs[0,1].set_ylabel('Acceleration (g)', color='k')
        axs[0,1].tick_params(axis='y', labelcolor='k')
        axs[0,1].plot(self.veh_motion.t, self.veh_motion.Ax/32.2, color='k', label = 'Ax')
        axs[0,1].plot(self.veh_motion.t, self.veh_motion.Ay/32.2, color='b', label = 'Ay')
        axs[0,1].plot(self.veh_motion.t, self.veh_motion.ax/32.2, color='k', linestyle='dashed', label = 'ax')
        axs[0,1].plot(self.veh_motion.t, self.veh_motion.ay/32.2, color='b', linestyle='dashed', label = 'ay')
        axs[0,1].legend(frameon = False)

        axs[1,0].set_ylabel('Forward Tire Forces (lb)', color='k')
        axs[1,0].tick_params(axis='y', labelcolor='k')
        axs[1,0].plot(self.veh_motion.t, self.veh_motion.lf_fx, color='b', label = 'LF')
        axs[1,0].plot(self.veh_motion.t, self.veh_motion.rf_fx, color='g', label = 'RF')
        axs[1,0].plot(self.veh_motion.t, self.veh_motion.rr_fx, color='m', label = 'RR')
        axs[1,0].plot(self.veh_motion.t, self.veh_motion.lr_fx, color='orange', label = 'LR')
        axs[1,0].legend(frameon = False)

        axs[1,1].set_ylabel('Rightward Tire Forces (lb)', color='k')
        axs[1,1].tick_params(axis='y', labelcolor='k')
        axs[1,1].plot(self.veh_motion.t, self.veh_motion.lf_fy, color='b', label = 'LF')
        axs[1,1].plot(self.veh_motion.t, self.veh_motion.rf_fy, color='g', label = 'RF')
        axs[1,1].plot(self.veh_motion.t, self.veh_motion.rr_fy, color='m', label = 'RR')
        axs[1,1].plot(self.veh_motion.t, self.veh_motion.lr_fy, color='orange', label = 'LR')
        axs[1,1].legend(frameon = False)

        axs[2,0].set_xlabel('Time (s)')
        axs[2,0].set_ylabel('Omega (deg/s), Alpha (deg/s/s)', color='k')
        axs[2,0].tick_params(axis='y', labelcolor='k')
        axs[2,0].plot(self.veh_motion.t, self.veh_motion.oz_deg, color='k', label = 'Omega')
        axs[2,0].plot(self.veh_motion.t, self.veh_motion.alphaz_deg, color='r', label = 'Alpha')
        axs[2,0].legend(frameon = False)

        axs[2,1].set_xlabel('Time (s)')
        axs[2,1].set_ylabel('Heading Angle (deg)', color='k')
        axs[2,1].tick_params(axis='y', labelcolor='k')
        axs[2,1].plot(self.veh_motion.t, self.veh_motion.theta_deg, color='k')

        plt.subplots_adjust(wspace=0.2, hspace = .1)
        plt.show()

    def CG_motion(self):
        """
        plot location of CG in global reference frame
        """
        fig = plt.figure(figsize=figure_size)
        ax = fig.gca()
        # determine extent of vehicle plot
        min_x_axis = min(self.veh_motion.Dx) - 20
        max_x_axis = max(self.veh_motion.Dx) + 20
        
        min_y_axis = min(self.veh_motion.Dy) - 20
        max_y_axis = max(self.veh_motion.Dy) + 20        

        ax.set_xticks(np.arange(min_x_axis, max_x_axis, 20))
        ax.set_yticks(np.arange(min_y_axis, max_y_axis, 20))
        plt.scatter(self.veh_motion.Dx, self.veh_motion.Dy, label = f'{self.veh.name}')

        plt.xlim([min_x_axis, max_x_axis])
        plt.ylim([min_y_axis, max_y_axis])

        plt.grid()
        plt.gca().invert_yaxis()
        plt.show()



