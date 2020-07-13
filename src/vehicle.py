# TODO: check properties of each input - use list of data types
# TODO: option to save inputs and outputs to csv

# %% modules
import matplotlib.pyplot as plt
from matplotlib.pyplot import text
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

mu_max = float(cons['mu_max'])    # maximum available friction
dt_motion = float(cons['dt_motion'])            # iteration time step

print('Current values for defined constants:')
print(f'maximum available friction (mu_max) = {mu_max}')
print(f'time step for vehicle motion (dt) = {dt_motion} s')

# TODO: create input for figure size - loads from "defaults" folder?
figure_size = (16,9)

# %% Create Classes for Project and Vehicles

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
"omega_z"]




class Vehicle:
    """
    Vehicle - contains all data assigned to a vehicle used to run various simulations
    not all values are required to create a vehicle instance
    requires 'Name' - used to idenify vehicle in simulations
    can be useful to create mutiple iterations of the same vehicles
    Veh1_Weight1, Veh1_Weight2, etc.
    """

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
            self.v_width = float(input_dict['v_width'])
            self.v_length = float(input_dict['v_length'])
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
            self.driver_input = input_dict['driver_input']    # dataframe (t | brake | steer)

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
        "v_width":self.v_width,
        "v_length":self.v_length,
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

    def time_inputs(self, time, brake, steer):
        """
        Driver inputs | time (s) | throttle (%) | braking (%) | steering (deg) |
        time step can be user defined, inputs will be interpolated to match dt for simulation
        user create data frame with the necessary columns
        """
        if len(time) == 0:
            print('Input data for time has zero length')
            print('No driver input applied to vehicle')
        else:
            inputdf = pd.DataFrame(list(zip(brake, steer)), columns = ['throttle', 'brake', 'steer'])
            t = list(np.arange(0, max(time)+dt_motion, dt_motion))  # create time array from 0 to max time in inputs, does not mean simulation will stop at this time_inputs
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
                print(f'Driver inputs applied as {self.name}.driver_input')
        else:
            print('No Time Input File Provided')

    def dist_inputs(self, filename):
        """
        Driver inputs | vehicle travel distance (ft) | brake (%) | steer (deg) |
        will override other inputs applied to vehicle
        """

    def impact_point(self):
        """
        generates a point in vehicle 1 (striking) reference frame
        sideswipe collisions - px, py will determine the extent of vehcle engagement with respect
        to contacting edge in vehicle 2 (struck)
        impact momentum model - px, py will be used along with the impact plane to determine time
        of impact and direction of normal and tangential contact planes
        """
        # set impact edge to zero
        self.edgeimpact = 0

        # test for required inputs
        if not self.lcgf:
            self.lcgf = float(input("Enter CG to front axle (ft)"))

        if not self.lcgr:
            self.lcgr = float(input("Enter CG to rear axle (ft)"))

        if not self.f_hang:
            self.f_hang = float(input("Enter front overhang (ft)"))

        if not self.r_hang:
            self.r_hang = float(input("Enter rear overhang (ft)"))

        if not self.v_width:
            self.v_width = float(input("Enter vehicle width (ft)"))

        # create figure of vehicle 1 with scale / grid and p1, p2, p3, p4 labeled when function is called
        # option 5 = custom location

        # x,y coordinates of vehicle outline:
        # left front corner
        self._b_lfc_x = self.lcgf + self.f_hang
        self._b_lfc_y = -1 * self.v_width / 2
        # right front corner
        self._b_rfc_x = self.lcgf + self.f_hang
        self._b_rfc_y = self.v_width / 2
        # right rear corner
        self._b_rrc_x = -1 * self.lcgr - self.r_hang
        self._b_rrc_y = self.v_width / 2
        # left rear corner
        self._b_lrc_x = -1 * self.lcgr - self.r_hang
        self._b_lrc_y = -1* self.v_width / 2

        bdy_x = (self._b_lfc_x, self._b_rfc_x, self._b_rrc_x, self._b_lrc_x, self._b_lfc_x)
        bdy_y = (self._b_lfc_y, self._b_rfc_y, self._b_rrc_y, self._b_lrc_y, self._b_lfc_y)

        # generate plot to show vehicle outline and default points for impact
        plt.figure(figsize=figure_size)
        plt.xlim([self._b_lrc_x * 1.5, self._b_lfc_x * 1.5])

        # adjust y axis length to keep aspect ratio defined in figure size
        x_axis_length = self._b_lfc_x * 1.5 - self._b_lrc_x * 1.5
        plt.ylim([-0.5 * x_axis_length * figure_size[1] / figure_size[0],
                0.5 * x_axis_length * figure_size[1] / figure_size[0]])

        plt.plot(bdy_x, bdy_y, 'k')  # body outline
        plt.scatter(bdy_x, bdy_y, c = 'r', s = 300)  # corner points
        plt.scatter(0, 0, c = 'g', s = 500)

        plt.text(self._b_lfc_x * 1.2, self._b_lfc_y, "1", horizontalalignment = 'right', size = 22)
        plt.text(self._b_rfc_x * 1.2, self._b_rfc_y, "2", horizontalalignment = 'right', size = 22)
        plt.text(self._b_rrc_x * 1.15, self._b_rrc_y, "3", horizontalalignment = 'left', size = 22)
        plt.text(self._b_lrc_x * 1.15, self._b_lrc_y, "4", horizontalalignment = 'left', size = 22)

        plt.text(1, -1, "CG", horizontalalignment = 'center', size = 22)
        plt.arrow(0, 0, 5, 0, head_width=.5, head_length=0.5, fc='k', ec='k')     # vehicle axes
        plt.arrow(0, 0, 0, 5, head_width=.5, head_length=0.5, fc='b', ec='b')     # vehicle axes
        plt.gca().invert_yaxis()
        plt.show(block = False)


        impact_option = int(input("Choose option for impact point (1, 2, 3, 4, custom = 99"))

        if impact_option not in [1, 2, 3, 4, 99]:
            print("Invalid impact point option - enter 1, 2, 3, 4 or 5")
            impact_option = int(input("Choose option for impact location"))
        elif impact_option != 99:
            if impact_option == 1:
                self.pimpact_x = self.lcgf + self.f_hang
                self.pimpact_y = -1 * self.v_width / 2
            elif impact_option == 2:
                self.pimpact_x = self.lcgf + self.f_hang
                self.pimpact_y = self.v_width / 2
            elif impact_option == 3:
                self.pimpact_x = -1 * self.lcgr - self.r_hang
                self.pimpact_y = self.v_width / 2
            elif impact_option == 4:
                self.pimpact_x = -1 * self.lcgr - self.r_hang
                self.pimpact_y = -1* self.v_width / 2
        elif impact_option == 99:
            self.pimpact_x = float(input("Enter x-coordinate of impact point in vehicle frame (ft):"))
            self.pimpact_y = float(input("Enter y-coordinate of impact point in vehicle frame (ft):"))

    def impact_edge(self):
        """
        generates an edge in vehicle 2 (struck) reference frame
        sideswipe collisions - edge will determine the extent of vehcle engagement with respect
        to contacting point in vehicle 1 (striking)
        impact momentum model - impact edge will be used along with the impact plane to determine time
        of impact
        """
        # test for required inputs
        if not self.lcgf:
            self.lcgf = float(input("Enter CG to front axle (ft)"))

        if not self.lcgr:
            self.lcgr = float(input("Enter CG to rear axle (ft)"))

        if not self.f_hang:
            self.f_hang = float(input("Enter front overhang (ft)"))

        if not self.r_hang:
            self.r_hang = float(input("Enter rear overhang (ft)"))

        if not self.v_width:
            self.v_width = float(input("Enter vehicle width (ft)"))

        # create figure of vehicle 1 with scale / grid and p1, p2, p3, p4 labeled when function is called
        # option 5 = custom location

        # x,y coordinates of vehicle outline:
        # left front corner
        self._b_lfc_x = self.lcgf + self.f_hang
        self._b_lfc_y = -1 * self.v_width / 2
        # right front corner
        self._b_rfc_x = self.lcgf + self.f_hang
        self._b_rfc_y = self.v_width / 2
        # right rear corner
        self._b_rrc_x = -1 * self.lcgr - self.r_hang
        self._b_rrc_y = self.v_width / 2
        # left rear corner
        self._b_lrc_x = -1 * self.lcgr - self.r_hang
        self._b_lrc_y = -1* self.v_width / 2

        bdy_x = (self._b_lfc_x, self._b_rfc_x, self._b_rrc_x, self._b_lrc_x, self._b_lfc_x)
        bdy_y = (self._b_lfc_y, self._b_rfc_y, self._b_rrc_y, self._b_lrc_y, self._b_lfc_y)

        # generate plot to show vehicle outline and default points for impact
        plt.figure(figsize=figure_size)
        plt.xlim([self._b_lrc_x * 1.5, self._b_lfc_x * 1.5])

        # adjust y axis length to keep aspect ratio defined in figure size
        x_axis_length = self._b_lfc_x * 1.5 - self._b_lrc_x * 1.5
        plt.ylim([-0.5 * x_axis_length * figure_size[1] / figure_size[0],
                0.5 * x_axis_length * figure_size[1] / figure_size[0]])

        plt.plot(bdy_x[:2], bdy_y[:2], 'k')
        plt.plot(bdy_x[1:3], bdy_y[1:3], 'b')
        plt.plot(bdy_x[2:4], bdy_y[2:4], 'g')
        plt.plot(bdy_x[3:5], bdy_y[3:5], 'orange')
        plt.scatter(0, 0, c = 'g', s = 500)

        plt.text(self._b_lfc_x * 1.2, 0, "1", horizontalalignment = 'right', size = 22)
        plt.text(-2, 1.2 * self.v_width / 2, "2", horizontalalignment = 'center', size = 22)
        plt.text(self._b_rrc_x * 1.2, 0, "3", horizontalalignment = 'left', size = 22)
        plt.text(-2, -1.2 * self.v_width / 2, "4", horizontalalignment = 'center', size = 22)

        plt.text(1, -1, "CG", horizontalalignment = 'center', size = 22)
        plt.arrow(0, 0, 5, 0, head_width=.5, head_length=0.5, fc='k', ec='k')     # vehicle axes
        plt.arrow(0, 0, 0, 5, head_width=.5, head_length=0.5, fc='b', ec='b')     # vehicle axes

        plt.gca().invert_yaxis()
        plt.show(block=False)

        impact_option = int(input("Choose option for impact edge"))

        if impact_option not in [1, 2, 3, 4]:
            raise ValueError("Invalid impact edge option - enter 1, 2, 3, 4")
        else:
            if impact_option == 1:
                self.edgeimpact = 1
                self.edgeimpact_x1 = self.lcgf + self.f_hang
                self.edgeimpact_y1 = -1 * self.v_width / 2
                self.edgeimpact_x2 = self.lcgf + self.f_hang
                self.edgeimpact_y2 = self.v_width / 2
            elif impact_option == 2:
                self.edgeimpact = 2
                self.edgeimpact_x1 = self.lcgf + self.f_hang
                self.edgeimpact_y1 = self.v_width / 2
                self.edgeimpact_x2 = -1 * self.lcgr - self.r_hang
                self.edgeimpact_y2 = self.v_width / 2
            elif impact_option == 3:
                self.edgeimpact = 3
                self.edgeimpact_x1 = -1 * self.lcgr - self.r_hang
                self.edgeimpact_y1 = self.v_width / 2
                self.edgeimpact_x2 = -1 * self.lcgr - self.r_hang
                self.edgeimpact_y2 = -1* self.v_width / 2
            elif impact_option == 4:
                self.edgeimpact = 4
                self.edgeimpact_x1 = -1 * self.lcgr - self.r_hang
                self.edgeimpact_y1 = -1 * self.v_width / 2
                self.edgeimpact_x2 = self.lcgf + self.f_hang
                self.edgeimpact_y2 = -1 * self.v_width / 2
