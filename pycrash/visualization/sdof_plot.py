"""
functions for plotting data related to SDOF models
"""
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import plotly.io as pio
pio.renderers.default = "browser"  # <- determines how plots are displayed using Plotly


# plot velocity of each vehicle
# can be a single model run or a list of runs
# fill between will fill the space between the first and last runs

def plot_fdx(run_list, run_colors = False, fill_diff = False, show_legend = True):
    """
    run_list can be a single SDOF model run or a list of multiple runs
    colors must be in 'rgb(0, 0, 0)' format
    """

    # test if user supplied a list of runs to plot
    if isinstance(run_list, list):
        plot_list = run_list
    else:
        plot_list = [run_list]  # if not a list, make it a list of length 1

    if run_colors:
        color_list = run_colors
    else:
        color_list = ['rgb(0, 26, 51)'] * len(plot_list)

    # set line types
    line_type = ['solid'] * len(plot_list)
    line_type[0] = 'dash'
    line_type[-1] = 'dashdot'

    # create plot for each run in list
    fig = go.Figure()
    for i, run in enumerate(plot_list):
        fig.add_trace(go.Scatter(x = run.model.dx * -12, y = run.model.springF,
                                mode = 'lines',
                                name = f"{run.name} - Closing Speed: {run.veh1.vx_initial - run.veh2.vx_initial} mph",
                                line = dict(color = color_list[i], width = 2.5, dash = line_type[i])
                                ))

    # fill spaces between first and last trace for each Vehicle
    if fill_diff:
        fig.add_trace(go.Scatter(x = plot_list[0].model.dx * -12, y = plot_list[0].model.springF,
                                mode = 'lines',
                                line = dict(color = color_list[0], width = 2.5, dash = line_type[0]),
                                name = f"{run.name} - Closing Speed: {run.veh1.vx_initial - run.veh2.vx_initial} mph",
                                fill = None,
                                showlegend = False
                                ))
        fig.add_trace(go.Scatter(x = plot_list[-1].model.dx * -12, y = plot_list[-1].model.springF,
                                mode = 'lines',
                                line = dict(color = color_list[-1], width = 2.5, dash = line_type[-1]),
                                name = f"{run.name} - Closing Speed: {run.veh1.vx_initial - run.veh2.vx_initial} mph",
                                fill = 'tonexty',
                                showlegend = False
                                ))

    fig.update_layout(
        legend = dict(orientation = "v", yanchor = 'top', y = 1, xanchor = 'left', x = 0.01),
        autosize = False,
        width = 1600,
        height = 900,
        title = f'Single Degree of Freedom Model - Mutual Force - Displacement',
        template = 'plotly_white',
        xaxis = dict(showgrid = False, title = 'Mutual Crush (in)'),
        font = dict(family = 'Arial', size = 28, color = 'black'))

    fig.update_layout(showlegend = show_legend)
    fig.update_yaxes(showgrid = False, showline=True, linewidth=1, linecolor='black', ticks="outside",
                     tickwidth=1, tickcolor='black', ticklen=10, zeroline=False, title_text = 'Force (lb)',
                     rangemode = "tozero", tickfont=dict(family='Arial', size=24))
    fig.update_xaxes(showline=True, linewidth=1, linecolor='black', ticks="outside", rangemode = "tozero",
                     tickwidth=1, tickcolor='black', ticklen=10, zeroline=False, tickfont=dict(family='Arial', size=24))
    fig.show()

def plot_vehicle_fdx(run_list, veh1_colors = False, veh2_colors = False, fill_diff = False, show_legend = True):
    """
    run_list can be a single SDOF model run or a list of multiple runs
    veh1_colors and veh2_colors can be lists of colors of the same length of run_list
    colors must be in 'rgb(0, 0, 0)' format
    """

    # test if user supplied a list of runs to plot
    if isinstance(run_list, list):
        plot_list = run_list
    else:
        plot_list = [run_list]  # if not a list, make it a list of length 1

    if veh1_colors:
        veh1_color_list = veh1_colors
    else:
        veh1_color_list = ['rgb(51, 51, 153)'] * len(plot_list)

    if veh2_colors:
        veh2_color_list = veh2_colors
    else:
        veh2_color_list = ['rgb(0, 153, 51)'] * len(plot_list)

    # set line types
    line_type = ['solid'] * len(plot_list)
    line_type[0] = 'dash'
    line_type[-1] = 'dashdot'

    # create plot for each run in list
    fig = go.Figure()
    for i, run in enumerate(plot_list):
        if run.k1known:
            fig.add_trace(go.Scatter(x = run.model.veh1_dx * -12, y = run.model.springF,
                                    mode = 'lines',
                                    name = f"{run.name} - V1",
                                    line = dict(color = veh1_color_list[i], width = 2.5, dash = line_type[i])
                                    ))
            if fill_diff:
                fig.add_trace(go.Scatter(x = plot_list[0].model.veh1_dx * -12, y = plot_list[0].model.springF,
                                        mode = 'lines',
                                        line = dict(color = veh1_color_list[0], width = 2.5, dash = line_type[0]),
                                        name = f"{run.name} - V1",
                                        fill = None,
                                        showlegend = False
                                        ))
                fig.add_trace(go.Scatter(x = plot_list[-1].model.veh1_dx * -12, y = plot_list[-1].model.springF,
                                        mode = 'lines',
                                        line = dict(color = veh1_color_list[-1], width = 2.5, dash = line_type[-1]),
                                        name = f"{run.name} - V1",
                                        fill = 'tonexty',
                                        showlegend = False
                                        ))

        if run.k2known:
            fig.add_trace(go.Scatter(x = run.model.veh2_dx * -12, y = run.model.springF,
                                    mode = 'lines',
                                    name = f"{run.name} - V2",
                                    line = dict(color = veh2_color_list[i], width = 2.5, dash = line_type[i])
                                    ))
            if fill_diff:
                fig.add_trace(go.Scatter(x = plot_list[0].model.veh2_dx * -12, y = plot_list[0].model.springF,
                                        mode = 'lines',
                                        line = dict(color = veh2_color_list[0], width = 2.5, dash = line_type[0]),
                                        name = f"{run.name} - V2",
                                        fill = None,
                                        showlegend = False
                                        ))
                fig.add_trace(go.Scatter(x = plot_list[-1].model.veh2_dx * -12, y = plot_list[-1].model.springF,
                                        mode = 'lines',
                                        line = dict(color = veh2_color_list[-1], width = 2.5, dash = line_type[-1]),
                                        name = f"{run.name} - V2",
                                        fill = 'tonexty',
                                        showlegend = False
                                        ))

    fig.update_layout(
        legend = dict(orientation = "v", yanchor = 'top', y = 1, xanchor = 'left', x = 0.01),
        autosize = False,
        width = 1600,
        height = 900,
        title = f'Single Degree of Freedom Model - Vehicle Crush',
        template = 'plotly_white',
        xaxis = dict(showgrid = False, title = 'Crush (in)'),
        font = dict(family = 'Arial', size = 28, color = 'black'))

    fig.update_layout(showlegend = show_legend)
    fig.update_yaxes(showgrid = False, showline=True, linewidth=1, linecolor='black', ticks="outside",
                     tickwidth=1, tickcolor='black', ticklen=10, zeroline=False, title_text = 'Force (lb)',
                     rangemode = "tozero")
    fig.update_xaxes(showline=True, linewidth=1, linecolor='black', ticks="outside",
                     tickwidth=1, tickcolor='black', ticklen=10, zeroline=False,
                     rangemode = "tozero")
    fig.show()

def plot_velocity(run_list, veh1_colors = False, veh2_colors = False, fill_diff = False, show_legend = True):
    """
    run_list can be a single SDOF model run or a list of multiple runs
    veh1_colors and veh2_colors can be lists of colors of the same length of run_list
    colors must be in 'rgb(0, 0, 0)' format
    """

    # test if user supplied a list of runs to plot
    if isinstance(run_list, list):
        plot_list = run_list
    else:
        plot_list = [run_list]  # if not a list, make it a list of length 1

    if veh1_colors:
        veh1_color_list = veh1_colors
    else:
        veh1_color_list = ['rgb(51, 51, 153)'] * len(plot_list)

    if veh2_colors:
        veh2_color_list = veh2_colors
    else:
        veh2_color_list = ['rgb(0, 153, 51)'] * len(plot_list)

    # set line types
    line_type = ['solid'] * len(plot_list)
    line_type[0] = 'dash'
    line_type[-1] = 'dash'

    # create plot for each run in list
    fig = go.Figure()
    for i, run in enumerate(plot_list):
        fig.add_trace(go.Scatter(x = run.model.t, y = run.model.v1 * 0.681818,
                                mode = 'lines',
                                name = f"{run.name} - {run.veh1.name}",
                                line = dict(color = veh1_color_list[i], width = 2, dash = line_type[i])
                                ))
        fig.add_trace(go.Scatter(x = run.model.t, y = run.model.v2 * 0.681818,
                                mode = 'lines',
                                name = f"{run.name} - {run.veh2.name}",
                                line = dict(color = veh2_color_list[i], width = 2, dash = line_type[i])
                                ))

    # fill spaces between first and last trace for each Vehicle
    if fill_diff:
        fig.add_trace(go.Scatter(x = plot_list[0].model.t, y = plot_list[0].model.v1 * 0.681818,
                                mode = 'lines',
                                line = dict(color = veh1_color_list[0], width = 1, dash = line_type[0]),
                                name = f"{run.name} - {run.veh1.name}",
                                fill = None,
                                showlegend = False
                                ))
        fig.add_trace(go.Scatter(x = plot_list[-1].model.t, y = plot_list[-1].model.v1 * 0.681818,
                                mode = 'lines',
                                line = dict(color = veh1_color_list[-1], width = 1, dash = line_type[-1]),
                                name = f"{run.name} - {run.veh1.name}",
                                fill = 'tonexty',
                                showlegend = False
                                ))
        fig.add_trace(go.Scatter(x = plot_list[0].model.t, y = plot_list[0].model.v2 * 0.681818,
                                mode = 'lines',
                                line = dict(color = veh2_color_list[0], width = 1, dash = line_type[0]),
                                name = f"{run.name} - {run.veh2.name}",
                                fill = None,
                                showlegend = False
                                ))
        fig.add_trace(go.Scatter(x = plot_list[-1].model.t, y = plot_list[-1].model.v2 * 0.681818,
                                mode = 'lines',
                                line = dict(color = veh2_color_list[-1], width = 1, dash = line_type[-1]),
                                name = f"{run.name} - {run.veh2.name}",
                                fill = 'tonexty',
                                showlegend = False
                                ))

    fig.update_layout(
        legend = dict(orientation = "h", yanchor = 'top', y = 1.1, xanchor = 'left', x = 0.01),
        autosize = False,
        width = 1600,
        height = 900,
        title = f'Single Degree of Freedom Model - Vehicle Velocity',
        template = 'plotly_white',
        xaxis = dict(showgrid = False, title = 'Time (s)'),
        font = dict(family = 'Arial', size = 28, color = 'black'))

    fig.update_layout(showlegend = show_legend)
    fig.update_yaxes(showgrid = False, showline=True, linewidth=1, linecolor='black', ticks="outside",
                     tickwidth=1, tickcolor='black', ticklen=10, zeroline=False, title_text = 'Velocity (mph)', tickfont=dict(family='Arial', size=28))
    fig.update_xaxes(showline=True, linewidth=1, linecolor='black', ticks="outside",
                     tickwidth=1, tickcolor='black', ticklen=10, zeroline=False, tickfont=dict(family='Arial', size=28))
    fig.show()

def plot_acceleration(run_list, veh1_colors = False, veh2_colors = False, fill_diff = False, show_legend = True):
    """
    run_list can be a single SDOF model run or a list of multiple runs
    veh1_colors and veh2_colors can be lists of colors of the same length of run_list
    colors must be in 'rgb(0, 0, 0)' format
    """

    # test if user supplied a list of runs to plot
    if isinstance(run_list, list):
        plot_list = run_list
    else:
        plot_list = [run_list]  # if not a list, make it a list of length 1

    if veh1_colors:
        veh1_color_list = veh1_colors
    else:
        veh1_color_list = ['rgb(51, 51, 153)'] * len(plot_list)

    if veh2_colors:
        veh2_color_list = veh2_colors
    else:
        veh2_color_list = ['rgb(0, 153, 51)'] * len(plot_list)

    # set line types
    line_type = ['solid'] * len(plot_list)
    line_type[0] = 'dash'
    line_type[-1] = 'dash'

    # create plot for each run in list
    fig = go.Figure()
    for i, run in enumerate(plot_list):
        fig.add_trace(go.Scatter(x = run.model.t, y = run.model.a1 / 32.2,
                                mode = 'lines',
                                name = f"{run.name} - {run.veh1.name}",
                                line = dict(color = veh1_color_list[i], width = 2, dash = line_type[i])
                                ))
        fig.add_trace(go.Scatter(x = run.model.t, y = run.model.a2 / 32.2,
                                mode = 'lines',
                                name = f"{run.name} - {run.veh2.name}",
                                line = dict(color = veh2_color_list[i], width = 2, dash = line_type[i])
                                ))

    # fill spaces between first and last trace for each Vehicle
    if fill_diff:
        fig.add_trace(go.Scatter(x = plot_list[0].model.t, y = plot_list[0].model.a1 / 32.2,
                                mode = 'lines',
                                line = dict(color = veh1_color_list[0], width = 1, dash = line_type[0]),
                                name = f"{run.name} - {run.veh1.name}",
                                fill = None,
                                showlegend = False
                                ))
        fig.add_trace(go.Scatter(x = plot_list[-1].model.t, y = plot_list[-1].model.a1 / 32.2,
                                mode = 'lines',
                                line = dict(color = veh1_color_list[-1], width = 1, dash = line_type[-1]),
                                name = f"{run.name} - {run.veh1.name}",
                                fill = 'tonexty',
                                showlegend = False
                                ))
        fig.add_trace(go.Scatter(x = plot_list[0].model.t, y = plot_list[0].model.a2 / 32.2,
                                mode = 'lines',
                                line = dict(color = veh2_color_list[0], width = 1, dash = line_type[0]),
                                name = f"{run.name} - {run.veh2.name}",
                                fill = None,
                                showlegend = False
                                ))
        fig.add_trace(go.Scatter(x = plot_list[-1].model.t, y = plot_list[-1].model.a2 / 32.2,
                                mode = 'lines',
                                line = dict(color = veh2_color_list[-1], width = 1, dash = line_type[-1]),
                                name = f"{run.name} - {run.veh2.name}",
                                fill = 'tonexty',
                                showlegend = False
                                ))

    fig.update_layout(
        legend = dict(orientation = "h", yanchor = 'top', y = 1.1, xanchor = 'left', x = 0.01),
        autosize = False,
        width = 1600,
        height = 900,
        title = f'Single Degree of Freedom Model - Vehicle Acceleration',
        template = 'plotly_white',
        xaxis = dict(showgrid = False, title = 'Time (s)'),
        font = dict(family = 'Arial', size = 28, color = 'black'))

    fig.update_layout(showlegend = show_legend)
    fig.update_yaxes(showgrid = False, showline=True, linewidth=1, linecolor='black', ticks="outside",
                     tickwidth=1, tickcolor='black', ticklen=10, zeroline=False, title_text = 'Acceleration (g)')
    fig.update_xaxes(showline=True, linewidth=1, linecolor='black', ticks="outside",
                     tickwidth=1, tickcolor='black', ticklen=10, zeroline=False)
    fig.show()
