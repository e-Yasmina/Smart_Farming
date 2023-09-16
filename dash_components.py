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

ph = html.Div(
    id="control-panel-ph",
    children=[
        daq.Gauge(
            id="ph-gauge",
            color={"gradient":True,"ranges":{"#E0093D":[0,3],"yellow":[3,4.5],"green":[4.5,8],"#E0D906":[8,10],"#E11901":[10,14]}},
            label="Ph",
            min=0,
            max=14,
            value=7,
)
    ],
    n_clicks=0,
)
