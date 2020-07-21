"""
vehicle motion for mutliple vehicles
"""
from data.defaults.config import default_dict
from src.tire import tire_model
import pandas as pd
import numpy as np
from scipy import integrate
import math
import csv
import os

# load defaults
mu_max = default_dict['mu_max']             # maximum available friction
dt_motion = default_dict['dt_motion']       # iteration time step



# column list for vehicle model
column_list = ['t','throttle', 'brake', 'vx','vy', 'Vx', 'Vy', 'Vr', 'oz_deg', 'oz_rad', 'delta_deg',
           'delta_rad', 'turn_rX', 'turn_rY', 'turn_rR', 'au', 'av', 'ax','ay', 'Ax', 'Ay', 'Ar',
           'alphaz', 'alphaz_deg', 'beta_deg','beta_rad', 'lf_fx', 'lf_fy', 'rf_fx', 'rf_fy',
           'rr_fx', 'rr_fy', 'lr_fx', 'lr_fy', 'lf_alpha', 'rf_alpha', 'rr_alpha', 'lr_alpha',
           'lf_lock', 'rf_lock', 'rr_lock', 'lr_lock', 'lf_fz', 'rf_fz', 'rr_fz', 'lr_fz',
           'theta_rad', 'theta_deg']

def vehicle_model(vehicle_list):
    """
    Calculate vehicle dynamics from driver inputs and environmental inputs
    vehicle_list is a list of vehicle class instances [veh1, veh2] - two currently
    model will use the max time from vehicle 1 for input, all vehicles
    need the same total driver input time
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

                ax = 32.2 / W * np.sum([lf_fx, rf_fx, rr_fx, lr_fx])  # inertial components of acceleration
                ay = 32.2 / W * np.sum([lf_fy, rf_fy, rr_fy, lr_fy])  # inertial components of acceleration
                alphaz = (1/izz) * np.sum([lf_fx * track / 2, lf_fy * lcgf, -1*rf_fx * track/2, rf_fy * lcgf,
                                                    -1 * rr_fx * track / 2, -1* rr_fy * lcgr, lr_fx * track /2 , -1 * lr_fy * lcgr])

                # update heading angle
                theta_rad = theta_rad + dt_motion * np.mean([v_model.loc[i-1, 'oz_rad'], oz_rad])

                # inertial frame components
                Vx = Vx + dt_motion*np.mean([Ax, (ax * math.cos(theta_rad) - ay * math.sin(theta_rad))])
                Vy = Vy + dt_motion*np.mean([Ay, (ax * math.sin(theta_rad) + ay * math.cos(theta_rad))])
                Ax = ax * math.cos(theta_rad) - ay * math.sin(theta_rad)
                Ay = ax * math.sin(theta_rad) + ay * math.cos(theta_rad)


            # these do not need to be part of the if statements, they are functions of the changing variables above
            delta_deg = veh.driver_input.loc[i, 'steer'] / veh.steer_ratio               # steer angle (delta) will always be derived from driver input
            delta_rad = delta_deg * (math.pi/180)
            if oz_rad > 0:
                turn_rX =  Vy / oz_rad    # turning radius in x direction
                turn_rY =  Vx / oz_rad    # turning radius in y direction
                turn_rR = math.sqrt(turn_rX**2 + turn_rY**2)
            else:
                turn_rX = 0   # should actually be inf or undefined
                turn_rY = 0   # should actually be inf or undefined
                turn_rR = 0   # should actually be inf or undefined

            alphaz_deg = alphaz * 180 / math.pi
            oz_deg = oz_rad * 180 / math.pi
            theta_deg = theta_rad * 180 / math.pi

            Vr = math.sqrt(Vx**2 + Vy**2)
            Ar = math.sqrt(Ax**2 + Ay**2)

            # velocity vector in inertial frame
            beta_rad = math.atan2(Vy, Vx)
            beta_deg = beta_rad * 180/math.pi

            # transform vehicle ax, ay to non-rotating vehicle frame
            au = ax                                                                 # - inertial component for tire model
            av = ay                                                                 # - inertial component for tire model
            ax = ax + oz_rad * vy
            ay = ay - oz_rad * vx


            columns = ['t','throttle', 'brake', 'vx','vy', 'Vx', 'Vy', 'Vr', 'oz_deg', 'oz_rad', 'delta_deg','delta_rad', 'turn_rX', 'turn_rY', 'turn_rR', 'au', 'av', 'ax','ay', 'Ax', 'Ay', 'Ar', 'alphaz', 'alphaz_deg', 'beta_deg','beta_rad', 'lf_fx', 'lf_fy', 'rf_fx', 'rf_fy', 'rr_fx', 'rr_fy', 'lr_fx', 'lr_fy',
                    'lf_alpha', 'rf_alpha', 'rr_alpha', 'lr_alpha', 'lf_lock', 'rf_lock', 'rr_lock', 'lr_lock', 'lf_fz', 'rf_fz', 'rr_fz', 'lr_fz', 'theta_rad', 'theta_deg']
            data = [t, driver_input.loc[i, 'throttle'], driver_input.loc[i, 'brake'], vx, vy, Vx, Vy, Vr, oz_deg, oz_rad, delta_deg, delta_rad, turn_rX, turn_rY, turn_rR, au, av, ax, ay, Ax, Ay, Ar, alphaz, alphaz_deg, beta_deg, beta_rad,
                    lf_fx, lf_fy, rf_fx, rf_fy, rr_fx, rr_fy, lr_fx, lr_fy, lf_alpha, rf_alpha, rr_alpha, lr_alpha, lf_lock, rf_lock, rr_lock, lr_lock, lf_fz, rf_fz, rr_fz, lr_fz, theta_rad, theta_deg]

            # create dataframe and add data row
            if i == 0:
                    v_model = pd.DataFrame(columns = columns)
                    v_model = v_model.append(pd.Series(data, index = columns), ignore_index=True)

            # append data to dataframe after i = 0
            if i > 0:
                    v_model = v_model.append(pd.Series(data, index = columns), ignore_index=True)

            del data

            # run tire model to get forces
            lf_fx, lf_fy, rf_fx, rf_fy, rr_fx, rr_fy, lr_fx, lr_fy, lf_alpha, rf_alpha, rr_alpha, lr_alpha, lf_lock, rf_lock, rr_lock, lr_lock, lf_fz, rf_fz, rr_fz, lr_fz = tire_model(v_model, veh, i)


    v_model['Dx'] = veh.init_x_pos + integrate.cumtrapz(list(v_model.Vx), list(v_model.t), initial=0)     # integrate vx to get distance traveled in x direction
    v_model['Dy'] = veh.init_y_pos + integrate.cumtrapz(list(v_model.Vy), list(v_model.t), initial=0)     # integrate vy to get distance traveled in y direction



    return v_model
