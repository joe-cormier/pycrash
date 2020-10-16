# Main Pycrash File
import os
#path_parent = os.getcwd()
project_dir = '/home/jmc/Documents/pycrash/projects/validation - single vehicle motion/'
#project_dir = 'D:\\OneDrive\\pycrash\\projects\\validation - single vehicle motion'

import sys
#sys.path.insert(0,'D:\\OneDrive\\pycrash')
sys.path.insert(0, '/home/jmc/Documents/pycrash')
import pycrash
from pycrash.project import Project, project_info, load_project
from pycrash.vehicle import Vehicle
from pycrash.kinematics import SingleMotion
from pycrash.visualization.kinematics_compare import compare_kinematics
from pycrash.visualization.tire_details import tire_details, vertical_forces, long_forces
from pycrash.visualization.cg_motion_compare import cg_motion

import pandas as pd
import numpy as np
import math
import plotly.io as pio
pio.renderers.default = "browser"  # <- determines how plots are displayed using Plotly
from scipy import integrate
pd.options.display.max_columns = None
pd.options.display.max_rows = None

"""
pc_crash_column_names = ['t', 'ax', 'ay', 'az', 'phi_deg', 'lf_fy', 'rf_fy',
                         'lr_fy', 'rr_fy', 'delta_deg', 'rf_delta_deg', 'steer',
                         'steer_rate', 'X', 'Y', 'Z', 'roll', 'pitch', 'theta_deg',
                         'Vx', 'Vy', 'Vz', 'lf_fz', 'rf_fz', 'lr_fz', 'rr_fz',
                         'lf_alpha', 'rf_alpha', 'lr_alpha', 'rr_alpha']
"""

pc_crash_column_names = ['t', 'ax', 'ay', 'az', 'phi_deg', 'rf_fy', 'lf_fy',
                         'rr_fy', 'lr_fy', 'delta_deg', 'rf_delta_deg', 'steer',
                         'steer_rate', 'X', 'Y', 'Z', 'roll', 'pitch', 'theta_deg',
                         'Vx', 'Vy', 'Vz', 'rf_fz', 'lf_fz', 'rr_fz', 'lr_fz',
                         'rf_alpha', 'lf_alpha', 'lr_alpha', 'rr_alpha']


#pc_crash_file = '15-mph-steer-data.xlsx'
#pc_crash_file = '30-mph-steer-data.xlsx'
pc_crash_file = '60-mph-steer-data.xlsx'
#pc_crash_file = '15-mph-steer-no-cg-height-data.xlsx'
#pc_crash_file = '15-mph-steer-rigid-suspension-data.xlsx'
#pc_crash_file = '15-mph-no-ac-steer-no-cg-height-data.xlsx'
df = pd.read_excel(os.path.join(project_dir, 'data', 'external', pc_crash_file),
                            na_filter = False, header = None, names = pc_crash_column_names, skiprows = 2,
                            usecols = 'A:AD')


# convert velocities to fps
df.Vx = [x * 1.46667 for x in df.Vx]
df.Vy = [x * 1.46667 for x in df.Vy]
df.Vz = [x * 1.46667 for x in df.Vz]

# convert acceleration to fps/s
df.ax = [x * 32.2 for x in df.ax]
df.ay = [x * 32.2 for x in df.ay]
df.az = [x * 32.2 for x in df.az]

# convert tire forces to lb
df.lf_fy = [x * 1000 for x in df.lf_fy]
df.rf_fy = [x * 1000 for x in df.rf_fy]
df.lr_fy = [x * 1000 for x in df.lr_fy]
df.rr_fy = [x * 1000 for x in df.rr_fy]

# steer angle in radians
df['delta_rad'] = [x / 180 * math.pi for x in df.delta_deg]

# integrate velocities to get displacements
df['Dx'] = 0 + integrate.cumtrapz(list(df.Vx), list(df.t), initial=0)
df['Dy'] = 0 + integrate.cumtrapz(list(df.Vy), list(df.t), initial=0)
df.head()


# PC Crash vehicle specifications
vehicle_input_dict = {"year":2004,  # <- creates dictionary of vehicle data for input
"make":"Chevrolet",
"model":"Malibu",
"weight":3298,
"vin":"1G1ZU54854F135916",
"brake":0,
"steer_ratio":15.9,
"init_x_pos":0,
"init_y_pos":0,
"head_angle":0,
"width":70 / 12,
"length":187 / 12,
"hcg":21.5 / 12,
"lcgf":38.1 / 12,
"lcgr":67.9 / 12,
"wb":106 / 12,
"track":60 / 12,
"f_hang":38 / 12,
"r_hang":43 / 12,
"tire_d":26.2 / 12,
"tire_w":8.5 / 12,
"izz":2040,
"fwd":1,
"rwd":0,
"awd":0,
"A":100,
"B":41,
"k":1000,
"L":0,
"c":0,
"vx_initial":0,
"vy_initial":0,
"omega_z":0}

end_time = df.t.max()
t = np.arange(0, end_time + 0.1, 0.1).tolist()
throttle = [0] * len(t)
brake = [0] * len(t)
steer = list(df.steer)
driver_input_dict = {'t':t, 'throttle':throttle, 'brake':brake, 'steer':steer}
driver_input_df = pd.DataFrame.from_dict(driver_input_dict)

veh2 = Vehicle('Veh2', vehicle_input_dict)
veh2.driver_input = driver_input_df
# apply validation data as a model result
veh2.model = df


veh1 = Vehicle('Veh1', vehicle_input_dict)
t = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11]
brake = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
throttle = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
steer = [0, 0, -360, -360, -360, -360, -360, -360, -360, -360, -360, -360]
#steer = [0, 0, 360, 360, 360, 360, 360, 360, 360, 360, 360, 360]
# ".time_inputs()" is an internal function that interpolates time inputs
veh1.time_inputs(t, throttle, brake, steer)
veh1.vx_initial = 60
veh1.hcg = 1.0  # vary cg height

simulation_name = '15_mph_steer'
print(f'Creating Simulation: {simulation_name}')
run = SingleMotion(simulation_name, veh1)

run.plot_model()

i = len(run.veh.model) - 1 # draw motion at end of simulation
print(f"Time: {run.veh.model.t[i]}")
run.global_motion(i)

# calculate vehicle slip angle for pycrash model - need to correct
phi_rad = []
phi_deg = []
for i in range(len(run.veh.model.t)):
    phi_rad.append(math.atan2(run.veh.model.vy[i], run.veh.model.vx[i]) * - 1)
    phi_deg.append(math.atan2(run.veh.model.vy[i], run.veh.model.vx[i]) * -1 *(180 / math.pi))

run.veh.model['phi_rad'] = phi_rad
run.veh.model['phi_deg'] = phi_deg

compare_kinematics(run.veh.model, df, 'pycrash', 'validate')

cg_motion(run.veh.model, df, 'pycrash', 'validate')

tire_details(run.veh)
long_forces(run.veh)
vertical_forces(run.veh)
