"""
Calculated vehicle premotion
Dependencies =
mu_max defined
"""
from .data.defaults.config import default_dict
from .tire_model import tire_forces
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
column_list = ['t', 'vx','vy', 'Vx', 'Vy', 'Vr', 'oz_deg', 'oz_rad', 'delta_deg',
           'delta_rad', 'turn_rX', 'turn_rY', 'turn_rR', 'au', 'av', 'ax','ay', 'Ax', 'Ay', 'Ar',
           'alphaz', 'alphaz_deg', 'beta_deg','beta_rad', 'lf_fx', 'lf_fy', 'rf_fx', 'rf_fy',
           'rr_fx', 'rr_fy', 'lr_fx', 'lr_fy', 'lf_alpha', 'rf_alpha', 'rr_alpha', 'lr_alpha',
           'lf_lock', 'rf_lock', 'rr_lock', 'lr_lock', 'lf_fz', 'rf_fz', 'rr_fz', 'lr_fz',
           'theta_rad', 'theta_deg', 'Fx', 'Fy', 'Mz']

def vehicle_model(veh):
    """
    Calculate vehicle dynamics from driver inputs and environmental inputs
    """
    print(f"Vehicle simulation will run for {max(veh.driver_input.t)} s")
    veh.model = pd.DataFrame(np.nan, index=np.arange(len(veh.driver_input.t)), columns = column_list)

    # assign values from dictionary
    W = veh.weight
    lcgr = veh.lcgr
    lcgf = veh.lcgf
    wb = veh.wb
    track = veh.track
    izz = veh.izz
    vin = veh.driver_input

    # Vehicle loop start here -
    for i in range(len(veh.driver_input.t)):
        veh.model.t[i] = round(i * dt_motion, 4) # assigning time

        if i == 0:
            # set all tire forces in vehicle frame to zero
            # Forward and Rightward Forces
            veh.model.lf_fx[i] = 0
            veh.model.lf_fy[i] = 0
            veh.model.rf_fx[i] = 0
            veh.model.rf_fy[i] = 0
            veh.model.rr_fx[i] = 0
            veh.model.rr_fy[i] = 0
            veh.model.lr_fx[i] = 0
            veh.model.lr_fy[i] = 0

            # vertical forces
            veh.model.lf_fz[i] = 0.5 * veh.weight * veh.lcgr / veh.wb
            veh.model.rf_fz[i] = 0.5 * veh.weight * veh.lcgr / veh.wb
            veh.model.rr_fz[i] = 0.5 * veh.weight * veh.lcgf / veh.wb
            veh.model.lr_fz[i] = 0.5 * veh.weight * veh.lcgf / veh.wb

            # Slip angle
            veh.model.lf_alpha[i] = 0
            veh.model.rf_alpha[i] = 0
            veh.model.rr_alpha[i] = 0
            veh.model.lr_alpha[i] = 0
            veh.model.lr_alpha[i] = 0

            # Tire lock status
            veh.model.lf_lock[i] = 0
            veh.model.rf_lock[i] = 0
            veh.model.rr_lock[i] = 0
            veh.model.lr_lock[i] = 0

            # these values are initially taken from driver input data
            veh.model.vx[i] = veh.vx_initial * 1.46667  # convert input in mph to fps
            veh.model.vy[i] = veh.vy_initial * 1.46667  # convert input in mph to fps
            veh.model.ax[i] = 32.2 * mu_max * (veh.driver_input.loc[i, 'throttle'] - veh.driver_input.loc[i, 'brake'])  # defined throttle and braking
            veh.model.ay[i] = 0

            # inertial frame  - capital letters
            veh.model.theta_rad[i] = veh.head_angle * math.pi / 180
            veh.model.Ax[i] = veh.model.ax[i] * math.cos(veh.model.theta_rad[i]) - veh.model.ay[i] * math.sin(veh.model.theta_rad[i])
            veh.model.Ay[i] = veh.model.ax[i] * math.sin(veh.model.theta_rad[i]) + veh.model.ay[i] * math.cos(veh.model.theta_rad[i])
            veh.model.Vx[i] = veh.model.vx[i] * math.cos(veh.model.theta_rad[i]) - veh.model.vy[i] * math.sin(veh.model.theta_rad[i])
            veh.model.Vy[i] = veh.model.vx[i] * math.sin(veh.model.theta_rad[i]) + veh.model.vy[i] * math.cos(veh.model.theta_rad[i])
            veh.model.oz_rad[i] = veh.omega_z * (math.pi/180)  # initial angular rate (deg/s) - input
            veh.model.alphaz[i] = 0


        if i > 0:                                                               # vehicle motion is calculated based on equations of motion
            # update velocity and oz_rad before redefining ax, ay, alphaz
            veh.model.oz_rad[i] = veh.model.oz_rad[i-1] + dt_motion * np.mean([veh.model.alphaz[i-1], (1 / veh.izz) * np.sum([veh.model.lf_fx[i-1] * veh.track / 2, veh.model.lf_fy[i-1] * veh.lcgf, -1 * veh.model.rf_fx[i-1] * veh.track / 2, veh.model.rf_fy[i-1] * veh.lcgf,
                                                -1 * veh.model.rr_fx[i-1] * veh.track / 2, -1 * veh.model.rr_fy[i-1] * veh.lcgr, veh.model.lr_fx[i-1] * veh.track / 2 , -1 * veh.model.lr_fy[i-1] * veh.lcgr])])

            veh.model.vx[i] = veh.model.vx[i-1] + dt_motion * np.mean([veh.model.ax[i-1], (1 / (veh.weight / 32.2)) * np.sum([veh.model.lf_fx[i-1], veh.model.rf_fx[i-1], veh.model.rr_fx[i-1], veh.model.lr_fx[i-1]]) + veh.model.oz_rad[i-1] * veh.model.vy[i-1]])   # integrates ax (actual i-1) and the current ax calculated - corrected for rotating reference frame
            veh.model.vy[i] = veh.model.vy[i-1] + dt_motion * np.mean([veh.model.ay[i-1], (1 / (veh.weight / 32.2)) * np.sum([veh.model.lf_fy[i-1], veh.model.rf_fy[i-1], veh.model.rr_fy[i-1], veh.model.lr_fy[i-1]]) - veh.model.oz_rad[i-1] * veh.model.vx[i-1]])   # integrates ax (actual i-1) and the current ax calculated

            veh.model.ax[i] = 32.2 / veh.weight * np.sum([veh.model.lf_fx[i-1], veh.model.rf_fx[i-1], veh.model.rr_fx[i-1], veh.model.lr_fx[i-1]])  # inertial components of acceleration
            veh.model.ay[i] = 32.2 / veh.weight * np.sum([veh.model.lf_fy[i-1], veh.model.rf_fy[i-1], veh.model.rr_fy[i-1], veh.model.lr_fy[i-1]])  # inertial components of acceleration
            veh.model.alphaz[i] = (1 / veh.izz) * np.sum([veh.model.lf_fx[i-1] * veh.track / 2, veh.model.lf_fy[i-1] * veh.lcgf, -1 * veh.model.rf_fx[i-1] * veh.track / 2, veh.model.rf_fy[i-1] * veh.lcgf,
                                                -1 * veh.model.rr_fx[i-1] * veh.track / 2, -1 * veh.model.rr_fy[i-1] * veh.lcgr, veh.model.lr_fx[i-1] * veh.track / 2 , -1 * veh.model.lr_fy[i-1] * veh.lcgr])

            # update heading angle
            veh.model.theta_rad[i] = veh.model.theta_rad[i-1] + dt_motion * np.mean([veh.model.oz_rad[i], veh.model.oz_rad[i-1]])

            # inertial frame components
            veh.model.Vx[i] = veh.model.Vx[i-1] + dt_motion * np.mean([veh.model.Ax[i-1], (veh.model.ax[i] * math.cos(veh.model.theta_rad[i]) - veh.model.ay[i] * math.sin(veh.model.theta_rad[i]))])
            veh.model.Vy[i] = veh.model.Vy[i-1] + dt_motion * np.mean([veh.model.Ay[i-1], (veh.model.ax[i] * math.sin(veh.model.theta_rad[i]) + veh.model.ay[i] * math.cos(veh.model.theta_rad[i]))])
            veh.model.Ax[i] = veh.model.ax[i-1] * math.cos(veh.model.theta_rad[i]) - veh.model.ay[i-1] * math.sin(veh.model.theta_rad[i])
            veh.model.Ay[i] = veh.model.ax[i-1] * math.sin(veh.model.theta_rad[i]) + veh.model.ay[i-1] * math.cos(veh.model.theta_rad[i])

        # these do not need to be part of the if statements, they are functions of the changing variables above
        veh.model.delta_deg[i] = veh.driver_input.steer[i] / veh.steer_ratio   # steer angle (delta) will always be derived from driver input
        veh.model.delta_rad[i] = veh.model.delta_deg[i] * (math.pi/180)

        if veh.model.oz_rad[i] != 0:
            veh.model.turn_rX[i] = veh.model.Vy[i] / veh.model.oz_rad[i]    # turning radius in x direction
            veh.model.turn_rY[i] = veh.model.Vx[i] / veh.model.oz_rad[i]    # turning radius in y direction
            veh.model.turn_rR[i] = math.sqrt(veh.model.turn_rX[i]**2 + veh.model.turn_rY[i]**2)
        else:
            veh.model.turn_rX[i] = 0   # should actually be inf or undefined
            veh.model.turn_rY[i] = 0   # should actually be inf or undefined
            veh.model.turn_rR[i] = 0   # should actually be inf or undefined

        veh.model.alphaz_deg[i] = veh.model.alphaz[i] * 180 / math.pi
        veh.model.oz_deg[i] = veh.model.oz_rad[i] * 180 / math.pi
        veh.model.theta_deg[i] = veh.model.theta_rad[i] * 180 / math.pi

        veh.model.Vr[i] = math.sqrt(veh.model.Vx[i]**2 + veh.model.Vy[i]**2)
        veh.model.Ar[i] = math.sqrt(veh.model.Ax[i]**2 + veh.model.Ay[i]**2)

        # velocity vector in inertial frame
        veh.model.beta_rad[i] = math.atan2(veh.model.Vy[i], veh.model.Vx[i])
        veh.model.beta_deg[i] = veh.model.beta_rad[i] * 180 / math.pi

        # transform vehicle ax, ay to non-rotating vehicle frame
        veh.model.au[i] = veh.model.ax[i]         # - inertial component for tire model
        veh.model.av[i] = veh.model.ay[i]         # - inertial component for tire model
        veh.model.ax[i] = veh.model.ax[i] + veh.model.oz_rad[i] * veh.model.vy[i]
        veh.model.ay[i] = veh.model.ay[i] - veh.model.oz_rad[i] * veh.model.vx[i]

            # get tire forces for the current time step
        veh = tire_forces(veh, i)

    veh.model['Dx'] = veh.init_x_pos + integrate.cumtrapz(list(veh.model.Vx), list(veh.model.t), initial=0)     # integrate vx to get distance traveled in x direction
    veh.model['Dy'] = veh.init_y_pos + integrate.cumtrapz(list(veh.model.Vy), list(veh.model.t), initial=0)     # integrate vy to get distance traveled in y direction

    return veh
