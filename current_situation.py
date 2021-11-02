from os import sep
import dash
from dash import dcc
from dash import html
import plotly.express as px
import pandas as pd
from datetime import datetime, timedelta
import helpers
from website_component import Website_Component
SHOW_HISTORIC_DAYS = 90
USE_DATA = [
    'hospitalizations_nl',
    'hospitalizations_il',
    'hospitalizations_nsw',
    'vaccinations_nl',
    'vaccinations_il',
    'vaccinations_nsw',
    'cases_nl',
    'cases_il',
    'cases_nsw'
]

class CurrentSituation(Website_Component):
    def __init__(self, data):
        start_date = datetime.today() - timedelta(days=SHOW_HISTORIC_DAYS)
        self.store_required_data(data, USE_DATA, start_date=start_date)

    def get_html(self):
        return [
            html.Div(
                className="container",
                children=[
                    html.Div(
                        className="titleBar",
                        children=[
                            html.H3('Current Situation'),
                            html.Hr()
                        ]),
                    html.Div(
                        className="situationBox negativeColors",
                        children=[
                            html.Div(
                                className="fiveGrid",
                                children= html.H4('Cases')
                            ),
                            html.Div(
                                className="fiveGrid cs_graph",
                                children=dcc.Graph(id="cs_cases_graph", className="cs_graph", figure={
                                    'data': [
                                        { 'x': self.data['cases_nl']['date'], 'y': self.data['cases_nl']['cases'], 'type': 'line',  'marker': {'symbol': 'circle'}, 'hovertemplate': '<b>%{y} Cases</b><extra></extra>' }
                                    ],
                                    'layout': {
                                        'xaxis': { 'showgrid': False, 'zeroline': False, 'visible': False, 'showticklabels': False },
                                        'yaxis': { 'showgrid': False, 'zeroline': False, 'visible': False, 'showticklabels': False, 'automargin': False },
                                        'autosize': True,
                                        'plot_bgcolor': 'rgba(255, 255, 255, 0)',
                                        'margin': { 'b': 0, 't': 0, 'r': 0, 'l': 0 },
                                        'marker': False,
                                        'hovermode': 'x unified',
                                        'hoverlabel': {
                                            'bordercolor': 'rgb(229 229 229)',
                                            'bgcolor': 'white',
                                            'font': {
                                                'color': 'black'
                                            }
                                        }
                                    }
                                }, config={ 'staticPlot': False })
                            ),
                            html.Div(
                                className="fiveGrid",
                                children= [
                                    html.Div(
                                        className="counter",
                                        children= [
                                            html.H5(children= helpers.get_latest_kpi_value(self.data['cases_nl'], 'cases')),
                                            html.P("since yesterday")
                                        ]
                                    )
                                ]
                            ),
                            html.Div(
                                className="fiveGrid",
                                children= helpers.get_kpi_trend(self.data['cases_nl'], 'cases')
                            ),
                            html.Div(
                                className="fiveGrid",
                                children= [
                                    html.Div(
                                        className="compairedCountries",
                                        children= [
                                            html.Span(children= [
                                                    html.P("Israël:"),
                                                    html.P(className="lightpar", children=helpers.get_latest_kpi_value(self.data['cases_il'], 'cases')),
                                                    helpers.get_kpi_trend_arrow(self.data['cases_il'], 'cases')
                                                ]),
                                            html.Span(children= [
                                                    html.P("Australia (NSW):"),
                                                    html.P(className="lightpar", children=helpers.get_latest_kpi_value(self.data['cases_nsw'], 'cases')),
                                                    helpers.get_kpi_trend_arrow(self.data['cases_nsw'], 'cases')
                                                ]),
                                        ]
                                    )
                                ]
                            )
                        ]),
                    html.Div(
                        className="situationBox negativeColors",
                        children=[
                            html.Div(
                                className="fiveGrid",
                                children= html.H4('Hospitalizations')
                            ),
                            html.Div(
                                className="fiveGrid cs_graph",
                                children=dcc.Graph(id="cs_hosp_graph", className="cs_graph", figure={
                                    'data': [
                                        { 'x': self.data['hospitalizations_nl']['date'], 'y': self.data['hospitalizations_nl']['hospitalizations'], 'type': 'line',  'marker': {'symbol': 'circle'}, 'hovertemplate': '<b>%{y} Hospitalizations</b><extra></extra>' }
                                    ],
                                    'layout': {
                                        'xaxis': { 'showgrid': False, 'zeroline': False, 'visible': False, 'showticklabels': False },
                                        'yaxis': { 'showgrid': False, 'zeroline': False, 'visible': False, 'showticklabels': False, 'automargin': False },
                                        'autosize': True,
                                        'plot_bgcolor': 'rgba(255, 255, 255, 0)',
                                        'margin': { 'b': 0, 't': 0, 'r': 0, 'l': 0 },
                                        'marker': False,
                                        'hovermode': 'x unified',
                                        'hoverlabel': {
                                            'bordercolor': 'rgb(229 229 229)',
                                            'bgcolor': 'white',
                                            'font': {
                                                'color': 'black'
                                            }
                                        }
                                    }
                                }, config={ 'staticPlot': False })
                            ),
                            html.Div(
                                className="fiveGrid",
                                children= [
                                    html.Div(
                                        className="counter",
                                        children= [
                                            html.H5(children= helpers.get_latest_kpi_value(self.data['hospitalizations_nl'], 'hospitalizations')),
                                            html.P("since yesterday")
                                        ]
                                    )
                                ]
                            ),
                            html.Div(
                                className="fiveGrid",
                                children= helpers.get_kpi_trend(self.data['cases_nl'], 'cases')
                            ),
                            html.Div(
                                className="fiveGrid",
                                children= [
                                    html.Div(
                                        className="compairedCountries",
                                        children= [
                                            html.Span(children= [
                                                    html.P("Israël:"),
                                                    html.P(className="lightpar", children=helpers.get_latest_kpi_value(self.data['hospitalizations_il'], 'hospitalizations')),
                                                    helpers.get_kpi_trend_arrow(self.data['hospitalizations_il'], 'hospitalizations')
                                                ]),
                                            html.Span(children= [
                                                    html.P("Australia (NSW):"),
                                                    html.P(className="lightpar", children=helpers.get_latest_kpi_value(self.data['hospitalizations_nsw'], 'hospitalizations')),
                                                    helpers.get_kpi_trend_arrow(self.data['hospitalizations_nsw'], 'hospitalizations')
                                                ]),
                                        ]
                                    )
                                ]
                            )
                        ]),
                     html.Div(
                        className="situationBox positiveColors",
                        children=[
                            html.Div(
                                className="fiveGrid",
                                children= html.H4('Vaccination')
                            ),
                            html.Div(
                                className="fiveGrid cs_graph",
                                children=dcc.Graph(id="cs_vac_graph", className="cs_graph", figure={
                                    'data': [
                                        { 'x': self.data['vaccinations_nl']['date'], 'y': self.data['vaccinations_nl']['vaccinations'], 'type': 'line',  'marker': {'symbol': 'circle'}, 'hovertemplate': '<b>%{y} Cases</b><extra></extra>' }
                                    ],
                                    'layout': {
                                        'xaxis': { 'showgrid': False, 'zeroline': False, 'visible': False, 'showticklabels': False },
                                        'yaxis': { 'showgrid': False, 'zeroline': False, 'visible': False, 'showticklabels': False, 'automargin': False },
                                        'autosize': True,
                                        'plot_bgcolor': 'rgba(255, 255, 255, 0)',
                                        'margin': { 'b': 0, 't': 0, 'r': 0, 'l': 0 },
                                        'marker': False,
                                        'hovermode': 'x unified',
                                        'hoverlabel': {
                                            'bordercolor': 'rgb(229 229 229)',
                                            'bgcolor': 'white',
                                            'font': {
                                                'color': 'black'
                                            }
                                        }
                                    }
                                }, config={ 'staticPlot': False })
                            ),
                            html.Div(
                                className="fiveGrid",
                                children= [
                                    html.Div(
                                        className="counter",
                                        children= [
                                            html.H5(children= helpers.get_latest_kpi_value(self.data['vaccinations_nl'], 'vaccinations')),
                                            html.P("since yesterday")
                                        ]
                                    )
                                ]
                            ),
                            html.Div(
                                className="fiveGrid",
                                children= helpers.get_kpi_trend(self.data['vaccinations_nl'], 'vaccinations')
                            ),
                            html.Div(
                                className="fiveGrid",
                                children= [
                                    html.Div(
                                        className="compairedCountries",
                                        children= [
                                            html.Span(children= [
                                                    html.P("Israël:"),
                                                    html.P(className="lightpar", children=helpers.get_latest_kpi_value(self.data['vaccinations_il'], 'vaccinations')),
                                                    helpers.get_kpi_trend_arrow(self.data['vaccinations_il'], 'vaccinations')
                                                ]),
                                            html.Span(children= [
                                                    html.P("Australia (NSW):"),
                                                    html.P(className="lightpar", children=helpers.get_latest_kpi_value(self.data['vaccinations_nsw'], 'vaccinations')),
                                                    helpers.get_kpi_trend_arrow(self.data['vaccinations_nsw'], 'vaccinations')
                                                ]),
                                        ]
                                    )
                                ]
                            )
                        ])

            ]
        )]