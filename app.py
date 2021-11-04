# Run this app with `python app.py` and
# visit http://127.0.0.1:8050/ in your web browser.

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

cases_il = pd.read_csv("data/Israel/Israel_COVIDandVaccinated/geographic-sum-per-day-ver_00536_DS4.csv")
cases_il = cases.get_cases_df_il()

vaccinations_il = pd.read_csv("data/Israel/vaccinated_city_table_ver_00218_DS5.csv")
vaccinations_il = vaccinations.get_vaccinations_df_il()

cases_nsw = pd.read_csv("data/NSW/confirmed_cases_table2_age_group_DS6.csv")
cases_nsw = cases.get_cases_df_nsw()

cases_nl = pd.read_csv(
    "data/Netherlands/COVID-19_aantallen_gemeente_per_dag.csv", sep=";"
)
cases_nl = cases.get_cases_df_nl()

fig_nl = px.line(cases_nl, x="date", y="cases")
fig_nsw = px.line(cases_nsw, x="date", y="cases")
fig_il = px.line(cases_il, x="date", y="cases")


fig_il_vaccinations = px.line(vaccinations_il, x="date", y="vaccinations")

app.layout = html.Div(
    children=[
        html.H1(children="Hello Dash"),
        html.Div(
            children="""
        Dash: A web application framework for your data.
    """
        ),
        dcc.Graph(id="nl_graph", figure=fig_nl),
        html.H5(
            children=f"Latest cases: {helpers.get_latest_kpi_value(cases_nl, 'cases')}, Latest cases per 100k: {helpers.get_latest_kpi_value(cases_nl, 'cases_per_100k')}, Trend {helpers.get_kpi_trend(cases_nl, 'cases')}"
        ),
        dcc.Graph(id="nsw_graph", figure=fig_nsw),
        html.H5(
            children=f"Latest cases: {helpers.get_latest_kpi_value(cases_nsw, 'cases')}, Latest cases per 100k: {helpers.get_latest_kpi_value(cases_nsw, 'cases_per_100k')}, Trend {helpers.get_kpi_trend(cases_nsw, 'cases')}"
        ),
        dcc.Graph(id="il_graph", figure=fig_il),
        html.H5(
            children=f"Latest cases: {helpers.get_latest_kpi_value(cases_il, 'cases')}, Latest cases per 100k: {helpers.get_latest_kpi_value(cases_il, 'cases_per_100k')}, Trend {helpers.get_kpi_trend(cases_il, 'cases')}"
        ),
        dcc.Graph(id="il_vaccinations_graph", figure=fig_il_vaccinations),
    ]
)

if __name__ == "__main__":
    app.run_server(debug=True)
