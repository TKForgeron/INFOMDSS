from os import sep
import dash
from dash import dcc
from dash import html
from website_component import Website_Component

USE_DATA = [
    'vaccinations_agegroup_nl'
]

class Vaccinations_AgeGroup(Website_Component):
    def __init__(self, data):
        self.store_required_data(data, USE_DATA)

    def get_html(self):
        return [
            html.Div(
                className="container",
                children=[
                        html.Div(
                        className="titleBar",
                        children=[
                            html.H3('Vaccinations Per Age Group'),
                            html.Hr()
                        ]),
                        html.Div(
                            children=dcc.Graph(id="cs_per_age_graph", figure={
                                'data': [
                                    { 'x': self.data['vaccinations_agegroup_nl']['date'], 'y': self.data['vaccinations_agegroup_nl']['<1931'], 'name': '90+','type': 'line',  'marker': {'symbol': 'circle'}, 'line': {'color': '#c5ceff', 'dash': 'solid'}, 'hovertemplate': '<b>Vaccinations: %{y} Date %{x}</b><extra></extra>', 'xaxis': 'x', 'yaxis': 'y', },
                                    { 'x': self.data['vaccinations_agegroup_nl']['date'], 'y': self.data['vaccinations_agegroup_nl']['1931-1935'], 'type': 'line',  'marker': {'symbol': 'circle'}, 'line': {'color': '#bac4fe', 'dash': 'solid'}, 'hovertemplate': '<b>Vaccinations: %{y} Date: %{x}</b><extra></extra>' },
                                    { 'x': self.data['vaccinations_agegroup_nl']['date'], 'y': self.data['vaccinations_agegroup_nl']['1936-1940'], 'type': 'line',  'marker': {'symbol': 'circle'}, 'line': {'color': '#afbafd', 'dash': 'solid'}, 'hovertemplate': '<b>Vaccinations: %{y} Date: %{x}</b><extra></extra>' },
                                    { 'x': self.data['vaccinations_agegroup_nl']['date'], 'y': self.data['vaccinations_agegroup_nl']['1946-1950'], 'type': 'line',  'marker': {'symbol': 'circle'}, 'line': {'color': '#a5b0fb', 'dash': 'solid'}, 'hovertemplate': '<b>Vaccinations: %{y} Date: %{x}</b><extra></extra>' },
                                    { 'x': self.data['vaccinations_agegroup_nl']['date'], 'y': self.data['vaccinations_agegroup_nl']['1941-1945'], 'type': 'line',  'marker': {'symbol': 'circle'}, 'line': {'color': '#9aa6fa', 'dash': 'solid'}, 'hovertemplate': '<b>Vaccinations: %{y} Date: %{x}</b><extra></extra>' },
                                    { 'x': self.data['vaccinations_agegroup_nl']['date'], 'y': self.data['vaccinations_agegroup_nl']['1951-1955'], 'type': 'line',  'marker': {'symbol': 'circle'}, 'line': {'color': '#909cf8', 'dash': 'solid'}, 'hovertemplate': '<b>Vaccinations: %{y} Date: %{x}</b><extra></extra>' },
                                    { 'x': self.data['vaccinations_agegroup_nl']['date'], 'y': self.data['vaccinations_agegroup_nl']['1956-1960'], 'type': 'line',  'marker': {'symbol': 'circle'}, 'line': {'color': '#8592f6', 'dash': 'solid'}, 'hovertemplate': '<b>Vaccinations: %{y} Date: %{x}</b><extra></extra>' },
                                    { 'x': self.data['vaccinations_agegroup_nl']['date'], 'y': self.data['vaccinations_agegroup_nl']['1961-1965'], 'type': 'line',  'marker': {'symbol': 'circle'}, 'line': {'color': '#7b88f4', 'dash': 'solid'}, 'hovertemplate': '<b>Vaccinations: %{y} Date: %{x}</b><extra></extra>' },
                                    { 'x': self.data['vaccinations_agegroup_nl']['date'], 'y': self.data['vaccinations_agegroup_nl']['1966-1970'], 'type': 'line',  'marker': {'symbol': 'circle'}, 'line': {'color': '#717ef2', 'dash': 'solid'}, 'hovertemplate': '<b>Vaccinations: %{y} Date: %{x}</b><extra></extra>' },
                                    { 'x': self.data['vaccinations_agegroup_nl']['date'], 'y': self.data['vaccinations_agegroup_nl']['1971-1975'], 'type': 'line',  'marker': {'symbol': 'circle'}, 'line': {'color': '#6674ef', 'dash': 'solid'}, 'hovertemplate': '<b>Vaccinations: %{y} Date: %{x}</b><extra></extra>' },
                                    { 'x': self.data['vaccinations_agegroup_nl']['date'], 'y': self.data['vaccinations_agegroup_nl']['1976-1980'], 'type': 'line',  'marker': {'symbol': 'circle'}, 'line': {'color': '#5c69ec', 'dash': 'solid'}, 'hovertemplate': '<b>Vaccinations :%{y} Date: %{x}</b><extra></extra>' },
                                    { 'x': self.data['vaccinations_agegroup_nl']['date'], 'y': self.data['vaccinations_agegroup_nl']['1976-1980'], 'type': 'line',  'marker': {'symbol': 'circle'}, 'line': {'color': '#515fe9', 'dash': 'solid'}, 'hovertemplate': '<b>Vaccinations: %{y} Date: %{x}</b><extra></extra>' },
                                    { 'x': self.data['vaccinations_agegroup_nl']['date'], 'y': self.data['vaccinations_agegroup_nl']['1981-1985'], 'type': 'line',  'marker': {'symbol': 'circle'}, 'line': {'color': '#4555e6', 'dash': 'solid'}, 'hovertemplate': '<b>Vaccinations: %{y} Date: %{x}</b><extra></extra>' },
                                    { 'x': self.data['vaccinations_agegroup_nl']['date'], 'y': self.data['vaccinations_agegroup_nl']['1986-1990'], 'type': 'line',  'marker': {'symbol': 'circle'}, 'line': {'color': '#394ae3', 'dash': 'solid'}, 'hovertemplate': '<b>Vaccinations: %{y} Date: %{x}</b><extra></extra>' },
                                    { 'x': self.data['vaccinations_agegroup_nl']['date'], 'y': self.data['vaccinations_agegroup_nl']['1991-1995'], 'type': 'line',  'marker': {'symbol': 'circle'}, 'line': {'color': '#2a3fdf', 'dash': 'solid'}, 'hovertemplate': '<b>Vaccinations: %{y} Date: %{x}</b><extra></extra>' },
                                    { 'x': self.data['vaccinations_agegroup_nl']['date'], 'y': self.data['vaccinations_agegroup_nl']['2004-2009'], 'type': 'line',  'marker': {'symbol': 'circle'}, 'line': {'color': '#293fdf', 'dash': 'solid'}, 'hovertemplate': '<b>Vaccinations: %{y} Date: %{x}</b><extra></extra>' },
                                    { 'x': self.data['vaccinations_agegroup_nl']['date'], 'y': self.data['vaccinations_agegroup_nl']['1996-2003'], 'type': 'line',  'marker': {'symbol': 'circle'}, 'line': {'color': '#1634db', 'dash': 'solid'}, 'hovertemplate': '<b>Vaccinations: %{y} Date: %{x} </b><extra></extra>' }
                                ],
                                'layout': {
                                    'plot_bgcolor': 'rgba(255, 255, 255, 0)',
                                    'margin': { 'b': 0, 't': 0, 'r': 0, 'l': 0 },
                                    'hoverlabel': {
                                        'bordercolor': 'rgb(229 229 229)',
                                        'bgcolor': 'white',
                                        'font': {
                                            'color': 'black'
                                        }
                                    },
                                    'xaxis': {'title': {'text': 'date'}},
                                    'yaxis': {'title': {'text': 'vaccination level'}}
                                },
                            },
                            config={ 'staticPlot': False })
                        ),
            ]
        )]
