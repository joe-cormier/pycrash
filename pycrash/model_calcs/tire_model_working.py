z


class tire


def tire_forces():

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
        lf_lonf = sign(lf_vx) * math.cos(veh.model.lf_alpha[i]) * mu_max * veh.model.lf_fz[i]  # force will be applied in the direction opposite of vehicle motion
        lf_latf = math.sin(veh.model.lf_alpha[i]) * mu_max * veh.model.lf_fz[i]
    elif math.sqrt(lf_app ** 2 + lf_latf ** 2) <= mu_max * veh.model.lf_fz[i]:
        veh.model.lf_lock[i] = 0
        lf_lonf = lf_app
        lf_latf = lf_latf

