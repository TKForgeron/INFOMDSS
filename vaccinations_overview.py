from os import sep
import dash
from dash import dcc
from dash import html
import plotly.express as px
import pandas as pd
import numpy as np
import colors
from dash.dependencies import Input, Output
from datetime import datetime, timedelta
import helpers
from website_component import Website_Component
import math
import vaccination_overview_config as config

USE_DATA = [
    'vaccinations_nl',
    'vaccinations_nsw',
    'vaccinations_il',
    'measures',
    'temperature_nl',
    'temperature_nsw',
    'temperature_il'
]

class Vaccinations_Overview(Website_Component):
    def __init__(self, data, app):
        self.store_required_data(data, USE_DATA)
        self.app = app
        self.traces = {}

        self.set_limmit_data_range()
        self.keys = config.keys
        self.preprocess_keys()
        self.dfs, self.colors, self.colors_list = self.create_dfs()

    def set_limmit_data_range(self):
        # limit range of IL and NSW
        days_to_show = 100
        start_date = datetime.today() - timedelta(days=days_to_show)
        self.data['vaccinations_il'] = self.data['vaccinations_il'][self.data['vaccinations_il']['date'] > start_date]
        self.data['vaccinations_nsw'] = self.data['vaccinations_nsw'][self.data['vaccinations_nsw']['date'] > start_date]

    def preprocess_keys(self):
        self.keys = list(map(self.preporcess_key, self.keys))

    def preporcess_key(self, key: dict) -> dict:
        if not 'legend_items' in key:
            key['legend_items'] = list(map(lambda l: l.split('- ')[1], key['labels_desc'].split('\n')))
        return key

    def create_dfs(self):
        dfs = {}
        color_palletes = {}
        color_lists = {}
        countries = [
            { 'CountryCode': 'NLD', 'data_name': 'vaccinations_nl', 'key': 'nl'}, 
        ]
        for country in countries:
            main_df = self.data[country['data_name']]
            main_df_bu = self.data[country['data_name']]
            colors_pallete = {}
            colors_list = {}
            for k in self.keys:
                new_data = None
                if k['data_type'] == 'measures':
                    new_data = self.data['measures']
                    new_data = new_data[new_data['CountryCode'] == country['CountryCode']]
                elif k['data_type'] == 'temperature':
                    new_data = self.data['temperature_' + country['key']]
                df = new_data[['date', k['key_name']]]

                df = pd.merge(main_df_bu[['date']], df, left_on='date', right_on='date', how='left')
                steps = None
                df[k['key_name'] + '_hd'] = df[k['key_name']] # hd = hover_Data
                if 'bins' in k and k['bins']:
                    bins = k['bins']
                    names = list(range(1, len(bins)))
                    steps = len(bins)
                    df[k['key_name']] = pd.cut(df[k['key_name']], bins, labels=names)
                elif 'steps' not in k or not k['steps']:
                    steps = k['value_range'][1] - k['value_range'][0] + 1
                else:
                    steps = k['steps']
                    df[k['key_name']] = np.floor((df[k['key_name']]  - k['value_range'][0]) / k['value_range'][1] * steps)
                

                df = self.create_seq(df.copy(), k['key_name'], k['key_name'] + '_seq')
                colors_pallete[k['key_name']], colors_list[k['key_name']]  = self.get_colors_pallete(df, k['key_name'], steps, k['key_name'] + '_seq')
                main_df = pd.merge(main_df, df, left_on='date', right_on='date', how='left')
            dfs[country['key']] = main_df
            color_palletes[country['key']] = colors_pallete
            color_lists[country['key']] = colors_list


        return dfs, color_palletes, color_lists

    def get_dropdown_options(self):
        return list(map(lambda k: { 'label': k['label'], 'value': k['key_name']}, self.keys))


    def get_callbacks(self):
        # used by Website() to get callbacks
        return [
            { 'output': [Output('vo_vaccinations_graph', 'figure'), Output('vo_ledgend', 'children'),  Output('vo_description', 'children')], 'input': Input('vo_dropdown', 'value'), 'funct': self.on_dropdown_change}
        ]

    def create_ledgend(self, legend_items: str, colors: list ):
        html_items = [html.H5('Ledgend') ]
        for i, c in enumerate(colors):
            label = 'None'
            if (i < len(legend_items)):
                label = legend_items[i]
            html_items.append(
                html.Div(
                    className="ledgend_item",
                    children=[
                        html.Div(
                            className="ledgend_color",
                            style={ 'backgroundColor': c }
                        ),
                        html.Div(
                            className="ledgend_label",
                            children=label
                        ),
                    ]
                )
            )
        return html_items

    def get_html(self):
        fig = px.line(self.dfs['nl'], x="date", y="vaccinations", color="H7_Vaccination policy_seq", color_discrete_sequence=self.colors['nl']['H7_Vaccination policy'], hover_data=['H7_Vaccination policy_hd'])
        fig.update_layout(showlegend=False, paper_bgcolor="#fff", plot_bgcolor="#ffffff")
        fig.update_xaxes(showgrid=False)
        fig.update_yaxes(showgrid=True, gridwidth=1, gridcolor='LightPink')

        dropdown_options = self.get_dropdown_options()
        return [
            html.Div(
                className="container co_container",
                children=[
                    html.Div(
                        className="titleBar",
                        children=[
                            html.H3('Vaccinations'),
                            html.Hr()
                        ]),
                    html.Div(
                        className="dropdownLabel",
                        children="Select variable to overlay on graphs:"
                    ),
                    dcc.Dropdown(id='vo_dropdown', options=dropdown_options,
                    value=dropdown_options[0]['value']),
                    html.Div(
                        className="co_main",
                        children=[
                            html.H4('The Netherlands'),
                            dcc.Graph(id="vo_vaccinations_graph", className="co_main_graph", figure=fig),
                            html.Div(
                                className="co_main_descr",
                                children=[
                                    html.Div(
                                        id="vo_ledgend",
                                        className="co_ledgend",
                                        children=
                                        self.create_ledgend(self.keys[0]['legend_items'], self.colors_list['nl'][self.keys[0]['key_name']])
                                    ),
                                    html.Div(
                                        id="vo_description",
                                        className="co_description",
                                        children=[html.H5('Description')] + self.keys[0]['description']
                                    )
                                ]
                            )
                        ]
                    
 
                    )
            ]
        )]

    def create_seq(self, df, col: str, seq_name: str):
        bu_df = df.copy()
        bu_df[seq_name] = np.nan
        df[seq_name] = (df[col] != df[col].shift(1)).cumsum()


        df = df.append(bu_df, ignore_index=True)
        df = df.sort_values(['date', seq_name])
        df['keep'] = (df[seq_name].isna()) & (df[col].shift(-1) != df[col].shift(1))

        df = df[(~df[seq_name].isna()) | ((df[seq_name].isna()) & (df['keep'] == True))]

        df[seq_name] = df[seq_name].fillna(method='bfill')
        df[seq_name] = df[seq_name].fillna(method='ffill')
        df = df.drop(['keep'], axis=1)

        df["date"] = pd.to_datetime(df["date"])
        return df
    
    def create_vaccinations_measures_df(self) -> pd.DataFrame:
        cases = self.data['vaccinations_nl']
        measures = self.data['measures']
        measures = measures[measures['CountryCode'] == 'NLD']
        merged = pd.merge(cases, measures, left_on='date', right_on='date', how='left')
        merged = merged.rename(columns={ 'vaccinations_x': 'cases' })
        merged = merged[['date', 'StringencyIndex', 'cases']]
        merged['strictness'] = np.floor(merged['StringencyIndex'] / 100 * 5)

        merged = self.create_seq(merged, 'strictness', 'measure_seq')

        return merged

    def create_vaccinations_temperature_df(self) -> pd.DataFrame:
        cases = self.data['vaccinations_nl']
        measures = self.data['temperature_nl']

        merged = pd.merge(cases, measures, left_on='date', right_on='date', how='left')

        bins = [-np.inf, 0, 10, 20, 30, np.inf]
        names = [1, 2, 3, 4, 5]
        
        merged['temp_cat'] = pd.cut(merged['temp'], bins, labels=names)

        merged = self.create_seq(merged, 'temp_cat', 'temp_seq')
        return merged

    def get_colors_pallete(self, df: pd.DataFrame, col: str, levels: int, seq_name: str) -> list:
        # this funciton assumes one col to be available named seq

        none_color = np.array([200, 200, 200])
        none_color = '#%02x%02x%02x' % (none_color[0], none_color[1], none_color[2])

        color_pallete = colors.create_color_list(levels)
        seq = 1
        pallete = []
        df = df.sort_values(['date', seq_name], ascending=(True, False))
        while True:
            filtered = df[df[seq_name] == seq]
            if (len(filtered) == 0): break
            level = filtered[col].tail(1).values[0]
            color = None
            if level == None or level == np.nan or math.isnan(level):
                color = none_color
            else:
                color = color_pallete[int(level)] # in rgb as np.array

            pallete.append(color) # to hex
            seq += 1

        return pallete, color_pallete

    def style_fig(self, fig):
        fig.update_layout(showlegend=False)
        fig.update_layout(margin=dict(r=20, t=0, l=20, b=20), paper_bgcolor='rgb(251, 251, 251)', plot_bgcolor='rgb(251, 251, 251)')
        fig.update_xaxes(gridcolor='rgb(217, 217, 217)')
        fig.update_yaxes(gridcolor='rgb(217, 217, 217)')


    def on_dropdown_change(self, value):
        fig = px.line(self.dfs['nl'], x="date", y="vaccinations", color=value + "_seq", color_discrete_sequence=self.colors['nl'][value], hover_data=[value + '_hd'])
        self.style_fig(fig)

        key = find_in_list(self.keys, lambda i: i['key_name'] == value)
        return fig, self.create_ledgend(key['legend_items'], self.colors_list['nl'][value]), [html.H5('Description')] + key['description']

def find_in_list(list: list, function):
    for item in list:
        if (function(item)): return item