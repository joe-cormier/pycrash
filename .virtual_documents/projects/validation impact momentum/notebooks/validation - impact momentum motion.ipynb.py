# get_ipython().run_line_magic("%", " allow reloading of modules")
get_ipython().run_line_magic("load_ext", " autoreload")
get_ipython().run_line_magic("autoreload", " 2")


import os
os.getcwd()


import sys
sys.path.insert(0, '/Users/joe/Documents/pycrash')


from pycrash.impact_main import Impact
from pycrash.vehicle import Vehicle


import pandas as pd
import numpy as np
import random
from scipy import integrate
pd.options.display.max_columns = None
pd.options.display.max_rows = None
import plotly.figure_factory as ff
import math


# for progress bars
from tqdm.notebook import tqdm, trange
import time


# import plotly
import plotly.graph_objects as go
# tell plotly to use browser for plotting
# if you are using jupyter notebook, then "notebook" will work for an option.
# otherwise, Pycharm and Jupyter Lab get along better with "browser"
import plotly.io as pio
pio.renderers.default = "plotly_mimetype"  # <- determines how plots are displayed using Plotly
#pio.renderers.default = "browser"  # <- determines how plots are displayed using Plotly


# python dictionary containing vehicle specifications
import projects.data.vehicle_data_collection as vehData


from pycrash.visualization.kinematics_compare import compare_kinematics
from pycrash.visualization.cg_motion_compare import cg_motion


veh1 = Vehicle('Striking', vehData.vehicle_data['ChevroletMalibu2004'])
veh1.striking = True  # <- set to striking vehicle

veh2 = Vehicle('Struck', vehData.vehicle_data['HondaAccord'])
veh2.striking = False  # <- set to struck

# create list of impact object
vehicles = [veh1, veh2]


t = [0, 5]
brake = [0, 0]
throttle = [0, 0]
steer = [0, 0]
veh1.time_inputs(t, throttle, brake, steer, show_plot=False)
veh1.vx_initial = 30


veh2.time_inputs(t, throttle, brake, steer, show_plot=False)
veh2.vx_initial = 0


# vehicle 1
# impact point = (x, y, impact plane normal angle [deg])
veh1.impact_points = [(veh1.lcgf + veh1.f_hang - 1, (-1 * veh1.width / 2) + 1, -16.5)]
#veh1.impact_points = [(-veh1.lcgr + 2, -veh1.width / 2, 90), (veh1.lcgf + veh1.f_hang, veh1.width / 2, 0)] # right front corner

# vehicle 2
veh2.edgeimpact = [3]
veh2.edgeimpact_points = [(-1 * veh2.lcgr - veh2.r_hang, -1 * veh2.width / 2, veh2.lcgf + veh2.f_hang, -1 * veh2.width / 2)]


# Vehicle 1
veh1.init_x_pos = 0
veh1.init_y_pos = 0
veh1.head_angle = 0

# Vehicle 2
veh2.init_x_pos = 40
veh2.init_y_pos = -10
veh2.head_angle = -90


# inputs kept constant
t = [0, 1, 2, 3, 4, 5]
throttle = [0] * len(t)
brake = [0] * len(t)
steer = [0] * len(t)
# inputs to vary
vx_initial_range = [25, 35]   # <- initial striking vehicle speed (mph)
imp_x_loc = [0.8, 1.2]        # <- vary impact x location +/- 20% of original value
imp_y_loc = [0.8, 1.2]        # <- vary impact y location +/- 20% of original value
friction_range = [0.3, 0.6]   # <- vary intervehicular friction
impact_order = [[0, 1]]
veh1.time_inputs(t, throttle, brake, steer, show_plot=False)

n=10
# blank dictionary for results
model_results = {}
veh1_dv = []
veh1_initial = []
veh2_dv = []
vehicle_mu = []
""" loop through various combinations """
p_bar = tqdm(range(0, n))
for i in p_bar:
    time.sleep(0.5)
    p_bar.set_description(f'Working on: {i}')
    # impact conditions
    impc_inputs = {0:{'vehicle_mu': random.uniform(friction_range[0], friction_range[1]), 'cor': 0.1}}
    
    # initial speed
    veh1.vx_initial = random.uniform(vx_initial_range[0], vx_initial_range[1])
    
    # impact location
    veh1.impact_points = [((veh1.lcgf + veh1.f_hang - 1) * random.uniform(imp_x_loc[0], imp_x_loc[1]),  # impact point -x (feet)
                           ((-1 * veh1.width / 2) + 1) * random.uniform(imp_y_loc[0], imp_y_loc[1]),    # impact point -y (feet)
                           -16.5)]                                                                      # impact point normal rotation (deg)

    imp = Impact('Scenario1', 2, 'IMPC', [veh1, veh2], impact_order, impc_inputs)
    imp.simulate(show_results=False)
    
    # combine results into lists
    veh1_dv.append(0.681818 * imp.impc_results[0]['veh1_impc_result']['dv'])
    veh1_initial.append(veh1.vx_initial)
    veh2_dv.append(0.681818 * imp.impc_results[0]['veh2_impc_result']['dv'])
    vehicle_mu.append(impc_inputs[0]['vehicle_mu'])

    
    del imp
                          


vehicle_mu_plot = [x * 50 for x in vehicle_mu]
veh2_dv_plot = [x * 2 for x in veh2_dv]


fig = go.Figure()
fig.add_trace(go.Scatter(x=veh1_dv, y=veh2_dv,
                    mode='markers',
                    name='Veh1 DV',
                    marker=dict(
                        color='LightSkyBlue',
                        size=vehicle_mu_plot,
                        line=dict(
                        color='Black',
                        width=1
            ))))
fig.update_layout(
                    showlegend=False,
                    autosize=False,
                    width=1200,
                    height=700,
                    title='Striking and Struck Vehicle Delta-V (n=200)',
                    template='plotly_white',
                    xaxis=dict(showgrid=False, title='Striking delta-V (mph)'),
                    yaxis=dict(showgrid=False, title='Struck delta-V (mph)'),
                    font=dict(family='Arial', size=22, color='black'))
fig.update_xaxes(showline=True, linewidth=1, linecolor='black', ticks="outside",
                 tickwidth=1, tickcolor='black', ticklen=10, zeroline=False)
fig.update_yaxes(showline=True, linewidth=1, linecolor='black', ticks="outside",
                 tickwidth=1, tickcolor='black', ticklen=10, zeroline=False, range=[0, 10])
fig.show()


fig = go.Figure()
fig.add_trace(go.Scatter(x=vehicle_mu, y=veh1_dv,
                    mode='markers',
                    name='Veh1 DV',
                    marker=dict(
                        color='LightSkyBlue',
                        size=veh2_dv_plot,
                        line=dict(
                        color='Black',
                        width=1
            ))))
fig.update_layout(
                    showlegend=False,
                    autosize=False,
                    width=1200,
                    height=700,
                    title='Striking Vehicle Delta-V by Intervehicular Friction (n=200)',
                    template='plotly_white',
                    xaxis=dict(showgrid=False, title='Friction'),
                    yaxis=dict(showgrid=False, title='delta-V (mph)'),
                    font=dict(family='Arial', size=22, color='black'))
fig.update_xaxes(showline=True, linewidth=1, linecolor='black', ticks="outside",
                 tickwidth=1, tickcolor='black', ticklen=10, zeroline=False)
fig.update_yaxes(showline=True, linewidth=1, linecolor='black', ticks="outside",
                 tickwidth=1, tickcolor='black', ticklen=10, zeroline=False, range=[0, 10])
fig.show()


#fig = ff.create_distplot([veh1_dv, veh2_dv], group_labels=['Vehicle 1', 'Vehicle 2'], curve_type='normal', bin_size=.2)
fig = ff.create_distplot([veh1_dv, veh2_dv], group_labels=['Vehicle 1', 'Vehicle 2'], bin_size=.2)
fig.update_layout(
                    showlegend=True,
                    autosize=False,
                    width=1200,
                    height=700,
                    title='Delta-V Distribution (n=200)',
                    template='plotly_white',
                    xaxis=dict(showgrid=False, title='Delta-V (mph)'),
                    yaxis=dict(showgrid=False, title='Density'),
                    font=dict(family='Arial', size=22, color='black'))
fig.update_xaxes(showline=True, linewidth=1, linecolor='black', ticks="outside",
                 tickwidth=1, tickcolor='black', ticklen=10, zeroline=False)
fig.update_yaxes(showline=True, linewidth=1, linecolor='black', ticks="outside",
                 tickwidth=1, tickcolor='black', ticklen=10, zeroline=False)
fig.show()


# name, endTime, impact_type, vehicle_list, impact_order=None, impc_inputs=None, user_sim_defaults=None
imp = Impact('Scenario1', 2, 'IMPC', [veh1, veh2], impact_order, impc_inputs)


imp.show_initial_position()


imp.simulate()


imp.plot_impact(0)


imp.plot_vehicle_motion(5, show_vector=True)


pc_crash_column_names = ['t', 'ax', 'ay', 'az', 'phi_deg', 'lf_fy', 'rf_fy',
                         'lr_fy', 'rr_fy', 'delta_deg', 'rf_delta_deg', 'steer',
                         'steer_rate', 'X', 'Y', 'Z', 'roll', 'pitch', 'theta_deg',
                         'Vx', 'Vy', 'Vz', 'rf_fz', 'lf_fz', 'rr_fz', 'lr_fz',
                         'rf_alpha', 'lf_alpha', 'lr_alpha', 'rr_alpha']


test_file_list = os.listdir(os.path.join(os.getcwd(), 'data', 'input'))
print('List of tests for analysis:')
test_file_list


test_do = 4 # <- cho|ose test number from list to process
print(f'Test to be processed: {test_file_list[test_do]}')


df = pd.read_excel(os.path.join(os.getcwd(), 'data', 'input', test_file_list[test_do]),
                            na_filter = False, header = None, names = pc_crash_column_names, skiprows = 2,
                            usecols = 'A:AD', nrows=51, sheet_name='target data')


df = pd.read_excel(os.path.join(os.getcwd(), 'data', 'input', test_file_list[test_do]),
                            na_filter = False, header = None, names = pc_crash_column_names, skiprows = 2,
                            usecols = 'A:AD', nrows=51, sheet_name='bullet data')


df.head()


#df.steer = [x * -1 for x in df.steer]  # reverse steer - PC-Crash is positive ccw

# convert velocities to fps
df.Vx = [x * 1.46667 for x in df.Vx]
df.Vy = [x * -1.46667 for x in df.Vy]
df.Vz = [x * 1.46667 for x in df.Vz]

# convert acceleration to fps/s
df.ax = [x * 32.2 for x in df.ax]
df.ay = [x * -32.2 for x in df.ay]
df.az = [x * 32.2 for x in df.az]

# convert tire forces to lb
df.lf_fy = [x * 1000 for x in df.lf_fy]
df.rf_fy = [x * 1000 for x in df.rf_fy]
df.lr_fy = [x * 1000 for x in df.lr_fy]
df.rr_fy = [x * 1000 for x in df.rr_fy]

# steer angle in radians
df['delta_rad'] = [x / 180 * np.pi for x in df.delta_deg]

# integrate velocities to get displacements
df['Dx'] = df.X
df['Dy'] = [x * -1 for x in df.Y]

df['theta_deg'] = [x * -1 for x in df.theta_deg]
df.head()


target = df.copy()


bullet = df.copy()


# calculate vehicle slip angle for pycrash model - need to correct
for j in range(0, len(imp.vehicles)):
    phi_rad = []
    phi_deg = []
    for i in range(len(imp.vehicles[j].model.t)):
        phi_rad.append(math.atan2(imp.vehicles[j].model.vy[i], imp.vehicles[j].model.vx[i]))
        phi_deg.append(math.atan2(imp.vehicles[j].model.vy[i], imp.vehicles[j].model.vx[i])*(180 / math.pi))
    imp.vehicles[j].model['phi_rad'] = phi_rad
    imp.vehicles[j].model['phi_deg'] = phi_deg


compare_kinematics(imp.vehicles[1].model, target, 'Pycrash', 'PC-Crash')


cg_motion(imp.vehicles[1].model, target, 'Pycrash', 'PC-Crash')






