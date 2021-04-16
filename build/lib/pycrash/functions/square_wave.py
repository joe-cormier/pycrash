""" 
generate square wave acceleration profile for free
particle analyses
"""

# %% modules
import os
os.chdir('D:\\OneDrive\\pycrash')

from data.defaults.config import default_dict
import matplotlib.pyplot as plt
from scipy import integrate
import pandas as pd
import numpy as np

dt_impact = default_dict['dt_impact']            # iteration time step

# %% reate input columns
end_time = 0.136                # time duration seconds
constant_accel = -1 * 32.2      # constant acceleration (f/s/s)
v_initial = 60 * 1.46667        # initial speed (fps)
x_initial = 0                   # initial position (ft)

t = list(np.arange(0, dt_impact + end_time, dt_impact))  # create time array from 0 to max time in inputs, this will be end time for simulation
t = [round(x, 4) for x in t]
a = [constant_accel] * len(t)
v = v_initial + integrate.cumtrapz(a, t, initial = 0)     # integrate accel to get velocity
x = x_initial + integrate.cumtrapz(v, t, initial = 0)     # integrate velocity to get position

# %% calculate free particle relative displacement

def relative_disp(t, x, v_initial):
    x_relative = [None] * len(t)
    for i in range(len(t)):
        free_part_x = v_initial * t[i]
        x_relative[i] = free_part_x - x[i]
    
    return x_relative

# %% Create range of runs
accel_list = [-0.5 * 32.2, -0.75 * 32.2, -1 * 32.2] # list for model runs   
x_list = [None] * len(accel_list)
v_list = [None] * len(accel_list)
x_relative_list = [None] * len(accel_list)

for i in range(len(accel_list)):
    a = [accel_list[i]] * len(t)
    v_list[i] = v_initial + integrate.cumtrapz(a, t, initial = 0)
    x_list[i] = x_initial + integrate.cumtrapz(v_list[i], t, initial = 0)
    x_relative_list[i] = relative_disp(t, x_list[i], v_initial)

# %% Plot Velocity
plt.figure(figsize = (16,9))
#plt.title('Velocity', fontsize=20)
color_list = ['b', 'g', 'k']

for i in range(len(accel_list)):
    v_mph = [x / 1.46667 for x in v_list[i]]
    print(f'Total Change in Speed = {v_mph[len(v_mph)-1] - v_mph[0]:0.2f} mph')
    print(f'Final Speed = {v_mph[len(v_mph)-1]:0.2f} mph')
    print("")
    plt.plot(t, v_mph, label = f'Accel = {accel_list[i]/32.2:0.2f} g', c = color_list[i])  

plt.xticks(fontsize=16)
plt.yticks(fontsize=16)
plt.xlim([0, max(t)])
plt.ylim([round(min(v_mph), 1) - 0.5, round(max(v_mph), 1)])
ax = plt.gca()
ax.spines['right'].set_visible(False)
ax.spines['top'].set_visible(False)
plt.xlabel('Time(s)', fontsize=20)
plt.ylabel('Velocity (mph)', fontsize=20)
plt.legend(fontsize=16, frameon = False)
plt.show()


# %% Plot Relative Displacement
plt.figure(figsize = (16,9))
#plt.title('Relative Displacement', fontsize=20)
color_list = ['b', 'g', 'k']

for i in range(len(accel_list)):
    x_rel_inches = [x * 12 for x in x_relative_list[i]]
    print(f'Total Relative Motion = {x_rel_inches[len(x_rel_inches)-1]:0.1f} in')
    print("")
    plt.plot(t, x_rel_inches, label = f'Accel = {accel_list[i]/32.2:0.2f} g', c = color_list[i])  

plt.xticks(fontsize=16)
plt.yticks(fontsize=16)
plt.xlim([0, max(t)])
plt.ylim([0, round(max(x_rel_inches), 1) + 0.5])
ax = plt.gca()
ax.spines['right'].set_visible(False)
ax.spines['top'].set_visible(False)
plt.xlabel('Time(s)', fontsize=20)
plt.ylabel('Relative Displacement (inch)', fontsize=20)
plt.legend(fontsize=16, frameon = False)
plt.show()
