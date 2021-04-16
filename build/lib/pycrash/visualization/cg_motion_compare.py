import plotly.graph_objects as go
import plotly.io as pio
pio.renderers.default = "browser"
font_size = 24
tick_font_size = 24
width = 1900
aspect_ratio = 16 / 9
figure_size = (width, width / aspect_ratio)


def cg_motion(model1, model2, name1, name2):
    dx_max = max(model1.Dx.max(), model2.Dx.max())
    dx_min = min(model1.Dx.min(), model2.Dx.min())
    dy_max = max(model1.Dy.max(), model2.Dy.max())
    dy_min = min(model1.Dy.min(), model2.Dy.min())

    dx = dx_max - dx_min
    dy = dy_max - dy_min

    if dx < dy:
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

    """
    plot location of CG in global reference frame
    """
    fig = go.Figure()

    fig.add_trace(go.Scatter(x=model1.Dx, y=model1.Dy,
                             mode='markers',
                             name=f'{name1}',
                             marker=dict(color='rgb(0, 0, 0)', size=3.5),
                             ))
    fig.add_trace(go.Scatter(x=model2.Dx, y=model2.Dy,
                             mode='markers',
                             name=f'{name2}',
                             marker=dict(color='rgb(0, 0, 256)', size=5)
                             ))

    fig.update_layout(
        showlegend=True,
        autosize=False,
        width=width,
        height=width / aspect_ratio,
        title='Vehicle Motion in Global Reference Frame',
        template='plotly_white',
        xaxis=dict(showgrid=False, title='x-axis - Forward (ft)', range = [dx_min, dx_max]),
        yaxis=dict(showgrid=False, title='y-axis - Rightward (ft)', range = [dy_max, dy_min]),
        font=dict(family='Arial', size=font_size, color='black'))

    fig.update_xaxes(showline=True, linewidth=1, linecolor='black', ticks="outside",
                     tickwidth=1, tickcolor='black', ticklen=10, zeroline=False, tickfont=dict(size=tick_font_size))
    fig.update_yaxes(showline=True, linewidth=1, linecolor='black', ticks="outside",
                     tickwidth=1, tickcolor='black', ticklen=10, zeroline=False, tickfont=dict(size=tick_font_size))
    fig.show()
