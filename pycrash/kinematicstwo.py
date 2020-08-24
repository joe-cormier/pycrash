"""
Calculated vehicle premotion
Dependencies = tire model
Inputs - pulled from Vehicle class - initial speed (static), variable - braking / steering
Interpolates braking steering with time / distance
"""

from scipy import integrate
import matplotlib.pyplot as plt
from .data.defaults.config import default_dict
from copy import deepcopy
from .multi_vehicle_model import multi_vehicle_model
from .position_data import position_data_static, position_data_motion
from .visualization.vehicle import plot_driver_inputs
from .collision_plane import define_impact_plane, define_impact_edge
import pandas as pd
import numpy as np
import math
import csv
import os

# load defaults
mu_max = default_dict['mu_max']                 # maximum available friction
dt_motion = default_dict['dt_motion']           # iteration time step
dt_impact = default_dict['dt_impact']           # impact time step

figure_size = (16,9)
xy_ratio = figure_size[0] / figure_size[1]

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
    def __init__(self, name, impact_type, veh1, veh2, mutual_stiffness = None, vehicle_friction = None):
        self.name = name
        self.type = 'multimotion'             # class type for saving files
        self.veh1 = deepcopy(veh1)
        self.veh2 = deepcopy(veh2)

        if (impact_type not in ["SS", "IMPC"]):
            print("Not a valid impact type, choose SS, IMPC or SDOF")
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
            else:
                print(f"Vehicle friection for {self.name} is empty")
                self.veh_mu = float(input("Enter value for intervehicular friction: "))

        if impact_type == 'SS':
            if mutual_stiffness:
                self.kmutual = mutual_stiffness
            else:
                print(f"Mutual Stiffness for {self.name} is empty")


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


        print(f"Create impact point for {self.veh1.name} = striking vehicle")
        print("")
        self.veh1 = define_impact_plane(veh1)

        print(f"Create impacting edge for {self.veh2.name} = struck vehicle")
        print("")
        self.veh2 = define_impact_edge(veh2, iplane = False)

    def plot_inputs(self):
        for veh in [self.veh1, self.veh2]:
            plot_driver_inputs(veh)

    def plot_motion(self):
        for veh in [self.veh1, self.veh2]:
            fig, axs = plt.subplots(3, 2, figsize=figure_size, sharex='col')
            fig.suptitle(f'{veh.name}', fontsize=16)
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

    # plot initial positions and any motion data to show vehicle paths
    def initial_position(self):
        # plot initial positions
        # grid grid based on initial positoin of vehicle
        # scale x,y axes accordingly
        # get static geometry
        self.veh1, self.veh2 = position_data_static([self.veh1, self.veh2])
        #
        fig = plt.figure(figsize=figure_size)
        ax = fig.gca()

        for veh in [self.veh1, self.veh2]:
            print(f'plotting vehicle {self.veh1.name}')
            bdy_x = (veh.Px.b_lfc, veh.Px.b_rfc, veh.Px.b_rrc, veh.Px.b_lrc, veh.Px.b_lfc)
            bdy_y = (veh.Py.b_lfc, veh.Py.b_rfc, veh.Py.b_rrc, veh.Py.b_lrc, veh.Py.b_lfc)

            lfw_x = (veh.Px.lfw_a, veh.Px.lfw_b, veh.Px.lfw_c, veh.Px.lfw_d, veh.Px.lfw_a)
            lfw_y = (veh.Py.lfw_a, veh.Py.lfw_b, veh.Py.lfw_c, veh.Py.lfw_d, veh.Py.lfw_a)

            rfw_x = (veh.Px.rfw_a, veh.Px.rfw_b, veh.Px.rfw_c, veh.Px.rfw_d, veh.Px.rfw_a)
            rfw_y = (veh.Py.rfw_a, veh.Py.rfw_b, veh.Py.rfw_c, veh.Py.rfw_d, veh.Py.rfw_a)

            rrw_x = (veh.Px.rrw_a, veh.Px.rrw_b, veh.Px.rrw_c, veh.Px.rrw_d, veh.Px.rrw_a)
            rrw_y = (veh.Py.rrw_a, veh.Py.rrw_b, veh.Py.rrw_c, veh.Py.rrw_d, veh.Py.rrw_a)

            lrw_x = (veh.Px.lrw_a, veh.Px.lrw_b, veh.Px.lrw_c, veh.Px.lrw_d, veh.Px.lrw_a)
            lrw_y = (veh.Py.lrw_a, veh.Py.lrw_b, veh.Py.lrw_c, veh.Py.lrw_d, veh.Py.lrw_a)

            plt.plot(bdy_x, bdy_y, 'k')
            plt.scatter(veh.Px.lfw, veh.Py.lfw, c='b')       # left front wheel center
            plt.plot(lfw_x, lfw_y, 'b')
            plt.scatter(veh.Px.rfw, veh.Py.rfw, c='g')       # right front wheel center
            plt.plot(rfw_x, rfw_y, 'g')
            plt.scatter(veh.Px.rrw, veh.Py.rrw, c='m')       # right rear wheel center
            plt.plot(rrw_x, rrw_y,'m')
            plt.scatter(veh.Px.lrw, veh.Py.lrw, c='orange')  # left rear wheel center
            plt.plot(lrw_x, lrw_y, 'orange')
            plt.scatter(veh.Px.cg, veh.Py.cg, s=100, c='k')   # vehicle CG
            # velocity vector
            plt.arrow(veh.Px.cg.iloc[0], veh.Py.cg.iloc[0], veh.Px.vel_v.iloc[0] - veh.Px.cg.iloc[0], veh.Py.vel_v.iloc[0] - veh.Py.cg.iloc[0], head_width=1, head_length=1, fc='r', ec='r')
            # vehicle axes
            plt.arrow(veh.Px.cg.iloc[0], veh.Py.cg.iloc[0], veh.Px.xaxis.iloc[0] - veh.Px.cg.iloc[0], veh.Py.xaxis.iloc[0] - veh.Py.cg.iloc[0], head_width=.5, head_length=0.5, fc='k', ec='k')
            plt.arrow(veh.Px.cg.iloc[0], veh.Py.cg.iloc[0], veh.Px.yaxis.iloc[0] - veh.Px.cg.iloc[0], veh.Py.yaxis.iloc[0] - veh.Py.cg.iloc[0], head_width=.5, head_length=0.5, fc='b', ec='b')

        # determine extent of vehicle plot
        min_x_axis = min([self.veh1.init_x_pos, self.veh2.init_x_pos]) - 20
        max_x_axis = max([self.veh1.init_x_pos, self.veh2.init_x_pos]) + 20
        min_y_axis = min([self.veh1.init_y_pos, self.veh2.init_y_pos]) - 20
        max_y_axis = max([self.veh1.init_y_pos, self.veh2.init_y_pos]) + 20

        """
        dx = max_x_axis - min_x_axis
        dy = max_y_axis - min_y_axis

        if (dx >= dy):
            plt.xlim([min_x_axis, max_x_axis])
            plt.ylim([min_y_axis * xy_ratio, max_y_axis * xy_ratio])
        else:
            plt.xlim([min_x_axis / xy_ratio, max_x_axis / xy_ratio])
            plt.ylim([min_y_axis, max_y_axis])
        """
        plt.xlim([min_x_axis, max_x_axis])
        plt.ylim([min_y_axis, max_y_axis])
        plt.grid()
        plt.gca().invert_yaxis()
        plt.show()

    # run vehicle models iteratively to evaluate for impact
    def simulate(self, ignore_driver=False):
        # run multi vehicle simulation model
        self.veh1, self.veh2, self.crush_data = multi_vehicle_model([self.veh1,self.veh2], self.kmutual, self.vehicle_mu, ignore_driver)
        self.veh1 = position_data_motion(self.veh1, striking = True)
        self.veh2 = position_data_motion(self.veh2)

    def draw_simulation(self, i, tire_path=True):
        # create point data in vehicle and global frame
        """
        Plot Vehicle in Global reference frame
        """
        fig = plt.figure(figsize = figure_size)

        for veh in [self.veh1, self.veh2]:
            bdy_x = (veh.p_gx.b_lfc[i], veh.p_gx.b_rfc[i], veh.p_gx.b_rrc[i], veh.p_gx.b_lrc[i], veh.p_gx.b_lfc[i])
            bdy_y = (veh.p_gy.b_lfc[i], veh.p_gy.b_rfc[i], veh.p_gy.b_rrc[i], veh.p_gy.b_lrc[i], veh.p_gy.b_lfc[i])

            lfw_x = (veh.p_gx.lfw_a[i], veh.p_gx.lfw_b[i], veh.p_gx.lfw_c[i], veh.p_gx.lfw_d[i], veh.p_gx.lfw_a[i])
            lfw_y = (veh.p_gy.lfw_a[i], veh.p_gy.lfw_b[i], veh.p_gy.lfw_c[i], veh.p_gy.lfw_d[i], veh.p_gy.lfw_a[i])

            rfw_x = (veh.p_gx.rfw_a[i], veh.p_gx.rfw_b[i], veh.p_gx.rfw_c[i], veh.p_gx.rfw_d[i], veh.p_gx.rfw_a[i])
            rfw_y = (veh.p_gy.rfw_a[i], veh.p_gy.rfw_b[i], veh.p_gy.rfw_c[i], veh.p_gy.rfw_d[i], veh.p_gy.rfw_a[i])

            rrw_x = (veh.p_gx.rrw_a[i], veh.p_gx.rrw_b[i], veh.p_gx.rrw_c[i], veh.p_gx.rrw_d[i], veh.p_gx.rrw_a[i])
            rrw_y = (veh.p_gy.rrw_a[i], veh.p_gy.rrw_b[i], veh.p_gy.rrw_c[i], veh.p_gy.rrw_d[i], veh.p_gy.rrw_a[i])

            lrw_x = (veh.p_gx.lrw_a[i], veh.p_gx.lrw_b[i], veh.p_gx.lrw_c[i], veh.p_gx.lrw_d[i], veh.p_gx.lrw_a[i])
            lrw_y = (veh.p_gy.lrw_a[i], veh.p_gy.lrw_b[i], veh.p_gy.lrw_c[i], veh.p_gy.lrw_d[i], veh.p_gy.lrw_a[i])

            plt.plot(bdy_x, bdy_y, 'k')
            plt.scatter(veh.p_gx.lfw[i], veh.p_gy.lfw[i], c='b')       # left front wheel center
            plt.plot(lfw_x, lfw_y, 'b')
            plt.scatter(veh.p_gx.rfw[i], veh.p_gy.rfw[i], c='g')       # right front wheel center
            plt.plot(rfw_x, rfw_y, 'g')
            plt.scatter(veh.p_gx.rrw[i], veh.p_gy.rrw[i], c='m')       # right rear wheel center
            plt.plot(rrw_x, rrw_y,'m')
            plt.scatter(veh.p_gx.lrw[i], veh.p_gy.lrw[i], c='orange')  # left rear wheel center
            plt.plot(lrw_x, lrw_y, 'orange')
            plt.scatter(veh.p_gx.cg[i], veh.p_gy.cg[i], s=100, c='k')   # vehicle CG

            if (veh.striking):  # striking vehicle
                plt.scatter(veh.p_gx.pimpact_x[i], veh.p_gy.pimpact_y[i], s = 100, c = 'r') # impact point
            # velocity vector
            plt.arrow(veh.p_gx.cg[i], veh.p_gy.cg[i], veh.p_gx.vel_v[i] - veh.p_gx.cg[i], veh.p_gy.vel_v[i] - veh.p_gy.cg[i], head_width=1, head_length=1, fc='r', ec='r')
            # vehicle axes
            plt.arrow(veh.p_gx.cg[i], veh.p_gy.cg[i], veh.p_gx.xaxis[i] - veh.p_gx.cg[i], veh.p_gy.xaxis[i] - veh.p_gy.cg[i], head_width=.5, head_length=0.5, fc='k', ec='k')
            plt.arrow(veh.p_gx.cg[i], veh.p_gy.cg[i], veh.p_gx.yaxis[i] - veh.p_gx.cg[i], veh.p_gy.yaxis[i] - veh.p_gy.cg[i], head_width=.5, head_length=0.5, fc='b', ec='b')

            # for loop up to i
            if (tire_path):
                for i in range(0, i):
                    if veh.p_gx.loc[i, 'lf_lock'] == 0:
                        plt.scatter(veh.p_gx.loc[i, 'lfw'], veh.p_gy.loc[i, 'lfw'], c = 'b', s = 1, marker = '.')
                    elif veh.p_gx.loc[i, 'lf_lock'] == 1:
                        plt.scatter(veh.p_gx.loc[i, 'lfw'], veh.p_gy.loc[i, 'lfw'], c = 'b', s = 4, marker = 's')

                    if veh.p_gx.loc[i, 'rf_lock'] == 0:
                        plt.scatter(veh.p_gx.loc[i, 'rfw'], veh.p_gy.loc[i, 'rfw'], c = 'g', s = 1, marker = '.')
                    elif veh.p_gx.loc[i, 'rf_lock'] == 1:
                        plt.scatter(veh.p_gx.loc[i, 'rfw'], veh.p_gy.loc[i, 'rfw'], c = 'g', s = 4, marker = 's')

                    if veh.p_gx.loc[i, 'rr_lock'] == 0:
                        plt.scatter(veh.p_gx.loc[i, 'rrw'], veh.p_gy.loc[i, 'rrw'], c = 'm', s = 1, marker = '.')
                    elif veh.p_gx.loc[i, 'rr_lock'] == 1:
                        plt.scatter(veh.p_gx.loc[i, 'rrw'], veh.p_gy.loc[i, 'rrw'], c = 'm', s = 4, marker = 's')

                    if veh.p_gx.loc[i, 'lr_lock'] == 0:
                        plt.scatter(veh.p_gx.loc[i, 'lrw'], veh.p_gy.loc[i, 'lrw'], c = 'orange', s = 1, marker = '.')
                    elif veh.p_gx.loc[i, 'lr_lock'] == 1:
                        plt.scatter(veh.p_gx.loc[i, 'lrw'], veh.p_gy.loc[i, 'lrw'], c = 'orange', s = 4, marker = 's')

        plt.gca().invert_yaxis()
        plt.show()
