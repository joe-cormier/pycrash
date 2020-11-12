"""
functions for plotting data related to vehicle kinematics
"""

import plotly.graph_objects as go
from plotly.subplots import make_subplots
import plotly.io as pio

pio.renderers.default = "browser"  # <- determines how plots are displayed using Plotly

figure_size = (1200, 700)
font_size = 18
"""
vehicle motion - single vehicle
"""


def plot_model(self):
    """
    takes SingleMotion class variable as input
    """

    fig = make_subplots(rows=2, cols=1,
                        shared_xaxes=True,
                        vertical_spacing=0.05)
    # velocity data
    fig.add_trace(go.Scatter(x=self.model.t, y=self.model.Vx / 1.46667,
                             mode='lines',
                             name='X',
                             line=dict(color='rgb(0, 255, 0)', width=2)),
                  row=1, col=1)
    fig.add_trace(go.Scatter(x=self.model.t, y=self.model.Vy / 1.46667,
                             mode='lines',
                             name='Y',
                             line=dict(color='rgb(0, 0, 255)', width=2)),
                  row=1, col=1)
    fig.add_trace(go.Scatter(x=self.model.t, y=self.model.Vr / 1.46667,
                             mode='lines',
                             name='Resultant',
                             line=dict(color='rgb(0, 0, 0)', width=2)),
                  row=1, col=1)
    # acceleration data
    fig.add_trace(go.Scatter(x=self.model.t, y=self.model.Ax / 32.2,
                             showlegend=False,
                             mode='lines',
                             name='Ax',
                             line=dict(color='rgb(0, 255, 0)', width=2)),
                  row=2, col=1)
    fig.add_trace(go.Scatter(x=self.model.t, y=self.model.Ay / 32.2,
                             showlegend=False,
                             mode='lines',
                             name='Ay',
                             line=dict(color='rgb(0, 0, 255)', width=2)),
                  row=2, col=1)
    fig.add_trace(go.Scatter(x=self.model.t, y=self.model.Ar / 32.2,
                             showlegend=False,
                             mode='lines',
                             name='Ar',
                             line=dict(color='rgb(0, 0, 0)', width=2)),
                  row=2, col=1)

    fig.update_layout(
        legend=dict(orientation="h", yanchor='top', y=1.1, xanchor='left', x=0.01),
        autosize=False,
        width=figure_size[0],
        height=figure_size[1],
        title=f'{self.name} - Inertial Frame Velocity | Acceleration',
        template='plotly_white',
        xaxis=dict(showgrid=False, title='Time (s)'),
        yaxis=dict(showgrid=False),
        font=dict(family='Arial', size=font_size, color='black'))

    fig.update_xaxes(showgrid=False, title_text='Time (s)', row=2, col=1)
    fig.update_xaxes(showgrid=False, title_text='', row=1, col=1)
    fig.update_yaxes(showgrid=False, title_text='Velocity (mph)', row=1, col=1)
    fig.update_yaxes(showgrid=False, title_text='Acceleration (g)', row=2, col=1)
    fig.update_xaxes(showline=True, linewidth=1, linecolor='black', ticks="outside",
                     tickwidth=1, tickcolor='black', ticklen=10, zeroline=False)
    fig.update_yaxes(showline=True, linewidth=1, linecolor='black', ticks="outside",
                     tickwidth=1, tickcolor='black', ticklen=10, zeroline=False)
    fig.show()

    fig = make_subplots(rows=2, cols=1,
                        shared_xaxes=True,
                        vertical_spacing=0.05)

    # velocity data in vehicle frame
    fig.add_trace(go.Scatter(x=self.model.t, y=self.model.vx / 1.46667,
                             mode='lines',
                             name='x',
                             line=dict(color='rgb(0, 255, 0)', width=2)),
                  row=1, col=1)
    fig.add_trace(go.Scatter(x=self.model.t, y=self.model.vy / 1.46667,
                             mode='lines',
                             name='y',
                             line=dict(color='rgb(0, 0, 255)', width=2)),
                  row=1, col=1)

    # acceleration data
    fig.add_trace(go.Scatter(x=self.model.t, y=self.model.ax / 32.2,
                             showlegend=False,
                             mode='lines',
                             name='ax',
                             line=dict(color='rgb(0, 255, 0)', width=2)),
                  row=2, col=1)
    fig.add_trace(go.Scatter(x=self.model.t, y=self.model.ay / 32.2,
                             showlegend=False,
                             mode='lines',
                             name='ay',
                             line=dict(color='rgb(0, 0, 255)', width=2)),
                  row=2, col=1)

    fig.update_layout(
        legend=dict(orientation="h", yanchor='top', y=1.1, xanchor='left', x=0.01),
        autosize=False,
        width=figure_size[0],
        height=figure_size[1],
        title=f'{self.name} - Vehicle Frame Velocity | Acceleration',
        template='plotly_white',
        xaxis=dict(showgrid=False, title='Time (s)'),
        yaxis=dict(showgrid=False),
        font=dict(family='Arial', size=font_size, color='black'))

    fig.update_xaxes(showgrid=False, title_text='Time (s)', row=2, col=1)
    fig.update_xaxes(showgrid=False, title_text='', row=1, col=1)
    fig.update_yaxes(showgrid=False, title_text='Velocity (mph)', row=1, col=1)
    fig.update_yaxes(showgrid=False, title_text='Acceleration (g)', row=2, col=1)
    fig.update_xaxes(showline=True, linewidth=1, linecolor='black', ticks="outside",
                     tickwidth=1, tickcolor='black', ticklen=10, zeroline=False)
    fig.update_yaxes(showline=True, linewidth=1, linecolor='black', ticks="outside",
                     tickwidth=1, tickcolor='black', ticklen=10, zeroline=False)
    fig.show()

    fig = make_subplots(rows=2, cols=1,
                        shared_xaxes=True,
                        vertical_spacing=0.05)

    # forward tire forces
    fig.add_trace(go.Scatter(x=self.model.t, y=self.model.lf_fx,
                             mode='lines',
                             name='LF',
                             line=dict(color='rgb(0, 0, 255)', width=2)),
                  row=1, col=1)
    fig.add_trace(go.Scatter(x=self.model.t, y=self.model.rf_fx,
                             mode='lines',
                             name='RF',
                             line=dict(color='rgb(0, 255, 0)', width=2)),
                  row=1, col=1)
    fig.add_trace(go.Scatter(x=self.model.t, y=self.model.rr_fx,
                             mode='lines',
                             name='RR',
                             line=dict(color='rgb(153, 0, 204)', width=2)),
                  row=1, col=1)
    fig.add_trace(go.Scatter(x=self.model.t, y=self.model.lr_fx,
                             mode='lines',
                             name='LR',
                             line=dict(color='rgb(255, 102, 0)', width=2)),
                  row=1, col=1)

    # rightward tire forces
    fig.add_trace(go.Scatter(x=self.model.t, y=self.model.lf_fy,
                             showlegend=False,
                             mode='lines',
                             name='LF',
                             line=dict(color='rgb(0, 0, 255)', width=2)),
                  row=2, col=1)
    fig.add_trace(go.Scatter(x=self.model.t, y=self.model.rf_fy,
                             showlegend=False,
                             mode='lines',
                             name='RF',
                             line=dict(color='rgb(0, 255, 0)', width=2)),
                  row=2, col=1)
    fig.add_trace(go.Scatter(x=self.model.t, y=self.model.rr_fy,
                             showlegend=False,
                             mode='lines',
                             name='RR',
                             line=dict(color='rgb(153, 0, 204)', width=2)),
                  row=2, col=1)
    fig.add_trace(go.Scatter(x=self.model.t, y=self.model.lr_fy,
                             showlegend=False,
                             mode='lines',
                             name='LR',
                             line=dict(color='rgb(255, 102, 0)', width=2)),
                  row=2, col=1)

    fig.update_layout(
        legend=dict(orientation="h", yanchor='top', y=1.1, xanchor='left', x=0.01),
        autosize=False,
        width=figure_size[0],
        height=figure_size[1],
        title=f'{self.name} - Tire Forces',
        template='plotly_white',
        xaxis=dict(showgrid=False, title='Time (s)'),
        yaxis=dict(showgrid=False),
        font=dict(family='Arial', size=font_size, color='black'))

    fig.update_xaxes(showgrid=False, title_text='Time (s)', row=2, col=1)
    fig.update_xaxes(showgrid=False, title_text='', row=1, col=1)
    fig.update_yaxes(showgrid=False, title_text='Forward (lb)', row=1, col=1)
    fig.update_yaxes(showgrid=False, title_text='Rightward (lb)', row=2, col=1)
    fig.update_xaxes(showline=True, linewidth=1, linecolor='black', ticks="outside",
                     tickwidth=1, tickcolor='black', ticklen=10, zeroline=False)
    fig.update_yaxes(showline=True, linewidth=1, linecolor='black', ticks="outside",
                     tickwidth=1, tickcolor='black', ticklen=10, zeroline=False)
    fig.show()

    fig = make_subplots(rows=2, cols=1,
                        shared_xaxes=True,
                        vertical_spacing=0.07)

    # heading
    fig.add_trace(go.Scatter(x=self.model.t, y=self.model.theta_deg,
                             mode='lines',
                             name='heading',
                             line=dict(color='rgb(0, 0, 0)', width=2)),
                  row=1, col=1)

    # rotational
    fig.add_trace(go.Scatter(x=self.model.t, y=self.model.oz_deg,
                             mode='lines',
                             name='omega',
                             line=dict(color='rgb(0, 255, 0)', width=2)),
                  row=2, col=1)
    fig.add_trace(go.Scatter(x=self.model.t, y=self.model.alphaz_deg,
                             mode='lines',
                             name='alpha',
                             line=dict(color='rgb(204, 0, 0)', width=2)),
                  row=2, col=1)

    fig.update_layout(
        legend=dict(orientation="h", yanchor='top', y=1.1, xanchor='left', x=0.01),
        autosize=False,
        width=figure_size[0],
        height=figure_size[1],
        title=f'{self.name} Heading and Rotation',
        template='plotly_white',
        xaxis=dict(showgrid=False, title='Time (s)'),
        yaxis=dict(showgrid=False),
        font=dict(family='Arial', size=font_size, color='black'))

    fig.update_xaxes(showgrid=False, title_text='Time (s)', row=2, col=1)
    fig.update_xaxes(showgrid=False, title_text='', row=1, col=1)
    fig.update_yaxes(showgrid=False, title_text='Heading (deg)', row=1, col=1)
    fig.update_yaxes(showgrid=False, title_text='Omega (deg/s), Alpha (deg/s/s)', row=2, col=1)

    fig.update_xaxes(showline=True, linewidth=1, linecolor='black', ticks="outside",
                     tickwidth=1, tickcolor='black', ticklen=10, zeroline=False)
    fig.update_yaxes(showline=True, linewidth=1, linecolor='black', ticks="outside",
                     tickwidth=1, tickcolor='black', ticklen=10, zeroline=False)
    fig.show()
