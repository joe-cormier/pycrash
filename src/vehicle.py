from tabulate import tabulate
from itertools import count
import inspect 
import os
import csv

# %% Create Classes for Project and Vehicles
input_query = ["Vehicle Identification Number (VIN)"
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
"Damage length L [in]"
"Crush depth c [in]"
"Initial forward velocity Vx (mph)",
"Initial lateral velocity Vy (mph)",
"Initial X position (ft)",
"Initial Y position (ft)",
"Initial heading angle (deg)"]

veh_inputs = ["vin"
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
        self.year = int(input("Model Year: "))
        self.make = input("Vehicle Make: ")
        self.model = input("Vehicle Model: ")
        self.weight = float(input("Vehicle Weight (lb): "))

        print(tabulate([["Vehicle", "Year", "Make", "Model", "Weight"],
                    [self.name, self.year, self.make, self.model, self.weight]]))

    def manual_input(self):  # loop through lists above to create inputs
        for i in range(len(input_query)):
                userEntry = input(input_query[i])
                setattr(self, veh_inputs[i], userEntry)
                print(f'{input_query[i]} = {userEntry}')

    def load_input(self, filename):
        """ provide path and file name to .csv file with defined layout 
            uses contents of csv to determine attributes for vehicle variables
            altering the key names will break functionality of the simulation  """
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