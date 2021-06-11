import pandas as pd
import numpy as np
from pycrash.sdof_model import SDOF_Model
from copy import deepcopy
from pycrash.functions.ar import cipriani_rest
from tqdm.notebook import tqdm
import time

def create_input(input_dict, num_iter, velocity_input=None):
    """ create inputs for monte carlo simulation using dictionary inputs """
    if input_dict['type'] == 'normal':
        return np.random.normal(input_dict['data'][0], input_dict['data'][1], num_iter)
    elif input_dict['type'] == 'range':
        return np.random.uniform(input_dict['data'][0], input_dict['data'][1], num_iter)
    elif input_dict['type'] == 'list':
        return [input_dict['data'][int(x)] for x in np.random.uniform(0, len(input_dict['data']), num_iter)]
    elif input_dict['type'] == 'cipriani':
        return [cipriani_rest(x) for x in velocity_input]
    else:
        print(f"Unknown data input type {input_dict['type']}")


class SDOF_MonteCarlo():
    """
    run monte-carlo type simulation using defined mean / standard deviation for various inputs into SDOF model
    veh1, veh2 - defined using pycrash Vehicle class
    name - provide string prefix "Run_"
    k - provide single value, list of values or mean and standard deviation
    veh1.k - provide single value, list of values or mean and standard deviation
    veh2.k - provide single value, list of values or mean and standard deviation
    initial velocity - provide range or single value
    cor - provide single value, list of values or mean and standard deviation

    model inputs provided using a dictionary for each input:
    kmutual = {'type': ['normal', 'range', 'list']},
              {'data': list - if 'normal' [mean, standard deviation],
                                    'range' [low value, high value],
                                    'list' [k1, k2, k3, etc.]}
    k1: vehicle 1 stiffness (optional) - same as kmutual
    k2: vehicle 2 stiffness (optional) - same as kmutual
    cor = {'type': ['normal', 'range', 'list', 'cipriani']},
          {'data': list - if 'normal' [mean, standard deviation],
                                    'range' [low value, high value],
                                    'list' [mu1, mu2, mu3, etc.],
                                    'cipriani': 'cirpiani'}

    initial_velocity = {'type': ['normal', 'range', 'list']},
                       {'data': list - if 'normal' [mean, standard deviation],
                                    'range' [low value, high value],
                                    'list' [v1, v2, v3, etc.]}

    when 'list' option is used, each model will be created by randomly selecting one of the values
    when 'range' option is used, each model will be created by selecting a random value between the low and high values

        model_inputs = {"name_prefix": 'prefixtext',  # <- prefix for each model name
                        "k": k_model_list[i],       # <- mutual stiffness
                        "cor": cor_list[i],
                        "tstop": 0.117
                    }
    combine all inputs into a dictionary:
    model_inputs = {kmutual, cor, initial_velocity}
    k1, k2 are entered seperately
    """
    def __init__(self, veh1, veh2, name_prefix, model_inputs=False, k1=None, k2=None):
        self.type = 'sodf_montecarlo'
        self.veh1 = deepcopy(veh1)
        self.veh2 = deepcopy(veh2)
        self.name_prefix = name_prefix
        self.tstop = None
        self.results = {'veh1_DV': [],
                        'veh2_DV': [],
                        'veh1_Acc': [],
                        'veh2_Acc': [],
                        'peak_crush': [],
                        'residual_crush': [],
                        'veh1_peak_crush': [],
                        'veh2_peak_crush': [],
                        'veh1_residual_crush': [],
                        'veh2_residual_Crush': []}  # <- empty lists for storing results

        if k1 is not None:
            print(f"Stiffness for vehicle 1 provided as type: {k1['type']}")
            print("")
            self.k1 = deepcopy(k1)
        else:
            self.k1 = None
        if k2 is not None:
            print(f"Stiffness for vehicle 1 provided as type: {k2['type']}")
            print("")
            self.k2 = deepcopy(k2)
        else:
            self.k2 = None

        if model_inputs:
            print(f"Mutual stiffness of type: {model_inputs['kmutual']['type']}")
            print("")
            self.kmutual = model_inputs['kmutual']
            print(f"Restitution of type: {model_inputs['cor']['type']}")
            print("")
            self.cor = model_inputs['cor']
            print(f"Initial Velocity of type: {model_inputs['initial_velocity']['type']}")
            print("")
            self.initial_velocity = model_inputs['initial_velocity']
        else:
            print('No model inputs specified')

    def run_simulation(self, num_iter: int):
        """ num_iter specifies number of iterations """
        # need to create velocity list first to get restitution
        self.velocity_input = create_input(self.initial_velocity, num_iter)
        self.cor_input = create_input(self.cor, num_iter, self.velocity_input)
        self.kmutual_input = create_input(self.kmutual, num_iter)

        if self.k1 is not None:
            self.k1_input = create_input(self.k1, num_iter)
        if self.k2 is not None:
            self.k2_input = create_input(self.k2, num_iter)

        """ loop through various combinations """
        p_bar = tqdm(range(0, num_iter))
        for i in p_bar:
            time.sleep(0.5)
            p_bar.set_description(f'Working on: {i}')

            model_inputs = {"name": f'{self.name_prefix}_{str(i)}',
                            "k": self.kmutual_input[i],
                            "cor": self.cor_input[i],
                            "tstop": self.tstop
                            }
            # closing speed
            self.veh1.vx_initial = self.velocity_input[i]
            # assign individual stiffness values to get vehicle-specific crush
            if self.k1 is not None:
                self.veh1.k = self.k1_input[i]
            if self.k2 is not None:
                self.veh2.k = self.k2_input[i]

            run = SDOF_Model(self.veh1, self.veh2, model_inputs=model_inputs)
            model = run.model
            # append results
            self.results['veh1_DV'].append((model.v1.iloc[0]-model.v1.iloc[-1]) / 1.46667)
            self.results['veh2_DV'].append((model.v2.iloc[-1]-model.v2.iloc[0]) / 1.46667)
            self.results['veh1_Acc'].append(min(model.a1) /32.2)
            self.results['veh2_Acc'].append(max(model.a2) /32.2)
            self.results['peak_crush'].append(min(model.dx) * 12)
            self.results['residual_crush'].append(model.dx.iloc[-1] * 12)
            if self.k1 is not None:
                self.results['veh1_peak_crush'].append(min(model.veh1_dx) * 12)
                self.results['veh1_residual_crush'].append(model.veh1_dx.iloc[-1] * 12)
            if self.k2 is not None:
                self.results['veh2_peak_crush'].append(min(model.veh2_dx) * 12)
                self.results['veh2_residual_crush'].append(model.veh2_dx.iloc[-1] * 12)

            del model, run

"""
return histogram of inputs / outputs
kernel density of delta-V / acceleration by vehicle
"""







