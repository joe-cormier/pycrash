get_ipython().run_line_magic("load_ext", " autoreload")
get_ipython().run_line_magic("autoreload", " 2")


import sys
import os
#sys.path.insert(0,'< your path >')
sys.path.insert(0, '/Users/joe/Documents/pycrash')


os.chdir('..')


os.getcwd()


import pycrash
from pycrash.project import Project, project_info, load_project
from pycrash.vehicle import Vehicle
from pycrash.kinematics import SingleMotion
from pycrash.visualization.kinematics_compare import compare_kinematics
from pycrash.visualization.tire_details import tire_details, vertical_forces, long_forces
from pycrash.visualization.cg_motion_compare import cg_motion
from pycrash.visualization.model_interval import plot_motion_interval

import pandas as pd
import numpy as np
import math
import matplotlib.pyplot as plt
from scipy import integrate
import os
pd.options.display.max_columns = None
pd.options.display.max_rows = None


pc_crash_column_names = ['t', 'ax', 'ay', 'az', 'phi_deg', 'rf_fy', 'lf_fy',
                         'rr_fy', 'lr_fy', 'delta_deg', 'rf_delta_deg', 'steer',
                         'steer_rate', 'X', 'Y', 'Z', 'roll', 'pitch', 'theta_deg',
                         'Vx', 'Vy', 'Vz', 'rf_fz', 'lf_fz', 'rr_fz', 'lr_fz',
                         'rf_alpha', 'lf_alpha', 'lr_alpha', 'rr_alpha']


test_file_list = os.listdir(os.path.join(os.getcwd(), 'data', 'external'))
print('List of tests for analysis:')
test_file_list


test_do = 1 # <- cho|ose test number from list to process
print(f'Test to be processed: {test_file_list[test_do]}')


df = pd.read_excel(os.path.join(os.getcwd(), 'data', 'external', test_file_list[test_do]),
                            na_filter = False, header = None, names = pc_crash_column_names, skiprows = 2,
                            usecols = 'A:AD')


#df.steer = [x * -1 for x in df.steer]  # reverse steer - PC-Crash is positive ccw

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


malibu = Vehicle('veh1')


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


df.plot(x='t', y='steer', figsize=(7,4))


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
veh1.time_inputs(t, throttle, brake, steer)
veh1.vx_initial = 30
veh1.hcg = 21.5 / 12  # <- set CG height


sim_defaults = {'dt_motion': 0.005,
                'mu_max': 0.76,
                'alpha_max': 0.174533}


simulation_name = '30 mph steer'
print(f'Creating Simulation: {simulation_name}')
run = SingleMotion(simulation_name, veh1)


plot_motion_interval(run.veh, num_itter = 12)


cg_motion(run.veh.model, df, 'Pycrash', 'PC-Crash')


#run.veh.model.to_csv('45_mphFishook_1footcg.csv', index=False)


run.plot_model()


run.veh.model.tail()


i = len(run.veh.model) - 1 # draw motion at end of simulation
print(f"Time: {run.veh.model.t[i]}")
run.global_motion(i)


# calculate vehicle slip angle for pycrash model - need to correct
phi_rad = []
phi_deg = []
for i in range(len(run.veh.model.t)):
    phi_rad.append(math.atan2(run.veh.model.vy[i], run.veh.model.vx[i])) 
    phi_deg.append(math.atan2(run.veh.model.vy[i], run.veh.model.vx[i])*(180 / math.pi))
    
run.veh.model['phi_rad'] = phi_rad
run.veh.model['phi_deg'] = phi_deg


compare_kinematics(run.veh.model, df, 'Pycrash', 'PC-Crash')


# pycrash
run.veh.model.head()


# forward acceleration greatest difference at peaks
print(f'Minimum forward acceleration Pycrash: {run.veh.model.au.min() / 32.2:0.2f} g')
print(f'Minimum forward acceleration PC-Crash: {df.ax.min() / 32.2:0.2f} g')
print(f'Difference: {(run.veh.model.au.min() - df.ax.min()) / 32.2:0.4f} g')
# rightward acceleration greatest difference at end
print(f'Rightward acceleration at end of sim Pycrash: {run.veh.model.av[len(run.veh.model)-1] / 32.2:0.2f} g')
print(f'Rightward acceleration at end of sim  PC-Crash: {df.ay[len(df)-1] / 32.2:0.2f} g')
print(f'Percent Difference: {(run.veh.model.av[len(run.veh.model)-1] - df.ay[len(df)-1]) / 32.2 :0.4f} g')


tire_details(run.veh)


vertical_forces(run.veh)


run.veh.model.plot(x='t', y='beta_deg', figsize=(7,4), title="Pycrash Heading Angle")


print(f"Pycrash vehicle heading angle of: {run.veh.model.beta_deg[650]:0.1f} deg at {run.veh.model.t[650]} s")
print(f"PC-Crash vehicle heading angle of: {df.theta_deg[65]:0.1f} deg at {df.t[65]} s")
print(f"Difference: {run.veh.model.beta_deg[650]-df.theta_deg[65]:0.1f}")


disp_pycrash = run.veh.model[['t', 'Dx', 'Dy']].copy()
disp_pycrash.rename(columns={'Dx':'Dx_pycrash', 'Dy':'Dy_pycrash'}, inplace=True)
disp_pccrash = df[['t', 'Dx', 'Dy']].copy()
disp_pccrash.rename(columns={'Dx':'Dx_pccrash', 'Dy':'Dy_pccrash'}, inplace=True)
disp_compare = pd.merge(disp_pccrash, disp_pycrash, how = 'left', on = 't')
disp_compare.head()


dx_pycrash = disp_compare.Dx_pycrash.to_list()
dy_pycrash = disp_compare.Dy_pycrash.to_list()
dx_pccrash = disp_compare.Dx_pccrash.to_list()
dy_pccrash = disp_compare.Dy_pccrash.to_list()
time = disp_compare.t.to_list()
dx_diff = [(x - y)**2 for (x,y) in zip(dx_pycrash, dx_pccrash)]
dy_diff = [(x - y)**2 for (x,y) in zip(dy_pycrash, dy_pccrash)]
c_sqrd = [np.sqrt(x + y) for (x,y) in zip(dx_diff, dy_diff)]


c_sqrd[65]


c_sqrd_21in = c_sqrd.copy()


c_sqrd_1ft = c_sqrd.copy()


max(c_sqrd)


c_sqrd_21in[65]


c_sqrd_1ft[65]


print(f"Maximum resultant distance between the CG: {max(c_sqrd):0.2} feet")


plt.figure(figsize=(9,6))
#plt.plot(time, c_sqrd_2, c='black', linewidth=2.0)
plt.plot(time, c_sqrd_1ft, c='black', linewidth=2.0)
plt.plot(time, c_sqrd_21in, c='green', linewidth=2.0)
plt.xlabel("Simulation Time (s)", fontsize=16)
plt.ylabel("Resultant Difference (feet)", fontsize=16)
plt.xticks(fontsize=16)
plt.yticks(fontsize=16)
plt.gca().spines['top'].set_visible(False)
plt.gca().spines['right'].set_visible(False)
plt.show()


x_diff_plot = [dx_pycrash[-1], dx_pccrash[-1]]
y_diff_plot = [dy_pycrash[-1], dy_pccrash[-1]]


colors = ['green', 'black']
plt.scatter(x_diff_plot, y_diff_plot, c=colors)
plt.show()


run.veh.model.to_pickle(os.path.join(os.getcwd(), 'reports', 'single_motion_model_run1.pkl'))


veh1.driver_input.to_pickle(os.path.join(os.getcwd(), 'reports', 'driver_input.pkl'))


os.getcwd()


project_info('validation - single vehicle motion')


proj, veh1, veh2, run = load_project('validation - single vehicle motion')
proj.show()


proj.__dict__


proj.project_path = '< new path if necessary >'


proj.save_project(veh1, veh2, run)


project_info('validation - single vehicle motion')


proj, veh1, veh2, run = load_project('validation - single vehicle motion')
proj.show()


veh1.show()



