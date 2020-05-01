#%% Change working directory from the workspace root to the ipynb file location. Turn this addition off with the DataScience.changeDirOnImportExport setting
import os
try:
	os.chdir(os.path.join(os.getcwd(), 'notebooks'))
	print(os.getcwd())
except:
	pass
#%% [markdown]
# ## Pycrash
# - Load vehicle data
# - Run vehicle motion
#     - without impact
#     - with impact - assess initial conditions
# - No pre-impact motion
#     - run impact simulation and vehicle runout
# - Generate reports

#%%
os.chdir("..")
print(os.path.abspath(os.curdir))


#%%
datadir = os.path.abspath(os.curdir) + '\data'
reportdir = os.path.abspath(os.curdir) + '\reports'

#%% [markdown]
# #### Load Vehicle Data 
#     1. vehicle specifications
#     2. pre-impact vehicle paths

#%%
import os

import __init__ 
from src.functions import vehicle_data, constants, premotion
from src.plots import plot_inputs
from src.vehicle_model import vehicle_model
from src.plots import plot_vehicle_pre_motion

#%% Vehicle Specifications

  



# #### Initiate Model
# - run initial code that loads vehicle specs and relavent inputs based on purpose
# - Vehicle motion analysis - evaluate potential pre-impact motion etc.
# - Impact simulation - isolate impact with known preimpact conditions - planar-impulse momentum
# - pre and post impact motion with impact simulation - how to determine impact location? 
# ### Additions
# - animation
# - parameter analyses / automated plotting / interations
# - restart kernal to reload inputs?  

#%%
v_info, v_df = vehicle_data()                                
print(v_info)


#%%
# calculate vehicle motion for Vehicle 1
v1_in = premotion(1)
plot_inputs(v1_in)


#%%
# calculate vehicle motion for Vehicle 2
v2_in = premotion(2)
plot_inputs(v2_in)

#%% Vehicle Pre-impact Motion


#%%
veh_1_pre_motion = vehicle_model(1)
plot_vehicle_pre_motion(v1_in, veh_1_pre_motion)


#%%
from src.global_frame import global_frame_df
draw_vx, draw_vy, draw_gx, draw_gy = global_frame_df(veh_1_pre_motion, 1)

from src.plots import draw_vehicle_motion
fig = draw_vehicle_motion(draw_gx, draw_gy, 1, len(draw_gx)-1)


#%%
draw_gx.head()


#%%
#%% Plot vehicle in vehicle frame
#from plots import draw_vehicle
#draw_vehicle(draw_vx, draw_vy, 1000)


#%%
fig.savefig('D:\\OneDrive\\Vehicle_Dynamics\\plots\\global.png')


#%%
# save data files
os.chdir('D:\\OneDrive\\Vehicle_Dynamics\\out')
veh_1_pre_motion.to_csv('veh_1_pre_motion.csv')
v1_in.to_csv('veh_1_pre_input.csv')

#%% [markdown]
# ### Import Image

#%%
import numpy as np
import pandas as pd
import math
import matplotlib.pyplot as plt


#%%
# load DX, DY
os.chdir('D:\\OneDrive\\Vehicle_Dynamics\\out')
v1_pre = pd.read_csv('veh_1_pre_motion.csv', header=0)

theta_shift = 200 * math.pi / 180
x_shift = 1200
y_shift = 700
# rotate and translate
for i in (range(len(v1_pre))):
    v1_pre.loc[i, 'Dx_'] = x_shift + v1_pre.loc[i, 'Dx']*math.cos(theta_shift) - v1_pre.loc[i, 'Dy']*math.sin(theta_shift)
    v1_pre.loc[i, 'Dy_'] = y_shift + v1_pre.loc[i, 'Dx']*math.sin(theta_shift) + v1_pre.loc[i, 'Dy']*math.cos(theta_shift)


#%%
img = plt.imread('D:\\OneDrive\\Vehicle_Dynamics\\Data\\pre_imapct_motion.jpg')
#plt.scatter(x,y,zorder=1)
# height = 1453 ft, 
# width = 2351.4 ft

fig = plt.figure(figsize=(19,15))
plt.scatter(v1_pre.Dx_, v1_pre.Dy_, s=3)
plt.imshow(img, zorder=0, extent=[0, 2451.2, 1453, 0])
plt.show()




