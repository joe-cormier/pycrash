"""
plotting functions for vehicle model data
"""
import plotly.graph_objects as go
from plotly.subplots import make_subplots


# TODO: create input for figure size - loads from "defaults" folder?
figure_size = (800,450)
figure_ratio = figure_size[0] / figure_size[1]
wheel_colors = ['rgb(0, 0, 255)', 'rgb(0, 255, 0)', 'rgb(153, 0, 204)', 'rgb(255, 102, 0)']


def plot_motion(veh, i, tire_path=True):

        # Body and tire outlines
        bdy_x = (veh.p_gx.b_lfc[i], veh.p_gx.b_rfc[i], veh.p_gx.b_rrc[i], veh.p_gx.b_lrc[i], veh.p_gx.b_lfc[i])
        bdy_y = (veh.p_gy.b_lfc[i], veh.p_gy.b_rfc[i], veh.p_gy.b_rrc[i], veh.p_gy.b_lrc[i], veh.p_gy.b_lfc[i])

        lfw_x = (veh.p_gx.lfw_a[i], veh.p_gx.lfw_b[i], veh.p_gx.lfw_c[i], veh.p_gx.lfw_d[i], veh.p_gx.lfw_a[i])
        lfw_y = (veh.p_gy.lfw_a[i], veh.p_gy.lfw_b[i], veh.p_gy.lfw_c[i], veh.p_gy.lfw_d[i], veh.p_gy.lfw_a[i])

        rfw_x = (veh.p_gx.rfw_a[i], veh.p_gx.rfw_b[i], veh.p_gx.rfw_c[i], veh.p_gx.rfw_d[i], veh.p_gx.rfw_a[i])
        rfw_y = (veh.p_gy.rfw_a[i], veh.p_gy.rfw_b[i], veh.p_gy.rfw_c[i], veh.p_gy.rfw_d[i], veh.p_gy.rfw_a[i])

        rrw_x = (veh.p_gx.rrw_a[i], veh.p_gx.rrw_b[i], veh.p_gx.rrw_c[i], veh.p_gx.rrw_d[i], veh.p_gx.rrw_a[i])
        rrw_y = (veh.p_gy.rrw_a[i], veh.p_gy.rrw_b[i], veh.p_gy.rrw_c[i], veh.p_gy.rrw_d[i], veh.p_gy.rrw_a[i])

        lrw_x = (veh.p_gx.lrw_a[i], veh.p_gx.lrw_b[i], veh.p_gx.lrw_c[i], veh.p_gx.lrw_d[i], veh.p_gx.lrw_a[i])
        lrw_y = (veh.p_gy.lrw_a[i], veh.p_gy.lrw_b[i], veh.p_gy.lrw_c[i], veh.p_gy.lrw_d[i], veh.p_gy.lrw_a[i])

        fig = go.Figure()

        # body outline
        fig.add_trace(go.Scatter(x = bdy_x, y = bdy_y,
                            mode = 'lines',
                            name = 'body',
                            line = dict(color = 'rgb(0, 0, 0)', width = 2)))
        # wheel outline
        fig.add_trace(go.Scatter(x = lfw_x, y = lfw_y,
                            mode = 'lines',
                            name = 'LF',
                            line = dict(color = 'rgb(0, 0, 255)', width = 1)))
        fig.add_trace(go.Scatter(x = rfw_x, y = rfw_y,
                            mode = 'lines',
                            name = 'RF',
                            line = dict(color = 'rgb(0, 255, 0)', width = 1)))
        fig.add_trace(go.Scatter(x = rrw_x, y = rrw_y,
                            mode = 'lines',
                            name = 'RR',
                            line = dict(color = 'rgb(153, 0, 204)', width = 1)))
        fig.add_trace(go.Scatter(x = lrw_x, y = lrw_y,
                            mode = 'lines',
                            name = 'LR',
                            line = dict(color = 'rgb(255, 102, 0)', width = 1)))
        # CG
        fig.add_trace(go.Scatter(x = [veh.p_gx.cg[i], veh.p_gx.cg[i]], y = [veh.p_gy.cg[i], veh.p_gy.cg[i]],
                            mode = 'markers',
                            name = 'CG',
                            marker = dict(color = 'rgb(0, 0, 0)', size = 20)))

        # velocity vector
        fig.add_annotation(x = veh.p_gx.vel_v[i],
                           y = veh.p_gy.vel_v[i],
                           ax = veh.p_gx.cg[i],
                           ay = veh.p_gy.cg[i],
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
        fig.add_annotation(x = veh.p_gx.xaxis[i],
                           y = veh.p_gy.cg[i],
                           ax = veh.p_gx.cg[i],
                           ay = veh.p_gy.cg[i],
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
        fig.add_annotation(x = veh.p_gx.cg[i],
                           y = veh.p_gy.yaxis[i],
                           ax = veh.p_gx.cg[i],
                           ay = veh.p_gy.cg[i],
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

        # tire center plot depends on lock condition
        def setmarker(x):
            if x == 0:
                return 'circle'
            elif x == 1:
                return 'square-x'

        # plotly requires at least two rows to plot, so if i == 0, it will be set to 1
        gx = veh.p_gx[0:i]
        gy = veh.p_gy[0:i]

        if (tire_path):
            fig.add_trace(go.Scatter(x = gx.lfw, y = gy.lfw,
                                mode = 'markers',
                                name = 'LF',
                                marker = dict(color = 'rgb(0, 0, 255)', size = 5,
                                symbol = list(map(setmarker, gx.lf_lock)))))

            """
            fig.add_trace(go.Scatter(x = veh.p_gx.rfw[i-1:i], y = veh.p_gy.rfw[i-1:i],
                                mode = 'markers',
                                name = 'RF',
                                marker = dict(color = 'rgb(0, 255, 0)', size = 5,
                                symbol = marker_options[veh.p_gx.rf_lock[i]])))

            fig.add_trace(go.Scatter(x = veh.p_gx.rrw[:i], y = veh.p_gy.rrw[:i],
                                mode = 'markers',
                                name = 'RR',
                                marker = dict(color = 'rgb(153, 0, 204)', size = 5,
                                symbol = marker_options[veh.p_gx.rr_lock[i]])))

        if veh.p_gx.lr_lock[i] == 0:
            fig.add_trace(go.Scatter(x = veh.p_gx.lrw[:i], y = veh.p_gy.lrw[:i],
                                mode = 'markers',
                                name = 'LR',
                                marker = dict(color = 'rgb(153, 0, 204)', size = 5,
                                symbol = 'circle')))
        elif veh.p_gx.lr_lock[i] == 1:
            fig.add_trace(go.Scatter(x = veh.p_gx.lrw[:i], y = veh.p_gy.lrw[:i],
                                mode = 'markers',
                                name = 'LR',
                                marker = dict(color = 'rgb(153, 0, 204)', size = 5,
                                symbol = 'square-x')))
                """

        fig.update_layout(
            showlegend = False,
            autosize = False,
            width = figure_size[0],
            height = figure_size[1],
            title = 'Vehicle Motion in Global Reference Frame',
            template = 'plotly_white',
            xaxis = dict(showgrid = False, title = 'x-axis - Forward (ft)'),
            yaxis = dict(scaleanchor = 'x', scaleratio = figure_ratio, showgrid = False, title = 'y-axis - Rightward (ft)'),
            font = dict(family = 'Arial', size = 16, color = 'black'))

        fig.update_xaxes(showline=True, linewidth=1, linecolor='black', ticks="outside",
                         tickwidth=1, tickcolor='black', ticklen=10, zeroline=False)
        fig.update_yaxes(autorange = 'reversed', showline=True, linewidth=1, linecolor='black', ticks="outside",
                         tickwidth=1, tickcolor='black', ticklen=10, zeroline=False)
        fig.show()
