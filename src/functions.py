# -*- coding: utf-8 -*-
"""
Created on Sun May 12 09:59:52 2019

@author: joemc

contains all functions needed by other modules
"""

from scipy import integrate
import numpy as np
import pandas as pd
import os
dt = 0.1



def vehicle_data():
    """
    Load vehicle information from excel file
    Global variables - v_info, v_df, v1_input, v2_input
    """
    global v_info, v_df, v1_input, v2_input, v1_post, v2_post
    v1_input = pd.read_excel('Input.xlsx', sheet_name = 'v1_input', header = 0, usecols = 'A:L')
    v2_input = pd.read_excel('Input.xlsx', sheet_name = 'v2_input', header = 0, usecols = 'A:L')
    v1_post = pd.read_excel('Input.xlsx', sheet_name = 'v1_post', header = 0, usecols = 'A:D')
    v2_post = pd.read_excel('Input.xlsx', sheet_name = 'v2_post', header = 0, usecols = 'A:D')
    v_info = pd.read_excel('Input.xlsx', sheet_name = 'vehicles', header = 0, usecols = 'A:E')
    v_df = v_info[['label','v1','v2']].copy().set_index('label')
    v_df = v_df.rename(columns = {'v1':'1', 'v2':'2'})
    return v_info, v_df


def constants(vehi):
    """
    Create dictionary of constants
    """
    mu_max = 0.9    # maximum available friction
    alpha_max = 20*3.14159/180  # maximum allowable tire slip Angle (20 deg)    [rad]
    roll_rate = 6   # semi-firm 7 = semi soft, 3 = extremely firm (corvette) (degrees / g)
    rc_cg = 18/12    # passenger car - roll center to cg height (h1)  (ft)
    roll_h = 6/12    # roll center height
    cor = 0.2        # coefficent of restitution
    cof = 0.3        # coefficent of friction for impact model

    if vehi == 1:
        weight = v_info.iloc[2, 1]
    if vehi == 2:
        weight = v_info.iloc[2, 2]

    roll_k = 0.5*(weight * rc_cg / roll_rate + weight * rc_cg)  # roll stiffness

    # create dictionary of values for constants
    cons = {'mu_max': mu_max, 'alpha_max': alpha_max, 'roll_rate': 6, 'rc_cg':rc_cg, 'roll_h': roll_h, 'roll_k':roll_k , 'cor':cor, 'cof':cof}
    return cons

def sign(x):
    # returns the sign of a number
    if x > 0:
        return 1
    elif x < 0:
        return -1
    elif x == 0:
        return 0
    else:
        return x

def dfdt(x,t,win):
# create function for taking derivative
# x = column variable to differentiate
# t = column of time data
# win = window length for averaging
    dx = np.zeros(len(x))
    for i in range(len(x)):
        if i == 0:
            dx[i] = 0
        elif i > 1:
            dx[i] = (x[i] - x[i-1]) / (t[i] - t[i-1])

    dx = pd.DataFrame(dx)
    dx_out = dx.rolling(win, min_periods = 1).mean()  # average data over 10 ms to remove large changes over 1 ms intervals
    return dx_out

def premotion(v_num):
    """
    read vehicle data and process initial vehicle motion from input file
    """

    if v_num == 1:
        vdf = v1_input  # detailed input from EDR type data
    if v_num == 2:
        vdf =v2_input   # detailed input from EDR type data

    # Create column vector for time at interval dt. Length will be determined by initial  time of input data and zero
    t = list(np.arange(vdf.input_t[0],0+dt,dt))                                    # last time in df will be 0

    df = pd.DataFrame()                                                             # create dataframe for vehicle input with interpolated values
    df['t'] = t

    # merge dataframe time column with input file by its time column
    vdf['input_t'] = vdf.input_t.round(3)  # force two time columns to have the same number of significant digits
    df['t'] = df.t.round(3)
    df = pd.merge(df, vdf, how = 'left', left_on = 't', right_on = 'input_t')
    df = df.interpolate(method = 'linear') # interpolate NaN values left after merging
    df['vx_edr'] = (df['vx_edr'] * 1.46667).round(1) # this is defined as the edr speed and is not the actual speed since it does not account for sliding and initial condidions
    df['vy_edr'] = (df['vy_edr'] * 1.46667).round(1) # this is defined as the edr speed and is not the actual speed since it does not account for sliding and initial conditions
    df['v_edr'] = (df['v_edr'] * 1.46667).round(1) # this is defined as the edr speed and is not the actual speed since it does not account for sliding and initial conditions
    df = df.drop(columns = ['input_t', 't'])  # drop input time column
    df['t'] = t # reset time column due to interpolating
    df['t'] = df.t.round(3) # reset signficant digits

    df_in = df  # reasign dataframe and delete old variables
    del df, vdf, t
    df_in = df_in.reset_index(drop = True)

    df_in['distx_edr'] = integrate.cumtrapz(list(df_in.vx_edr), list(df_in.t), initial=0)     # integrate edr speed to get overall distance - need initial=0 value to match length
    df_in['disty_edr'] = integrate.cumtrapz(list(df_in.vy_edr), list(df_in.t), initial=0)     # integrate edr speed to get overall distance - need initial=0 value to match length
    df_in['a_edr'] = dfdt(df_in.v_edr, df_in.t, 10)                                           # calcualte derivative of velocity from EDR to get acceleration fps/s

    return df_in

def post_input(v_num):
    """
    interpolate steering wheel angle, throttle and brake data for post impact motion
    """

    if v_num == 1:
        vdf = v1_post  # detailed input from EDR type data
    if v_num == 2:
        vdf =v2_post   # detailed input from EDR type data

    # Create column vector for time at interval dt. Length will be determined by initial  time of input data and zero
    t = list(np.arange(0,vdf.input_t.max()+dt,dt))                                    # first time in df will be 0

    df = pd.DataFrame()                                                             # create dataframe for vehicle input with interpolated values
    df['t'] = t

    # merge dataframe time column with input file by its time column
    vdf['input_t'] = vdf.input_t.round(3)  # force two time columns to have the same number of significant digits
    df['t'] = df.t.round(3)
    df = pd.merge(df, vdf, how = 'left', left_on = 't', right_on = 'input_t')
    df = df.interpolate(method = 'linear') # interpolate NaN values left after merging
    df = df.drop(columns = ['input_t', 't'])  # drop input time column
    df['t'] = t # reset time column due to interpolating
    df['t'] = df.t.round(3) # reset signficant digits

    df_in = df  # reasign dataframe and delete old variables
    del df, vdf, t
    df_in = df_in.reset_index(drop = True)

    return df_in
