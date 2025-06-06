
import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import plotly.graph_objects as go
import pandas as pd

cities = {
    'Tokyo': (35.6895, 139.6917),
    'Osaka': (34.6937, 135.5023),
    'Nagoya': (35.1815, 136.9066),
    'Sapporo': (43.0621, 141.3544),
    'Fukuoka': (33.5902, 130.4017),
    'Kobe': (34.6901, 135.1956),
    'Kyoto': (35.0116, 135.7681),
    'Sendai': (38.2682, 140.8694),
    'Hiroshima': (34.3853, 132.4553),
    'Naha': (26.2124, 127.6809)
}

df_cities = pd.DataFrame(cities, index=['lat', 'lon']).T

app = dash.Dash(__name__)

app.layout = html.Div([
    html.Div([
        html.H4("Earthquake Simulation Controls"),
        dcc.RadioItems(
            id='wave-type',
            options=[
                {'label': 'P waves', 'value': 'P'},
                {'label': 'S waves', 'value': 'S'},
                {'label': 'L waves', 'value': 'L'}
            ],
            value='P'
        )
    ], style={'width': '20%', 'display': 'inline-block', 'verticalAlign': 'top'}),

    html.Div([
        dcc.Graph(id='map-graph', config={'scrollZoom': False})
    ], style={'width': '75%', 'display': 'inline-block'})
])

@app.callback(
    Output('map-graph', 'figure'),
    [Input('map-graph', 'clickData'),
     Input('wave-type', 'value')]
)
def update_map(clickData, wave_type):
    fig = go.Figure()

    fig.add_trace(go.Scattermapbox(
        lat=df_cities['lat'],
        lon=df_cities['lon'],
        mode='markers+text',
        marker=dict(size=10, color='red'),
        text=df_cities.index,
        textposition='top right'
    ))

    fig.update_layout(
        mapbox_style="open-street-map",
        mapbox_center={"lat": 36.2048, "lon": 138.2529},
        mapbox_zoom=4,
        margin={"r":0,"t":0,"l":0,"b":0}
    )

    if clickData:
        lat = clickData['points'][0]['lat']
        lon = clickData['points'][0]['lon']

        wave_speeds = {'P': 6, 'S': 3.5, 'L': 2}
        wave_speed = wave_speeds[wave_type]
        max_radius = 10
        num_circles = 5

        for i in range(1, num_circles + 1):
            radius = i * max_radius / num_circles
            fig.add_trace(go.Scattermapbox(
                lat=[lat],
                lon=[lon],
                mode='markers',
                marker=dict(size=radius * 10, color='blue', opacity=0.3),
                showlegend=False
            ))

    return fig

if __name__ == '__main__':
    app.run_server(debug=True)
