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
from pycrash.project import Project
project_name = 'validation'

project_inputs = {'name':project_name,
                  'pdesc':'single vehicle motion',
                  'sim_type':'SV',
                  'impact_type':None,
                  'note':'j-turn manuevers'}

proj = Project(project_inputs)


# TODO: create script to ask for user inputs