"""
create vehicle velocity / displacement given an acceleration profile and heading
vehicle will follow steer angle regardless of speed
"""
import numpy as np
import pandas as pd
from scipy import integrate
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import plotly.io as pio

pio.renderers.default = "browser"
figure_size = (1200, 700)
font_size = 18


steer_ratio = 20

# inputs
time = [0, 1, 2, 3, 4.4, 4.6, 5]
throttle = [0.08, 0.08, 0.08, 0.08, 0.08, 0, 0]
brake = [0, 0, 0, 0, 0, 0.8, 0.8]
steer = [0, 360, 360+90, 360+180, 360+180, 360+180, 360+180]


def time_inputs(time, throttle, brake, steer, init_vel=0, dt_motion=0.01, show_plot=True):
    """
    Driver inputs | time (s) | throttle (g) | braking (g) | steering (deg) |
    braking is positive
    braking will always override throttle
    """
    inputdf = pd.DataFrame(list(zip(throttle, brake, steer)), columns=['throttle', 'brake', 'steer'])
    t = list(np.arange(0, max(time) + dt_motion, dt_motion))  # create time array from 0 to max time in inputs, does not mean simulation will stop at this time_inputs
    t = [float(i) for i in t]
    df = pd.DataFrame()  # create dataframe for vehicle input with interpolated values
    df['t'] = t
    inputdf['input_t'] = [float(num) for num in time]
    df.t = df.t.round(3).astype(float)
    df = pd.merge(df, inputdf, how='left', left_on='t', right_on='input_t')  # merge input data with time data at specified time step
    df = df.interpolate(method='linear', axis=0)  # interpolate NaN values left after merging
    df.drop(columns=['input_t', 't'], inplace=True)  # drop input time column
    df['t'] = t  # reset time column due to interpolating
    df['t'] = df.t.round(3)  # reset significant digits
    df = df.reset_index(drop=True)

    if show_plot:
        fig = make_subplots(specs=[[{"secondary_y": True}]])

        fig.add_trace(go.Scatter(x=df.t, y=df.throttle,
                                 mode='lines',
                                 name='throttle',
                                 line=dict(color='rgb(0, 255, 0)', width=2)),
                      secondary_y=False)
        fig.add_trace(go.Scatter(x=df.t, y=df.brake,
                                 mode='lines',
                                 name='brake',
                                 line=dict(color='rgb(255, 0, 0)', width=2)),
                      secondary_y=False)
        fig.add_trace(go.Scatter(x=df.t, y=df.steer,
                                 mode='lines',
                                 name='steer',
                                 line=dict(color='rgb(0, 0, 0)', width=2)),
                      secondary_y=True)

        fig.update_layout(
            legend=dict(orientation="h", yanchor='top', y=1.05, xanchor='left', x=0.45),
            autosize=False,
            width=figure_size[0],
            height=figure_size[1],
            title=f'Driver Inputs',
            template='plotly_white',
            xaxis=dict(showgrid=False, title='Time (s)'),
            yaxis=dict(showgrid=False),
            font=dict(family='Arial', size=font_size, color='black'))

        fig.update_yaxes(showgrid=False, title_text='Steer Angle (deg)', secondary_y=True)
        fig.update_yaxes(showgrid=False, title_text='Brake | Throttle', secondary_y=False)

        fig.update_xaxes(showline=True, linewidth=1, linecolor='black', ticks="outside",
                         tickwidth=1, tickcolor='black', ticklen=10, zeroline=False,
                         tickfont=dict(size=14))
        fig.update_yaxes(showline=True, linewidth=1, linecolor='black', ticks="outside",
                         tickwidth=1, tickcolor='black', ticklen=10, zeroline=False,
                         tickfont=dict(size=14))
        fig.show()

    # tire angle
    df['delta_deg'] = [x / steer_ratio for x in df.steer]
    df['delta_rad'] = [x * np.pi / 180 for x in df.delta_deg]

    # overall accel - braking always overrides accel
    df['accel'] = np.where(df.brake > 0, -1 * df.brake, df.throttle)
    df['accel_x'] = [np.cos(x) * y for x, y in zip(df.delta_rad, df.accel)]
    df['accel_y'] = [np.sin(x) * y for x, y in zip(df.delta_rad, df.accel)]

    df['accel_x_fps'] = df.accel_x.mul(32.2)
    df['accel_y_fps'] = df.accel_y.mul(32.2)
    df['accel_fps'] = df.accel.mul(32.2)

    # integrate acceleration to get velocity
    print(f'Initial Velocity: {init_vel} mph')
    init_vel_fps = init_vel * 1.46667
    df['vx'] = integrate.cumtrapz(list(df.accel_x_fps), list(df.t), initial=0)
    df['vy'] = integrate.cumtrapz(list(df.accel_y_fps), list(df.t), initial=0)
    df['v'] = init_vel_fps + integrate.cumtrapz(list(df.accel_fps), list(df.t), initial=0)

    df['vx_mph'] = df.vx.mul(0.681818)
    df['vy_mph'] = df.vy.mul(0.681818)
    df['v_mph'] = df.v.mul(0.681818)

    df['dx'] = integrate.cumtrapz(list(df.vx), list(df.t), initial=0)
    df['dy'] = integrate.cumtrapz(list(df.vy), list(df.t), initial=0)
    df['disp'] = integrate.cumtrapz(list(df.v), list(df.t), initial=0)

    # heading angle?
    df['heading_rad'] = [np.arctan2(dx, dy) for dx, dy in zip(df.dx, df.dy)]
    df['heading_deg'] = [x * 180 / np.pi for x in df.heading_rad]

    return df


"""
vehicle motion - single vehicle
"""

def plot_model(df):
    """
    takes SingleMotion class variable as input
    """

    fig = make_subplots(rows=2, cols=1,
                        shared_xaxes=True,
                        vertical_spacing=0.05)
    # velocity data
    fig.add_trace(go.Scatter(x=df.t, y=df.vx_mph,
                             mode='lines',
                             name='X',
                             line=dict(color='rgb(0, 255, 0)', width=2)),
                  row=1, col=1)
    fig.add_trace(go.Scatter(x=df.t, y=df.vy_mph,
                             mode='lines',
                             name='Y',
                             line=dict(color='rgb(0, 0, 255)', width=2)),
                  row=1, col=1)
    fig.add_trace(go.Scatter(x=df.t, y=df.v_mph,
                             mode='lines',
                             name='Resultant',
                             line=dict(color='rgb(0, 0, 0)', width=2)),
                  row=1, col=1)
    # acceleration data
    fig.add_trace(go.Scatter(x=df.t, y=df.accel_x,
                             showlegend=False,
                             mode='lines',
                             name='Ax',
                             line=dict(color='rgb(0, 255, 0)', width=2)),
                  row=2, col=1)
    fig.add_trace(go.Scatter(x=df.t, y=df.accel_y,
                             showlegend=False,
                             mode='lines',
                             name='Ay',
                             line=dict(color='rgb(0, 0, 255)', width=2)),
                  row=2, col=1)
    fig.add_trace(go.Scatter(x=df.t, y=df.accel,
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
        title=f'Velocity | Acceleration',
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

    fig = go.Figure()
    # dx
    fig.add_trace(go.Scatter(x=df.t, y=df.dx,
                             mode='lines',
                             name='X',
                             line=dict(color='rgb(0, 255, 0)', width=2)))
    fig.add_trace(go.Scatter(x=df.t, y=df.dy,
                             mode='lines',
                             name='Y',
                             line=dict(color='rgb(0, 0, 255)', width=2)))
    fig.add_trace(go.Scatter(x=df.t, y=df.disp,
                             mode='lines',
                             name='Resultant',
                             line=dict(color='rgb(0, 0, 0)', width=2)))

    fig.update_layout(
        legend=dict(orientation="h", yanchor='top', y=1.1, xanchor='left', x=0.01),
        autosize=False,
        width=figure_size[0],
        height=figure_size[1],
        title=f'Displacement',
        template='plotly_white',
        xaxis=dict(showgrid=False, title='Time (s)'),
        yaxis=dict(showgrid=False),
        font=dict(family='Arial', size=font_size, color='black'))

    fig.update_xaxes(showgrid=False, title_text='Time (s)')
    fig.update_yaxes(showgrid=False, title_text='Displacement (ft)')

    fig.update_xaxes(showline=True, linewidth=1, linecolor='black', ticks="outside",
                     tickwidth=1, tickcolor='black', ticklen=10, zeroline=False)
    fig.update_yaxes(showline=True, linewidth=1, linecolor='black', ticks="outside",
                     tickwidth=1, tickcolor='black', ticklen=10, zeroline=False)
    fig.show()


    fig = go.Figure()
    # heading
    fig.add_trace(go.Scatter(x=df.t, y=df.heading_deg,
                             mode='lines',
                             name='heading',
                             line=dict(color='rgb(0, 0, 0)', width=2)))

    fig.update_layout(
        legend=dict(orientation="h", yanchor='top', y=1.1, xanchor='left', x=0.01),
        autosize=False,
        width=figure_size[0],
        height=figure_size[1],
        title=f'Heading',
        template='plotly_white',
        xaxis=dict(showgrid=False, title='Time (s)'),
        yaxis=dict(showgrid=False),
        font=dict(family='Arial', size=font_size, color='black'))

    fig.update_xaxes(showgrid=False, title_text='Time (s)')
    fig.update_yaxes(showgrid=False, title_text='Heading (deg)')

    fig.update_xaxes(showline=True, linewidth=1, linecolor='black', ticks="outside",
                     tickwidth=1, tickcolor='black', ticklen=10, zeroline=False)
    fig.update_yaxes(showline=True, linewidth=1, linecolor='black', ticks="outside",
                     tickwidth=1, tickcolor='black', ticklen=10, zeroline=False)
    fig.show()



driver = time_inputs(time, throttle, brake, steer)

plot_model(driver)
