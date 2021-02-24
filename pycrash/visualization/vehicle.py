"""
plots used within vehicle class
"""
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import plotly.io as pio

pio.renderers.default = "browser"  # <- determines how plots are displayed using Plotly

# TODO: create input for figure size - loads from "defaults" folder?
figure_size = (1200, 700)
font_size = 24
tick_font_size = 22

"""
generating impact point - striking vehicle
"""


def plot_impact_points(veh, iplane=True):
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
    veh._b_lrc_y = -1 * veh.width / 2

    bdy_x = (veh._b_lfc_x, veh._b_rfc_x, veh._b_rrc_x, veh._b_lrc_x, veh._b_lfc_x)
    bdy_y = (veh._b_lfc_y, veh._b_rfc_y, veh._b_rrc_y, veh._b_lrc_y, veh._b_lfc_y)

    x_axis_length = veh._b_lfc_x * 1.5 - veh._b_lrc_x * 1.5

    # generate plot to show vehicle outline and default points for impact
    fig = go.Figure()

    # body outline
    fig.add_trace(go.Scatter(x=bdy_x, y=bdy_y,
                             mode='lines+markers',
                             line=dict(color='rgb(67,67,67)', width=2),
                             marker=dict(color='rgb(255, 0, 0)', size=8)))
    # cg
    fig.add_trace(go.Scatter(x=[0, 0], y=[0, 0],
                             mode='markers',
                             marker=dict(color='rgb(51, 204, 51)', size=20)))

    fig.add_annotation(x=1,
                       y=-1,
                       showarrow=False,
                       text="CG")
    # vehicle x-axis
    fig.add_annotation(x=5,
                       y=0,
                       axref='x',
                       ayref='y',
                       text="",
                       showarrow=True,
                       ax=0,
                       ay=0,
                       arrowsize=2,
                       arrowhead=1,
                       arrowwidth=1.5,
                       arrowcolor='rgb(0, 0, 0)')
    # vehicle y-axis
    fig.add_annotation(x=0,
                       y=5,
                       axref='x',
                       ayref='y',
                       text="",
                       showarrow=True,
                       ax=0,
                       ay=0,
                       arrowsize=2,
                       arrowhead=1,
                       arrowwidth=1.5,
                       arrowcolor='rgb(0, 0, 255)')


    fig.add_annotation(x=veh._b_lfc_x * 1.1,
                       y=veh._b_lfc_y,
                       showarrow=False,
                       text="1")
    fig.add_annotation(x=veh._b_rfc_x * 1.1,
                       y=veh._b_rfc_y,
                       showarrow=False,
                       text="2")
    fig.add_annotation(x=veh._b_rrc_x * 1.1,
                       y=veh._b_rrc_y,
                       showarrow=False,
                       text="3")
    fig.add_annotation(x=veh._b_lrc_x * 1.1,
                       y=veh._b_lrc_y,
                       showarrow=False,
                       text="4")

    if iplane:
        for i in range(len(veh.impact_points)):
            # normal impact plane
            fig.add_annotation(x=veh.impact_norm[i][0],
                               y=veh.impact_norm[i][1],
                               axref='x',
                               ayref='y',
                               text="",
                               showarrow=True,
                               ax=veh.impact_points[i][0],
                               ay=veh.impact_points[i][1],
                               arrowsize=2,
                               arrowhead=2,
                               arrowwidth=1.5,
                               arrowcolor='rgb(153, 0, 51)')
            # tangential impact plane
            fig.add_annotation(x=veh.impact_tang[i][0],
                               y=veh.impact_tang[i][1],
                               axref='x',
                               ayref='y',
                               text="",
                               showarrow=True,
                               ax=veh.impact_points[i][0],
                               ay=veh.impact_points[i][1],
                               arrowsize=1,
                               arrowhead=1,
                               arrowwidth=1,
                               arrowcolor='rgb(153, 0, 51)')

            fig.add_trace(go.Scatter(x=[veh.impact_points[i][0], veh.impact_points[i][0]],
                                     y=[veh.impact_points[i][1], veh.impact_points[i][1]],
                                     mode='markers',
                                     name=f'POI: {i}',
                                     marker=dict(color='rgb(153, 0, 51)', size=7),
                                     ))

    fig.update_layout(
        showlegend=False,
        autosize=False,
        width=figure_size[0],
        height=figure_size[1],
        title='Selecting Impact Point for Striking Vehicle',
        template='plotly_white',
        xaxis=dict(showgrid=False, title='x-axis - Forward (ft)'),
        yaxis=dict(showgrid=False, title='y-axis - Rightward (ft)'),
        font=dict(family='Arial', size=16, color='black'))

    fig.update_xaxes(showline=True, linewidth=1, linecolor='black', ticks="outside",
                     tickwidth=1, tickcolor='black', ticklen=10, zeroline=False,
                     range=[veh._b_lrc_x * 1.5, veh._b_lfc_x * 1.5])
    fig.update_yaxes(autorange='reversed', showline=True, linewidth=1, linecolor='black', ticks="outside",
                     tickwidth=1, tickcolor='black', ticklen=10, zeroline=False,
                     range=[-0.5 * x_axis_length * figure_size[1] / figure_size[0],
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
    veh._b_lrc_y = -1 * veh.width / 2

    bdy_x = (veh._b_lfc_x, veh._b_rfc_x, veh._b_rrc_x, veh._b_lrc_x, veh._b_lfc_x)
    bdy_y = (veh._b_lfc_y, veh._b_rfc_y, veh._b_rrc_y, veh._b_lrc_y, veh._b_lfc_y)

    x_axis_length = veh._b_lfc_x * 1.5 - veh._b_lrc_x * 1.5

    # generate plot to show vehicle outline and default points for impact
    fig = go.Figure()

    # body outline
    fig.add_trace(go.Scatter(x=bdy_x[:2], y=bdy_y[:2],
                             mode='lines+text',
                             line=dict(color='rgb(0, 0, 0)', width=2)))
    fig.add_trace(go.Scatter(x=bdy_x[1:3], y=bdy_y[1:3],
                             mode='lines+text',
                             line=dict(color='rgb(51, 102, 204)', width=2)))
    fig.add_trace(go.Scatter(x=bdy_x[2:4], y=bdy_y[2:4],
                             mode='lines+text',
                             line=dict(color='rgb(0, 153, 51)', width=2)))
    fig.add_trace(go.Scatter(x=bdy_x[3:5], y=bdy_y[3:5],
                             mode='lines+text',
                             line=dict(color='rgb(255, 102, 0)', width=2)))

    # cg
    fig.add_trace(go.Scatter(x=[0, 0], y=[0, 0],
                             mode='markers',
                             marker=dict(color='rgb(51, 204, 51)', size=20)))

    # edge labels
    x_coordinates = [veh._b_lfc_x * 1.1, -2, veh._b_rrc_x * 1.1, -2]
    y_coordinates = [0, 1.2 * veh.width / 2, 0, -1.2 * veh.width / 2]
    for i in range(0, 4):
        if i in veh.edgeimpact:
            text = f'Edge {i} - POI {veh.edgeimpact.index(i)}'
        else:
            text = f'Edge {i}'
            
        fig.add_annotation(x=x_coordinates[i],
                           y=y_coordinates[i],
                           showarrow=False,
                           text=text)


    fig.add_annotation(x=1,
                       y=-1,
                       showarrow=False,
                       text="CG")
    fig.add_annotation(x=5,
                       y=0,
                       axref='x',
                       ayref='y',
                       text="",
                       showarrow=True,
                       ax=0,
                       ay=0,
                       arrowsize=2,
                       arrowhead=1,
                       arrowwidth=1.5,
                       arrowcolor='rgb(0, 0, 0)')

    fig.add_annotation(x=0,
                       y=5,
                       axref='x',
                       ayref='y',
                       text="",
                       showarrow=True,
                       ax=0,
                       ay=0,
                       arrowsize=2,
                       arrowhead=1,
                       arrowwidth=1.5,
                       arrowcolor='rgb(0, 0, 255)')

    fig.update_layout(
        showlegend=False,
        autosize=False,
        width=figure_size[0],
        height=figure_size[1],
        title='Selecting Impact Edge for Struck Vehicle',
        template='plotly_white',
        xaxis=dict(showgrid=False, title='x-axis - Forward (ft)'),
        yaxis=dict(showgrid=False, title='y-axis - Rightward (ft)'),
        font=dict(family='Arial', size=16, color='black'))

    fig.update_xaxes(showline=True, linewidth=1, linecolor='black', ticks="outside",
                     tickwidth=1, tickcolor='black', ticklen=10, zeroline=False,
                     range=[veh._b_lrc_x * 1.5, veh._b_lfc_x * 1.5])
    fig.update_yaxes(autorange='reversed', showline=True, linewidth=1, linecolor='black', ticks="outside",
                     tickwidth=1, tickcolor='black', ticklen=10, zeroline=False,
                     range=[-0.5 * x_axis_length * figure_size[1] / figure_size[0],
                            0.5 * x_axis_length * figure_size[1] / figure_size[0]])
    fig.show()


"""
plot driver inputs
"""


def plot_driver_inputs(self):
    fig = make_subplots(specs=[[{"secondary_y": True}]])

    fig.add_trace(go.Scatter(x=self.driver_input.t, y=self.driver_input.throttle * 100,
                             mode='lines',
                             name='throttle',
                             line=dict(color='rgb(0, 255, 0)', width=2)),
                  secondary_y=False)
    fig.add_trace(go.Scatter(x=self.driver_input.t, y=self.driver_input.brake * 100,
                             mode='lines',
                             name='brake',
                             line=dict(color='rgb(255, 0, 0)', width=2)),
                  secondary_y=False)
    fig.add_trace(go.Scatter(x=self.driver_input.t, y=self.driver_input.steer,
                             mode='lines',
                             name='steer',
                             line=dict(color='rgb(0, 0, 0)', width=2)),
                  secondary_y=True)

    fig.update_layout(
        legend=dict(orientation="h", yanchor='top', y=1.05, xanchor='left', x=0.45),
        autosize=False,
        width=figure_size[0],
        height=figure_size[1],
        title=f'Driver Inputs for {self.name}',
        template='plotly_white',
        xaxis=dict(showgrid=False, title='Time (s)'),
        yaxis=dict(showgrid=False),
        font=dict(family='Arial', size=font_size, color='black'))

    fig.update_yaxes(showgrid=False, title_text='Steer Angle (deg)', secondary_y=True)
    fig.update_yaxes(showgrid=False, title_text='Brake | Throttle (%)', secondary_y=False)

    fig.update_xaxes(showline=True, linewidth=1, linecolor='black', ticks="outside",
                     tickwidth=1, tickcolor='black', ticklen=10, zeroline=False, tickfont=dict(size=tick_font_size))
    fig.update_yaxes(showline=True, linewidth=1, linecolor='black', ticks="outside",
                     tickwidth=1, tickcolor='black', ticklen=10, zeroline=False, tickfont=dict(size=tick_font_size))
    fig.show()
