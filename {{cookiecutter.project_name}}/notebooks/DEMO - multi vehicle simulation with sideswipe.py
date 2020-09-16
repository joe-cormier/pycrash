# %% Initilizing
import os
path_parent = os.path.dirname(os.getcwd())
data_directory = os.path.join(path_parent, "data")
os.chdir(path_parent)

# %% allow reloading of modules
%load_ext autoreload
%autoreload 2
# %% Import Modules
import matplotlib.pyplot as plt
from matplotlib.pyplot import text
from src.functions import EnergyDV, SpringSeriesKeff
from src.project import Project, project_info, load_project
from src.vehicle import Vehicle
from src.kinematicstwo import KinematicsTwo
from scipy import signal
from scipy import integrate
import pandas as pd
import numpy as np
import pickle
import json

pd.options.display.max_columns = None
from IPython import get_ipython
from IPython.display import display
get_ipython().run_line_magic('matplotlib', 'inline')

# %% Create Project
# projects are used to store basic information about the project
# - name, type of impact, type of simulation to be run, description, notes
# the project will be used to save all associated aspects, vehicles, simulations etc.
project_inputs = {'name':'Practice', 'pdesc':'single motion', 'sim_type':'SV', 'impact_type':'none',
                  'note':'single vehicle motion demo'}
proj = Project(project_inputs)

# %% generate dataframe with driver inputs for vehicle 1 (striking vehicle)
# note - think of a dataframe as a basic excel sheet (header row and data columns)
# the time duration "end_time" is critical becuase it determines length of simulation

end_time = 5  # 5 second simulation
t = list(np.arange(0, end_time+0.1, 0.1))  # create time array from 0 to end time from user
throttle = [0] * len(t)                                # no throttle
brake = [0] * len(t)                                   # no braking
steer = [0] * len(t)                                   # no steering
driver_input_dict = {'t':t, 'throttle':throttle, 'brake':brake, 'steer':steer}
driver_input_df = pd.DataFrame.from_dict(driver_input_dict)
print('Vehicle 1 Driver Inputs:')
driver_input_df.head() # first 5 rows of driver input data

# %% Create Vehicle 1:
# "Vehicle" stores information about a single vehicle - all possible inputs do not need to be entered
# creating a Vehicle requries a "name" which is used to identify the vehicle in outputs / plots etc. 

vehicle_input_dict = {"year":2016,
"make":"Subaru",
"model":"WRX Sti",
"weight":3200,
"vin":"123abc",
"brake":0,
"steer_ratio":16.5,
"init_x_pos":0,
"init_y_pos":0,
"head_angle":0,
"v_width":6,
"v_length":19.3,
"hcg":2,
"lcgf":4.88,
"lcgr":6.96,
"wb":11.84,
"track":6.6,
"f_hang":3.2,
"r_hang":4.1,
"tire_d":2.716666667,
"tire_w":0.866666667,
"izz":2500,
"fwd":0,
"rwd":1,
"awd":0,
"A":100,
"B":41,
"k":1000,
"L":0,
"c":0,
"vx_initial":10,
"vy_initial":0,
"omega_z":0,
"driver_input":driver_input_df}

veh1 = Vehicle('Veh1', vehicle_input_dict)
#veh1.load_specs('subaru.csv')  # vehicle spectifications loaded from .csv file located in data/input
#veh1.manual_specs()  # user prompted for input

# %% Assign impact point for Vehicle 1
# user will be prompted for a choice using a helper graphic
veh1.impact_point()


# %% Create Vehicle 2
# vehicle data can also be created by importing a CSV file in the data/input directory

veh2 = Vehicle('Veh2')
veh2.load_specs('fordGT.csv')

# %% driver input can be added at anytime
end_time = 5  # 5 second simulation
t = list(np.arange(0, end_time+0.1, 0.1))  # create time array from 0 to end time from user
throttle = [0] * len(t)                                # no throttle
brake = [0] * len(t)                                   # no braking
steer = [0] * len(t)                                   # no steering
driver_input_dict = {'t':t, 'throttle':throttle, 'brake':brake, 'steer':steer}
driver_input_df = pd.DataFrame.from_dict(driver_input_dict)
print('Vehicle 2 Driver Inputs:')

veh2.driver_input = driver_input_df
veh2.driver_input.head() # first 5 rows of driver input data

# %% Assing impact edge for Vehicle 2
# user will be prompted for a choice

veh2.impact_edge()
# %% Save Project with vehicle
proj.save_project(veh1, veh2)



# %% Generate an instance of multi vehicle model
# this function takes a list of vehicles - always set in order of [striking, struck]
# requires two inputs:
# 1. vehicle_list = [vehicle1, vehicle2]
# 2. impact_type = {'ss' (sideswipe), 'impc' (impulse momentum)}
# optional - ignore_driver = False (default) - simulation will ignore driver inputs after impact and use entry at impact

ss1 = KinematicsTwo('intersection', veh1, veh2)

# %% set-up vehicle initial location
# use an motion data to show paths



# %% run simulation
ss1.simulate(impact_type = 'ss', ignore_driver = False)

# %%
