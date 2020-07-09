# To add a new cell, type '# %%'
# To add a new markdown cell, type '# %% [markdown]'
# %% Initilizing
import os
path_parent = os.path.dirname(os.getcwd())
data_directory = os.path.join(path_parent, "data")
os.chdir(path_parent)

# %% Import Modules
import matplotlib.pyplot as plt
from matplotlib.pyplot import text
from IPython.display import display
from src.functions import EnergyDV, SpringSeriesKeff
from src.sdof_model import SDOF_Model
from src.project import Project, project_info, load_project
from src.vehicle import Vehicle
from scipy import signal
from scipy import integrate
import pandas as pd
import numpy as np
import pickle
import json

pd.options.display.max_columns = None
from IPython import get_ipython
get_ipython().run_line_magic('matplotlib', 'qt')


# %% create updated class variables
project_input = {'name':'Burns',
                 'pdesc':'low speed rear',
                 'sim_type':'MV',
                 'impact_type':'SDOF',
                 'note':'exemplar vehicle inspections'}
proj = Project(project_input)

# %% Vehicle 1

vehicle1_input_dict = {"year":2003,
"make":"Honda",
"model":"CRV",
"weight":3263,
"vin":"SHSRD68483U101517",
"brake":0,
"steer_ratio":0,
"init_x_pos":0,
"init_y_pos":0,
"head_angle":0,
"v_width":0,
"v_length":0,
"hcg":0,
"lcgf":0,
"lcgr":0,
"wb":0,
"track":0,
"f_hang":0,
"r_hang":0,
"tire_d":0,
"tire_w":0,
"izz":0,
"fwd":1,
"rwd":0,
"awd":0,
"A":0,
"B":0,
"k":0,
"L":0,
"c":0,
"vx_initial":5,
"vy_initial":0,
"omega_z";0}

veh1 = Vehicle('CRV', input_dict = vehicle1_input_dict)

# %% Vehicle 2

vehicle2_input_dict = {"year":2014,
"make":"Toyota",
"model":"Camry",
"weight":3177,
"vin":"4T1BF1FK6EU806359",
"brake":0,
"steer_ratio":0,
"init_x_pos":0,
"init_y_pos":0,
"head_angle":0,
"v_width":0,
"v_length":0,
"hcg":0,
"lcgf":0,
"lcgr":0,
"wb":0,
"track":0,
"f_hang":0,
"r_hang":0,
"tire_d":0,
"tire_w":0,
"izz":0,
"fwd":1,
"rwd":0,
"awd":0,
"A":0,
"B":0,
"k":0,
"L":0,
"c":0,
"vx_initial":0,
"vy_initial":0,
"omega_z":0}

veh2 = Vehicle('Camry', input_dict = vehicle2_input_dict)

# %% Save project inputs
proj.save_project(veh1, veh2)

# %% Load Project Data
project_info('Burns')

proj, veh1, veh2 = load_project('Burns')

# %% [markdown]
# # Reconstruction
# %% [markdown]
# ### Load Cell Barrier Data

# %%
#os.chdir('D:\\OneDrive\\BIOCORE Cases\\Burns\\JMC Work\\veh1\\NHTSA4048')
os.listdir('D:\\OneDrive\\BIOCORE Cases\\Burns\\JMC Work\\veh1\\NHTSA4048')

# %%
# channel names
file_names = ['v04084_112fa0_B2.txt',
 'v04084_113fa0_B3.txt',
 'v04084_114fa0_B4.txt',
 'v04084_115fa0_B5.txt',
 'v04084_116fa0_B6.txt',
 'v04084_117fa0_B7.txt',
 'v04084_118fa0_B8.txt',
 'v04084_119fa0_B9.txt',
 'v04084_121fa0_C2.txt',
 'v04084_122fa0_C3.txt',
 'v04084_123fa0_C4.txt',
 'v04084_124fa0_C5.txt',
 'v04084_125fa0_C6.txt',
 'v04084_126fa0_C7.txt',
 'v04084_127fa0_C8.txt',
 'v04084_128fa0_C9.txt',
 'v04084_disp.txt']

chnames = ['B2', 'B3', 'B4', 'B5', 'B6', 'B7', 'B8', 'B9',
           'C2', 'C3', 'C4', 'C5', 'C6', 'C7', 'C8', 'C9', 'disp']

nhtsa_directory = 'D:\\OneDrive\\BIOCORE Cases\\Burns\\JMC Work\\veh1\\NHTSA4048'

# %% Load NHTSA Data
for i in range(len(file_names)):
        channel = chnames[i]
        SingleChannel = pd.read_csv(os.path.join(nhtsa_directory, file_names[i]), sep = '\t', names = ['time', channel])
        if i == 0:
            df = SingleChannel
        if i > 0:
            df = pd.merge(df, SingleChannel, how = 'left', on = 'time')

        del SingleChannel

df.head()

# %% Create crush profile that applies to each load cell column


# %% [markdown]
# ### Sum forces by row

# %% Combine forces to grille
df['lower'] = df[['B2', 'B3', 'B4', 'B5', 'B6', 'B7', 'B8', 'B9']].sum(axis = 1)
df['upper'] = df[['C2', 'C3', 'C4', 'C5', 'C6', 'C7', 'C8', 'C9']].sum(axis = 1)
df['total'] = df[['lower', 'upper']].sum(axis = 1)

#convert displacement to feet and force to lb
df['disp_ft'] = df.disp.apply(lambda x: x * 0.00328084)
df['disp_in'] = df.disp_ft.apply(lambda x: x * 12)
df['total_lb'] = df.total.apply(lambda x: x * 0.2248090795)

# %%
plt.figure(figsize = (19,10))
plt.title('NHTSA 4084 Honda CRV - Load Cell Barrier Forces', fontsize=22)
plt.ylabel('Force (lb)', fontsize=16)
plt.xlabel('Time (s)', fontsize=16)
plt.xticks(fontsize=16)
plt.yticks(fontsize=16)
plt.gca().spines['top'].set_visible(False)
plt.gca().spines['right'].set_visible(False)
plt.plot(df.time, df.lower * 0.224809, linewidth = 2, marker = None, c = 'green')
plt.plot(df.time, df.upper * 0.224809, linewidth = 2, marker = None, c = 'blue')
plt.plot(df.time, df.total * 0.224809, linewidth = 2, marker = None, c = 'black')
plt.legend(['Bumper - Lower Row', 'Bumper - Upper Row', 'Bumper - Total'], frameon=False, prop={'size': 14}, loc = 2)
#plt.xlim(0, 10)
#plt.ylim(0, 1000)


# %%
plt.figure(figsize = (19,10))
plt.title('NHTSA 4084 Honda CRV - Load Cell Barrier Forces', fontsize=22)
plt.ylabel('Force (lb)', fontsize=16)
plt.xlabel('Displacement (in)', fontsize=16)
plt.xticks(fontsize=16)
plt.yticks(fontsize=16)
plt.gca().spines['top'].set_visible(False)
plt.gca().spines['right'].set_visible(False)
plt.plot(df.disp * 0.0393701, df.lower * 0.224809, linewidth = 2, marker = None, c = 'green')
plt.plot(df.disp * 0.0393701, df.upper * 0.224809, linewidth = 2, marker = None, c = 'blue')
plt.plot(df.disp * 0.0393701, df.total * 0.224809, linewidth = 2, marker = None, c = 'black')
plt.legend(['Bumper - Lower Row', 'Bumper - Upper Row', 'Bumper - Total'], frameon=False, prop={'size': 14}, loc = 2)
plt.xlim(0, 25)
#plt.ylim(0, 1000)

# %% use load cell data to create dataframe for stiffness data
df['mutual_disp'] = df.disp_ft.apply(lambda x: x * 2)
k = df[['mutual_disp', 'total_lb']].copy()
k = k[k.mutual_disp >= 0].copy()
k_low = k.copy()
k_low.total_lb = k_low.total_lb.apply(lambda x: x / 2)
k.head()

# %% create model inputs
v1_vx_initial = [5.5, 6, 7.5]      # initial speeds for striking vehicle
colorList = ['k', 'g', 'b']
run_list_names = ['run1', 'run2', 'run3']
cor_list = [0.2 , 0.2, 0.2]  # low restitution from sideswipe

# %% Run three models and plot force-deflection

fig = plt.figure(figsize = (14,12))
plt.title('Mutual Force', fontsize=20)
models =[None] * len(run_list_names)  # create empty list for model runs

for i in range(len(v1_vx_initial)):

    if i == 0:
        kmodel = k_low.copy()
    else:
        kmodel = k.copy()

    model_inputs = {"name":run_list_names[i],
            "k":kmodel,
            "cor":cor_list[i],
            "tstop":0.12
        }

    veh1.vx_initial = v1_vx_initial[i]
    #veh1.k = veh1_k[i]
    #veh2.k = veh2_k[i]
    models[i] = SDOF_Model(veh1, veh2, model_inputs)

    # Calculate vehicle specific crush
    #models[i].model_result['veh1_dx'] = models[i].model_result.dx * (models[i].k / veh1.k)
    #models[i].model_result['veh2_dx'] = models[i].model_result.dx * (models[i].k / veh2.k)
    print(f'Peak Camry Acceleration Model {models[i].name} = {models[i].model_result.a2.max() / 32.2:.2f} g')

    plt.plot(models[i].model_result.t, -1 * models[i].model_result.dx * 12, label = f'Mutual F-dx Vi={v1_vx_initial[i]} mph', color = colorList[i])
    plt.xticks(fontsize=14)
    plt.yticks(fontsize=14)

    plt.xlabel('Time (s)', fontsize=20)
    plt.ylabel('Mutal Crush (in)', fontsize=20)
    plt.grid(which='both', axis='both')
    plt.legend(fontsize=14)
    plt.show()

# %% assign final models
run1, run2, run3 = models

# %% comparison velocity plot - list of models
veh1_colors = ['g', 'g', 'g']
veh2_colors = ['b', 'b', 'b']

def velocity_compare(model_list, veh1_colors, veh2_colors, fill_diff = False, show_legend = False):
    """
    three model runs will be plotted together
    runs should be arranged low / mid / high
    """

    fig = plt.figure(figsize = (14,12))
    plt.title('Vehicle Velocity', fontsize=20)

    for i in range(len(model_list)):
        plt.plot(model_list[i].model_result.t, model_list[i].model_result.v1 * 0.681818, label = f'{model_list[i].name} - {model_list[i].veh1.name}', color = veh1_colors[i])
        plt.plot(model_list[i].model_result.t, model_list[i].model_result.v2 * 0.681818, label = f'{model_list[i].name} - {model_list[i].veh2.name}', color = veh2_colors[i])

    if fill_diff:
        plt.fill_between(model_list[0].model_result.t, model_list[0].model_result.v1 * 0.681818, model_list[len[model_list]].model_result.v1 * 0.681818, alpha=0.3, facecolor=veh1_colors[1])
        plt.fill_between(model_list[0].model_result.t, model_list[0].model_result.v2 * 0.681818, model_list[len[model_list]].model_result.v2 * 0.681818, alpha=0.3, facecolor=veh2_colors[1])


    plt.xticks(fontsize=16)
    plt.yticks(fontsize=16)

    # update to keep track of max / min values
    #plt.xlim([0, max(max(run1.model_result.t), max(run2.model_result.t), max(run3.model_result.t))])
    #plt.ylim([0, 1 + round(max(max(run1.model_result.v1) * 0.681818, max(run2.model_result.v1) * 0.681818, max(run3.model_result.v1) * 0.681818,
                       max(run1.model_result.v2) * 0.681818, max(run2.model_result.v2) * 0.681818, max(run3.model_result.v2) * 0.681818))])

    ax = plt.gca()
    ax.spines['right'].set_visible(False)
    ax.spines['top'].set_visible(False)

    plt.xlabel('Time (s)', fontsize=20)
    plt.ylabel('Velocity (mph)', fontsize=20)

    if show_legend:
        plt.legend(fontsize=14, frameon = False)

    plt.show()


# %% comparison velocity plot
veh1_colors = ['g', 'g', 'g']
veh2_colors = ['b', 'b', 'b']

def velocity_compare(run1, run2, run3, veh1_colors, veh2_colors, fill_diff = False, show_legend = False):
    """
    three model runs will be plotted together
    runs should be arranged low / mid / high
    """

    fig = plt.figure(figsize = (14,12))
    plt.title('Vehicle Velocity', fontsize=20)
    plt.plot(run1.model_result.t, run1.model_result.v1 * 0.681818, label = f'{run1.name} - {run1.veh1.name}', color = veh1_colors[0])
    plt.plot(run2.model_result.t, run2.model_result.v1 * 0.681818, label = f'{run1.name} - {run1.veh1.name}', color = veh1_colors[1])
    plt.plot(run3.model_result.t, run3.model_result.v1 * 0.681818, label = f'{run1.name} - {run1.veh1.name}', color = veh1_colors[2])

    plt.plot(run1.model_result.t, run1.model_result.v2 * 0.681818, label = f'{run1.name} - {run1.veh2.name}', color = veh2_colors[0])
    plt.plot(run2.model_result.t, run2.model_result.v2 * 0.681818, label = f'{run1.name} - {run1.veh2.name}', color = veh2_colors[1])
    plt.plot(run3.model_result.t, run3.model_result.v2 * 0.681818, label = f'{run1.name} - {run1.veh2.name}', color = veh2_colors[2])

    if fill_diff:
        plt.fill_between(run1.model_result.t, run1.model_result.v1 * 0.681818, run3.model_result.v1 * 0.681818, alpha=0.3, facecolor=veh1_colors[1])
        plt.fill_between(run1.model_result.t, run1.model_result.v2 * 0.681818, run3.model_result.v2 * 0.681818, alpha=0.3, facecolor=veh2_colors[1])


    plt.xticks(fontsize=16)
    plt.yticks(fontsize=16)

    plt.xlim([0, max(max(run1.model_result.t), max(run2.model_result.t), max(run3.model_result.t))])
    plt.ylim([0, 1 + round(max(max(run1.model_result.v1) * 0.681818, max(run2.model_result.v1) * 0.681818, max(run3.model_result.v1) * 0.681818,
                       max(run1.model_result.v2) * 0.681818, max(run2.model_result.v2) * 0.681818, max(run3.model_result.v2) * 0.681818))])

    ax = plt.gca()
    ax.spines['right'].set_visible(False)
    ax.spines['top'].set_visible(False)

    plt.xlabel('Time (s)', fontsize=20)
    plt.ylabel('Velocity (mph)', fontsize=20)

    if show_legend:
        plt.legend(fontsize=14, frameon = False)

    plt.show()


# %% Acceleration Plot

def accel_compare(run1, run2, run3, veh1_colors, veh2_colors, fill_diff = False, show_legend = False):
    """
    three model runs will be plotted together
    runs should be arranged low / mid / high
    """

    fig = plt.figure(figsize = (14,12))
    plt.title('Vehicle Acceleration', fontsize=20)
    plt.plot(run1.model_result.t, run1.model_result.a1 / 32.2, label = f'{run1.name} - {run1.veh1.name}', color = veh1_colors[0])
    plt.plot(run2.model_result.t, run2.model_result.a1 / 32.2, label = f'{run1.name} - {run1.veh1.name}', color = veh1_colors[1])
    plt.plot(run3.model_result.t, run3.model_result.a1 / 32.2, label = f'{run1.name} - {run1.veh1.name}', color = veh1_colors[2])

    plt.plot(run1.model_result.t, run1.model_result.a2 / 32.2, label = f'{run1.name} - {run1.veh2.name}', color = veh2_colors[0])
    plt.plot(run2.model_result.t, run2.model_result.a2 / 32.2, label = f'{run1.name} - {run1.veh2.name}', color = veh2_colors[1])
    plt.plot(run3.model_result.t, run3.model_result.a2 / 32.2, label = f'{run1.name} - {run1.veh2.name}', color = veh2_colors[2])

    if fill_diff:
        plt.fill_between(run1.model_result.t, run1.model_result.a1 / 32.2, run3.model_result.v1 / 32.2, alpha=0.3, facecolor=veh1_colors[1])
        plt.fill_between(run1.model_result.t, run1.model_result.a2 / 32.2, run3.model_result.v2 / 32.2, alpha=0.3, facecolor=veh2_colors[1])


    plt.xticks(fontsize=16)
    plt.yticks(fontsize=16)

    plt.xlim([0, max(max(run1.model_result.t), max(run2.model_result.t), max(run3.model_result.t))])
    plt.ylim([-1 + round(min(min(run1.model_result.a1) / 32.2, min(run2.model_result.a1) / 32.2, min(run3.model_result.a1) / 32.2,
                       min(run1.model_result.a2) / 32.2, min(run2.model_result.a2) / 32.2, min(run3.model_result.a2) / 32.2)),
              1 + round(max(max(run1.model_result.a1) / 32.2, max(run2.model_result.a1) / 32.2, max(run3.model_result.a1) / 32.2,
                       max(run1.model_result.a2) / 32.2, max(run2.model_result.a2) / 32.2, max(run3.model_result.a2) / 32.2))])

    ax = plt.gca()
    ax.spines['right'].set_visible(False)
    ax.spines['top'].set_visible(False)

    plt.xlabel('Time (s)', fontsize=20)
    plt.ylabel('Acceleration (g)', fontsize=20)

    if show_legend:
        plt.legend(fontsize=14, frameon = False)

    plt.show()

# %% Plot velocities
velocity_compare(run1, run2, run3, veh1_colors, veh2_colors, fill_diff = True)
accel_compare(run1, run2, run3, veh1_colors, veh2_colors, fill_diff = False)

# %% Force-Deflection
run_colors = ['b', 'g', 'k']
fig = plt.figure(figsize = (14,12))
plt.title('Mutual Force - Deflection', fontsize=20)

for i in range(len(run_list_names)):
    plt.plot(models[i].model_result.dx * -12, models[i].model_result.springF, label = f'{models[i].name} - {models[i].veh1.name}', color = run_colors[i])

plt.xticks(fontsize=14)
plt.yticks(fontsize=14)

plt.xlim([0, -12 * min(min(run1.model_result.dx), min(run2.model_result.dx), min(run3.model_result.dx))])
plt.ylim([0, round(max(max(run1.model_result.springF), max(run2.model_result.springF), max(run3.model_result.springF)))])

ax = plt.gca()
ax.spines['right'].set_visible(False)
ax.spines['top'].set_visible(False)


plt.xlabel('Mutal Crush (in)', fontsize=20)
plt.ylabel('Force (lb)', fontsize=20)
#plt.legend(fontsize=14)

#plt.vlines(0.9, 0, 7000, linestyles='--', colors='r')
#plt.text(0.85, 4000, 'Subject Explorer Deformation', fontdict={'size':16} , rotation=90)
plt.show()

# %% Delta-V | Acceleration
for i in range(len(v1_vx_initial)):
    print(f'Striking Vehicle - {models[i].veh1.name} delta-V in {models[i].name} = {(models[i].model_result.v1.max()-models[i].model_result.v1.min())*0.681818:.2f} mph')
    print(f'Struck Vehicle - {models[i].veh2.name} delta-V in {models[i].name} = {(models[i].model_result.v2.max()-models[i].model_result.v2.min())*0.681818:.2f} mph')
    print("")

for i in range(len(v1_vx_initial)):
    print(f'Striking Vehicle - {models[i].veh1.name} Acceleration in {models[i].name} = {models[i].model_result.a1.min() / 32.2:.2f} g')
    print(f'Struck Vehicle - {models[i].veh2.name} Acceleration in {models[i].name} = {models[i].model_result.a2.max() / 32.2:.2f} g')
    print("")
