
from tabulate import tabulate
import os
import pickle

# TODO: when initializing project, directory for project must be specified
# this directory will be used to save all files

class Project:
    """
    class object for project variables
    name - project name - will be used to save and load project data
    pdesc - brief description of project, impact type, etc.
    sim_type - what type of simulation performed, single or multi vehicle
    impact_type - sideswipe (SS), momentum (IMPC), single degree of freedom (SDOF)
                - defaults to "none"
    note - user note
    """

    def __init__(self, project_input = None):
        if (project_input == None):
            self.name = input("Project Name: ")
            self.pdesc = input("Project Description: ")
            self.sim_type = input("Simulation Type [Single Vehicle = SV | Multi-Vehicle = MV]: ")
            self.type = "project"      # class type

            if self.sim_type == "MV":
                self.impact_type = input("Impact Type (SDOF, SS, IMPC): ")

                if (self.impact_type not in ["SS", "IMPC", "SDOF"]):
                    print("Not a valid impact type, choose SS, IMPC or SDOF. Value set to SDOF")
                    self.impact_type == "SDOF"
            else:
                self.impact_type = "none"

            self.note = input("Note: ")
        else:
            self.name = project_input['name']
            self.pdesc = project_input['pdesc']
            self.sim_type = project_input['sim_type']
            self.impact_type = project_input['impact_type']
            self.note = project_input['note']

        print(tabulate([["Project", "Description", "Impact Type", "Simulation Type", "Note"],
                    [self.name, self.pdesc, self.impact_type, self.sim_type, self.note]]))

    def show(self):
        print(tabulate([["Project", "Description", "Impact Type", "Simulation Type", "Note"],
                         [self.name, self.pdesc, self.impact_type, self.sim_type, self.note]]))

    def save_project(self, root_path, *args):
        """
        root_path - directory to store project data
        save project to filename along with vehicles of Class Vehicle
        will create a directory and subdirectory for data and reports if
        they don't exist
        TODO: add functionality for 3+ vehicles and model runs
        """
        nvehicles = 0
        nsdof_models = 0
        nsideswipe = 0
        project_objects = {}
        project_objects.update({self.name:self})

        for a in args:
            if (a.type == 'vehicle'):
                nvehicles += 1
                project_objects.update({f'veh{nvehicles}':a})
            elif (a.type == 'sdof'):
                nsdof_models += 1
                project_objects.update({f'run{nsdof_models}':a})
            elif (a.type == 'sideswipe'):
                nsideswipe += 1
                project_objects.update({f'run{nsideswipe}':a})
            else:
                print(f"Unknown object type for {a} of type {type(a)}")

        # filename for data is the project Name
        datafileName = ''.join([self.name, 'pkl'])

        # check if data and report directories exist, if not create them
        if os.path.isdir(os.path.join(root_path, self.name)) == False:
            try: os.makedirs(os.path.join(root_path, self.name, "data"))

            except OSError:
                print (f'Creation of the directory {os.path.join("root_path", self.name)} failed')

        if os.path.isdir(os.path.join(root_path, self.name)):
                 os.mkdir(os.path.join(root_path, self.name, "reports"))
                 os.mkdir(os.path.join(root_path, self.name, "visualization"))

        # test if ProjectData.pkl exists
        if os.path.exists(os.path.join(root_path, self.name, "data", datafileName)):
            with open(os.path.join(root_path, self.name, "data", datafileName), 'rb') as handle:
                ProjectData = pickle.load(handle)
            # add new project to data file
            ProjectData.update({self.name:project_objects})
        elif os.path.exists(os.path.join(root_path, self.name, "data", datafileName)) == False:
            # create new file for saving project data
            ProjectData = {}
            ProjectData.update({self.name:project_objects})

        with open(os.path.join(root_path, self.name, "data", datafileName), 'wb') as handle:
            pickle.dump(ProjectData, handle, protocol=pickle.HIGHEST_PROTOCOL)


    def project_info(project_name, project_path):
        """
        pulls project data to be used when reloading saved data
        """
        datafileName = ''.join([project_name, 'pkl'])

        out_names = []

        print("This saved project contains:")
        with open(os.path.join("project_path", "project_name", "data", datafileName), 'rb') as handle:
            ProjectData = pickle.load(handle)
            project_data = ProjectData[project_name]
        for key, value in project_data.items():
            print(f'Object of type "{value.type}" with name "{value.name}"')
            out_names.append(value.name)

        print(f'Project objects: {out_names} at path: {os.path.join("project_path", "project_name", "data")}')


    # %%   Load project data
    def load_project(project_name, project_path):
        """
        load saved project data using information from "project_info"
        requires multiple variables for input:

        Example prject with two vehicles:
        project, veh1, veh2 = load_project('ProjectName')
        """

        out_data = []
        with open(os.path.join("project_path", "project_name", "data", datafileName), 'rb') as handle:
            ProjectData = pickle.load(handle)
            project_data = ProjectData[project]
        for key, value in project_data.items():
            out_data.append(value)

        return out_data
