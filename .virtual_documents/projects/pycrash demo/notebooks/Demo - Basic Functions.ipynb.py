# if running without installing from pip - insert path to pycrash here
import sys
sys.path.insert(0, '< your path >')


# jupyter notebook option - imports modules when changes are made
get_ipython().run_line_magic("load_ext", " autoreload")
get_ipython().run_line_magic("autoreload", " 2")


import pandas as pd
pd.options.display.max_columns = None  # show all dataframe columns
import numpy as np
from sklearn.linear_model import LinearRegression


import pycrash.functions.ar as ar
import pycrash.functions.arPlots as arplot


w1 = 3000     # <- vehicle 1 weight [lbs] (striking)
w2 = 5000     # <- vehicle 2 weight [lbs] (struck)
v1 = 10       # <- vehicle 1 initial speed [mph]
v2 = 0        # <- vehicle 2 initial speed [mph]

restitution = ar.cipriani_rest(v1-v2)    # <- solve for restitution using Cipriani et al. (2002) fit
ar.StrikingDV(w1, w2, v1, v2, restitution)

# print statement:
print(f'Striking vehicle change in speed: {StrikingDV(w1, w2, v1, v2, rest):0.1f} mph with restitution of: {restitution:0.2f}')


# import Vehicle module
from pycrash.vehicle import Vehicle


# create vehicle
veh1 = Vehicle('Malibu')
veh1.year = 2015
veh1.make = 'Chevrolet'
veh1.model = 'Malibu'
veh1.weight = 3639

# show what is stored inside "veh1"
veh1.show()


# retrieve value stored in vehicle class:
veh1.weight
print(f'The weight of {veh1.name} is: {veh1.weight} lbs')


# import crash_plot function
from pycrash.functions.vehicle_stiffness import crash_plot


# get_ipython().run_line_magic("%", " Create crash plot for A / B stiffness values")
# initialize crash plot data
abscissa = np.array([])
ordinate = np.array([])

# create inputs for crash plot function
# get_ipython().run_line_magic("%", " create test with zero crush at 3 mph - only returns a single value for intercept at 0 crush")
crush_length = 1415 * 0.0393701  # crush width [inches]

# 6 point crush profile
c_list = [0] * 6                # no crush
test_speed = 3                  # no crush speed [mph]
restitution = 0

test_data = {'test_crush':c_list,
             'test_speed':test_speed,
             'damage_length':crush_length,
             'epsilon':restitution}

x_no_damage, y_no_damage = crash_plot(test_data, veh1)
abscissa = np.append(abscissa, x_no_damage)  # append values to the array
ordinate = np.append(ordinate, y_no_damage)  # append values to the array

# crush measurements [inches], say average crush depth
c1 = 10.1
c2 = 10.1
c3 = 10.1
c4 = 10.1
c5 = 10.1
c6 = 10.1

crush_length = 1415 * 0.0393701  # crush width [inches]
# 6 point crush profile
c_list = [c1, c2, c3, c4, c5, c6]  # list of crush measurements

test_speed = 56.51 * 0.621371 # [mph]
restitution = 0.013           # <- from test data

# input data is put into a python dictionary for input
test_data = {'test_crush':c_list,
             'test_speed':test_speed,
             'damage_length':crush_length,
             'epsilon':restitution}

# crash_plot function returns the x,y values associated with the crash plot
ave_x, ave_y = crash_plot(test_data, veh1)
abscissa = np.append(abscissa, ave_x)  # append values to the array
ordinate = np.append(ordinate, ave_y)  # append values to the array

# add another data point to crash plot -
c1 = 13
c2 = 13
c3 = 13
c4 = 13
c5 = 13
c6 = 13

crush_length = 1415 * 0.0393701  # crush width [inches]

# 6 point crush profile
c_list = [c1, c2, c3, c4, c5, c6]

test_speed = 60 * 0.621371 # [mph]
restitution = 0.008  # <- from test data

test_data = {'test_crush':c_list,
             'test_speed':test_speed,
             'damage_length':crush_length,
             'epsilon':restitution
}

x_new, y_new = crash_plot(test_data, veh1)

abscissa = np.append(abscissa, x_new)  # append values to the array
ordinate = np.append(ordinate, y_new)  # append values to the array


# linear regression of crash plot data
model = LinearRegression().fit(abscissa.reshape((-1, 1)), ordinate)

# calculate A and B values:
A = (model.coef_ * model.intercept_).item()
B = (model.coef_** 2).item()

# assign A + B values to veh1
veh1.A = A
veh1.B = B

# data for crash plot
crash_plot_x = [*range(0, int(round(max(abscissa))) + 2, 1)]
crash_plot_y = [x * model.coef_.item() + model.intercept_ for x in crash_plot_x]


# import plotly
import plotly.graph_objects as go
# tell plotly to use browser for plotting
# if you are using jupyter notebook, then "notebook" will work for an option.
# otherwise, Pycharm and Jupyter Lab get along better with "browser"
import plotly.io as pio
pio.renderers.default = "plotly_mimetype"  # <- determines how plots are displayed using Plotly
#pio.renderers.default = "browser"  # <- determines how plots are displayed using Plotly


# get_ipython().run_line_magic("%", " Create crash plot for A / B stiffness values")
fig = go.Figure()
# velocity data
fig.add_trace(go.Scatter(x = abscissa, y = ordinate,
                        mode = 'markers',
                        name = '2015 Malibu',
                        marker = dict(color = 'rgb(102, 255, 51)', size = 8)))
fig.add_trace(go.Scatter(x = crash_plot_x, y = crash_plot_y,
                        mode = 'lines',
                        name = 'regression',
                        line = dict(color = 'rgb(67,67,67)', width = 2)))
fig.add_annotation(x = 2,
                    y = 200,
                    showarrow = False,
                    text = f"A = {A:.0f} lb/in<br>B = {B:.0f} lb/in/in")

fig.update_layout(
    legend=dict(
    yanchor="bottom",
    y=0.1,
    xanchor="left",
    x=0.7),
    autosize = False,
    width = 2000,
    height = 1100,
    title = 'Crash Plot',
    #template = 'plotly_white',  # turn off / on background color / grid
    xaxis = dict(showgrid = True, title = '(form factor) * average crush (in)'),
    yaxis = dict(showgrid = True, title = 'Energy Crush Factor'),
    font = dict(family = 'Arial', size = 16, color = 'black'))


# load modules
import os # operating system interface - used to change directories and create paths
import pycrash.functions.process_nhtsa_loadcelldata_ascii_ver1 as load_cell


# this test was missing data for two load cells, so F_1 was set to F_2 and C_4 was taken as the average of C_3 and C_5
# the function will ask for inputs to handle missing data
# the respective entries are F_1 and C_3, C_5

test_num = 10146
path = os.path.join(os.getcwd(), 'data', 'input', f'v{test_num}ascii')  # create path input
row_list = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K']     # list of rows to be processed
num_columns = 17                                                       # number of load cell columns
impact_velocity = 57.09  # test impact speed [kph]


# two dataframes are produced, one containing the force across all columns summed
# the other contains the processed force data for each load cell
load_cell.process_loadcell_asii(test_num, path, row_list, num_columns, impact_velocity, english=True)


# individual forces:
force_dx = pd.read_pickle(os.path.join(path, f'ProcessedNHTSATestData_{test_num}.pkl'))
# first five rows:
force_dx.head()


# summed row data
summed_dx = pd.read_pickle(os.path.join(path, f'RowSum_ProcessedNHTSA_Test_{test_num}.pkl'))
# rename column for displacement to be more friendly:
summed_dx.rename(columns = {'LEFT REAR SEAT CROSSMEMBER X Disp': 'Disp'}, inplace=True)
# first five rows:
summed_dx.head()


summed_dx['TotalForce'] = summed_dx[row_list].sum(axis=1)
arplot.plot_TotalFdx(summed_dx)


# import function for integrating load cell data
from pycrash.functions.ar import CrushEnergyInt
print(f'Total Crush Energy: {CrushEnergyInt(summed_dx.Disp, summed_dx.TotalForce *-1):0.0f} ft-lb')


# import function to get barrier impact speed from weight and energy
from pycrash.functions.ar import BEVfromE
print(f'BEV from integrated load cell barrier energy: {BEVfromE(3330, CrushEnergyInt(summed_dx.Disp, summed_dx.TotalForce *-1)):0.1f} mph')


# example, take sum of 3 rows of load cell data  -
# sum all rows
summed_dx['Force'] = summed_dx[['F', 'G', 'H']].sum(axis=1)
veh1_fdx = summed_dx[['time', 'Disp', 'Force']].copy()  # create separate dataframe for analysis
veh1_fdx = veh1_fdx[veh1_fdx.time < 0.021].copy()  # select force up to about 1 foot of crush


# use Bonugli for mutual stiffness value
from IPython.display import display, Image
display(Image(filename=os.path.join(os.getcwd(), 'visualization', 'Bonugli2017.jpg')))


# as an example, take Car to Car
k_mutual = 27734
k_mutual_low = k_mutual - 9512
k_mutual_high = k_mutual + 9512
# create arrays to plot
displacement = [0, 1]
f_mutual = [0, k_mutual]
f_mutual_low = [0, k_mutual_low]
f_mutual_high = [0, k_mutual_high]


# get initial stiffness value from load cell data
# get displacement at max force value in the first foot of crush
veh1_disp = veh1_fdx.loc[veh1_fdx.Force == veh1_fdx.Force.min(), 'Disp'].item()
print(f'Vehicle 1 Displacement at initial max force: {veh1_disp:0.3f} feet')


veh1_fdx_half = veh1_fdx[veh1_fdx.time < 0.010].copy()  # select force up to about 1/2 foot of crush
veh1_disp_half = veh1_fdx_half.loc[veh1_fdx_half.Force == veh1_fdx_half.Force.min(), 'Disp'].item()
print(f'Vehicle 1 Displacement at initial max force to half a foot: {veh1_disp_half:0.3f} feet')


# create initial stiffness for vehicle 1:
k_veh1 = -1 * veh1_fdx.Force.min() / veh1_disp  # [lb/ft]
f_veh1 = [0, k_veh1]
print(f'Stiffness of striking vehicle: {k_veh1:0.1f} lb/ft')


fig = go.Figure()
fig.add_trace(go.Scatter(x = veh1_fdx.Disp,
                         y = veh1_fdx.Force * -1,
                        mode = 'lines',
                        name = "Total Force",
                        line = dict(color = "rgb(52, 64, 235)", width = 2)
                        ))
fig.add_trace(go.Scatter(x = [0, veh1_disp],
                         y = [0, veh1_fdx.Force.min() * -1],
                        mode = 'lines',
                        name = "Linear Stiffness (1 ft)",
                        line = dict(color = "rgb(0, 0, 100)", width = 2)
                        ))
fig.add_trace(go.Scatter(x = [0, veh1_disp_half],
                         y = [0, veh1_fdx_half.Force.min() * -1],
                        mode = 'lines',
                        name = "Linear Stiffness (1/2 ft)",
                        line = dict(color = "rgb(0, 0, 100)", width = 2, dash = 'dash')
                        ))
fig.update_layout(
    autosize = False,
    width = 1000,
    height = 550,
    title = f'Load Cell Barrier Force-Displacement Data - First foot of crush',
    template = 'plotly_white',
    xaxis = dict(showgrid = False, title = 'Displacement (feet)'),
    font = dict(family = 'Arial', size = 24, color = 'black'))

fig.update_layout(showlegend = False)
fig.update_yaxes(showgrid = False, showline=True, linewidth=1, linecolor='black', ticks="outside",
                 tickwidth=1, tickcolor='black', ticklen=10, zeroline=False, title_text = 'Force (lb)')
fig.update_xaxes(showline=True, linewidth=1, linecolor='black', ticks="outside",
                 tickwidth=1, tickcolor='black', ticklen=10, zeroline=False)
fig.show()


from pycrash.functions.ar import SpringSeriesKeff  # calculates mutual stiffness given stiffness value for each vehicle
# get_ipython().run_line_magic("%", " md")
#### Example using Scipy optimize


from scipy.optimize import minimize


# create function to minimize
def objective_func(k_veh2):
    return (27734 - SpringSeriesKeff(60127.1, k_veh2))**2  # error between calculated mutual stiffness versus desired

minimize(objective_func, 30000)


# try result from minimize
SpringSeriesKeff(51479, k_veh1)


k_veh2 = 51479  # stiffness for rear of Vehicle 2
k_veh2_low = 26145
k_veh2_high = 97875
# repeat above to get high / low values of k_veh2
def objective_func(k_veh2):
    return (k_mutual_high - SpringSeriesKeff(60127.1, k_veh2))**2 # error between calculated mutual stiffness versus desired

minimize(objective_func, 30000)


fig = go.Figure()
fig.add_trace(go.Scatter(x = displacement,
                         y = f_veh1,
                        mode = 'lines',
                        name = 'Striking Vehicle Stiffness - Load Cell Derived',
                        line = dict(color = "rgb(0, 0, 0)", width = 3, dash = 'solid')
                        ))
fig.add_trace(go.Scatter(x = displacement,
                         y = f_mutual,
                        mode = 'lines',
                        name = 'Average Mutual Stiffness (Bonugli 2017)',
                        line = dict(color = "rgb(50, 115, 168)", width = 3, dash = 'solid')
                        ))
fig.add_trace(go.Scatter(x = displacement,
                         y = [0, k_mutual_high],
                        mode = 'lines',
                        name = 'Mutual Stiffness - High',
                        line = dict(color = "rgb(50, 115, 168)", width = 3, dash = 'dash')
                        ))
fig.add_trace(go.Scatter(x = displacement,
                         y = [0, k_mutual_low],
                        mode = 'lines',
                        name = 'Mutual Stiffness - Low',
                        line = dict(color = "rgb(50, 115, 168)", width = 3, dash = 'dash')
                        ))
fig.update_layout(legend = dict(orientation = "v", yanchor = 'top', y = 1, xanchor = 'left', x = 0),
    autosize = False,
    width = 1400,
    height = 800,
    title = f'Force Displacement Response for Impact Model',
    template = 'plotly_white',
    xaxis = dict(showgrid = False, title = 'Displacement (feet)'),
    font = dict(family = 'Arial', size = 28, color = 'black'))

fig.update_layout(showlegend = True)
fig.update_yaxes(showgrid = False, showline=True, linewidth=1, linecolor='black', ticks="outside",
                 tickwidth=1, tickcolor='black', ticklen=10, zeroline=False, range = [0, 60000], title_text = 'Force (lb)')
fig.update_xaxes(showline=True, linewidth=1, linecolor='black', ticks="outside",
                 tickwidth=1, tickcolor='black', ticklen=10, zeroline=False)
fig.show()



