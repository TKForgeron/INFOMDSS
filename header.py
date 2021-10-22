from dash import html


class Header:
    def get_html():
        return html.Div(
                children="""
            Dash: A web application framework for your data.
        """
            )
