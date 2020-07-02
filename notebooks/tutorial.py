# %% Initilizing
import os
path_parent = os.path.dirname(os.getcwd())
data_directory = os.path.join(path_parent, "data")
os.chdir(path_parent)


# %% Import Modules
import matplotlib.pyplot as plt
from matplotlib.pyplot import text
from src.functions import EnergyDV, SpringSeriesKeff
from src.project import Project, project_info, load_project
from src.vehicle import Vehicle
from src.sdof_model import SDOF_Model
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

proj = Project()



# %% Create vehicle instances
# Vehicle 1:
# TODO: create dictionary for vehicle inputs, then add function for reproducing dictionary
# "Vehicle" stores information about a single vehicle - all possible inputs do not need to be entered
# creating a Vehicle requries a "name" which is used to identify the vehicle in outputs / plots etc. 

vehicle_input_dict = {"year":2016,
"make":"Subaru",
"model":"WRX Sti",
"weight":3000,
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
"izz":13615,
"fwd":0,
"rwd":1,
"awd":0,
"A":100,
"B":41,
"k":1000,
"L":0,
"c":0,
"vx_initial":5,
"vy_initial":0}


veh1 = Vehicle('Veh1', vehicle_input_dict)
#veh1.load_specs('subaru.csv')  # vehicle spectifications loaded from .csv file located in data/input
#veh1.manual_specs()  # user prompted for input

# %% impact point
veh1.impact_point()

# %% impact edge
veh1.impact_edge()

# %% Vehicle 2
veh2 = Vehicle('Veh2')
veh2.load_specs('fordGT.csv')

# %% Save Project with vehicle
proj.save_project(veh1, veh2)

# %% Save Project with vehicle
proj.save_project_test(veh1, veh2)




# %% vehicle input dictionary

vehicle_input_dict = {"year":2016,
"make":"Subaru",
"model":"WRX Sti",
"weight":3000,
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
"izz":13615,
"fwd":0,
"rwd":1,
"awd":0,
"A":100,
"B":41,
"k":1000,
"L":0,
"c":0,
"vx_initial":5,
"vy_initial":0}



# %%
