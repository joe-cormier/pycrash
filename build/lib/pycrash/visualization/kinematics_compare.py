"""
functions for plotting data related to vehicle kinematics for multiple vehicles
"""
import math
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import plotly.io as pio
pio.renderers.default = "browser"


# TODO: create input for figure size - loads from "defaults" folder?
aspect_ratio = 16 / 9
font_size = 22
tick_font_size = 18
line_width = 2.5
figure_size_wide = (1600, 1200)
figure_size_tall = (1200, 1200)
y_titlefontSize = 18  # <- font size for y axis plots with 4 rows

def compare_kinematics(model1, model2, name1, name2):
    fig = make_subplots(rows=2, cols=1,
                        shared_xaxes=True,
                        vertical_spacing=0.07)

    # CG translations
    fig.add_trace(go.Scatter(x=model1.t, y=model1.Dx,
                             mode='lines',
                             name=f'{name1} - X',
                             line=dict(color='rgb(0, 255, 0)', width=line_width)),
                  row=1, col=1)
    fig.add_trace(go.Scatter(x=model2.t, y=model2.Dx,
                             mode='lines',
                             name=f'{name2} - X',
                             line=dict(color='rgb(0, 255, 0)', width=line_width, dash='dash')),
                  row=1, col=1)

    fig.add_trace(go.Scatter(x=model1.t, y=model1.Dy,
                             mode='lines',
                             name=f'{name1} - Y',
                             line=dict(color='rgb(0, 0, 255)', width=line_width)),
                  row=1, col=1)
    fig.add_trace(go.Scatter(x=model2.t, y=model2.Dy,
                             mode='lines',
                             name=f'{name2} - Y',
                             line=dict(color='rgb(0, 0, 255)', width=line_width, dash='dash')),
                  row=1, col=1)
    # Heading angle
    fig.add_trace(go.Scatter(x=model1.t, y=model1.theta_deg,
                             mode='lines',
                             name=f'{name1} - heading',
                             line=dict(color='rgb(0, 0, 0)', width=line_width)),
                  row=2, col=1)
    fig.add_trace(go.Scatter(x=model2.t, y=model2.theta_deg,
                             mode='lines',
                             name=f'{name2} - heading',
                             line=dict(color='rgb(0, 0, 0)', width=line_width, dash='dash')),
                  row=2, col=1)

    fig.update_layout(
        legend=dict(orientation="v", yanchor='top', y=.95, xanchor='left', x=1.05),
        autosize=False,
        width=figure_size_wide[0],
        height=figure_size_wide[1],
        template='plotly_white',
        yaxis=dict(showgrid=False),
        font=dict(family='Arial', size=font_size, color='black'))

    fig.update_xaxes(showgrid=False, title_text='Time (s)', tickfont=dict(size=tick_font_size), row=2, col=1)
    fig.update_xaxes(showgrid=False, title_text='', tickfont=dict(size=tick_font_size), row=1, col=1)
    fig.update_yaxes(showgrid=False, title_text='Displacement (ft)', tickfont=dict(size=tick_font_size), row=1, col=1)
    fig.update_yaxes(showgrid=False, title_text='Heading Angle (deg)', tickfont=dict(size=tick_font_size), row=2, col=1)
    fig.update_xaxes(showline=True, linewidth=1, linecolor='black', ticks="outside",
                     tickwidth=1, tickcolor='black', ticklen=10, zeroline=False)
    fig.update_yaxes(showline=True, linewidth=1, linecolor='black', ticks="outside",
                     tickwidth=1, tickcolor='black', ticklen=10, zeroline=False)
    fig.show()

    """
    velocity
    slip angle
    """
    fig = make_subplots(rows=2, cols=1,
                        shared_xaxes=True,
                        vertical_spacing=0.07)

    # CG Velocity
    fig.add_trace(go.Scatter(x=model1.t, y=model1.Vx / 1.46667,
                             mode='lines',
                             name=f'{name1} - X',
                             line=dict(color='rgb(0, 255, 0)', width=line_width)),
                  row=1, col=1)
    fig.add_trace(go.Scatter(x=model2.t, y=model2.Vx / 1.46667,
                             mode='lines',
                             name=f'{name2} - X',
                             line=dict(color='rgb(0, 255, 0)', width=line_width, dash='dash')),
                  row=1, col=1)

    fig.add_trace(go.Scatter(x=model1.t, y=model1.Vy / 1.46667,
                             mode='lines',
                             name=f'{name1} - Y',
                             line=dict(color='rgb(0, 0, 255)', width=line_width)),
                  row=1, col=1)
    fig.add_trace(go.Scatter(x=model2.t, y=model2.Vy / 1.46667,
                             mode='lines',
                             name=f'{name2} - Y',
                             line=dict(color='rgb(0, 0, 255)', width=line_width, dash='dash')),
                  row=1, col=1)
    # Slip angle - compare to beta_deg
    fig.add_trace(go.Scatter(x=model1.t, y=model1.phi_deg,
                             mode='lines',
                             name=f'{name1} - slip angle',
                             line=dict(color='rgb(0, 0, 0)', width=line_width)),
                  row=2, col=1)
    fig.add_trace(go.Scatter(x=model2.t, y=model2.phi_deg,
                             mode='lines',
                             name=f'{name2} - slip angle',
                             line=dict(color='rgb(0, 0, 0)', width=line_width, dash='dash')),
                  row=2, col=1)

    fig.update_layout(
        legend=dict(orientation="h", yanchor='top', y=1.1, xanchor='left', x=0.01),
        autosize=False,
        width=figure_size_tall[0],
        height=figure_size_tall[1],
        template='plotly_white',
        yaxis=dict(showgrid=False),
        font=dict(family='Arial', size=font_size, color='black'))

    fig.update_xaxes(showgrid=False, title_text='Time (s)', row=2, col=1)
    fig.update_xaxes(showgrid=False, title_text='', row=1, col=1)
    fig.update_yaxes(showgrid=False, title_text='Velocity (mph)', row=1, col=1)
    fig.update_yaxes(showgrid=False, title_text='Slip Angle (deg)', row=2, col=1)
    fig.update_xaxes(showline=True, linewidth=1, linecolor='black', ticks="outside",
                     tickwidth=1, tickcolor='black', ticklen=10, zeroline=False)
    fig.update_yaxes(showline=True, linewidth=1, linecolor='black', ticks="outside",
                     tickwidth=1, tickcolor='black', ticklen=10, zeroline=False)
    fig.show()


    fig = make_subplots(rows=4, cols=1,
                        shared_xaxes=True,
                        vertical_spacing=0.05)

    """
    rightward tire forces
    """
    fig.add_trace(go.Scatter(x=model1.t, y=model1.lf_fy,
                             mode='lines',
                             name=f'LF - {name1}',
                             line=dict(color='rgb(0, 0, 255)', width=line_width)),
                  row=1, col=1)
    fig.add_trace(go.Scatter(x=model2.t, y=model2.lf_fy,
                             mode='lines',
                             name=f'LF - {name2}',
                             line=dict(color='rgb(0, 0, 255)', width=line_width, dash='dash')),
                  row=1, col=1)
    fig.add_trace(go.Scatter(x=model1.t, y=model1.rf_fy,
                             mode='lines',
                             name=f'RF - {name1}',
                             line=dict(color='rgb(0, 255, 0)', width=line_width)),
                  row=2, col=1)
    fig.add_trace(go.Scatter(x=model2.t, y=model2.rf_fy,
                             mode='lines',
                             name=f'RF - {name2}',
                             line=dict(color='rgb(0, 255, 0)', width=line_width, dash='dash')),
                  row=2, col=1)
    fig.add_trace(go.Scatter(x=model1.t, y=model1.rr_fy,
                             mode='lines',
                             name=f'RR - {name1}',
                             line=dict(color='rgb(153, 0, 204)', width=line_width)),
                  row=3, col=1)
    fig.add_trace(go.Scatter(x=model2.t, y=model2.rr_fy,
                             mode='lines',
                             name=f'RR - {name2}',
                             line=dict(color='rgb(153, 0, 204)', width=line_width, dash='dash')),
                  row=3, col=1)
    fig.add_trace(go.Scatter(x=model1.t, y=model1.lr_fy,
                             mode='lines',
                             name=f'LR - {name1}',
                             line=dict(color='rgb(255, 102, 0)', width=line_width)),
                  row=4, col=1)
    fig.add_trace(go.Scatter(x=model2.t, y=model2.lr_fy,
                             mode='lines',
                             name=f'LR - {name2}',
                             line=dict(color='rgb(255, 102, 0)', width=line_width, dash='dash')),
                  row=4, col=1)

    fig.update_layout(
        legend=dict(orientation="v", yanchor='top', y=1.1, xanchor='left', x=1.01),
        autosize=False,
        width=figure_size_tall[0],
        height=figure_size_tall[1],
        title='Tire Rightward Forces',
        template='plotly_white',
        xaxis=dict(showgrid=False),
        yaxis=dict(showgrid=False),
        font=dict(family='Arial', size=font_size, color='black'))

    fig.update_xaxes(showgrid=False, title_text='Time (s)', row=4, col=1,
                     showline=True, linewidth=1, linecolor='black', ticks="outside",
                     tickwidth=1, tickcolor='black', ticklen=10, zeroline=False)
    fig.update_xaxes(showgrid=False, title_text='', row=1, col=1,
                     showline=True, linewidth=1, linecolor='black', ticks="outside",
                     tickwidth=1, tickcolor='black', ticklen=10, zeroline=False)
    fig.update_xaxes(showgrid=False, title_text='', row=2, col=1,
                     showline=True, linewidth=1, linecolor='black', ticks="outside",
                     tickwidth=1, tickcolor='black', ticklen=10, zeroline=False)
    fig.update_xaxes(showgrid=False, title_text='', row=3, col=1,
                     showline=True, linewidth=1, linecolor='black', ticks="outside",
                     tickwidth=1, tickcolor='black', ticklen=10, zeroline=False)
    fig.update_yaxes(showgrid=False, title_text='LF - Rightward Force (lb)', row=1, col=1,
                     showline=True, linewidth=1, linecolor='black', ticks="outside",
                     tickwidth=1, tickcolor='black', ticklen=10, zeroline=False, titlefont=dict(size=y_titlefontSize))
    fig.update_yaxes(showgrid=False, title_text='RF - Rightward Force (lb)', row=2, col=1,
                     showline=True, linewidth=1, linecolor='black', ticks="outside",
                     tickwidth=1, tickcolor='black', ticklen=10, zeroline=False, titlefont=dict(size=y_titlefontSize))
    fig.update_yaxes(showgrid=False, title_text='RR - Rightward Force (lb)', row=3, col=1,
                     showline=True, linewidth=1, linecolor='black', ticks="outside",
                     tickwidth=1, tickcolor='black', ticklen=10, zeroline=False, titlefont=dict(size=y_titlefontSize))
    fig.update_yaxes(showgrid=False, title_text='LR - Rightward Force (lb)', row=4, col=1,
                     showline=True, linewidth=1, linecolor='black', ticks="outside",
                     tickwidth=1, tickcolor='black', ticklen=10, zeroline=False, titlefont=dict(size=y_titlefontSize))
    fig.show()

    """
    forward tire forces
    """
    fig = make_subplots(rows=4, cols=1,
                        shared_xaxes=True,
                        vertical_spacing=0.05)

    fig.add_trace(go.Scatter(x=model1.t, y=model1.lf_fx,
                             mode='lines',
                             name=f'LF - {name1}',
                             line=dict(color='rgb(0, 0, 255)', width=line_width)),
                  row=1, col=1)
    fig.add_trace(go.Scatter(x=model1.t, y=model1.rf_fx,
                             mode='lines',
                             name=f'RF - {name1}',
                             line=dict(color='rgb(0, 255, 0)', width=line_width)),
                  row=2, col=1)
    fig.add_trace(go.Scatter(x=model1.t, y=model1.rr_fx,
                             mode='lines',
                             name=f'RR - {name1}',
                             line=dict(color='rgb(153, 0, 204)', width=line_width)),
                  row=3, col=1)

    fig.add_trace(go.Scatter(x=model1.t, y=model1.lr_fx,
                             mode='lines',
                             name=f'LR - {name1}',
                             line=dict(color='rgb(255, 102, 0)', width=line_width)),
                  row=4, col=1)
    fig.update_layout(
        legend=dict(orientation="v", yanchor='top', y=1.1, xanchor='left', x=1.01),
        autosize=False,
        width=figure_size_tall[0],
        height=figure_size_tall[1],
        title='Tire Forward Forces',
        template='plotly_white',
        xaxis=dict(showgrid=False),
        yaxis=dict(showgrid=False),
        font=dict(family='Arial', size=font_size, color='black'))

    fig.update_xaxes(showgrid=False, title_text='Time (s)', row=4, col=1,
                     showline=True, linewidth=1, linecolor='black', ticks="outside",
                     tickwidth=1, tickcolor='black', ticklen=10, zeroline=False)
    fig.update_xaxes(showgrid=False, title_text='', row=1, col=1,
                     showline=True, linewidth=1, linecolor='black', ticks="outside",
                     tickwidth=1, tickcolor='black', ticklen=10, zeroline=False)
    fig.update_xaxes(showgrid=False, title_text='', row=2, col=1,
                     showline=True, linewidth=1, linecolor='black', ticks="outside",
                     tickwidth=1, tickcolor='black', ticklen=10, zeroline=False)
    fig.update_xaxes(showgrid=False, title_text='', row=3, col=1,
                     showline=True, linewidth=1, linecolor='black', ticks="outside",
                     tickwidth=1, tickcolor='black', ticklen=10, zeroline=False)
    fig.update_yaxes(showgrid=False, title_text='LF - Rightward Force (lb)', row=1, col=1,
                     showline=True, linewidth=1, linecolor='black', ticks="outside",
                     tickwidth=1, tickcolor='black', ticklen=10, zeroline=False, titlefont=dict(size=y_titlefontSize))
    fig.update_yaxes(showgrid=False, title_text='RF - Rightward Force (lb)', row=2, col=1,
                     showline=True, linewidth=1, linecolor='black', ticks="outside",
                     tickwidth=1, tickcolor='black', ticklen=10, zeroline=False, titlefont=dict(size=y_titlefontSize))
    fig.update_yaxes(showgrid=False, title_text='RR - Rightward Force (lb)', row=3, col=1,
                     showline=True, linewidth=1, linecolor='black', ticks="outside",
                     tickwidth=1, tickcolor='black', ticklen=10, zeroline=False, titlefont=dict(size=y_titlefontSize))
    fig.update_yaxes(showgrid=False, title_text='LR - Rightward Force (lb)', row=4, col=1,
                     showline=True, linewidth=1, linecolor='black', ticks="outside",
                     tickwidth=1, tickcolor='black', ticklen=10, zeroline=False, titlefont=dict(size=y_titlefontSize))
    fig.show()


    fig = make_subplots(rows=4, cols=1,
                        shared_xaxes=True,
                        vertical_spacing=0.05)

    """
    slip angles
    """
    fig.add_trace(go.Scatter(x=model1.t, y=model1.lf_alpha * 180 / math.pi,
                             mode='lines',
                             name=f'LF - {name1}',
                             line=dict(color='rgb(0, 0, 255)', width=2)),
                  row=1, col=1)
    fig.add_trace(go.Scatter(x=model2.t, y=model2.lf_alpha * -1,
                             mode='lines',
                             name=f'LF - {name2}',
                             line=dict(color='rgb(0, 0, 255)', width=line_width, dash='dash')),
                  row=1, col=1)
    fig.add_trace(go.Scatter(x=model1.t, y=model1.rf_alpha * 180 / math.pi,
                             mode='lines',
                             name=f'RF - {name1}',
                             line=dict(color='rgb(0, 255, 0)', width=line_width)),
                  row=2, col=1)
    fig.add_trace(go.Scatter(x=model2.t, y=model2.rf_alpha * -1,
                             mode='lines',
                             name=f'RF - {name2}',
                             line=dict(color='rgb(0, 255, 0)', width=line_width, dash='dash')),
                  row=2, col=1)
    fig.add_trace(go.Scatter(x=model1.t, y=model1.rr_alpha * 180 / math.pi,
                             mode='lines',
                             name=f'RR - {name1}',
                             line=dict(color='rgb(153, 0, 204)', width=2)),
                  row=3, col=1)
    fig.add_trace(go.Scatter(x=model2.t, y=model2.rr_alpha * -1,
                             mode='lines',
                             name=f'RR - {name2}',
                             line=dict(color='rgb(153, 0, 204)', width=line_width, dash='dash')),
                  row=3, col=1)
    fig.add_trace(go.Scatter(x=model1.t, y=model1.lr_alpha * 180 / math.pi,
                             mode='lines',
                             name=f'LR - {name1}',
                             line=dict(color='rgb(255, 102, 0)', width=2)),
                  row=4, col=1)
    fig.add_trace(go.Scatter(x=model2.t, y=model2.lr_alpha * -1,
                             mode='lines',
                             name=f'LR - {name2}',
                             line=dict(color='rgb(255, 102, 0)', width=line_width, dash='dash')),
                  row=4, col=1)

    fig.update_layout(
        legend=dict(orientation="v", yanchor='top', y=1.1, xanchor='left', x=1.01),
        autosize=False,
        width=figure_size_tall[0],
        height=figure_size_tall[1],
        title='Tire Slip Angles',
        template='plotly_white',
        xaxis=dict(showgrid=False),
        yaxis=dict(showgrid=False),
        font=dict(family='Arial', size=font_size, color='black'))

    fig.update_xaxes(showgrid=False, title_text='Time (s)', row=4, col=1,
                     showline=True, linewidth=1, linecolor='black', ticks="outside",
                     tickwidth=1, tickcolor='black', ticklen=10, zeroline=False)
    fig.update_xaxes(showgrid=False, title_text='', row=1, col=1,
                     showline=True, linewidth=1, linecolor='black', ticks="outside",
                     tickwidth=1, tickcolor='black', ticklen=10, zeroline=False)
    fig.update_xaxes(showgrid=False, title_text='', row=2, col=1,
                     showline=True, linewidth=1, linecolor='black', ticks="outside",
                     tickwidth=1, tickcolor='black', ticklen=10, zeroline=False)
    fig.update_xaxes(showgrid=False, title_text='', row=3, col=1,
                     showline=True, linewidth=1, linecolor='black', ticks="outside",
                     tickwidth=1, tickcolor='black', ticklen=10, zeroline=False)
    fig.update_yaxes(showgrid=False, title_text='LF - Slip Angle (deg)', row=1, col=1,
                     showline=True, linewidth=1, linecolor='black', ticks="outside",
                     tickwidth=1, tickcolor='black', ticklen=10, zeroline=False, titlefont=dict(size=y_titlefontSize))
    fig.update_yaxes(showgrid=False, title_text='RF - Slip Angle (deg)', row=2, col=1,
                     showline=True, linewidth=1, linecolor='black', ticks="outside",
                     tickwidth=1, tickcolor='black', ticklen=10, zeroline=False, titlefont=dict(size=y_titlefontSize))
    fig.update_yaxes(showgrid=False, title_text='RR - Slip Angle (deg)', row=3, col=1,
                     showline=True, linewidth=1, linecolor='black', ticks="outside",
                     tickwidth=1, tickcolor='black', ticklen=10, zeroline=False, titlefont=dict(size=y_titlefontSize))
    fig.update_yaxes(showgrid=False, title_text='LR - Slip Angle (deg)', row=4, col=1,
                     showline=True, linewidth=1, linecolor='black', ticks="outside",
                     tickwidth=1, tickcolor='black', ticklen=10, zeroline=False, titlefont=dict(size=y_titlefontSize))
    fig.show()

    """
    # acceleration
    """

    fig = make_subplots(rows=2, cols=1,
                        shared_xaxes=True,
                        vertical_spacing=0.07)

    # acceleration
    fig.add_trace(go.Scatter(x=model1.t, y=model1.au / 32.2,
                             mode='lines',
                             name=f'{name1} - ax',
                             line=dict(color='rgb(0, 255, 0)', width=line_width)),
                  row=1, col=1)
    fig.add_trace(go.Scatter(x=model2.t, y=model2.ax / 32.2,
                             mode='lines',
                             name=f'{name2} - ax',
                             line=dict(color='rgb(0, 255, 0)', width=line_width, dash='dash')),
                  row=1, col=1)

    fig.add_trace(go.Scatter(x=model1.t, y=model1.av / 32.2,
                             mode='lines',
                             name=f'{name1} - ay',
                             line=dict(color='rgb(0, 0, 255)', width=line_width)),
                  row=2, col=1)
    fig.add_trace(go.Scatter(x=model2.t, y=model2.ay / 32.2,
                             mode='lines',
                             name=f'{name2} - ay',
                             line=dict(color='rgb(0, 0, 255)', width=line_width, dash='dash')),
                  row=2, col=1)

    fig.update_layout(
        legend=dict(orientation="h", yanchor='top', y=1.05, xanchor='left', x=0.1),
        autosize=False,
        width=figure_size_tall[0],
        height=figure_size_tall[1],
        title='Acceleration',
        template='plotly_white',
        xaxis=dict(showgrid=False),
        yaxis=dict(showgrid=False),
        font=dict(family='Arial', size=font_size, color='black'))

    fig.update_xaxes(showgrid = False, title_text = '', row = 1, col = 1,
                     showline=True, linewidth=1, linecolor='black', ticks="outside",
                     tickwidth=1, tickcolor='black', ticklen=10, zeroline=False)
    fig.update_xaxes(showgrid = False, title_text = 'Time (s)', row = 2, col = 1,
                     showline=True, linewidth=1, linecolor='black', ticks="outside",
                     tickwidth=1, tickcolor='black', ticklen=10, zeroline=False)
    fig.update_yaxes(showgrid=False, title_text='Forward Accel (g)', row=1, col=1,
                     showline=True, linewidth=1, linecolor='black', ticks="outside",
                     tickwidth=1, tickcolor='black', ticklen=10, zeroline=False)
    fig.update_yaxes(showgrid=False, title_text='Rightward Accel (g)', row=2, col=1,
                     showline=True, linewidth=1, linecolor='black', ticks="outside",
                     tickwidth=1, tickcolor='black', ticklen=10, zeroline=False)
    fig.show()


    """
    vertical tire forces
    """

    fig = make_subplots(rows=4, cols=1,
                        shared_xaxes=True,
                        vertical_spacing=0.05)

    fig.add_trace(go.Scatter(x=model1.t, y=model1.lf_fz,
                             mode='lines',
                             name=f'LF - {name1}',
                             line=dict(color='rgb(0, 0, 255)', width=2)), row=1, col=1)
    fig.add_trace(go.Scatter(x=model2.t, y=model2.lf_fz * 1000,
                             mode='lines',
                             name=f'LF - {name2}',
                             line=dict(color='rgb(0, 0, 255)', width=line_width, dash='dash')), row=1, col=1)
    fig.add_trace(go.Scatter(x=model1.t, y=model1.rf_fz,
                             mode='lines',
                             name=f'RF - {name1}',
                             line=dict(color='rgb(0, 255, 0)', width=line_width)), row=2, col=1)
    fig.add_trace(go.Scatter(x=model2.t, y=model2.rf_fz * 1000,
                             mode='lines',
                             name=f'RF - {name2}',
                             line=dict(color='rgb(0, 255, 0)', width=line_width, dash='dash')), row=2, col=1)
    fig.add_trace(go.Scatter(x=model1.t, y=model1.rr_fz,
                             mode='lines',
                             name=f'RR - {name1}',
                             line=dict(color='rgb(153, 0, 204)', width=line_width)), row=3, col=1)
    fig.add_trace(go.Scatter(x=model2.t, y=model2.rr_fz * 1000,
                             mode='lines',
                             name=f'RR - {name2}',
                             line=dict(color='rgb(153, 0, 204)', width=line_width, dash='dash')), row=3, col=1)
    fig.add_trace(go.Scatter(x=model1.t, y=model1.lr_fz,
                             mode='lines',
                             name=f'LR - {name1}',
                             line=dict(color='rgb(255, 102, 0)', width=line_width)), row=4, col=1)
    fig.add_trace(go.Scatter(x=model2.t, y=model2.lr_fz * 1000,
                             mode='lines',
                             name=f'LR - {name2}',
                             line=dict(color='rgb(255, 102, 0)', width=line_width, dash='dash')), row=4, col=1)

    fig.update_layout(
        legend=dict(orientation="v", yanchor='top', y=1.1, xanchor='left', x=1.01),
        autosize=False,
        width=figure_size_tall[0],
        height=figure_size_tall[1],
        title='Vertical Tire Forces',
        template='plotly_white',
        xaxis=dict(showgrid=False),
        yaxis=dict(showgrid=False, titlefont=dict(size=14)),
        font=dict(family='Arial', size=font_size, color='black'))

    fig.update_xaxes(showgrid=False, title_text='Time (s)', row=4, col=1,
                     showline=True, linewidth=1, linecolor='black', ticks="outside",
                     tickwidth=1, tickcolor='black', ticklen=10, zeroline=False)
    fig.update_xaxes(showgrid=False, title_text='', row=1, col=1,
                     showline=True, linewidth=1, linecolor='black', ticks="outside",
                     tickwidth=1, tickcolor='black', ticklen=10, zeroline=False)
    fig.update_xaxes(showgrid=False, title_text='', row=2, col=1,
                     showline=True, linewidth=1, linecolor='black', ticks="outside",
                     tickwidth=1, tickcolor='black', ticklen=10, zeroline=False)
    fig.update_xaxes(showgrid=False, title_text='', row=3, col=1,
                     showline=True, linewidth=1, linecolor='black', ticks="outside",
                     tickwidth=1, tickcolor='black', ticklen=10, zeroline=False)
    fig.update_yaxes(showgrid=False, title_text='LF - Force (lb)', row=1, col=1,
                     showline=True, linewidth=1, linecolor='black', ticks="outside",
                     tickwidth=1, tickcolor='black', ticklen=10, zeroline=False, titlefont=dict(size=y_titlefontSize))
    fig.update_yaxes(showgrid=False, title_text='RF - Force (lb)', row=2, col=1,
                     showline=True, linewidth=1, linecolor='black', ticks="outside",
                     tickwidth=1, tickcolor='black', ticklen=10, zeroline=False, titlefont=dict(size=y_titlefontSize))
    fig.update_yaxes(showgrid=False, title_text='RR - Force (lb)', row=3, col=1,
                     showline=True, linewidth=1, linecolor='black', ticks="outside",
                     tickwidth=1, tickcolor='black', ticklen=10, zeroline=False, titlefont=dict(size=y_titlefontSize))
    fig.update_yaxes(showgrid=False, title_text='LR - Force (lb)', row=4, col=1,
                     showline=True, linewidth=1, linecolor='black', ticks="outside",
                     tickwidth=1, tickcolor='black', ticklen=10, zeroline=False, titlefont=dict(size=y_titlefontSize))
    fig.show()
