import plotly.graph_objects as go
import math

width = 1000
aspect_ratio = 16 / 9
figure_size = (width, width / aspect_ratio)
wheel_colors = ['rgb(0, 0, 255)', 'rgb(0, 255, 0)', 'rgb(153, 0, 204)', 'rgb(255, 102, 0)']
# plot initial positions and any motion data to show vehicle paths
def initial_position(veh1, veh2, i):
    # plot initial positions
    # grid grid based on initial position of vehicle
    # scale x,y axes accordingly
    # static geometry from model_calcs.position_data

    """
    combine two vehicles into a single df, to allow for max / min check
    """
    fig = go.Figure()
    for veh in [veh1, veh2]:
        # Body and tire outlines
        bdy_x = (veh.Px.b_lfc[i], veh.Px.b_rfc[i], veh.Px.b_rrc[i], veh.Px.b_lrc[i], veh.Px.b_lfc[i])
        bdy_y = (veh.Py.b_lfc[i], veh.Py.b_rfc[i], veh.Py.b_rrc[i], veh.Py.b_lrc[i], veh.Py.b_lfc[i])

        lfw_x = (veh.Px.lfw_a[i], veh.Px.lfw_b[i], veh.Px.lfw_c[i], veh.Px.lfw_d[i], veh.Px.lfw_a[i])
        lfw_y = (veh.Py.lfw_a[i], veh.Py.lfw_b[i], veh.Py.lfw_c[i], veh.Py.lfw_d[i], veh.Py.lfw_a[i])

        rfw_x = (veh.Px.rfw_a[i], veh.Px.rfw_b[i], veh.Px.rfw_c[i], veh.Px.rfw_d[i], veh.Px.rfw_a[i])
        rfw_y = (veh.Py.rfw_a[i], veh.Py.rfw_b[i], veh.Py.rfw_c[i], veh.Py.rfw_d[i], veh.Py.rfw_a[i])

        rrw_x = (veh.Px.rrw_a[i], veh.Px.rrw_b[i], veh.Px.rrw_c[i], veh.Px.rrw_d[i], veh.Px.rrw_a[i])
        rrw_y = (veh.Py.rrw_a[i], veh.Py.rrw_b[i], veh.Py.rrw_c[i], veh.Py.rrw_d[i], veh.Py.rrw_a[i])

        lrw_x = (veh.Px.lrw_a[i], veh.Px.lrw_b[i], veh.Px.lrw_c[i], veh.Px.lrw_d[i], veh.Px.lrw_a[i])
        lrw_y = (veh.Py.lrw_a[i], veh.Py.lrw_b[i], veh.Py.lrw_c[i], veh.Py.lrw_d[i], veh.Py.lrw_a[i])


        # body outline
        fig.add_trace(go.Scatter(x = bdy_x, y = bdy_y,
                                    mode = 'lines',
                                    name = f'{veh.name} - body',
                                    line = dict(color = 'rgb(0, 0, 0)', width = 2)))

        # wheel outline
        fig.add_trace(go.Scatter(x = lfw_x, y = lfw_y,
                            mode = 'lines',
                            name = 'LF',
                            line = dict(color = wheel_colors[0], width = 1)))
        fig.add_trace(go.Scatter(x = rfw_x, y = rfw_y,
                            mode = 'lines',
                            name = 'RF',
                            line = dict(color = wheel_colors[1], width = 1)))
        fig.add_trace(go.Scatter(x = rrw_x, y = rrw_y,
                            mode = 'lines',
                            name = 'RR',
                            line = dict(color = wheel_colors[2], width = 1)))
        fig.add_trace(go.Scatter(x = lrw_x, y = lrw_y,
                            mode = 'lines',
                            name = 'LR',
                            line = dict(color = wheel_colors[3], width = 1)))

        # CG
        cgx = [veh.Px.cg[i], veh.Px.cg[i]]
        cgy = [veh.Py.cg[i], veh.Py.cg[i]]

        # adjust axes to keep aspect aspect ratio
        """
        dx_max = veh.p_gx.cg.max() + 15
        dx_min = veh.p_gx.cg.min() - 15
        dy_max = veh.p_gy.cg.max() + 15
        dy_min = veh.p_gy.cg.min() - 15

        dx = dx_max - dx_min
        dy = dy_max - dy_min

        if dx > dy:
            adj_x = aspect_ratio * dy / dx
            adj_y = 1
            print(f" dx > dy -> adj_x = {adj_x}, adj_y = {adj_y}")
            dx_min = round(dx_min * adj_x)
            dx_max = round(dx_max * adj_x)
            print(f"dx_min = {dx_min}, dx_max = {dx_max}")
            print(f"dy_min = {dy_min}, dy_max = {dy_max}")
        else:
            adj_x = 1
            adj_y = (1 / aspect_ratio) * dx / dy
            print(f" dy > dx -> adj_x = {adj_x}, adj_y = {adj_y}")
            dy_min = round(dy_min * adj_y)
            dy_max = round(dy_max * adj_y)
            print(f"dx_min = {dx_min}, dx_max = {dx_max}")
            print(f"dy_min = {dy_min}, dy_max = {dy_max}")
        """

        fig.add_trace(go.Scatter(x = cgx, y = cgy,
                            mode = 'markers',
                            name = f'CG - {veh.name}',
                            marker = dict(color = 'rgb(0, 0, 0)', size = 10),
                            ))


        # velocity vector
        fig.add_annotation(x = veh.Px.vel_v[i],
                           y = veh.Py.vel_v[i],
                           ax = veh.Px.cg[i],
                           ay = veh.Py.cg[i],
                           axref = 'x',
                           ayref = 'y',
                           xref = 'x',
                           yref = 'y',
                           text = "",
                           showarrow = True,
                           arrowsize = 2.5,
                           arrowhead = 1,
                           arrowwidth = 1.7,
                           arrowcolor = 'rgb(255, 0, 0)')

        # x axis
        fig.add_annotation(x = veh.Px.xaxis[i],
                           y = veh.Py.xaxis[i],
                           ax = veh.Px.cg[i],
                           ay = veh.Py.cg[i],
                           axref = 'x',
                           ayref = 'y',
                           xref = 'x',
                           yref = 'y',
                           text = "",
                           showarrow = True,
                           arrowsize = 2,
                           arrowhead = 1,
                           arrowwidth = 1.5,
                           arrowcolor = 'rgb(0, 0, 0)')

        # y axis
        fig.add_annotation(x = veh.Px.yaxis[i],
                           y = veh.Py.yaxis[i],
                           ax = veh.Px.cg[i],
                           ay = veh.Py.cg[i],
                           axref = 'x',
                           ayref = 'y',
                           xref = 'x',
                           yref = 'y',
                           text = "",
                           showarrow = True,
                           arrowsize = 2,
                           arrowhead = 1,
                           arrowwidth = 1.5,
                           arrowcolor = 'rgb(0, 0, 255)')

    fig.update_layout(
        showlegend = False,
        autosize = False,
        width = width,
        height = width / aspect_ratio,
        title = 'Initial Vehicle Positions',
        template = 'plotly_white',
        xaxis = dict(showgrid = True, title = 'Forward (ft)'),
        yaxis = dict(showgrid = True, title = 'Rightward (ft)'),
        font = dict(family = 'Arial', size = 16, color = 'black'))

    fig.update_xaxes(showline=True, linewidth=1, linecolor='black', ticks="outside",
                     tickwidth=1, tickcolor='black', ticklen=10, zeroline=False)
    fig.update_yaxes(autorange="reversed", showline=True, linewidth=1, linecolor='black', ticks="outside",
                     tickwidth=1, tickcolor='black', ticklen=10, zeroline=False)

    fig.show()

    # Table of initial conditions

    fig = go.Figure(data=[go.Table(
    header=dict(values=['Vehicle', 'Vx (mph)', 'Vy (mph)', 'V (mph)', 'Omega (deg/s)', 'X Position (ft)', 'Y Position (ft)'],
                line_color='darkslategray',
                fill_color='lightskyblue',
                align='left'),
    cells=dict(values=[[f'{veh1.name}', f'{veh2.name}'],
                       [veh1.vx_initial, veh2.vx_initial],
                       [veh1.vy_initial, veh2.vy_initial],
                       [math.sqrt(veh1.vx_initial**2 + veh1.vy_initial**2), math.sqrt(veh2.vx_initial**2 + veh2.vy_initial**2)],
                       [veh1.omega_z, veh2.omega_z],
                       [veh1.init_x_pos, veh2.init_x_pos],
                       [veh1.init_y_pos, veh2.init_y_pos]],
               line_color='darkslategray',
               fill_color='lightcyan',
               align='left'))
               ])

    fig.update_layout(width=500, height=300)
    fig.show()
