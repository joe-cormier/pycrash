import pandas as pd
import numpy as np

# columns for vehicle motion DataFrame
column_list = ['b_lfc', 'b_rfc', 'b_rrc', 'b_lrc', 'lfw', 'lfw_a', 'lfw_b',
               'lfw_c', 'lfw_d', 'rfw', 'rfw_a', 'rfw_b', 'rfw_c', 'rfw_d',
                'rrw', 'rrw_a',	'rrw_b', 'rrw_c', 'rrw_d', 'lrw',  'lrw_a',
                'lrw_b', 'lrw_c', 'lrw_d', 'cg', 'xaxis', 'yaxis', 'vel_v']

def position_data_motion(veh):
    """
    set striking to True to return location of impact point in vehicle 1
    """
    # initialize empty dataframe
    veh.p_vx = pd.DataFrame(columns = column_list)                                      # time variant vehicle geometry for plotting in vehicle frame
    veh.p_vy = pd.DataFrame(columns = column_list)                                      # time variant vehicle geometry for plotting in vehicle frame

    # loop for creating seperate dataframes for X and Y components of vehicle drawing in vehicle frame
    for i in (range(len(veh.model.t))):
        """
        vehicle frame coordinates for body geometry, tire positions and velocity vector
        if MV = True - impact point and edge points will be tansformed here as well
        """

        veh.p_vx = veh.p_vx.append({'b_lfc': veh.lcgf + veh.f_hang,     # body outline
                                  'b_rfc': veh.lcgf + veh.f_hang,
                                  'b_rrc': -1 * (veh.lcgr + veh.r_hang),
                                  'b_lrc': -1 * (veh.lcgr + veh.r_hang),
                                  'lfw':   veh.lcgf,                         # left front wheel
                                  'lfw_a': veh.lcgf + veh.tire_d / 2 * np.cos(veh.model.loc[i,'delta_rad']) - -1 * veh.tire_w / 2 * np.sin(veh.model.loc[i,'delta_rad']),
                                  'lfw_b': veh.lcgf + veh.tire_d / 2 * np.cos(veh.model.loc[i,'delta_rad']) - veh.tire_w / 2 * np.sin(veh.model.loc[i,'delta_rad']),
                                  'lfw_c': veh.lcgf + -1 * veh.tire_d / 2 * np.cos(veh.model.loc[i,'delta_rad']) - veh.tire_w / 2 * np.sin(veh.model.loc[i,'delta_rad']),
                                  'lfw_d': veh.lcgf + -1 * veh.tire_d / 2 * np.cos(veh.model.loc[i,'delta_rad']) - -1 * veh.tire_w / 2*np.sin(veh.model.loc[i,'delta_rad']),
                                  'rfw':   veh.lcgf,                         # Right front wheel
                                  'rfw_a': veh.lcgf + veh.tire_d / 2 * np.cos(veh.model.loc[i,'delta_rad']) - -1 * veh.tire_w / 2 * np.sin(veh.model.loc[i,'delta_rad']),
                                  'rfw_b': veh.lcgf + veh.tire_d / 2 * np.cos(veh.model.loc[i,'delta_rad']) - veh.tire_w / 2 * np.sin(veh.model.loc[i,'delta_rad']),
                                  'rfw_c': veh.lcgf + -1 * veh.tire_d / 2 * np.cos(veh.model.loc[i,'delta_rad']) - veh.tire_w / 2 * np.sin(veh.model.loc[i,'delta_rad']),
                                  'rfw_d': veh.lcgf + -1 * veh.tire_d / 2*np.cos(veh.model.loc[i,'delta_rad']) - -1 * veh.tire_w / 2 * np.sin(veh.model.loc[i,'delta_rad']),
                                  'rrw':   -1 * veh.lcgr,                          # Right rear wheel
                                  'rrw_a': -1 * veh.lcgr + veh.tire_d / 2,
                                  'rrw_b': -1 * veh.lcgr + veh.tire_d / 2,
                                  'rrw_c': -1 * veh.lcgr - veh.tire_d / 2,
                                  'rrw_d': -1 * veh.lcgr - veh.tire_d / 2,
                                  'lrw':   -1 * veh.lcgr,                          # Left rear wheel
                                  'lrw_a': -1 * veh.lcgr + veh.tire_d / 2,
                                  'lrw_b': -1 * veh.lcgr + veh.tire_d / 2,
                                  'lrw_c': -1 * veh.lcgr - veh.tire_d / 2,
                                  'lrw_d': -1 * veh.lcgr - veh.tire_d / 2,
                                  'cg': 0,                                         # CG
                                  'xaxis': veh.lcgf + veh.f_hang + 1.5,            # line for x-axis
                                  'yaxis': 0,                                      # line for y-axis
                                  'vel_v': veh.model.vx[i]}, ignore_index=True)    # line for velocity vector

        veh.p_vy = veh.p_vy.append({'b_lfc': -1 * veh.width / 2,     # body outline
                                  'b_rfc': veh.width / 2,
                                  'b_rrc': veh.width / 2,
                                  'b_lrc': -1 * veh.width / 2,
                                  'lfw':   -1 * (veh.width / 2 - veh.tire_w / 2),                         # left front wheel
                                  'lfw_a': -1 * (veh.width / 2 - veh.tire_w / 2) + veh.tire_d / 2 * np.sin(veh.model.loc[i,'delta_rad']) + -1 * veh.tire_w / 2 * np.cos(veh.model.loc[i,'delta_rad']),
                                  'lfw_b': -1 * (veh.width / 2 - veh.tire_w / 2) + veh.tire_d / 2 *np.sin(veh.model.loc[i,'delta_rad']) + veh.tire_w / 2 * np.cos(veh.model.loc[i,'delta_rad']),
                                  'lfw_c': -1 * (veh.width / 2 - veh.tire_w / 2) + -1 * veh.tire_d / 2 * np.sin(veh.model.loc[i,'delta_rad']) + veh.tire_w / 2 * np.cos(veh.model.loc[i,'delta_rad']),
                                  'lfw_d': -1 * (veh.width / 2 - veh.tire_w / 2) + -1 * veh.tire_d / 2 * np.sin(veh.model.loc[i,'delta_rad']) + -1 * veh.tire_w / 2 * np.cos(veh.model.loc[i,'delta_rad']),
                                  'rfw':   (veh.width / 2 - veh.tire_w / 2),                         # Right front wheel
                                  'rfw_a': (veh.width / 2 - veh.tire_w / 2) + veh.tire_d / 2 * np.sin(veh.model.loc[i,'delta_rad']) + -1 * veh.tire_w / 2 * np.cos(veh.model.loc[i,'delta_rad']),
                                  'rfw_b': (veh.width / 2 - veh.tire_w / 2) + veh.tire_d / 2 * np.sin(veh.model.loc[i,'delta_rad']) + veh.tire_w / 2 * np.cos(veh.model.loc[i,'delta_rad']),
                                  'rfw_c': (veh.width / 2 - veh.tire_w / 2) + -1*veh.tire_d / 2 * np.sin(veh.model.loc[i,'delta_rad']) + veh.tire_w / 2 * np.cos(veh.model.loc[i,'delta_rad']),
                                  'rfw_d': (veh.width / 2 - veh.tire_w / 2) + -1*veh.tire_d / 2 * np.sin(veh.model.loc[i,'delta_rad']) + -1 * veh.tire_w / 2 * np.cos(veh.model.loc[i,'delta_rad']),
                                  'rrw':   (veh.width / 2 - veh.tire_w / 2),                          # Right rear wheel
                                  'rrw_a': veh.width / 2 - veh.tire_w,
                                  'rrw_b': veh.width / 2,
                                  'rrw_c': veh.width / 2,
                                  'rrw_d': veh.width / 2 - veh.tire_w,
                                  'lrw':   -1 * (veh.width / 2 - veh.tire_w / 2),                          # Left rear wheel
                                  'lrw_a': -1 * veh.width / 2,
                                  'lrw_b': -1 * veh.width / 2 + veh.tire_w,
                                  'lrw_c': -1 * veh.width / 2 + veh.tire_w,
                                  'lrw_d': -1 * veh.width / 2,
                                  'cg':    0,                                         # CG
                                  'xaxis': 0,                                         # line for x-axis
                                  'yaxis': veh.width / 2 + 1.5,                     # line for y-axis
                                  'vel_v': veh.model.vy[i]}, ignore_index=True)       # line for velocity vector

    cgx = veh.model[['Dx']].copy()                          # CG location in inertial frame
    cgy = veh.model[['Dy']].copy()



    if veh.striking:  # impact point (veh1 - striking vehicle)
        # add impact point locations in vehicle frame
        i=0
        for impPoint in veh.impact_points:
            veh.p_vx[f'POI_{i}'] = impPoint[0]
            veh.p_vy[f'POI_{i}'] = impPoint[1]

            norm_length = veh.width
            tang_length = veh.width / 2

            veh.p_vx[f'impact_{i}_norm'] = impPoint[0] + norm_length * np.cos(impPoint[2] * np.pi / 180)
            veh.p_vy[f'impact_{i}_norm'] = impPoint[1] + norm_length * np.sin(impPoint[2] * np.pi / 180)

            veh.p_vx[f'impact_{i}_tang'] = impPoint[0] + tang_length * np.cos(impPoint[2] * np.pi / 180 + np.pi / 2)
            veh.p_vy[f'impact_{i}_tang'] = impPoint[1] + tang_length * np.sin(impPoint[2] * np.pi / 180 + np.pi / 2)

            i+=1

    veh.p_gx = veh.p_vx.copy()                              # time variant vehicle geometry for plotting motion in inertial frame
    veh.p_gy = veh.p_vy.copy()                              # time variant vehicle geometry for plotting motion in inertial frame

    for i in range(0, len(veh.p_gx)):
           for j in range(0, len(veh.p_vx.columns)):
              # coordinate transformation - rotating vehicle frame to draw vehicle
              veh.p_gx.iloc[i, j] = cgx.Dx[i] + veh.p_vx.iloc[i, j] * np.cos(veh.model.loc[i, 'theta_rad']) - veh.p_vy.iloc[i, j] * np.sin(veh.model.loc[i, 'theta_rad'])
              veh.p_gy.iloc[i, j] = cgy.Dy[i] + veh.p_vx.iloc[i, j] * np.sin(veh.model.loc[i, 'theta_rad']) + veh.p_vy.iloc[i, j] * np.cos(veh.model.loc[i, 'theta_rad'])

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

        veh.px = {'b_lfc': veh.lcgf + veh.f_hang,     # body outline
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
                  'rrw':   -1 * veh.lcgr,                          # Right rear wheel
                  'rrw_a': -1 * veh.lcgr + veh.tire_d / 2,
                  'rrw_b': -1 * veh.lcgr + veh.tire_d / 2,
                  'rrw_c': -1 * veh.lcgr - veh.tire_d / 2,
                  'rrw_d': -1 * veh.lcgr - veh.tire_d / 2,
                  'lrw':   -1 * veh.lcgr,                          # Left rear wheel
                  'lrw_a': -1 * veh.lcgr + veh.tire_d / 2,
                  'lrw_b': -1 * veh.lcgr + veh.tire_d / 2,
                  'lrw_c': -1 * veh.lcgr - veh.tire_d / 2,
                  'lrw_d': -1 * veh.lcgr - veh.tire_d / 2,
                  'cg': 0,                                         # CG
                  'xaxis': veh.lcgf + veh.f_hang + 1.5,           # line for x-axis
                  'yaxis': 0,                                      # line for y-axis
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

                veh.impact_norm_global.append((pimpact_X + norm_length * np.cos(impPoints[2] * np.pi / 180),
                                              pimpact_Y + norm_length * np.sin(impPoints[2] * np.pi / 180)))

                veh.impact_tang_global.append((pimpact_X + tang_length * np.cos(impPoints[2] * np.pi / 180 + np.pi / 2),
                                              pimpact_Y + tang_length * np.sin(impPoints[2] * np.pi / 180 + np.pi / 2)))


    return vehicle_list
