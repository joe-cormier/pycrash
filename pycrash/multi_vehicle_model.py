"""
vehicle motion for multiple vehicles
"""
from .model_calcs.sideswipe import ss
from .model_calcs.tire_model import tire_forces
from .model_calcs.impact_detect import detect
from .model_calcs.carpenter_momentum_calcs import impc
import pandas as pd
import numpy as np
from scipy import integrate
import math
import csv
import os

# column list for vehicle model
column_list = ['t', 'vx', 'vy', 'Vx', 'Vy', 'Vr', 'vehicleslip_deg', 'vehicleslip_rad', 'oz_deg', 'oz_rad', 'delta_deg',
               'delta_rad', 'turn_rX', 'turn_rY', 'turn_rR', 'au', 'av', 'ax', 'ay', 'ar', 'Ax', 'Ay', 'Ar',
               'alphaz', 'alphaz_deg', 'beta_deg', 'beta_rad', 'lf_fx', 'lf_fy', 'rf_fx', 'rf_fy',
               'rr_fx', 'rr_fy', 'lr_fx', 'lr_fy', 'lf_alpha', 'rf_alpha', 'rr_alpha', 'lr_alpha',
               'lf_lock', 'rf_lock', 'rr_lock', 'lr_lock', 'lf_fz', 'rf_fz', 'rr_fz', 'lr_fz',
               'theta_rad', 'theta_deg', 'Fx', 'Fy', 'Mz']


# TODO: ignore driver inputs after impact
# TODO: disable tire after impact

def multi_vehicle_model(vehicle_list, sim_defaults, impact_type, ignore_driver=False, kmutual=None, vehicle_mu=None):
    """
    Calculate vehicle dynamics from driver inputs and environmental inputs
    vehicle_list is a list of vehicle class instances [veh1, veh2] - two currently
    model will use the max time from vehicle 1 for input, all vehicles
    need the same total driver input time
    model_type indicates the type of impact to be simulated (sideswipe (ss), or impulse-momentum (impc))
    ignore_driver (False) will use driver_inputs after impact.  True will ignore all driver inputs and keep
    last input for remainder of simulation
    kmutual must be defined by sideswipe simulations
    """
    impact = False
    impc_complete = False  # flag to allow impc model to run only once

    print(f"Impact Type: {impact_type}")
    # load defaults
    dt_motion = sim_defaults['dt_motion']  # iteration time step

    j = 0

    print(f"Two vehicle simulation will run for {max(vehicle_list[0].driver_input.t)} s")

    for veh in vehicle_list:
        veh.model = pd.DataFrame(np.nan, index=np.arange(len(veh.driver_input.t)), columns=column_list)
        veh.model.Fx[0] = 0
        veh.model.Fy[0] = 0
        veh.model.Mz[0] = 0
        veh.model.au[0] = 0  # no initial vehicle pitch
        veh.model.av[0] = 0  # no initial vehicle roll
        veh.model.vx[0] = veh.vx_initial * 1.46667  # convert input in mph to fps
        veh.model.vy[0] = veh.vy_initial * 1.46667  # convert input in mph to fps
        veh.model.theta_rad[0] = veh.head_angle * math.pi / 180  # initial heading angle
        veh.model.oz_rad[0] = veh.omega_z * (math.pi / 180)  # initial angular rate (deg/s) - input
        veh.model.Vx[0] = veh.model.vx[0] * math.cos(veh.model.theta_rad[0]) - veh.model.vy[0] * math.sin(veh.model.theta_rad[0])
        veh.model.Vy[0] = veh.model.vx[0] * math.sin(veh.model.theta_rad[0]) + veh.model.vy[0] * math.cos(veh.model.theta_rad[0])

    for i in (range(len(vehicle_list[0].driver_input.t))):

        # step through each vehicle
        for veh in vehicle_list:
            veh.model.t[i] = round(i * dt_motion, 4)  # assigning time

            # get tire forces for t = 0
            veh = tire_forces(veh, i, sim_defaults)

            # setting vehicle forces to zero if no impact
            # impact may occur as a result of vehicle 2 motion in which case, the forces for t=i will be
            # updated for each vehicle
            if impact_type != 'SS':
                veh.model.Fx[i] = 0
                veh.model.Fy[i] = 0
                veh.model.Mz[i] = 0
            elif (impact_type == 'SS') & (impact == False):
                veh.model.Fx[i] = 0
                veh.model.Fy[i] = 0
                veh.model.Mz[i] = 0

            print(f"Model Fx: {veh.model.Fx[i]} at i: {i}")
            # local vehicle acceleration
            veh.model.au[i] = 32.2 / veh.weight * np.sum([veh.model.lf_fx[i],
                                                          veh.model.rf_fx[i],
                                                          veh.model.rr_fx[i],
                                                          veh.model.lr_fx[i],
                                                          veh.model.Fx[i]])

            veh.model.av[i] = 32.2 / veh.weight * np.sum([veh.model.lf_fy[i],
                                                          veh.model.rf_fy[i],
                                                          veh.model.rr_fy[i],
                                                          veh.model.lr_fy[i],
                                                          veh.model.Fy[i]])

            # rotation acceleration - alpha-z
            veh.model.alphaz[i] = (1 / veh.izz) * np.sum([veh.model.lf_fx[i] * veh.track / 2,
                                                          veh.model.lf_fy[i] * veh.lcgf,
                                                          -1 * veh.model.rf_fx[i] * veh.track / 2,
                                                          veh.model.rf_fy[i] * veh.lcgf,
                                                          -1 * veh.model.rr_fx[i] * veh.track / 2,
                                                          -1 * veh.model.rr_fy[i] * veh.lcgr,
                                                          veh.model.lr_fx[i] * veh.track / 2,
                                                          -1 * veh.model.lr_fy[i] * veh.lcgr,
                                                         veh.model.Mz[i]])

            if i == 0:
                # vehicle acceleration in inertial frame
                veh.model.ax[i] = veh.model.au[i] + veh.model.oz_rad[i] * veh.model.vy[i]
                veh.model.ay[i] = veh.model.av[i] - veh.model.oz_rad[i] * veh.model.vx[i]
                veh.model.ar[i] = math.sqrt(veh.model.ax[i] ** 2 + veh.model.ay[i] ** 2)

                # inertial frame coorindates - capital letters
                veh.model.Ax[i] = veh.model.au[i] * math.cos(veh.model.theta_rad[i]) - veh.model.av[i] * math.sin(veh.model.theta_rad[i])
                veh.model.Ay[i] = veh.model.au[i] * math.sin(veh.model.theta_rad[i]) + veh.model.av[i] * math.cos(veh.model.theta_rad[i])

            if i > 0:
                # vehicle acceleration in inertial frame
                veh.model.ax[i] = veh.model.au[i] + veh.model.oz_rad[i - 1] * veh.model.vy[i - 1]
                veh.model.ay[i] = veh.model.av[i] - veh.model.oz_rad[i - 1] * veh.model.vx[i - 1]
                veh.model.ar[i] = math.sqrt(veh.model.ax[i] ** 2 + veh.model.ay[i] ** 2)

                # vehicle velocities
                veh.model.vx[i] = veh.model.vx[i - 1] + dt_motion * np.mean([veh.model.ax[i - 1], veh.model.ax[i]])
                veh.model.vy[i] = veh.model.vy[i - 1] + dt_motion * np.mean([veh.model.ay[i - 1], veh.model.ay[i]])

                # omega
                veh.model.oz_rad[i] = veh.model.oz_rad[i - 1] + dt_motion * np.mean([veh.model.alphaz[i - 1], veh.model.alphaz[i]])

                # heading angle
                veh.model.theta_rad[i] = veh.model.theta_rad[i - 1] + dt_motion * np.mean([veh.model.oz_rad[i], veh.model.oz_rad[i - 1]])

                # inertial frame coorindates - capital letters
                veh.model.Ax[i] = veh.model.au[i] * math.cos(veh.model.theta_rad[i]) - veh.model.av[i] * math.sin(veh.model.theta_rad[i])
                veh.model.Ay[i] = veh.model.au[i] * math.sin(veh.model.theta_rad[i]) + veh.model.av[i] * math.cos(veh.model.theta_rad[i])

                veh.model.Vx[i] = veh.model.Vx[i - 1] + dt_motion * np.mean([veh.model.Ax[i - 1], veh.model.Ax[i]])
                veh.model.Vy[i] = veh.model.Vy[i - 1] + dt_motion * np.mean([veh.model.Ay[i - 1], veh.model.Ay[i]])

                # velocity vector in inertial frame
                veh.model.beta_rad[i] = math.atan2(veh.model.Vy[i], veh.model.Vx[i])  # move to seperate calc

            # vehicle position
            veh.model['Dx'] = veh.init_x_pos + integrate.cumtrapz(list(veh.model.Vx), list(veh.model.t), initial=0)
            veh.model['Dy'] = veh.init_y_pos + integrate.cumtrapz(list(veh.model.Vy), list(veh.model.t), initial=0)
            veh.model.alphaz_deg = [row * 180 / math.pi for row in veh.model.alphaz]  # move to seperate calc
            veh.model.oz_deg = [row * 180 / math.pi for row in veh.model.oz_rad]  # move to seperate calc
            veh.model.theta_deg = [row * 180 / math.pi for row in veh.model.theta_rad]  # move to seperate calc
            veh.model.beta_deg = [row * 180 / math.pi for row in veh.model.beta_rad]  # move to seperate calc

        # detect impact using current vehicle positions after first iterations
        if i == 0:
            crush_data = None

        """
        for multiple crashes, vehicles need to seperate before second impact is allowed
        """

        if impc_complete == False:
            crush_data = detect(vehicle_list, i, crush_data)

        print(f"Impact Detect: {crush_data.impact[i]} at i: {i}")
        if (crush_data.impact[i] == True) & (impc_complete == False):
            impact = True
            print(f'Impact detected at t = {veh.model.t[i]} seconds')
            print(f'i: {i}')
            if impact_type == 'IMPC':
                vehicle_list, impc_energy = impc(i, crush_data.impactp_veh2x[i], crush_data.impactp_veh2y[i], vehicle_list=vehicle_list,
                                                 sim_defaults=sim_defaults)  # run impc model - create inputs using vehicle class
                veh.model.Fx[i] = 0
                veh.model.Fy[i] = 0
                veh.model.Mz[i] = 0
                impc_complete = True  # <- only run IMPC model once
            elif impact_type == 'SS':
                vehicle_list = ss(vehicle_list, crush_data, kmutual, vehicle_mu, i)
            else:
                print(f'impact_type {impact_type} is not defined - no impact forces generated')
                veh.model.Fx[i] = 0
                veh.model.Fy[i] = 0
                veh.model.Mz[i] = 0


    return vehicle_list, crush_data
