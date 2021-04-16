"""
plotting functions for vehicle model data
"""
import plotly.graph_objects as go
import numpy as np
from plotly.subplots import make_subplots
import plotly.io as pio
pio.renderers.default = "browser"

# TODO: create input for figure size - loads from "defaults" environmental variable?
width = 900
aspect_ratio = 16 / 9
figure_size = (width, width / aspect_ratio)
wheel_colors = ['rgb(0, 0, 255)', 'rgb(0, 255, 0)', 'rgb(153, 0, 204)', 'rgb(255, 102, 0)']
font_size = 24
tick_font_size = 22

def get_impactNum(i, impactIndex):
    if i < max(impactIndex):
        for key, value in impactIndex.items():
            if i <= key:
                return(value)
    else:
        return max(impactIndex.values())

def plot_impact(veh_list, i, impactIndex, tire_path=True, show_vector=False):
    fig = go.Figure()
    plotImpactPoint = get_impactNum(i, impactIndex)
    for veh in veh_list:
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
        cgx = [veh.p_gx.cg[i], veh.p_gx.cg[i]]
        cgy = [veh.p_gy.cg[i], veh.p_gy.cg[i]]
        time = [veh.model.t[i], veh.model.t[i]]

        fig.add_trace(go.Scatter(x = cgx, y = cgy,
                            mode = 'markers',
                            name = 'CG',
                            marker = dict(color = 'rgb(0, 0, 0)', size = 10),
                            customdata = time,
                            hovertemplate = '<b>x</b>:%{x:.1f}<br>' + '<b>Y</b>: %{y:.1f}<br>' + '<b>time</b>: %{customdata:.3f}'))

        # velocity vector
        if show_vector:
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
                           y = veh.p_gy.xaxis[i],
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
        fig.add_annotation(x = veh.p_gx.yaxis[i],
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
        #print(gx)

        if (tire_path):
            fig.add_trace(go.Scatter(x = gx.lfw, y = gy.lfw,
                                mode = 'markers',
                                name = 'LF',
                                marker = dict(color = 'rgb(0, 0, 255)', size = 2,
                                symbol = list(map(setmarker, gx.lf_lock)))))

            fig.add_trace(go.Scatter(x = gx.rfw, y = gy.rfw,
                                mode = 'markers',
                                name = 'RF',
                                marker = dict(color = 'rgb(0, 255, 0)', size = 2,
                                symbol = list(map(setmarker, gx.rf_lock)))))

            fig.add_trace(go.Scatter(x = gx.rrw, y = gy.rrw,
                                mode = 'markers',
                                name = 'RR',
                                marker = dict(color = 'rgb(153, 0, 204)', size = 2,
                                symbol = list(map(setmarker, gx.rr_lock)))))

            fig.add_trace(go.Scatter(x = gx.lrw, y = gy.lrw,
                                mode = 'markers',
                                name = 'LR',
                                marker = dict(color = 'rgb(255, 102, 0)', size = 2,
                                symbol = list(map(setmarker, gx.lr_lock)))))

        if veh.striking:
            # plot each impact plane
            fig.add_annotation(x=veh.p_gx[f'impact_{plotImpactPoint}_norm'][i],
                               y=veh.p_gy[f'impact_{plotImpactPoint}_norm'][i],
                               axref='x',
                               ayref='y',
                               text="",
                               showarrow=True,
                               ax=veh.p_gx[f'POI_{plotImpactPoint}'][i],
                               ay=veh.p_gy[f'POI_{plotImpactPoint}'][i],
                               arrowsize=2,
                               arrowhead=2,
                               arrowwidth=1.5,
                               arrowcolor='rgb(153, 0, 51)')
            # tangential impact plane
            fig.add_annotation(x=veh.p_gx[f'impact_{plotImpactPoint}_tang'][i],
                               y=veh.p_gy[f'impact_{plotImpactPoint}_tang'][i],
                               axref='x',
                               ayref='y',
                               text="",
                               showarrow=True,
                               ax=veh.p_gx[f'POI_{plotImpactPoint}'][i],
                               ay=veh.p_gy[f'POI_{plotImpactPoint}'][i],
                               arrowsize=1,
                               arrowhead=1,
                               arrowwidth=1,
                               arrowcolor='rgb(153, 0, 51)')

            fig.add_trace(go.Scatter(x=[veh.p_gx[f'POI_{plotImpactPoint}'][i], veh.p_gx[f'POI_{plotImpactPoint}'][i]],
                                     y=[veh.p_gy[f'POI_{plotImpactPoint}'][i], veh.p_gy[f'POI_{plotImpactPoint}'][i]],
                                     mode='markers',
                                     name=f'POI: {plotImpactPoint}',
                                     marker=dict(color='rgb(153, 0, 51)', size=7),
                                     ))

    # adjust axes to keep aspect aspect ratio
    """
    dx_max = veh.p_gx.cg.max() + 15
    dx_min = veh.p_gx.cg.min() - 15
    dy_max = veh.p_gy.cg.max() + 15
    dy_min = veh.p_gy.cg.min() - 15
    """
    dx_max = 15
    dx_min = -15
    dy_max = 10
    dy_min = -35

    dx = dx_max - dx_min
    dy = dy_max - dy_min

    if dx > dy:
        adj_x = aspect_ratio * dy / dx
        adj_y = 1
        #print(f" dx > dy -> adj_x = {adj_x}, adj_y = {adj_y}")
        dx_min = round(dx_min * adj_x)
        dx_max = round(dx_max * adj_x)
        #print(f"dx_min = {dx_min}, dx_max = {dx_max}")
        #print(f"dy_min = {dy_min}, dy_max = {dy_max}")
    else:
        adj_x = 1
        adj_y = (1 / aspect_ratio) * dx / dy
        #print(f" dy > dx -> adj_x = {adj_x}, adj_y = {adj_y}")
        dy_min = round(dy_min * adj_y)
        dy_max = round(dy_max * adj_y)
        #print(f"dx_min = {dx_min}, dx_max = {dx_max}")
        #print(f"dy_min = {dy_min}, dy_max = {dy_max}")

    fig.update_layout(
        showlegend = False,
        autosize = False,
        width = width,
        height = width / aspect_ratio,
        title = 'Vehicle Motion in Global Reference Frame',
        template = 'plotly_white',
        xaxis = dict(showgrid = False, title = 'x-axis - Forward (ft)', range = [2*dx_min, 2*dx_max], constrain="domain"),
        yaxis = dict(showgrid = False, title = 'y-axis - Rightward (ft)', scaleanchor = "x", scaleratio = 1),
        font = dict(family = 'Arial', size = font_size, color = 'black'))

    fig.update_xaxes(showline=True, linewidth=1, linecolor='black', ticks="outside",
                     tickwidth=1, tickcolor='black', ticklen=10, zeroline=False, tickfont=dict(size=tick_font_size))
    fig.update_yaxes(autorange="reversed", showline=True, linewidth=1, linecolor='black', ticks="outside",
                     tickwidth=1, tickcolor='black', ticklen=10, zeroline=False, tickfont=dict(size=tick_font_size))

    fig.show()
