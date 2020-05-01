"""
Translate vehicle motion into global coordinates
requires output from vehicle Model
translates vehicle motion to global DataFrame
X - positive to the right
Y - positive up
vin - from impact model
delta_rad (steer tire turn angle)
beta_rad (velocity vector)
Dx, Dy, vehicle displacement in global frame

"""

import pandas as pd
import math
import os

datadir = os.path.abspath(os.curdir) + '\\data\\input'
os.chdir(datadir)

v_info = pd.read_excel('Input.xlsx', sheet_name = 'vehicles', header = 0)

#%% X,Y dataframes for drawing vehicle
head = pd.read_excel('Input.xlsx',sheet_name = 'draw_columns')
columns = head.columns.values.tolist() # Column Headers

def global_frame_impact(impact):
    theta_rad = impact['theta_rad']
    beta_rad = impact['beta_rad']
    DX = impact['DX']
    DY = impact['DY']
    poiX = impact['poiX']
    poiY = impact['poiY']
    delta_rad = impact['delta_rad']

    # convert dataframe of vehicle info to a dictionary for the designated vehicle
    if impact['vehno'] == 1:
        v_dict = v_info[['label', 'v1']].copy().set_index('label').to_dict('dict')
        v_dict = v_dict['v1']
    if impact['vehno'] == 2:
        v_dict = v_info[['label', 'v2']].copy().set_index('label').to_dict('dict')
        v_dict = v_dict['v2']

    draw_vx = pd.DataFrame(columns = columns)                                      # time variant vehicle geometry for plotting in vehicle frame
    draw_vy = pd.DataFrame(columns = columns)                                      # time variant vehicle geometry for plotting in vehicle frame

    draw_vx = draw_vx.append({'b_lfc': v_dict['lcgf'] + v_dict['f_hang'],     # body outline
                              'b_rfc': v_dict['lcgf'] + v_dict['f_hang'],
                              'b_rrc': -1* (v_dict['lcgr'] + v_dict['r_hang']),
                              'b_lrc': -1* (v_dict['lcgr'] + v_dict['r_hang']),
                              'lfw': v_dict['lcgf'],                         # left front wheel
                              'lfw_a': v_dict['lcgf'] + v_dict['tire_d']/2*math.cos(delta_rad) - -1*v_dict['tire_w']/2*math.sin(delta_rad),
                              'lfw_b': v_dict['lcgf'] + v_dict['tire_d']/2*math.cos(delta_rad) - v_dict['tire_w']/2*math.sin(delta_rad),
                              'lfw_c': v_dict['lcgf'] + -1*v_dict['tire_d']/2*math.cos(delta_rad) - v_dict['tire_w']/2*math.sin(delta_rad),
                              'lfw_d': v_dict['lcgf'] + -1*v_dict['tire_d']/2*math.cos(delta_rad) - -1*v_dict['tire_w']/2*math.sin(delta_rad),
                              'rfw': v_dict['lcgf'],                         # Right front wheel
                              'rfw_a': v_dict['lcgf'] + v_dict['tire_d']/2*math.cos(delta_rad) - -1*v_dict['tire_w']/2*math.sin(delta_rad),
                              'rfw_b': v_dict['lcgf'] + v_dict['tire_d']/2*math.cos(delta_rad) - v_dict['tire_w']/2*math.sin(delta_rad),
                              'rfw_c': v_dict['lcgf'] + -1*v_dict['tire_d']/2*math.cos(delta_rad) - v_dict['tire_w']/2*math.sin(delta_rad),
                              'rfw_d': v_dict['lcgf'] + -1*v_dict['tire_d']/2*math.cos(delta_rad) - -1*v_dict['tire_w']/2*math.sin(delta_rad),
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
                              'cg': impact['DX'],                                         # CG
                              'xaxis':v_dict['lcgf'] + v_dict['f_hang']+1.5,   # line for x-axis
                              'yaxis': 0,                                      # line for y-axis
                              'vel_v':10*math.cos(beta_rad)}, ignore_index=True)  # line for velocity vector

    draw_vy = draw_vy.append({'b_lfc': -1*v_dict['v_width']/2,     # body outline
                              'b_rfc': v_dict['v_width']/2,
                              'b_rrc': v_dict['v_width']/2,
                              'b_lrc': -1*v_dict['v_width']/2,
                              'lfw':  -1 * (v_dict['v_width']/2 - v_dict['tire_w']/2),                         # left front wheel
                              'lfw_a': -1 * (v_dict['v_width']/2 - v_dict['tire_w']/2) + v_dict['tire_d']/2*math.sin(delta_rad) + -1*v_dict['tire_w']/2*math.cos(delta_rad),
                              'lfw_b': -1 * (v_dict['v_width']/2 - v_dict['tire_w']/2) + v_dict['tire_d']/2*math.sin(delta_rad) + v_dict['tire_w']/2*math.cos(delta_rad),
                              'lfw_c': -1 * (v_dict['v_width']/2 - v_dict['tire_w']/2) + -1*v_dict['tire_d']/2*math.sin(delta_rad) + v_dict['tire_w']/2*math.cos(delta_rad),
                              'lfw_d': -1 * (v_dict['v_width']/2 - v_dict['tire_w']/2) + -1*v_dict['tire_d']/2*math.sin(delta_rad) + -1*v_dict['tire_w']/2*math.cos(delta_rad),
                              'rfw': (v_dict['v_width']/2 - v_dict['tire_w']/2),                         # Right front wheel
                              'rfw_a': (v_dict['v_width']/2 - v_dict['tire_w']/2) + v_dict['tire_d']/2*math.sin(delta_rad) + -1*v_dict['tire_w']/2*math.cos(delta_rad),
                              'rfw_b':(v_dict['v_width']/2 - v_dict['tire_w']/2) + v_dict['tire_d']/2*math.sin(delta_rad) + v_dict['tire_w']/2*math.cos(delta_rad),
                              'rfw_c':(v_dict['v_width']/2 - v_dict['tire_w']/2) + -1*v_dict['tire_d']/2*math.sin(delta_rad) + v_dict['tire_w']/2*math.cos(delta_rad),
                              'rfw_d':(v_dict['v_width']/2 - v_dict['tire_w']/2) + -1*v_dict['tire_d']/2*math.sin(delta_rad) + -1*v_dict['tire_w']/2*math.cos(delta_rad),
                              'rrw': (v_dict['v_width']/2 - v_dict['tire_w']/2),                          # Right rear wheel
                              'rrw_a':v_dict['v_width']/2 - v_dict['tire_w'],
                              'rrw_b': v_dict['v_width']/2,
                              'rrw_c':v_dict['v_width']/2,
                              'rrw_d':v_dict['v_width']/2 - v_dict['tire_w'],
                              'lrw': -1 * (v_dict['v_width']/2 - v_dict['tire_w']/2),                          # Left rear wheel
                              'lrw_a': -1 * v_dict['v_width']/2,
                              'lrw_b': -1 * v_dict['v_width']/2 + v_dict['tire_w'],
                              'lrw_c': -1 * v_dict['v_width']/2 + v_dict['tire_w'],
                              'lrw_d': -1 * v_dict['v_width']/2,
                              'cg': impact['DY'],                                         # CG
                              'xaxis': 0,   # line for x-axis
                              'yaxis': v_dict['v_width']/2+1.5,                                      # line for y-axis
                              'vel_v':10*math.sin(beta_rad)}, ignore_index=True)  # line for velocity vector

    draw_gx = draw_vx.copy()                                                    # time variant vehicle geometry for plotting motion in inertial frame
    draw_gy = draw_vy.copy()                                                    # time variant vehicle geometry for plotting motion in inertial frame

    for j in range(0, len(draw_vx.columns)):
      # coordinate transformation - rotating vehicle frame to draw vehicle
      draw_gx.iloc[0, j] = draw_vx.loc[0,'cg'] + draw_vx.iloc[0,j]*math.cos(theta_rad) - draw_vy.iloc[0,j] * math.sin(theta_rad)
      draw_gy.iloc[0, j] = draw_vy.loc[0,'cg'] + draw_vx.iloc[0,j]*math.sin(theta_rad) + draw_vy.iloc[0,j] * math.cos(theta_rad)
      draw_gx['cg'] = impact['DX']
      draw_gy['cg'] = impact['DY']
      #draw_gx['vel_v'] = 10*math.cos(beta_rad)
      #draw_gy['vel_v'] = 8*math.sin(beta_rad)
      draw_gx['poi'] = poiX
      draw_gy['poi'] = poiY

    return draw_gx, draw_gy
