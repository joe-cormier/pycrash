"""
Use this script to create a new project and directory for storing Pycrash files
Directory Structure:

|-- ProjectName
    |--data
        |--archive      <- stores Pyrcrash compressed data in .pkl format
        |--input        <- place input files here, input created by user will be saved here as .csv files
        |--results      <- model results stored here by Pycrash in .csv format
    |--notebooks        <- store .py or Jupyter Notebook files used to run your Pycrash project
    |--reports          <- used to consolidate output files, user generated reports
    |--visualization    <- Pycrash plots saved here
"""
import sys
sys.path.append("/home/joemcormier/github/pycrash")


import os
path_parent = os.path.dirname(os.getcwd())
os.chdir(os.path.join(path_parent, 'pycrash'))
print(os.path.join(path_parent, 'pycrash'))

from pycrash.project import Project

project_inputs = {'name':'Demo',
                  'path':os.path.join(path_parent, 'projects'),
                  'pdesc':'low speed frontal',
                  'sim_type':'MV',
                  'impact_type':'IMPC',
                  'note':'backing trailer'}

proj = Project(project_inputs)


# TODO: create script to ask for user inputs
