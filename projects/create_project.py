"""
Use this script to create a new project and directory for storing Pycrash files
Directory Structure:

|-- ProjectName
    |--data
        |--archive      <- stores Pyrcrash compressed data in .pkl format
        |--input        <- place input files here, input created by user will be saved here as .csv files
        |--results      <- model results stored here by Pycrash in .csv format
    |--docs             <- store supporting / reference documents here
    |--notebooks        <- store .py or Jupyter Notebook files used to run your Pycrash project
    |--reports          <- used to consolidate output files, user generated reports
    |--visualization    <- Pycrash plots saved here
"""

import os
# current_dir = os.getcwd()

import sys

# sys.path.append("/home/jmc/Documents/pycrash")
#sys.path.append("/home/joemcormier/pycrash/")
sys.path.append("D:\\OneDrive\\pycrash")


print(os.getcwd())
from pycrash.project import Project

print(os.getcwd())

project_name = 'validation sdof'
project_inputs = {'name': project_name,
                  'pdesc': 'validate sdof model',
                  'project_path': "D:\\OneDrive\\pycrash\\projects",
                  'sim_type': 'MV',
                  'impact_type': 'SDOF',
                  'note': 'validate sdof model using load cell barrier data'}

proj = Project(project_inputs)

# TODO: create script to ask for user inputs
