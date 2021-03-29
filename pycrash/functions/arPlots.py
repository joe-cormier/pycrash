import plotly.graph_objects as go
import plotly.io as pio

pio.renderers.default = "plotly_mimetype"  # <- determines how plots are displayed using Plotly
# "browser"  # <- determines how plots are displayed using Plotly


def plot_TotalFdx(df):
    """ dataframe with at least two columns
    Disp - vehicle displacment in feet
    TotalForce - barrier force in lb
    """
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=df.Disp,
                             y=df.TotalForce * -1,
                             mode='lines',
                             name="Total Force",
                             line=dict(color="rgb(52, 64, 235)", width=2)
                             ))
    fig.update_layout(
        autosize=False,
        width=1000,
        height=550,
        title=f'Load Cell Barrier Force-Displacement Data',
        template='plotly_white',
        xaxis=dict(showgrid=False, title='Displacement (feet)'),
        font=dict(family='Arial', size=24, color='black'))

    fig.update_layout(showlegend=False)
    fig.update_yaxes(showgrid=False, showline=True, linewidth=1, linecolor='black', ticks="outside",
                     tickwidth=1, tickcolor='black', ticklen=10, zeroline=False, title_text='Force (lb)')
    fig.update_xaxes(showline=True, linewidth=1, linecolor='black', ticks="outside",
                     tickwidth=1, tickcolor='black', ticklen=10, zeroline=False)
    fig.show()
