import pandas as pd
import numpy as np
from copy import deepcopy
from .vehicle_model import vehicle_model
from pycrash.model_calcs.position_data import position_data_motion
from .visualization.vehicle import plot_driver_inputs
from .visualization.kinematics import plot_model
from .visualization.model import plot_motion
from .visualization.tire_details import tire_details, vertical_forces

figure_size = (16, 9)

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

class SingleMotion:
    """
    Generates vehicle motion based on inputs defined within Vehicle class
    No external forces
    Environment slope and bank is optionally defined as a function of X,Y components
    creates independent copy of vehicle at instantiation
    """

    def __init__(self, name, veh, user_sim_defaults=None):
        """
        default values necessary for single motion simulation are loaded when a vehicle is instantiated
        """
        # load defaults
        if user_sim_defaults:
            # TODO: create check for user sim_defaults_input
            sim_defaults = user_sim_defaults
        else:
            sim_defaults = {'dt_motion': 0.01,
                            'mu_max': 0.76,
                            'alpha_max': 0.174533}

        self.mu_max = sim_defaults['mu_max']  # maximum available friction
        self.dt_motion = sim_defaults['dt_motion']  # iteration time step
        self.alpha_max = sim_defaults['alpha_max']  # maximum tire slip angle (rad)


        print(f"Maximum allowable friction: {self.mu_max}")
        print(f"Time step for vehicle motion (s) : {self.dt_motion}")
        print(f"Maximum tire slip angle (deg): {self.alpha_max * 180 / 3.14159:0.2f}")

        self.name = name
        self.type = 'singlemotion'  # class type for saving files
        self.veh = deepcopy(veh)
        self.veh.striking = False  # single vehicle motion will not have contact

        # check for driver inputs
        if isinstance(self.veh.driver_input, pd.DataFrame):
            print(f"Driver input for {self.veh.name} of shape = {self.veh.driver_input.shape}")
        else:
            print(f'Driver input for {self.veh.name} not provided - no braking or steering applied')
            print(f'Current driver input of type: {type(self.veh.driver_input)}')
            end_time = int(input('Enter duration for simulation (seconds):'))
            t = list(np.arange(0, end_time + dt_motion, dt_motion))  # create time array from 0 to end time from user
            throttle = [0] * len(t)
            brake = [0] * len(t)
            steer = [0] * len(t)
            driver_input_dict = {'t': t, 'throttle': throttle, 'brake': brake, 'steer': steer}
            self.veh.driver_input = pd.DataFrame.from_dict(driver_input_dict)
            print(f'Driver inputs for {self.veh.name} set to zero for {end_time} seconds')

        # TODO: need to check if time in driver_inputs is the correct dt?
        # TODO: check for init_x_pos, init_y_pos

        # run planar vehicle motion simulation
        self.veh = vehicle_model(self.veh, sim_defaults)

        # create point data in vehicle and global frame
        self.veh = position_data_motion(self.veh)

    def plot_inputs(self):
        plot_driver_inputs(self.veh)

    def vehicle_info(self):
        """
        get input on the vehicle used to create Kinematics object
        """
        print(f'Vehicle name is {self.veh.name}')

    def plot_model(self):
        plot_model(self.veh)

    def global_motion(self, i):
        plot_motion(self.veh, i)

    def tire_detail(self):
        tire_details(self.veh)
        vertical_forces(self.veh)

    def CG_motion(self):
        """
        plot location of CG in global reference frame
        """
        fig = plt.figure(figsize=figure_size)
        ax = fig.gca()
        # determine extent of vehicle plot
        min_x_axis = min(self.veh.model.Dx) - 20
        max_x_axis = max(self.veh.model.Dx) + 20

        min_y_axis = min(self.veh.model.Dy) - 20
        max_y_axis = max(self.veh.model.Dy) + 20

        ax.set_xticks(np.arange(min_x_axis, max_x_axis, 20))
        ax.set_yticks(np.arange(min_y_axis, max_y_axis, 20))
        plt.scatter(self.veh.model.Dx, self.veh.model.Dy, label=f'{self.veh.name}')

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

        # Plot Vehicle in Vehicle reference frame
        plt.figure(figsize=figure_size)
        plt.xlim([-20, 20])
        plt.ylim([-10, 10])

        plt.plot(bdy_x, bdy_y, 'k')
        plt.scatter(self.p_vx.lfw[i], self.p_vy.lfw[i], c='b')  # left front wheel center
        plt.plot(lfw_x, lfw_y, 'b')
        plt.scatter(self.p_vx.rfw[i], self.p_vy.rfw[i], c='g')  # right front wheel center
        plt.plot(rfw_x, rfw_y, 'g')
        plt.scatter(self.p_vx.rrw[i], self.p_vy.rrw[i], c='m')  # right rear wheel center
        plt.plot(rrw_x, rrw_y, 'm')
        plt.scatter(self.p_vx.lrw[i], self.p_vy.lrw[i], c='orange')  # left rear wheel center
        plt.plot(lrw_x, lrw_y, 'orange')

        # vehicle CG
        plt.scatter(self.p_vx.cg[i], self.p_vy.cg[i], s=500, c='k')

        # velocity vector
        plt.arrow(self.p_vx.cg[i], self.p_vy.cg[i], self.p_vx.vel_v[i] - self.p_vx.cg[i],
                  self.p_vy.vel_v[i] - self.p_vy.cg[i], head_width=.5, head_length=0.5, fc='r', ec='r')

        # vehicle axes
        plt.arrow(self.p_vx.cg[i], self.p_vy.cg[i], self.p_vx.xaxis[i] - self.p_vx.cg[i],
                  self.p_vy.xaxis[i] - self.p_vy.cg[i], head_width=.5, head_length=0.5, fc='k', ec='k')
        plt.arrow(self.p_vx.cg[i], self.p_vy.cg[i], self.p_vx.yaxis[i] - self.p_vx.cg[i],
                  self.p_vy.yaxis[i] - self.p_vy.cg[i], head_width=.5, head_length=0.5, fc='b', ec='b')
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

        fig = plt.figure(figsize=figure_size)
        # plt.xlim([-300, 50])
        # plt.ylim([-100, 100])

        plt.plot(bdy_x, bdy_y, 'k')
        plt.scatter(self.p_gx.lfw[i], self.p_gy.lfw[i], c='b')  # left front wheel center
        plt.plot(lfw_x, lfw_y, 'b')
        plt.scatter(self.p_gx.rfw[i], self.p_gy.rfw[i], c='g')  # right front wheel center
        plt.plot(rfw_x, rfw_y, 'g')
        plt.scatter(self.p_gx.rrw[i], self.p_gy.rrw[i], c='m')  # right rear wheel center
        plt.plot(rrw_x, rrw_y, 'm')
        plt.scatter(self.p_gx.lrw[i], self.p_gy.lrw[i], c='orange')  # left rear wheel center
        plt.plot(lrw_x, lrw_y, 'orange')
        plt.scatter(self.p_gx.cg[i], self.p_gy.cg[i], s=100, c='k')  # vehicle CG
        # velocity vector
        plt.arrow(self.p_gx.cg[i], self.p_gy.cg[i], self.p_gx.vel_v[i] * 0.2, self.p_gy.vel_v[i] * 0.2, head_width=.5,
                  head_length=0.5, fc='r', ec='r')
        # vehicle axes
        plt.arrow(self.p_gx.cg[i], self.p_gy.cg[i], self.p_gx.xaxis[i] - self.p_gx.cg[i],
                  self.p_gy.xaxis[i] - self.p_gy.cg[i], head_width=.5, head_length=0.5, fc='k', ec='k')
        plt.arrow(self.p_gx.cg[i], self.p_gy.cg[i], self.p_gx.yaxis[i] - self.p_gx.cg[i],
                  self.p_gy.yaxis[i] - self.p_gy.cg[i], head_width=.5, head_length=0.5, fc='b', ec='b')

        # for loop up to i
        if (tire_path):
            for i in range(0, i):
                if self.p_gx.loc[i, 'lf_lock'] == 0:
                    plt.scatter(self.p_gx.loc[i, 'lfw'], self.p_gy.loc[i, 'lfw'], c='b', s=1, marker='.')
                elif self.p_gx.loc[i, 'lf_lock'] == 1:
                    plt.scatter(self.p_gx.loc[i, 'lfw'], self.p_gy.loc[i, 'lfw'], c='b', s=4, marker='s')

                if self.p_gx.loc[i, 'rf_lock'] == 0:
                    plt.scatter(self.p_gx.loc[i, 'rfw'], self.p_gy.loc[i, 'rfw'], c='g', s=1, marker='.')
                elif self.p_gx.loc[i, 'rf_lock'] == 1:
                    plt.scatter(self.p_gx.loc[i, 'rfw'], self.p_gy.loc[i, 'rfw'], c='g', s=4, marker='s')

                if self.p_gx.loc[i, 'rr_lock'] == 0:
                    plt.scatter(self.p_gx.loc[i, 'rrw'], self.p_gy.loc[i, 'rrw'], c='m', s=1, marker='.')
                elif self.p_gx.loc[i, 'rr_lock'] == 1:
                    plt.scatter(self.p_gx.loc[i, 'rrw'], self.p_gy.loc[i, 'rrw'], c='m', s=4, marker='s')

                if self.p_gx.loc[i, 'lr_lock'] == 0:
                    plt.scatter(self.p_gx.loc[i, 'lrw'], self.p_gy.loc[i, 'lrw'], c='orange', s=1, marker='.')
                elif self.p_gx.loc[i, 'lr_lock'] == 1:
                    plt.scatter(self.p_gx.loc[i, 'lrw'], self.p_gy.loc[i, 'lrw'], c='orange', s=4, marker='s')

        plt.gca().invert_yaxis()
        plt.show()
