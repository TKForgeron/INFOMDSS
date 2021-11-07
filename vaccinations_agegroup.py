from dash import dcc
from dash import html
from website_component import Website_Component

USE_DATA = [
    'vaccinations_agegroup_nl'
] # Defines wich df to load for this component

class Vaccinations_AgeGroup(Website_Component):
    def __init__(self, data):
        self.store_required_data(data, USE_DATA) # imports the data defined in USE_DATA

    def get_html(self):
        """
            Creates the HTML for this element
        """
        return [
            html.Div(
                className="container mb",
                children=[
                    html.Div(
                        className="co_main",
                        children= [
                            html.H4('Vaccinations Per Age Group'),
                            dcc.Graph(id="cs_per_age_graph", className="legendstyle",figure={
                            'data': self.agegroups_data(self),
                            'layout': {
                                'plot_bgcolor': 'rgb(251, 251, 251)',
                                'hoverlabel': {
                                    'bordercolor': 'rgb(229 229 229)',
                                    'bgcolor': 'white',
                                    'font': {
                                        'font-family': 'acumin-pro, sans-serif',
                                        'font-weight': '400',
                                        'color': 'black'
                                    }
                                },
                                'xaxis': {
                                    'title': {'text': 'date'}
                                },
                                'yaxis': {'title': {'text': 'vaccination level'}},
                                'legend': {
                                    'orientation': 'h',
                                    'yanchor': 'center',
                                    'y':'-0.3',
                                    'xanchor':'top',
                                    'x':'0'
                                }
                            },
                            },
                            config={ 'staticPlot': False })
                        ]
                    )
            ]
        )]
    
    def agegroups_data(self):
        """
            Creates the data attribute needed for the graph
        """
        age_groups_nl = list(self.data['vaccinations_agegroup_nl'])
        age_groups_nl.remove('date')
        colorgradient=['#c5ceff','#b9c2f7','#adb5ef','#a1a9e8','#959de0','#8991d8','#7e85d0','#7379c8','#686ebf','#5d62b7','#5257af','#464ca7','#3b419e','#2f3696','#212b8e','#0e2085']
        data = [ ]
        for (group,color) in zip(age_groups_nl, colorgradient):
            dict = { 'x': self.data['vaccinations_agegroup_nl']['date'], 'y': self.data['vaccinations_agegroup_nl'][group], 'name': group,'type': 'line',  'marker': {'symbol': 'circle'}, 'line': {'color': color, 'dash': 'solid'}, 'hovertemplate': '<b>Vaccinations: %{y} Date %{x}</b><extra></extra>', 'xaxis': 'x', 'yaxis': 'y', }
            data.append(dict)
        return data