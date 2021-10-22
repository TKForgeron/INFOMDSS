import dash
from header import Header
from dash import dcc
from dash import html


class Website:
    def __init__(self):
        html = self.get_html()
        self.run_website(html)

    def get_html(self):
        html = []
        html.append(Header.get_html())

    def run_website(self, allHtml):
        app = dash.Dash(__name__)
        app.layout = html.Div(children=allHtml)
        app.run_server(debug=True)

