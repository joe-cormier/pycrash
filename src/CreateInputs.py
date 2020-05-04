"""
create dictionary for inputs manually or from saved file
"""
import os
from os import path
import pickle

input_query = ["Make",
"Model",
"VIN",
"Weight (lb)",
"Steering ratio",
"Initial X position (ft)",
"Initial Y position (ft)",
"Heading angle (deg)",
"Vehicle width (ft)",
"Vehicle length (ft)",
"CG height (ft)",
"CG to front axle (ft)",
"CG to rear axle (ft)",
"Wheelbase (ft)",
"Track width (ft)",
"Front overhang (ft)",
"Rear overhang (ft)",
"Tire diameter (ft)",
"Tire width (ft)",
"Izz (slug - ft^2)",
"Front wheel drive (0/1)",
"Rear wheel drive (0/1)",
"All wheel drive (0/1)",
"A",
"B",
"k",
"Initial velocity (mph)"]

veh_inputs = [
"make",
"model",
"vin",
"weight",
"steer_ratio",
"init_x_pos",
"init_y_pos",
"head_angle",
"v_width",
"v_length",
"hcg",
"lcgf",
"lcgr",
"wb",
"track",
"f_hang",
"r_hang",
"tire_d",
"tire_w",
"izz",
"fwd",
"rwd",
"awd",
"A",
"B",
"k",
"v_initial"]

pname = input('Project Name:')
pdesc = input('Project Description:')
impact_type = input('Impact Type:')
sim_type = input('Simulation Type (SV/MV):')
note = input('Note:')

info = {'pdesc':pdesc, 'impact_type':impact_type, 'sim_type':sim_type, 'note':note}
veh_one_inputs = list(range(len(veh_inputs)))
veh_two_inputs = list(range(len(veh_inputs)))

if sim_type == 'SV':
    veh_one_inputs = list(range(len(veh_inputs)))
    print(f'<=== Inputs for single vehicle simulation ===>')
    for i in range(len(input_query)):
            veh_one_inputs[i] = (input(input_query[i]))
            veh_two_inputs[i] = ""

if sim_type == 'MV':
    for j in range (2):
        print(f'<=== Inputs for vehicle {j} ===>')
        for i in range(len(input_query)):
            if j == 0:
                veh_one_inputs[i] = (input(input_query[i]))
            if j == 1:
                veh_two_inputs[i] = (input(input_query[i]))

if (sim_type != 'SV' or sim_type != 'MV'):
    print('Incorrect Simulation Type. Use "SV" or "MV" only.')

veh1_data = dict(zip(veh_inputs, veh_one_inputs))
veh2_data = dict(zip(veh_inputs, veh_two_inputs))

project_data = {}
project_data['info'] = info
project_data['veh1'] = veh1_data
project_data['veh2'] = veh2_data

os.chdir('/home/joemcormier/github/pycrash/data')
# test if ProjectData.pkl exists
if path.exists("ProjectData.pkl") == True:
    with open('ProjectData.pkl', 'rb') as handle:
        allProjectData = pickle.load(handle)
    # add new project to data file
    allProjectData[pname] = project_data
elif path.exists("ProjectData.pkl") == False:
    # create new file for saving project data
    allProjectData = {}
    allProjectData[pname] = project_data


with open('ProjectData.pkl', 'wb') as handle:
    pickle.dump(allProjectData, handle, protocol=pickle.HIGHEST_PROTOCOL)


# extract vehicle data
def vehData(ProjectName):
    if ProjectDatabase[ProjectName]['info']['sim_type'] == 'SV':
        VehData = ProjectDatabase[ProjectName]['veh1']
        return veh1
    else:
        veh1 = ProjectDatabase[ProjectName]['veh1']
        veh2 = ProjectDatabase[ProjectName]['veh2']
        return veh1, veh2


# make a change to a given field
def updateinfo(ProjectName, Vehicle, Field, NewValue):
"""
loads project database / updates values / saves database
"""
    os.chdir('/home/joemcormier/github/pycrash/data')

    with open('ProjectData.pkl', 'rb') as handle:
        allProjectData = pickle.load(handle)

    allProjectData[ProjectName][Vehicle][Field] = NewValue

    with open('ProjectData.pkl', 'wb') as handle:
        pickle.dump(allProjectData, handle, protocol=pickle.HIGHEST_PROTOCOL)


vehData(pname)
