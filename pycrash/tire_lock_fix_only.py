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
            if veh.fwd == 1 or veh.awd == 1:  # '|' binds tighter than '==', which ignored awd
                drive = 1
            tire_values = [1, drive, 0, 0]
        elif tire_name in ['rr', 'lr']:
            if veh.rwd == 1 or veh.awd == 1:
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
    # lateral shift: total side-to-side transfer is m * av * hcg / track, split equally between
    # the front and rear axles (no roll stiffness distribution yet), so 0.5 of it at each tire
    veh_m = veh.weight / 32.2
    lat_shift = 0.5 * veh_m * veh.model.av[j] * veh.hcg / veh.track
    veh.model.lf_fz[i] = 0.5 * ((-veh_m * veh.model.au[j] * veh.hcg + veh.weight * veh.lcgr) / veh.wb) + lat_shift
    veh.model.rf_fz[i] = 0.5 * ((-veh_m * veh.model.au[j] * veh.hcg + veh.weight * veh.lcgr) / veh.wb) - lat_shift
    veh.model.rr_fz[i] = 0.5 * ((veh_m * veh.model.au[j] * veh.hcg + veh.weight * veh.lcgf) / veh.wb) - lat_shift
    veh.model.lr_fz[i] = 0.5 * ((veh_m * veh.model.au[j] * veh.hcg + veh.weight * veh.lcgf) / veh.wb) + lat_shift

    return veh

def tire_force(vx, vy, fz, steer_angle, brake, throttle, alpha_max=0.174533, mu_max=0.8, v_low=2.0):
    """
    vx, vy - local velocity at tire in the vehicle frame (x forward, y right) (ft/s)
    fz - vertical load on tire (lb)
    steer_angle - steer angle at tire (rad)
    brake - braking as a fraction (0 - 1) of available friction
    throttle - throttle as a fraction (0 - 1) of available friction
    v_low - below this speed (ft/s) the brake force and slip angle are ramped to zero so the
            tire does not chatter back and forth across v = 0 when the vehicle stops
    returns longitudinal and lateral force in the tire frame, lock status, slip angle (rad)
    """
    if fz <= 0:  # wheel has lifted off, no force available
        return 0.0, 0.0, 0, 0.0

    # velocity in the tire frame - the steered tire is rotated steer_angle from the vehicle x axis
    v_lon = vx * np.cos(steer_angle) + vy * np.sin(steer_angle)
    v_lat = -vx * np.sin(steer_angle) + vy * np.cos(steer_angle)

    # slip angle - angle between the tire heading and its direction of travel
    # arctan2(vy, vx) returns +/-180 deg when the tire rolls backward (vehicle stopping, spinning,
    # reversing), which saturated the lateral force and flagged the tire as locked; using |v_lon|
    # keeps alpha within +/-90 deg so forward and backward rolling are handled the same way
    alpha = -np.arctan2(v_lat, max(abs(v_lon), v_low))

    # direction of travel along the tire (+1 forward, -1 backward), ramped linearly through zero
    dir_lon = np.clip(v_lon / v_low, -1, 1)

    # following Steffan 1996 SAE No. 960886
    # lateral force
    if np.abs(alpha) > alpha_max:
        lat_force = sign(alpha) * mu_max * fz  # lateral force if alpha is greater than maximum slip angle - input
    else:
        lat_force = (alpha / alpha_max) * mu_max * fz  # lateral force for slip angle less than maximum allowed - input
    # longitudinal force applied (attempted) - braking opposes the direction of travel
    long_app = fz * (mu_max * (throttle - brake * dir_lon))
    # Equation 3 - is the force applied greater than available from friction at tire?
    if np.sqrt(long_app ** 2 + lat_force ** 2) > (mu_max * fz):
        # tire is sliding - friction acts opposite the sliding velocity
        # cos(alpha) > 0 for all alpha within +/-90 deg, so direction comes from dir_lon only
        lock_status = 1
        long_force = -dir_lon * np.cos(alpha) * mu_max * fz
        lat_force = np.sin(alpha) * mu_max * fz
    else:
        lock_status = 0
        long_force = long_app

    return long_force, lat_force, int(lock_status), alpha
