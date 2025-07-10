from .visualization.vehicle import plot_driver_inputs
from . import tire as tire
import pandas as pd
import numpy as np
import os
import csv

project_dir = os.path.dirname(os.getcwd())
input_dir = os.path.join(project_dir, 'data', 'input')

# load defaults
sim_defaults = {'dt_motion': 0.01,
                'mu_max': 0.8,
                'alpha_max': 0.174533}

mu_max = sim_defaults['mu_max']  # maximum available friction
dt_motion = sim_defaults['dt_motion']  # iteration time step

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
               "Initial Yaw Rate (deg/s)",
               "Striking Vehicle? (True/False)",
               "notes"]

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
              "omega_z",
              "striking",
              "notes"]

class Vehicle:
    """
    Vehicle - contains all data assigned to a vehicle used to run various simulations
    not all values are required to create a vehicle instance
    requires 'Name' - used to identify vehicle in simulations
    """

    def __init__(self, name, input_dict=None):
        self.name = str(name)
        self.type = "vehicle"   # class type for reference
        self.model = None       # model will be created if used in impact simulation

        if input_dict != None:
            for key, value in input_dict.items():
                if key in veh_inputs:
                    if key in ['make', 'model', 'vin', 'notes']:
                        setattr(self, key, str(value))
                    elif key in ['fwd', 'rwd', 'awd']:
                        setattr(self, key, bool(value))
                    else:
                        setattr(self, key, float(value))
                else:
                    print(f"Input entry {key} unknown, setting to {value}")
                    setattr(self, key, float(value))

            print(f'Vehicle inputs for {self.name} applied successfully')

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
        vehicle_input_dict = {"year": self.year,
                              "make": self.make,
                              "model": self.model,
                              "weight": self.weight,
                              "vin": self.vin,
                              "brake": self.brake,
                              "steer_ratio": self.steer_ratio,
                              "init_x_pos": self.init_x_pos,
                              "init_y_pos": self.init_y_pos,
                              "head_angle": self.head_angle,
                              "width": self.width,
                              "length": self.length,
                              "hcg": self.hcg,
                              "lcgf": self.lcgf,
                              "lcgr": self.lcgr,
                              "wb": self.wb,
                              "track": self.track,
                              "f_hang": self.f_hang,
                              "r_hang": self.r_hang,
                              "tire_d": self.tire_d,
                              "tire_w": self.tire_w,
                              "izz": self.izz,
                              "fwd": self.fwd,
                              "rwd": self.rwd,
                              "awd": self.awd,
                              "A": self.A,
                              "B": self.B,
                              "k": self.k,
                              "L": self.L,
                              "c": self.c,
                              "vx_initial": self.vx_initial,
                              "vy_initial": self.vy_initial,
                              "omega_z": self.omega_z}

        return vehicle_input_dict

    def time_inputs(self, time, throttle, brake, steer, show_plot=True):
        """
        Driver inputs | time (s) | throttle (%) | braking (%) | steering (deg) |
        time step can be user defined, inputs will be interpolated to match dt for simulation
        user create data frame with the necessary columns
        """
        if len(time) == 0:
            print('Input data for time has zero length')
            print('No driver input applied to vehicle')
        else:
            inputdf = pd.DataFrame(list(zip(throttle, brake, steer)), columns=['throttle', 'brake', 'steer'])
            t = list(np.arange(0, max(time) + dt_motion,
                               dt_motion))  # create time array from 0 to max time in inputs, does not mean simulation will stop at this time_inputs
            t = [float(i) for i in t]
            df = pd.DataFrame()  # create dataframe for vehicle input with interpolated values
            df['t'] = t
            inputdf['input_t'] = [float(num) for num in time]
            df.t = df.t.round(3).astype(float)
            df = pd.merge(df, inputdf, how='left', left_on='t',
                          right_on='input_t')  # merge input data with time data at specified time step
            df = df.interpolate(method='linear', axis=0)  # interpolate NaN values left after merging
            df.drop(columns=['input_t', 't'], inplace=True)  # drop input time column
            df['t'] = t  # reset time column due to interpolating
            df['t'] = df.t.round(3)  # reset significant digits
            df = df.reset_index(drop=True)
            self.driver_input = df
            print(f'Driver inputs applied to {self.name}')
            if show_plot:
                plot_driver_inputs(self)

    def read_time_inputsCSV(self, filename):
        """
        Driver inputs | time (s) | throttle (%) | brake (%) | steer (deg) |
        time step can be user defined, inputs will be interpolated to match dt for simulation
        reads data from csv file
        will override other inputs applied to vehicle
        filename should include .csv - "example_file_name.csv"
        """
        header_list = ["time", "throttle", "brake", "steer"]
        if os.path.isfile(os.path.join(input_dir, filename)):
            time_inputs = pd.read_csv(os.path.join(input_dir, filename), skiprows=1, header=None, names=header_list)
            time_inputs = time_inputs.astype(float)
            if len(time_inputs) == 0:
                print('Time input file appears blank')
            else:
                t = list(np.arange(0, dt_motion + time_inputs.loc[len(time_inputs.time) - 1, 'time'],
                                   dt_motion))  # create time array from 0 to max time in inputs, this will be end time for simulation
                df = pd.DataFrame()  # create dataframe for vehicle input with interpolated values
                df['t'] = t
                time_inputs['input_t'] = time_inputs.time.round(3)
                df.t = df.t.round(3)
                df = pd.merge(df, time_inputs, how='left', left_on='t',
                              right_on='input_t')  # merge input data with time data at specified time step
                df = df.interpolate(method='linear')  # interpolate NaN values left after merging
                df.drop(columns=['input_t', 't'], inplace=True)  # drop input time column
                df['t'] = t  # reset time column due to interpolating
                df['t'] = df.t.round(3)  # reset signficant digits
                df = df.reset_index(drop=True)
                self.driver_input = df
                print(f'Driver inputs applied to {self.name}')
        else:
            print('No Time Input File Provided')

        plot_driver_inputs(self)

    def create_tires(self):
        """
        create each tire based on default settings
        will add inputs for percent / time to disable tire
        """
        setattr(self, 'tires', tire.create_tires(self, names=['lf', 'rf', 'rr', 'lr']))

    """
    Calculate tire forces
    - will require the model attribute assigned within impact_main class
    """
    def calc_tire_forces(self, i, sim_defaults):
        if i == 0:
            j = i
        else:
            j = i - 1  # tire forces based on prior time step

        # current steer angle
        self.model.delta_deg[i] = self.driver_input.steer[i] / self.steer_ratio  # steer angle (delta) will always be derived from driver input
        self.model.delta_rad[i] = self.model.delta_deg[i] * (np.pi / 180)        # net steer angle

        # ackerman steering
        self.model.lf_steer_angle[i], self.model.rf_steer_angle[i] = tire.ackerman_steer(i,
                                                                                         self.model.delta_rad[i],
                                                                                         self.wb,
                                                                                         self.track)

        # Forward / Rearward weight shift due to braking or acceleration
        veh_m = self.weight / 32.2
        self.model.lf_fz[i] = 0.5 * ((-veh_m * self.model.au[j] * self.hcg + self.weight * self.lcgr) / self.wb) + veh_m * self.model.av[j] * self.hcg / self.track
        self.model.rf_fz[i] = 0.5 * ((-veh_m * self.model.au[j] * self.hcg + self.weight * self.lcgr) / self.wb) - veh_m * self.model.av[j] * self.hcg / self.track
        self.model.rr_fz[i] = 0.5 * ((veh_m * self.model.au[j] * self.hcg + self.weight * self.lcgf) / self.wb) - veh_m * self.model.av[j] * self.hcg / self.track
        self.model.lr_fz[i] = 0.5 * ((veh_m * self.model.au[j] * self.hcg + self.weight * self.lcgf) / self.wb) + veh_m * self.model.av[j] * self.hcg / self.track

        # local tire velocities
        # left front
        self.model.lf_vx[i] = self.model.vx[j] + self.model.oz_rad[j] * (self.track / 2)
        self.model.lf_vy[i] = self.model.vy[j] + self.model.oz_rad[j] * self.lcgf
        # right front
        self.model.rf_vx[i] = self.model.vx[j] - self.model.oz_rad[j] * (self.track / 2)
        self.model.rf_vy[i] = self.model.vy[j] + self.model.oz_rad[j] * self.lcgf
        # right rear
        self.model.rr_vx[i] = self.model.vx[j] - self.model.oz_rad[j] * (self.track / 2)
        self.model.rr_vy[i] = self.model.vy[j] - self.model.oz_rad[j] * self.lcgr
        # left rear
        self.model.lr_vx[i] = self.model.vx[j] + self.model.oz_rad[j] * (self.track / 2)
        self.model.lr_vy[i] = self.model.vy[j] - self.model.oz_rad[j] * self.lcgr

        # tire forces
        # left front
        self.model.lf_lonf[i], self.model.lf_latf[i], self.model.lf_lock[i] = tire.tire_force(self.model.lf_vx[i],
                                                                                              self.model.lf_vy[i],
                                                                                              self.model.lf_fz[i],
                                                                                              self.model.lf_steer_angle[i] * self.tires['lf']['steer'],
                                                                                              self.driver_input.brake[i],
                                                                                              self.driver_input.throttle[i] * self.tires['lf']['drive'],
                                                                                              sim_defaults['alpha_max'],
                                                                                              sim_defaults['mu_max'])
        # right front
        self.model.rf_lonf[i], self.model.rf_latf[i], self.model.rf_lock[i] = tire.tire_force(self.model.rf_vx[i],
                                                                                              self.model.rf_vy[i],
                                                                                              self.model.rf_fz[i],
                                                                                              self.model.rf_steer_angle[i] * self.tires['rf']['steer'],
                                                                                              self.driver_input.brake[i],
                                                                                              self.driver_input.throttle[i] * self.tires['rf']['drive'],
                                                                                              sim_defaults['alpha_max'],
                                                                                              sim_defaults['mu_max'])
        # right rear
        self.model.rr_lonf[i], self.model.rr_latf[i], self.model.rr_lock[i] = tire.tire_force(self.model.rr_vx[i],
                                                                                              self.model.rr_vy[i],
                                                                                              self.model.rr_fz[i],
                                                                                              0,
                                                                                              self.driver_input.brake[i],
                                                                                              self.driver_input.throttle[i] * self.tires['rr']['drive'],
                                                                                              sim_defaults['alpha_max'],
                                                                                              sim_defaults['mu_max'])
        # left rear
        self.model.lr_lonf[i], self.model.lr_latf[i], self.model.lr_lock[i] = tire.tire_force(self.model.lr_vx[i],
                                                                                              self.model.lr_vy[i],
                                                                                              self.model.lr_fz[i],
                                                                                              0,
                                                                                              self.driver_input.brake[i],
                                                                                              self.driver_input.throttle[i] * self.tires['lr']['drive'],
                                                                                              sim_defaults['alpha_max'],
                                                                                              sim_defaults['mu_max'])

        # tire forces in vehicle frame
        self.model.lf_fx[i] = self.model.lf_lonf[i] * np.cos(self.model.delta_rad[i]) - self.model.lf_latf[i] * np.sin(self.model.delta_rad[i])
        self.model.lf_fy[i] = self.model.lf_lonf[i] * np.sin(self.model.delta_rad[i]) + self.model.lf_latf[i] * np.cos(self.model.delta_rad[i])
        # Right Front Tire #
        self.model.rf_fx[i] = self.model.rf_lonf[i] * np.cos(self.model.delta_rad[i]) - self.model.rf_latf[i] * np.sin(self.model.delta_rad[i])
        self.model.rf_fy[i] = self.model.rf_lonf[i] * np.sin(self.model.delta_rad[i]) + self.model.rf_latf[i] * np.cos(self.model.delta_rad[i])
        # Right Rear Tire #
        self.model.rr_fx[i] = self.model.rr_lonf[i]
        self.model.rr_fy[i] = self.model.rr_latf[i]
        # Left Rear Tire #
        self.model.lr_fx[i] = self.model.lr_lonf[i]
        self.model.lr_fy[i] = self.model.lr_latf[i]

    def plot_driver_inputs(self):
        plot_driver_inputs(self)

    def show(self):
        for key in self.__dict__.keys():
            if isinstance(self.__dict__[key], pd.DataFrame):
                print("")
                print(f"First five rows of {key}:")
                print(self.__dict__[key].head())
            else:
                print(f"{key} -> {self.__dict__[key]}")
