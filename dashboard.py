import pandas as pd
import numpy as np
import random
from datetime import datetime, timedelta
import time


from dash_components import temperature
from dash_components import ph
from dash_components import humidity

import dash
from dash import dcc, html
from dash.dependencies import State, Input, Output 
import dash_daq as daq

import plotly
import plotly.graph_objs as go
import plotly.express as px

columns = [
    'timestamp', 'temperature', 'humidity', 'soil_temperature', 'soil_moisture',
    'soil_ph', 'soil_nitrogen', 'soil_phosphorus', 'soil_potassium', 'soil_conductivity'
]

# Define mean and standard deviation for each column
column_stats = {
    'temperature': {'mean': 25, 'std': 5},
    'humidity': {'mean': 60, 'std': 10},
    'soil_temperature': {'mean': 20, 'std': 4},
    'soil_moisture': {'mean': 50, 'std': 15},
    'soil_ph': {'mean': 6.5, 'std': 0.5},
    'soil_nitrogen': {'mean': 20, 'std': 5},
    'soil_phosphorus': {'mean': 10, 'std': 3},
    'soil_potassium': {'mean': 15, 'std': 4},
    'soil_conductivity': {'mean': 1000, 'std': 200}
}



def generate_historical_and_real_time_data():
    # Create a list to store data
    synthetic_data = []

    # Start with the current time for both historical and real-time data
    current_timestamp1 = current_timestamp2 = datetime.now()

    # Generate historical data for 24 hours
    for _ in range(6 * 12 * 60):  # 24 hours * 60 minutes *12
        row = ["ferme anoljdid", "90A5446B6867", current_timestamp1]

        for column in columns[1:]:
            mean = column_stats[column]['mean']
            std = column_stats[column]['std']
            value = random.normalvariate(mean, std)
            row.append(value)

        synthetic_data.append(row)
        current_timestamp1 -= timedelta(seconds=5)  # Subtract 5 seconds for the next data point

    # Reverse the list to have data in ascending order
    synthetic_data.reverse()

    # Create a DataFrame from the historical data
    historical_df = pd.DataFrame(synthetic_data, columns=[
        'Device Name','Device Number','timestamp', 'temperature', 'humidity', 'soil_temperature', 'soil_moisture',
        'soil_ph', 'soil_nitrogen', 'soil_phosphorus', 'soil_potassium', 'soil_conductivity'
    ])

    return historical_df




# Initialize the Dash app
app = dash.Dash(__name__)
server=app.server

# Define custom CSS styles
custom_styles = {
    'backgroundColor': '#1e1917',
    'color': 'white',
}

# Generate the initial DataFrame
df =generate_historical_and_real_time_data()
temperature_value =df['temperature'].iloc[-1]
ph_value= df['soil_ph'].iloc[-1]
humidity_value= df['humidity'].iloc[-1]

# Define the layout of your dashboard
app.layout = html.Div([
    html.H1("Farm Data Dashboard", className="dash-title"),

    html.Div([
        html.Div([
            html.Label("Select a Device", style={'color': '#1e1917'}),
            dcc.Dropdown(
                id='device-dropdown',
                options=[{'label': device, 'value': device} for device in df['Device Name'].unique()],
                value=df['Device Name'].unique()[0],
                multi=False,
            ),
        ], className="dropdown-container"),

        html.Div([
            html.Label("Select a Variable", style={'color': '#1e1917'}),
            dcc.Dropdown(
                id='variable-dropdown',
                options=[{'label': variable, 'value': variable} for variable in df.columns if variable not in ['Number', 'Device Name', 'Device Number', 'Receive Time','timestamp', 'unit']],
                value='temperature',
                multi=False,
            ),
        ], className="dropdown-container"),
    ], className="dropdown-row"),

    dcc.Graph(id='selected-variable-graph', animate=True),

    html.Div(
        children=[
            temperature,
            ph,
            humidity,
        ],
        className="gauges-row"
    ),
    dcc.Interval(id='graph-update', interval=5*1000),
])

# Define callback to update the graph based on device and variable selection
@app.callback(
    Output('selected-variable-graph', 'figure'),
    [Input('device-dropdown', 'value'),
     Input('variable-dropdown', 'value'),
     Input('graph-update', 'n_intervals')]
)
def update_graph(selected_device, selected_variable, n):
    global df, temperature_value, ph_value, humidity_value  # Make sure we use the global DataFrame for real-time updates

    # Append new real-time data to the existing DataFrame
    row = ["ferme anoljdid", "90A5446B6867", datetime.now()]

    for column in columns[1:]:
        mean = column_stats[column]['mean']
        std = column_stats[column]['std']
        value = random.normalvariate(mean, std)
        row.append(value)
    
    temperature_value = row[3]
    ph_value= row[7]
    humidity_value= row[4]
    new_data = pd.DataFrame([row], columns=df.columns)
    df = pd.concat([df, new_data], ignore_index=True)
    
    df = df.iloc[-60:]

    filtered_df = df[df['Device Name'] == selected_device]

    # Create a line chart for the selected variable
    trace = go.Scatter(
        x=filtered_df['timestamp'],
        y=filtered_df[selected_variable],
        mode="lines",
        name=selected_variable,
        line={"color": "rgb(196, 69, 237)"},
    )

    # Format the variable name for the title
    formatted_variable = selected_variable.replace('_', ' ').title()

    fig = go.Figure(data=[trace])
    fig.update_layout(
    # title={'text': f'{formatted_variable} over Time', 'x': 0.5},
    title=dict(
            text=f'{formatted_variable} over Time',
            font=dict(size=20),
            x=0.5  # center the title
        ),
    xaxis=dict(range=[min(filtered_df['timestamp']), max(filtered_df['timestamp'])]),
    yaxis=dict(range=[min(filtered_df[selected_variable]), max(filtered_df[selected_variable])]),
    template='plotly_dark',
    )
    return fig


# Define callback to update the temperature gauge
@app.callback(
    [Output("temperature-gauge", "value"), Output("temperature-gauge", "color")],
    Input('graph-update', 'n_intervals')
)
def update_temperature_and_color(n):
    # Replace this with your real-time temperature data source
    new_temperature_value = temperature_value
    color = "#D90702"  # Default color
    if 25 <= new_temperature_value <= 45:
        color = "#36c92e"  # Green if within [25, 45] range
    
    return new_temperature_value, color


@app.callback(
    Output("ph-gauge", "value"),
    Input('graph-update', 'n_intervals')
)
def update_ph_value(n):
    # Replace this with your real-time temperature data source
    new_ph_value = ph_value
    
    return new_ph_value


@app.callback(
    Output("humidity-gauge", "value"),
    Input('graph-update', 'n_intervals')
)
def update_humidity_value(n):
    # Replace this with your real-time temperature data source
    new_humidity_value = humidity_value
    
    return new_humidity_value
