"""
function for processing load cell barrier data from NHTSA
load cell data are downloaded individually as .txt files
displacement data is downloaded as a single .txt file
functions below will merge force and displacement data into a single dataframe for analyses
"""

# %% modules
import os
path_parent = os.path.dirname(os.getcwd())
data_directory = os.path.join(path_parent, "project", "demo", "input")
os.chdir(path_parent)

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from src.project import Project, project_info, load_project
from src.vehicle import Vehicle
from src.sdof_model import SDOF_Model
from src.functions import cipriani

# %% Test Data info
test_info = {'name':'NHTSA 6953', 'number':6953, 'vehicle':'2011 Toyota Camry'}

# %%  get list of files contained in directory with NHTSA load cell data
os.chdir('D:\\OneDrive\\BIOCORE Cases\\Gerard\\JMC Work\\veh2\\nhtsa6953')
os.listdir()


# %%  copy output from above and past below
# channel names
file_names = ['v06953_106fa0_B1.txt',
 'v06953_107fa0_B2.txt',
 'v06953_108fa0_B3.txt',
 'v06953_109fa0_B4.txt',
 'v06953_110fa0_B5.txt',
 'v06953_111fa0_B6.txt',
 'v06953_112fa0_B7.txt',
 'v06953_113fa0_B8.txt',
 'v06953_114fa0_B9.txt',
 'v06953_115fa0_C1.txt',
 'v06953_116fa0_C2.txt',
 'v06953_117fa0_C3.txt',
 'v06953_118fa0_C4.txt',
 'v06953_119fa0_C5.txt',
 'v06953_120fa0_C6.txt',
 'v06953_121fa0_C7.txt',
 'v06953_122fa0_C8.txt',
 'v06953_123fa0_C9.txt',
 'v069AVG_disp.txt']

# create list of user friendly variable names
chnames = ['B1', 'B2', 'B3', 'B4', 'B5', 'B6', 'B7', 'B8', 'B9',
           'C1', 'C2', 'C3', 'C4', 'C5', 'C6', 'C7', 'C8', 'C9', 'disp']

# %% Load NHTSA Data and combine into a single dataframe
for i in range(len(file_names)):
        channel = chnames[i]
        SingleChannel = pd.read_csv(file_names[i], sep = '\t', names = ['time', channel])
        if i == 0:
            df = SingleChannel
        if i > 0:
            df = pd.merge(df, SingleChannel, how = 'left', on = 'time')        

        del SingleChannel

print(f'Combined Load Cell data of shape = {df.shape}')
print('Data is in SI units [N], [mm]')
df.head()

# %% Combined data by columns - 
df['lower'] = df[['B1', 'B2', 'B3', 'B4', 'B5', 'B6', 'B7', 'B8', 'B9']].sum(axis = 1)
df['upper'] = df[['C1', 'C2', 'C3', 'C4', 'C5', 'C6', 'C7', 'C8', 'C9']].sum(axis = 1)
df['total'] = df[['lower', 'upper']].sum(axis = 1)


# %% Plot Functions - English
def load_cell_fdt(df, t_max = 0.150):
    plt.figure(figsize = (19,10))
    plt.title(f"NHTSA {test_info['number']} - {test_info['vehicle']} - Load Cell Barrier Forces", fontsize=22)
    plt.ylabel('Force (lb)', fontsize=16)
    plt.xlabel('Time (s)', fontsize=16)
    plt.xticks(fontsize=16)
    plt.yticks(fontsize=16)
    plt.gca().spines['top'].set_visible(False)
    plt.gca().spines['right'].set_visible(False)
    plt.plot(df.time, df.lower * 0.224809, linewidth = 2, marker = None, c = 'green')
    plt.plot(df.time, df.upper * 0.224809, linewidth = 2, marker = None, c = 'blue')
    plt.plot(df.time, df.total * 0.224809, linewidth = 2, marker = None, c = 'black')
    plt.legend(['Bumper - Lower Row', 'Bumper - Upper Row', 'Bumper - Total'], frameon=False, prop={'size': 14}, loc = 4)
    plt.xlim(0, t_max)
    plt.ylim(min(df.total) * 0.224809 - 5000, max(df.total)* 0.224809 + 5000)
    return plt.show()

def load_cell_fdx(df):
    plt.figure(figsize = (19,10))
    plt.title(f"NHTSA {test_info['number']} - {test_info['vehicle']} - Load Cell Barrier Forces", fontsize=22)
    plt.ylabel('Force (lb)', fontsize=16)
    plt.xlabel('Displacement (in)', fontsize=16)
    plt.xticks(fontsize=16)
    plt.yticks(fontsize=16)
    plt.gca().spines['top'].set_visible(False)
    plt.gca().spines['right'].set_visible(False)
    plt.plot(df.disp * 0.0393701, df.lower * 0.224809, linewidth = 2, marker = None, c = 'green')
    plt.plot(df.disp * 0.0393701, df.upper * 0.224809, linewidth = 2, marker = None, c = 'blue')
    plt.plot(df.disp * 0.0393701, df.total * 0.224809, linewidth = 2, marker = None, c = 'black')
    plt.legend(['Bumper - Lower Row', 'Bumper - Upper Row', 'Bumper - Total'], frameon=False, prop={'size': 14}, loc = 3)
    plt.xlim(0, max(df.disp) * 0.0393701 + 5)
    plt.ylim(min(df.total) * 0.224809 - 5000, max(df.total)* 0.224809 + 5000)

# %% call plot functions
load_cell_fdt(df)
load_cell_fdx(df)

# %% case specific - max dispacements of interest
# create new dataframe limited to <= 0.1 seconds to eliminate rebound
df_model = df[df.time <= 0.1].copy()
#convert displacement to feet and force to lb
df_model['disp_ft'] = df_model.disp.apply(lambda x: x * 0.00328084)
df_model['total_lb'] = df_model.total.apply(lambda x: x * 0.2248090795)
df_model['upper_lb'] = df_model.upper.apply(lambda x: x * 0.2248090795)
df_model['lower_lb'] = df_model.lower.apply(lambda x: x * 0.2248090795)

# use lower bumper force up to 3.3 inches, then only use upper
df_model['model_force'] = np.where((df_model.disp_ft < (3.3/12)), df_model.total_lb, df_model.upper_lb)

# %% plot columns of interest

def plot_fdx(x, y, plot_title = False):
    plt.figure(figsize = (19,10))
    if (plot_title):
        plt.title(plot_title, fontsize=22)
    
    plt.ylabel('Force (lb)', fontsize=16)
    plt.xlabel('Displacement (in)', fontsize=16)
    plt.xticks(fontsize=16)
    plt.yticks(fontsize=16)
    plt.gca().spines['top'].set_visible(False)
    plt.gca().spines['right'].set_visible(False)
   # plt.plot(x * 0.0393701, y * 0.224809, linewidth = 2, marker = None, c = 'green')
   # plt.plot(x * 0.0393701, y * 0.224809, linewidth = 2, marker = None, c = 'blue')
    plt.plot(x * 12, y, linewidth = 2, marker = None, c = 'black')
   # plt.legend(['Bumper - Lower Row', 'Bumper - Upper Row', 'Bumper - Total'], frameon=False, prop={'size': 14}, loc = 3)
    plt.xlim(0, max(x) * 12 + 5)
    plt.ylim(min(y) - 1000, max(y) + 1000)

plot_title = f"NHTSA {test_info['number']} - {test_info['vehicle']} - Load Cell Barrier Forces"
plot_fdx(df_model.disp_ft, df_model.model_force, plot_title)

# %% get percentage of force applied to vehicle by ramp
impactor_height = 0.0254 # [m]
force_height = 2 * 0.246 # [m]
trailer_ratio = impactor_height / force_height

plot_title = f"Trailer Impact Force: Total / Upper Split"
df_model['trailer_force'] = df_model.model_force.apply(lambda x: x * trailer_ratio)
plot_fdx(df_model.disp_ft, df_model.trailer_force, plot_title)

# %%
df_model['total_force_trailer'] = df_model.total_lb.apply(lambda x: x * trailer_ratio)
plot_title = f"Trailer Impact Force: Total"
plot_fdx(df_model.disp_ft, df_model.total_force_trailer, plot_title)


# %% Create Project instance
project_inputs = {'name':'Gerard', 'pdesc':'low speed frontal', 'sim_type':'MV', 'impact_type':'SDOF',
                  'note':'backing trailer with ramp'}

proj = Project(project_inputs)

# %% Create Vehicle Instances


vehicle_input_dict = {"year":2007,
"make":"Chevy",
"model":"Sierra C250",
"weight":3200,
"vin":"1GTHC24KX7E564611",
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
# %% Build model stiffness that will use load cell data from above
kmodel = df_model[['disp_ft', 'total_force_trailer']].copy()

v1_initial = [3, 4, 5]            # initial speeds for striking vehicle
cor_list = [cipriani(i) for i in v1_initial]
colorList = ['k', 'b', 'g']
run_list = ['run1', 'run2', 'run3']
for i in range(len(v1_initial)):
    print(i)
    model_inputs = {"name":run_list[i],
                    "k":kmodel,
                    "cor":cor_list[i], 
                    "tstop":None
                }

    veh1.vx_initial = v1_initial[i]
    run_list[i] = SDOF_Model(veh1, veh2, model_inputs)


# %%
