import pandas as pd
import numpy as np
from scipy import integrate
import matplotlib.pyplot as plt
from data.defaults.config import default_dict
from copy import deepcopy
from src.vehicle_model import vehicle_model
from src.vehicle_motion_plot import position_data
import math
import csv
import os

# TODO: create inputs for plots
figure_size = (16,9)

# load defaults
mu_max = default_dict['mu_max']    # maximum available friction
dt_motion = default_dict['dt_motion']            # iteration time step

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
        self.type = 'singlemotion'  # class type for saving files
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
        # TODO: check for init_x_pos, init_y_pos

        # run planar vehicle motion simulation
        self.veh_motion = vehicle_model(self.veh)

        # create point data in vehicle and global frame
        self.p_vx, self.p_vy, self.p_gx, self.p_gy = position_data(self.veh_motion)

    def plot_inputs(self):
        fig, ax1 = plt.subplots(figsize = figure_size)
        ax1.scatter(self.veh.driver_input.t, self.veh.driver_inpu.throttle * 100, color='g', label = 'throttle')
        ax1.scatter(self.veh.driver_input.t, self.veh.driver_inpu.brake * 100, color='r', label = 'brake')
        ax2 = ax1.twinx()
        ax2.scatter(self.veh.driver_input.t, self.veh.driver_inpu.steer, color='k', label = 'steer')
        ax1.set_ylabel('Throttle | Brake (%)')
        ax1.set_xlabel('Time (s)')
        ax2.set_ylabel('Steer Angle (deg)')
        plt.legend(frameon = False)
        plt.show()


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

    def draw_vehicle(self, i):
        """
        plots vehicle motion along with velocity vector and coordinate axes
        """

        #  These dataframes link the components together for plotting
        bdy_x = (self.p_vx.b_lfc[i], self.p_vx.b_rfc[i], self.p_vx.b_rrc[i], self.p_vx.b_lrc[i], self.p_vx.b_lfc[i])
        bdy_y = (self.p_vy.b_lfc[i], self.p_vy.b_rfc[i], self.p_vy.b_rrc[i], self.p_vy.b_lrc[i], self.p_vy.b_lfc[i])

        lfw_x = (self.p_vx.lfw_a[i], self.p_vx.lfw_b[i], self.p_vx.lfw_c[i], self.p_vx.lfw_d[i], self.p_vx.lfw_a[i])
        lfw_y = (self.p_vy.lfw_a[i], self.p_vy.lfw_b[i], self.p_vy.lfw_c[i], self.p_vy.lfw_d[i], self.p_vy.lfw_a[i])

        rfw_x = (self.p_vx.rfw_a[i], self.p_vx.rfw_b[i], self.p_vx.rfw_c[i], self.p_vx.rfw_d[i], self.p_vx.rfw_a[i])
        rfw_y = (self.p_vy.rfw_a[i], self.p_vy.rfw_b[i], self.p_vy.rfw_c[i], self.p_vy.rfw_d[i], self.p_vy.rfw_a[i])

        rrw_x = (self.p_vx.rrw_a[i], self.p_vx.rrw_b[i], self.p_vx.rrw_c[i], self.p_vx.rrw_d[i], self.p_vx.rrw_a[i])
        rrw_y = (self.p_vy.rrw_a[i], self.p_vy.rrw_b[i], self.p_vy.rrw_c[i], self.p_vy.rrw_d[i], self.p_vy.rrw_a[i])

        lrw_x = (self.p_vx.lrw_a[i], self.p_vx.lrw_b[i], self.p_vx.lrw_c[i], self.p_vx.lrw_d[i], self.p_vx.lrw_a[i])
        lrw_y = (self.p_vy.lrw_a[i], self.p_vy.lrw_b[i], self.p_vy.lrw_c[i], self.p_vy.lrw_d[i], self.p_vy.lrw_a[i])

        #%% Plot Vehicle in Vehicle reference frame
        plt.figure(figsize = figure_size)
        plt.xlim([-20, 20])
        plt.ylim([-10, 10])

        plt.plot(bdy_x, bdy_y, 'k')
        plt.scatter(self.p_vx.lfw[i], self.p_vy.lfw[i], c = 'b')         # left front wheel center
        plt.plot(lfw_x, lfw_y, 'b')
        plt.scatter(self.p_vx.rfw[i], self.p_vy.rfw[i], c = 'g')         # right front wheel center
        plt.plot(rfw_x, rfw_y, 'g')
        plt.scatter(self.p_vx.rrw[i], self.p_vy.rrw[i], c = 'm')         # right rear wheel center
        plt.plot(rrw_x, rrw_y, 'm')
        plt.scatter(self.p_vx.lrw[i], self.p_vy.lrw[i], c = 'orange')     # left rear wheel center
        plt.plot(lrw_x, lrw_y, 'orange')

        # vehicle CG
        plt.scatter(self.p_vx.cg[i], self.p_vy.cg[i],s = 500, c = 'k')

        # velocity vector
        plt.arrow(self.p_vx.cg[i], draw_vy.cg[i], self.p_vx.vel_v[i] - self.p_vx.cg[i], self.p_vy.vel_v[i] - self.p_vy.cg[i], head_width=.5, head_length=0.5, fc='r', ec='r')

        # vehicle axes
        plt.arrow(self.p_vx.cg[i], self.p_vy.cg[i], self.p_vx.xaxis[i] - self.p_vx.cg[i], self.p_vy.xaxis[i] - self.p_vy.cg[i], head_width=.5, head_length=0.5, fc='k', ec='k')
        plt.arrow(self.p_vx.cg[i], self.p_vy.cg[i], self.p_vx.yaxis[i] - self.p_vx.cg[i], self.p_vy.yaxis[i] - self.p_vy.cg[i], head_width=.5, head_length=0.5, fc='b', ec='b')
        plt.gca().invert_yaxis()
        plt.show()

    def draw_vehicle_motion(self, i, tire_path=True):
        """
        Plot Vehicle in Global reference frame
        """

        bdy_x = (self.p_gx.b_lfc[i], self.p_gx.b_rfc[i], self.p_gx.b_rrc[i], self.p_gx.b_lrc[i], self.p_gx.b_lfc[i])
        bdy_y = (self.p_gy.b_lfc[i], self.p_gy.b_rfc[i], self.p_gy.b_rrc[i], self.p_gy.b_lrc[i], self.p_gy.b_lfc[i])

        lfw_x = (self.p_gx.lfw_a[i], self.p_gx.lfw_b[i], self.p_gx.lfw_c[i], self.p_gx.lfw_d[i], self.p_gx.lfw_a[i])
        lfw_y = (self.p_gy.lfw_a[i], self.p_gy.lfw_b[i], self.p_gy.lfw_c[i], self.p_gy.lfw_d[i], self.p_gy.lfw_a[i])

        rfw_x = (self.p_gx.rfw_a[i], self.p_gx.rfw_b[i], self.p_gx.rfw_c[i], self.p_gx.rfw_d[i], self.p_gx.rfw_a[i])
        rfw_y = (self.p_gy.rfw_a[i], self.p_gy.rfw_b[i], self.p_gy.rfw_c[i], self.p_gy.rfw_d[i], self.p_gy.rfw_a[i])

        rrw_x = (self.p_gx.rrw_a[i], self.p_gx.rrw_b[i], self.p_gx.rrw_c[i], self.p_gx.rrw_d[i], self.p_gx.rrw_a[i])
        rrw_y = (self.p_gy.rrw_a[i], self.p_gy.rrw_b[i], self.p_gy.rrw_c[i], self.p_gy.rrw_d[i], self.p_gy.rrw_a[i])

        lrw_x = (self.p_gx.lrw_a[i], self.p_gx.lrw_b[i], self.p_gx.lrw_c[i], self.p_gx.lrw_d[i], self.p_gx.lrw_a[i])
        lrw_y = (self.p_gy.lrw_a[i], self.p_gy.lrw_b[i], self.p_gy.lrw_c[i], self.p_gy.lrw_d[i], self.p_gy.lrw_a[i])


        fig = plt.figure(figsize = figure_size)
        #plt.xlim([-300, 50])
        #plt.ylim([-100, 100])

        plt.plot(bdy_x, bdy_y, 'k')
        plt.scatter(self.p_gx.lfw[i], self.p_gy.lfw[i], c='b')       # left front wheel center
        plt.plot(lfw_x, lfw_y, 'b')
        plt.scatter(self.p_gx.rfw[i], self.p_gy.rfw[i], c='g')       # right front wheel center
        plt.plot(rfw_x, rfw_y, 'g')
        plt.scatter(self.p_gx.rrw[i], self.p_gy.rrw[i], c='m')       # right rear wheel center
        plt.plot(rrw_x, rrw_y,'m')
        plt.scatter(self.p_gx.lrw[i], self.p_gy.lrw[i], c='orange')  # left rear wheel center
        plt.plot(lrw_x, lrw_y, 'orange')
        plt.scatter(self.p_gx.cg[i], self.p_gy.cg[i], s=100, c='k')   # vehicle CG
        # velocity vector
        plt.arrow(self.p_gx.cg[i], self.p_gy.cg[i], self.p_gx.vel_v[i] * 0.2, self.p_gy.vel_v[i] * 0.2, head_width=.5, head_length=0.5, fc='r', ec='r')
        # vehicle axes
        plt.arrow(self.p_gx.cg[i], self.p_gy.cg[i], self.p_gx.xaxis[i] - self.p_gx.cg[i], self.p_gy.xaxis[i] - self.p_gy.cg[i], head_width=.5, head_length=0.5, fc='k', ec='k')
        plt.arrow(self.p_gx.cg[i], self.p_gy.cg[i], self.p_gx.yaxis[i] - self.p_gx.cg[i], self.p_gy.yaxis[i] - self.p_gy.cg[i], head_width=.5, head_length=0.5, fc='b', ec='b')

        # for loop up to i
        if (tire_path):
            for i in range(0, i):
                if self.p_gx.loc[i, 'lf_lock'] == 0:
                    plt.scatter(self.p_gx.loc[i, 'lfw'], self.p_gy.loc[i, 'lfw'], c = 'b', s = 1, marker = '.')
                elif self.p_gx.loc[i, 'lf_lock'] == 1:
                    plt.scatter(self.p_gx.loc[i, 'lfw'], self.p_gy.loc[i, 'lfw'], c = 'b', s = 4, marker = 's')

                if self.p_gx.loc[i, 'rf_lock'] == 0:
                    plt.scatter(self.p_gx.loc[i, 'rfw'], self.p_gy.loc[i, 'rfw'], c = 'g', s = 1, marker = '.')
                elif self.p_gx.loc[i, 'rf_lock'] == 1:
                    plt.scatter(self.p_gx.loc[i, 'rfw'], self.p_gy.loc[i, 'rfw'], c = 'g', s = 4, marker = 's')

                if self.p_gx.loc[i, 'rr_lock'] == 0:
                    plt.scatter(self.p_gx.loc[i, 'rrw'], self.p_gy.loc[i, 'rrw'], c = 'm', s = 1, marker = '.')
                elif self.p_gx.loc[i, 'rr_lock'] == 1:
                    plt.scatter(self.p_gx.loc[i, 'rrw'], self.p_gy.loc[i, 'rrw'], c = 'm', s = 4, marker = 's')

                if self.p_gx.loc[i, 'lr_lock'] == 0:
                    plt.scatter(self.p_gx.loc[i, 'lrw'], self.p_gy.loc[i, 'lrw'], c = 'orange', s = 1, marker = '.')
                elif self.p_gx.loc[i, 'lr_lock'] == 1:
                    plt.scatter(self.p_gx.loc[i, 'lrw'], self.p_gy.loc[i, 'lrw'], c = 'orange', s = 4, marker = 's')

        plt.gca().invert_yaxis()
        plt.show()
