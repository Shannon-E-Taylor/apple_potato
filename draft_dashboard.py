import dash
from dash import dcc, html, Input, Output
import plotly.express as px
import pandas as pd
import plotly.graph_objects as go


simulation = pd.read_csv('data/MAP.csv', sep = ';')

simulation['time'] = simulation['Time']
ICs = simulation[simulation['Time'] == 1]

name = '1'

app = dash.Dash(__name__)
server=app.server

app.layout = html.Div([
    html.Div([
        dcc.Graph(
            id='scatter-3d',
            figure=px.scatter_3d(
                ICs,
                x='X', y='Y', z='Z', color='Wnt',
                custom_data=['TrackID']
            )
        )
    ], style={'width':'50%', 'display':'inline-block'}),

    html.Div([
        dcc.Graph(id='linegraph')
    ], style={'width':'50%', 'display':'inline-block'})
])

@app.callback(
    Output('linegraph', 'figure'),
    Input('scatter-3d', 'clickData')
)
def update_line_graph(clickData):
    print(clickData)
    if clickData is None:
        # Default figure when nothing clicked
        return px.line(title="Click a cell in the 3D scatter")

    track_id = clickData['points'][0]['customdata'][0]
    track_id = f'{track_id}.0'
    track_id = 1000091997.0

    fname = f'data/net{name}_trackID_{track_id}.csv'
    tempo_fname = f'data/net{name}_tempo_trackID_{track_id}.csv'

    tempo = pd.read_csv(tempo_fname)

    df = pd.read_csv(fname)

    attr_fname = f'data/net{name}_attr_trackID_{track_id}.csv'
    attr = pd.read_csv(attr_fname)
    attr.loc[attr['type'] == 'b', 'col'] = 'blue'

    fig = px.line_3d(df, x='x', y='y', z='z',
                    line_group='trajectory')
    fig.update_traces(line_color="#000000", line_width=1)

    # Add tempo
    fig.add_trace(
        go.Scatter3d(
            x=tempo['g1'],
            y=tempo['g2'],
            z=tempo['g3'],

            mode='markers',
            marker=dict(
                size=3,
                color=tempo['tempo'],  # set color to an array/list of desired values
                colorscale='Viridis',   # choose a colorscale
                cmin = 0, cmax = 500,
                opacity=0.8
            )
        )
    )


    # Add attractor
    fig.add_trace(
        go.Scatter3d(
            x=attr['g1'],
            y=attr['g2'],
            z=attr['g3'],
            mode='markers',
            marker=dict(
                size=5,
                color=attr['col'],                # set color to an array/list of desired values
                opacity=0.8
            )
        )
    )
    # Set the initial camera angle
    fig.update_layout(
        scene=dict(
            camera=dict(
                eye=dict(x=0, y=2.5, z=.2)  # controls the view direction
            )
        )
    )

    return fig



if __name__ == '__main__':
    app.run_server(debug=True)
