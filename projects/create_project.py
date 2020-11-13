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


from pycrash.project import Project

projects_dir = "C:\\directory where project will be created"


"""
Change inputs below for project info:
"""

project_name = 'pycrash project'
project_inputs = {'name': project_name,
                  'pdesc': 'project description',
                  'project_path': projects_dir,
                  'sim_type': 'MV',
                  'impact_type': 'SDOF',
                  'note': 'detail about project'}

proj = Project(project_inputs)