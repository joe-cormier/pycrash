import plotly.graph_objects as go


def cg_motion(model1, model2, name1, name2):
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
        width=900,
        height=900,
        title='Vehicle Motion in Global Reference Frame',
        template='plotly_white',
        xaxis=dict(showgrid=False, title='x-axis - Forward (ft)'),
        yaxis=dict(showgrid=False, title='y-axis - Rightward (ft)'),
        font=dict(family='Arial', size=16, color='black'))

    fig.update_xaxes(showline=True, linewidth=1, linecolor='black', ticks="outside",
                     tickwidth=1, tickcolor='black', ticklen=10, zeroline=False)
    fig.update_yaxes(autorange='reversed', showline=True, linewidth=1, linecolor='black', ticks="outside",
                     tickwidth=1, tickcolor='black', ticklen=10, zeroline=False)
    fig.show()
