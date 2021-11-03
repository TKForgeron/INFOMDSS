from os import sep
import dash
from dash import dcc
from dash import html
import plotly.express as px
import pandas as pd
from datetime import datetime, timedelta
import helpers
from website_component import Website_Component
USE_DATA = [
    'measures',
]

class Measure_Strictness(Website_Component):
    def __init__(self, data):
        self.store_required_data(data, USE_DATA, start_date=None)

    def get_html(self):
        self.data['measures'].to_csv('test_i.csv')
        fig = px.line(self.data['measures'], x="date", y="StringencyIndex", color="CountryName")
        return [
            html.Div(
                className="container",
                children=[
                    html.Div(
                        className="titleBar",
                        children=[
                            html.H3('Strictness'),
                            html.Hr()
                        ]
                    ),
                    html.Div(
                        className="ms_graph_container",
                        children=[
                            dcc.Graph(id="ms_strictness_graph", figure=fig)
                        ]
                    )
                ])    
        ]
