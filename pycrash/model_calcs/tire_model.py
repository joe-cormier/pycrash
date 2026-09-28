"""
Tire Model - Calculates forces at each tire
accounts for pitch due to braking and roll from cornering forces

Dependencies - v, vx, vy, au, av, omega, constants
Vehicle frame - x forward, y right, positive yaw rate clockwise when viewed from above
"""

import math

from ..tire import ackerman_steer, vertical_load, tire_force

"""
TODO: detailed suspension properties
roll_rate = 6    # semi-firm 7 = semi soft, 3 = extremely firm (corvette) (degrees / g)
rc_cg = 18/12    # passenger car - roll center to cg height (h1)  (ft)
roll_h = 6/12    # roll center height
"""


def tire_forces(veh, i, sim_defaults):
    """
    calculate tire forces for the given time step
    """
    # load defaults
    mu_max = sim_defaults['mu_max']  # maximum available friction
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
    lf_steer_angle, rf_steer_angle = ackerman_steer(i, veh.model.delta_rad[i], veh.wb, veh.track)

    # Forward / Rearward and side to side weight shift
    veh = vertical_load(i, j, veh)

    # throttle only reaches driven wheels, brakes act on all wheels
    front_throttle = veh.driver_input.throttle[i] if (veh.fwd == 1 or veh.awd == 1) else 0
    rear_throttle = veh.driver_input.throttle[i] if (veh.rwd == 1 or veh.awd == 1) else 0
    brake = veh.driver_input.brake[i]

    # tire: (x from cg, y from cg (right positive), steer angle, throttle)
    tires = {'lf': (veh.lcgf, -veh.track / 2, lf_steer_angle, front_throttle),
             'rf': (veh.lcgf, veh.track / 2, rf_steer_angle, front_throttle),
             'rr': (-veh.lcgr, veh.track / 2, 0, rear_throttle),
             'lr': (-veh.lcgr, -veh.track / 2, 0, rear_throttle)}

    oz = veh.model.oz_rad[j]
    for name, (x, y, steer_angle, throttle) in tires.items():
        # local velocity at the tire - v_cg + omega x r
        tire_vx = veh.model.vx[j] - oz * y
        tire_vy = veh.model.vy[j] + oz * x
        veh.model.at[i, f'{name}_vy'] = tire_vy

        lonf, latf, lock, alpha = tire_force(tire_vx, tire_vy, veh.model.at[i, f'{name}_fz'], steer_angle,
                                             brake, throttle, alpha_max, mu_max)

        # tire frame to vehicle frame - rotate by the same steer angle used for the slip angle
        veh.model.at[i, f'{name}_fx'] = lonf * math.cos(steer_angle) - latf * math.sin(steer_angle)
        veh.model.at[i, f'{name}_fy'] = lonf * math.sin(steer_angle) + latf * math.cos(steer_angle)
        veh.model.at[i, f'{name}_alpha'] = alpha
        veh.model.at[i, f'{name}_lock'] = lock

    return veh
