"""
Tire Model - Calculates forces at each tire
accounts for pitch due to braking and roll from cornering forces

Dependencies - v, vx, vy, au, av, omega, constants
"""

import math
import numpy as np
import math

"""
TODO: detailed suspension properties
roll_rate = 6    # semi-firm 7 = semi soft, 3 = extremely firm (corvette) (degrees / g)
rc_cg = 18/12    # passenger car - roll center to cg height (h1)  (ft)
roll_h = 6/12    # roll center height
"""
def sign(x):
    # returns the sign of a number
    if x > 0:
        return 1
    elif x < 0:
        return -1
    elif x == 0:
        return 0


def tire_forces(veh, i, sim_defaults):
    """
    calculate tire forces for the given time step
    """
    # load defaults
    mu_max = sim_defaults['mu_max']  # maximum available friction
    tire_mu = 1
    alpha_max = sim_defaults['alpha_max']  # maximum tire slip angle (rad)
    alpha_max = alpha_max * mu_max
    # TODO: incorporate grade / bank

    if i == 0:
        j = i
    else:
        j = i - 1  # tire forces based on prior time step

    # current steer angle
    veh.model.delta_deg[i] = veh.driver_input.steer[i] / veh.steer_ratio   # steer angle (delta) will always be derived from driver input
    veh.model.delta_rad[i] = veh.model.delta_deg[i] * (math.pi/180)        # net steer angle

    # Ackerman steering
    if veh.model.delta_rad[i] > 0:   # positive steer
        r_net = veh.wb / np.tan(veh.model.delta_rad[i])  # turn radius  (Gillespie)
        rf_steer_angle = np.arctan(veh.wb / (r_net - veh.track))
        lf_steer_angle = veh.model.delta_rad[i]
    elif veh.model.delta_rad[i] < 0:
        r_net = veh.wb / np.tan(veh.model.delta_rad[i])  # turn radius  (Gillespie)
        rf_steer_angle = veh.model.delta_rad[i]
        lf_steer_angle = np.arctan(veh.wb / (r_net + veh.track))
    elif veh.model.delta_rad[i] == 0:
        rf_steer_angle = 0
        lf_steer_angle = 0

    # Forward / Rearward weight shift due to braking or acceleration
    veh_m = veh.weight / 32.2
    veh.model.lf_fz[i] = 0.5 * ((-veh_m * veh.model.au[j] * veh.hcg + veh.weight * veh.lcgr) / veh.wb + veh_m * veh.model.av[j] * veh.hcg / veh.track)
    veh.model.rf_fz[i] = 0.5 * ((-veh_m * veh.model.au[j] * veh.hcg + veh.weight * veh.lcgr) / veh.wb - veh_m * veh.model.av[j] * veh.hcg / veh.track)
    veh.model.rr_fz[i] = 0.5 * ((veh_m * veh.model.au[j] * veh.hcg + veh.weight * veh.lcgf) / veh.wb - veh_m * veh.model.av[j] * veh.hcg / veh.track)
    veh.model.lr_fz[i] = 0.5 * ((veh_m * veh.model.au[j] * veh.hcg + veh.weight * veh.lcgf) / veh.wb + veh_m * veh.model.av[j] * veh.hcg / veh.track)

    # ------------------------ Left Front Tire ----------------------------------- #
    # local velocity
    lf_vx = veh.model.vx[j] + veh.model.oz_rad[j] * (veh.track / 2)
    lf_vy = veh.model.vy[j] + veh.model.oz_rad[j] * veh.lcgf

    veh.model.lf_lock[i] = 0  # locked status of Left Front Wheel - initially set to unlocked
    veh.model.lf_alpha[i] = -1 * np.arctan2(lf_vy, lf_vx) + lf_steer_angle   # tire slip angle (rad)

    if math.fabs(veh.model.lf_alpha[i]) > alpha_max:  # following Steffan 1996 SAE No. 960886
        lf_latf = sign(veh.model.lf_alpha[i]) * mu_max * veh.model.lf_fz[i]  # lateral force if alpha is greater than maximum slip angle - input
    else:
        lf_latf = (veh.model.lf_alpha[i] / alpha_max) * mu_max * veh.model.lf_fz[i]  # lateral force for slip angle less than maximum allowed - input

    if veh.fwd == 1:
        lf_app = veh.model.lf_fz[i] * (mu_max * (veh.driver_input.throttle[i] - veh.driver_input.brake[i] * sign(lf_vx)))  # longitudinal force applied throttle and braking are expressed as % of total friction, will not occur at same time, so add for efficiency
    elif veh.rwd == 1:
        lf_app = -1 * veh.model.lf_fz[i] * (mu_max * veh.driver_input.brake[i] * sign(lf_vx))  # rear wheel drive, front wheel will not apply throttle force
    elif veh.awd == 1:
        lf_app = veh.model.lf_fz[i] * (mu_max * (veh.driver_input.throttle[i] - veh.driver_input.brake[i] * sign(lf_vx)))

    if math.sqrt(lf_app ** 2 + lf_latf ** 2) > (mu_max * veh.model.lf_fz[i]):  # Equation 3 - is the force applied greater than available from friction at tire?
        veh.model.lf_lock[i] = 1
        lf_lonf = -1 * sign(lf_vx) * math.cos(veh.model.lf_alpha[i]) * mu_max * veh.model.lf_fz[i]  # force will be applied in the direction opposite of vehicle motion
        lf_latf = math.sin(veh.model.lf_alpha[i]) * mu_max * veh.model.lf_fz[i]
    elif math.sqrt(lf_app ** 2 + lf_latf ** 2) <= mu_max * veh.model.lf_fz[i]:
        veh.model.lf_lock[i] = 0
        lf_lonf = lf_app
        lf_latf = lf_latf

    # ------------------------ Right Front Tire ----------------------------------- #
    # local velocity
    rf_vx = veh.model.vx[j] - veh.model.oz_rad[j] * (veh.track / 2)
    rf_vy = veh.model.vy[j] + veh.model.oz_rad[j] * veh.lcgf

    veh.model.rf_lock[i] = 0  # locked status - initially set to unlocked
    veh.model.rf_alpha[i] = -1 * np.arctan2(rf_vy, rf_vx) + rf_steer_angle  # tire slip angle (rad)

    if math.fabs(veh.model.rf_alpha[i]) > alpha_max:  # following Steffan 1996 SAE No. 960886
        rf_latf = sign(veh.model.rf_alpha[i]) * mu_max * veh.model.rf_fz[i]  # lateral force if alpha is greater than maximum slip angle - input
    else:
        rf_latf = (veh.model.rf_alpha[i] / alpha_max) * mu_max * veh.model.rf_fz[i]  # lateral force for slip angle less than maximum allowed - input

    # longitudinal Force Applied = f(Vehicle drive tires)
    if veh.fwd == 1:
        rf_app = veh.model.rf_fz[i] * (mu_max * (veh.driver_input.throttle[i] - veh.driver_input.brake[i] * sign(rf_vx)))  # longitudinal force applied throttle and braking are expressed as % of total friction, will not occur at same time, so add for efficiency
    elif veh.rwd == 1:
        rf_app = -1 * veh.model.rf_fz[i] * (mu_max * veh.driver_input.brake[i] * sign(rf_vx))  # rear wheel drive, front wheel will not apply accelerative force
    elif veh.awd == 1:
        rf_app = veh.model.rf_fz[i] * (mu_max * (veh.driver_input.throttle[i]) - veh.driver_input.brake[i] * sign(rf_vx))

    if math.sqrt(rf_app ** 2 + rf_latf ** 2) > mu_max * veh.model.rf_fz[i]:
        veh.model.rf_lock[i] = 1
        rf_lonf = -1 * sign(rf_vx) * math.cos(veh.model.rf_alpha[i]) * mu_max * veh.model.rf_fz[i]
        rf_latf = math.sin(veh.model.rf_alpha[i]) * mu_max * veh.model.rf_fz[i]
    elif math.sqrt(rf_app ** 2 + rf_latf ** 2) <= mu_max * veh.model.rf_fz[i]:
        veh.model.rf_lock[i] = 0
        rf_lonf = rf_app
        rf_latf = rf_latf

    # ------------------------ Right Rear Tire ----------------------------------- #
    # local velocity
    rr_vx = veh.model.vx[j] - veh.model.oz_rad[j] * (veh.track / 2)
    rr_vy = veh.model.vy[j] - veh.model.oz_rad[j] * veh.lcgr

    veh.model.rr_lock[i] = 0  # locked status - initially set to unlocked
    veh.model.rr_alpha[i] = -1 * np.arctan2(rr_vy, rr_vx)  # tire slip angle (rad)

    if math.fabs(veh.model.rr_alpha[i]) > alpha_max:  # following Steffan 1996 SAE No. 960886
        rr_latf = sign(veh.model.rr_alpha[i]) * mu_max * veh.model.rr_fz[i]  # lateral force if alpha is greater than maximum slip angle - input
    else:
        rr_latf = (veh.model.rr_alpha[i] / alpha_max) * mu_max * veh.model.rr_fz[i]  # lateral force for slip angle less than maximum allowed - input

    # longitudinal Force Applied = f(Vehicle drive tires)
    if veh.fwd == 1:
        rr_app = -1 * veh.model.rr_fz[i] * (mu_max * veh.driver_input.brake[i] * sign(rr_vx))  # front wheel drive, rear wheel will not apply accelerative force
    elif veh.rwd == 1:
        rr_app = veh.model.rr_fz[i] * (mu_max * (veh.driver_input.throttle[i] - veh.driver_input.brake[i] * sign(rr_vx)))  # longitudinal force applied throttle and braking are expressed as % of total friction, will not occur at same time, so add for efficiency   (cons['mu_max'] * (veh.driver_input.throttle[i] - veh.driver_input.brake[i]) / 2)
    elif veh.awd == 1:
        rr_app = veh.model.rr_fz[i] * (mu_max * (veh.driver_input.throttle[i] - veh.driver_input.brake[i] * sign(rr_vx)))

    if math.sqrt(rr_app ** 2 + rr_latf ** 2) > mu_max * veh.model.rr_fz[i]:
        veh.model.rr_lock[i] = 1
        rr_lonf = -1 * sign(rr_vx) * math.cos(veh.model.rr_alpha[i]) * mu_max * veh.model.rr_fz[i]
        rr_latf = math.sin(veh.model.rr_alpha[i]) * mu_max * veh.model.rr_fz[i]
    elif math.sqrt(rr_app ** 2 + rr_latf ** 2) <= mu_max * veh.model.rr_fz[i]:
        veh.model.rr_lock[i] = 0
        rr_lonf = rr_app
        rr_latf = rr_latf

    # ------------------------ Left Rear Tire ------------------------------------ #
    lr_vx = veh.model.vx[j] + veh.model.oz_rad[j] * (veh.track / 2)
    lr_vy = veh.model.vy[j] - veh.model.oz_rad[j] * veh.lcgr
    veh.model.lr_lock[i] = 0  # locked status - initially set to unlocked
    veh.model.lr_alpha[i] = -1 * np.arctan2(lr_vy, lr_vx)  # tire slip angle (rad)

    if math.fabs(veh.model.lr_alpha[i]) > alpha_max:  # following Steffan 1996 SAE No. 960886
        lr_latf = sign(veh.model.lr_alpha[i]) * mu_max * veh.model.lr_fz[i]  # lateral force if alpha is greater than maximum slip angle - input
    else:
        lr_latf = (veh.model.lr_alpha[i] / alpha_max) * mu_max * veh.model.lr_fz[i]  # lateral force for slip angle less than maximum allowed - input

    if veh.fwd == 1:
        lr_app = -1 * veh.model.lr_fz[i] * (mu_max * veh.driver_input.brake[i] * sign(lr_vx))  # front wheel drive, rear wheel will not apply accelerative force
    elif veh.rwd == 1:
        lr_app = veh.model.lr_fz[i] * (mu_max * (veh.driver_input.throttle[i] - veh.driver_input.brake[i] * sign(lr_vx)))  # longitudinal force applied throttle and braking are expressed as % of total friction, will not occur at same time, so add for efficiency   (cons['mu_max'] * (veh.driver_input.throttle[i] - veh.driver_input.brake[i]) / 2)
    elif veh.awd == 1:
        lr_app = veh.model.lr_fz[i] * (mu_max * (veh.driver_input.throttle[i] - veh.driver_input.brake[i] * sign(lr_vx)))

    if math.sqrt(lr_app ** 2 + lr_latf ** 2) > mu_max * veh.model.lr_fz[i]:
        veh.model.lr_lock[i] = 1
        lr_lonf = -1 * sign(lr_vx) * math.cos(veh.model.lr_alpha[i]) * mu_max * veh.model.lr_fz[i]
        lr_latf = math.sin(veh.model.lr_alpha[i]) * mu_max * veh.model.lr_fz[i]
    elif math.sqrt(lr_app ** 2 + lr_latf ** 2) <= mu_max * veh.model.lr_fz[i]:
        veh.model.lr_lock[i] = 0
        lr_lonf = lr_app
        lr_latf = lr_latf

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

    veh.model.lf_lock[i] = veh.model.lf_lock[i].astype(int)
    veh.model.rf_lock[i] = veh.model.rf_lock[i].astype(int)
    veh.model.rr_lock[i] = veh.model.rr_lock[i].astype(int)
    veh.model.lr_lock[i] = veh.model.lr_lock[i].astype(int)

    return veh
