import dash
from dash import dcc
from dash import html
from dash.dependencies import Input, Output
import pandas as pd
import plotly.express as px

# Initialize the Dash app
app = dash.Dash(__name__)
server=app.server

# Load your Excel data
file_path = "90A5446B6867-ferme anoljdidÀúÊ·Êý¾Ý (3).xls"
df = pd.read_excel(file_path)

# Define the layout of your dashboard
app.layout = html.Div([
    html.H1("Farm Data Dashboard"),

    # Dropdown to select a device
    dcc.Dropdown(
        id='device-dropdown',
        options=[{'label': device, 'value': device} for device in df['Device Name'].unique()],
        value=df['Device Name'].unique()[0],
        multi=False
    ),

    # Dropdown to select a variable
    dcc.Dropdown(
        id='variable-dropdown',
        options=[{'label': variable, 'value': variable} for variable in df.columns if variable not in ['Number', 'Device Name', 'Device Number', 'Receive Time']],
        value='temperature',  # Default variable to display
        multi=False
    ),

    # Line chart for the selected variable
    dcc.Graph(id='selected-variable-graph'),
])

# Define callback to update the graph based on device and variable selection
@app.callback(
    Output('selected-variable-graph', 'figure'),
    [Input('device-dropdown', 'value'),
     Input('variable-dropdown', 'value')]
)
def update_graph(selected_device, selected_variable):
    filtered_df = df[df['Device Name'] == selected_device]

    # Create a line chart for the selected variable
    variable_graph = px.line(filtered_df, x='Receive Time', y=selected_variable, title=f'{selected_variable} over Time')

    return variable_graph

# Run the app
if __name__ == '__main__':
    app.run_server(debug=True)
