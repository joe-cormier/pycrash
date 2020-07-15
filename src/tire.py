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

def tire_model(v, veh, i):
    # global lf_fz, rf_fz, rr_fz, lr_fz, lf_lonf, lf_latf, rf_lonf, rf_latf, rr_lonf, rr_latf, lr_lonf, lr_latf

    # create dataframe and add data row
    if i == 0:  # setting initial tire forces to zero at t=0
        lf_fx = 0
        lf_fy = 0
        rf_fx = 0
        rf_fy = 0
        rr_fx = 0
        rr_fy = 0
        lr_fx = 0
        lr_fy = 0
        lf_alpha = 0
        rf_alpha = 0
        rr_alpha = 0
        lr_alpha = 0
        lf_lock = 0
        rf_lock = 0
        rr_lock = 0
        lr_lock = 0
        lf_fz = 0.5 * veh.weight * veh.lcgr / veh.wb
        rf_fz = 0.5 * veh.weight * veh.lcgr / veh.wb
        rr_fz = 0.5 * veh.weight * veh.lcgf / veh.wb
        lr_fz = 0.5 * veh.weight * veh.lcgf / veh.wb
        return lf_fx, lf_fy, rf_fx, rf_fy, rr_fx, rr_fy, lr_fx, lr_fy, lf_alpha, rf_alpha, rr_alpha, lr_alpha, lf_lock, rf_lock, rr_lock, lr_lock, lf_fz, rf_fz, rr_fz, lr_fz

    else:

        # ------------    Initialize Vehicle Tire Variables ------------------------ #

        ffs = veh.weight * veh.lcgr / veh.wb  # Force Static Front
        frs = veh.weight * veh.lcgf / veh.wb  # Force Static Rear
        ffaxl = ffs
        fraxl = frs

        # --------- Loop through tire force calculations --------------------------- #

        au = v.loc[i, 'au']
        av = v.loc[i, 'av']
        vx = v.loc[i, 'vx']
        vy = v.loc[i, 'vy']
        oz_rad = v.loc[i, 'oz_rad']

        # Forward / Rearward weight shift due to braking or acceleration
        if au == 0:
            ffaxl == ffs
            fraxl = frs
        elif au != 0:
            ffaxl = ffs - veh.weight * (au / 32.2) * veh.hcg / veh.wb
            fraxl = frs + veh.weight * (au / 32.2) * veh.hcg / veh.wb

        # Left / Right weight shift due to cornering - vehicle dynamics - modular?
        # mf = ((roll_rate * veh.weight * rc_cg * (av / 32.2)) / (roll_rate + roll_rate - veh.weight * rc_cg)) + ffs * roll_h * (av / 32.2) # front moment - in terms of av vs turning radius
        # mr = ((roll_rate * veh.weight * rc_cg * (av / 32.2)) / (roll_rate + roll_rate - veh.weight * rc_cg)) + frs * roll_h * (av / 32.2)  # rear moment - in terms of av vs turning radius
        df_roll = math.fabs((ffs * veh.hcg * av / 32.2) / veh.track)  # change in vertical force from roll moment - front
        dr_roll = math.fabs((frs * veh.hcg * av / 32.2) / veh.track)  # rear

        # calcualtion vertical force at each tire accounting for pitch and roll
        # account for inside / outside of turn - in a positive turn (right) av will be positive
        if av == 0:
            lf_fz = ffaxl / 2  # no acceleration - no shift in weight
            rf_fz = ffaxl / 2
            rr_fz = fraxl / 2
            lr_fz = fraxl / 2
        elif av > 0:
            lf_fz = ffaxl / 2 + df_roll  # outside tire
            rf_fz = ffaxl / 2 - df_roll  # inside tire
            rr_fz = fraxl / 2 - dr_roll  # inside tire
            lr_fz = fraxl / 2 + dr_roll  # outside tire
        elif av < 0:
            lf_fz = ffaxl / 2 - df_roll  # inside tire
            rf_fz = ffaxl / 2 + df_roll  # outside tire
            rr_fz = fraxl / 2 + dr_roll  # outside tire
            lr_fz = fraxl / 2 - dr_roll  # inside tire
        else:
            print('Vehicle av Not Defined')

        # ------------------------ Left Front Tire ----------------------------------- #
        lf_lock = 0  # locked status of Left Front Wheel - initially set to unlocked
        lf_alpha = v.loc[i, 'delta_rad'] - np.arctan2((vy + oz_rad * veh.lcgf),
                                                      (vx + oz_rad * (veh.track / 2)))  # tire slip angle (rad)

        if math.fabs(lf_alpha) >= alpha_max:  # following Steffan 1996 SAE No. 960886
            lf_latf = np.sign(lf_alpha) * mu_max * lf_fz  # lateral force if alpha is greater than maximum slip angle - input
        else:
            lf_latf = lf_alpha / alpha_max * mu_max * lf_fz  # lateral force for slip angle less than maximum allowed - input

        # longitudinal Force Applied = f(Vehicle drive tires)
        if veh.fwd == 1:
            lf_app = lf_fz * (mu_max * (v.loc[i, 'throttle'] / 2 - v.loc[
                i, 'brake']))  # longitudinal force applied throttle and braking are expressed as % of total friction, will not occur at same time, so add for efficiency
        elif veh.rwd == 1:
            lf_app = -1 * lf_fz * (mu_max * v.loc[
                i, 'brake'])  # rear wheel drive, front wheel will not apply accelerative force
        elif veh.awd == 1:
            lf_app = lf_fz * (mu_max * (v.loc[i, 'throttle'] / 4 - v.loc[i, 'brake']))

        if math.sqrt(lf_app ** 2 + lf_latf ** 2) >= mu_max * lf_fz:  # Equation 3 - is the force applied greater than available from friction at tire?
            lf_lock = 1
            lf_lonf = -1 * math.cos(lf_alpha) * mu_max * lf_fz  # force will be applied in the direction opposite of vehicle motion
            lf_latf = math.sin(lf_alpha) * mu_max * lf_fz
        elif math.sqrt(lf_app ** 2 + lf_latf ** 2) < mu_max * lf_fz:
            lf_lock = 0
            lf_lonf = lf_app
            lf_latf = lf_alpha / alpha_max * mu_max * lf_fz

        # ------------------------ Right Front Tire ----------------------------------- #
        rf_lock = 0  # locked status - initially set to unlocked
        rf_alpha = v.loc[i, 'delta_rad'] - np.arctan2(vy + oz_rad * veh.lcgf,
                                                      (vx - oz_rad * (veh.track / 2)))  # tire slip angle (rad)

        if math.fabs(rf_alpha) >= alpha_max:  # following Steffan 1996 SAE No. 960886
            rf_latf = np.sign(rf_alpha) * mu_max * rf_fz  # lateral force if alpha is greater than maximum slip angle - input
        else:
            rf_latf = rf_alpha / alpha_max * mu_max * rf_fz  # lateral force for slip angle less than maximum allowed - input

        # longitudinal Force Applied = f(Vehicle drive tires)
        if veh.fwd == 1:
            rf_app = rf_fz * (mu_max * (v.loc[i, 'throttle'] / 2 - v.loc[
                i, 'brake']))  # longitudinal force applied throttle and braking are expressed as % of total friction, will not occur at same time, so add for efficiency
        elif veh.rwd == 1:
            rf_app = -1 * rf_fz * (mu_max * v.loc[
                i, 'brake'])  # rear wheel drive, front wheel will not apply accelerative force
        elif veh.awd == 1:
            rf_app = rf_fz * (mu_max * (v.loc[i, 'throttle'] / 4) - v.loc[i, 'brake'])

        if math.sqrt(rf_app ** 2 + rf_latf ** 2) >= mu_max * rf_fz:
            rf_lock = 1
            rf_lonf = -1 * math.cos(rf_alpha) * mu_max * rf_fz
            rf_latf = math.sin(rf_alpha) * mu_max * rf_fz
        elif math.sqrt(rf_app ** 2 + rf_latf ** 2) < mu_max * rf_fz:
            rf_lock = 0
            rf_lonf = rf_app
            rf_latf = rf_alpha / alpha_max * mu_max * rf_fz

        # ------------------------ Right Rear Tire ----------------------------------- #
        rr_lock = 0  # locked status - initially set to unlocked

        rr_alpha = -1 * np.arctan2(vy - oz_rad * veh.lcgr,
                                   (vx - oz_rad * (veh.track / 2)))  # tire slip angle (rad)

        if math.fabs(rr_alpha) >= alpha_max:  # following Steffan 1996 SAE No. 960886
            rr_latf = np.sign(rr_alpha) * mu_max * rr_fz  # lateral force if alpha is greater than maximum slip angle - input
        else:
            rr_latf = rr_alpha / alpha_max * mu_max * rr_fz  # lateral force for slip angle less than maximum allowed - input

        # longitudinal Force Applied = f(Vehicle drive tires)
        if veh.fwd == 1:
            rr_app = -1 * rr_fz * (mu_max * v.loc[
                i, 'brake'])  # front wheel drive, rear wheel will not apply accelerative force
        elif veh.rwd == 1:
            rr_app = rr_fz * (mu_max * (v.loc[i, 'throttle'] / 2 - v.loc[
                i, 'brake']))  # longitudinal force applied throttle and braking are expressed as % of total friction, will not occur at same time, so add for efficiency   (cons['mu_max'] * (v.loc[i, 'throttle'] - v.loc[i, 'brake']) / 2)
        elif veh.awd == 1:
            rr_app = rr_fz * (mu_max * (v.loc[i, 'throttle'] / 4 - v.loc[i, 'brake']))

        if math.sqrt(rr_app ** 2 + rr_latf ** 2) >= mu_max * rr_fz:
            rr_lock = 1
            rr_lonf = -1 * math.cos(rr_alpha) * mu_max * rr_fz
            rr_latf = math.sin(rr_alpha) * mu_max * rr_fz
        elif math.sqrt(rr_app ** 2 + rr_latf ** 2) < mu_max * rr_fz:
            rr_lock = 0
            rr_lonf = rr_app
            rr_latf = rr_alpha / alpha_max * mu_max * rr_fz

        # ------------------------ Left Rear Tire ------------------------------------ #
        lr_lock = 0  # locked status - initially set to unlocked
        lr_alpha = -1 * np.arctan2(vy - oz_rad * veh.lcgr,
                                   (vx + oz_rad * (veh.track / 2)))  # tire slip angle (rad)

        if math.fabs(lr_alpha) >= alpha_max:  # following Steffan 1996 SAE No. 960886
            lr_latf = np.sign(lr_alpha) * mu_max * lr_fz  # lateral force if alpha is greater than maximum slip angle - input
        else:
            lr_latf = rr_alpha / alpha_max * mu_max * lr_fz  # lateral force for slip angle less than maximum allowed - input

        # longitudinal Force Applied = f(Vehicle drive tires)
        if veh.fwd == 1:
            lr_app = -1 * lr_fz * (mu_max * v.loc[i, 'brake'])  # front wheel drive, rear wheel will not apply accelerative force
        elif veh.rwd == 1:
            lr_app = lr_fz * (mu_max * (v.loc[i, 'throttle'] / 2 - v.loc[i, 'brake']))  # longitudinal force applied throttle and braking are expressed as % of total friction, will not occur at same time, so add for efficiency   (cons['mu_max'] * (v.loc[i, 'throttle'] - v.loc[i, 'brake']) / 2)
        elif veh.awd == 1:
            lr_app = lr_fz * (mu_max * (v.loc[i, 'throttle'] / 4 - v.loc[i, 'brake']))

        if math.sqrt(lr_app ** 2 + lr_latf ** 2) >= mu_max * lr_fz:
            lr_lock = 1
            lr_lonf = -1 * math.cos(lr_alpha) * mu_max * lr_fz
            lr_latf = math.sin(lr_alpha) * mu_max * lr_fz
        elif math.sqrt(lr_app ** 2 + lr_latf ** 2) < mu_max * lr_fz:
            lr_lock = 0
            lr_lonf = lr_app
            lr_latf = lr_alpha / alpha_max * mu_max * lr_fz

        # Calculate vehicle forces in vehicle frame
        # Left Front Tire #
        lf_fx = lf_lonf * math.cos(v.loc[i, 'delta_rad']) - lf_latf * math.sin(v.loc[i, 'delta_rad'])
        lf_fy = lf_lonf * math.sin(v.loc[i, 'delta_rad']) + lf_latf * math.cos(v.loc[i, 'delta_rad'])
        # Right Front Tire #
        rf_fx = rf_lonf * math.cos(v.loc[i, 'delta_rad']) - rf_latf * math.sin(v.loc[i, 'delta_rad'])
        rf_fy = rf_lonf * math.sin(v.loc[i, 'delta_rad']) + rf_latf * math.cos(v.loc[i, 'delta_rad'])
        # Right Rear Tire #
        rr_fx = rr_lonf
        rr_fy = rr_latf
        # Left Rear Tire #
        lr_fx = lr_lonf
        lr_fy = lr_latf

        # compile data into row
        # data = [t, ffs, frs, ffaxl, fraxl, mf, mr, lf_fz, rf_fz, rr_fz, lr_fz, lf_lock, lf_alpha, lf_latf, lf_lonf , lf_app, rf_lock, rf_alpha, rf_latf, rf_lonf, rf_app,
        #        rr_lock, rr_alpha, rr_latf, rr_lonf, rr_app, lr_lock, lr_alpha, lr_latf, lr_lonf, lr_app]

        # append data to dataframe after i = 0
        return lf_fx, lf_fy, rf_fx, rf_fy, rr_fx, rr_fy, lr_fx, lr_fy, lf_alpha, rf_alpha, rr_alpha, lr_alpha, lf_lock, rf_lock, rr_lock, lr_lock, lf_fz, rf_fz, rr_fz, lr_fz


#del lf_fx, lf_fy, rf_fx, rf_fy, rr_fx, rr_fy, lr_fx, lr_fy, lf_alpha, rf_alpha, rr_alpha, lr_alpha, lf_lock, rf_lock, rr_lock, lr_lock, lf_fz, rf_fz, rr_fz, lr_fz, lf_lonf, lf_latf, rf_lonf, rf_latf, rr_lonf, rr_latf, lr_lonf, lr_latf
