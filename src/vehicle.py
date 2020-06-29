from tabulate import tabulate
from itertools import count
import pandas as pd
import numpy as np
import inspect
import os
import csv

# load constants
with open(os.path.join(os.getcwd(), "data", "input", "constants.csv")) as csvfile:
    readCSV = csv.reader(csvfile, delimiter=',')
    cons = {}
    for row in readCSV:
        cons[row[1]] = float(row[2])
print('Current values for defined constants:')
print(cons)
mu_max = cons['mu_max']    # maximum available friction
dt = cons['dt']           # iteration time step


# %% Create Classes for Project and Vehicles
input_query = ["Model year",
"Vehicle make",
"Vehicle model",
"Vehicle weight (lb)",
"Vehicle Identification Number (VIN)",
"Percent Braking",
"Steering ratio",
"Initial X position (ft)",
"Initial Y position (ft)",
"Heading angle (deg)",
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
"Izz (slug - ft^2)",
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
"Initial X position (ft)",
"Initial Y position (ft)",
"Initial heading angle (deg)"]

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
"v_width",
"v_length",
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
"x_pos",
"y_pos",
"head_angle"]



# Create vehicle class
class Vehicle:
    """requires 'Name' - used to idenify vehicle in simulations
    can be useful to create mutiple iterations of the same vehicles
    Veh1_W1, Veh1_W2, etc.
    """

    def __init__(self, name):
        self.name = name
        self.type = "vehicle" # class type
#        self.year = int(input("Model Year: "))
#        self.make = input("Vehicle Make: ")
#        self.model = input("Vehicle Model: ")
#        self.weight = float(input("Vehicle Weight (lb): "))

#        print(tabulate([["Vehicle", "Year", "Make", "Model", "Weight"],
#                    [self.name, self.year, self.make, self.model, self.weight]]))

    def manual_specs(self):  # loop through lists above to create inputs
        for i in range(len(input_query)):
                userEntry = input(input_query[i])
                setattr(self, veh_inputs[i], userEntry)
                print(f'{input_query[i]} = {userEntry}')

    def load_specs(self, filename):
        """ provide path and file name to .csv file with defined layout
            uses contents of csv to determine attributes for vehicle variables
            altering the key names will break functionality of the simulation
        """
        with open(filename) as csvfile:
            readCSV = csv.reader(csvfile, delimiter=',')
            for row in readCSV:
                print(f'{row[0]} = {row[2]}')
                setattr(self, row[1], row[2])

    def show(self):
        """ display all attributes assigned to the vehicle """
        for i in inspect.getmembers(self):
            if not i[0].startswith('_'):
                if not inspect.ismethod(i[1]):
                    print(i)

    def time_inputs(self, time, brake, steer):
        """
        Driver inputs | time (s) | braking (%) | steering (%) |
        time step can be user defined, inputs will be interpolated to match dt for simulation
        user create data frame with the necessary columns
        """
        if len(time) == 0:
            print('Input data for time has zero length')
            print('No driver input applied to vehicle')
        else:
            inputdf = pd.DataFrame(list(zip(brake, steer)), columns = ['brake', 'steer'])
            t = list(np.arange(0, max(time)+dt, dt))  # create time array from 0 to max time in inputs, does not mean simulation will stop at this time_inputs
            df = pd.DataFrame()                                                           # create dataframe for vehicle input with interpolated values
            df['t'] = t
            inputdf['input_t'] = time.round(3)
            df.t = df.t.round(3)
            df = pd.merge(df, inputdf, how = 'left', left_on = 't', right_on = 'input_t') # merge input data with time data at specified time step
            df = df.interpolate(method = 'linear') # interpolate NaN values left after merging
            df.drop(columns = ['input_t', 't'], inplace = True)  # drop input time column
            df['t'] = t # reset time column due to interpolating
            df['t'] = df.t.round(3) # reset signficant digits
            df = df.reset_index(drop = True)
            self.driver_input = df
            print('Driver inputs applied as "driver_input"')

    def read_time_inputsCSV(self, filename):
        """
        Driver inputs | time (s) | braking (%) | steering (%) |
        time step can be user defined, inputs will be interpolated to match dt for simulation
        reads data from csv file
        will override other inputs applied to vehicle
        """
        if os.path.isfile(filename):
            time_inputs = pd.read_csv(filename)
            if len(time_inputs) == 0:
                print('Time input file appears blank')
            else:
                t = list(np.arange(0, dt+time_inputs.loc[len(time_inputs.time)-1, 'time']), dt)  # create time array from 0 to max time in inputs, does not mean simulation will stop at this time_inputs
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
                print('Driver inputs applied as "driver_input"')
        else:
            print('No Time Input File Provided')

    def dist_inputs(self, filename):
        """
        Driver inputs | vehicle travel distance (ft) | braking (%) | steering (%) |
        will override other inputs applied to vehicle
        """
