

import pandas as pd
import numpy as np
import random
from datetime import datetime, timedelta
import time


import dash
from dash import dcc, html
from dash.dependencies import Input, Output 
import pandas as pd
import plotly.express as px

import plotly
import random
import plotly.graph_objs as go


# Replace these with the actual column names
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
    for _ in range(6 * 60):  # 24 hours * 60 minutes
        row = ["ferme anoljdid", "90A5446B6867", current_timestamp1]

        for column in columns[1:]:
            mean = column_stats[column]['mean']
            std = column_stats[column]['std']
            value = random.normalvariate(mean, std)
            row.append(value)

        synthetic_data.append(row)
        current_timestamp1 -= timedelta(minutes=1)  # Subtract 1 minute for the next data point

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

# Define custom CSS styles
custom_styles = {
    'backgroundColor': '#1e1917',
    'color': 'white',
}

# Generate the initial DataFrame
df =generate_historical_and_real_time_data()

# Define the layout of your dashboard
app.layout = html.Div(style={'backgroundColor': '#d2bea5', 'color': 'white'}, children=[
    html.H1("Farm Data Dashboard", style={'color': '#744e3a'}),

    html.Div([
        html.Div([
            html.Label("Select a Device", style={'color': '#1e1917'}),
            dcc.Dropdown(
                id='device-dropdown',
                options=[{'label': device, 'value': device} for device in df['Device Name'].unique()],
                value=df['Device Name'].unique()[0],
                multi=False,
            ),
        ], style={'margin-bottom': '20px', 'width': '48%', 'display': 'inline-block', 'margin-right': '100px', 'margin-left': '100px'}),

        html.Div([
            html.Label("Select a Variable", style={'color': '#1e1917'}),
            dcc.Dropdown(
                id='variable-dropdown',
                options=[{'label': variable, 'value': variable} for variable in df.columns if variable not in ['Number', 'Device Name', 'Device Number', 'Receive Time','timestamp', 'unit']],
                value='temperature',  # Default variable to display
                multi=False,
            ),
        ], style={'margin-bottom': '20px', 'width': '48%', 'display': 'inline-block', 'margin-right': '100px', 'margin-left': '100px'}),
    ]),

    dcc.Graph(id='selected-variable-graph', animate=True),
    dcc.Interval( id='graph-update', interval=5*1000),
])

# Define callback to update the graph based on device and variable selection
# Define callback to update the graph based on device and variable selection
@app.callback(
    Output('selected-variable-graph', 'figure'),
    [Input('device-dropdown', 'value'),
     Input('variable-dropdown', 'value'),
     Input('graph-update', 'n_intervals')]
)


def update_graph(selected_device, selected_variable, n):
    global df  # Make sure we use the global DataFrame for real-time updates

    # Append new real-time data to the existing DataFrame
    row = ["ferme anoljdid", "90A5446B6867", datetime.now()]

    for column in columns[1:]:
        mean = column_stats[column]['mean']
        std = column_stats[column]['std']
        value = random.normalvariate(mean, std)
        row.append(value)

    new_data = pd.DataFrame([row], columns=df.columns)
    df = pd.concat([df, new_data], ignore_index=True)
    
    df = df.iloc[-60:]

    filtered_df = df[df['Device Name'] == selected_device]

    # Create a line chart for the selected variable
     # Create the graph trace
    trace = go.Scatter(
        x=filtered_df['timestamp'],
        y=filtered_df[selected_variable],
        mode="lines",
        name=selected_variable,
        line={"color": "rgb(230, 25, 2)"},

    )

    # Create the graph layout
    layout = go.Layout(
        title=f'{selected_variable} over Time',
        xaxis=dict(range=[min(filtered_df['timestamp']), max(filtered_df['timestamp'])]),
        yaxis=dict(range=[min(filtered_df[selected_variable]), max(filtered_df[selected_variable])]),
    )
    

    variable_graph = {"data": [trace], "layout": layout}

    return variable_graph
