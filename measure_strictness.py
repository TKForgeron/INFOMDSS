from os import sep
import dash
from dash import dcc
from dash import html
import plotly.express as px
import pandas as pd
from datetime import datetime, timedelta
import helpers
import colors
from website_component import Website_Component
USE_DATA = [
    'measures',
    'prediction'
]


class Measure_Strictness(Website_Component):
    def __init__(self, data):
        self.store_required_data(data, USE_DATA, start_date=None)
        self.levels = 10
        self.get_prediction_vars()

    def get_prediction_vars(self):
        prediction = self.data['prediction']
        print(prediction)
        self.cur_level = round(prediction['stringency_nl_now'].values[0] / 100 * self.levels)
        self.predicted_level = round(prediction['stringency_prediction'].values[0] / 100 * self.levels)

    def get_html(self):
        self.data['prediction'].to_csv('test_i.csv')
        fig = px.line(self.data['measures'], x="date", y="StringencyIndex", color="CountryName")
        self.style_fig(fig)
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
                        className="ms_graph_container co_main",
                        children=[
                            dcc.Graph(id="ms_strictness_graph", figure=fig)
                        ]
                    ),
                    html.Div(
                        className="ms_strictness_container co_main",
                        children=[
                            html.Div(
                                className="ms_container_left",
                                children=[
                                    html.Div(
                                        className="ms_strictness_left",
                                        children=[
                                            html.Div(
                                                className="ms_strictness_current",
                                                children=[
                                                    html.Div(
                                                        className="ms_strictness_label",
                                                        children='Current strictness'
                                                    ),
                                                    html.Div(
                                                        className="ms_strictness_count",
                                                        children=self.get_label_of_level(self.cur_level)
                                                    )
                                                ]
                                            ),
                                            html.Div(
                                                className="ms_strictness_predicted",
                                                children=[
                                                    html.Div(
                                                        className="ms_strictness_label",
                                                        children='Predicted strictness'
                                                    ),
                                                    html.Div(
                                                        className="ms_strictness_count",
                                                        children=self.get_label_of_level(self.predicted_level)
                                                    )
                                                ]
                                            ),
                                            html.Div(
                                                className="ms_bar",
                                                children=self.create_color_bar()
                                            )
                                        ]
                                    ),
                                ]
                            ),
                        html.Div(
                                className="ms_container_right",
                                children=[
                                    html.Div(
                                        children = [
                                            html.H5('Information'),
                                            dcc.Markdown('''
                                            The stringency index ranges between 0 - 100 and indicates the combined strictness of the measures in a country. The higher the index value, the stricter the measures. The model is trained to output a prediction consistent with a synthesis of Dutch, Australian, and Israeli government policies in the past. The algorithm takes in the current data to give an indication on whether it is advisable to increase or decrease stringency policies. This stringency index is provided by [the Oxford Covid-19 Government Response Tracker project](https://github.com/OxCGRT/covid-policy-tracker).
                                            ''')
                                        ]
                                    )
                                ]
                            )
                        ]
                    )
                ])    
        ]

    def get_label_of_level(self, level):
        return str(level * self.levels) + '-' + str((level + 1) * self.levels)

    def style_fig(self, fig):
        fig.update_layout(legend_orientation="h")
        fig.update_layout(margin=dict(r=20, t=0, l=20, b=20), paper_bgcolor='rgb(251, 251, 251)', plot_bgcolor='rgb(251, 251, 251)')
        fig.update_xaxes(gridcolor='rgb(217, 217, 217)')
        fig.update_yaxes(gridcolor='rgb(217, 217, 217)')

    def create_color_bar(self):
        color_list = colors.create_color_list(self.levels)
        html_list = []
        for i, c in enumerate(color_list):
            cur_el = []
            top_childs = []
            if i == self.cur_level:
                top_childs.append(
                    html.Div(
                        className='ms_bar_cur_pointer',
                        children=[
                            html.P("Current"),
                        ]
                    )
                )
            cur_el.append(
                html.Div(
                    className="ms_bar_cur_arrow_container",
                    children=top_childs
                )
            )
            cur_el.append(
                html.Div(
                    className="ms_bar_part_bar",
                    style={ 'backgroundColor': c }
                )
            )
            bottom_childs = []
            if (i == self.predicted_level):
                bottom_childs.append(
                    html.Div(
                        className='ms_bar_pred_pointer',
                        children=[
                            html.P("Predicted"),
                        ]
                    )
                )
            cur_el.append(
                html.Div(
                    className="ms_bar_pred_arrow_container",
                    children=bottom_childs
                )
            )
            html_list.append(
                html.Div(
                    className="ms_bar_part",
                    children=cur_el
                )
            )
        return html_list

