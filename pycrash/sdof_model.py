import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
from .sdof_calcs.sdof_calculations import SingleDOFmodel
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

    def __init__(self, veh1, veh2, AB_offset = 0, model_inputs=None):
        self.type = "sdof"        # class type
        # create independent copy of vehicle class instances
        self.veh1 = deepcopy(veh1)
        self.veh2 = deepcopy(veh2)
        self.AB_offset = AB_offset     # <- [inches] adjust model crush to account for force required to initiate crush (offset = -A/B)
        # manually create inputs if not provided
        if (model_inputs == None):
            self.name = input('Enter name of SDOF model run:')
            self.cor = float(input('Provide a coefficient of restitution:'))
            self.k = input('Provide a single value or dataframe for mutual stiffness [lb/ft]:')
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
            self.ktype = 'constantK'               # define stiffness type for model
            if hasattr(self.veh1, 'k'):
                self.k1known = True   # if k1 is known, then veh1 crush can be calculated
            else:
                self.k1known = False

            if hasattr(self.veh2, 'k'):
                self.k2known = True
            else:
                self.k2known = False # if k2 is known, then veh2 crush can be calculated

        elif isinstance(self.k, pd.DataFrame):
            print(f"Stiffness Function Dataframe [disp (ft) | force (lb)] of shape = {self.k.shape}")
            self.ktype = 'tableK'                   # define stiffness type for model
            if hasattr(self.veh1, 'k'):
                self.k1known = True   # if k1 is known, then veh1 crush can be calculated
            else:
                self.k1known = False

            if hasattr(self.veh2, 'k'):
                self.k2known = True
            else:
                self.k2known = False # if k2 is known, then veh2 crush can be calculated

        if (isinstance(self.tstop, int)) or (isinstance(self.tstop, float)):
            print(f"Model will run until t = {self.tstop} seconds")
            self.ttype = 1                           # define t stop criteria
        elif (self.tstop == None):
            print("No stop time provided - model will run until vehicle separation")
            self.ttype = 0                           # define t stop criteria
        else:
            print('Something other than a number or "None" used for stop time - model will run until vehicle separation')
            self.ttype = 0                           # define t stop criteria

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
        self.model = SingleDOFmodel(W1 = self.veh1.weight,
                                    v1_initial = self.veh1.vx_initial,
                                    v1_brake = self.veh1.brake,
                                    W2 = self.veh2.weight,
                                    v2_initial = self.veh2.vx_initial,
                                    v2_brake = self.veh2.brake,
                                    k = self.k,
                                    cor = self.cor,
                                    tstop = self.tstop,
                                    ktype = self.ktype,
                                    ttype = self.ttype
                                    )
        if (self.AB_offset != 0):
            """The offset corrects for the force required to initiate permanent crush based on the A/B assumptions
            """
            print(f"Model Diplacement 'Dx' will be reduced by {self.AB_offset} inches")
            self.model.dx = [row + self.AB_offset / 12 for row in self.model.dx]

        if self.k1known:
            print("Vehicle 1 crush determined using provided stiffness")
            if self.ktype == "constantK":
                self.model['veh1_dx'] = [row * self.k / self.veh1.k for row in self.model.dx]

        if self.k2known:
            print("Vehicle 2 crush determined using provided stiffness")
            if self.ktype == "constantK":
                self.model['veh2_dx'] = [row * self.k / self.veh2.k for row in self.model.dx]

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
        plt.plot(self.model.dx * -12, self.model.springF, label = f'V1={self.veh1.vx_initial} mph', color = "k")
        plt.xticks(fontsize=16)
        plt.yticks(fontsize=16)
        plt.xlim([0, round(-12 * min(self.model.dx) + 1)])
        plt.ylim([0, round(max(self.model.springF)+100)])
        ax = plt.gca()
        ax.spines['right'].set_visible(False)
        ax.spines['top'].set_visible(False)
        plt.xlabel('Mutual Crush (in)', fontsize=20)
        plt.ylabel('Force (lb)', fontsize=20)
        #plt.grid(which='both', axis='both')
        #plt.legend(fontsize=14, frameon = False)
        fig.show()

    def plot_fdx_vehicle(self, vehNum):
        """
        Plot force - mutual crush from model result
        """
        if vehNum == 1:
            vehicle_dx = self.model.veh1_dx * -12
        else:
            vehicle_dx = self.model.veh2_dx * -12
        fig = plt.figure(figsize = (14,12))
        plt.title('Vehicle Crush and Impact Force', fontsize=20)
        plt.plot(vehicle_dx, self.model.springF, label = f'V1={self.veh1.vx_initial} mph', color = "k")
        plt.xticks(fontsize=16)
        plt.yticks(fontsize=16)
        plt.xlim([0, round(-12 * min(self.model.dx) + 1)])
        plt.ylim([0, round(max(self.model.springF)+100)])
        ax = plt.gca()
        ax.spines['right'].set_visible(False)
        ax.spines['top'].set_visible(False)
        plt.xlabel('Crush (in)', fontsize=20)
        plt.ylabel('Force (lb)', fontsize=20)
        #plt.grid(which='both', axis='both')
        #plt.legend(fontsize=14, frameon = False)
        fig.show()

    def crush_energy(self):
        """ inegrate force-displacement data to get energy """

        """ divide disp-force data """
        disp_max_i = self.model.dx.idxmin()

        # integrate f-dx
        loading = self.model.iloc[0: disp_max_i].copy()
        energy_absorbed = np.trapz(loading.springF, loading.dx)
        unloading = self.model.iloc[disp_max_i: len(self.model)]
        energy_returned = np.trapz(unloading.springF, unloading.dx)
        cor = np.sqrt(np.abs(energy_returned) / np.abs(energy_absorbed))

        print(f'Mutual crush energy for {self.name}:')
        print(f'Energy absorbed: {energy_absorbed:0.1f} ft-lb')
        print(f'Energy returned: {energy_returned:0.1f} ft-lb')
        print(f'Coefficient of restitution: {cor:0.2f}')
        print('')

        out = {'mutual_energy_absorbed': energy_absorbed,
                'mutual_energy_returned': energy_returned,
                'cor': cor}

        if self.k1known:
            """ energy for vehicle 1 """
            disp_max_i = self.model.veh1_dx.idxmin()
            loading = self.model.iloc[0: disp_max_i].copy()
            energy_absorbed = np.trapz(loading.springF, loading.veh1_dx)
            unloading = self.model.iloc[disp_max_i: len(self.model)]
            energy_returned = np.trapz(unloading.springF, unloading.veh1_dx)
            cor = np.sqrt(np.abs(energy_returned) / np.abs(energy_absorbed))

            print(f'Crush energy for vehicle {self.veh1.name}:')
            print(f'Energy absorbed: {energy_absorbed:0.1f} ft-lb')
            print(f'Energy returned: {energy_returned:0.1f} ft-lb')
            print(f'Coefficient of restitution: {cor:0.2f}')
            print('')

            out['veh1_energy_absorbed'] = energy_absorbed
            out['veh1_energy_returned'] = energy_returned
            out['veh1_cor'] = cor

        if self.k2known:
            """ energy for vehicle 2 """
            disp_max_i = self.model.veh2_dx.idxmin()
            loading = self.model.iloc[0: disp_max_i].copy()
            energy_absorbed = np.trapz(loading.springF, loading.veh2_dx)
            unloading = self.model.iloc[disp_max_i: len(self.model)]
            energy_returned = np.trapz(unloading.springF, unloading.veh2_dx)
            cor = np.sqrt(np.abs(energy_returned) / np.abs(energy_absorbed))

            print(f'Crush energy for vehicle {self.veh2.name}:')
            print(f'Energy absorbed: {energy_absorbed:0.1f} ft-lb')
            print(f'Energy returned: {energy_returned:0.1f} ft-lb')
            print(f'Coefficient of restitution: {cor:0.2f}')
            print('')

            out['veh2_energy_absorbed'] = energy_absorbed
            out['veh2_energy_returned'] = energy_returned
            out['veh2_cor'] = cor

        return out


    def get_results(self):
        print('')
        print(f'Simulation results for {self.veh1.name}:')
        print(f'delta-V: {(self.model.v1.iloc[0]-self.model.v1.iloc[-1]) / 1.46667:0.2f} mph')
        print(f'Peak acceleration: {min(self.model.a1) /32.2:0.1f} g')
        if self.k1known:
            print(f'Residual crush: {self.model.veh1_dx.iloc[-1] * 12:0.2f} inches')

        print('')
        print(f'Simulation results for {self.veh2.name}:')
        print(f'delta-V: {(self.model.v2.iloc[-1]-self.model.v2.iloc[0]) / 1.46667:0.2f} mph')
        print(f'Peak acceleration: {max(self.model.a2) / 32.2:0.1f} g')
        if self.k2known:
            print(f'Residual crush: {self.model.veh2_dx.iloc[-1] * 12:0.2f} inches')
