# TODO: check properties of each input - use list of data types
# TODO: option to save inputs and outputs to csv

# %% modules
from .data.defaults.config import default_dict
from tabulate import tabulate
from itertools import count
from .visualization.vehicle import plot_impact_points, plot_impact_edge, plot_driver_inputs
from .collision_plane import define_impact_plane, define_impact_edge
import pandas as pd
import numpy as np
import inspect
import os
import csv

# load defaults
mu_max = default_dict['mu_max']    # maximum available friction
dt_motion = default_dict['dt_motion']            # iteration time step

print('Current values for defined constants:')
print(f'maximum available friction (mu_max) = {mu_max}')
print(f'time step for vehicle motion (dt) = {dt_motion} s')

# vehicle inputs - values used in csv file for input should match these below
# additional values requires a value for input_query, veh_input, dtype be provided
# must be in same position in each list

input_query = ["Model year",
"Vehicle make",
"Vehicle model",
"Vehicle weight (lb)",
"Vehicle Identification Number (VIN)",
"Percent Braking",
"Steering ratio",
"Initial X position (ft)",
"Initial Y position (ft)",
"Initial heading angle (deg)",
"Vehicle width (ft)",
"Vehicle length (ft)",
"CG height (ft)",
"CG to front axle (ft)",
"CG to rear axle (ft)",
"Wheelbase (ft)",
"Track width (ft)",
"Front overhang (ft)",
"Rear overhang (ft)",
"Tire diameter (ft)",
"Tire width (ft)",
"Izz (lb-ft-s^2)",
"Front wheel drive (0/1)",
"Rear wheel drive (0/1)",
"All wheel drive (0/1)",
"Stiffness value A [lb/in]",
"Stiffness slope B [lb/in/in]",
"Effective spring stiffness k [lb/in]",
"Damage length L [in]",
"Crush depth c [in]",
"Initial forward velocity Vx (mph)",
"Initial lateral velocity Vy (mph)",
"Initial Yaw Rate (deg/s)"]

veh_inputs = ["year",
"make",
"model",
"weight",
"vin",
"brake",
"steer_ratio",
"init_x_pos",
"init_y_pos",
"head_angle",
"width",
"length",
"hcg",
"lcgf",
"lcgr",
"wb",
"track",
"f_hang",
"r_hang",
"tire_d",
"tire_w",
"izz",
"fwd",
"rwd",
"awd",
"A",
"B",
"k",
"L",
"c",
"vx_initial",
"vy_initial",
"omega_z"]




class Vehicle:
    """
    Vehicle - contains all data assigned to a vehicle used to run various simulations
    not all values are required to create a vehicle instance
    requires 'Name' - used to idenify vehicle in simulations
    can be useful to create mutiple iterations of the same vehicles
    Veh1_Weight1, Veh1_Weight2, etc.
    """

    # TODO: create a loop through the input dictionary and assign to class

    def __init__(self, name, input_dict=None):
        self.name = str(name)
        self.type = "vehicle"   # class type for reference

        if input_dict != None:
            self.year = int(input_dict['year'])
            self.make = str(input_dict['make'])
            self.model = str(input_dict['model'])
            self.weight = float(input_dict['weight'])
            self.vin = str(input_dict['vin'])
            self.brake = float(input_dict['brake'])
            self.steer_ratio = float(input_dict['steer_ratio'])
            self.init_x_pos = float(input_dict['init_x_pos'])
            self.init_y_pos = float(input_dict['init_y_pos'])
            self.head_angle = float(input_dict['head_angle'])
            self.width = float(input_dict['width'])
            self.length = float(input_dict['length'])
            self.hcg = float(input_dict['hcg'])
            self.lcgf = float(input_dict['lcgf'])
            self.lcgr = float(input_dict['lcgr'])
            self.wb = float(input_dict['wb'])   # can calculate
            self.track = float(input_dict['track'])
            self.f_hang = float(input_dict['f_hang'])
            self.r_hang = float(input_dict['r_hang'])
            self.tire_d = float(input_dict['tire_d'])
            self.tire_w = float(input_dict['tire_w'])
            self.izz = float(input_dict['izz'])
            self.fwd = int(input_dict['fwd'])   # consolidate
            self.rwd = int(input_dict['rwd'])   # consolidate
            self.awd = int(input_dict['awd'])   # consolidate
            self.A = float(input_dict['A'])     # unused
            self.B = float(input_dict['B'])     # unused
            self.k = float(input_dict['k'])
            self.L = float(input_dict['L'])     # unused
            self.c = float(input_dict['c'])     # unused
            self.vx_initial = float(input_dict['vx_initial'])
            self.vy_initial = float(input_dict['vy_initial'])
            self.omega_z = float(input_dict['omega_z'])

            print(f'Vehicle inputs for {self.name} applied succesfully')

    def manual_specs(self):  # loop through lists above to create inputs
        for i in range(len(input_query)):
                userEntry = input(input_query[i])
                try:
                    setattr(self, veh_inputs[i], float(userEntry))  # convert to float if possible
                except:
                    setattr(self, veh_inputs[i], userEntry)
                print(f'{input_query[i]} = {userEntry}')

    def load_specs(self, filename):
        """ provide file name to .csv file with defined layout
            file must be located in "input" directory
            uses contents of csv to determine attributes for vehicle variables
            altering the key names will break functionality of the simulation
        """
        with open(os.path.join(os.getcwd(), "data", "input", filename)) as csvfile:
            readCSV = csv.reader(csvfile, delimiter=',')
            for row in readCSV:
                print(f'{row[0]} = {row[2]}')
                try:
                    setattr(self, row[1], float(row[2]))  # convert to float if possible
                except:
                    setattr(self, row[1], row[2])

    def input_dict(self):
        vehicle_input_dict = {"year":self.year,
        "make":self.make,
        "model":self.model,
        "weight":self.weight,
        "vin":self.vin,
        "brake":self.brake,
        "steer_ratio":self.steer_ratio,
        "init_x_pos":self ,
        "init_y_pos":self.init_y_pos,
        "head_angle":self.head_angle,
        "width":self.width,
        "length":self.length,
        "hcg":self.hcg,
        "lcgf":self.lcgf,
        "lcgr":self.lcgr,
        "wb":self.wb,
        "track":self.track,
        "f_hang":self.f_hang,
        "r_hang":self.r_hang,
        "tire_d":self.tire_d,
        "tire_w":self.tire_w,
        "izz":self.izz,
        "fwd":self.fwd,
        "rwd":self.rwd,
        "awd":self.awd,
        "A":self.A,
        "B":self.B,
        "k":self.k,
        "L":self.L,
        "c":self.c,
        "vx_initial":self.vx_initial,
        "vy_initial":self.vy_initial,
        "omega_z":self.omega_z}

        return vehicle_input_dict

    def time_inputs(self, time, throttle, brake, steer):
        """
        Driver inputs | time (s) | throttle (%) | braking (%) | steering (deg) |
        time step can be user defined, inputs will be interpolated to match dt for simulation
        user create data frame with the necessary columns
        """
        if len(time) == 0:
            print('Input data for time has zero length')
            print('No driver input applied to vehicle')
        else:
            inputdf = pd.DataFrame(list(zip(throttle, brake, steer)), columns = ['throttle', 'brake', 'steer'])
            t = list(np.arange(0, max(time) + dt_motion, dt_motion))  # create time array from 0 to max time in inputs, does not mean simulation will stop at this time_inputs
            df = pd.DataFrame()                                                           # create dataframe for vehicle input with interpolated values
            df['t'] = t
            inputdf['input_t'] = [round(num, 3) for num in time]
            df.t = df.t.round(3)
            df = pd.merge(df, inputdf, how = 'left', left_on = 't', right_on = 'input_t') # merge input data with time data at specified time step
            df = df.interpolate(method = 'linear', axis = 0) # interpolate NaN values left after merging
            df.drop(columns = ['input_t', 't'], inplace = True)  # drop input time column
            df['t'] = t # reset time column due to interpolating
            df['t'] = df.t.round(3) # reset signficant digits
            df = df.reset_index(drop = True)
            self.driver_input = df
            print(f'Driver inputs applied to {self.name}')
            plot_driver_inputs(self)

    def read_time_inputsCSV(self, filename):
        """
        Driver inputs | time (s) | throttle (%) | brake (%) | steer (deg) |
        time step can be user defined, inputs will be interpolated to match dt for simulation
        reads data from csv file
        will override other inputs applied to vehicle
        """
        header_list = ["time", "throttle", "brake", "steer"]
        if os.path.isfile(filename):
            time_inputs = pd.read_csv(filename, skiprows=1, header=None, names = header_list)
            time_inputs = time_inputs.astype(float)
            if len(time_inputs) == 0:
                print('Time input file appears blank')
            else:
                t = list(np.arange(0, dt_motion+time_inputs.loc[len(time_inputs.time)-1, 'time'], dt_motion))  # create time array from 0 to max time in inputs, this will be end time for simulation
                df = pd.DataFrame()                                                           # create dataframe for vehicle input with interpolated values
                df['t'] = t
                time_inputs['input_t'] = time_inputs.time.round(3)
                df.t = df.t.round(3)
                df = pd.merge(df, time_inputs, how = 'left', left_on = 't', right_on = 'input_t') # merge input data with time data at specified time step
                df = df.interpolate(method = 'linear') # interpolate NaN values left after merging
                df.drop(columns = ['input_t', 't'], inplace = True)  # drop input time column
                df['t'] = t # reset time column due to interpolating
                df['t'] = df.t.round(3) # reset signficant digits
                df = df.reset_index(drop = True)
                self.driver_input = df
                print(f'Driver inputs applied to {self.name}')
        else:
            print('No Time Input File Provided')

        plot_driver_inputs(self)

    def plot_driver_inputs(self):
            plot_driver_inputs(self)

    # TODO: create ability to change inputs by distance
    def dist_inputs(self, filename):
        """
        Driver inputs | vehicle travel distance (ft) | brake (%) | steer (deg) |
        will override other inputs applied to vehicle
        """

    def __repr__(self):
        for attr, value in self.__dict__.items():
                if isinstance(value, pd.DataFrame):
                    print(f"{attr}:")
                    print(value.head())
                else:
                    return str(attr) "=" str(value)
