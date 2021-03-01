import plotly.graph_objects as go
import plotly.io as pio
pio.renderers.default = "browser"  # <- determines how plots are displayed using Plotly

width = 1900
aspect_ratio = 16 / 9
figure_size = (width, width / aspect_ratio)
wheel_colors = ['rgb(0, 0, 255)', 'rgb(0, 255, 0)', 'rgb(153, 0, 204)', 'rgb(255, 102, 0)']


# plot initial positions and any motion data to show vehicle paths
def initial_position(vehicle_list):
    # plot initial positions
    # grid grid based on initial position of vehicle
    # scale x,y axes accordingly
    # static geometry from model_calcs.position_data

    """
    combine two vehicles into a single df, to allow for max / min check
    """
    fig = go.Figure()
    for veh in vehicle_list:
        # Body and tire outlines
        bdy_x = (veh.Px['b_lfc'], veh.Px['b_rfc'], veh.Px['b_rrc'], veh.Px['b_lrc'], veh.Px['b_lfc'])
        bdy_y = (veh.Py['b_lfc'], veh.Py['b_rfc'], veh.Py['b_rrc'], veh.Py['b_lrc'], veh.Py['b_lfc'])

        lfw_x = (veh.Px['lfw_a'], veh.Px['lfw_b'], veh.Px['lfw_c'], veh.Px['lfw_d'], veh.Px['lfw_a'])
        lfw_y = (veh.Py['lfw_a'], veh.Py['lfw_b'], veh.Py['lfw_c'], veh.Py['lfw_d'], veh.Py['lfw_a'])

        rfw_x = (veh.Px['rfw_a'], veh.Px['rfw_b'], veh.Px['rfw_c'], veh.Px['rfw_d'], veh.Px['rfw_a'])
        rfw_y = (veh.Py['rfw_a'], veh.Py['rfw_b'], veh.Py['rfw_c'], veh.Py['rfw_d'], veh.Py['rfw_a'])

        rrw_x = (veh.Px['rrw_a'], veh.Px['rrw_b'], veh.Px['rrw_c'], veh.Px['rrw_d'], veh.Px['rrw_a'])
        rrw_y = (veh.Py['rrw_a'], veh.Py['rrw_b'], veh.Py['rrw_c'], veh.Py['rrw_d'], veh.Py['rrw_a'])

        lrw_x = (veh.Px['lrw_a'], veh.Px['lrw_b'], veh.Px['lrw_c'], veh.Px['lrw_d'], veh.Px['lrw_a'])
        lrw_y = (veh.Py['lrw_a'], veh.Py['lrw_b'], veh.Py['lrw_c'], veh.Py['lrw_d'], veh.Py['lrw_a'])

        # body outline
        fig.add_trace(go.Scatter(x=bdy_x, y=bdy_y,
                                 mode='lines',
                                 name=f'{veh.name} - body',
                                 line=dict(color='rgb(0, 0, 0)', width=2)))

        # wheel outline
        fig.add_trace(go.Scatter(x=lfw_x, y=lfw_y,
                                 mode='lines',
                                 name='LF',
                                 line=dict(color=wheel_colors[0], width=1)))
        fig.add_trace(go.Scatter(x=rfw_x, y=rfw_y,
                                 mode='lines',
                                 name='RF',
                                 line=dict(color=wheel_colors[1], width=1)))
        fig.add_trace(go.Scatter(x=rrw_x, y=rrw_y,
                                 mode='lines',
                                 name='RR',
                                 line=dict(color=wheel_colors[2], width=1)))
        fig.add_trace(go.Scatter(x=lrw_x, y=lrw_y,
                                 mode='lines',
                                 name='LR',
                                 line=dict(color=wheel_colors[3], width=1)))

        # CG
        cgx = [veh.init_x_pos, veh.init_x_pos]
        cgy = [veh.init_y_pos, veh.init_y_pos]

        fig.add_trace(go.Scatter(x=cgx, y=cgy,
                                 mode='markers',
                                 name=f'CG - {veh.name}',
                                 marker=dict(color='rgb(0, 0, 0)', size=10),
                                 ))

        # velocity vector
        fig.add_annotation(x=veh.Px['vel_v'],
                           y=veh.Py['vel_v'],
                           ax=veh.Px['cg'],
                           ay=veh.Py['cg'],
                           axref='x',
                           ayref='y',
                           xref='x',
                           yref='y',
                           text="",
                           showarrow=True,
                           arrowsize=2.5,
                           arrowhead=1,
                           arrowwidth=1.7,
                           arrowcolor='rgb(255, 0, 0)')

        # x axis
        fig.add_annotation(x=veh.Px['xaxis'],
                           y=veh.Py['xaxis'],
                           ax=veh.Px['cg'],
                           ay=veh.Py['cg'],
                           axref='x',
                           ayref='y',
                           xref='x',
                           yref='y',
                           text="",
                           showarrow=True,
                           arrowsize=2,
                           arrowhead=1,
                           arrowwidth=1.5,
                           arrowcolor='rgb(0, 0, 0)')

        # y axis
        fig.add_annotation(x=veh.Px['yaxis'],
                           y=veh.Py['yaxis'],
                           ax=veh.Px['cg'],
                           ay=veh.Py['cg'],
                           axref='x',
                           ayref='y',
                           xref='x',
                           yref='y',
                           text="",
                           showarrow=True,
                           arrowsize=2,
                           arrowhead=1,
                           arrowwidth=1.5,
                           arrowcolor='rgb(0, 0, 255)')

        if (veh.striking):
            # plot each impact plane
            for i in range(len(veh.impact_points)):
                # normal impact plane
                fig.add_annotation(x=veh.impact_norm_global[i][0],
                                   y=veh.impact_norm_global[i][1],
                                   axref='x',
                                   ayref='y',
                                   text="",
                                   showarrow=True,
                                   ax=veh.impact_points_global[i][0],
                                   ay=veh.impact_points_global[i][1],
                                   arrowsize=2,
                                   arrowhead=2,
                                   arrowwidth=1.5,
                                   arrowcolor='rgb(153, 0, 51)')
                # tangential impact plane
                fig.add_annotation(x=veh.impact_tang_global[i][0],
                                   y=veh.impact_tang_global[i][1],
                                   axref='x',
                                   ayref='y',
                                   text="",
                                   showarrow=True,
                                   ax=veh.impact_points_global[i][0],
                                   ay=veh.impact_points_global[i][1],
                                   arrowsize=1,
                                   arrowhead=1,
                                   arrowwidth=1,
                                   arrowcolor='rgb(153, 0, 51)')

                fig.add_trace(go.Scatter(x=[veh.impact_points_global[i][0], veh.impact_points_global[i][0]],
                                         y=[veh.impact_points_global[i][1], veh.impact_points_global[i][1]],
                                         mode='markers',
                                         name=f'POI: {i}',
                                         marker=dict(color='rgb(153, 0, 51)', size=7),
                                         ))

    fig.update_layout(
        showlegend=False,
        autosize=False,
        width=width,
        height=width / aspect_ratio,
        title='Initial Vehicle Positions',
        template='plotly_white',
        xaxis=dict(showgrid=True, title='Forward (ft)'),
        yaxis=dict(showgrid=True, title='Rightward (ft)'),
        font=dict(family='Arial', size=22, color='black'))

    fig.update_xaxes(showline=True, linewidth=1, linecolor='black', ticks="outside", constrain="domain",
                     tickwidth=1, tickcolor='black', ticklen=10, zeroline=False)
    fig.update_yaxes(autorange="reversed", showline=True, linewidth=1, linecolor='black', ticks="outside", scaleanchor = "x", scaleratio = 1,
                     tickwidth=1, tickcolor='black', ticklen=10, zeroline=False)

    fig.show()

    # Table of initial conditions


"""
    fig = go.Figure(data=[go.Table(
    header=dict(values=['Vehicle', 'Vx (mph)', 'Vy (mph)', 'V (mph)', 'Omega (deg/s)', 'X Position (ft)', 'Y Position (ft)'],
                line_color='darkslategray',
                fill_color='lightskyblue',
                align='left'),
    cells=dict(values=[[f'{vehicle_list[0].name}', f'{vehicle_list[1].name}'],
                       [vehicle_list[0].vx_initial, vehicle_list[1].vx_initial],
                       [vehicle_list[0].vy_initial, vehicle_list[1].vy_initial],
                       [np.sqrt(vehicle_list[0].vx_initial**2 + vehicle_list[0].vy_initial**2), np.sqrt(vehicle_list[1].vx_initial**2 + vehicle_list[1].vy_initial**2)],
                       [vehicle_list[0].omega_z, vehicle_list[1].omega_z],
                       [vehicle_list[0].init_x_pos, vehicle_list[1].init_x_pos],
                       [vehicle_list[0].init_y_pos, vehicle_list[1].init_y_pos]],
               line_color='darkslategray',
               fill_color='lightcyan',
               align='left'))
               ])

    fig.update_layout(width=500, height=300)
    fig.show()
"""
