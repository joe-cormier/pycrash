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

""" if running pycrash without installing:"""

import sys
sys.path.insert(0, '/Users/joe/Documents/pycrash')

from pycrash.project import Project
import os


projects_dir = "C:\\directory where project will be created"
projects_dir = os.getcwd()  # <- use current directory


"""
Change inputs below for project info:
"""

project_name = 'multiple vehicle impact'
project_inputs = {'name': project_name,
                  'pdesc': 'multi vehicle impact',
                  'project_path': projects_dir,
                  'sim_type': 'MV',
                  'impact_type': 'IMPC',
                  'note': 'updated pycrash model for multiple impacts and 2+ vehicles'}

proj = Project(project_inputs)
