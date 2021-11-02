from os import sep
import dash
from dash import dcc
from dash import html
import plotly.express as px
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import helpers
from website_component import Website_Component


USE_DATA = [
    'cases_nl',
    'measures'
]

class Cases_Overview(Website_Component):
    def __init__(self, data):
        self.store_required_data(data, USE_DATA)
        self.df = self.create_cases_measures_df()
        self.df_colors = self.get_colors_pallete(self.df, 'strictness', 5)

    def get_html(self):
        print('000')
        print(self.df_colors)
        fig = px.line(self.df, x="date", y="cases", color="seq", color_discrete_sequence=self.df_colors)
        return [
            html.Div(
                className="container",
                children=[
                    dcc.Graph(id="ov_cases_graph", figure=fig)

            ]
        )]

    def create_cases_measures_df(self) -> pd.DataFrame:
        cases = self.data['cases_nl']
        measures = self.data['measures']
        measures = measures[measures['CountryCode'] == 'NLD']
        merged = pd.merge(cases, measures, left_on='date', right_on='date', how='left')
        merged = merged.rename(columns={ 'cases_x': 'cases' })
        merged = merged[['date', 'StringencyIndex', 'cases']]
        merged['strictness'] = np.floor(merged['StringencyIndex'] / 100 * 5)
        # print(merged.groupby('strictness').first()['date'])
        bu_merged = merged.copy()
        bu_merged['seq'] = np.nan
        merged['seq'] = (merged['strictness'] != merged['strictness'].shift(1)).cumsum()
        # print(bu_merged)

        merged = merged.append(bu_merged, ignore_index=True)
        merged = merged.sort_values(['date', 'seq'])
        merged['keep'] = (merged['seq'].isna()) & (merged['strictness'].shift(-1) != merged['strictness'].shift(1))
        # print(merged[merged['keep'] == True])
        # print(merged[merged['seq'].isna()])
        merged = merged[(~merged['seq'].isna()) | ((merged['seq'].isna()) & (merged['keep'] == True))]
        # print(len(merged[merged['seq'].isna()]))
        merged['seq'] = merged['seq'].fillna(method='bfill')
        merged['seq'] = merged['seq'].fillna(method='ffill')
        # merged.loc[merged['keep'] == True, ['date']] = pd.DatetimeIndex(merged[merged['keep'] == True]['date']) + pd.DateOffset(1)
        # merged.loc[merged['keep'] == True, ['seq']] = merged[merged['keep'] == True]['seq'] + 1
        merged["date"] = pd.to_datetime(merged["date"])
        print(merged[merged.duplicated(subset=['date'], keep=False)])
        merged = merged.sort_values(['date', 'seq'], ascending=(True, False))
        merged.to_csv('test.csv')
        # print(merged)
        return merged

    def get_colors_pallete(self, df: pd.DataFrame, col: str, levels: int) -> list:
        # this funciton assumes one col to be available named seq

        start_color = np.array([0, 255, 0])
        end_color = np.array([255, 0, 0])
        
        vector = end_color - start_color

        color_pallete = []

        for n in range(0, levels):
            color_pallete.append((start_color + (n / (levels - 1) * vector)).astype(int))

        print(color_pallete)
        seq = 1
        pallete = []
        while True:
            filtered = df[df['seq'] == seq]
            if (len(filtered) == 0): break
            level = filtered[col].tail(1).values[0]
            color = color_pallete[int(level)] # in rgb as np.array
            print(filtered.tail(1))
            print(int(level))
            pallete.append('#%02x%02x%02x' % (color[0], color[1], color[2])) # to hex
            seq += 1
        return pallete