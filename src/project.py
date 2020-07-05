from tabulate import tabulate
import os
import pickle


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

    def __init__(self):
        self.name = input("Project Name: ")
        self.pdesc = input("Project Description: ")
        self.sim_type = input("Simulation Type [Single Vehicle = SV/ Multi-Vehicle = MV]: ")
        self.type = "project"      # class type

        if self.sim_type == "MV":
            self.impact_type = input("Impact Type (SS, IMPC, SDOF): ")

            if (self.impact_type not in ["SS", "IMPC", "SDOF"]):
                print("Not a valid impact type, choose SS, IMPC or SDOF. Value set to SDOF")
                self.impact_type == "SDOF"
        else:
            self.impact_type = "none"

        self.note = input("Note: ")

        print(tabulate([["Project", "Description", "Impact Type", "Simulation Type", "Note"],
                    [self.name, self.pdesc, self.impact_type, self.sim_type, self.note]]))

    def show(self):
        print(tabulate([["Project", "Description", "Impact Type", "Simulation Type", "Note"],
                         [self.name, self.pdesc, self.impact_type, self.sim_type, self.note]]))

    def save_project(self, *args):
        """ save project to filename along with vehicles of Class Vehicle
        saved in an appended file that contains all prior project data
        Will append the current project to the prexisting dataset if it exists
        TODO: add functionality for 3+ vehicles and model runs
        """
        nvehicles = 0
        nsdof_models = 0
        project_objects = {}
        project_objects.update({self.name:self})

        for a in args:
            if (a.type == 'vehicle'):
                nvehicles += 1
                project_objects.update({f'veh{nvehicles}':a})
            elif (a.type == 'sdof'):
                nsdof_models += 1
                project_objects.update({f'run{nsdof_models}':a})
            else:
                print(f"Unknown object type for {a} of type {type(a)}")


        # test if ProjectData.pkl exists
        if os.path.exists(os.path.join(os.getcwd(), "data", "archive", "ProjectDataArchive.pkl")) == True:
            with open(os.path.join(os.getcwd(), "data", "archive", "ProjectDataArchive.pkl"), 'rb') as handle:
                ProjectArhive = pickle.load(handle)
            # add new project to data file
            ProjectArhive.update({self.name:project_objects})
        elif os.path.exists(os.path.join(os.getcwd(), "data" "archive", "ProjectDataArchive.pkl")) == False:
            # create new file for saving project data
            ProjectArhive = {}
            ProjectArhive.update({self.name:project_objects})

        with open(os.path.join(os.getcwd(), "data", "archive", "ProjectDataArchive.pkl"), 'wb') as handle:
            pickle.dump(ProjectArhive, handle, protocol=pickle.HIGHEST_PROTOCOL)

# %% get project info
def project_info(project):
    """
    pulls project data to be used when reloading saved data
    """
    out_names = []

    print("This saved project contains:")
    with open(os.path.join(os.getcwd(), "data", "archive", "ProjectDataArchive.pkl"), 'rb') as handle:
        ProjectArhive = pickle.load(handle)
        project_data = ProjectArhive[project]
    for key, value in project_data.items():
        print(f'Object of type "{value.type}" with name "{value.name}"')
        out_names.append(value.name)

    print(f"{out_names}")

# %%   Load project data
def load_project(project):
    """
    load saved project data using information from "project_info"
    requires multiple variables for input:
    project, veh1, veh2 = load_project('ProjectName')
    """
    out_data = []
    with open(os.path.join(os.getcwd(), "data", "archive", "ProjectDataArchive.pkl"), 'rb') as handle:
        ProjectArhive = pickle.load(handle)
        project_data = ProjectArhive[project]
    for key, value in project_data.items():
        out_data.append(value)

    return out_data
