from dash import dcc, html

import dash

from dash.dependencies import State, Input, Output
import dash_daq as daq



temperature = html.Div(
    id="control-panel-temperature",
    children=[
        daq.Thermometer(
            id="temperature-gauge",
            label="Temperature",
            min=0,
            max=100,
            value=72.5,
            units="°C",
            showCurrentValue=True,
            color="#D90702"
        )
    ],
    n_clicks=0,
)
