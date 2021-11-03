from os import sep
import dash
from dash import dcc
from dash import html
import plotly.express as px
import pandas as pd
import numpy as np
from dash.dependencies import Input, Output
from datetime import datetime, timedelta
import helpers
from website_component import Website_Component
import math

USE_DATA = [
    'cases_nl',
    'cases_nsw',
    'cases_il',
    'measures',
    'temperature_nl',
    'temperature_nsw',
    'temperature_il'
]

class Cases_Overview(Website_Component):
    def __init__(self, data, app):
        self.store_required_data(data, USE_DATA)
        self.app = app
        self.traces = {}

        self.keys = [
            
            { 'key_name': 'C1_School closing', 'value_range': [0, 3], 'steps': None, 'colors': 'norm', 'label': 'Schools closing', 'descr': ''' 	0 - no measures
1 - recommend closing or all schools open with alterations resulting in significant differences compared to non-Covid-19 operations
2 - require closing (only some levels or categories, eg just high school, or just public schools)
3 - require closing all levels
Blank - no data ''', 'data_type': 'measures' },
{ 'key_name': 'C2_Workplace closing', 'value_range': [0, 3], 'steps': None, 'colors': 'norm', 'label': 'Workplace closing', 'descr': ''' 	0 - no measures
1 - recommend closing (or recommend work from home) or all businesses open with alterations resulting in significant differences compared to non-Covid-19 operation
2 - require closing (or work from home) for some sectors or categories of workers
3 - require closing (or work from home) for all-but-essential workplaces (eg grocery stores, doctors)
Blank - no data ''', 'data_type': 'measures' },
{ 'key_name': 'C3_Cancel public events', 'value_range': [0, 2], 'steps': None, 'colors': 'norm', 'label': 'Cancel public events closing', 'descr': ''' 	0 - no measures
1 - recommend cancelling
2 - require cancelling ''', 'data_type': 'measures' },
{ 'key_name': 'StringencyIndex', 'value_range': [0, 100], 'steps': 5, 'colors': 'norm', 'label': 'Measures', 'descr': ''' 	0 - no measures
1 - recommend closing or all schools open with alterations resulting in significant differences compared to non-Covid-19 operations
2 - require closing (only some levels or categories, eg just high school, or just public schools)
3 - require closing all levels
Blank - no data ''', 'legend_items': ['0 - 20', '20 - 40', '40 - 60', '60 - 80', '80 - 100'], 'data_type': 'measures' },
{ 'key_name': 'temp', 'bins': [-np.inf, 0, 10, 20, 30, np.inf], 'colors': 'norm', 'label': 'Temperature', 'descr': ''' ''', 'legend_items': ['< 0', '0 - 10', '10 - 20', '20 - 30', '30+'], 'data_type': 'temperature' },
        ]
        self.preprocess_keys()
        self.dfs, self.colors, self.colors_list = self.create_dfs()

        # self.df_measures_strictness = self.create_cases_measures_df()
        # self.df_measures_strictness_colors = self.get_colors_pallete(self.df_measures_strictness, 'strictness', 5)
        # self.df_temperature = self.create_cases_temperature_df()
        # self.df_temperature_colors = self.get_colors_pallete(self.df_temperature, 'temp_cat', 5)
        # app.callback(Output('ov_cases_graph', 'figure'), Input('dropdown', 'value'))(self.on_dropdown_change)

    def preprocess_keys(self):
        self.keys = list(map(self.preporcess_key, self.keys))

    def preporcess_key(self, key: dict) -> dict:
        if not 'legend_items' in key:
            key['legend_items'] = list(map(lambda l: l.split('- ')[1], key['descr'].split('\n')))
        return key

    def create_dfs(self):
        ## ADD Measures
        dfs = {}
        color_palletes = {}
        color_lists = {}
        countries = [
            { 'CountryCode': 'NLD', 'data_name': 'cases_nl', 'key': 'nl'}, 
            { 'CountryCode': 'ISR', 'data_name': 'cases_il', 'key': 'il'},
            { 'CountryCode': 'AUS', 'data_name': 'cases_nsw', 'key': 'nsw'}
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
        # return []
        return [
            { 'output': [Output('ov_cases_graph', 'figure'), Output('ov_cases_graph_il', 'figure'), Output('ov_cases_graph_nsw', 'figure'), Output('co_ledgend', 'children')], 'input': Input('dropdown', 'value'), 'funct': self.on_dropdown_change}
        ]

    def create_ledgend(self, legend_items: str, colors: list ):
        html_items = []
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
        fig = px.line(self.dfs['nl'], x="date", y="cases", color="C1_School closing_seq", color_discrete_sequence=self.colors['nl']['C1_School closing'], hover_data=['C1_School closing_hd'])
        fig.update_layout(showlegend=False)
        # fig = px.line(self.dfs, x="date", y="cases", color="seq", color_discrete_sequence=self.df_measures_strictness_colors)
        # fig = px.line(self.df_temperature, x="date", y="cases", color="seq", color_discrete_sequence=self.df_temperature_colors, hover_data=['temp'])

        fig_il = px.line(self.dfs['il'], x="date", y="cases", color="C1_School closing_seq", color_discrete_sequence=self.colors['il']['C1_School closing'], hover_data=['C1_School closing_hd'])
        fig_il.update_layout(showlegend=False)

        fig_nsw = px.line(self.dfs['nsw'], x="date", y="cases", color="C1_School closing_seq", color_discrete_sequence=self.colors['nsw']['C1_School closing'], hover_data=['C1_School closing_hd'])
        fig_nsw.update_layout(showlegend=False)
        dropdown_options = self.get_dropdown_options()
        return [
            html.Div(
                className="container",
                children=[
                    html.Div(
                        className="titleBar",
                        children=[
                            html.H3('Cases overview'),
                            html.Hr()
                        ]),
                    dcc.Dropdown(id='dropdown', options=dropdown_options,
                    value=dropdown_options[0]['value']),
                    dcc.Graph(id="ov_cases_graph", figure=fig),
                    html.Div(
                        id="co_ledgend",
                        className="ledgend",
                        children=
                           self.create_ledgend(self.keys[0]['legend_items'], self.colors_list['nl'][self.keys[0]['key_name']])
 
                    ),
                    html.Div(
                        className="ov_cases_splitted",
                        children=[
                            html.Div(
                                className="ov_cases_splitted_graph",
                                children=[dcc.Graph(id="ov_cases_graph_il", figure=fig_il)]
                            ),
                            html.Div(
                                className="ov_cases_splitted_graph",
                                children=[dcc.Graph(id="ov_cases_graph_nsw", figure=fig_nsw)]
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
        # merged.loc[merged['keep'] == True, ['date']] = pd.DatetimeIndex(merged[merged['keep'] == True]['date']) + pd.DateOffset(1)
        # merged.loc[merged['keep'] == True, [seq_name]] = merged[merged['keep'] == True][seq_name] + 1
        df["date"] = pd.to_datetime(df["date"])
        return df
    
    def create_cases_measures_df(self) -> pd.DataFrame:
        cases = self.data['cases_nl']
        measures = self.data['measures']
        measures = measures[measures['CountryCode'] == 'NLD']
        merged = pd.merge(cases, measures, left_on='date', right_on='date', how='left')
        merged = merged.rename(columns={ 'cases_x': 'cases' })
        merged = merged[['date', 'StringencyIndex', 'cases']]
        merged['strictness'] = np.floor(merged['StringencyIndex'] / 100 * 5)

        merged = self.create_seq(merged, 'strictness', 'measure_seq')

        return merged

    def create_cases_temperature_df(self) -> pd.DataFrame:
        cases = self.data['cases_nl']
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
        start_color = np.array([47, 47, 255])
        end_color = np.array([247, 0, 0])
        
        vector = end_color - start_color

        color_pallete = []

        for n in range(0, levels):
            color = start_color + (n / (levels - 1) * vector).astype(int)
            color_pallete.append('#%02x%02x%02x' % (color[0], color[1], color[2]))


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

    def on_dropdown_change(self, value):
        fig = px.line(self.dfs['nl'], x="date", y="cases", color=value + "_seq", color_discrete_sequence=self.colors['nl'][value], hover_data=[value + '_hd'])
        fig.update_layout(showlegend=False)

        fig_il = px.line(self.dfs['il'], x="date", y="cases", color=value + "_seq", color_discrete_sequence=self.colors['il'][value], hover_data=[value + '_hd'])
        fig_il.update_layout(showlegend=False)
        # print(self.colors['il'])


        fig_nsw = px.line(self.dfs['nsw'], x="date", y="cases", color=value + "_seq", color_discrete_sequence=self.colors['nsw'][value], hover_data=[value + '_hd'])
        fig_nsw.update_layout(showlegend=False)
        # if value == 'temp':
        # elif value == 'none':
        #     fig = px.line(self.data['cases_nl'], x="date", y="cases")
        # else:
        #     fig = px.line(self.df_measures_strictness, x="date", y="cases", color="seq", color_discrete_sequence=self.df_measures_strictness_colors)
        key = find_in_list(self.keys, lambda i: i['key_name'] == value)
        return fig, fig_il, fig_nsw, self.create_ledgend(key['legend_items'], self.colors_list['nl'][value])

def find_in_list(list: list, function):
    for item in list:
        if (function(item)): return item