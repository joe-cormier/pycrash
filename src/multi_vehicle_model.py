"""
vehicle motion for mutliple vehicles
"""
from data.defaults.config import default_dict
from src.multi_vehicle_tire import multi_tire_model
import pandas as pd
import numpy as np
from scipy import integrate
import math
import csv
import os

# load defaults
mu_max = default_dict['mu_max']             # maximum available friction
dt_motion = default_dict['dt_motion']       # iteration time step
impact_occurred = False                     # indicates if an impact has been detected


# column list for vehicle model
column_list = ['t','throttle', 'brake', 'vx','vy', 'Vx', 'Vy', 'Vr', 'oz_deg', 'oz_rad', 'delta_deg',
           'delta_rad', 'turn_rX', 'turn_rY', 'turn_rR', 'au', 'av', 'ax','ay', 'Ax', 'Ay', 'Ar',
           'alphaz', 'alphaz_deg', 'beta_deg','beta_rad', 'lf_fx', 'lf_fy', 'rf_fx', 'rf_fy',
           'rr_fx', 'rr_fy', 'lr_fx', 'lr_fy', 'lf_alpha', 'rf_alpha', 'rr_alpha', 'lr_alpha',
           'lf_lock', 'rf_lock', 'rr_lock', 'lr_lock', 'lf_fz', 'rf_fz', 'rr_fz', 'lr_fz',
           'theta_rad', 'theta_deg', 'Fx', 'Fy', 'Mz']

# TODO: ignore driver inputs after impact
# TODO: disable tire after impact

def multi_vehicle_model(vehicle_list, impact_type, ignore_driver = False):
"""
Calculate vehicle dynamics from driver inputs and environmental inputs
vehicle_list is a list of vehicle class instances [veh1, veh2] - two currently
model will use the max time from vehicle 1 for input, all vehicles
need the same total driver input time
model_type indicates the type of impact to be simulated (sideswipe (ss), or impulse-momentum (impc))
ignore_driver (False) will use driver_inputs after impact.  True will ignore all driver inputs and keep
last input for remainder of simulation
"""

    print(f"Two vehicle simulation will run for {max(vehicle_list[0].driver_input.t)} s")

    for veh in vehicle_list:
        veh.veh_model = pd.DataFrame(np.nan, index=np.arange(len(veh.driver_input.t)), columns = column_list)


    # Simulation time step loop start here -
    for i in (range(len(vehicle_list[0].driver_input.t))):

        # step through each vehicle
        for veh in vehicle_list:
            veh.veh_model.t[i] = round(i * dt_motion, 4)

            if i == 0:
                # set all tire forces in vehicle frame to zero
                # Forward and Rightward Forces
                veh.veh_model.lf_fx[i] = 0
                veh.veh_model.lf_fy[i] = 0
                veh.veh_model.rf_fx[i] = 0
                veh.veh_model.rf_fy[i] = 0
                veh.veh_model.rr_fx[i] = 0
                veh.veh_model.rr_fy[i] = 0
                veh.veh_model.lr_fx[i] = 0
                veh.veh_model.lr_fy[i] = 0

                # vertical forces
                veh.veh_model.lf_fz[i] = 0.5 * veh.weight * veh.lcgr / veh.wb
                veh.veh_model.rf_fz[i] = 0.5 * veh.weight * veh.lcgr / veh.wb
                veh.veh_model.rr_fz[i] = 0.5 * veh.weight * veh.lcgf / veh.wb
                veh.veh_model.lr_fz[i] = 0.5 * veh.weight * veh.lcgf / veh.wb

                # Slip angle
                veh.veh_model.lf_alpha[i] = 0
                veh.veh_model.rf_alpha[i] = 0
                veh.veh_model.rr_alpha[i] = 0
                veh.veh_model.lr_alpha[i] = 0
                veh.veh_model.lr_alpha[i] = 0

                # Tire lock status
                veh.veh_model.lf_lock[i] = 0
                veh.veh_model.rf_lock[i] = 0
                veh.veh_model.rr_lock[i] = 0
                veh.veh_model.lr_lock[i] = 0

                # these values are initially taken from driver input data
                veh.veh_model.vx[i] = veh.vx_initial * 1.46667  # convert input in mph to fps
                veh.veh_model.vy[i] = veh.vy_initial * 1.46667  # convert input in mph to fps
                veh.veh_model.ax[i] = 32.2 * mu_max * (veh.driver_input.loc[i, 'throttle'] - veh.driver_input.loc[i, 'brake'])  # defined throttle and braking
                veh.veh_model.ay[i] = 0

                # inertial frame  - capital letters
                veh.veh_model.theta_rad[i] = veh.head_angle * math.pi / 180
                veh.veh_model.Ax[i] = veh.veh_model.ax[i] * math.cos(veh.veh_model.theta_rad[i]) - veh.veh_model.ay[i] * math.sin(veh.veh_model.theta_rad[i])
                veh.veh_model.Ay[i] = veh.veh_model.ax[i] * math.sin(veh.veh_model.theta_rad[i]) + veh.veh_model.ay[i] * math.cos(veh.veh_model.theta_rad[i])
                veh.veh_model.Vx[i] = veh.veh_model.vx[i] * math.cos(veh.veh_model.theta_rad[i]) - veh.veh_model.vy[i] * math.sin(veh.veh_model.theta_rad[i])
                veh.veh_model.Vy[i] = veh.veh_model.vx[i] * math.sin(veh.veh_model.theta_rad[i]) + veh.veh_model.vy[i] * math.cos(veh.veh_model.theta_rad[i])
                veh.veh_model.oz_rad[i] = veh.omega_z * (math.pi/180)
                veh.veh_model.alphaz[i] = 0


            if i > 0:                                                               # vehicle motion is calculated based on equations of motion
                # update velocity and oz_rad before redefining ax, ay, alphaz
                veh.veh_model.oz_rad[i] = veh.veh_model.oz_rad[i-1] + dt_motion * np.mean([veh.veh_model.alphaz[i-1], (1 / veh.izz) * np.sum([veh.lf_fx * veh.track / 2, veh.veh_motion.lf_fy[i-1] * veh.lcgf, -1 * veh.veh_motion.rf_fx[i-1] * veh.track / 2, veh.veh_model.rf_fy[i-1] * veh.lcgf,
                                                    -1 * veh.veh_model.rr_fx[i-1] * veh.track / 2, -1 * veh.veh_model.rr_fy[i-1] * veh.lcgr, veh.veh_model.lr_fx[i-1] * veh.track / 2 , -1 * veh.veh_model.lr_fy[i-1] * veh.lcgr])])

                veh.veh_model.vx[i] = veh.veh_model.vx[i-1] + dt_motion * np.mean([veh.veh_model.ax[i-1], (1 / (veh.weight / 32.2)) * np.sum([veh.veh_model.lf_fx[i-1], veh.veh_model.rf_fx[i-1], veh.veh_model.rr_fx[i-1], veh.veh_model.lr_fx[i-1]]) + veh.veh_model.oz_rad[i-1] * veh.veh_model.vy[i-1]])   # integrates ax (actual i-1) and the current ax calculated - corrected for rotating reference frame
                veh.veh_model.vy[i] = veh.veh_model.vy[i-1] + dt_motion * np.mean([veh.veh_model.ay[i-1], (1 / (veh.weight / 32.2)) * np.sum([veh.veh_model.lf_fy[i-1], veh.veh_model.rf_fy[i-1], veh.veh_model.rr_fy[i-1], veh.veh_model.lr_fy[i-1]]) - veh.veh_model.oz_rad[i-1] * veh.veh_model.vx[i-1]])   # integrates ax (actual i-1) and the current ax calculated

                veh.veh_model.ax[i] = 32.2 / veh.weight * np.sum([veh.veh_model.lf_fx[i-1], veh.veh_model.rf_fx[i-1], veh.veh_model.rr_fx[i-1], veh.veh_model.lr_fx[i-1]])  # inertial components of acceleration
                veh.veh_model.ay[i] = 32.2 / veh.weight * np.sum([veh.veh_model.lf_fy[i-1], veh.veh_model.rf_fy[i-1], veh.veh_model.rr_fy[i-1], veh.veh_model.lr_fy[i-1]])  # inertial components of acceleration
                veh.veh_model.alphaz[i] = (1 / veh.izz) * np.sum([veh.veh_model.lf_fx[i-1] * veh.track / 2, veh.veh_model.lf_fy[i-1] * veh.lcgf, -1 * veh.veh_model.rf_fx[i-1] * veh.track / 2, veh.veh_model.rf_fy[i-1] * veh.lcgf,
                                                    -1 * veh.veh_model.rr_fx[i-1] * veh.track / 2, -1 * veh.veh_model.rr_fy[i-1] * veh.lcgr, veh.veh_model.lr_fx[i-1] * veh.track / 2 , -1 * veh.veh_model.lr_fy[i-1] * veh.lcgr])

                # update heading angle
                veh.veh_model.theta_rad[i] = veh.veh_model.theta_rad[i-1] + dt_motion * np.mean([veh.veh_model.oz_rad[i], veh.veh_model.oz_rad[i-1]])

                # inertial frame components
                veh.veh_model.Vx[i] = veh.veh_model.Vx[i-1] + dt_motion * np.mean([veh.veh_model.Ax[i-1], (veh.veh_model.ax[i] * math.cos(veh.veh_model.theta_rad[i]) - veh.veh_model.ay[i] * math.sin(veh.veh_model.theta_rad[i]))])
                veh.veh_model.Vy[i] = veh.veh_model.Vy[i-1] + dt_motion * np.mean([veh.veh_model.Ay[i-1], (veh.veh_model.ax[i] * math.sin(veh.veh_model.theta_rad[i]) + veh.veh_model.ay[i] * math.cos(veh.veh_model.theta_rad[i]))])
                veh.veh_model.Ax[i] = veh.veh_model.ax[i-1] * math.cos(veh.veh_model.theta_rad[i]) - veh.veh_model.ay[i-1] * math.sin(veh.veh_model.theta_rad[i])
                veh.veh_model.Ay[i] = veh.veh_model.ax[i-1] * math.sin(veh.veh_model.theta_rad[i]) + veh.veh_model.ay[i-1] * math.cos(veh.veh_model.theta_rad[i])


            # these do not need to be part of the if statements, they are functions of the changing variables above
            veh.veh_model.delta_deg[i] = veh.driver_input.steer[i] / veh.steer_ratio               # steer angle (delta) will always be derived from driver input
            veh.veh_model.delta_rad[i] = delta_deg * (math.pi/180)

            if veh.veh_model.oz_rad[i] > 0:
                veh.veh_model.turn_rX[i] =  veh.veh_model.Vy[i] / veh.veh_model.oz_rad[i]    # turning radius in x direction
                veh.veh_model.turn_rY[i] =  veh.veh_model.Vx[i] / veh.veh_model.oz_rad[i]    # turning radius in y direction
                veh.veh_model.turn_rR[i] = math.sqrt(veh.veh_model.turn_rX[i]**2 + veh.veh_model.turn_rY[i]**2)
            else:
                veh.veh_model.turn_rX[i] = 0   # should actually be inf or undefined
                veh.veh_model.turn_rY[i] = 0   # should actually be inf or undefined
                veh.veh_model.turn_rR[i] = 0   # should actually be inf or undefined

            veh.veh_model.alphaz_deg[i] = veh.veh_model.alphaz[i] * 180 / math.pi
            veh.veh_model.oz_deg[i] = veh.veh_model.oz_rad[i] * 180 / math.pi
            veh.veh_model.theta_deg[i] = veh.veh_model.theta_rad[i] * 180 / math.pi

            veh.veh_model.Vr[i] = math.sqrt(veh.veh_model.Vx[i]**2 + veh.veh_model.Vy[i]**2)
            veh.veh_model.Ar[i] = math.sqrt(veh.veh_model.Ax[i]**2 + veh.veh_model.Ay[i]**2)

            # velocity vector in inertial frame
            veh.veh_model.beta_rad[i] = math.atan2(veh.veh_model.Vy[i], veh.veh_model.Vx[i])
            veh.veh_model.beta_deg[i] = veh.veh_model.beta_rad[i] * 180 / math.pi

            # transform vehicle ax, ay to non-rotating vehicle frame
            veh.veh_model.au[i] = veh.veh_model.ax[i]                                                               # - inertial component for tire model
            veh.veh_model.av[i] = veh.veh_model.ay[i]                                                                 # - inertial component for tire model
            veh.veh_model.ax[i] = veh.veh_model.ax[i] + veh.veh_model.oz_rad[i] * veh.veh_model.vy[i]
            veh.veh_model.ay[i = veh.veh_model.ay[i] - veh.veh_model.oz_rad[i] * veh.veh_model.vx[i]

            # get tire forces for the current time step
            veh = multi_tire_model(veh, i)

            veh.veh_model.v_model['Dx'] = veh.init_x_pos + integrate.cumtrapz(list(veh.veh_model.Vx), list(veh.veh_model.t), initial=0)     # integrate vx to get distance traveled in x direction
            veh.veh_model.v_model['Dy'] = veh.init_y_pos + integrate.cumtrapz(list(veh.veh_model.Vy), list(veh.veh_model.t), initial=0)     # integrate vy to get distance traveled in y direction

            # function for detecting impact
            impact_detect = impact_detect(vehicle_list)

            if (impact_dectect['impact']):
                impact_occurred = 1
                if (impact_type == 'impc'):
                    impc_result = impc(vehicle_list)              # run impc model - create inputs using vehicle class
                elif (impact_type == 'ss'):
                    impact_force = ss(vehicle_list, impact_detect)
                else:
                    print(f'impact_type {impact_type} is not defined')
                    break
            else:
                veh.veh_model.Fx[i] = 0
                veh.veh_model.Fy[i] = 0
                veh.veh_model.Mz[i] = 0




    return vehicle_list
