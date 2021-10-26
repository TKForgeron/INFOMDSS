from os import sep
import dash
from dash import dcc
from dash import html
import plotly.express as px
import pandas as pd
from datetime import datetime
import cases
import vaccinations
import helpers

app = dash.Dash(__name__)

cases_il = pd.read_csv("data/Israel/cases/geographic-sum-per-day-ver_00536_DS4.csv")
cases_il = cases.get_cases_df_il(cases_il, months=1)

vaccinations_il = pd.read_csv("data/Israel/vaccinated_city_table_ver_00218_DS5.csv")
vaccinations_il = vaccinations.get_vaccinations_df_il(vaccinations_il, months=1)

cases_nsw = pd.read_csv("data/NSW/cases/confirmed_cases_table2_age_group_DS6.csv")
cases_nsw = cases.get_cases_df_nsw(cases_nsw, months=1)

cases_nl = pd.read_csv(
    "data/Netherlands/cases/COVID-19_aantallen_gemeente_per_dag.csv", sep=";"
)
cases_nl = cases.get_cases_df_nl(cases_nl, months=1)

fig_nl = px.line(cases_nl, x="date", y="cases")
fig_nsw = px.line(cases_nsw, x="date", y="cases")
fig_il = px.line(cases_il, x="date", y="cases")

fig_il_vaccinations = px.line(vaccinations_il, x="date", y ="vaccinations")

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
                        className="situationBox",
                        children=[
                            html.Div(
                                className="fiveGrid",
                                children= html.H4('Cases')
                            ),
                            html.Div(
                                className="fiveGrid",
                                children= html.H4('Cases')
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
                                children= html.H4('Cases')
                            )
                        ]),
                    html.Div(
                        className="situationBox",
                        children=[
                            html.H4('Hospitalisations')
                        ]),
                     html.Div(
                        className="situationBox",
                        children=[
                            html.H4('Vaccinations')
                        ])

            ]
        )]