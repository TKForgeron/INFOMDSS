import dash
from header import Header
from current_situation import CurrentSituation
from cases_overview import Cases_Overview
from dash import dcc
from dash import html
import sys
from data_importer import Data_Importer


class Website:
    def __init__(self, args: list):
        self.print_launch()
        self.html = None
        no_cache = False
        if ('-oc' in args or '--overwrite-cache' in args):
            no_cache = True
        self.data = Data_Importer(no_cache=no_cache).get_data()
        self.app = dash.Dash(__name__)
        self.get_html()
        self.run_website(html)


    def get_html(self):
        allHtml = []
        callbacks = []
        allHtml = allHtml + Header().get_html()
        allHtml = allHtml + CurrentSituation(self.data).get_html()
        cases_overview = Cases_Overview(self.data, self.app)
        callbacks = callbacks + cases_overview.get_callbacks()
        allHtml = allHtml + cases_overview.get_html()
        self.callbacks = callbacks
        self.html = html.Div(
            className="pageContainer",
            children=allHtml
        )

    def run_website(self, allHtml):
        for c in self.callbacks:
            self.app.callback(c['output'], c['input'])(c['funct'])
        self.app.layout = html.Div(children=self.html)
        self.app.run_server(debug=True)
    
    def print_launch(self):
        print('|------------------------------------------------|')
        print('| Data science & society project                 |')
        print('| COVID-19 Dashboard                             |')
        print('| Group 01                                       |')
        print('|------------------------------------------------|')
        print('')
        print('')
        print('Starting dashboard...')