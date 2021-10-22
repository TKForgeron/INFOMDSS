from dash import html

class Header:
    def __init__(self):
        False

    def get_html(self):
        return [html.Div(
            children="""
        Dash: A web application framework for your data.
    """
        )]
