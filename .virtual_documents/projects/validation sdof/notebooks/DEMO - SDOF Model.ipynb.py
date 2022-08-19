# commands for Jupyter Notebook
# get_ipython().run_line_magic("%", " allow reloading of modules")
get_ipython().run_line_magic("load_ext", " autoreload")
get_ipython().run_line_magic("autoreload", " 2")


import pandas as pd
pd.options.display.max_columns = None
import plotly.figure_factory as ff
import plotly.graph_objects as go
import plotly.io as pio
pio.renderers.default = "plotly_mimetype"  # <- determines how plots are displayed using Plotly


import sys
sys.path.insert(0, '< path to pycrash >')  # if not installing with pip


import pycrash
from pycrash.sdof_model_mc import SDOF_Model
from pycrash.project import Project, project_info, load_project
from pycrash.vehicle import Vehicle
from pycrash.visualization.sdof_plot import plot_velocity, plot_acceleration, plot_fdx, plot_vehicle_fdx
from pycrash.functions.ar import cipriani_rest # get restitution


project_info('validation sdof')


proj = load_project('validation sdof')


# minimal vehicle data is needed for SDOF model:


veh1 = Vehicle('Striking')
veh1.year = 2020
veh1.make = 'Honda'
veh1.model = 'Civic'
veh1.weight = 3500
veh1.brake = 0
veh1.vx_initial = 5


veh2 = Vehicle('Struck')
veh2.year = 2020
veh2.make = 'Honda'
veh2.model = 'Civic'
veh2.weight = 3500
veh2.brake = 0
veh2.vx_initial = 0


# create model inputs:
v1_vx_initial = [5, 7, 10]  # initial speeds for striking vehicle
run_list_names = ['Low', 'Average', 'High']
cor_list = [cipriani_rest(x) for x in v1_vx_initial]  # low restitution from sideswipe
# stiffness values determined in Demo = Basic Functions
k_mutual = 27734
k_mutual_low = k_mutual - 9512
k_mutual_high = k_mutual + 9512
k_model_list = [k_mutual_low, k_mutual, k_mutual_high]
models =[None] * len(run_list_names)  # create empty list for model runs

k_veh2 = 51479  # stiffness for rear of Vehicle 2
k_veh2_low = 26145
k_veh2_high = 97875
veh2_stiffnes_list = [k_veh2_low, k_veh2, k_veh2_high]


for i in range(len(v1_vx_initial)):

    model_inputs = {"name": run_list_names[i],
            "k": k_model_list[i],
            "cor": cor_list[i],
            "tstop": 0.117
        }
    # closing speed
    veh1.vx_initial = v1_vx_initial[i]
    # assign individual stiffness values to get vehicle-specific crush
    veh1.k = 60127
    veh2.k = veh2_stiffnes_list[i]
    models[i] = SDOF_Model(veh1, veh2, model_inputs=model_inputs)


plot_fdx(models)


# assign individual stiffness values to get vehicle-specific crush

plot_vehicle_fdx(models)  # <- vehicle specific Fdx


# plot velocity
plot_velocity(models, fill_diff = True, show_legend = False)


# plot acceleration
plot_acceleration(models, fill_diff = True, show_legend = False)


from pycrash.sdof_calcs.sodf_montecarlo import SDOF_MonteCarlo



num_iter = 200  # <- number of interations
name_prefix = 'run_'
# stiffness data: car-to-car
model_inputs = {'kmutual': {'type': 'normal',  # <- normal distribution
                            'data': [27734, 9512]},     # <- mean, std dev
                'cor': {'type': 'cipriani', 'data': 'cipriani'},    # <- use Cipriani fit to get restitution
                'initial_velocity': {'type': 'range',
                                     'data': [10, 10]}    # <- will create a uniform distribution of values between 5 and 10
                }
sim = SDOF_MonteCarlo(veh1, veh2, name_prefix, model_inputs=model_inputs, k1=None, k2=None)


sim.run_simulation(num_iter)


sim.results



sim.results['veh2_DV']


fig = ff.create_distplot([sim.results['veh1_DV'], sim.results['veh2_DV']], group_labels=['Vehicle 1', 'Vehicle 2'], bin_size=.2)
fig.update_layout(
                    showlegend=True,
                    autosize=False,
                    width=900,
                    height=700,
                    title=f'Delta-V Distribution (n={num_iter})',
                    template='plotly_white',
                    xaxis=dict(showgrid=False, title='Delta-V (mph)'),
                    yaxis=dict(showgrid=False, title='Density'),
                    font=dict(family='Arial', size=22, color='black'))
fig.update_xaxes(showline=True, linewidth=1, linecolor='black', ticks="outside",
                 tickwidth=1, tickcolor='black', ticklen=10, zeroline=False)
fig.update_yaxes(showline=True, linewidth=1, linecolor='black', ticks="outside",
                 tickwidth=1, tickcolor='black', ticklen=10, zeroline=False)
fig.show()


fig = ff.create_distplot([sim.results['residual_crush']], group_labels=['Residual Crush'], bin_size=.2)
fig.update_layout(
                    showlegend=False,
                    autosize=False,
                    width=900,
                    height=700,
                    title=f'Residual Mutual Crush (n={num_iter})',
                    template='plotly_white',
                    xaxis=dict(showgrid=False, title='Mutual Crush (inches)'),
                    yaxis=dict(showgrid=False, title='Density'),
                    font=dict(family='Arial', size=22, color='black'))
fig.update_xaxes(showline=True, linewidth=1, linecolor='black', ticks="outside",
                 tickwidth=1, tickcolor='black', ticklen=10, zeroline=False)
fig.update_yaxes(showline=True, linewidth=1, linecolor='black', ticks="outside",
                 tickwidth=1, tickcolor='black', ticklen=10, zeroline=False)
fig.show()



fig = go.Figure(data=[go.Box(y=sim.results['residual_crush'],
            name='Car to Car Simulation',
            boxpoints='all',
            jitter=0.3,
            pointpos=-1.8,
            notched=True,
            boxmean=True,
            marker_color='green'
              )])
fig.update_layout(
                    showlegend=False,
                    autosize=False,
                    width=900,
                    height=700,
                    title=f'Residual Mutual Crush (n={num_iter})',
                    template='plotly_white',
                    xaxis=dict(showgrid=False, title=''),
                    yaxis=dict(showgrid=False, title='Residual Crush (inches)'),
                    font=dict(family='Arial', size=22, color='black'))
fig.update_xaxes(showline=True, linewidth=1, linecolor='black', ticks="outside",
                 tickwidth=1, tickcolor='black', ticklen=10, zeroline=False)
fig.update_yaxes(showline=True, linewidth=1, linecolor='black', ticks="outside",
                 tickwidth=1, tickcolor='black', ticklen=10, zeroline=False, range=[0, -15])
fig.show()



