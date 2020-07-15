"""
Calculated vehicle premotion
Dependencies =
mu_max defined
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

def vehicle_model(veh):
    """
    Calculate vehicle dynamics from driver inputs and environmental inputs
    """

    # assign values from dictionary
    W = veh.weight
    lcgr = veh.lcgr
    lcgf = veh.lcgf
    wb = veh.wb
    track = veh.track
    izz = veh.izz
    vin = veh.driver_input

    # Vehicle loop start here -
    for i in (range(len(vin))):
        t = i * dt_motion

        if i == 0:
            # set all tire forces in vehicle frame to zero
            # Forward and Rightward Forces
            lf_fx = 0
            lf_fy = 0
            rf_fx = 0
            rf_fy = 0
            rr_fx = 0
            rr_fy = 0
            lr_fx = 0
            lr_fy = 0

            # vertical forces
            lf_fz = 0.5 * W * lcgr / wb
            rf_fz = 0.5 * W * lcgr / wb
            rr_fz = 0.5 * W * lcgf / wb
            lr_fz = 0.5 * W * lcgf / wb

            # Slip angle
            lf_alpha = 0
            rf_alpha = 0
            rr_alpha = 0
            lr_alpha = 0
            lr_alpha = 0

            # Tire lock status
            lf_lock = 0
            rf_lock = 0
            rr_lock = 0
            lr_lock = 0

            # these values are initially taken from driver input data
            vx = veh.vx_initial * 1.46667  # convert input in mph to fps
            vy = veh.vy_initial * 1.46667  # convert input in mph to fps
            ax = 32.2 * mu_max * (veh.driver_input.loc[i, 'throttle'] - veh.driver_input.loc[i, 'brake'])  # defined throttle and braking
            ay = 0

            # inertial frame  - capital letters
            theta_rad = veh.head_angle * math.pi / 180
            Ax = ax * math.cos(theta_rad) - ay * math.sin(theta_rad)
            Ay = ax * math.sin(theta_rad) + ay * math.cos(theta_rad)
            Vx = vx * math.cos(theta_rad) - vy * math.sin(theta_rad)
            Vy = vx * math.sin(theta_rad) + vy * math.cos(theta_rad)
            oz_rad = veh.omega_z * (math.pi/180)
            alphaz = 0


        if i > 0:                                                               # vehicle motion is calculated based on equations of motion
            # update velocity and oz_rad before redefining ax, ay, alphaz
            oz_rad = oz_rad + dt_motion*np.mean([alphaz, (1/izz) * np.sum([lf_fx * track / 2, lf_fy * lcgf, -1*rf_fx * track / 2, rf_fy * lcgf,
                                                   -1 * rr_fx * track / 2, -1* rr_fy * lcgr, lr_fx * track/2 , -1 * lr_fy * lcgr])])

            vx = vx + dt_motion * np.mean([ax, (1/(W/32.2)) * np.sum([lf_fx, rf_fx, rr_fx, lr_fx]) + oz_rad * vy])   # integrates ax (actual i-1) and the current ax calculated - corrected for rotating reference frame
            vy = vy + dt_motion * np.mean([ay, (1/(W/32.2)) * np.sum([lf_fy, rf_fy, rr_fy, lr_fy]) - oz_rad * vx])   # integrates ax (actual i-1) and the current ax calculated

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
        data = [t, vin.loc[i, 'throttle'], vin.loc[i, 'brake'], vx, vy, Vx, Vy, Vr, oz_deg, oz_rad, delta_deg, delta_rad, turn_rX, turn_rY, turn_rR, au, av, ax, ay, Ax, Ay, Ar, alphaz, alphaz_deg, beta_deg, beta_rad,
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
