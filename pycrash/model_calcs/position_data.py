import pandas as pd
import numpy as np

# columns for vehicle motion DataFrame ([fast/pandas3] no longer used by position_data_motion, kept for reference)
column_list = ['b_lfc', 'b_rfc', 'b_rrc', 'b_lrc', 'lfw', 'lfw_a', 'lfw_b',
               'lfw_c', 'lfw_d', 'rfw', 'rfw_a', 'rfw_b', 'rfw_c', 'rfw_d',
               'rrw', 'rrw_a',  'rrw_b', 'rrw_c', 'rrw_d', 'lrw',  'lrw_a',
               'lrw_b', 'lrw_c', 'lrw_d', 'cg', 'xaxis', 'yaxis', 'vel_v']

def position_data_motion(veh):
    """
    set striking to True to return location of impact point in vehicle 1
    [fast/pandas3] rewritten with whole-column numpy math - same tables as before (p_vx, p_vy, p_gx, p_gy)
    the previous version grew the tables one row at a time with pd.concat and then filled p_gx / p_gy
    cell by cell, which was about half of an Impact simulation's run time
    """
    m = veh.model
    n = len(m)
    ones = np.ones(n)
    d = m['delta_rad'].to_numpy(dtype=float)    # steer angle at each time step
    cd, sd = np.cos(d), np.sin(d)
    hd, hw = veh.tire_d / 2, veh.tire_w / 2
    lfy = -1 * (veh.width / 2 - veh.tire_w / 2)  # front wheel centres, lateral
    rfy = veh.width / 2 - veh.tire_w / 2

    # vehicle frame coordinates for body geometry, tire positions and velocity vector - x components
    p_vx = {'b_lfc': (veh.lcgf + veh.f_hang) * ones,  # body outline
            'b_rfc': (veh.lcgf + veh.f_hang) * ones,
            'b_rrc': -1 * (veh.lcgr + veh.r_hang) * ones,
            'b_lrc': -1 * (veh.lcgr + veh.r_hang) * ones,
            'lfw': veh.lcgf * ones,  # left front wheel
            'lfw_a': veh.lcgf + hd * cd - -1 * hw * sd,
            'lfw_b': veh.lcgf + hd * cd - hw * sd,
            'lfw_c': veh.lcgf + -1 * hd * cd - hw * sd,
            'lfw_d': veh.lcgf + -1 * hd * cd - -1 * hw * sd,
            'rfw': veh.lcgf * ones,  # Right front wheel
            'rfw_a': veh.lcgf + hd * cd - -1 * hw * sd,
            'rfw_b': veh.lcgf + hd * cd - hw * sd,
            'rfw_c': veh.lcgf + -1 * hd * cd - hw * sd,
            'rfw_d': veh.lcgf + -1 * hd * cd - -1 * hw * sd,
            'rrw': -1 * veh.lcgr * ones,  # Right rear wheel
            'rrw_a': (-1 * veh.lcgr + hd) * ones,
            'rrw_b': (-1 * veh.lcgr + hd) * ones,
            'rrw_c': (-1 * veh.lcgr - hd) * ones,
            'rrw_d': (-1 * veh.lcgr - hd) * ones,
            'lrw': -1 * veh.lcgr * ones,  # Left rear wheel
            'lrw_a': (-1 * veh.lcgr + hd) * ones,
            'lrw_b': (-1 * veh.lcgr + hd) * ones,
            'lrw_c': (-1 * veh.lcgr - hd) * ones,
            'lrw_d': (-1 * veh.lcgr - hd) * ones,
            'cg': 0 * ones,  # CG
            'xaxis': (veh.lcgf + veh.f_hang + 1.5) * ones,  # line for x-axis
            'yaxis': 0 * ones,  # line for y-axis
            'vel_v': m['vx'].to_numpy(dtype=float)}

    # y components
    p_vy = {'b_lfc': -1 * veh.width / 2 * ones,  # body outline
            'b_rfc': veh.width / 2 * ones,
            'b_rrc': veh.width / 2 * ones,
            'b_lrc': -1 * veh.width / 2 * ones,
            'lfw': lfy * ones,  # left front wheel
            'lfw_a': lfy + hd * sd + -1 * hw * cd,
            'lfw_b': lfy + hd * sd + hw * cd,
            'lfw_c': lfy + -1 * hd * sd + hw * cd,
            'lfw_d': lfy + -1 * hd * sd + -1 * hw * cd,
            'rfw': rfy * ones,  # Right front wheel
            'rfw_a': rfy + hd * sd + -1 * hw * cd,
            'rfw_b': rfy + hd * sd + hw * cd,
            'rfw_c': rfy + -1 * hd * sd + hw * cd,
            'rfw_d': rfy + -1 * hd * sd + -1 * hw * cd,
            'rrw': rfy * ones,  # Right rear wheel
            'rrw_a': (veh.width / 2 - veh.tire_w) * ones,
            'rrw_b': veh.width / 2 * ones,
            'rrw_c': veh.width / 2 * ones,
            'rrw_d': (veh.width / 2 - veh.tire_w) * ones,
            'lrw': lfy * ones,  # Left rear wheel
            'lrw_a': -1 * veh.width / 2 * ones,
            'lrw_b': (-1 * veh.width / 2 + veh.tire_w) * ones,
            'lrw_c': (-1 * veh.width / 2 + veh.tire_w) * ones,
            'lrw_d': -1 * veh.width / 2 * ones,
            'cg': 0 * ones,  # CG
            'xaxis': 0 * ones,  # line for x-axis
            'yaxis': (veh.width / 2 + 1.5) * ones,  # line for y-axis
            'vel_v': m['vy'].to_numpy(dtype=float)}  # line for velocity vector

    if veh.striking:  # impact point (veh1 - striking vehicle)
        # add impact point locations in vehicle frame
        norm_length = veh.width
        tang_length = veh.width / 2
        for i, impPoint in enumerate(veh.impact_points):
            p_vx[f'POI_{i}'] = impPoint[0] * ones
            p_vy[f'POI_{i}'] = impPoint[1] * ones
            p_vx[f'impact_{i}_norm'] = (impPoint[0] + norm_length * np.cos(impPoint[2] * np.pi / 180)) * ones
            p_vy[f'impact_{i}_norm'] = (impPoint[1] + norm_length * np.sin(impPoint[2] * np.pi / 180)) * ones
            p_vx[f'impact_{i}_tang'] = (impPoint[0] + tang_length * np.cos(impPoint[2] * np.pi / 180 + np.pi / 2)) * ones
            p_vy[f'impact_{i}_tang'] = (impPoint[1] + tang_length * np.sin(impPoint[2] * np.pi / 180 + np.pi / 2)) * ones

    veh.p_vx = pd.DataFrame(p_vx)    # time variant vehicle geometry for plotting in vehicle frame
    veh.p_vy = pd.DataFrame(p_vy)

    # coordinate transformation - rotating vehicle frame to draw vehicle in the inertial frame
    theta = m['theta_rad'].to_numpy(dtype=float)[:, None]
    cgx = m['Dx'].to_numpy(dtype=float)[:, None]     # CG location in inertial frame
    cgy = m['Dy'].to_numpy(dtype=float)[:, None]
    vx, vy = veh.p_vx.to_numpy(), veh.p_vy.to_numpy()
    veh.p_gx = pd.DataFrame(cgx + vx * np.cos(theta) - vy * np.sin(theta), columns=veh.p_vx.columns)
    veh.p_gy = pd.DataFrame(cgy + vx * np.sin(theta) + vy * np.cos(theta), columns=veh.p_vy.columns)

    # copy locked info from vehicle model
    veh.p_gx['lf_lock'] = veh.model.lf_lock.copy()
    veh.p_gx['rf_lock'] = veh.model.rf_lock.copy()
    veh.p_gx['rr_lock'] = veh.model.rr_lock.copy()
    veh.p_gx['lr_lock'] = veh.model.lr_lock.copy()

    return veh




def position_data_static(vehicle_list):
    """
    static data for plotting vehicle location in global frame
    """

    for veh in vehicle_list:
        if veh.isTrailer:
            veh.px = {'b_lfc': veh.lcgf + veh.f_hang,  # body outline
                      'b_rfc': veh.lcgf + veh.f_hang,
                      'b_rrc': -1 * (veh.lcgr + veh.r_hang),
                      'b_lrc': -1 * (veh.lcgr + veh.r_hang),
                      'rrw': -1 * veh.lcgr,  # Right rear wheel
                      'rrw_a': -1 * veh.lcgr + veh.tire_d / 2,
                      'rrw_b': -1 * veh.lcgr + veh.tire_d / 2,
                      'rrw_c': -1 * veh.lcgr - veh.tire_d / 2,
                      'rrw_d': -1 * veh.lcgr - veh.tire_d / 2,
                      'lrw': -1 * veh.lcgr,  # Left rear wheel
                      'lrw_a': -1 * veh.lcgr + veh.tire_d / 2,
                      'lrw_b': -1 * veh.lcgr + veh.tire_d / 2,
                      'lrw_c': -1 * veh.lcgr - veh.tire_d / 2,
                      'lrw_d': -1 * veh.lcgr - veh.tire_d / 2,
                      'cg': 0,  # CG
                      'xaxis': veh.lcgf + veh.f_hang + 1.5,  # line for x-axis
                      'yaxis': 0,  # line for y-axis
                      'vel_v': veh.vx_initial}

            veh.py = {'b_lfc': -1 * veh.width / 2,  # body outline
                      'b_rfc': veh.width / 2,
                      'b_rrc': veh.width / 2,
                      'b_lrc': -1 * veh.width / 2,
                      'rrw': (veh.width / 2 - veh.tire_w / 2),  # Right rear wheel
                      'rrw_a': veh.width / 2 - veh.tire_w,
                      'rrw_b': veh.width / 2,
                      'rrw_c': veh.width / 2,
                      'rrw_d': veh.width / 2 - veh.tire_w,
                      'lrw': -1 * (veh.width / 2 - veh.tire_w / 2),  # Left rear wheel
                      'lrw_a': -1 * veh.width / 2,
                      'lrw_b': -1 * veh.width / 2 + veh.tire_w,
                      'lrw_c': -1 * veh.width / 2 + veh.tire_w,
                      'lrw_d': -1 * veh.width / 2,
                      'cg': 0,  # CG
                      'xaxis': 0,  # line for x-axis
                      'yaxis': veh.width / 2 + 1.5,  # line for y-axis
                      'vel_v': veh.vy_initial}
        else:
            veh.px = {'b_lfc': veh.lcgf + veh.f_hang,           # body outline
                      'b_rfc': veh.lcgf + veh.f_hang,
                      'b_rrc': -1 * (veh.lcgr + veh.r_hang),
                      'b_lrc': -1 * (veh.lcgr + veh.r_hang),
                      'lfw':   veh.lcgf,                         # left front wheel
                      'lfw_a': veh.lcgf + veh.tire_d / 2,
                      'lfw_b': veh.lcgf + veh.tire_d / 2,
                      'lfw_c': veh.lcgf + -1 * veh.tire_d / 2,
                      'lfw_d': veh.lcgf + -1 * veh.tire_d / 2,
                      'rfw':   veh.lcgf,                         # Right front wheel
                      'rfw_a': veh.lcgf + veh.tire_d / 2,
                      'rfw_b': veh.lcgf + veh.tire_d / 2,
                      'rfw_c': veh.lcgf + -1 * veh.tire_d / 2,
                      'rfw_d': veh.lcgf + -1 * veh.tire_d / 2,
                      'rrw':   -1 * veh.lcgr,                     # Right rear wheel
                      'rrw_a': -1 * veh.lcgr + veh.tire_d / 2,
                      'rrw_b': -1 * veh.lcgr + veh.tire_d / 2,
                      'rrw_c': -1 * veh.lcgr - veh.tire_d / 2,
                      'rrw_d': -1 * veh.lcgr - veh.tire_d / 2,
                      'lrw':   -1 * veh.lcgr,                      # Left rear wheel
                      'lrw_a': -1 * veh.lcgr + veh.tire_d / 2,
                      'lrw_b': -1 * veh.lcgr + veh.tire_d / 2,
                      'lrw_c': -1 * veh.lcgr - veh.tire_d / 2,
                      'lrw_d': -1 * veh.lcgr - veh.tire_d / 2,
                      'cg': 0,                                      # CG
                      'xaxis': veh.lcgf + veh.f_hang + 1.5,         # line for x-axis
                      'yaxis': 0,                                   # line for y-axis
                      'vel_v': veh.vx_initial}

            veh.py = {'b_lfc': -1 * veh.width / 2,     # body outline
                      'b_rfc': veh.width / 2,
                      'b_rrc': veh.width / 2,
                      'b_lrc': -1 * veh.width / 2,
                      'lfw':   -1 * (veh.width / 2 - veh.tire_w / 2),                         # left front wheel
                      'lfw_a': -1 * (veh.width / 2),
                      'lfw_b': -1 * (veh.width / 2 - veh.tire_w),
                      'lfw_c': -1 * (veh.width / 2 - veh.tire_w),
                      'lfw_d': -1 * (veh.width / 2),
                      'rfw':   (veh.width / 2 - veh.tire_w / 2),                         # Right front wheel
                      'rfw_a': (veh.width / 2 - veh.tire_w),
                      'rfw_b': (veh.width / 2),
                      'rfw_c': (veh.width / 2),
                      'rfw_d': (veh.width / 2 - veh.tire_w),
                      'rrw':   (veh.width / 2 - veh.tire_w / 2),                          # Right rear wheel
                      'rrw_a': veh.width / 2 - veh.tire_w,
                      'rrw_b': veh.width / 2,
                      'rrw_c': veh.width / 2,
                      'rrw_d': veh.width / 2 - veh.tire_w,
                      'lrw': -1 * (veh.width / 2 - veh.tire_w / 2),                          # Left rear wheel
                      'lrw_a': -1 * veh.width / 2,
                      'lrw_b': -1 * veh.width / 2 + veh.tire_w,
                      'lrw_c': -1 * veh.width / 2 + veh.tire_w,
                      'lrw_d': -1 * veh.width / 2,
                      'cg': 0,                                         # CG
                      'xaxis': 0,   # line for x-axis
                      'yaxis': veh.width / 2 + 1.5,                                      # line for y-axis
                      'vel_v': veh.vy_initial}

        veh.Px = veh.px.copy()
        veh.Py = veh.py.copy()

        # rotate vehicle coordinates using initial heading angle (head_angle)
        for key in veh.Px:
            veh.Px[key] = veh.init_x_pos + veh.px[key]*np.cos(veh.head_angle * np.pi / 180) - veh.py[key]*np.sin(veh.head_angle * np.pi / 180)
            veh.Py[key] = veh.init_y_pos + veh.px[key]*np.sin(veh.head_angle * np.pi / 180) + veh.py[key]*np.cos(veh.head_angle * np.pi / 180)

        if veh.striking:
            # impact point (veh1 - striking vehicle)
            veh.impact_points_global = []
            veh.impact_norm_global = []
            veh.impact_tang_global = []

            for impPoints in veh.impact_points:
                """ create list of impact points in the global reference frame """
                pimpact_X = veh.init_x_pos + impPoints[0] * np.cos(veh.head_angle * np.pi / 180) - impPoints[1] * np.sin(veh.head_angle * np.pi / 180)
                pimpact_Y = veh.init_y_pos + impPoints[0] * np.sin(veh.head_angle * np.pi / 180) + impPoints[1] * np.cos(veh.head_angle * np.pi / 180)

                veh.impact_points_global.append((pimpact_X, pimpact_Y))

                norm_length = veh.width
                tang_length = veh.width / 2

                veh.impact_norm_global.append((pimpact_X + norm_length * np.cos((veh.head_angle + impPoints[2]) * np.pi / 180),
                                              pimpact_Y + norm_length * np.sin((veh.head_angle + impPoints[2]) * np.pi / 180)))

                veh.impact_tang_global.append((pimpact_X + tang_length * np.cos((veh.head_angle + impPoints[2]) * np.pi / 180 + np.pi / 2),
                                              pimpact_Y + tang_length * np.sin((veh.head_angle + impPoints[2]) * np.pi / 180 + np.pi / 2)))


    return vehicle_list
