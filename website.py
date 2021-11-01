import dash
from header import Header
from current_situation import CurrentSituation
from dash import dcc
from dash import html
import sys
from data_importer import Data_Importer


class Website:
    def __init__(self, args: list):
        self.html = None
        no_cache = False
        if ('-oc' in args or '--overwrite-cache' in args):
            no_cache = True
        self.data = Data_Importer(no_cache=no_cache).get_data()
        self.get_html()
        self.run_website(html)


    def get_html(self):
        allHtml = []
        allHtml = allHtml + Header().get_html() + CurrentSituation(self.data).get_html()
        self.html = html.Div(
            className="pageContainer",
            children=allHtml
        )

    def run_website(self, allHtml):
        app = dash.Dash(__name__)
        app.layout = html.Div(children=self.html)
        app.run_server(debug=True)