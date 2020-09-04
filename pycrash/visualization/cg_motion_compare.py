import plotly.graph_objects as go

width = 900
aspect_ratio = 16 / 9
figure_size = (width, width / aspect_ratio)


def cg_motion(model1, model2, name1, name2):
    dx_max = max(model1.Dx.max(), model2.Dx.max())
    dx_min = min(model1.Dx.min(), model2.Dx.min())
    dy_max = max(model1.Dy.max(), model2.Dy.max())
    dy_min = min(model1.Dy.min(), model2.Dy.min())

    dx = dx_max - dx_min
    dy = dy_max - dy_min

    if dx > dy:
        adj_y = aspect_ratio * dy / dx
        adj_x = 1
        print(f" dx > dy -> adj_x = {adj_x}, adj_y = {adj_y}")
        print(f"dx_min = {dx_min}, dx_max = {dx_max}")
        print(f"dy_min = {dy_min}, dy_max = {dy_max}")
    else:
        adj_y = 1
        adj_x = (1 / aspect_ratio) * dx / dy
        print(f" dy > dx -> adj_x = {adj_x}, adj_y = {adj_y}")
        print(f"dx_min = {dx_min}, dx_max = {dx_max}")
        print(f"dy_min = {dy_min}, dy_max = {dy_max}")

    """
    plot location of CG in global reference frame
    """
    fig = go.Figure()

    fig.add_trace(go.Scatter(x=model1.Dx, y=model1.Dy,
                             mode='markers',
                             name=f'{name1}',
                             marker=dict(color='rgb(0, 0, 0)', size=2)
                             ))
    fig.add_trace(go.Scatter(x=model2.Dx, y=model2.Dy,
                             mode='markers',
                             name=f'{name2}',
                             marker=dict(color='rgb(0, 0, 256)', size=2)
                             ))

    fig.update_layout(
        showlegend=False,
        autosize=False,
        width=width,
        height=width / aspect_ratio,
        title='Vehicle Motion in Global Reference Frame',
        template='plotly_white',
        xaxis=dict(showgrid=False, title='x-axis - Forward (ft)'),
        yaxis=dict(showgrid=False, title='y-axis - Rightward (ft)'),
        font=dict(family='Arial', size=16, color='black'))

    fig.update_xaxes(showline=True, linewidth=1, linecolor='black', ticks="outside",
                     tickwidth=1, tickcolor='black', ticklen=10, zeroline=False, range = [dx_min * adj_x, dx_max * adj_x])
    fig.update_yaxes(autorange='reversed', showline=True, linewidth=1, linecolor='black', ticks="outside",
                     tickwidth=1, tickcolor='black', ticklen=10, zeroline=False, range = [-67, dy_max * adj_y])
    fig.show()
