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


USE_DATA = [
    'cases_nl',
    'measures',
    'temperature_nl'
]

class Cases_Overview(Website_Component):
    def __init__(self, data, app):
        self.store_required_data(data, USE_DATA)
        self.app = app
        self.df_measures_strictness = self.create_cases_measures_df()
        self.df_measures_strictness_colors = self.get_colors_pallete(self.df_measures_strictness, 'strictness', 5)
        self.df_temperature = self.create_cases_temperature_df()
        self.df_temperature_colors = self.get_colors_pallete(self.df_temperature, 'temp_cat', 5)
        # app.callback(Output('ov_cases_graph', 'figure'), [Input('dropdown', 'value')])(self.on_dropdown_change)

    def get_html(self):
        # print('000')
        print(self.df_measures_strictness_colors)
        # fig = px.line(self.df_measures_strictness, x="date", y="cases", color="seq", color_discrete_sequence=self.df_measures_strictness_colors)
        fig = px.line(self.df_temperature, x="date", y="cases", color="seq", color_discrete_sequence=self.df_temperature_colors, hover_data=['temp'])
        return [
            html.Div(
                className="container",
                children=[
                    # dcc.Dropdown(id='dropdown', options=[
                    # {'label': 'A', 'value': 'A'},
                    # {'label': 'B', 'value': 'B'}],
                    # value = 'A'),
                    dcc.Graph(id="ov_cases_graph", figure=fig)

            ]
        )]

    def create_seq(self, df, col: str):
        bu_df = df.copy()
        bu_df['seq'] = np.nan
        df['seq'] = (df[col] != df[col].shift(1)).cumsum()
        # print(bu_merged)

        df = df.append(bu_df, ignore_index=True)
        df = df.sort_values(['date', 'seq'])
        df['keep'] = (df['seq'].isna()) & (df[col].shift(-1) != df[col].shift(1))
        # print(merged[merged['keep'] == True])
        # print(merged[merged['seq'].isna()])
        df = df[(~df['seq'].isna()) | ((df['seq'].isna()) & (df['keep'] == True))]
        # print(len(merged[merged['seq'].isna()]))
        df['seq'] = df['seq'].fillna(method='bfill')
        df['seq'] = df['seq'].fillna(method='ffill')
        # merged.loc[merged['keep'] == True, ['date']] = pd.DatetimeIndex(merged[merged['keep'] == True]['date']) + pd.DateOffset(1)
        # merged.loc[merged['keep'] == True, ['seq']] = merged[merged['keep'] == True]['seq'] + 1
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
        # print(merged.groupby('strictness').first()['date'])
        merged = self.create_seq(merged, 'strictness')
        # print(merged[merged.duplicated(subset=['date'], keep=False)])
        # print(merged)
        return merged

    def create_cases_temperature_df(self) -> pd.DataFrame:
        cases = self.data['cases_nl']
        measures = self.data['temperature_nl']

        merged = pd.merge(cases, measures, left_on='date', right_on='date', how='left')

        bins = [-np.inf, 0, 10, 20, 30, np.inf]
        names = [1, 2, 3, 4, 5]
        
        merged['temp_cat'] = pd.cut(merged['temp'], bins, labels=names)

        merged = self.create_seq(merged, 'temp_cat')
        return merged

    def get_colors_pallete(self, df: pd.DataFrame, col: str, levels: int) -> list:
        # this funciton assumes one col to be available named seq

        start_color = np.array([47, 47, 255])
        end_color = np.array([247, 0, 0])
        
        vector = end_color - start_color

        color_pallete = []

        for n in range(0, levels):
            color_pallete.append((start_color + (n / (levels - 1) * vector)).astype(int))

        # print(color_pallete)
        seq = 1
        pallete = []
        df = df.sort_values(['date', 'seq'], ascending=(True, False))
        while True:
            filtered = df[df['seq'] == seq]
            if (len(filtered) == 0): break
            level = filtered[col].tail(1).values[0]
            color = color_pallete[int(level)] # in rgb as np.array
            # print(filtered.tail(1))
            # print(int(level))
            pallete.append('#%02x%02x%02x' % (color[0], color[1], color[2])) # to hex
            seq += 1
        return pallete

    def on_dropdown_change(self, value):
        print(value)

