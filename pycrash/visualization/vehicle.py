"""
plots used witin vehicle class
"""
import plotly.graph_objects as go
from plotly.subplots import make_subplots

# TODO: create input for figure size - loads from "defaults" folder?
figure_size = (800,450)


"""
generating impact point - striking vehicle
"""

def plot_impact_points(veh, user_loc = False, iplane = True):
    # x,y coordinates of vehicle outline:
    # left front corner
    veh._b_lfc_x = veh.lcgf + veh.f_hang
    veh._b_lfc_y = -1 * veh.width / 2
    # right front corner
    veh._b_rfc_x = veh.lcgf + veh.f_hang
    veh._b_rfc_y = veh.width / 2
    # right rear corner
    veh._b_rrc_x = -1 * veh.lcgr - veh.r_hang
    veh._b_rrc_y = veh.width / 2
    # left rear corner
    veh._b_lrc_x = -1 * veh.lcgr - veh.r_hang
    veh._b_lrc_y = -1* veh.width / 2

    bdy_x = (veh._b_lfc_x, veh._b_rfc_x, veh._b_rrc_x, veh._b_lrc_x, veh._b_lfc_x)
    bdy_y = (veh._b_lfc_y, veh._b_rfc_y, veh._b_rrc_y, veh._b_lrc_y, veh._b_lfc_y)

    x_axis_length = veh._b_lfc_x * 1.5 - veh._b_lrc_x * 1.5

    # generate plot to show vehicle outline and default points for impact
    fig = go.Figure()

    # body outline
    fig.add_trace(go.Scatter(x = bdy_x, y = bdy_y,
                            mode = 'lines+markers',
                            line = dict(color = 'rgb(67,67,67)', width = 2),
                            marker = dict(color = 'rgb(255, 0, 0)', size = 8)))
    # cg
    fig.add_trace(go.Scatter(x = [0,0], y = [0,0],
                            mode='markers',
                            marker = dict(color = 'rgb(51, 204, 51)', size = 20)))

    fig.add_annotation(x = 1,
                       y = -1,
                       showarrow = False,
                       text = "CG")
    # vehicle x-axis
    fig.add_annotation(x = 5,
                       y = 0,
                       axref = 'x',
                       ayref = 'y',
                       text = "",
                       showarrow = True,
                       ax = 0,
                       ay = 0,
                       arrowsize = 2,
                       arrowhead = 1,
                       arrowwidth = 1.5,
                       arrowcolor = 'rgb(0, 0, 0)')
    # vehicle y-axis
    fig.add_annotation(x = 0,
                       y = 5,
                       axref = 'x',
                       ayref = 'y',
                       text = "",
                       showarrow = True,
                       ax = 0,
                       ay = 0,
                       arrowsize = 2,
                       arrowhead = 1,
                       arrowwidth = 1.5,
                       arrowcolor = 'rgb(0, 0, 255)')

    if (user_loc):
        fig.add_trace(go.Scatter(x = [veh.pimpact_x, veh.pimpact_x,], y = [veh.pimpact_y, veh.pimpact_y,],
                            mode = 'markers+text',
                            marker = dict(color = 'rgb(255, 0, 0)', size = 8),
                            text = ['Impact Point', ""],
                            textposition = 'bottom center'))

    else:
        fig.add_annotation(x = veh._b_lfc_x * 1.1,
                           y = veh._b_lfc_y,
                           showarrow = False,
                           text = "1")
        fig.add_annotation(x = veh._b_rfc_x * 1.1,
                           y = veh._b_rfc_y,
                           showarrow = False,
                           text = "2")
        fig.add_annotation(x = veh._b_rrc_x * 1.1,
                           y = veh._b_rrc_y,
                           showarrow = False,
                           text = "3")
        fig.add_annotation(x = veh._b_lrc_x * 1.1,
                           y = veh._b_lrc_y,
                           showarrow = False,
                           text = "4")

    if (iplane):
        # normal impact plane
        fig.add_annotation(x = veh.impact_norm_x,
                           y = veh.impact_norm_y,
                           axref = 'x',
                           ayref = 'y',
                           text = "",
                           showarrow = True,
                           ax = veh.pimpact_x,
                           ay = veh.pimpact_y,
                           arrowsize = 2,
                           arrowhead = 2,
                           arrowwidth = 1.5,
                           arrowcolor = 'rgb(153, 0, 51)')
        # tangential impact plane
        fig.add_annotation(x = veh.impact_tang_x,
                           y = veh.impact_tang_y,
                           axref = 'x',
                           ayref = 'y',
                           text = "",
                           showarrow = True,
                           ax = veh.pimpact_x,
                           ay = veh.pimpact_y,
                           arrowsize = 1,
                           arrowhead = 1,
                           arrowwidth = 1,
                           arrowcolor = 'rgb(153, 0, 51)')

    fig.update_layout(
        showlegend=False,
        autosize=False,
        width=figure_size[0],
        height=figure_size[1],
        title = 'Selecting Impact Point for Striking Vehicle',
        template = 'plotly_white',
        xaxis = dict(showgrid = False, title = 'x-axis - Forward (ft)'),
        yaxis = dict(showgrid = False, title = 'y-axis - Rightward (ft)'),
        font = dict(family = 'Arial', size = 16, color = 'black'))

    fig.update_xaxes(showline=True, linewidth=1, linecolor='black', ticks="outside",
                     tickwidth=1, tickcolor='black', ticklen=10, zeroline=False, range = [veh._b_lrc_x * 1.5, veh._b_lfc_x * 1.5])
    fig.update_yaxes(autorange = 'reversed', showline=True, linewidth=1, linecolor='black', ticks="outside",
                     tickwidth=1, tickcolor='black', ticklen=10, zeroline=False,
                     range = [-0.5 * x_axis_length * figure_size[1] / figure_size[0],
                             0.5 * x_axis_length * figure_size[1] / figure_size[0]])
    fig.show()


    """
    generating impacting edge - struck vehicle
    """

def plot_impact_edge(veh):
    # x,y coordinates of vehicle outline:
    # left front corner
    veh._b_lfc_x = veh.lcgf + veh.f_hang
    veh._b_lfc_y = -1 * veh.width / 2
    # right front corner
    veh._b_rfc_x = veh.lcgf + veh.f_hang
    veh._b_rfc_y = veh.width / 2
    # right rear corner
    veh._b_rrc_x = -1 * veh.lcgr - veh.r_hang
    veh._b_rrc_y = veh.width / 2
    # left rear corner
    veh._b_lrc_x = -1 * veh.lcgr - veh.r_hang
    veh._b_lrc_y = -1* veh.width / 2

    bdy_x = (veh._b_lfc_x, veh._b_rfc_x, veh._b_rrc_x, veh._b_lrc_x, veh._b_lfc_x)
    bdy_y = (veh._b_lfc_y, veh._b_rfc_y, veh._b_rrc_y, veh._b_lrc_y, veh._b_lfc_y)

    x_axis_length = veh._b_lfc_x * 1.5 - veh._b_lrc_x * 1.5

    # generate plot to show vehicle outline and default points for impact
    fig = go.Figure()

    # body outline
    fig.add_trace(go.Scatter(x = bdy_x[:2], y = bdy_y[:2],
                            mode = 'lines+text',
                            line = dict(color = 'rgb(0, 0, 0)', width = 2)))
    fig.add_trace(go.Scatter(x = bdy_x[1:3], y = bdy_y[1:3],
                            mode = 'lines+text',
                            line = dict(color = 'rgb(51, 102, 204)', width = 2)))
    fig.add_trace(go.Scatter(x = bdy_x[2:4], y = bdy_y[2:4],
                            mode = 'lines+text',
                            line = dict(color = 'rgb(0, 153, 51)', width = 2)))
    fig.add_trace(go.Scatter(x = bdy_x[3:5], y = bdy_y[3:5],
                            mode = 'lines+text',
                            line = dict(color = 'rgb(255, 102, 0)', width = 2)))

    # cg
    fig.add_trace(go.Scatter(x = [0,0], y = [0,0],
                            mode='markers',
                            marker = dict(color = 'rgb(51, 204, 51)', size = 20)))

    # edge labels
    fig.add_annotation(x = veh._b_lfc_x * 1.1,
                       y = 0,
                       showarrow = False,
                       text = "1")
    fig.add_annotation(x = -2,
                       y = 1.2 * veh.width / 2,
                       showarrow = False,
                       text = "2")
    fig.add_annotation(x = veh._b_rrc_x * 1.1,
                       y = 0,
                       showarrow = False,
                       text = "3")
    fig.add_annotation(x = -2,
                       y = -1.2 * veh.width / 2,
                       showarrow = False,
                       text = "4")


    fig.add_annotation(x = 1,
                       y = -1,
                       showarrow = False,
                       text = "CG")
    fig.add_annotation(x = 5,
                       y = 0,
                       axref = 'x',
                       ayref = 'y',
                       text = "",
                       showarrow = True,
                       ax = 0,
                       ay = 0,
                       arrowsize = 2,
                       arrowhead = 1,
                       arrowwidth = 1.5,
                       arrowcolor = 'rgb(0, 0, 0)')

    fig.add_annotation(x = 0,
                       y = 5,
                       axref = 'x',
                       ayref = 'y',
                       text = "",
                       showarrow = True,
                       ax = 0,
                       ay = 0,
                       arrowsize = 2,
                       arrowhead = 1,
                       arrowwidth = 1.5,
                       arrowcolor = 'rgb(0, 0, 255)')



    fig.update_layout(
        showlegend=False,
        autosize=False,
        width=figure_size[0],
        height=figure_size[1],
        title = 'Selecting Impact Edge for Struck Vehicle',
        template = 'plotly_white',
        xaxis = dict(showgrid = False, title = 'x-axis - Forward (ft)'),
        yaxis = dict(showgrid = False, title = 'y-axis - Rightward (ft)'),
        font = dict(family = 'Arial', size = 16, color = 'black'))

    fig.update_xaxes(showline=True, linewidth=1, linecolor='black', ticks="outside",
                     tickwidth=1, tickcolor='black', ticklen=10, zeroline=False, range = [veh._b_lrc_x * 1.5, veh._b_lfc_x * 1.5])
    fig.update_yaxes(autorange = 'reversed', showline=True, linewidth=1, linecolor='black', ticks="outside",
                     tickwidth=1, tickcolor='black', ticklen=10, zeroline=False,
                     range = [-0.5 * x_axis_length * figure_size[1] / figure_size[0],
                             0.5 * x_axis_length * figure_size[1] / figure_size[0]])
    fig.show()


"""
plot driver inputs
"""
def plot_driver_inputs(self):
    fig = make_subplots(specs=[[{"secondary_y": True}]])

    fig.add_trace(go.Scatter(x = self.driver_input.t, y = self.driver_input.throttle * 100,
                            mode = 'lines',
                            name = 'throttle',
                            line = dict(color = 'rgb(0, 255, 0)', width = 2)),
                            secondary_y = False)
    fig.add_trace(go.Scatter(x = self.driver_input.t, y = self.driver_input.brake * 100,
                            mode = 'lines',
                            name = 'brake',
                            line = dict(color = 'rgb(255, 0, 0)', width = 2)),
                            secondary_y = False)
    fig.add_trace(go.Scatter(x = self.driver_input.t, y = self.driver_input.steer,
                            mode = 'lines',
                            name = 'steer',
                            line = dict(color = 'rgb(0, 0, 0)', width = 2)),
                            secondary_y = True)

    fig.update_layout(
        legend = dict(orientation = "h", yanchor = 'top', y = 1.15, xanchor = 'left', x = 0.01),
        autosize=False,
        width=figure_size[0],
        height=figure_size[1],
        title = f'Driver Inputs for {self.name}',
        template = 'plotly_white',
        xaxis = dict(showgrid = False, title = 'Time (s)'),
        yaxis = dict(showgrid = False),
        font = dict(family = 'Arial', size = 16, color = 'black'))

    fig.update_yaxes(showgrid = False, title_text = 'Steer Angle (deg)', secondary_y = True)
    fig.update_yaxes(showgrid = False, title_text = 'Brake | Throttle (%)', secondary_y = False)

    fig.update_xaxes(showline=True, linewidth=1, linecolor='black', ticks="outside",
                     tickwidth=1, tickcolor='black', ticklen=10, zeroline=False)
    fig.update_yaxes(autorange = 'reversed', showline=True, linewidth=1, linecolor='black', ticks="outside",
                     tickwidth=1, tickcolor='black', ticklen=10, zeroline=False)
    fig.show()
