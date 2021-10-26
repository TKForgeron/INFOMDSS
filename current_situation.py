from dash import html

class CurrentSituation:
    def __init__(self):
        False

    def get_html(self):
        return [
            html.Div(
                className="container",
                children=[
                    html.Div(
                        className="titleBar",
                        children=[
                            html.H3('Current Situation'),
                            html.Hr()
                        ]
            )]
        )]