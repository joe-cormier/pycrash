"""

"""
from .model_calcs.tire_model import tire_forces
import pandas as pd
import numpy as np
from scipy import integrate
import math
import csv
import os



# column list for vehicle model
column_list = ['t', 'vx','vy', 'Vx', 'Vy', 'Vr', 'oz_deg', 'oz_rad', 'delta_deg',
           'delta_rad', 'turn_rX', 'turn_rY', 'turn_rR', 'au', 'av',
           'ax','ay', 'ar', 'Ax', 'Ay', 'Ar', 'alphaz', 'alphaz_deg',
           'beta_deg','beta_rad', 'lf_fx', 'lf_fy', 'rf_fx', 'rf_fy',
           'rr_fx', 'rr_fy', 'lr_fx', 'lr_fy', 'lf_alpha', 'rf_alpha', 'rr_alpha', 'lr_alpha',
           'lf_lock', 'rf_lock', 'rr_lock', 'lr_lock', 'lf_fz', 'rf_fz', 'rr_fz', 'lr_fz',
           'theta_rad', 'theta_deg']

def vehicle_model(veh, sim_defaults):
    """
    Calculate vehicle dynamics from driver inputs and environmental inputs
    """
    # load defaults
    dt_motion = sim_defaults['dt_motion']  # iteration time step

    print(f"Vehicle motion will be simulated for {max(veh.driver_input.t)} seconds")
    veh.model = pd.DataFrame(np.nan, index=np.arange(len(veh.driver_input.t)), columns = column_list)

    veh.model.au[0] = 0         # no initial vehicle pitch
    veh.model.av[0] = 0         # no initial vehicle roll
    veh.model.vx[0] = veh.vx_initial * 1.46667  # convert input in mph to fps
    veh.model.vy[0] = veh.vy_initial * 1.46667  # convert input in mph to fps
    veh.model.theta_rad[0] = veh.head_angle * math.pi / 180   # initial heading angle
    veh.model.oz_rad[0] = veh.omega_z * (math.pi/180)  # initial angular rate (deg/s) - input
    veh.model.Vx[0] = veh.model.vx[0] * math.cos(veh.model.theta_rad[0]) - veh.model.vy[0] * math.sin(veh.model.theta_rad[0])
    veh.model.Vy[0] = veh.model.vx[0] * math.sin(veh.model.theta_rad[0]) + veh.model.vy[0] * math.cos(veh.model.theta_rad[0])

    for i in range(len(veh.driver_input.t)):
        veh.model.t[i] = round(i * dt_motion, 4)  # assigning time

        # get tire forces for t = 0
        veh = tire_forces(veh, i, sim_defaults)

        # local vehicle acceleration
        veh.model.au[i] = 32.2 / veh.weight * np.sum([veh.model.lf_fx[i],
                                                      veh.model.rf_fx[i],
                                                      veh.model.rr_fx[i],
                                                      veh.model.lr_fx[i]])

        veh.model.av[i] = 32.2 / veh.weight * np.sum([veh.model.lf_fy[i],
                                                      veh.model.rf_fy[i],
                                                      veh.model.rr_fy[i],
                                                      veh.model.lr_fy[i]])

        # rotation acceleration - alpha-z
        veh.model.alphaz[i] = (1 / veh.izz) * np.sum([veh.model.lf_fx[i] * veh.track / 2,
                                                      veh.model.lf_fy[i] * veh.lcgf,
                                                      -1 * veh.model.rf_fx[i] * veh.track / 2,
                                                      veh.model.rf_fy[i] * veh.lcgf,
                                                      -1 * veh.model.rr_fx[i] * veh.track / 2,
                                                      -1 * veh.model.rr_fy[i] * veh.lcgr,
                                                      veh.model.lr_fx[i] * veh.track / 2,
                                                      -1 * veh.model.lr_fy[i] * veh.lcgr])

        if i == 0:
            # vehicle acceleration in inertial frame
            veh.model.ax[i] = veh.model.au[i] + veh.model.oz_rad[i] * veh.model.vy[i]
            veh.model.ay[i] = veh.model.av[i] - veh.model.oz_rad[i] * veh.model.vx[i]
            veh.model.ar[i] = math.sqrt(veh.model.ax[i]**2 + veh.model.ay[i]**2)

            # inertial frame coordinates - capital letters
            veh.model.Ax[i] = veh.model.au[i] * math.cos(veh.model.theta_rad[i]) - veh.model.av[i] * math.sin(veh.model.theta_rad[i])
            veh.model.Ay[i] = veh.model.au[i] * math.sin(veh.model.theta_rad[i]) + veh.model.av[i] * math.cos(veh.model.theta_rad[i])

        if i > 0:
            # vehicle acceleration in inertial frame
            veh.model.ax[i] = veh.model.au[i] + veh.model.oz_rad[i-1] * veh.model.vy[i-1]
            veh.model.ay[i] = veh.model.av[i] - veh.model.oz_rad[i-1] * veh.model.vx[i-1]
            veh.model.ar[i] = math.sqrt(veh.model.ax[i]**2 + veh.model.ay[i]**2)

            # vehicle velocities
            veh.model.vx[i] = veh.model.vx[i-1] + dt_motion * np.mean([veh.model.ax[i-1], veh.model.ax[i]])
            veh.model.vy[i] = veh.model.vy[i-1] + dt_motion * np.mean([veh.model.ay[i-1], veh.model.ay[i]])

            # omega
            veh.model.oz_rad[i] = veh.model.oz_rad[i-1] + dt_motion * np.mean([veh.model.alphaz[i-1], veh.model.alphaz[i]])

            # heading angle
            veh.model.theta_rad[i] = veh.model.theta_rad[i-1] + dt_motion * np.mean([veh.model.oz_rad[i], veh.model.oz_rad[i-1]])

            # inertial frame coordinates - capital letters
            veh.model.Ax[i] = veh.model.au[i] * math.cos(veh.model.theta_rad[i]) - veh.model.av[i] * math.sin(veh.model.theta_rad[i])
            veh.model.Ay[i] = veh.model.au[i] * math.sin(veh.model.theta_rad[i]) + veh.model.av[i] * math.cos(veh.model.theta_rad[i])

            veh.model.Vx[i] = veh.model.Vx[i-1] + dt_motion * np.mean([veh.model.Ax[i-1], veh.model.Ax[i]])
            veh.model.Vy[i] = veh.model.Vy[i-1] + dt_motion * np.mean([veh.model.Ay[i-1], veh.model.Ay[i]])

        """

        """
        if veh.model.oz_rad[i] != 0:
            veh.model.turn_rX[i] = veh.model.Vy[i] / veh.model.oz_rad[i]    # turning radius in x direction
            veh.model.turn_rY[i] = veh.model.Vx[i] / veh.model.oz_rad[i]    # turning radius in y direction
            veh.model.turn_rR[i] = math.sqrt(veh.model.turn_rX[i]**2 + veh.model.turn_rY[i]**2)
        else:
            veh.model.turn_rX[i] = 0   # should actually be inf or undefined
            veh.model.turn_rY[i] = 0   # should actually be inf or undefined
            veh.model.turn_rR[i] = 0   # should actually be inf or undefined

        veh.model.Vr[i] = math.sqrt(veh.model.Vx[i]**2 + veh.model.Vy[i]**2)    # move to seperate calc
        veh.model.Ar[i] = math.sqrt(veh.model.Ax[i]**2 + veh.model.Ay[i]**2)

        # velocity vector in inertial frame
        veh.model.beta_rad[i] = math.atan2(veh.model.Vy[i], veh.model.Vx[i])    # move to seperate calc

    # vehicle position
    veh.model['Dx'] = veh.init_x_pos + integrate.cumtrapz(list(veh.model.Vx), list(veh.model.t), initial=0)
    veh.model['Dy'] = veh.init_y_pos + integrate.cumtrapz(list(veh.model.Vy), list(veh.model.t), initial=0)

    # converting to degrees
    # TODO: remove for speed
    veh.model.alphaz_deg = [row * 180 / math.pi for row in veh.model.alphaz]    # move to seperate calc
    veh.model.oz_deg = [row * 180 / math.pi for row in veh.model.oz_rad]        # move to seperate calc
    veh.model.theta_deg = [row * 180 / math.pi for row in veh.model.theta_rad]  # move to seperate calc
    veh.model.beta_deg = [row * 180 / math.pi for row in veh.model.beta_rad]    # move to seperate calc

    return veh
