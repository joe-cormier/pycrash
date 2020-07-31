"""
Tire Model - Calculates forces at each tire
accounts for pitch due to braking and roll from cornering forces

Dependencies - v, vx, vy, au, av, omega, constants
"""
from data.defaults.config import default_dict
import math
import numpy as np
import pandas as pd
import csv
import os

# load defaults
mu_max = default_dict['mu_max']                  # maximum available friction
dt_motion = default_dict['dt_motion']            # iteration time step
alpha_max = default_dict['alpha_max']             # maximum tire slip angle (rad)


"""
TODO: detailed suspension properties
roll_rate = 6    # semi-firm 7 = semi soft, 3 = extremely firm (corvette) (degrees / g)
rc_cg = 18/12    # passenger car - roll center to cg height (h1)  (ft)
roll_h = 6/12    # roll center height
"""

def tire_forces(veh, i):
    """
    calculate tire forces for the given time step
    """

    # create dataframe and add data row
    if i == 0:  # setting initial vertical force
        # TODO: incorporate grade / bank
        veh.model.lf_fz[i] = 0.5 * veh.weight * veh.lcgr / veh.wb
        veh.model.rf_fz[i] = 0.5 * veh.weight * veh.lcgr / veh.wb
        veh.model.rr_fz[i] = 0.5 * veh.weight * veh.lcgf / veh.wb
        veh.model.lr_fz[i] = 0.5 * veh.weight * veh.lcgf / veh.wb


    # ------------    Initialize Vehicle Tire Variables ------------------------ #

    ffs = veh.weight * veh.lcgr / veh.wb  # Force Static Front
    frs = veh.weight * veh.lcgf / veh.wb  # Force Static Rear
    ffaxl = ffs
    fraxl = frs

    # --------- Loop through tire force calculations --------------------------- #

    # Forward / Rearward weight shift due to braking or acceleration
    if veh.model.au[i] == 0:
        ffaxl == ffs
        fraxl = frs
    elif veh.model.au[i] != 0:
        ffaxl = ffs - veh.weight * (veh.model.au[i] / 32.2) * veh.hcg / veh.wb
        fraxl = frs + veh.weight * (veh.model.au[i] / 32.2) * veh.hcg / veh.wb

    # Left / Right weight shift due to cornering - vehicle dynamics - modular?
    # mf = ((roll_rate * veh.weight * rc_cg * (av / 32.2)) / (roll_rate + roll_rate - veh.weight * rc_cg)) + ffs * roll_h * (av / 32.2) # front moment - in terms of av vs turning radius
    # mr = ((roll_rate * veh.weight * rc_cg * (av / 32.2)) / (roll_rate + roll_rate - veh.weight * rc_cg)) + frs * roll_h * (av / 32.2)  # rear moment - in terms of av vs turning radius
    df_roll = math.fabs((ffs * veh.hcg * veh.model.av[i] / 32.2) / veh.track)  # change in vertical force from roll moment - front
    dr_roll = math.fabs((frs * veh.hcg * veh.model.av[i] / 32.2) / veh.track)  # rear

    # calcualtion vertical force at each tire accounting for pitch and roll
    # account for inside / outside of turn - in a positive turn (right) av will be positive
    if veh.model.av[i] == 0:
        veh.model.lf_fz[i] = ffaxl / 2  # no acceleration - no shift in weight
        veh.model.rf_fz[i] = ffaxl / 2
        veh.model.rr_fz[i] = fraxl / 2
        veh.model.lr_fz[i] = fraxl / 2
    elif veh.model.av[i] > 0:
        veh.model.lf_fz[i] = ffaxl / 2 + df_roll  # outside tire
        veh.model.rf_fz[i] = ffaxl / 2 - df_roll  # inside tire
        veh.model.rr_fz[i] = fraxl / 2 - dr_roll  # inside tire
        veh.model.lr_fz[i] = fraxl / 2 + dr_roll  # outside tire
    elif veh.model.av[i] < 0:
        veh.model.lf_fz[i] = ffaxl / 2 - df_roll  # inside tire
        veh.model.rf_fz[i] = ffaxl / 2 + df_roll  # outside tire
        veh.model.rr_fz[i] = fraxl / 2 + dr_roll  # outside tire
        veh.model.lr_fz[i] = fraxl / 2 - dr_roll  # inside tire
    else:
        print(f'Vehicle av Not Defined i = {i}, time = {veh.model.t[i]}')

    # ------------------------ Left Front Tire ----------------------------------- #
    veh.model.lf_lock[i] = 0  # locked status of Left Front Wheel - initially set to unlocked
    veh.model.lf_alpha[i] = veh.model.delta_rad[i] - np.arctan2((veh.model.vy[i] + veh.model.oz_rad[i] * veh.lcgf),
                                                  (veh.model.vx[i] + veh.model.oz_rad[i] * (veh.track / 2)))  # tire slip angle (rad)

    if math.fabs(veh.model.lf_alpha[i]) >= alpha_max:  # following Steffan 1996 SAE No. 960886
        lf_latf = np.sign(veh.model.lf_alpha[i]) * mu_max * veh.model.lf_fz[i]  # lateral force if alpha is greater than maximum slip angle - input
    else:
        lf_latf = veh.model.lf_alpha[i] / alpha_max * mu_max * veh.model.lf_fz[i]  # lateral force for slip angle less than maximum allowed - input

    # longitudinal Force Applied = f(Vehicle drive tires)
    if veh.fwd == 1:
        lf_app = veh.model.lf_fz[i] * (mu_max * (veh.driver_input.throttle[i] / 2 - veh.driver_input.brake[i]))  # longitudinal force applied throttle and braking are expressed as % of total friction, will not occur at same time, so add for efficiency
    elif veh.rwd == 1:
        lf_app = -1 * veh.model.lf_fz[i] * (mu_max * veh.driver_input.brake[i])  # rear wheel drive, front wheel will not apply accelerative force
    elif veh.awd == 1:
        lf_app = veh.model.lf_fz[i] * (mu_max * (veh.driver_input.throttle[i] / 4 - veh.driver_input.brake[i]))

    if math.sqrt(lf_app ** 2 + lf_latf ** 2) >= mu_max * veh.model.lf_fz[i]:  # Equation 3 - is the force applied greater than available from friction at tire?
        veh.model.lf_lock[i] = 1
        lf_lonf = -1 * math.cos(veh.model.lf_alpha[i]) * mu_max * veh.model.lf_fz[i]  # force will be applied in the direction opposite of vehicle motion
        lf_latf = math.sin(veh.model.lf_alpha[i]) * mu_max * veh.model.lf_fz[i]
    elif math.sqrt(lf_app ** 2 + lf_latf ** 2) < mu_max * veh.model.lf_fz[i]:
        veh.model.lf_lock[i] = 0
        lf_lonf = lf_app
        lf_latf = veh.model.lf_alpha[i] / alpha_max * mu_max * veh.model.lf_fz[i]

    # ------------------------ Right Front Tire ----------------------------------- #
    veh.model.rf_lock[i] = 0  # locked status - initially set to unlocked
    veh.model.rf_alpha[i] = veh.model.delta_rad[i] - np.arctan2(veh.model.vy[i] + veh.model.oz_rad[i] * veh.lcgf,
                                                  (veh.model.vx[i] - veh.model.oz_rad[i] * (veh.track / 2)))  # tire slip angle (rad)

    if math.fabs(veh.model.rf_alpha[i]) >= alpha_max:  # following Steffan 1996 SAE No. 960886
        rf_latf = np.sign(veh.model.rf_alpha[i]) * mu_max * veh.model.rf_fz[i]  # lateral force if alpha is greater than maximum slip angle - input
    else:
        rf_latf = veh.model.rf_alpha[i] / alpha_max * mu_max * veh.model.rf_fz[i]  # lateral force for slip angle less than maximum allowed - input

    # longitudinal Force Applied = f(Vehicle drive tires)
    if veh.fwd == 1:
        rf_app = veh.model.rf_fz[i] * (mu_max * (veh.driver_input.throttle[i] / 2 - veh.driver_input.brake[i]))  # longitudinal force applied throttle and braking are expressed as % of total friction, will not occur at same time, so add for efficiency
    elif veh.rwd == 1:
        rf_app = -1 * veh.model.rf_fz[i] * (mu_max * veh.driver_input.brake[i])  # rear wheel drive, front wheel will not apply accelerative force
    elif veh.awd == 1:
        rf_app = veh.model.rf_fz[i] * (mu_max * (veh.driver_input.throttle[i] / 4) - veh.driver_input.brake[i])

    if math.sqrt(rf_app ** 2 + rf_latf ** 2) >= mu_max * veh.model.rf_fz[i]:
        veh.model.rf_lock[i] = 1
        rf_lonf = -1 * math.cos(veh.model.rf_alpha[i]) * mu_max * veh.model.rf_fz[i]
        rf_latf = math.sin(veh.model.rf_alpha[i]) * mu_max * veh.model.rf_fz[i]
    elif math.sqrt(rf_app ** 2 + rf_latf ** 2) < mu_max * veh.model.rf_fz[i]:
        veh.model.rf_lock[i] = 0
        rf_lonf = rf_app
        rf_latf = veh.model.rf_alpha[i] / alpha_max * mu_max * veh.model.rf_fz[i]

    # ------------------------ Right Rear Tire ----------------------------------- #
    veh.model.rr_lock[i] = 0  # locked status - initially set to unlocked

    veh.model.rr_alpha[i] = -1 * np.arctan2(veh.model.vy[i] - veh.model.oz_rad[i] * veh.lcgr,
                               (veh.model.vx[i] - veh.model.oz_rad[i] * (veh.track / 2)))  # tire slip angle (rad)

    if math.fabs(veh.model.rr_alpha[i]) >= alpha_max:  # following Steffan 1996 SAE No. 960886
        rr_latf = np.sign(veh.model.rr_alpha[i]) * mu_max * veh.model.rr_fz[i]  # lateral force if alpha is greater than maximum slip angle - input
    else:
        rr_latf = veh.model.rr_alpha[i] / alpha_max * mu_max * veh.model.rr_fz[i]  # lateral force for slip angle less than maximum allowed - input

    # longitudinal Force Applied = f(Vehicle drive tires)
    if veh.fwd == 1:
        rr_app = -1 * veh.model.rr_fz[i] * (mu_max * veh.driver_input.brake[i])  # front wheel drive, rear wheel will not apply accelerative force
    elif veh.rwd == 1:
        rr_app = veh.model.rr_fz[i] * (mu_max * (veh.driver_input.throttle[i] / 2 - veh.driver_input.brake[i]))  # longitudinal force applied throttle and braking are expressed as % of total friction, will not occur at same time, so add for efficiency   (cons['mu_max'] * (veh.driver_input.throttle[i] - veh.driver_input.brake[i]) / 2)
    elif veh.awd == 1:
        rr_app = veh.model.rr_fz[i] * (mu_max * (veh.driver_input.throttle[i] / 4 - veh.driver_input.brake[i]))

    if math.sqrt(rr_app ** 2 + rr_latf ** 2) >= mu_max * veh.model.rr_fz[i]:
        veh.model.rr_lock[i] = 1
        rr_lonf = -1 * math.cos(veh.model.rr_alpha[i]) * mu_max * veh.model.rr_fz[i]
        rr_latf = math.sin(veh.model.rr_alpha[i]) * mu_max * veh.model.rr_fz[i]
    elif math.sqrt(rr_app ** 2 + rr_latf ** 2) < mu_max * veh.model.rr_fz[i]:
        veh.model.rr_lock[i] = 0
        rr_lonf = rr_app
        rr_latf = veh.model.rr_alpha[i] / alpha_max * mu_max * veh.model.rr_fz[i]

    # ------------------------ Left Rear Tire ------------------------------------ #
    veh.model.lr_lock[i] = 0  # locked status - initially set to unlocked
    veh.model.lr_alpha[i] = -1 * np.arctan2(veh.model.vy[i] - veh.model.oz_rad[i] * veh.lcgr,
                               (veh.model.vx[i] + veh.model.oz_rad[i] * (veh.track / 2)))  # tire slip angle (rad)

    if math.fabs(veh.model.lr_alpha[i]) >= alpha_max:  # following Steffan 1996 SAE No. 960886
        lr_latf = np.sign(veh.model.lr_alpha[i]) * mu_max * veh.model.lr_fz[i]  # lateral force if alpha is greater than maximum slip angle - input
    else:
        lr_latf = veh.model.rr_alpha[i] / alpha_max * mu_max * veh.model.lr_fz[i]  # lateral force for slip angle less than maximum allowed - input

    # longitudinal Force Applied = f(Vehicle drive tires)
    if veh.fwd == 1:
        lr_app = -1 * veh.model.lr_fz[i] * (mu_max * veh.driver_input.brake[i])  # front wheel drive, rear wheel will not apply accelerative force
    elif veh.rwd == 1:
        lr_app = veh.model.lr_fz[i] * (mu_max * (veh.driver_input.throttle[i] / 2 - veh.driver_input.brake[i]))  # longitudinal force applied throttle and braking are expressed as % of total friction, will not occur at same time, so add for efficiency   (cons['mu_max'] * (veh.driver_input.throttle[i] - veh.driver_input.brake[i]) / 2)
    elif veh.awd == 1:
        lr_app = veh.model.lr_fz[i] * (mu_max * (veh.driver_input.throttle[i] / 4 - veh.driver_input.brake[i]))

    if math.sqrt(lr_app ** 2 + lr_latf ** 2) >= mu_max * veh.model.lr_fz[i]:
        veh.model.lr_lock[i] = 1
        lr_lonf = -1 * math.cos(veh.model.lr_alpha[i]) * mu_max * veh.model.lr_fz[i]
        lr_latf = math.sin(veh.model.lr_alpha[i]) * mu_max * veh.model.lr_fz[i]
    elif math.sqrt(lr_app ** 2 + lr_latf ** 2) < mu_max * veh.model.lr_fz[i]:
        veh.model.lr_lock[i] = 0
        lr_lonf = lr_app
        lr_latf = veh.model.lr_alpha[i] / alpha_max * mu_max * veh.model.lr_fz[i]

    # Calculate vehicle forces in vehicle frame
    # Left Front Tire #
    veh.model.lf_fx[i] = lf_lonf * math.cos(veh.model.delta_rad[i]) - lf_latf * math.sin(veh.model.delta_rad[i])
    veh.model.lf_fy[i] = lf_lonf * math.sin(veh.model.delta_rad[i]) + lf_latf * math.cos(veh.model.delta_rad[i])
    # Right Front Tire #
    veh.model.rf_fx[i] = rf_lonf * math.cos(veh.model.delta_rad[i]) - rf_latf * math.sin(veh.model.delta_rad[i])
    veh.model.rf_fy[i] = rf_lonf * math.sin(veh.model.delta_rad[i]) + rf_latf * math.cos(veh.model.delta_rad[i])
    # Right Rear Tire #
    veh.model.rr_fx[i] = rr_lonf
    veh.model.rr_fy[i] = rr_latf
    # Left Rear Tire #
    veh.model.lr_fx[i] = lr_lonf
    veh.model.lr_fy[i] = lr_latf

    return veh
