"""
plots used witin vehicle class
"""
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import math

# TODO: create input for figure size - loads from "defaults" folder?
figure_size = (800, 450)

wheel_colors = ['rgb(0, 0, 255)', 'rgb(0, 255, 0)', 'rgb(153, 0, 204)', 'rgb(255, 102, 0)']


def tire_details(veh):
    fig = make_subplots(rows=2, cols=1,
                        shared_xaxes=True,
                        vertical_spacing=0.11)

    # tire center plot depends on lock condition
    def setdash(x):
        if x == 0:
            return 'dash'
        elif x == 1:
            return 'solid'

    # slip angle
    fig.add_trace(go.Scatter(x=veh.model.t, y=veh.model.lf_alpha * 180 / math.pi,
                             mode='lines',
                             name='LF',
                             line=dict(color=wheel_colors[0], width=1,
                                       dash='solid')),
                  row=1, col=1)
    fig.add_trace(go.Scatter(x=veh.model.t, y=veh.model.rf_alpha * 180 / math.pi,
                             mode='lines',
                             name='RF',
                             line=dict(color=wheel_colors[1], width=1,
                                       dash='solid')),
                  row=1, col=1)
    fig.add_trace(go.Scatter(x=veh.model.t, y=veh.model.rr_alpha * 180 / math.pi,
                             mode='lines',
                             name='RR',
                             line=dict(color=wheel_colors[2], width=1,
                                       dash='solid')),
                  row=1, col=1)
    fig.add_trace(go.Scatter(x=veh.model.t, y=veh.model.lr_alpha * 180 / math.pi,
                             mode='lines',
                             name='LR',
                             line=dict(color=wheel_colors[3], width=1,
                                       dash='solid')),
                  row=1, col=1)
    # locked Status
    fig.add_trace(go.Scatter(x=veh.model.t, y=veh.model.lf_lock,
                             showlegend=False,
                             mode='lines',
                             name='LF',
                             line=dict(color=wheel_colors[0], width=1,
                                       dash='solid')),
                  row=2, col=1)

    fig.add_trace(go.Scatter(x=veh.model.t, y=veh.model.rf_lock,
                             showlegend=False,
                             mode='lines',
                             name='RF',
                             line=dict(color=wheel_colors[1], width=1,
                                       dash='solid')),
                  row=2, col=1)

    fig.add_trace(go.Scatter(x=veh.model.t, y=veh.model.rr_lock,
                             showlegend=False,
                             mode='lines',
                             name='RR',
                             line=dict(color=wheel_colors[2], width=1,
                                       dash='solid')),
                  row=2, col=1)

    fig.add_trace(go.Scatter(x=veh.model.t, y=veh.model.lr_lock,
                             showlegend=False,
                             mode='lines',
                             name='LR',
                             line=dict(color=wheel_colors[3], width=1,
                                       dash='solid')),
                  row=2, col=1)

    fig.update_layout(
        legend=dict(orientation="h", yanchor='top', y=1.15, xanchor='left', x=0.01),
        autosize=False,
        width=figure_size[0],
        height=figure_size[1],
        title='Tire Slip Angle & Saturation (locked) Status',
        template='plotly_white',
        font=dict(family='Arial', size=16, color='black'))

    fig.update_xaxes(showline=True, linewidth=1, linecolor='black', ticks="outside",
                     tickwidth=1, tickcolor='black', ticklen=10, zeroline=False)
    fig.update_yaxes(showline=True, linewidth=1, linecolor='black', ticks="outside",
                     tickwidth=1, tickcolor='black', ticklen=10, zeroline=False)
    fig.update_xaxes(showgrid=False, title_text='Time (s)', row=2, col=1)
    fig.update_xaxes(showgrid=False, title_text='', row=1, col=1)
    fig.update_yaxes(showgrid=False, title_text='Locked Satus', row=2, col=1)
    fig.update_yaxes(showgrid=False, title_text='Slip Angle (degrees)', row=1, col=1)

    fig.show()


def vertical_forces(veh):
    fig = go.Figure()

    fig.add_trace(go.Scatter(x=veh.model.t, y=veh.model.lf_fz,
                             mode='lines',
                             name='LF',
                             line=dict(color=wheel_colors[0], width=1,
                                       dash='solid')))
    fig.add_trace(go.Scatter(x=veh.model.t, y=veh.model.rf_fz,
                             mode='lines',
                             name='RF',
                             line=dict(color=wheel_colors[1], width=1,
                                       dash='solid')))
    fig.add_trace(go.Scatter(x=veh.model.t, y=veh.model.rr_fz,
                             mode='lines',
                             name='RR',
                             line=dict(color=wheel_colors[2], width=1,
                                       dash='solid')))
    fig.add_trace(go.Scatter(x=veh.model.t, y=veh.model.lr_fz,
                             mode='lines',
                             name='LR',
                             line=dict(color=wheel_colors[3], width=1,
                                       dash='solid')))
    fig.update_layout(
        legend=dict(orientation="h", yanchor='top', y=1.15, xanchor='left', x=0.01),
        autosize=False,
        width=figure_size[0],
        height=figure_size[1],
        title='Vertical Tire Forces',
        template='plotly_white',
        font=dict(family='Arial', size=16, color='black'))

    fig.update_xaxes(showline=True, linewidth=1, linecolor='black', ticks="outside",
                     tickwidth=1, tickcolor='black', ticklen=10, zeroline=False, title_text='Time (s)')
    fig.update_yaxes(showline=True, linewidth=1, linecolor='black', ticks="outside",
                     tickwidth=1, tickcolor='black', ticklen=10, zeroline=False, title_text='Vertical Force (lb)')

    fig.show()


def long_forces(veh):
    fig = go.Figure()

    fig.add_trace(go.Scatter(x=veh.model.t, y=veh.model.lf_fx,
                             mode='lines',
                             name='LF',
                             line=dict(color=wheel_colors[0], width=1,
                                       dash='solid')))
    fig.add_trace(go.Scatter(x=veh.model.t, y=veh.model.rf_fx,
                             mode='lines',
                             name='RF',
                             line=dict(color=wheel_colors[1], width=1,
                                       dash='solid')))
    fig.add_trace(go.Scatter(x=veh.model.t, y=veh.model.rr_fx,
                             mode='lines',
                             name='RR',
                             line=dict(color=wheel_colors[2], width=1,
                                       dash='solid')))
    fig.add_trace(go.Scatter(x=veh.model.t, y=veh.model.lr_fx,
                             mode='lines',
                             name='LR',
                             line=dict(color=wheel_colors[3], width=1,
                                       dash='solid')))
    fig.update_layout(
        legend=dict(orientation="h", yanchor='top', y=1.15, xanchor='left', x=0.01),
        autosize=False,
        width=figure_size[0],
        height=figure_size[1],
        title='Forward Tire Forces',
        template='plotly_white',
        font=dict(family='Arial', size=16, color='black'))

    fig.update_xaxes(showline=True, linewidth=1, linecolor='black', ticks="outside",
                     tickwidth=1, tickcolor='black', ticklen=10, zeroline=False, title_text='Time (s)')
    fig.update_yaxes(showline=True, linewidth=1, linecolor='black', ticks="outside",
                     tickwidth=1, tickcolor='black', ticklen=10, zeroline=False, title_text='Forward Force (lb)')

    fig.show()
