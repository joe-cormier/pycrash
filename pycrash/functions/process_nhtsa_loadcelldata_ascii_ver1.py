import os
import pickle
import pandas as pd
import numpy as np
from scipy import integrate
from pycrash.functions.CFCFilter import cfcfilt


def process_loadcell_asii(test_num, path, row_list, num_columns, impact_speed, english=True):
    """

    this version using the keyword "BARRIER" to locate load cell data within the .EV5 file
    if you file does not have this, try ver2
    download the NHTSA asii data into a single directory
    test_num -> NHTSA test number
    path -> path to directory containing asii files, including the .EV5 file
    row_list -> list containing row names (alphabetical) to be including in processing
    num_columns -> number of columns (integer)
    impact_velocity - barrier impact speed [kph]
    outputs will be saved in same directory
    defaults to English units, can be set to False
    will print cells that are missing data

    """

    format_file = f'v{test_num}.EV5'  # file containing channel info
    if english:
        accel_convert = 32.2
        impact_velocity = impact_speed * 0.911344  # convert kph to fps
        force_convert = 0.224809
    else:
        accel_convert = 9.81
        impact_velocity = impact_speed * 0.277778  # convert kph to m/s
        force_convert = 1

    # find lines with instrumentation info
    with open(os.path.join(path, format_file)) as myFile:
        for num, line in enumerate(myFile, 1):
            if 'INSTRUMENTATION' in line:
                print(f'Instrumentation data found at line: {num}')
                instStart = num
            elif '- END -' in line:
                print(f'Instrumentation data found at line: {num}')
                instEnd = num

    # find info for barrier data Fx
    test_data = {}  # <- dictionary of load cell data
    with open(os.path.join(path, format_file)) as myFile:
        for num, line in enumerate(myFile, 1):
            # search for load cell barrier channels
            if (num > instStart) & (num < instEnd) & ('Fx' in line) & ('BARRIER' in line):
                # print(line.split('|'))
                channel_name = line.split('|')[-1].replace('\n', '')
                channel_num = int(line.split('|')[1])
                lc_row = channel_name[8]
                lc_col = int(channel_name[10:12])
                print(f'Channel: {channel_name} #{channel_num} at row: {lc_row}, col: {lc_col}')
                test_data[channel_name] = {'type': 'LC',
                                           'num': channel_num,
                                           'row': lc_row,
                                           'col': lc_col,
                                           'fileName': f'v{test_num}.{channel_num}'}

            # search for vehicle crossmember acceleration data Ax
            elif (num > instStart) & (num < instEnd) & ('REAR SEAT CROSSMEMBER X' in line):
                channel_name = line.split('|')[-1].replace('\n', '')
                channel_num = int(line.split('|')[1])
                print(f'Channel: {channel_name} #{channel_num}')
                if channel_num > 99:
                    fileName = f'v{test_num}.{channel_num}'
                elif (channel_num <= 99) & (channel_num > 9):
                    fileName = f'v{test_num}.0{channel_num}'
                elif channel_num <= 9:
                    fileName = f'v{test_num}.00{channel_num}'
                test_data[channel_name] = {'type': 'Accel',
                                           'name': channel_name,
                                           'num': channel_num,
                                           'loc': 'Crossmember',
                                           'dir': 'x',
                                           'fileName': fileName}

    # load data and load cell data for desired rows
    for key, value in test_data.items():
        if value['type'] == 'LC':
            if (value['row'] in row_list) & ('No valid data' in key):
                print(f'No valid data: {key}')
                test_data[key]['colName'] = f'{value["row"]}_{value["col"]}'
                test_data[key]['time'] = timeData
                test_data[key]['rawforce'] = [0] * len(timeData)  # set force to zero if missing
                test_data[key]['rawforce'] = [0] * len(timeData)  # set force to zero if missing
                test_data[key]['force'] = [0] * len(timeData)
            elif (value['row'] in row_list) & ('No valid data' not in key):
                print(f'loading file {value["fileName"]}')
                # load file with numpy
                data_array = np.loadtxt(os.path.join(path, value["fileName"]), delimiter='\t')
                all_time = list(data_array[:, 0])
                all_data = list(data_array[:, 1])
                zero_time_index = all_time.index(0)
                time = all_time[zero_time_index:]
                data = all_data[zero_time_index:]
                test_data[key]['colName'] = f'{value["row"]}_{value["col"]}'
                test_data[key]['time'] = time
                test_data[key]['rawforce'] = [x * force_convert for x in data]
                test_data[key]['force'] = cfcfilt(60, [x * force_convert for x in data], time[1] - time[0])
                timeData = time
        elif value['type'] == 'Accel':
            data_array = np.loadtxt(os.path.join(path, value["fileName"]), delimiter='\t')
            all_time = list(data_array[:, 0])
            all_data = list(data_array[:, 1])
            zero_time_index = all_time.index(0)
            time = all_time[zero_time_index:]
            data = all_data[zero_time_index:]
            test_data[key]['colName'] = value['name']
            test_data[key]['time'] = time
            test_data[key]['rawAccel'] = data
            filtered_accel = cfcfilt(60, data, time[1] - time[0])
            test_data[key]['Accel'] = filtered_accel  # filtered acceleration [g]
            accel_ = [x * accel_convert for x in filtered_accel]
            velocity = integrate.cumtrapz(accel_, time, initial=0)
            velocity = [x + impact_velocity for x in velocity]
            test_data[key]['Velocity'] = velocity  # velocity [fps / m/s]
            test_data[key]['Displacement'] = integrate.cumtrapz(velocity, time, initial=0)

    # create dictionary of filtered force
    forceDict = {}
    forceDict['time'] = test_data[next(iter(test_data))]['time']
    for key, value in test_data.items():
        if value['type'] == 'LC':
            # print(value['colName'])
            forceDict[value['colName']] = value['force']  # filtered force data

    # convert to dataframe
    forceDF = pd.DataFrame.from_dict(forceDict)
    print(f'Column Names in Force data: {list(forceDF)}')
    # fix columns with missing data
    for label, content in forceDF.items():
        if sum(content) == 0:
            print(f'Column {label} = 0')
            average_list = [str(x) for x in input("Enter a list of column names to average to replace missing data: (example: C_3, C_5)").split(', ')]
            if len(average_list) == 1:
                print(f'Assigning missing column data to column {average_list[0]}')
                forceDF.loc[:, label] = forceDF.loc[:, average_list[0]].copy()
            else:
                forceDF.loc[:, label] = forceDF[average_list].mean(axis=1)

    column_list = list(np.arange(1, num_columns))
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
            AccelDict[f"{value['colName']} Velocity"] = value['Velocity']  # velocity [fps, mps]
            AccelDict[f"{value['colName']} Disp"] = value['Displacement']  # displacement [ft, m]

    AccelDF = pd.DataFrame.from_dict(AccelDict)

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
    # merge summed forces and displacement df
    Fdx = pd.merge(RowForcedf, AccelDF, how='left', on='time')
    Fdx.to_pickle(os.path.join(path, f'RowSum_ProcessedNHTSA_Test_{test_num}.pkl'))

    # all force data with accel / displacement df
    test_data_accel = pd.merge(forceDF, AccelDF, how='left', on='time')
    test_data_accel.to_pickle(os.path.join(path, f'ProcessedNHTSATestData_{test_num}.pkl'))

    print("Processing Complete - Files Saved to Path Provided")
