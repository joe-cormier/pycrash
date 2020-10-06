
import os
path_parent = os.path.dirname(os.getcwd())

import sys
#sys.path.append("D:\\OneDrive\\pycrash")
#sys.path.append('/home/joemcormier/pycrash')
sys.path.insert(0,'/home/jmc/Documents/pycrash')

import pycrash
from pycrash.project import Project, project_info, load_project
from pycrash.vehicle import Vehicle
from pycrash.kinematicstwo import KinematicsTwo

import pandas as pd
import numpy as np
import math
from scipy import integrate
pd.options.display.max_columns = None
pd.options.display.max_rows = None

# Create Vehicle 1:
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
"width":6,
"length":19.3,
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
"omega_z":0}

veh1 = Vehicle('Veh1', vehicle_input_dict)

# %% Create Vehicle 2:

vehicle_input_dict2 = {"year":2016,
"make":"Subaru",
"model":"WRX Sti",
"weight":3200,
"vin":"123abc",
"brake":0,
"steer_ratio":16.5,
"init_x_pos":25,
"init_y_pos":10,
"head_angle":270,
"width":6,
"length":19.3,
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
"vx_initial":15,
"vy_initial":0,
"omega_z":0}

veh2 = Vehicle('Veh2', vehicle_input_dict2)

t = [0, 1, 2]
brake = [0, 0, 0]
throttle = [0, 0, 0]
steer = [0, 0, 0]
veh1.time_inputs(t, throttle, brake, steer)
veh1.vx_initial = 15
veh1.hcg = 2   # vary cg height


veh2.time_inputs(t, throttle, brake, steer)
veh2.vx_initial = 15
veh2.hcg = 2   # vary cg height

# define impact point - Vehicle 1
# option 2
veh1.pimpact_x = veh1.lcgf + veh1.f_hang
veh1.pimpact_y = 0
veh1.impact_norm_rad = 0
veh1.striking = True

# define impact edge - Vehicle 2
#option 4
veh2.edgeimpact = 4
veh2.edgeimpact_x1 = -1 * veh2.lcgr - veh2.r_hang
veh2.edgeimpact_y1 = -1 * veh2.width / 2
veh2.edgeimpact_x2 = veh2.lcgf + veh2.f_hang
veh2.edgeimpact_y2 = -1 * veh2.width / 2
veh2.striking = False

run = KinematicsTwo('run1', 'IMPC', veh1, veh2)

run.simulate()

#run.draw_simulation(len(run.veh1.model)-1)
run.draw_simulation(100)
