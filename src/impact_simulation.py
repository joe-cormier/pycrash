"""
use input data to determine simulation type
will determine what type of simulation is run - internal function
"""
import os
import pickle

def ImpactSim(ProjectName):
    os.chdir('/home/joemcormier/github/pycrash/data')
    with open('ProjectData.pkl', 'rb') as handle:
        allProjectData = pickle.load(handle)

    sim_type = allProjectData[ProjectName]['info']['sim_type']
    return sim_type


ImpactSim('test')
