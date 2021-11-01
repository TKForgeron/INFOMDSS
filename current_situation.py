from os import sep
import dash
from dash import dcc
from dash import html
import plotly.express as px
import pandas as pd
from datetime import datetime
import cases
import vaccinations
import hospitalizations
import helpers

cases_nl = cases.get_cases_df_nl()
cases_il = cases.get_cases_df_il()
cases_nsw = cases.get_cases_df_nsw()

vaccinations_nl = vaccinations.get_vaccinations_df_nl()
vaccinations_il = vaccinations.get_vaccinations_df_il()
vaccinations_nsw = vaccinations.get_vaccinations_df_nsw()

hospitalizations_nl = hospitalizations.get_hospitalizations_df_nl()
hospitalizations_il = hospitalizations.get_hospitalizations_df_il()
hospitalizations_nsw = hospitalizations.get_hospitalizations_df_nsw()


class CurrentSituation:
    def __init__(self):
        False

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
                                        { 'x': cases_nl['date'], 'y': cases_nl['cases'], 'type': 'line',  'marker': {'symbol': 'circle'}, 'hovertemplate': '%{x}<br><b>%{y} Cases</b><extra></extra>' }
                                    ],
                                    'layout': {
                                        'xaxis': { 'showgrid': False, 'zeroline': False, 'visible': False, 'showticklabels': False },
                                        'yaxis': { 'showgrid': False, 'zeroline': False, 'visible': False, 'showticklabels': False, 'automargin': False },
                                        'autosize': True,
                                        'plot_bgcolor': 'rgba(255, 255, 255, 0)',
                                        'margin': { 'b': 0, 't': 0, 'r': 0, 'l': 0 },
                                        'marker': False,
                                        'hovermode': 'x',
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
                                            html.H5(children= helpers.get_latest_kpi_value(cases_nl, 'cases')),
                                            html.P("since yesterday")
                                        ]
                                    )
                                ]
                            ),
                            html.Div(
                                className="fiveGrid",
                                children= helpers.get_kpi_trend(cases_nl, 'cases')
                            ),
                            html.Div(
                                className="fiveGrid",
                                children= [
                                    html.Div(
                                        className="compairedCountries",
                                        children= [
                                            html.Span(children= [
                                                    html.P("Israël:"),
                                                    html.P(className="lightpar", children=helpers.get_latest_kpi_value(cases_il, 'cases')),
                                                    helpers.get_kpi_trend_arrow(cases_il, 'cases')
                                                ]),
                                            html.Span(children= [
                                                    html.P("Australia (NSW):"),
                                                    html.P(className="lightpar", children=helpers.get_latest_kpi_value(cases_nsw, 'cases')),
                                                    helpers.get_kpi_trend_arrow(cases_nsw, 'cases')
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
                                        { 'x': hospitalizations_nl['date'], 'y': hospitalizations_nl['hospitalizations'], 'type': 'line',  'marker': {'symbol': 'circle'}, 'hovertemplate': '%{x}<br><b>%{y} Cases</b><extra></extra>' }
                                    ],
                                    'layout': {
                                        'xaxis': { 'showgrid': False, 'zeroline': False, 'visible': False, 'showticklabels': False },
                                        'yaxis': { 'showgrid': False, 'zeroline': False, 'visible': False, 'showticklabels': False, 'automargin': False },
                                        'autosize': True,
                                        'plot_bgcolor': 'rgba(255, 255, 255, 0)',
                                        'margin': { 'b': 0, 't': 0, 'r': 0, 'l': 0 },
                                        'marker': False,
                                        'hovermode': 'x',
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
                                            html.H5(children= helpers.get_latest_kpi_value(hospitalizations_nl, 'hospitalizations')),
                                            html.P("since yesterday")
                                        ]
                                    )
                                ]
                            ),
                            html.Div(
                                className="fiveGrid",
                                children= helpers.get_kpi_trend(cases_nl, 'cases')
                            ),
                            html.Div(
                                className="fiveGrid",
                                children= [
                                    html.Div(
                                        className="compairedCountries",
                                        children= [
                                            html.Span(children= [
                                                    html.P("Israël:"),
                                                    html.P(className="lightpar", children=helpers.get_latest_kpi_value(hospitalizations_il, 'hospitalizations')),
                                                    helpers.get_kpi_trend_arrow(hospitalizations_il, 'hospitalizations')
                                                ]),
                                            html.Span(children= [
                                                    html.P("Australia (NSW):"),
                                                    html.P(className="lightpar", children=helpers.get_latest_kpi_value(hospitalizations_nsw, 'hospitalizations')),
                                                    helpers.get_kpi_trend_arrow(hospitalizations_nsw, 'hospitalizations')
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
                                        { 'x': vaccinations_nl['date'], 'y': vaccinations_nl['vaccinations'], 'type': 'line',  'marker': {'symbol': 'circle'}, 'hovertemplate': '%{x}<br><b>%{y} Cases</b><extra></extra>' }
                                    ],
                                    'layout': {
                                        'xaxis': { 'showgrid': False, 'zeroline': False, 'visible': False, 'showticklabels': False },
                                        'yaxis': { 'showgrid': False, 'zeroline': False, 'visible': False, 'showticklabels': False, 'automargin': False },
                                        'autosize': True,
                                        'plot_bgcolor': 'rgba(255, 255, 255, 0)',
                                        'margin': { 'b': 0, 't': 0, 'r': 0, 'l': 0 },
                                        'marker': False,
                                        'hovermode': 'x',
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
                                            html.H5(children= helpers.get_latest_kpi_value(vaccinations_nl, 'vaccinations')),
                                            html.P("since yesterday")
                                        ]
                                    )
                                ]
                            ),
                            html.Div(
                                className="fiveGrid",
                                children= helpers.get_kpi_trend(vaccinations_nl, 'vaccinations')
                            ),
                            html.Div(
                                className="fiveGrid",
                                children= [
                                    html.Div(
                                        className="compairedCountries",
                                        children= [
                                            html.Span(children= [
                                                    html.P("Israël:"),
                                                    html.P(className="lightpar", children=helpers.get_latest_kpi_value(vaccinations_il, 'vaccinations')),
                                                    helpers.get_kpi_trend_arrow(vaccinations_il, 'vaccinations')
                                                ]),
                                            html.Span(children= [
                                                    html.P("Australia (NSW):"),
                                                    html.P(className="lightpar", children=helpers.get_latest_kpi_value(vaccinations_nsw, 'vaccinations')),
                                                    helpers.get_kpi_trend_arrow(vaccinations_nsw, 'vaccinations')
                                                ]),
                                        ]
                                    )
                                ]
                            )
                        ])

            ]
        )]