from copy import deepcopy
import csv
import os

# load constants
with open(os.path.join(os.getcwd(), "data", "input", "constants.csv")) as csvfile:
    readCSV = csv.reader(csvfile, delimiter=',')
    cons = {}
    for row in readCSV:
        cons[row[1]] = float(row[2])

mu_max = cons['mu_max']    # maximum available friction
dt = cons['dt']            # iteration time step


class Sideswipe():
    """
    performs vehicle motion analysis along with sideswipe simulations
    requires impact point for striking vehicle (Vehicle 1) and impacting
    edge in struck vehicle (Vehicle 2)
    """
    def __init__(self,veh1, veh2, model_inputs = None):
        self.__dt = 0.0001              # TODO: default time step for collisions - create input for this
        self.type = "sideswipe"         # class type
        # create independent copy of vehicle class instances
        self.veh1 = deepcopy(veh1)
        self.veh2 = deepcopy(veh2)

        # manually create inputs if not provided
        if (model_inputs == None):
            self.name = input('Enter name of Sideswipe model run:')
            self.cor = float(input('Coefficient of restitution:'))
            self.cof = float(input('Intervehicular coefficient of friction:'))
            self.k = input('Provide a single value or dataframe for mutual stiffness [lb/in]:')
            self.tstop = float(input('Enter cut-off time (tstop (s)) to stop simulation or "None" to run simulation up to seperation:'))
        else:
            self.name = model_inputs['name']
            self.cor = model_inputs['cor']
            self.cof = model_inputs['cof']
            self.k = model_inputs['k']
            self.tstop = model_inputs['tstop']

        print("------------ Model Inputs ---------------")
        print(f"Sideswipe Run = {self.name}")
        print(f"Coefficient of Restitution = {self.cor}")
        print(f"Intervhicular coefficient of festitution = {self.cor}")

        if (isinstance(self.k, int)) or (isinstance(self.k, float)):
            print(f"Constant Mutual Stiffness = {self.k} lb/in ")
            self.__ktype = 'constantK'               # define stiffness type for model
        elif isinstance(self.k, pd.DataFrame):
            print(f"Stiffness Function Dataframe of shape = {self.k.shape}")
            self.__ktype = 'tableK'                   # define stiffness type for model

        if (isinstance(self.tstop, int)) or (isinstance(self.tstop, float)):
            print(f"Model will run until t = {self.tstop} seconds")
            self.__ttype = 1                           # define t stop criteria
        elif (self.tstop == None):
            print("No stop time provided - model will run until vehicle seperation")
            self.__ttype = 0                           # define t stop criteria
        else:
            print('Something other than a number or "None" used for stop time - model will run until vehicle seperation')
            self.__ttype = 0                           # define t stop criteria

        # collect vehicle specific inputs

        print("")
        print("|------------ Vehicle Inputs -----------|")

        print("")
        print("<- Vehicle 1 ->")
        print("")

        if len(self.veh1.driver_input.t) == 0:
            print('Input data for time has zero length')
            print('No driver input applied to Vehicle 1')


        print("")
        print("<- Vehicle 2 ->")
        print("")

        if len(self.veh2.driver_input.t) == 0:
            print('Input data for time has zero length')
            print('No driver input applied to Vehicle 2')

        # TODO: plot driver inputs for vehicles
        # TODO: plot vehicle motion without creating impact - allow for change to initial position

        print("|----------- Input Complete ------------|")
        print("")

        model_results = sideswipe_model(W1 = self.veh1.weight,
                                        v1x_initial = self.veh1.vx_initial,
                                        v1y_initial = self.veh1.vy_initial,
                                        v1_xpos = self.veh1.init_x_pos,
                                        v1_ypos = self.veh1.init_y_pos,
                                        v1_head_angle = self.veh1.head_angle,
                                        v1_input_time = self.veh1.driver_input.t,
                                        v1_brake = self.veh1.driver_input.brake,
                                        v1_steer = self.veh1.driver_input.steer,
                                        v1_steer_ratio = self.veh1.steer_ratio,
                                        W2 = self.veh2.weight,
                                        v2x_initial = self.veh2.vx_initial,
                                        v2y_initial = self.veh2.vy_initial,
                                        v2_xpos = self.veh2.init_x_pos,
                                        v2_ypos = self.veh2.init_y_pos,
                                        v2_head_angle = self.veh2.head_angle,
                                        v2_input_time = self.veh2.driver_input.t,
                                        v2_brake = self.veh2.driver_input.brake,
                                        v2_steer = self.veh2.driver_input.steer,
                                        v2_steer_ratio = self.veh2.steer_ratio,
                                        k = self.k,
                                        cor = self.cor,
                                        cof = self.cof,
                                        tstop = self.tstop,
                                        ktype = self.__ktype,
                                        ttype = self.__ttype,
                                        dt = self.__dt)

def sideswipe_model(veh1, veh2, input_dict):
        """
        modify vehicle motion to accept forces
        """
