import pandas as pd
import numpy as np
from copy import deepcopy
from .impact_vehicle_model import multi_vehicle_model
from .model_calcs.impact_detect import detect
from .model_calcs.collision_plane import define_impact_plane, define_impact_edge
from pycrash.model_calcs.position_data import position_data_motion, position_data_static
from .visualization.model_interval_two_vehicles import plot_motion_interval
from .visualization.initial_positions import initial_position
from .model_calcs.carpenter_momentum_calcs import impc
from .visualization.kinematics import plot_model
from .visualization.vehicles_at_impact import plot_impact
# TODO: add ability to use force-displacement data
# TODO: change self.sim_defaults to sim_settings
# TODO: environment data

# column list for vehicle model
vehicle_data_columns = ['t', 'vx', 'vy', 'Vx', 'Vy', 'Vr', 'vehicleslip_deg', 'vehicleslip_rad', 'oz_deg', 'oz_rad', 'delta_deg',
                        'delta_rad', 'turn_rX', 'turn_rY', 'turn_rR', 'au', 'av', 'ax', 'ay', 'ar', 'Ax', 'Ay', 'Ar',
                        'alphaz', 'alphaz_deg', 'beta_deg', 'beta_rad', 'lf_fx', 'lf_fy', 'rf_fx', 'rf_fy',
                        'rr_fx', 'rr_fy', 'lr_fx', 'lr_fy', 'lf_alpha', 'rf_alpha', 'rr_alpha', 'lr_alpha',
                        'lf_lock', 'rf_lock', 'rr_lock', 'lr_lock', 'lf_fz', 'rf_fz', 'rr_fz', 'lr_fz',
                        'theta_rad', 'theta_deg', 'Fx', 'Fy', 'Mz']

#model = pd.DataFrame(np.zeros(shape=(1, len(vehicle_data_columns))), columns=vehicle_data_columns)

""" create inputs for impact """
def create_impact_order():
    """ create list of impacts with list of striking and struck vehicle for each impact """
    print('Creating list of striking and struck vehicle for each impact')
    print('Vehicle indices start at 0')
    impactTotal = int(input("Enter total number of impacts: "))
    impact_order = []
    for i in range(0, impactTotal):
        striking = int(input(f"Enter striking vehicle number for impact {i}: "))
        struck = int(input(f"Enter struck vehicle number for impact {i}: "))
        impact_order.append([striking, struck])

    print(f'Impact order defined as: {impact_order}')
    return impact_order

def create_impc_inputs(numImpacts):
    """ create dictionary for each impact with intervehicle friction and restitution
        defined for each impact  """
    impc_inputs = {}
    for i in range(0, numImpacts):
        mu = float(input(f"Enter intervehicular friction for impact {i}: "))
        cor = float(input(f"Enter coefficient of restitution for impact {i}: "))
        impc_inputs[i] = {'vehicle_mu': mu,
                          'cor': cor}

    print(f'IMPC inputs defined as: {impc_inputs}')
    return impc_inputs



"""
main file for controlling vehicle motion simulation and impact
"""

class Impact():
    def __init__(self, name, endTime, impact_type, vehicle_list, impact_order=None, impc_inputs=None, user_sim_defaults=None):
        """ impact_order defines the [striking , struck] vehicle using a list of lists
        impc_inputs is a dictionary of inputs for each impact of the form {0:{'vehicle_mu': 0.3, 'cor': 0.1}}"""
        self.name = name
        self.type = 'impact'
        self.vehicles = deepcopy(vehicle_list)
        self.impactNum = 0  # counter for the number of impacts in simulation
        self.endTime = endTime  # total simulation time (s)
        self.impc_inputs = impc_inputs  # dictionary of inputs for IMPC by impact

        # initialize vehicle variables
        for veh in self.vehicles:
            veh.impactTotal = 0

        """ test for impact_order """
        if impact_order:
            print(f'Impact order defined as: {impact_order}')
            self.impact_order = impact_order
        else:
            self.impact_order = create_impact_order()

        """ get number of impacts per vehicle """
        self._impactsPerVehicle = [0] * len(self.vehicles)  # count impacts per vehicle
        for imp in self.impact_order:
            self._impactsPerVehicle[imp[0]] += 1
            self._impactsPerVehicle[imp[1]] += 1
            self.vehicles[imp[0]].impactTotal += 1
            self.vehicles[imp[1]].impactTotal += 1

        """ test for impact_inputs """
        if impc_inputs:
            print(f'IMPC inputs defined as: {impc_inputs}')
            if len(impc_inputs) != len(impact_order):
                print(f'{len(impc_inputs)} IMPC inputs provided. Impact order indicates {len(impact_order)} are required.')
            else:
                self.impc_inputs = impc_inputs
        else:
            self.impc_inputs = create_impc_inputs(len(self.impact_order))

        if (impact_type not in ["SS", "IMPC", "impc"]):
            print("Not a valid impact type, choose SS, IMPC")
            impact_type = input("Enter an impact type of SS or IMPC: ")

            if (impact_type not in ["SS", "IMPC", "impc"]):
                print("Not a valid impact type - value set to None")
                self.impact_type == None
            else:
                self.impact_type = impact_type
        else:
            self.impact_type = impact_type   # <- assign impact type to provided value

        # load defaults
        if user_sim_defaults:
            # TODO: create check for user sim_defaults_input
            self.sim_defaults = user_sim_defaults
        else:
            self.sim_defaults = {'dt_motion': 0.01,
                                 'mu_max': 0.76,
                                 'alpha_max': 0.174533,  # 10 degrees
                                }

        # check for driver inputs
        for veh in self.vehicles:
            if hasattr(veh, 'driver_input'):
                print(f"Driver input for {veh.name} of shape = {veh.driver_input.shape}")
            else:
                print(f'Driver input for {veh.name} not provided - no braking or steering applied')
                end_time = int(input('Enter duration for simulation (seconds):'))
                t = list(np.arange(0, end_time + self.sim_defaults['dt_motion'], self.sim_defaults['dt_motion']))  # create time array from 0 to end time from user
                throttle = [0] * len(t)
                brake = [0] * len(t)
                steer = [0] * len(t)
                veh.driver_input = pd.DataFrame.from_dict({'t': t, 'throttle': throttle, 'brake': brake, 'steer': steer})
                print(f'Driver inputs for {veh.name} set to zero for {end_time} seconds')

        # TODO: convert sideswipe to lists of tuples like impc
            # sideswipe will not have iplane=True
        """ IMPC model - impact points and edge detection """
        # TODO: test for totalIMpacts = number of impact points / edges
        if self.impact_type in ['IMPC', 'impc']:
            for veh in self.vehicles:
                if veh.striking:
                    if hasattr(veh, 'impact_points'):
                        print(f'Predefined impact points for {veh.name}: [x (ft), y (ft), impact plane angle (deg)] = {veh.impact_points}')
                        veh._impactPoints = len(veh.impact_points)
                    else:
                        print(f"Create impact point(s) for {veh.name} [striking vehicle]")
                        print("")
                        veh = define_impact_plane(veh, iplane=True)
                    print(f'Total impacts for {veh.name}: {len(veh.impact_points)}')

                else:
                    if hasattr(veh, 'edgeimpact_points'):
                        print(f'Predefined impact edge for {veh.name}: {veh.edgeimpact}')
                    else:
                        print(f"Create impacting edge for {veh.name} [stuck vehicle]")
                        print("")
                        veh = define_impact_edge(veh, iplane=False)
                    print(f'Total impacts for {veh.name} - total defined edges: {len(veh.edgeimpact_points)}')

        """ initialize vehicle motion dataframes """
        # TODO: resolve differences between vehicle input time duration and simulation duration - input must be > than simulation?

        for veh in self.vehicles:
            if veh.type == 'Barrier':
                # create vehicle with no motion for "Barrier" type
                veh.model = pd.DataFrame(np.nan, index=np.arange(1+len(np.arange(0, self.endTime, self.sim_defaults['dt_motion']))), columns=vehicle_data_columns)
                veh.model['Dx'] = veh.init_x_pos
                veh.model['Dy'] = veh.init_y_pos
                veh.model = veh.model.fillna(0)
            else:
                veh.model = pd.DataFrame(np.nan, index=np.arange(1+len(np.arange(0, self.endTime, self.sim_defaults['dt_motion']))), columns=vehicle_data_columns)
                veh.model.Fx[0] = 0
                veh.model.Fy[0] = 0
                veh.model.Mz[0] = 0
                veh.model.au[0] = 0  # no initial vehicle pitch
                veh.model.av[0] = 0  # no initial vehicle roll
                veh.model.vx[0] = veh.vx_initial * 1.46667  # convert input in mph to fps
                veh.model.vy[0] = veh.vy_initial * 1.46667  # convert input in mph to fps
                veh.model.theta_rad[0] = veh.head_angle * np.pi / 180  # initial heading angle
                veh.model.oz_rad[0] = veh.omega_z * (np.pi / 180)  # initial angular rate (deg/s) - input
                veh.model.Vx[0] = veh.vx_initial * 1.46667 * np.cos(veh.head_angle * np.pi / 180) - veh.vy_initial * 1.46667 * np.sin(veh.head_angle * np.pi / 180)
                veh.model.Vy[0] = veh.vx_initial * 1.46667 * np.sin(veh.head_angle * np.pi / 180) + veh.vy_initial * 1.46667 * np.cos(veh.head_angle * np.pi / 180)

        self.detect_data = pd.DataFrame(np.nan, index=np.arange(1+len(np.arange(0, self.endTime, self.sim_defaults['dt_motion']))),
                                   columns=['impact', 'edge_loc', 'normal_crush', 'impactp_veh2x', 'impactp_veh2y', 'ImpactNumber'])

        """ dictionaries for storing impact related data """
        self._impactList = list(range(0, len(self.impact_order)))
        self.impc_results = dict.fromkeys(self._impactList)
        self._impPointEdge = dict.fromkeys(self._impactList)
        self._impactIndex = {}  # index of each impact for plotting

        # create list of striking and struck vehicle
        self._strikingVehicleList = []
        self._struckVehicleList = []
        impactsPerVehicle = [0] * len(self.vehicles)  # count impacts per vehicle
        counter = 0
        for imp in self.impact_order:
            self._strikingVehicleList.append(imp[0])  # striking vehicle in each impact
            self._struckVehicleList.append(imp[1])    # struck vehicle in each impact

            # dictionary of impact points and edges for each impact - starts at zero
            self._impPointEdge[counter] = {'impact_points': self.vehicles[imp[0]].impact_points[impactsPerVehicle[imp[0]]],
                                           'edgeimpact_points': self.vehicles[imp[1]].edgeimpact_points[impactsPerVehicle[imp[1]]]}  # impact points and edge for each impact
            impactsPerVehicle[imp[0]] += 1
            impactsPerVehicle[imp[1]] += 1
            counter += 1

        print(self._impPointEdge)
        """ create impact object is complete """
        print(f'Impact simulation created with {len(self.vehicles)} vehicles of type {self.impact_type}')
        print(f'Simulation inputs: {self.sim_defaults}')

    """ plot initial positions: include impact planes """
    # plot initial position

    def show_initial_position(self):
        initial_position(position_data_static(self.vehicles))

    """ plot vehicle motion """
    def plot_vehicle_motion(self, n_intervals, tire_path=True, show_vector=False):
        # TODO: adjust what impact point to plot
        plotImpactPoint = 0     # starts at 1
        plot_motion_interval(self.vehicles, self._impactIndex, n_intervals,
                             tire_path=tire_path, show_vector=show_vector)

    """ plot vehicles at impact """
    def plot_impact(self, impactNum):
            for key, value in self._impactIndex.items():
                if value == impactNum:
                    plot_impact(self.vehicles, key-1, self._impactIndex, show_vector=True)
                    print(f'Plotting impact {value} at index {key}')

    """ plot kinematic data """
    def plot_model(self, vehNum):
        plot_model(self.vehicles[vehNum])

    """ initiate impact simulation """

    def simulate(self, show_results=True):
        """
        end_time <- default time of simulation (seconds), simulation will still stop if vehicle motion is zero
        """
        self.show_results = show_results   # print results from impact simulation calculations
        separation = True   # vehicles are separated / not engaged
        impactsComplete = False  # all impacts have occurred

        for i in range(0, 1 + int(self.endTime / self.sim_defaults['dt_motion'])):
            #print(i)
            for veh in self.vehicles:
                """ calculate current position of each vehicle """
                if veh.type != 'Barrier':
                    #print(f'Simulating Vehicle: {veh.name}')
                    veh = multi_vehicle_model(veh, i, self.sim_defaults, self.impact_type)

            if not impactsComplete:

                """ use impact detect to look for impacts"""
                strikingVehicle = self.impact_order[self.impactNum][0]  # index of striking vehicle
                struckVehicle = self.impact_order[self.impactNum][1]    # index of struck vehicle

                # separate crush data for each impact - create dictionary for each impact
                #print(f'Looking for impact {self.impactNum} between vehicles: {self.impact_order[self.impactNum]}')
                #print(f'vehicles are separated: {separation}')
                self.detect_data = detect(i, self.impactNum, self.vehicles, self._impPointEdge, strikingVehicle, struckVehicle, self.detect_data)

                if self.detect_data.impact[i]:
                    print('')
                    print(f"Impact #{self.impactNum} detected at i: {i}, t: {i * self.sim_defaults['dt_motion']}")
                    print('')
                    """ apply momentum IMPC if impact only if vehicles are separated """
                    if (self.detect_data.impact[i] & separation):
                        if self.impact_type in ["IMPC", "impc"]:

                            self.vehicles, self.impc_results[self.impactNum] = impc(i,
                                                                                   self.impactNum,
                                                                                   self.detect_data.impactp_veh2x[i],
                                                                                   self.detect_data.impactp_veh2y[i],
                                                                                   self._impPointEdge,
                                                                                   self.vehicles,
                                                                                   strikingVehicle,
                                                                                   struckVehicle,
                                                                                   self.impc_inputs[self.impactNum],
                                                                                   self.sim_defaults['dt_motion'],
                                                                                   self.show_results)  # run impc model

                        separation = False
                        self._impactIndex[i] = self.impactNum
                        self.impactNum += 1

                else:
                    if (not separation) and (not self.detect_data.impact[i]):
                        # separation is false and impact is true - vehicles have now separated
                        print(f'Vehicles separated')
                        separation = True

            if self.impactNum == len(self.impact_order):
                impactsComplete = True

        """ convert and position data for plots """
        for veh in self.vehicles:
            veh.model.alphaz_deg = [row * 180 / np.pi for row in veh.model.alphaz]  # move to seperate calc
            veh.model.oz_deg = [row * 180 / np.pi for row in veh.model.oz_rad]  # move to seperate calc
            veh.model.theta_deg = [row * 180 / np.pi for row in veh.model.theta_rad]  # move to seperate calc
            veh.model.beta_deg = [row * 180 / np.pi for row in veh.model.beta_rad]  # move to seperate calc
            # get position data
            veh = position_data_motion(veh)





