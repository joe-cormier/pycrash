from tabulate import tabulate
from itertools import count
import pickle
from os import path
import os
import csv

# not sure how to ensure the pather will always be correct
path_parent = os.path.dirname(os.getcwd())
data_directory = os.path.join(path_parent, "data")

#  Create Classes for Project and Vehicles
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
"A",
"B",
"k",
"Initial velocity (mph)"]

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
"v_initial"]


# Create Project
class Project:
    """
    """

    def __init__(self):
        self.pname = input("Project Name: ")
        self.pdesc = input("Project Description: ")
        self.sim_type = input("Simulation Type [Single Vehicle = SV/ Multi-Vehicle = MV]: ")

        if self.sim_type == "MV":
            self.impact_type = input("Impact Type (SS, IMPC, SDOF): ")

            if (self.impact_type not in ["SS", "IMPC", "SDOF"]):
                print("Not a valid impact type, choose SS, IMPC or SDOF. Value set to SDOF")
                self.impact_type == "SDOF"
        else:
            self.impact_type = "none"

        self.note = input("Note: ")

        print(tabulate([["Project", "Description", "Impact Type", "Simulation Type", "Note"],
                    [self.pname, self.pdesc, self.impact_type, self.sim_type, self.note]]))

    def show(self):
        print(tabulate([["Project", "Description", "Impact Type", "Simulation Type", "Note"],
                         [self.pname, self.pdesc, self.impact_type, self.sim_type, self.note]]))


    # TODO: add vehicles to project?
    #def add_vehicles(vehicle_list)

# Create vehicle class
class Vehicle:
    """requires 'Name' - used to idenify vehicle in simulations
    can be useful to create mutiple iterations of the same vehicles
    Veh1_W1, Veh1_W2, etc.
    """

    _vehCount = count(0)

    def __init__(self, name):
        self.name = name
        self.year = int(input("Model Year: "))
        self.make = input("Vehicle Make: ")
        self.model = input("Vehicle Model: ")
        self.weight = float(input("Vehicle Weight (lb): "))
        self._vehCount = next(self._vehCount)

        print(tabulate([["Vehicle", "Year", "Make", "Model", "Weight"],
                    [self.name, self.year, self.make, self.model, self.weight]]))

    def manual_input(self):  # loop through lists above to create inputs
        for i in range(len(input_query)):
                userEntry = input(input_query[i])
                setattr(self, veh_inputs[i], userEntry)
                print(f'{input_query[i]} = {userEntry}')

    def load_input(self, filename):
        """ provide path and file name to .csv file with defined layout
            uses contents of csv to determine attributes for vehicle variable
            altering these values will break functionality of the simulation  """
        with open(filename) as csvfile:
            readCSV = csv.reader(csvfile, delimiter=',')
            for row in readCSV:
                print(f'{row[0]} = {row[2]}')
                setattr(self, row[1], row[2])


# Function for saving project and vehicle objects

def save_project(project, vehicle1, vehicle2):
    """ save project to filename along with vehicles of Class Vehicle
    Will append the current project to the prexisting dataset if it exists
    """

    project_data = [project, vehicle1, vehicle2]

    # test if ProjectData.pkl exists
    if path.exists(os.path.join(data_directory, "project", "ProjectData.pkl")) == True:
        with open('ProjectData.pkl', 'rb') as handle:
            allProjectData = pickle.load(handle)
        # add new project to data file
        allProjectData[project.pname] = project_data
    elif path.exists(os.path.join(data_directory, "project", "ProjectData.pkl")) == False:
        # create new file for saving project data
        allProjectData = {}
        allProjectData[project.pname] = project_data

    with open(os.path.join(data_directory, "project", "ProjectData.pkl"), 'wb') as handle:
        pickle.dump(allProjectData, handle, protocol=pickle.HIGHEST_PROTOCOL)


# Read project data
def load_project(project):
    with open(os.path.join(data_directory, "project", "ProjectData.pkl"), 'rb') as handle:
        allProjectData = pickle.load(handle)
        project_data = allProjectData[project]
    return project_data[0], project_data[1], project_data[2]


# create vehicle motion

# TODO: add vehicles to planar motion, plot motion for each vehicle added?

class PlanarMotion(vehicle):
    def __init__(self):
        pass

    # TODO: save data to pick and a csv file
    # def

    def get_count(self):
        print(Vehicle.veh_count)

# create vehicle motion
# TODO: add vehicles to planar motion, plot motion for each vehicle added?
class PlanarMotion(vehicle):
    def __init__(self):
        pass
