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
    fig.add_trace(go.Scatter(x = self.veh1.t, y = self.veh1.Dx,
                            mode = 'lines',
                            name = f'{veh1.name} - X',
                            line = dict(color = 'rgb(0, 255, 0)', width = 2)),
                            row = 1, col = 1)
    fig.add_trace(go.Scatter(x = self.veh2.t, y = self.veh2.Dx,
                            mode = 'lines',
                            name = f'{veh2.name} - X',
                            line = dict(color = 'rgb(0, 255, 0)', width = 2, dash='dash')),
                            row = 1, col = 1)

    fig.add_trace(go.Scatter(x = self.veh1.t, y = self.veh1.Dy,
                            mode = 'lines',
                            name = f'{veh1.name} - Y',
                            line = dict(color = 'rgb(0, 0, 255)', width = 2)),
                            row = 1, col = 1)
    fig.add_trace(go.Scatter(x = self.veh2.t, y = self.veh2.Dy,
                            mode = 'lines',
                            name = f'{veh2.name} - Y',
                            line = dict(color = 'rgb(0, 0, 255)', width = 2, dash='dash')),
                            row = 1, col = 1)
    # Heading angle
    fig.add_trace(go.Scatter(x = self.veh1.t, y = self.veh1.theta_deg,
                            mode = 'lines',
                            name = f'{veh1.name} - heading',
                            line = dict(color = 'rgb(0, 0, 0)', width = 2)),
                            row = 2, col = 1)
    fig.add_trace(go.Scatter(x = self.veh2.t, y = self.veh2.theta_deg,
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
    fig.add_trace(go.Scatter(x = self.veh1.t, y = self.veh1.Vx / 1.46667,
                            mode = 'lines',
                            name = f'{veh1.name} - X',
                            line = dict(color = 'rgb(0, 255, 0)', width = 2)),
                            row = 1, col = 1)
    fig.add_trace(go.Scatter(x = self.veh2.t, y = self.veh2.Vx / 1.46667,
                            mode = 'lines',
                            name = f'{veh2.name} - X',
                            line = dict(color = 'rgb(0, 255, 0)', width = 2, dash='dash')),
                            row = 1, col = 1)

    fig.add_trace(go.Scatter(x = self.veh1.t, y = self.veh1.Vy / 1.46667,
                            mode = 'lines',
                            name = f'{veh1.name} - Y',
                            line = dict(color = 'rgb(0, 0, 255)', width = 2)),
                            row = 1, col = 1)
    fig.add_trace(go.Scatter(x = self.veh2.t, y = self.veh2.Vy / 1.46667,
                            mode = 'lines',
                            name = f'{veh2.name} - Y',
                            line = dict(color = 'rgb(0, 0, 255)', width = 2, dash='dash')),
                            row = 1, col = 1)
    # Heading angle
    # TODO: calculate vehicle slip angle
    fig.add_trace(go.Scatter(x = self.veh1.t, y = self.veh1.theta_deg,
                            mode = 'lines',
                            name = f'{veh1.name} - heading',
                            line = dict(color = 'rgb(0, 0, 0)', width = 2)),
                            row = 2, col = 1)
    fig.add_trace(go.Scatter(x = self.veh2.t, y = self.veh2.theta_deg,
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
