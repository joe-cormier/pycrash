import pandas as pd
import math

# columns for vehicle motion DataFrame
column_list = ['b_lfc', 'b_rfc', 'b_rrc', 'b_lrc', 'lfw', 'lfw_a', 'lfw_b',
               'lfw_c', 'lfw_d', 'rfw', 'rfw_a', 'rfw_b', 'rfw_c', 'rfw_d',
                'rrw', 'rrw_a',	'rrw_b', 'rrw_c', 'rrw_d', 'lrw',  'lrw_a',
                'lrw_b', 'lrw_c', 'lrw_d', 'cg', 'xaxis', 'yaxis', 'vel_v']


def position_data_motion(SingleMotion, MV=False):
    """
    set MV to True to return location of impact point in vehicle 1
    """
    # initialize empty dataframe
    p_vx = pd.DataFrame(columns = column_list)                                      # time variant vehicle geometry for plotting in vehicle frame
    p_vy = pd.DataFrame(columns = column_list)                                      # time variant vehicle geometry for plotting in vehicle frame

    # loop for creating seperate dataframes for X and Y components of vehicle drawing in vehicle frame
    for i in (range(len(SingleMotion.veh_motion.t))):
        """
        vehicle frame coordinates for body geometry, tire positions and velocity vector
        if MV = True - impact point and edge points will be tansformed here as well
        """

        p_vx = p_vx.append({'b_lfc': SingleMotion.veh.lcgf + SingleMotion.veh.f_hang,     # body outline
                                  'b_rfc': SingleMotion.veh.lcgf + SingleMotion.veh.f_hang,
                                  'b_rrc': -1* SingleMotion.veh.lcgr + SingleMotion.veh.r_hang,
                                  'b_lrc': -1* SingleMotion.veh.lcgr + SingleMotion.veh.r_hang,
                                  'lfw':   SingleMotion.veh.lcgf,                         # left front wheel
                                  'lfw_a': SingleMotion.veh.lcgf + SingleMotion.veh.tire_d / 2 * math.cos(SingleMotion.SingleMotion.veh_motion.loc[i,'delta_rad']) - -1 * SingleMotion.veh.tire_w / 2 * math.sin(SingleMotion.SingleMotion.veh_motion.loc[i,'delta_rad']),
                                  'lfw_b': SingleMotion.veh.lcgf + SingleMotion.veh.tire_d / 2 * math.cos(SingleMotion.SingleMotion.veh_motion.loc[i,'delta_rad']) - SingleMotion.veh.tire_w / 2 * math.sin(SingleMotion.SingleMotion.veh_motion.loc[i,'delta_rad']),
                                  'lfw_c': SingleMotion.veh.lcgf + -1 * SingleMotion.veh.tire_d / 2 * math.cos(SingleMotion.SingleMotion.veh_motion.loc[i,'delta_rad']) - SingleMotion.veh.tire_w / 2 * math.sin(SingleMotion.SingleMotion.veh_motion.loc[i,'delta_rad']),
                                  'lfw_d': SingleMotion.veh.lcgf + -1 * SingleMotion.veh.tire_d / 2 * math.cos(SingleMotion.SingleMotion.veh_motion.loc[i,'delta_rad']) - -1 * SingleMotion.veh.tire_w / 2*math.sin(SingleMotion.SingleMotion.veh_motion.loc[i,'delta_rad']),
                                  'rfw':   SingleMotion.veh.lcgf,                         # Right front wheel
                                  'rfw_a': SingleMotion.veh.lcgf + SingleMotion.veh.tire_d / 2 * math.cos(SingleMotion.SingleMotion.veh_motion.loc[i,'delta_rad']) - -1 * SingleMotion.veh.tire_w / 2 * math.sin(SingleMotion.SingleMotion.veh_motion.loc[i,'delta_rad']),
                                  'rfw_b': SingleMotion.veh.lcgf + SingleMotion.veh.tire_d / 2 * math.cos(SingleMotion.SingleMotion.veh_motion.loc[i,'delta_rad']) - SingleMotion.veh.tire_w / 2 * math.sin(SingleMotion.SingleMotion.veh_motion.loc[i,'delta_rad']),
                                  'rfw_c': SingleMotion.veh.lcgf + -1 * SingleMotion.veh.tire_d / 2 * math.cos(SingleMotion.SingleMotion.veh_motion.loc[i,'delta_rad']) - SingleMotion.veh.tire_w / 2 * math.sin(SingleMotion.SingleMotion.veh_motion.loc[i,'delta_rad']),
                                  'rfw_d': SingleMotion.veh.lcgf + -1 * SingleMotion.veh.tire_d / 2*math.cos(SingleMotion.SingleMotion.veh_motion.loc[i,'delta_rad']) - -1 * SingleMotion.veh.tire_w / 2 * math.sin(SingleMotion.SingleMotion.veh_motion.loc[i,'delta_rad']),
                                  'rrw':   -1 * SingleMotion.veh.lcgf,                          # Right rear wheel
                                  'rrw_a': -1 * SingleMotion.veh.lcgf + SingleMotion.veh.tire_d / 2,
                                  'rrw_b': -1 * SingleMotion.veh.lcgf + SingleMotion.veh.tire_d / 2,
                                  'rrw_c': -1 * SingleMotion.veh.lcgf - SingleMotion.veh.tire_d / 2,
                                  'rrw_d': -1 * SingleMotion.veh.lcgf - SingleMotion.veh.tire_d / 2,
                                  'lrw':   -1 * SingleMotion.veh.lcgf,                          # Left rear wheel
                                  'lrw_a': -1 * SingleMotion.veh.lcgf + SingleMotion.veh.tire_d / 2,
                                  'lrw_b': -1 * SingleMotion.veh.lcgf + SingleMotion.veh.tire_d / 2,
                                  'lrw_c': -1 * SingleMotion.veh.lcgf - SingleMotion.veh.tire_d / 2,
                                  'lrw_d': -1 * SingleMotion.veh.lcgf - SingleMotion.veh.tire_d / 2,
                                  'cg': 0,                                         # CG
                                  'xaxis': SingleMotion.veh.lcgf + SingleMotion.veh.f_hang + 1.5,   # line for x-axis
                                  'yaxis': 0,                                      # line for y-axis
                                  'vel_v': 10 * math.cos(SingleMotion.SingleMotion.veh_motion.beta_rad[i])}, ignore_index=True)  # line for velocity vector

        p_vy = p_vy.append({'b_lfc': -1 * SingleMotion.veh.v_width / 2,     # body outline
                                  'b_rfc': SingleMotion.veh.v_width / 2,
                                  'b_rrc': SingleMotion.veh.v_width / 2,
                                  'b_lrc': -1 * SingleMotion.veh.v_width / 2,
                                  'lfw':   -1 * (SingleMotion.veh.v_width / 2 - SingleMotion.veh.tire_w / 2),                         # left front wheel
                                  'lfw_a': -1 * (SingleMotion.veh.v_width / 2 - SingleMotion.veh.tire_w / 2) + SingleMotion.veh.tire_d / 2 * math.sin(SingleMotion.SingleMotion.veh_motion.loc[i,'delta_rad']) + -1 * SingleMotion.veh.tire_w / 2 * math.cos(SingleMotion.SingleMotion.veh_motion.loc[i,'delta_rad']),
                                  'lfw_b': -1 * (SingleMotion.veh.v_width / 2 - SingleMotion.veh.tire_w / 2) + SingleMotion.veh.tire_d / 2 *math.sin(SingleMotion.SingleMotion.veh_motion.loc[i,'delta_rad']) + SingleMotion.veh.tire_w / 2 * math.cos(SingleMotion.SingleMotion.veh_motion.loc[i,'delta_rad']),
                                  'lfw_c': -1 * (SingleMotion.veh.v_width / 2 - SingleMotion.veh.tire_w / 2) + -1 * SingleMotion.veh.tire_d / 2 * math.sin(SingleMotion.SingleMotion.veh_motion.loc[i,'delta_rad']) + vSingleMotion.veh.tire_w / 2 * math.cos(SingleMotion.SingleMotion.veh_motion.loc[i,'delta_rad']),
                                  'lfw_d': -1 * (SingleMotion.veh.v_width / 2 - SingleMotion.veh.tire_w / 2) + -1 * SingleMotion.veh.tire_d / 2 * math.sin(SingleMotion.SingleMotion.veh_motion.loc[i,'delta_rad']) + -1 * SingleMotion.veh.tire_w / 2 * math.cos(SingleMotion.SingleMotion.veh_motion.loc[i,'delta_rad']),
                                  'rfw':   (SingleMotion.veh.v_width / 2 - SingleMotion.veh.tire_w / 2),                         # Right front wheel
                                  'rfw_a': (SingleMotion.veh.v_width / 2 - SingleMotion.veh.tire_w / 2) + v_dict['tire_d']/2*math.sin(SingleMotion.SingleMotion.veh_motion.loc[i,'delta_rad']) + -1*v_dict['tire_w']/2*math.cos(SingleMotion.SingleMotion.veh_motion.loc[i,'delta_rad']),
                                  'rfw_b': (SingleMotion.veh.v_width / 2 - SingleMotion.veh.tire_w / 2) + v_dict['tire_d']/2*math.sin(SingleMotion.SingleMotion.veh_motion.loc[i,'delta_rad']) + v_dict['tire_w']/2*math.cos(SingleMotion.SingleMotion.veh_motion.loc[i,'delta_rad']),
                                  'rfw_c': (SingleMotion.veh.v_width / 2 - SingleMotion.veh.tire_w / 2) + -1*v_dict['tire_d']/2*math.sin(SingleMotion.SingleMotion.veh_motion.loc[i,'delta_rad']) + v_dict['tire_w']/2*math.cos(SingleMotion.SingleMotion.veh_motion.loc[i,'delta_rad']),
                                  'rfw_d': (SingleMotion.veh.v_width / 2 - SingleMotion.veh.tire_w / 2) + -1*v_dict['tire_d']/2*math.sin(SingleMotion.SingleMotion.veh_motion.loc[i,'delta_rad']) + -1*v_dict['tire_w']/2*math.cos(SingleMotion.SingleMotion.veh_motion.loc[i,'delta_rad']),
                                  'rrw':   (SingleMotion.veh.v_width / 2 - SingleMotion.veh.tire_w / 2),                          # Right rear wheel
                                  'rrw_a': SingleMotion.veh.v_width / 2 - SingleMotion.veh.tire_w,
                                  'rrw_b': SingleMotion.veh.v_width / 2,
                                  'rrw_c': SingleMotion.veh.v_width / 2,
                                  'rrw_d': SingleMotion.veh.v_width / 2 - SingleMotion.veh.tire_w,
                                  'lrw':   -1 * (SingleMotion.veh.v_width / 2 - SingleMotion.veh.tire_w / 2),                          # Left rear wheel
                                  'lrw_a': -1 * SingleMotion.veh.v_width / 2,
                                  'lrw_b': -1 * SingleMotion.veh.v_width / 2 + SingleMotion.veh.tire_w,
                                  'lrw_c': -1 * SingleMotion.veh.v_width / 2 + SingleMotion.veh.tire_w,
                                  'lrw_d': -1 * SingleMotion.veh.v_width / 2,
                                  'cg':    0,                                         # CG
                                  'xaxis': 0,   # line for x-axis
                                  'yaxis': SingleMotion.veh.tire_w / 2 + 1.5,                                      # line for y-axis
                                  'vel_v': 10 * math.sin(SingleMotion.SingleMotion.veh_motion.beta_rad[i])}, ignore_index=True)  # line for velocity vector

    cgx = SingleMotion.veh_motion[['Dx']].copy()                          # CG location in inertial frame
    cgy = SingleMotion.veh_motion[['Dy']].copy()

    p_gx = p_vx.copy()                                                    # time variant vehicle geometry for plotting motion in inertial frame
    p_gy = p_vy.copy()                                                    # time variant vehicle geometry for plotting motion in inertial frame

    if (MV == True and SingleMotion.veh.edgeimpact == 0):  # impact point (veh1 - striking vehicle)
        # create impact point dataframes with same length as vehicle position data
        impactp_vx = pd.DataFrame({'pimpact_x': [SingleMotion.veh.pimpact_x] * len(SingleMotion.veh_motion.t)})
        impactp_vy = pd.DataFrame({'pimpact_y': [SingleMotion.veh.pimpact_y] * len(SingleMotion.veh_motion.t)})
        impactp_gx = impactp_vx.copy()
        impactp_gy = impactp_vy.copy()

    for i in range(0, len(p_gx)):

           for j in range(0, len(draw_vx.columns)):
              # coordinate transformation - rotating vehicle frame to draw vehicle
              p_gx.iloc[i, j] = cgx.Dx[i] + p_vx.iloc[i,j]*math.cos(SingleMotion.veh_motion.loc[i,'theta_rad']) - p_vy.iloc[i,j] * math.sin(SingleMotion.veh_motion.loc[i,'theta_rad'])
              p_gy.iloc[i, j] = cgy.Dy[i] + p_vx.iloc[i,j]*math.sin(SingleMotion.veh_motion.loc[i,'theta_rad']) + p_vy.iloc[i,j] * math.cos(SingleMotion.veh_motion.loc[i,'theta_rad'])

              if (MV == True and SingleMotion.veh.edgeimpact == 0):
                # impact point (veh1 - striking vehicle)
                impactp_gx.pimpact_x[i] = cgx.Dx[i] + SingleMotion.veh.pimpact_x * math.cos(SingleMotion.veh_motion.loc[i,'theta_rad']) - SingleMotion.veh.pimpact_y * math.sin(SingleMotion.veh_motion.loc[i,'theta_rad'])
                impactp_gy.pimpact_y[i] = cgy.Dy[i] + SingleMotion.veh.pimpact_x * math.sin(SingleMotion.veh_motion.loc[i,'theta_rad']) + SingleMotion.veh.pimpact_y * math.cos(SingleMotion.veh_motion.loc[i,'theta_rad']) # time variant vehicle geometry for plotting in vehicle frame

    # copy locked info from vehicle model
    p_gx['lf_lock'] = motion.lf_lock.copy()
    p_gx['rf_lock'] = motion.rf_lock.copy()
    p_gx['rr_lock'] = motion.rr_lock.copy()
    p_gx['lr_lock'] = motion.lr_lock.copy()

    if (MV == True and SingleMotion.veh.edgeimpact == 0):
        # join impact points with vehicle position data
        p_vx = p_vx.join(impactp_vx)
        p_vy = p_vy.join(impactp_vy)
        p_gx = p_vx.join(impactp_gx)
        p_gy = p_vy.join(impactp_gy)

    return p_vx, p_vy, p_gx, p_gy


# columns for vehicle motion DataFrame
column_list = ['b_lfc', 'b_rfc', 'b_rrc', 'b_lrc', 'lfw', 'lfw_a', 'lfw_b',
               'lfw_c', 'lfw_d', 'rfw', 'rfw_a', 'rfw_b', 'rfw_c', 'rfw_d',
                'rrw', 'rrw_a',	'rrw_b', 'rrw_c', 'rrw_d', 'lrw',  'lrw_a',
                'lrw_b', 'lrw_c', 'lrw_d', 'cg', 'xaxis', 'yaxis', 'vel_v']

def position_data_static(veh1, veh2):
        for veh in [veh1, veh2]:
            veh.px = p_vx.append({'b_lfc': SingleMotion.veh.lcgf + SingleMotion.veh.f_hang,     # body outline
                                    'b_rfc': SingleMotion.veh.lcgf + SingleMotion.veh.f_hang,
                                    'b_rrc': -1* SingleMotion.veh.lcgr + SingleMotion.veh.r_hang,
                                    'b_lrc': -1* SingleMotion.veh.lcgr + SingleMotion.veh.r_hang,
                                    'lfw':   SingleMotion.veh.lcgf,                         # left front wheel
                                    'lfw_a': SingleMotion.veh.lcgf + SingleMotion.veh.tire_d / 2 * math.cos(SingleMotion.SingleMotion.veh_motion.loc[i,'delta_rad']) - -1 * SingleMotion.veh.tire_w / 2 * math.sin(SingleMotion.SingleMotion.veh_motion.loc[i,'delta_rad']),
                                    'lfw_b': SingleMotion.veh.lcgf + SingleMotion.veh.tire_d / 2 * math.cos(SingleMotion.SingleMotion.veh_motion.loc[i,'delta_rad']) - SingleMotion.veh.tire_w / 2 * math.sin(SingleMotion.SingleMotion.veh_motion.loc[i,'delta_rad']),
                                    'lfw_c': SingleMotion.veh.lcgf + -1 * SingleMotion.veh.tire_d / 2 * math.cos(SingleMotion.SingleMotion.veh_motion.loc[i,'delta_rad']) - SingleMotion.veh.tire_w / 2 * math.sin(SingleMotion.SingleMotion.veh_motion.loc[i,'delta_rad']),
                                    'lfw_d': SingleMotion.veh.lcgf + -1 * SingleMotion.veh.tire_d / 2 * math.cos(SingleMotion.SingleMotion.veh_motion.loc[i,'delta_rad']) - -1 * SingleMotion.veh.tire_w / 2*math.sin(SingleMotion.SingleMotion.veh_motion.loc[i,'delta_rad']),
                                    'rfw':   SingleMotion.veh.lcgf,                         # Right front wheel
                                    'rfw_a': SingleMotion.veh.lcgf + SingleMotion.veh.tire_d / 2 * math.cos(SingleMotion.SingleMotion.veh_motion.loc[i,'delta_rad']) - -1 * SingleMotion.veh.tire_w / 2 * math.sin(SingleMotion.SingleMotion.veh_motion.loc[i,'delta_rad']),
                                    'rfw_b': SingleMotion.veh.lcgf + SingleMotion.veh.tire_d / 2 * math.cos(SingleMotion.SingleMotion.veh_motion.loc[i,'delta_rad']) - SingleMotion.veh.tire_w / 2 * math.sin(SingleMotion.SingleMotion.veh_motion.loc[i,'delta_rad']),
                                    'rfw_c': SingleMotion.veh.lcgf + -1 * SingleMotion.veh.tire_d / 2 * math.cos(SingleMotion.SingleMotion.veh_motion.loc[i,'delta_rad']) - SingleMotion.veh.tire_w / 2 * math.sin(SingleMotion.SingleMotion.veh_motion.loc[i,'delta_rad']),
                                    'rfw_d': SingleMotion.veh.lcgf + -1 * SingleMotion.veh.tire_d / 2*math.cos(SingleMotion.SingleMotion.veh_motion.loc[i,'delta_rad']) - -1 * SingleMotion.veh.tire_w / 2 * math.sin(SingleMotion.SingleMotion.veh_motion.loc[i,'delta_rad']),
                                    'rrw':   -1 * SingleMotion.veh.lcgf,                          # Right rear wheel
                                    'rrw_a': -1 * SingleMotion.veh.lcgf + SingleMotion.veh.tire_d / 2,
                                    'rrw_b': -1 * SingleMotion.veh.lcgf + SingleMotion.veh.tire_d / 2,
                                    'rrw_c': -1 * SingleMotion.veh.lcgf - SingleMotion.veh.tire_d / 2,
                                    'rrw_d': -1 * SingleMotion.veh.lcgf - SingleMotion.veh.tire_d / 2,
                                    'lrw':   -1 * SingleMotion.veh.lcgf,                          # Left rear wheel
                                    'lrw_a': -1 * SingleMotion.veh.lcgf + SingleMotion.veh.tire_d / 2,
                                    'lrw_b': -1 * SingleMotion.veh.lcgf + SingleMotion.veh.tire_d / 2,
                                    'lrw_c': -1 * SingleMotion.veh.lcgf - SingleMotion.veh.tire_d / 2,
                                    'lrw_d': -1 * SingleMotion.veh.lcgf - SingleMotion.veh.tire_d / 2,
                                    'cg': 0,                                         # CG
                                    'xaxis': SingleMotion.veh.lcgf + SingleMotion.veh.f_hang + 1.5,   # line for x-axis
                                    'yaxis': 0,                                      # line for y-axis
                                    'vel_v': 10 * math.cos(SingleMotion.SingleMotion.veh_motion.beta_rad[i])}, ignore_index=True)  # line for velocity vector

            veh.py = p_vy.append({'b_lfc': -1 * SingleMotion.veh.v_width / 2,     # body outline
                                    'b_rfc': SingleMotion.veh.v_width / 2,
                                    'b_rrc': SingleMotion.veh.v_width / 2,
                                    'b_lrc': -1 * SingleMotion.veh.v_width / 2,
                                    'lfw':   -1 * (SingleMotion.veh.v_width / 2 - SingleMotion.veh.tire_w / 2),                         # left front wheel
                                    'lfw_a': -1 * (SingleMotion.veh.v_width / 2 - SingleMotion.veh.tire_w / 2) + SingleMotion.veh.tire_d / 2 * math.sin(SingleMotion.SingleMotion.veh_motion.loc[i,'delta_rad']) + -1 * SingleMotion.veh.tire_w / 2 * math.cos(SingleMotion.SingleMotion.veh_motion.loc[i,'delta_rad']),
                                    'lfw_b': -1 * (SingleMotion.veh.v_width / 2 - SingleMotion.veh.tire_w / 2) + SingleMotion.veh.tire_d / 2 *math.sin(SingleMotion.SingleMotion.veh_motion.loc[i,'delta_rad']) + SingleMotion.veh.tire_w / 2 * math.cos(SingleMotion.SingleMotion.veh_motion.loc[i,'delta_rad']),
                                    'lfw_c': -1 * (SingleMotion.veh.v_width / 2 - SingleMotion.veh.tire_w / 2) + -1 * SingleMotion.veh.tire_d / 2 * math.sin(SingleMotion.SingleMotion.veh_motion.loc[i,'delta_rad']) + vSingleMotion.veh.tire_w / 2 * math.cos(SingleMotion.SingleMotion.veh_motion.loc[i,'delta_rad']),
                                    'lfw_d': -1 * (SingleMotion.veh.v_width / 2 - SingleMotion.veh.tire_w / 2) + -1 * SingleMotion.veh.tire_d / 2 * math.sin(SingleMotion.SingleMotion.veh_motion.loc[i,'delta_rad']) + -1 * SingleMotion.veh.tire_w / 2 * math.cos(SingleMotion.SingleMotion.veh_motion.loc[i,'delta_rad']),
                                    'rfw':   (SingleMotion.veh.v_width / 2 - SingleMotion.veh.tire_w / 2),                         # Right front wheel
                                    'rfw_a': (SingleMotion.veh.v_width / 2 - SingleMotion.veh.tire_w / 2) + v_dict['tire_d']/2*math.sin(SingleMotion.SingleMotion.veh_motion.loc[i,'delta_rad']) + -1*v_dict['tire_w']/2*math.cos(SingleMotion.SingleMotion.veh_motion.loc[i,'delta_rad']),
                                    'rfw_b': (SingleMotion.veh.v_width / 2 - SingleMotion.veh.tire_w / 2) + v_dict['tire_d']/2*math.sin(SingleMotion.SingleMotion.veh_motion.loc[i,'delta_rad']) + v_dict['tire_w']/2*math.cos(SingleMotion.SingleMotion.veh_motion.loc[i,'delta_rad']),
                                    'rfw_c': (SingleMotion.veh.v_width / 2 - SingleMotion.veh.tire_w / 2) + -1*v_dict['tire_d']/2*math.sin(SingleMotion.SingleMotion.veh_motion.loc[i,'delta_rad']) + v_dict['tire_w']/2*math.cos(SingleMotion.SingleMotion.veh_motion.loc[i,'delta_rad']),
                                    'rfw_d': (SingleMotion.veh.v_width / 2 - SingleMotion.veh.tire_w / 2) + -1*v_dict['tire_d']/2*math.sin(SingleMotion.SingleMotion.veh_motion.loc[i,'delta_rad']) + -1*v_dict['tire_w']/2*math.cos(SingleMotion.SingleMotion.veh_motion.loc[i,'delta_rad']),
                                    'rrw':   (SingleMotion.veh.v_width / 2 - SingleMotion.veh.tire_w / 2),                          # Right rear wheel
                                    'rrw_a': SingleMotion.veh.v_width / 2 - SingleMotion.veh.tire_w,
                                    'rrw_b': SingleMotion.veh.v_width / 2,
                                    'rrw_c': SingleMotion.veh.v_width / 2,
                                    'rrw_d': SingleMotion.veh.v_width / 2 - SingleMotion.veh.tire_w,
                                    'lrw':   -1 * (SingleMotion.veh.v_width / 2 - SingleMotion.veh.tire_w / 2),                          # Left rear wheel
                                    'lrw_a': -1 * SingleMotion.veh.v_width / 2,
                                    'lrw_b': -1 * SingleMotion.veh.v_width / 2 + SingleMotion.veh.tire_w,
                                    'lrw_c': -1 * SingleMotion.veh.v_width / 2 + SingleMotion.veh.tire_w,
                                    'lrw_d': -1 * SingleMotion.veh.v_width / 2,
                                    'cg':    0,                                         # CG
                                    'xaxis': 0,   # line for x-axis
                                    'yaxis': SingleMotion.veh.tire_w / 2 + 1.5,                                      # line for y-axis
                                    'vel_v': 10 * math.sin(SingleMotion.SingleMotion.veh_motion.beta_rad[i])}, ignore_index=True)  # line for velocity vector

        cgx = SingleMotion.veh_motion[['Dx']].copy()                          # CG location in inertial frame
        cgy = SingleMotion.veh_motion[['Dy']].copy()   

                p_gx.iloc[i, j] = cgx.Dx[i] + p_vx.iloc[i,j]*math.cos(SingleMotion.veh_motion.loc[i,'theta_rad']) - p_vy.iloc[i,j] * math.sin(SingleMotion.veh_motion.loc[i,'theta_rad'])
                p_gy.iloc[i, j] = cgy.Dy[i] + p_vx.iloc[i,j]*math.sin(SingleMotion.veh_motion.loc[i,'theta_rad']) + p_vy.iloc[i,j] * math.cos(SingleMotion.veh_motion.loc[i,'theta_rad'])