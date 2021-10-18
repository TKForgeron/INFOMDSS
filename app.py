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

app = dash.Dash(__name__)

cases_il = pd.read_csv("data/Israel/cases/geographic-sum-per-day-ver_00536_DS4.csv")
cases_nsw = pd.read_csv("data/NSW/cases/confirmed_cases_table2_age_group_DS6.csv")
cases_nl = pd.read_csv(
    "data/Netherlands/cases/COVID-19_aantallen_gemeente_per_dag.csv", sep=";"
)


def get_vacc_per_agegroup(df: pd.DataFrame) -> pd.DataFrame:
    pass


fig_nl = px.line(
    cases.get_last_month_cases_df_nl(cases_nl), x="Date_of_publication", y="cases"
)
fig_nsw = px.line(
    cases.get_last_month_cases_df_nsw(cases_nsw), x="notification_date", y="cases"
)
fig_il = px.line(cases.get_last_month_cases_df_il(cases_il), x="date", y="cases")

app.layout = html.Div(
    children=[
        html.H1(children="Hello Dash"),
        html.Div(
            children="""
        Dash: A web application framework for your data.
    """
        ),
        dcc.Graph(id="nl_graph", figure=fig_nl),
        dcc.Graph(id="nsw_graph", figure=fig_nsw),
        dcc.Graph(id="il_graph", figure=fig_il),
    ]
)

if __name__ == "__main__":
    app.run_server(debug=True)
