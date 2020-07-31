
# %%
import os
path_parent = os.path.dirname(os.getcwd())
validation_dir = os.path.join(path_parent, "validation")
os.chdir(validation_dir)

import numpy as np
from nptdms import TdmsFile
from pprint import pprint
import matplotlib.pyplot as plt
import plotly.graph_objects as go
from varname import varname, nameof
# %% list of test folders

test_dir = ['2020FordExplorer_smalloverlapCEN1908',
'FordTaurusintoFordTarus']


# %% Select test for analysis
valdiation_test_no = 1
print(f'Running Analysis for {test_dir[valdiation_test_no]}')
print("")

data_dir = os.path.join(validation_dir, 'sources', test_dir[valdiation_test_no], 'data')

# get list of data files
data_files = os.listdir(data_dir)
print(f'Data Files: {pprint(data_files)}')

# %% Open tdms data file - Vehicle A

iihs_data = data_files[7]
tdms_file = TdmsFile.read(os.path.join(data_dir, iihs_data))

tdms_file.properties

# %% assign filtered data - Vehicle A
fdataA = tdms_file['Filtered Data']
vehAax = fdataA['11VEHC0000__ACXD'][:]
vehAay = fdataA['11VEHC0000__ACYD'][:]
vehAaz = fdataA['11VEHC0000__ACZD'][:]

# %% Calculated Channels
calcedA = tdms_file['Calculated Channels']

# %% Open tdms data file - Vehicle B

iihs_data = data_files[17]
tdms_file = TdmsFile.read(os.path.join(data_dir, iihs_data))

tdms_file.properties

# %% assign filtered data - Vehicle A
fdataB = tdms_file['Filtered Data']
vehBax = fdataB['11VEHC0000__ACXD'][:]
vehBay = fdataB['11VEHC0000__ACYD'][:]
vehBaz = fdataB['11VEHC0000__ACZD'][:]

# %% Calculated Channels
calcedB = tdms_file['Calculated Channels']



# %% create time array
time = np.arange(-0.05, 0.35, 0.0001)

# %%

plt.plot(time, vehBax, 'b', time, vehBay, 'g', time, vehBaz, 'k')

# %%
def plt_common_x(data_list):
    """
    where data_list must have common time as first entry
    """
    fig = go.Figure()

    # Add traces
    time = data_list[0]
    data = data_list[1:]

    for trace in data:
        fig.add_trace(go.Scatter(x = time, y = trace,
                            mode='lines',
                            name=nameof(trace))
                     )


    fig.update_layout(
        autosize=False,
        width=800,
        height=450,
        title = 'IIHS Vehicle Data',
        template = 'plotly_white',
        xaxis = dict(showgrid = False, title = 'Time (s)'),
        yaxis = dict(showgrid = False, title = 'Acceleration (g)'),
        font = dict(family = 'Arial', size = 16, color = 'black'),
    )

    fig.update_xaxes(showline=True, linewidth=1, linecolor='black', ticks="outside", tickwidth=1, tickcolor='black', ticklen=10)
    fig.update_yaxes(showline=True, linewidth=1, linecolor='black', ticks="outside", tickwidth=1, tickcolor='black', ticklen=10, zeroline=False)
    fig.show()

# %%
plt_common_x([time, vehBax, vehBay, vehBaz])

# %%
from varname import nameof
