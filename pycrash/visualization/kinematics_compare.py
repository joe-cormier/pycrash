"""
functions for plotting data related to vehicle kinematics for multiple vehicles
"""
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import math
# TODO: create input for figure size - loads from "defaults" folder?
figure_size = (800,450)

def compare_kinematics(veh1, veh2):
    fig = make_subplots(rows = 2, cols = 1,
                    shared_xaxes = True,
                    vertical_spacing = 0.07)

    # CG translations
    fig.add_trace(go.Scatter(x = veh1.model.t, y = veh1.model.Dx,
                            mode = 'lines',
                            name = f'{veh1.name} - X',
                            line = dict(color = 'rgb(0, 255, 0)', width = 2)),
                            row = 1, col = 1)
    fig.add_trace(go.Scatter(x = veh2.model.t, y = veh2.model.Dx,
                            mode = 'lines',
                            name = f'{veh2.name} - X',
                            line = dict(color = 'rgb(0, 255, 0)', width = 2, dash='dash')),
                            row = 1, col = 1)

    fig.add_trace(go.Scatter(x = veh1.model.t, y = veh1.model.Dy,
                            mode = 'lines',
                            name = f'{veh1.name} - Y',
                            line = dict(color = 'rgb(0, 0, 255)', width = 2)),
                            row = 1, col = 1)
    fig.add_trace(go.Scatter(x = veh2.model.t, y = veh2.model.Dy,
                            mode = 'lines',
                            name = f'{veh2.name} - Y',
                            line = dict(color = 'rgb(0, 0, 255)', width = 2, dash='dash')),
                            row = 1, col = 1)
    # Heading angle
    fig.add_trace(go.Scatter(x = veh1.model.t, y = veh1.model.theta_deg,
                            mode = 'lines',
                            name = f'{veh1.name} - heading',
                            line = dict(color = 'rgb(0, 0, 0)', width = 2)),
                            row = 2, col = 1)
    fig.add_trace(go.Scatter(x = veh2.model.t, y = veh2.model.theta_deg,
                            mode = 'lines',
                            name = f'{veh2.name} - heading',
                            line = dict(color = 'rgb(0, 0, 0)', width = 2, dash='dash')),
                            row = 2, col = 1)

    fig.update_layout(
        legend = dict(orientation = "h", yanchor = 'top', y = 1.1, xanchor = 'left', x = 0.01),
        autosize=False,
        width = 900,
        height = 500,
        template = 'plotly_white',
        yaxis = dict(showgrid = False),
        font = dict(family = 'Arial', size = 14, color = 'black'))

    fig.update_xaxes(showgrid = False, title_text = 'Time (s)', row = 2, col = 1)
    fig.update_xaxes(showgrid = False, title_text = '', row = 1, col = 1)
    fig.update_yaxes(showgrid = False, title_text = 'Displacement (ft)', row = 1, col = 1)
    fig.update_yaxes(showgrid = False, title_text = 'Heading Angle (deg)', row = 2, col = 1)
    fig.update_xaxes(showline=True, linewidth=1, linecolor='black', ticks="outside",
                     tickwidth=1, tickcolor='black', ticklen=10, zeroline=False)
    fig.update_yaxes(showline=True, linewidth=1, linecolor='black', ticks="outside",
                     tickwidth=1, tickcolor='black', ticklen=10, zeroline=False)
    fig.show()

    """
    velocity
    slip angle
    """
    fig = make_subplots(rows = 2, cols = 1,
                    shared_xaxes = True,
                    vertical_spacing = 0.07)

    # CG translations
    fig.add_trace(go.Scatter(x = veh1.model.t, y = veh1.model.Vx / 1.46667,
                            mode = 'lines',
                            name = f'{veh1.name} - X',
                            line = dict(color = 'rgb(0, 255, 0)', width = 2)),
                            row = 1, col = 1)
    fig.add_trace(go.Scatter(x = veh2.model.t, y = veh2.model.Vx / 1.46667,
                            mode = 'lines',
                            name = f'{veh2.name} - X',
                            line = dict(color = 'rgb(0, 255, 0)', width = 2, dash='dash')),
                            row = 1, col = 1)

    fig.add_trace(go.Scatter(x = veh1.model.t, y = veh1.model.Vy / 1.46667,
                            mode = 'lines',
                            name = f'{veh1.name} - Y',
                            line = dict(color = 'rgb(0, 0, 255)', width = 2)),
                            row = 1, col = 1)
    fig.add_trace(go.Scatter(x = veh2.model.t, y = veh2.model.Vy / 1.46667,
                            mode = 'lines',
                            name = f'{veh2.name} - Y',
                            line = dict(color = 'rgb(0, 0, 255)', width = 2, dash='dash')),
                            row = 1, col = 1)
    # Slip angle - compare to beta_deg
    fig.add_trace(go.Scatter(x = veh1.model.t, y = veh1.model.vehicleslip_deg,
                            mode = 'lines',
                            name = f'{veh1.name} - heading',
                            line = dict(color = 'rgb(0, 0, 0)', width = 2)),
                            row = 2, col = 1)
    fig.add_trace(go.Scatter(x = veh2.model.t, y = veh2.model.vehicleslip_deg,
                            mode = 'lines',
                            name = f'{veh2.name} - heading',
                            line = dict(color = 'rgb(0, 0, 0)', width = 2, dash='dash')),
                            row = 2, col = 1)

    fig.update_layout(
        legend = dict(orientation = "h", yanchor = 'top', y = 1.1, xanchor = 'left', x = 0.01),
        autosize=False,
        width = 900,
        height = 500,
        template = 'plotly_white',
        yaxis = dict(showgrid = False),
        font = dict(family = 'Arial', size = 14, color = 'black'))

    fig.update_xaxes(showgrid = False, title_text = 'Time (s)', row = 2, col = 1)
    fig.update_xaxes(showgrid = False, title_text = '', row = 1, col = 1)
    fig.update_yaxes(showgrid = False, title_text = 'Velocity (mph)', row = 1, col = 1)
    fig.update_yaxes(showgrid = False, title_text = 'Slip Angle (deg)', row = 2, col = 1)
    fig.update_xaxes(showline=True, linewidth=1, linecolor='black', ticks="outside",
                     tickwidth=1, tickcolor='black', ticklen=10, zeroline=False)
    fig.update_yaxes(showline=True, linewidth=1, linecolor='black', ticks="outside",
                     tickwidth=1, tickcolor='black', ticklen=10, zeroline=False)
    fig.show()

    fig = make_subplots(rows = 4, cols = 1,
                    shared_xaxes = True,
                    vertical_spacing = 0.05)

    """
    right tire forces
    """
    fig.add_trace(go.Scatter(x = veh1.model.t, y = veh1.model.lf_fy,
                            mode = 'lines',
                            name = 'LF - Pycrash',
                            line = dict(color = 'rgb(0, 0, 255)', width = 2)),
                            row = 1, col = 1)
    fig.add_trace(go.Scatter(x = veh2.model.t, y = veh2.model.lf_fy,
                            mode = 'lines',
                            name = 'LF - Validate',
                            line = dict(color = 'rgb(0, 0, 255)', width = 2, dash = 'dash')),
                            row = 1, col = 1)
    fig.add_trace(go.Scatter(x = veh1.model.t, y = veh1.model.rf_fy,
                            mode = 'lines',
                            name = 'RF - Pycrash',
                            line = dict(color = 'rgb(0, 255, 0)', width = 2)),
                            row = 2, col = 1)
    fig.add_trace(go.Scatter(x = veh2.model.t, y = veh2.model.rf_fy,
                            mode = 'lines',
                            name = 'RF - Validate',
                            line = dict(color = 'rgb(0, 255, 0)', width = 2, dahs = 'dash')),
                            row = 2, col = 1)
    fig.add_trace(go.Scatter(x = veh1.model.t, y = veh2.model.rr_fy,
                            mode = 'lines',
                            name = 'RR - Pycrash',
                            line = dict(color = 'rgb(153, 0, 204)', width = 2)),
                            row = 3, col = 1)
    fig.add_trace(go.Scatter(x = veh2.model.t, y = veh2.model.rr_fy,
                            mode = 'lines',
                            name = 'RR - Validate',
                            line = dict(color = 'rgb(153, 0, 204)', width = 2, dahs = 'dash')),
                            row = 3, col = 1)
    fig.add_trace(go.Scatter(x = veh1.model.t, y = veh1.model.lr_fy,
                            mode = 'lines',
                            name = 'LR - Pycrash',
                            line = dict(color = 'rgb(255, 102, 0)', width = 2)),
                            row = 4, col = 1)
    fig.add_trace(go.Scatter(x = veh2.model.t, y = veh2.model.lr_fy,
                            mode = 'lines',
                            name = 'LR - Validate',
                            line = dict(color = 'rgb(255, 102, 0)', width = 2, dahs = 'dash')),
                            row = 4, col = 1)

    fig.update_layout(
        legend = dict(orientation = "h", yanchor = 'top', y = 1.1, xanchor = 'left', x = 0.01),
        autosize=False,
        width = 900,
        height = 500,
        title = f'{self.name} - Tire Rightward Forces',
        template = 'plotly_white',
        xaxis = dict(showgrid = False),
        yaxis = dict(showgrid = False),
        font = dict(family = 'Arial', size = 14, color = 'black'))

    fig.update_xaxes(showgrid = False, title_text = 'Time (s)', row = 4, col = 1,
                    showline=True, linewidth=1, linecolor='black', ticks="outside",
                     tickwidth=1, tickcolor='black', ticklen=10, zeroline=False)
    fig.update_xaxes(showgrid = False, title_text = '', row = 1, col = 1,
                     showline=True, linewidth=1, linecolor='black', ticks="outside",
                     tickwidth=1, tickcolor='black', ticklen=10, zeroline=False)
    fig.update_xaxes(showgrid = False, title_text = '', row = 2, col = 1,
                     showline=True, linewidth=1, linecolor='black', ticks="outside",
                     tickwidth=1, tickcolor='black', ticklen=10, zeroline=False)
    fig.update_xaxes(showgrid = False, title_text = '', row = 3, col = 1,
                     showline=True, linewidth=1, linecolor='black', ticks="outside",
                     tickwidth=1, tickcolor='black', ticklen=10, zeroline=False)
    fig.update_yaxes(showgrid = False, title_text = 'RF - Rightward Force (lb)', row = 1, col = 1,
                     showline=True, linewidth=1, linecolor='black', ticks="outside",
                     tickwidth=1, tickcolor='black', ticklen=10, zeroline=False)
    fig.update_yaxes(showgrid = False, title_text = 'LF - Rightward Force (lb)', row = 2, col = 1,
                     showline=True, linewidth=1, linecolor='black', ticks="outside",
                     tickwidth=1, tickcolor='black', ticklen=10, zeroline=False)
    fig.update_yaxes(showgrid = False, title_text = 'RR - Rightward Force (lb)', row = 3, col = 1,
                     showline=True, linewidth=1, linecolor='black', ticks="outside",
                     tickwidth=1, tickcolor='black', ticklen=10, zeroline=False)
    fig.update_yaxes(showgrid = False, title_text = 'LR - Rightward Force (lb)', row = 4, col = 1,
                     showline=True, linewidth=1, linecolor='black', ticks="outside",
                     tickwidth=1, tickcolor='black', ticklen=10, zeroline=False)
    fig.show()
