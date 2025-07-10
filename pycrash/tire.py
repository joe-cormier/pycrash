import numpy as np


input_dict = {
              'rx': 0,       # tire radius in x direction
              'ry': 0,       # tire radius in y direction
              'steer': True,
              'drive': False,
              'alpha_max': 0.174533,    # max slip angle
              'percent_disabled': 0,
              'time_disabled': 0
             }

def sign(x):
    # returns the sign of a number
    if x > 0:
        return 1
    elif x < 0:
        return -1
    elif x == 0:
        return 0

def create_tires(
                 veh,
                 names,
                 ):
    """
    create instance of a tire as nested dictionaries
    define x/y radii of each tire, tire properties which will determine
    how forces are calculated
    """
    tire_keys = ['steer', 'drive', 'percent_disabled', 'time_disabled']
    tire_properties = {}
    for tire_name in names:
        tire_properties[tire_name] = {}
        drive = 0
        if tire_name in ['lf', 'rf']:
            if veh.fwd == 1 | veh.awd == 1:
                drive = 1
            tire_values = [1, drive, 0, 0]
        elif tire_name in ['rr', 'lr']:
            if veh.rwd == 1 | veh.awd == 1:
                drive = 1
            tire_values = [0, drive, 0, 0]

        tire_properties[tire_name] = dict(zip(tire_keys, tire_values))
        print(f'Tire {tire_name} properties: {tire_properties[tire_name]}')

    return tire_properties


def ackerman_steer(i, delta_rad, wb, track):
    rf_steer_angle = 0
    lf_steer_angle = 0

    if delta_rad > 0:   # positive steer
        r_net = wb / np.tan(delta_rad)  # turn radius  (Gillespie)
        rf_steer_angle = np.arctan(wb / (r_net - track))
        lf_steer_angle = delta_rad
    elif delta_rad < 0:
        r_net = wb / np.tan(delta_rad)  # turn radius  (Gillespie)
        rf_steer_angle = delta_rad
        lf_steer_angle = np.arctan(wb / (r_net + track))

    return lf_steer_angle, rf_steer_angle

def vertical_load(i, j, veh):
    # Forward / Rearward weight shift due to braking or acceleration
    veh_m = veh.weight / 32.2
    veh.model.lf_fz[i] = 0.5 * ((-veh_m * veh.model.au[j] * veh.hcg + veh.weight * veh.lcgr) / veh.wb) + veh_m * veh.model.av[j] * veh.hcg / veh.track
    veh.model.rf_fz[i] = 0.5 * ((-veh_m * veh.model.au[j] * veh.hcg + veh.weight * veh.lcgr) / veh.wb) - veh_m * veh.model.av[j] * veh.hcg / veh.track
    veh.model.rr_fz[i] = 0.5 * ((veh_m * veh.model.au[j] * veh.hcg + veh.weight * veh.lcgf) / veh.wb) - veh_m * veh.model.av[j] * veh.hcg / veh.track
    veh.model.lr_fz[i] = 0.5 * ((veh_m * veh.model.au[j] * veh.hcg + veh.weight * veh.lcgf) / veh.wb) + veh_m * veh.model.av[j] * veh.hcg / veh.track

    return veh

def tire_force(vx, vy, fz, steer_angle, brake, throttle, alpha_max=0.174533, mu_max=0.8):
    """
    vx, vy - local velocity at tire
    fz - vertical load on tire
    steer_angle - steer angle at tire
    brake - percent brake
    throttle - percent throttle
    """
    # local velocity
    #veh.model.lf_lock[i] = 0  # locked status of Left Front Wheel - initially set to unlocked
    alpha = (1.5708 - np.arctan2(vx, vy)) - steer_angle   # tire slip angle (rad)
    #alpha = -1 * np.arctan2(vy, vx) + steer_angle
    # following Steffan 1996 SAE No. 960886
    # lateral force
    if np.abs(alpha) > alpha_max:
        lat_force = sign(alpha) * mu_max * fz  # lateral force if alpha is greater than maximum slip angle - input
    else:
        lat_force = (alpha / alpha_max) * mu_max * fz  # lateral force for slip angle less than maximum allowed - input
    # longitudinal force applied (attempted)
    long_app = fz * (mu_max * (throttle - brake * sign(vx)))
    # Equation 3 - is the force applied greater than available from friction at tire?
    if np.sqrt(long_app ** 2 + lat_force ** 2) > (mu_max * fz):
        lock_status = 1
        long_force = sign(vx) * np.cos(alpha) * mu_max * fz     # force will be applied in the direction opposite of vehicle motion
        lat_force = np.sin(alpha) * mu_max * fz
    elif np.sqrt(long_app ** 2 + lat_force ** 2) <= mu_max * fz:
        lock_status = 0
        long_force = long_app
        lat_force = lat_force

    return long_force, lat_force, int(lock_status)
