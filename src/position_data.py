import pandas as pd
import math

# columns for vehicle motion DataFrame
column_list = ['b_lfc', 'b_rfc', 'b_rrc', 'b_lrc', 'lfw', 'lfw_a', 'lfw_b',
               'lfw_c', 'lfw_d', 'rfw', 'rfw_a', 'rfw_b', 'rfw_c', 'rfw_d',
                'rrw', 'rrw_a',	'rrw_b', 'rrw_c', 'rrw_d', 'lrw',  'lrw_a',
                'lrw_b', 'lrw_c', 'lrw_d', 'cg', 'xaxis', 'yaxis', 'vel_v']


def position_data_motion(veh, striking=False):
    """
    set striking to True to return location of impact point in vehicle 1
    """
    # initialize empty dataframe
    veh.p_vx = pd.DataFrame(columns = column_list)                                      # time variant vehicle geometry for plotting in vehicle frame
    veh.p_vy = pd.DataFrame(columns = column_list)                                      # time variant vehicle geometry for plotting in vehicle frame

    # loop for creating seperate dataframes for X and Y components of vehicle drawing in vehicle frame
    for i in (range(len(veh.veh_model.t))):
        """
        vehicle frame coordinates for body geometry, tire positions and velocity vector
        if MV = True - impact point and edge points will be tansformed here as well
        """

        veh.p_vx = veh.p_vx.append({'b_lfc': veh.lcgf + veh.f_hang,     # body outline
                                  'b_rfc': veh.lcgf + veh.f_hang,
                                  'b_rrc': -1 * (veh.lcgr + veh.r_hang),
                                  'b_lrc': -1 * (veh.lcgr + veh.r_hang),
                                  'lfw':   veh.lcgf,                         # left front wheel
                                  'lfw_a': veh.lcgf + veh.tire_d / 2 * math.cos(veh.veh_model.loc[i,'delta_rad']) - -1 * veh.tire_w / 2 * math.sin(veh.veh_model.loc[i,'delta_rad']),
                                  'lfw_b': veh.lcgf + veh.tire_d / 2 * math.cos(veh.veh_model.loc[i,'delta_rad']) - veh.tire_w / 2 * math.sin(veh.veh_model.loc[i,'delta_rad']),
                                  'lfw_c': veh.lcgf + -1 * veh.tire_d / 2 * math.cos(veh.veh_model.loc[i,'delta_rad']) - veh.tire_w / 2 * math.sin(veh.veh_model.loc[i,'delta_rad']),
                                  'lfw_d': veh.lcgf + -1 * veh.tire_d / 2 * math.cos(veh.veh_model.loc[i,'delta_rad']) - -1 * veh.tire_w / 2*math.sin(veh.veh_model.loc[i,'delta_rad']),
                                  'rfw':   veh.lcgf,                         # Right front wheel
                                  'rfw_a': veh.lcgf + veh.tire_d / 2 * math.cos(veh.veh_model.loc[i,'delta_rad']) - -1 * veh.tire_w / 2 * math.sin(veh.veh_model.loc[i,'delta_rad']),
                                  'rfw_b': veh.lcgf + veh.tire_d / 2 * math.cos(veh.veh_model.loc[i,'delta_rad']) - veh.tire_w / 2 * math.sin(veh.veh_model.loc[i,'delta_rad']),
                                  'rfw_c': veh.lcgf + -1 * veh.tire_d / 2 * math.cos(veh.veh_model.loc[i,'delta_rad']) - veh.tire_w / 2 * math.sin(veh.veh_model.loc[i,'delta_rad']),
                                  'rfw_d': veh.lcgf + -1 * veh.tire_d / 2*math.cos(veh.veh_model.loc[i,'delta_rad']) - -1 * veh.tire_w / 2 * math.sin(veh.veh_model.loc[i,'delta_rad']),
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
                                  'xaxis': veh.lcgf + veh.f_hang + 1.5,   # line for x-axis
                                  'yaxis': 0,                                      # line for y-axis
                                  'vel_v': veh.veh_model.vx[i] / 10}, ignore_index=True)  # line for velocity vector

        veh.p_vy = veh.p_vy.append({'b_lfc': -1 * veh.v_width / 2,     # body outline
                                  'b_rfc': veh.v_width / 2,
                                  'b_rrc': veh.v_width / 2,
                                  'b_lrc': -1 * veh.v_width / 2,
                                  'lfw':   -1 * (veh.v_width / 2 - veh.tire_w / 2),                         # left front wheel
                                  'lfw_a': -1 * (veh.v_width / 2 - veh.tire_w / 2) + veh.tire_d / 2 * math.sin(veh.veh_model.loc[i,'delta_rad']) + -1 * veh.tire_w / 2 * math.cos(veh.veh_model.loc[i,'delta_rad']),
                                  'lfw_b': -1 * (veh.v_width / 2 - veh.tire_w / 2) + veh.tire_d / 2 *math.sin(veh.veh_model.loc[i,'delta_rad']) + veh.tire_w / 2 * math.cos(veh.veh_model.loc[i,'delta_rad']),
                                  'lfw_c': -1 * (veh.v_width / 2 - veh.tire_w / 2) + -1 * veh.tire_d / 2 * math.sin(veh.veh_model.loc[i,'delta_rad']) + veh.tire_w / 2 * math.cos(veh.veh_model.loc[i,'delta_rad']),
                                  'lfw_d': -1 * (veh.v_width / 2 - veh.tire_w / 2) + -1 * veh.tire_d / 2 * math.sin(veh.veh_model.loc[i,'delta_rad']) + -1 * veh.tire_w / 2 * math.cos(veh.veh_model.loc[i,'delta_rad']),
                                  'rfw':   (veh.v_width / 2 - veh.tire_w / 2),                         # Right front wheel
                                  'rfw_a': (veh.v_width / 2 - veh.tire_w / 2) + veh.tire_d / 2 * math.sin(veh.veh_model.loc[i,'delta_rad']) + -1 * veh.tire_w / 2 * math.cos(veh.veh_model.loc[i,'delta_rad']),
                                  'rfw_b': (veh.v_width / 2 - veh.tire_w / 2) + veh.tire_d / 2 * math.sin(veh.veh_model.loc[i,'delta_rad']) + veh.tire_w / 2 * math.cos(veh.veh_model.loc[i,'delta_rad']),
                                  'rfw_c': (veh.v_width / 2 - veh.tire_w / 2) + -1*veh.tire_d / 2 * math.sin(veh.veh_model.loc[i,'delta_rad']) + veh.tire_w / 2 * math.cos(veh.veh_model.loc[i,'delta_rad']),
                                  'rfw_d': (veh.v_width / 2 - veh.tire_w / 2) + -1*veh.tire_d / 2 * math.sin(veh.veh_model.loc[i,'delta_rad']) + -1 * veh.tire_w / 2 * math.cos(veh.veh_model.loc[i,'delta_rad']),
                                  'rrw':   (veh.v_width / 2 - veh.tire_w / 2),                          # Right rear wheel
                                  'rrw_a': veh.v_width / 2 - veh.tire_w,
                                  'rrw_b': veh.v_width / 2,
                                  'rrw_c': veh.v_width / 2,
                                  'rrw_d': veh.v_width / 2 - veh.tire_w,
                                  'lrw':   -1 * (veh.v_width / 2 - veh.tire_w / 2),                          # Left rear wheel
                                  'lrw_a': -1 * veh.v_width / 2,
                                  'lrw_b': -1 * veh.v_width / 2 + veh.tire_w,
                                  'lrw_c': -1 * veh.v_width / 2 + veh.tire_w,
                                  'lrw_d': -1 * veh.v_width / 2,
                                  'cg':    0,                                         # CG
                                  'xaxis': 0,   # line for x-axis
                                  'yaxis': veh.tire_w / 2 + 1.5,                                      # line for y-axis
                                  'vel_v': veh.veh_model.vy[i] / 10}, ignore_index=True)  # line for velocity vector

    cgx = veh.veh_model[['Dx']].copy()                          # CG location in inertial frame
    cgy = veh.veh_model[['Dy']].copy()

    veh.p_gx = veh.p_vx.copy()                                                    # time variant vehicle geometry for plotting motion in inertial frame
    veh.p_gy = veh.p_vy.copy()                                                    # time variant vehicle geometry for plotting motion in inertial frame

    if (striking == True and veh.edgeimpact == 0):  # impact point (veh1 - striking vehicle)
        # create impact point dataframes with same length as vehicle position data
        impactp_vx = pd.DataFrame({'pimpact_x': [veh.pimpact_x] * len(veh.veh_model.t)})
        impactp_vy = pd.DataFrame({'pimpact_y': [veh.pimpact_y] * len(veh.veh_model.t)})
        impactp_gx = impactp_vx.copy()
        impactp_gy = impactp_vy.copy()

    for i in range(0, len(veh.p_gx)):

           for j in range(0, len(veh.p_vx.columns)):
              # coordinate transformation - rotating vehicle frame to draw vehicle
              veh.p_gx.iloc[i, j] = cgx.Dx[i] + veh.p_vx.iloc[i,j] * math.cos(veh.veh_model.loc[i,'theta_rad']) - veh.p_vy.iloc[i,j] * math.sin(veh.veh_model.loc[i,'theta_rad'])
              veh.p_gy.iloc[i, j] = cgy.Dy[i] + veh.p_vx.iloc[i,j] * math.sin(veh.veh_model.loc[i,'theta_rad']) + veh.p_vy.iloc[i,j] * math.cos(veh.veh_model.loc[i,'theta_rad'])

              if (striking == True and veh.edgeimpact == 0):
                # impact point (veh1 - striking vehicle)
                impactp_gx.pimpact_x[i] = cgx.Dx[i] + veh.pimpact_x * math.cos(veh.veh_model.loc[i,'theta_rad']) - veh.pimpact_y * math.sin(veh.veh_model.loc[i,'theta_rad'])
                impactp_gy.pimpact_y[i] = cgy.Dy[i] + veh.pimpact_x * math.sin(veh.veh_model.loc[i,'theta_rad']) + veh.pimpact_y * math.cos(veh.veh_model.loc[i,'theta_rad']) # time variant vehicle geometry for plotting in vehicle frame

    # copy locked info from vehicle model
    veh.p_gx['lf_lock'] = veh.veh_model.lf_lock.copy()
    veh.p_gx['rf_lock'] = veh.veh_model.rf_lock.copy()
    veh.p_gx['rr_lock'] = veh.veh_model.rr_lock.copy()
    veh.p_gx['lr_lock'] = veh.veh_model.lr_lock.copy()

    if (striking == True and veh.edgeimpact == 0):
        # join impact points with vehicle position data
        veh.p_vx = pd.concat([veh.p_vx, impactp_vx], axis = 1)
        veh.p_vy = pd.concat([veh.p_vy, impactp_vy], axis = 1)
        veh.p_gx = pd.concat([veh.p_gx, impactp_gx], axis = 1)
        veh.p_gy = pd.concat([veh.p_gy, impactp_gy], axis = 1)

    return veh




def position_data_static(vehicle_list):
    """
    static data for plotting vehicle location in global frame
    """

    for veh in vehicle_list:
        veh.px = pd.DataFrame(columns = column_list)                                      # time variant vehicle geometry for plotting in vehicle frame
        veh.py = pd.DataFrame(columns = column_list)

        veh.px = veh.px.append({'b_lfc': veh.lcgf + veh.f_hang,     # body outline
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
                                'vel_v': veh.vx_initial}, ignore_index=True)

        veh.py = veh.py.append({'b_lfc': -1 * veh.v_width / 2,     # body outline
                                'b_rfc': veh.v_width / 2,
                                'b_rrc': veh.v_width / 2,
                                'b_lrc': -1 * veh.v_width / 2,
                                'lfw':   -1 * (veh.v_width / 2 - veh.tire_w / 2),                         # left front wheel
                                'lfw_a': -1 * (veh.v_width / 2),
                                'lfw_b': -1 * (veh.v_width / 2 - veh.tire_w),
                                'lfw_c': -1 * (veh.v_width / 2 - veh.tire_w),
                                'lfw_d': -1 * (veh.v_width / 2),
                                'rfw':   (veh.v_width / 2 - veh.tire_w / 2),                         # Right front wheel
                                'rfw_a': (veh.v_width / 2 - veh.tire_w),
                                'rfw_b': (veh.v_width / 2),
                                'rfw_c': (veh.v_width / 2),
                                'rfw_d': (veh.v_width / 2 - veh.tire_w),
                                'rrw':   (veh.v_width / 2 - veh.tire_w / 2),                          # Right rear wheel
                                'rrw_a': veh.v_width / 2 - veh.tire_w,
                                'rrw_b': veh.v_width / 2,
                                'rrw_c': veh.v_width / 2,
                                'rrw_d': veh.v_width / 2 - veh.tire_w,
                                'lrw':   -1 * (veh.v_width / 2 - veh.tire_w / 2),                          # Left rear wheel
                                'lrw_a': -1 * veh.v_width / 2,
                                'lrw_b': -1 * veh.v_width / 2 + veh.tire_w,
                                'lrw_c': -1 * veh.v_width / 2 + veh.tire_w,
                                'lrw_d': -1 * veh.v_width / 2,
                                'cg':    0,                                         # CG
                                'xaxis': 0,   # line for x-axis
                                'yaxis': veh.v_width / 2 + 1.5,                                      # line for y-axis
                                'vel_v': veh.vy_initial}, ignore_index=True)
        veh.Px = veh.px.copy()
        veh.Py = veh.py.copy()

        # rotate vehicle coordinates using initial heading angle (head_angle)
        veh.Px = veh.init_x_pos + veh.px.mul(math.cos(veh.head_angle * math.pi / 180)) - veh.py.mul(math.sin(veh.head_angle * math.pi / 180))
        veh.Py = veh.init_y_pos + veh.px.mul(math.sin(veh.head_angle * math.pi / 180)) + veh.py.mul(math.cos(veh.head_angle * math.pi / 180))

    return vehicle_list
