"""
Translate vehicle motion into global coordinates
requires output from vehicle Model
translates vehicle motion to global DataFrame
X - positive to the right
Y - positive up
vin - frome vehicle pre premotion or from impact model
delta_rad (steer tire turn angle)
beta_rad (velocity vector)
Dx, Dy, vehicle displacement in global frame

"""

import pandas as pd
import math

v_info = pd.read_excel('Input.xlsx', sheet_name = 'vehicles', header = 0)

#%% X,Y dataframes for drawing vehicle
head = pd.read_excel('Input.xlsx',sheet_name = 'draw_columns')
columns = head.columns.values.tolist() # Column Headers

def global_frame_df(vin, vehi):
    # convert dataframe of vehicle info to a dictionary for the designated vehicle
    if vehi == 1:
        v_dict = v_info[['label', 'v1']].copy().set_index('label').to_dict('dict')
        v_dict = v_dict['v1']
    if vehi == 2:
        v_dict = v_info[['label', 'v2']].copy().set_index('label').to_dict('dict')
        v_dict = v_dict['v2']

    draw_vx = pd.DataFrame(columns = columns)                                      # time variant vehicle geometry for plotting in vehicle frame
    draw_vy = pd.DataFrame(columns = columns)                                      # time variant vehicle geometry for plotting in vehicle frame

    # loop for creating seperate dataframes for X and Y components of vehicle drawing in vehicle frame
    for i in (range(len(vin))):

        draw_vx = draw_vx.append({'b_lfc': v_dict['lcgf'] + v_dict['f_hang'],     # body outline
                                  'b_rfc': v_dict['lcgf'] + v_dict['f_hang'],
                                  'b_rrc': -1* (v_dict['lcgr'] + v_dict['r_hang']),
                                  'b_lrc': -1* (v_dict['lcgr'] + v_dict['r_hang']),
                                  'lfw': v_dict['lcgf'],                         # left front wheel
                                  'lfw_a': v_dict['lcgf'] + v_dict['tire_d']/2*math.cos(vin.loc[i,'delta_rad']) - -1*v_dict['tire_w']/2*math.sin(vin.loc[i,'delta_rad']),
                                  'lfw_b': v_dict['lcgf'] + v_dict['tire_d']/2*math.cos(vin.loc[i,'delta_rad']) - v_dict['tire_w']/2*math.sin(vin.loc[i,'delta_rad']),
                                  'lfw_c': v_dict['lcgf'] + -1*v_dict['tire_d']/2*math.cos(vin.loc[i,'delta_rad']) - v_dict['tire_w']/2*math.sin(vin.loc[i,'delta_rad']),
                                  'lfw_d': v_dict['lcgf'] + -1*v_dict['tire_d']/2*math.cos(vin.loc[i,'delta_rad']) - -1*v_dict['tire_w']/2*math.sin(vin.loc[i,'delta_rad']),
                                  'rfw': v_dict['lcgf'],                         # Right front wheel
                                  'rfw_a': v_dict['lcgf'] + v_dict['tire_d']/2*math.cos(vin.loc[i,'delta_rad']) - -1*v_dict['tire_w']/2*math.sin(vin.loc[i,'delta_rad']),
                                  'rfw_b': v_dict['lcgf'] + v_dict['tire_d']/2*math.cos(vin.loc[i,'delta_rad']) - v_dict['tire_w']/2*math.sin(vin.loc[i,'delta_rad']),
                                  'rfw_c': v_dict['lcgf'] + -1*v_dict['tire_d']/2*math.cos(vin.loc[i,'delta_rad']) - v_dict['tire_w']/2*math.sin(vin.loc[i,'delta_rad']),
                                  'rfw_d': v_dict['lcgf'] + -1*v_dict['tire_d']/2*math.cos(vin.loc[i,'delta_rad']) - -1*v_dict['tire_w']/2*math.sin(vin.loc[i,'delta_rad']),
                                  'rrw': -1*v_dict['lcgr'],                          # Right rear wheel
                                  'rrw_a': -1*v_dict['lcgr'] + v_dict['tire_d']/2,
                                  'rrw_b': -1*v_dict['lcgr'] + v_dict['tire_d']/2,
                                  'rrw_c': -1*v_dict['lcgr'] - v_dict['tire_d']/2,
                                  'rrw_d': -1*v_dict['lcgr'] - v_dict['tire_d']/2,
                                  'lrw': -1*v_dict['lcgr'],                          # Left rear wheel
                                  'lrw_a': -1*v_dict['lcgr'] + v_dict['tire_d']/2,
                                  'lrw_b': -1*v_dict['lcgr'] + v_dict['tire_d']/2,
                                  'lrw_c': -1*v_dict['lcgr'] - v_dict['tire_d']/2,
                                  'lrw_d': -1*v_dict['lcgr'] - v_dict['tire_d']/2,
                                  'cg': 0,                                         # CG
                                  'xaxis':v_dict['lcgf'] + v_dict['f_hang']+1.5,   # line for x-axis
                                  'yaxis': 0,                                      # line for y-axis
                                  'vel_v':10*math.cos(vin.beta_rad[i])}, ignore_index=True)  # line for velocity vector

        draw_vy = draw_vy.append({'b_lfc': -1*v_dict['width']/2,     # body outline
                                  'b_rfc': v_dict['width']/2,
                                  'b_rrc': v_dict['width']/2,
                                  'b_lrc': -1*v_dict['width']/2,
                                  'lfw':  -1 * (v_dict['width']/2 - v_dict['tire_w']/2),                         # left front wheel
                                  'lfw_a': -1 * (v_dict['width']/2 - v_dict['tire_w']/2) + v_dict['tire_d']/2*math.sin(vin.loc[i,'delta_rad']) + -1*v_dict['tire_w']/2*math.cos(vin.loc[i,'delta_rad']),
                                  'lfw_b': -1 * (v_dict['width']/2 - v_dict['tire_w']/2) + v_dict['tire_d']/2*math.sin(vin.loc[i,'delta_rad']) + v_dict['tire_w']/2*math.cos(vin.loc[i,'delta_rad']),
                                  'lfw_c': -1 * (v_dict['width']/2 - v_dict['tire_w']/2) + -1*v_dict['tire_d']/2*math.sin(vin.loc[i,'delta_rad']) + v_dict['tire_w']/2*math.cos(vin.loc[i,'delta_rad']),
                                  'lfw_d': -1 * (v_dict['width']/2 - v_dict['tire_w']/2) + -1*v_dict['tire_d']/2*math.sin(vin.loc[i,'delta_rad']) + -1*v_dict['tire_w']/2*math.cos(vin.loc[i,'delta_rad']),
                                  'rfw': (v_dict['width']/2 - v_dict['tire_w']/2),                         # Right front wheel
                                  'rfw_a': (v_dict['width']/2 - v_dict['tire_w']/2) + v_dict['tire_d']/2*math.sin(vin.loc[i,'delta_rad']) + -1*v_dict['tire_w']/2*math.cos(vin.loc[i,'delta_rad']),
                                  'rfw_b':(v_dict['width']/2 - v_dict['tire_w']/2) + v_dict['tire_d']/2*math.sin(vin.loc[i,'delta_rad']) + v_dict['tire_w']/2*math.cos(vin.loc[i,'delta_rad']),
                                  'rfw_c':(v_dict['width']/2 - v_dict['tire_w']/2) + -1*v_dict['tire_d']/2*math.sin(vin.loc[i,'delta_rad']) + v_dict['tire_w']/2*math.cos(vin.loc[i,'delta_rad']),
                                  'rfw_d':(v_dict['width']/2 - v_dict['tire_w']/2) + -1*v_dict['tire_d']/2*math.sin(vin.loc[i,'delta_rad']) + -1*v_dict['tire_w']/2*math.cos(vin.loc[i,'delta_rad']),
                                  'rrw': (v_dict['width']/2 - v_dict['tire_w']/2),                          # Right rear wheel
                                  'rrw_a':v_dict['width']/2 - v_dict['tire_w'],
                                  'rrw_b': v_dict['width']/2,
                                  'rrw_c':v_dict['width']/2,
                                  'rrw_d':v_dict['width']/2 - v_dict['tire_w'],
                                  'lrw': -1 * (v_dict['width']/2 - v_dict['tire_w']/2),                          # Left rear wheel
                                  'lrw_a': -1 * v_dict['width']/2,
                                  'lrw_b': -1 * v_dict['width']/2 + v_dict['tire_w'],
                                  'lrw_c': -1 * v_dict['width']/2 + v_dict['tire_w'],
                                  'lrw_d': -1 * v_dict['width']/2,
                                  'cg': 0,                                         # CG
                                  'xaxis':0,   # line for x-axis
                                  'yaxis': v_dict['width']/2+1.5,                                      # line for y-axis
                                  'vel_v':10*math.sin(vin.beta_rad[i])}, ignore_index=True)  # line for velocity vector

        # translate vehicle coordinates above to global frame
        # create new dataframes for global coordinates

    cgx = vin[['Dx']].copy()                                                    # CG location in inertial frame
    cgy = vin[['Dy']].copy()

    draw_gx = draw_vx.copy()                                                    # time variant vehicle geometry for plotting motion in inertial frame
    draw_gy = draw_vy.copy()                                                    # time variant vehicle geometry for plotting motion in inertial frame

    for i in range(0, len(draw_vx)):                                            # loop for coordinate transformation
           #print(i)
           for j in range(0, len(draw_vx.columns)):
              #print(i,j)
              # coordinate transformation - rotating vehicle frame to draw vehicle
              draw_gx.iloc[i, j] = cgx.loc[i,'Dx'] + draw_vx.iloc[i,j]*math.cos(vin.loc[i,'theta_rad']) - draw_vy.iloc[i,j] * math.sin(vin.loc[i,'theta_rad'])
              draw_gy.iloc[i, j] = cgy.loc[i,'Dy'] + draw_vx.iloc[i,j]*math.sin(vin.loc[i,'theta_rad']) + draw_vy.iloc[i,j] * math.cos(vin.loc[i,'theta_rad'])
              #draw_gx.loc[i, 'vel_v'] = 10*math.cos(vin.beta_rad[i])
              #draw_gy.loc[i, 'vel_v'] = 8*math.sin(vin.beta_rad[i])

    # copy locked info from vehicle model
    draw_gx['lf_lock'] = vin.lf_lock.copy()
    draw_gx['rf_lock'] = vin.rf_lock.copy()
    draw_gx['rr_lock'] = vin.rr_lock.copy()
    draw_gx['lr_lock'] = vin.lr_lock.copy()

    return draw_vx, draw_vy, draw_gx, draw_gy
