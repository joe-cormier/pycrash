import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
from .sdof_calculations import SingleDOFmodel
from copy import deepcopy
import inspect
import csv
import os

class SDOF_Model():
    """
    Inputs can be provided using a predefined dictionary "model_inputs"

    or inputs can be entered through user prompts
    if "None" is used for tstop model will run until vehicles seperate otherwise
    model will run to tstop if seperation has ocurred
    if a single value is used for model stiffness k, vehicle response will be
    calculated using a constant stiffness
    if a dataframe with 2 columns is entered [disp(ft) | force(lb)],
    vehicle response will be calculated using dataframe as a lookup table
    for force at a given displacement
    """

    def __init__(self, veh1, veh2, model_inputs=None):
        self.type = "sdof"        # class type
        # create independent copy of vehicle class instances
        self.veh1 = deepcopy(veh1)
        self.veh2 = deepcopy(veh2)
        # manually create inputs if not provided
        if (model_inputs == None):
            self.name = input('Enter name of SDOF model run:')
            self.cor = float(input('Provide a coefficient of restitution:'))
            self.k = input('Provide a single value or dataframe for mutual stiffness [lb/in]:')
            self.tstop = float(input('Enter cut-off time (tstop (s)) to stop simulation or "None" to run simulation up to seperation:'))
        else:
            self.name = model_inputs['name']
            self.cor = model_inputs['cor']
            self.k = model_inputs['k']
            self.tstop = model_inputs['tstop']

        print("")
        print("------------ Model Inputs ---------------")
        print(f"Model Run = {self.name}")
        print(f"Coefficient of Restitution = {self.cor}")
        if (isinstance(self.k, int)) or (isinstance(self.k, float)):
            print(f"Constant Mutual Stiffness = {self.k} lb/ft ")
            self.__ktype = 'constantK'               # define stiffness type for model
        elif isinstance(self.k, pd.DataFrame):
            print(f"Stiffness Function Dataframe [disp (ft) | force (lb)] of shape = {self.k.shape}")
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
        try:
            if (isinstance(self.veh1.brake, int)) or (isinstance(self.veh1.brake, float)):
                print(f"{self.veh1.name} braking at {self.veh1.brake*100}%")
            else:
                print(f"{self.veh1.name} does not have a valid 'brake' entry")
                print(f"{self.veh1.name} - braking  set to 0 %")
                self.veh1.brake = 0
        except AttributeError:
            print(f"Braking not defined for {self.veh1.name} - value set to 0 %")
            self.veh1.brake = 0

        try:
            if (isinstance(self.veh1.vx_initial, int)) or (isinstance(self.veh1.vx_initial, float)):
                print(f"{self.veh1.name} initial speed is {self.veh1.vx_initial} mph")
            else:
                print(f"{self.veh1.name} does not have a valid initial forward velocity entry")
                print(f"{self.veh1.name} - velocity set to 0 mph")
                self.veh1.vx_initial = 0
        except AttributeError:
            print(f"Initial forward speed not defined for {self.veh1.name} - value set to 0 mph")
            self.veh1.vx_initial = 0

        print("")
        print("<- Vehicle 2 ->")
        print("")
        try:
            if (isinstance(self.veh2.brake, int)) or (isinstance(self.veh2.brake, float)):
                print(f"{self.veh2.name} braking at {self.veh2.brake*100}%")
            else:
                print(f"{self.veh2.name} does not have a valid 'brake' entry")
                print(f"{self.veh2.name} - braking  set to 0 %")
                self.veh2.brake = 0
        except AttributeError:
            print(f"Braking not defined for {self.veh2.name} - value set to 0 %")
            self.veh2.brake = 0

        try:
            if (isinstance(self.veh2.vx_initial, int)) or (isinstance(self.veh2.vx_initial, float)):
                print(f"{self.veh2.name} initial speed is {self.veh2.vx_initial} mph")
            else:
                print(f"{self.veh2.name} does not have a valid initial forward velocity entry")
                print(f"{self.veh2.name} - velocity set to 0 mph")
                self.veh2.vx_initial = 0
        except AttributeError:
            print(f"Initial forward speed not defined for {self.veh2.name} - value set to 0 mph")
            self.veh2.vx_initial = 0

        print(f"Model Closing Speed = {self.veh1.vx_initial - self.veh2.vx_initial} mph")
        print("")
        print("|----------- Input Complete ------------|")
        print("")

    #  Run SDOF Model
        self.model_result = SingleDOFmodel(W1 = self.veh1.weight,
                                        v1_initial = self.veh1.vx_initial,
                                        v1_brake = self.veh1.brake,
                                        W2 = self.veh2.weight,
                                        v2_initial = self.veh2.vx_initial,
                                        v2_brake = self.veh2.brake,
                                        k = self.k,
                                        cor = self.cor,
                                        tstop = self.tstop,
                                        ktype = self.__ktype,
                                        ttype = self.__ttype
                                        )

        # TODO: create attribute for vehicle inputs for saving / plotting run

    def input_dict(self):
        """
        return a dictionary to save / modify inputs
        """
        return {"name":self.name,
                "k":self.k,
                "cor":self.cor,
                "tstop":self.__ttype
                }

    def show(self):
        """ display all attributes assigned to the sdof model """
        for i in inspect.getmembers(self):
            if not i[0].startswith('_'):
                if not inspect.ismethod(i[1]):
                    print(i)

    def plot_fdx(self):
        """
        Plot force - mutual crush from model result
        """
        fig = plt.figure(figsize = (14,12))
        plt.title('Mutual Crush and Impact Force', fontsize=20)
        plt.plot(self.model_result.dx * -12, self.model_result.springF, label = f'V1={self.veh1.vx_initial} mph', color = "k")
        plt.xticks(fontsize=16)
        plt.yticks(fontsize=16)
        plt.xlim([0, round(-12 * min(self.model_result.dx) + 1)])
        plt.ylim([0, round(max(self.model_result.springF)+100)])
        ax = plt.gca()
        ax.spines['right'].set_visible(False)
        ax.spines['top'].set_visible(False)
        plt.xlabel('Mutual Crush (in)', fontsize=20)
        plt.ylabel('Force (lb)', fontsize=20)
        #plt.grid(which='both', axis='both')
        #plt.legend(fontsize=14, frameon = False)
        fig.show()

    def plot_v(self):

        """
        plot vehicle velocities
        """
