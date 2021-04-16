from .model_calcs.tire_model import tire_forces
import pandas as pd
import numpy as np
from scipy import integrate
import math

"""
comprehensive vehicle model that can be used to run single vehicle motion as well as
impact related motion
"""

# TODO: ignore driver inputs after impact
# TODO: disable tire after impact

def multi_vehicle_model(veh, i, sim_defaults, impact_type, ignore_driver=False, kmutual=None, vehicle_mu=None):
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
    #print(f'i in vehicle model {i}')

    dt_motion = sim_defaults['dt_motion']
    veh.model.t[i] = round(i * dt_motion, 4)  # assigning time
    #print(round(i * dt_motion, 4))
    #print(veh.model.t[i])
    # get tire forces for t = 0
    veh = tire_forces(veh, i, sim_defaults)

    # setting vehicle forces to zero if no impact
    # impact may occur as a result of vehicle 2 motion in which case, the forces for t=i will be
    # updated for each vehicle
    # TODO: update for sideswipe / force model
    veh.model.Fx[i] = 0
    veh.model.Fy[i] = 0
    veh.model.Mz[i] = 0
    """
    if impact_type != 'SS':
        veh.model.Fx[i] = 0
        veh.model.Fy[i] = 0
        veh.model.Mz[i] = 0
    elif (impact_type == 'SS') & (impact == False):
        veh.model.Fx[i] = 0
        veh.model.Fy[i] = 0
        veh.model.Mz[i] = 0
    """

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
        veh.model.ar[i] = np.sqrt(veh.model.ax[i] ** 2 + veh.model.ay[i] ** 2)

        # inertial frame coorindates - capital letters
        veh.model.Ax[i] = veh.model.au[i] * np.cos(veh.model.theta_rad[i]) - veh.model.av[i] * np.sin(veh.model.theta_rad[i])
        veh.model.Ay[i] = veh.model.au[i] * np.sin(veh.model.theta_rad[i]) + veh.model.av[i] * np.cos(veh.model.theta_rad[i])

    if i > 0:
        # vehicle acceleration in inertial frame
        veh.model.ax[i] = veh.model.au[i] + veh.model.oz_rad[i - 1] * veh.model.vy[i - 1]
        veh.model.ay[i] = veh.model.av[i] - veh.model.oz_rad[i - 1] * veh.model.vx[i - 1]
        veh.model.ar[i] = np.sqrt(veh.model.ax[i] ** 2 + veh.model.ay[i] ** 2)

        # vehicle velocities
        veh.model.vx[i] = veh.model.vx[i - 1] + dt_motion * np.mean([veh.model.ax[i - 1], veh.model.ax[i]])
        veh.model.vy[i] = veh.model.vy[i - 1] + dt_motion * np.mean([veh.model.ay[i - 1], veh.model.ay[i]])

        # omega
        veh.model.oz_rad[i] = veh.model.oz_rad[i - 1] + dt_motion * np.mean([veh.model.alphaz[i - 1], veh.model.alphaz[i]])

        # heading angle
        veh.model.theta_rad[i] = veh.model.theta_rad[i - 1] + dt_motion * np.mean([veh.model.oz_rad[i], veh.model.oz_rad[i - 1]])

        # inertial frame coorindates - capital letters
        veh.model.Ax[i] = veh.model.au[i] * np.cos(veh.model.theta_rad[i]) - veh.model.av[i] * np.sin(veh.model.theta_rad[i])
        veh.model.Ay[i] = veh.model.au[i] * np.sin(veh.model.theta_rad[i]) + veh.model.av[i] * np.cos(veh.model.theta_rad[i])

        veh.model.Vx[i] = veh.model.Vx[i - 1] + dt_motion * np.mean([veh.model.Ax[i - 1], veh.model.Ax[i]])
        veh.model.Vy[i] = veh.model.Vy[i - 1] + dt_motion * np.mean([veh.model.Ay[i - 1], veh.model.Ay[i]])

        # velocity vector in inertial frame
        # TODO: use numpy arctan2?
        veh.model.beta_rad[i] = math.atan2(veh.model.Vy[i], veh.model.Vx[i])  # move to seperate calc

    # vehicle position
    veh.model['Dx'] = veh.init_x_pos + integrate.cumtrapz(list(veh.model.Vx), list(veh.model.t), initial=0)
    veh.model['Dy'] = veh.init_y_pos + integrate.cumtrapz(list(veh.model.Vy), list(veh.model.t), initial=0)

    return veh
