from os import sep
from dash import dcc
from dash import html
import plotly.express as px
import pandas as pd
import numpy as np
import colors
from dash.dependencies import Input, Output
from website_component import Website_Component
import math
import cases_overview_config as config

USE_DATA = [
    'hospitalizations_nl',
    'measures',
    'temperature_nl'
] # Defines wich df to load for this component

class Hospitalizations_Overview(Website_Component):
    def __init__(self, data):
        self.store_required_data(data, USE_DATA)
        self.traces = {}
        self.keys = config.keys # The Keys config has data on what keys to use for overaying data on the graphs 
        self.preprocess_keys() # process the keys described above
        self.dfs, self.colors, self.colors_list = self.create_dfs()


    def preprocess_keys(self):
        self.keys = list(map(self.preporcess_key, self.keys))

    def preporcess_key(self, key: dict) -> dict:
        """
            Convert the legend_items text field to an array that is used to make a nice legend.
        """
        if not 'legend_items' in key:
            key['legend_items'] = list(map(lambda l: l.split('- ')[1], key['labels_desc'].split('\n')))
        return key

    def create_dfs(self):
        """
            This function prepares the dataframes according to the configuration imported in the __init__() function.
            Changing the countries array you can add extra countries if the data is available in the self.data dict
            For each key the data is processes. If 'bins' is provided in the dict it converts the data to the corresponding bins
            if 'steps' is povided it will devided the value in to a certain number of levels difined in 'steps'. If not it will just assume
            values are integers between the data provided in 'value_range'

            The graph(s) overlay a certain variable, where which is implemented as follows: Each color change is a new line, so not all the same colors are the same line
            when the overlaid variable changes it is a new line indicated by the (key + _seq) column in the dataframe. We need to override the colors plotly wants to assign them.
            The function therefore returns color_palletes which is a list for all different valies that _seq can take and has the colors corresponding the the original level.

            Added columns for each key to the dataframe:
            (1) key + _seq: Is the sequence number that increases everytime that value changes
            (2) key: This column might be altered if requested by the config (e.g. converting it to bins or steps)
            (3) key + '_hd': Is the data also shown when hovering the graph and is the original value of the metric.

            It returns three variables.
            (1) The dataframes for each country each with all the keys in the config
            (2) The color pallete containing a list with a color for each sequencie
            (3) The unqiue colors in the graph (ordered)
        """
        dfs = {}
        color_palletes = {}
        color_lists = {}
        countries = [
            { 'CountryCode': 'NLD', 'data_name': 'hospitalizations_nl', 'key': 'nl'}, 
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
        """
            used by Website() to get callbacks
        """
        return [
            { 'output': [Output('ho_hospitalizations_graph', 'figure'), Output('ho_ledgend', 'children'),  Output('ho_description', 'children')], 'input': Input('ho_dropdown', 'value'), 'funct': self.on_dropdown_change}
        ]

    def create_ledgend(self, legend_items: str, colors: list ):
        """
            Creates a HTML ledgend based on legend_items, and colors.
        """
        html_items = [html.H5('Legend') ]
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
        """
            Creates the HTML for this element
        """
        fig = px.line(self.dfs['nl'], x="date", y="hospitalizations", color="C1_School closing_seq", color_discrete_sequence=self.colors['nl']['C1_School closing'], hover_data=['C1_School closing_hd'])
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
                            html.H3('Hospitalisations'),
                            html.Hr()
                        ]),
                    html.Div(
                        className="dropdownLabel",
                        children="Select variable to overlay on graphs:"
                    ),
                    dcc.Dropdown(id='ho_dropdown', options=dropdown_options,
                    value=dropdown_options[0]['value']),
                    html.Div(
                        className="co_main",
                        children=[
                            html.H4('The Netherlands'),
                            dcc.Graph(id="ho_hospitalizations_graph", className="co_main_graph", figure=fig),
                            html.Div(
                                className="co_main_descr",
                                children=[
                                    html.Div(
                                        id="ho_ledgend",
                                        className="co_ledgend",
                                        children=
                                        self.create_ledgend(self.keys[0]['legend_items'], self.colors_list['nl'][self.keys[0]['key_name']])
                                    ),
                                    html.Div(
                                        id="ho_description",
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
        """
            This function takes a DF and creates the column named 'seq_name' by looking at the value in column 'col'. If that value changes
            it increments this value. In order to ensure a conitues line when plotting the graph a row is diplicated once the seq changes
            and takes the value of the previous seq value. 

            Bc the plot relies on using different lines for all different sequences it doesn't link the lines if we don't duplicate certain values.
            (Since there is no line with values between the dates where the value changes)
        """
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
    
    def get_colors_pallete(self, df: pd.DataFrame, col: str, levels: int, seq_name: str) -> list:
        """
            This function takes a df and looks assigns a color to it based on the value of the col names 'col'.
            It does this by taking the last value of rows where col names 'seq_name' is of the sequence value.
            The sequence value starts at 1 and runs untill it can't find any rows with that sequence.
            The system furthermore creates the color pallete based on the color module. it uses the 'levels' argument for this
            'levels' is how about how many values the 'col' column can take.
        """
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
        """
            Styling
        """
        fig.update_layout(showlegend=False)
        fig.update_layout(margin=dict(r=20, t=0, l=20, b=20), paper_bgcolor='rgb(251, 251, 251)', plot_bgcolor='rgb(251, 251, 251)')
        fig.update_xaxes(gridcolor='rgb(217, 217, 217)')
        fig.update_yaxes(gridcolor='rgb(217, 217, 217)')


    def on_dropdown_change(self, value):
        """
            This function is called by dash everytime the dropdown changes. It plots the corresponding graph from the self.dfs value.
        """
        fig = px.line(self.dfs['nl'], x="date", y="hospitalizations", color=value + "_seq", color_discrete_sequence=self.colors['nl'][value], hover_data=[value + '_hd'])
        self.style_fig(fig)

        key = find_in_list(self.keys, lambda i: i['key_name'] == value)
        return fig, self.create_ledgend(key['legend_items'], self.colors_list['nl'][value]), [html.H5('Description')] + key['description']
def find_in_list(list: list, function):
    for item in list:
        if (function(item)): return item