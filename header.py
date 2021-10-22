from dash import html

class Header:
    def __init__(self):
        False

    def get_html(self):
        return [html.Div(
            className="appHeader",
            children=[
                    html.H1('Dashboard'),
                    html.H2('Project DSS')
                ]
        )]