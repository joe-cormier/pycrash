"""
Functions for loading external validation data to compare to pycrash
output
validation data should be placed in /data/input/ project directory
"""

from pandas import import pd
import os

# load valdiation data and rename columns
project_dir = os.chdir(os.path.dirname(os.getcwd()))
input_dir = os.path.join(project_dir, 'data', 'input')


filename = 'validation_data.csv'
original = pd.read_csv(os.path.join(input_dir, filename), na_filter = False)

# get list of column names
orginal_columns = original.columns.values()

# create dictionary to change column names to match pycrash convention
new_column_names = [] # list of new names that corrispond to old names

change_names = dict(zip(orginal_columns, new_column_names))
original.rename(columns = change_names, inplace = True)

# %% Create Vehicle instance with validation vehicle properties

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
"width":6.6,
"length":20.66,
"hcg":2,
"lcgf":5.6,
"lcgr":7.76,
"wb":13.36,
"track":5.7,
"f_hang":3.2,
"r_hang":3.873,
"tire_d":2.716666667,
"tire_w":0.866666667,
"izz":3711,
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

val_veh = Vehicle('Veh1', vehicle_input_dict)

# %% Create driver input, or upload from .csv file
end_time = 5  # 5 second simulation
t = list(np.arange(0, end_time+0.1, 0.1))  # create time array from 0 to end time from user
throttle = [0] * len(t)                                # no throttle
brake = [0] * len(t)                                   # no braking
steer = [0] * len(t)                                   # no steering
driver_input_dict = {'t':t, 'throttle':throttle, 'brake':brake, 'steer':steer}
driver_input_df = pd.DataFrame.from_dict(driver_input_dict)

val_veh.driver_input = driver_input_df
