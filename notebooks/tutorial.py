# %% Initilizing
import os
path_parent = os.path.dirname(os.getcwd())
data_directory = os.path.join(path_parent, "data")
os.chdir(path_parent)


# %% Import Modules
import matplotlib.pyplot as plt
from matplotlib.pyplot import text
from src.functions import EnergyDV, SpringSeriesKeff
from src.project import Project, project_info, load_project
from src.vehicle import Vehicle
from src.sdof_model import SDOF_Model
from scipy import signal
from scipy import integrate
import pandas as pd
import numpy as np
import pickle
import json

pd.options.display.max_columns = None
from IPython import get_ipython
from IPython.display import display
get_ipython().run_line_magic('matplotlib', 'qt')

# %% Create Project
# projects are used to store basic information about the project
# - name, type of impact, type of simulation to be run, description, notes
# the project will be used to save all associated aspects, vehicles, simulations etc.

proj = Project()

# %% Vehicle 1
veh1 = Vehicle('Veh1')
veh1.manual_specs()

# %% Vehicle 2
veh2 = Vehicle('Veh2')
veh2.manual_specs()

# %% Save Project with vehicle
proj.save_project(veh1, veh2)

# %% Save Project with vehicle
proj.save_project_test(veh1, veh2)
