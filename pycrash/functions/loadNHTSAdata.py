# Load NHTSA asii data file
"""
when downloading the ascii data from NHTSA, it will include a .EV5 file, this had the channel info
"""

import os
import pickle
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from scipy import integrate
from pycrash.functions.CFCFilter import cfcfilt


test_num = 10146
data_dir = 'C:\\Users\\jcormier.BIOCORE\\Desktop\\NHTSAData\\v10146ascii'  # will be also used to save data
format_file = f'v{test_num}.EV5'
impact_velocity = 57.09  # test impact speed [kph]

english_units = False
if english_units:
    accel_convert = 32.2
    impact_velocity = impact_velocity * 0.911344  # convert kph to fps
else:
    accel_convert = 9.81
    impact_velocity = impact_velocity * 0.277778  # convert kph to m/s

# find lines with instrumentation info
with open(os.path.join(data_dir, format_file)) as myFile:
    for num, line in enumerate(myFile, 1):
        if 'INSTRUMENTATION' in line:
            print(f'Instrumentation data found at line: {num}')
            instStart = num
        elif '- END -' in line:
            print(f'Instrumentation data found at line: {num}')
            instEnd = num

# find info for barrier data Fx
test_data = {}  # <- dictionary of load cell data
with open(os.path.join(data_dir, format_file)) as myFile:
    for num, line in enumerate(myFile, 1):
        # search for load cell barrier channels
        if (num > instStart) & (num < instEnd) & ('Fx' in line) & ('BARRIER' in line):
            #print(line.split('|'))
            channel_name = line.split('|')[-1].replace('\n','')
            channel_num = int(line.split('|')[1])
            lc_row = channel_name[8]
            lc_col = int(channel_name[10:12])
            print(f'Channel: {channel_name} #{channel_num} at row: {lc_row}, col: {lc_col}')
            test_data[channel_name] = {'type':'LC',
                                       'num':channel_num,
                                       'row':lc_row,
                                       'col':lc_col,
                                       'fileName':f'v{test_num}.{channel_num}'}
        # search for vehicle crossmember acceleration data Ax
        elif (num > instStart) & (num < instEnd) & ('REAR SEAT CROSSMEMBER X' in line):
            channel_name = line.split('|')[-1].replace('\n','')
            channel_num = int(line.split('|')[1])
            print(f'Channel: {channel_name} #{channel_num}')
            if channel_num > 99:
                fileName = f'v{test_num}.{channel_num}'
            elif (channel_num <= 99) & (channel_num > 9):
                fileName = f'v{test_num}.0{channel_num}'
            elif channel_num <= 9:
                fileName = f'v{test_num}.00{channel_num}'
            test_data[channel_name] = {'type':'Accel',
                                       'name':channel_name,
                                       'num':channel_num,
                                       'loc':'Crossmember',
                                       'dir':'x',
                                       'fileName':fileName}


# load data and load cell data for desired rows
row_list = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K']
for key, value in test_data.items():
    if value['type'] == 'LC':
        if (value['row'] in row_list) & ('No valid data' in key):
            print(f'No valid data: {key}')
            test_data[key]['colName'] = f'{value["row"]}_{value["col"]}'
            test_data[key]['time'] = timeData
            test_data[key]['rawforce'] = [0] * len(timeData) # set force to zero if missing
            test_data[key]['rawforce'] = [0] * len(timeData) # set force to zero if missing
            test_data[key]['force'] = [0] * len(timeData)
        elif (value['row'] in row_list) & ('No valid data' not in key):
            print(f'loading file {value["fileName"]}')
            #df = pd.read_csv(os.path.join(data_dir, value["fileName"]), names=['time','data'], sep='\t')
            # load file with numpy
            data_array = np.loadtxt(os.path.join(data_dir, value["fileName"]), delimiter='\t')
            all_time = list(data_array[:, 0])
            all_data = list(data_array[:, 1])
            zero_time_index = all_time.index(0)
            time = all_time[zero_time_index:]
            data = all_data[zero_time_index:]
            test_data[key]['colName'] = f'{value["row"]}_{value["col"]}'
            test_data[key]['time'] = time
            test_data[key]['rawforce'] = data
            test_data[key]['force'] = cfcfilt(60, data, time[1]-time[0])
            timeData = time
    elif value['type'] == 'Accel':
        #df = pd.read_csv(os.path.join(data_dir, value["fileName"]), names=['time', 'data'], sep='\t')
        data_array = np.loadtxt(os.path.join(data_dir, value["fileName"]), delimiter='\t')
        all_time = list(data_array[:, 0])
        all_data = list(data_array[:, 1])
        zero_time_index = all_time.index(0)
        time = all_time[zero_time_index:]
        data = all_data[zero_time_index:]
        test_data[key]['colName'] = value['name']
        test_data[key]['time'] = time
        test_data[key]['rawAccel'] = data
        filtered_accel = cfcfilt(60, data, time[1] - time[0])
        test_data[key]['Accel'] = filtered_accel # filtered acceleration [g]
        accel_ = [x * accel_convert for x in filtered_accel]
        velocity = integrate.cumtrapz(accel_, time, initial=0)
        velocity = [x + impact_velocity for x in velocity]
        #displacement = integrate.cumtrapz(velocity, time, initial=0)
        test_data[key]['Velocity'] = velocity  # velocity [fps / m/s]
        test_data[key]['Displacement'] = integrate.cumtrapz(velocity, time, initial=0)
        #test_data[key]['Displacement'] = [x - displacement[0] for x in displacement]  # 0 at 0 displacement [ft / mm]


# create dictionary of filtered force
forceDict = {}
forceDict['time'] = test_data[next(iter(test_data))]['time']
for key, value in test_data.items():
    if value['type'] == 'LC':
        #print(value['colName'])
        forceDict[value['colName']] = value['force']  # filtered force data

# convert to dataframe
forceDF = pd.DataFrame.from_dict(forceDict)
# fix columns with missing data
for label, content in forceDF.items():
    if sum(content) == 0:
        print(f'Column {label} = 0')

forceDF.F_1 = forceDF.F_2
forceDF.C_4 = np.mean([forceDF.C_3, forceDF.C_5])

# sum by row
row_list = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K']
column_list = list(np.arange(1, 17))

for row in row_list:
    sum_columns = [row + "_" + str(s) for s in column_list]
    forceDF[f'{row}_Sum'] = forceDF[sum_columns].sum(axis=1)

# get velocity / displacement data
AccelDict = {}
AccelDict['time'] = test_data[next(iter(test_data))]['time']
for key, value in test_data.items():
    if value['type'] == 'Accel':
        print(value['colName'])
        AccelDict[value['colName']] = value['Accel']  # filtered acceleration [g]
        AccelDict[f"{value['colName']} Velocity"] = value['Velocity']  # velocity [fps]
        AccelDict[f"{value['colName']} Disp"] = value['Displacement']  # displacement [ft]

AccelDF = pd.DataFrame.from_dict(AccelDict)

AccelDF.plot(x='time', y = 'LEFT REAR SEAT CROSSMEMBER X', figsize=(12,7))
plt.show()
AccelDF.plot(x='time', y = 'LEFT REAR SEAT CROSSMEMBER X Velocity', figsize=(12,7))
plt.show()
AccelDF.plot(x='time', y = 'LEFT REAR SEAT CROSSMEMBER X Disp', figsize=(12,7))
plt.show()


# save
with open(os.path.join(data_dir, f'ProcessedNHTSATestData_{test_num}.pkl'), 'wb') as handle:
    pickle.dump(test_data, handle, protocol=pickle.HIGHEST_PROTOCOL)

# %% Combined data by columns -
# sum by row
rowForce = {}
rowForce['time'] = test_data[next(iter(test_data))]['time']
rowSum = [0] * len(test_data[next(iter(test_data))]['time'])
currentRow = 'K'
for key, value in test_data.items():
    if value['type'] == 'LC':
        if value['row'] == currentRow:
            rowSum = [a + b for a, b in zip(rowSum, value['force'])]
            rowForce[value['row']] = rowSum
        else:
            rowSum = [0] * len(test_data[next(iter(test_data))]['time'])
            rowSum = [a + b for a, b in zip(rowSum, value['force'])]
            rowForce[value['row']] = rowSum
            currentRow = value['row']


RowForcedf = pd.DataFrame.from_dict(rowForce)


# merge force and displacement df
Fdx = pd.merge(RowForcedf, AccelDF, how = 'left', on='time')
Fdx.to_pickle(os.path.join(data_dir, f'Force_DisplacementNHTSA_Test_{test_num}.pkl'))

Fdx.plot(x='time', y = 'LEFT REAR SEAT CROSSMEMBER X', figsize=(12,7))
plt.show()