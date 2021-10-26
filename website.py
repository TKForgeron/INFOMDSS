import dash
from header import Header
from current_situation import CurrentSituation
from dash import dcc
from dash import html

class Website:
    def __init__(self):
        self.html = None
        self.get_html()
        self.run_website(html)

    def get_html(self):
        allHtml = []
        allHtml = allHtml + Header().get_html() + CurrentSituation().get_html()
        self.html = html.Div(
            className="pageContainer",
            children=allHtml
        )

    def run_website(self, allHtml):
        app = dash.Dash(__name__)
        app.layout = html.Div(children=self.html)
        app.run_server(debug=True)

