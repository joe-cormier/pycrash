# -*- coding: utf-8 -*-
"""
Main file used for initiating inputs and running vehicle models
Set paths for vehicle data and driver inputs

"""
# TODO: add video animation


#from _init_ import initialize_model
import os
os.chdir('D:\OneDrive\Vehicle_Dynamics\Code')


from _init_ import initialize_model, constants
from functions import premotion
from plots import plot_inputs
from vehicle import vehicle_model


v_info, v_df = initialize_model()                                         # loads input files
print(v_df)

# calculate vehicle motion for Vehicle 1

v1_in = premotion(1)
cons = constants(1)
#df_in.head()

#plot vehicle data
plot_inputs(v1_in)


# Run models
"""
Vehicle model is run first to create the first record t=0 for velocity data
Tire model is run within the vehicle model to generate forces
"""

veh_1_pre_motion = vehicle_model(v1_in, 1)

"""
Translate vehicle motion into global coordinates
"""


#%%

from plots import plot_vehicle_pre_motion
plot_vehicle_pre_motion(veh_1_pre_motion)

#%%
from global_frame import global_frame_df
       # generates vehicle and global coordinates to draw vehicle outlines
#draw_vx, draw_vy = global_frame_df(veh_1_pre_motion , 1)
draw_vx, draw_vy, draw_gx, draw_gy = global_frame_df(veh_1_pre_motion , 1)


#%% Plot vehicle in vehicle frame
from plots import draw_vehicle
draw_vehicle(draw_vx, draw_vy, 0)

#%% Plot vehicle in global frame
from plots import draw_vehicle_motion
draw_vehicle_motion(draw_gx, draw_gy ,200)

#%% Vehicle.py
# -*- coding: utf-8 -*-
"""
Calculated vehicle premotion
Dependencies = "Inputs" from EDR / manual Inputs
(v_info, v1_in or v2_in)
mu_max defined
"""
import os
os.chdir('D:\OneDrive\Vehicle_Dynamics\Code')

from tire import tire_model
import pandas as pd
import numpy as np
from scipy import integrate
import math


v_info = pd.read_excel('D:\\OneDrive\\Vehicle_Dynamics\\Data\\Input.xlsx', sheet_name = 'vehicles', header = 0)

mu_max = 0.9    # maximum available friction
dt = 0.005

def vehicle_model(vin, vehi):
    # convert dataframe of vehicle info to a dictionary for the designated vehicle
    if vehi == 1:
        v_dict = v_info[['label', 'v1']].copy().set_index('label').to_dict('dict')
        v_dict = v_dict['v1']
    if vehi == 2:
        v_dict = v_info[['label', 'v2']].copy().set_index('label').to_dict('dict')
        v_dict = v_dict['v2']

# Vehicle loop start here -
    for i in (range(len(vin))):
        t = i*dt

        if i == 0:
            # these values are initially taken from edr / input data
            v = vin.loc[i, 'v_edr']
            vx = vin.loc[i, 'vx_edr']
            vy = vin.loc[i, 'vy_edr']
            ax = mu_max * (vin.loc[i, 'throttle'] - vin.loc[i, 'brake'])         # defined throttle and braking - not directly from "EDR" columns
            ay = 0
            oz = vin.loc[i, 'oz']
            oz_rad = vin.loc[i, 'oz']*(math.pi/180)                                   # omega is initially taken from edr / driver input, but will be calcualted after



        if i > 0:                                                                       # vehicle motion is calculated based on equations of motion
            ax = 0
            ay = 0
            vx = 0
            vy = 0
            oz_rad = 0
            oz = oz_rad * 180 / math.pi


     #df['v_edr'] = df.apply(lambda row: np.sqrt(np.square(row.vx_edr) + np.square(row.vy_edr)), axis = 1) # take resultant  velocity



        # these do not need to be part of the loop, they are functions of the changing variables above
        delta_deg = vin.loc[i, 'sw_angle']/ v_dict['steer_ratio']                  # will always be derived from edr data - or manual driver input
        delta_rad = vin.loc[i, 'sw_angle']*(math.pi/180) / v_dict['steer_ratio']
        edr_turn_r = v_dict['wb'] / delta_rad                                       # will always be derived from edr data - or manual driver input
        turn_r =  v**2 / ay                                                         # calculated based on velocity and lateral force on vehicle ()
        beta_deg = math.atan2(vy , vx)*180/math.pi
        beta_rad = math.atan2(vy , vx)
        a = math.sqrt(ax**2 + ay**2)
        v = math.sqrt(vx**2 + vy**2)

        # create row vector to be appended to vehicle data frame
        columns = ['t','v','vx','vy','oz', 'oz_rad', 'delta_deg','delta_rad','edr_turn_r', 'turn_r', 'ax','ay', 'a', 'beta_deg','beta_rad']
        data = [t, v, vx, vy, oz, oz_rad, delta_deg, delta_rad, edr_turn_r, turn_r, ax, ay, a, beta_deg, beta_rad]

        # create dataframe and add data row
        if i == 0:
                v = pd.DataFrame(columns = columns)
                v = v.append(pd.Series(data, index = columns), ignore_index=True)

        # append data to dataframe after i = 0
        if i > 0:
                v = v.append(pd.Series(data, index = columns), ignore_index=True)


        # run tire model to get forces
        if vehi == 1:
            tire_df = tire_model(v, vehi, i)
        if vehi == 2:
            tire_df = tire_model(v, vehi, i)
    return v
