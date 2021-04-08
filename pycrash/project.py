from tabulate import tabulate
from cookiecutter.main import cookiecutter
import os
import pickle

# TODO: when loading project, pull saved project data

def yes_or_no(question):
    while "the answer is invalid":
        reply = str(input(question + ' (y/n): ')).lower().strip()
        if reply[:1] == 'y':
            return True
        if reply[:1] == 'n':
            return False


def save_project_data(projectself):
    """
    save project data in pycrash data directory to share project info with other modules
    """
    if os.path.exists(os.path.join(projectself.project_path, projectself.name, "data", "archive", datafileName)):
        over_write_file = yes_or_no("Project file already exists here - overwrite?: ")
        if over_write_file:
            os.remove(
                os.path.join(projectself.project_path, projectself.name, "data", "archive", datafileName))  # delete current file
            ProjectData = project_objects

        else:
            new_project_name = str(input("Enter new project name: "))
            projectself.name = new_project_name
            ProjectData = project_objects


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

    def __init__(self, project_input=None):
        if (project_input == None):
            self.name = input("Project Name: ")
            self.project_path = str(input("Enter path to project directory: ")),
            self.pdesc = input("Project Description: ")
            self.sim_type = input("Simulation Type [Single Vehicle = SV | Multi-Vehicle = MV]: ")
            self.type = "project"  # class type

            if self.sim_type == "MV":
                self.impact_type = input("Impact Type (SDOF, SS, IMPC): ")

                if self.impact_type not in ["SS", "IMPC", "SDOF"]:
                    print("Not a valid impact type, choose SS, IMPC or SDOF. Value set to SDOF")
                    self.impact_type = None
            else:
                self.impact_type = None

            self.note = input("Note: ")
        else:
            self.name = project_input['name']
            self.project_path = project_input['project_path']
            self.pdesc = project_input['pdesc']
            self.sim_type = project_input['sim_type']
            self.impact_type = project_input['impact_type']
            self.note = project_input['note']
            self.type = 'project'  # class type

        # check if project directory exists
        # if it does, then a new project data file can be created at project/data/archive
        if not os.path.isdir(os.path.join(self.project_path, self.name)):
            os.chdir(self.project_path)
            cookie_cutter_repo = f'https://github.com/joe-cormier/pycrash.git'
            cookiecutter(cookie_cutter_repo, no_input=True, extra_context={'project_name': self.name})
        else:
            print(f'Project directory {os.path.join(self.project_path, self.name)} already exists')

        print(f'Project directories located here: {os.path.join(self.project_path, self.name)}')
        print(f'Place any input files to be used in {os.path.join(self.project_path, self.name, "data", "input")}')
        print('')

        # save data into archive for notebook reference
        datafileName = ''.join([self.name, '.pkl'])
        project_objects = {}
        project_objects.update({self.name: self})
        # test if datafileName.pkl exists
        if os.path.exists(os.path.join(self.project_path, self.name, "data", "archive", datafileName)):
            over_write_file = yes_or_no("Project file already exists here - overwrite?: ")
            if over_write_file:
                os.remove(
                    os.path.join(self.project_path, self.name, "data", "archive", datafileName))  # delete current file
                ProjectData = project_objects

            else:
                new_project_name = str(input("Enter new project name: "))
                datafileName = ''.join([new_project_name, '.pkl'])
                self.name = new_project_name
                ProjectData = project_objects

        else:
            # create new file for saving project data
            ProjectData = project_objects

        with open(os.path.join(self.project_path, self.name, "data", "archive", datafileName), 'wb') as handle:
            pickle.dump(ProjectData, handle, protocol=pickle.HIGHEST_PROTOCOL)

        print(tabulate([["Project", "Description", "Impact Type", "Simulation Type", "Note"],
                        [self.name, self.pdesc, self.impact_type, self.sim_type, self.note]]))

    def show(self):
        print(tabulate([["Project", "Description", "Impact Type", "Simulation Type", "Note"],
                        [self.name, self.pdesc, self.impact_type, self.sim_type, self.note]]))


    def save_project(self, *args):
        """
        root_path - directory to store project data
        save project to filename along with vehicles of Class Vehicle
        will create a directory and subdirectory for data and reports if
        they don't exist
        """
        nvehicles = 0
        nsdof_models = 0
        nsideswipe = 0
        nmultimotion = 0
        nsinglemotion = 0
        project_objects = {}
        project_objects.update({self.name: self})

        for a in args:
            if (a.type == 'vehicle'):
                nvehicles += 1
                project_objects.update({f'veh{nvehicles}': a})
            elif (a.type == 'sdof'):
                nsdof_models += 1
                project_objects.update({f'sdof{nsdof_models}': a})
            elif (a.type == 'sideswipe'):
                nsideswipe += 1
                project_objects.update({f'ss{nsideswipe}': a})
            elif (a.type == 'singlemotion'):
                nsinglemotion += 1
                project_objects.update({f'singlemotion{nsinglemotion}': a})
            elif (a.type == 'multimotion'):
                nmultimotion += 1
                project_objects.update({f'multimotion{nmultimotion}': a})
            else:
                print(f"Unknown object type for {a} of type {type(a)}")

        # filename for data is the project Name
        datafileName = ''.join([self.name, '.pkl'])

        # test if ProjectData.pkl exists
        if os.path.exists(os.path.join(self.project_path, self.name, "data", "archive", datafileName)):
            with open(os.path.join(self.project_path, self.name, "data", "archive", datafileName), 'rb') as handle:
                ProjectData = pickle.load(handle)
                # add new project to data file
                ProjectData = project_objects
        else:
            ProjectData = project_objects

        with open(os.path.join(self.project_path, self.name, "data", "archive", datafileName), 'wb') as handle:
            pickle.dump(ProjectData, handle, protocol=pickle.HIGHEST_PROTOCOL)


def project_info(project_name, proj_dir=False):
    """
    pulls project data to be used when reloading saved data
    will default to the project > data > archive folder
    """
    datafileName = ''.join([project_name, '.pkl'])

    if proj_dir:
        projectPath = proj_dir
    else:
        projectPath = os.path.join(os.getcwd(), "data", "archive")

    out_names = []
    print("This saved project contains:")
    with open(os.path.join(projectPath, datafileName), 'rb') as handle:
        ProjectData = pickle.load(handle)
    for key, value in ProjectData.items():
        print(f'Object of type "{value.type}" with name "{value.name}"')
        out_names.append(value.name)

    print(f'list objects in this order for loading project: {out_names}')
    print(f"Example: project_name, veh1, veh2 = load_project('project_name')")

def load_project(project_name, proj_dir=False):
    """
    load saved project data using information from "project_info"
    requires multiple variables for input:

    Example project with two vehicles:
    project, veh1, veh2 = load_project('ProjectName')
    """

    datafileName = ''.join([project_name, '.pkl'])

    if proj_dir:
        projectPath = proj_dir
    else:
        projectPath = os.path.join(os.getcwd(), "data", "archive")

    out_data = []
    with open(os.path.join(projectPath, datafileName), 'rb') as handle:
        ProjectData = pickle.load(handle)
        value_iterator = iter(ProjectData.values())
        first_value = next(value_iterator)
        print(f'Attributes in project: {len(ProjectData.values())}')
    if len(ProjectData) == 1:
        return first_value
    else:
        for key, value in ProjectData.items():
            out_data.append(value)
        return out_data
