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
#current_dir = os.getcwd()

import sys
#sys.path.append("/home/jmc/Documents/pycrash")
sys.path.append("/home/joemcormier/pycrash/")

#os.chdir("/home/joemcormier/pycrash/")
print(os.getcwd())
from pycrash.project import Project

#os.chdir(current_dir)
print(os.getcwd())

project_name = 'validation sideswipe'
project_inputs = {'name':project_name,
                  'pdesc':'validate sideswipe models',
				  'project_path':"/home/joemcormier/pycrash/projects/",
                  'sim_type':'MV',
                  'impact_type':'SS',
                  'note':'validate sideswipe against published data'}

proj = Project(project_inputs)



# TODO: create script to ask for user inputs
