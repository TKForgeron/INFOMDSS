# Libraries
import dash
from dash import html

# Website components:
from header import Header
from current_situation import CurrentSituation
from cases_overview import Cases_Overview
from hospitalizations_overview import Hospitalizations_Overview
from vaccinations_agegroup import Vaccinations_AgeGroup
from measure_strictness import Measure_Strictness
from vaccinations_overview import Vaccinations_Overview
from data_importer import Data_Importer


class Website:
    def __init__(self, args: list):
        self.print_launch()
        self.html = None
        no_cache = False
        if ('-oc' in args or '--overwrite-cache' in args):
            no_cache = True
        self.host = '0.0.0.0'
        self.debug = False
        if ('-dev' in args or '--debug' in args):
            self.ip = '127.0.0.1'
            self.debug = True
        self.data = Data_Importer(no_cache=no_cache).get_data() # Gets the dat
        self.get_html() # populates the self.html
        self.run_website()


    def get_html(self):
        # Also retrieves callbacks
        allHtml = []
        callbacks = []

        allHtml = allHtml + Header().get_html()

        allHtml = allHtml + CurrentSituation(self.data).get_html()

        allHtml = allHtml + Measure_Strictness(self.data).get_html()

        cases_overview = Cases_Overview(self.data)
        callbacks = callbacks + cases_overview.get_callbacks()
        allHtml = allHtml + cases_overview.get_html()

        hospitalization_overview = Hospitalizations_Overview(self.data)
        callbacks = callbacks + hospitalization_overview.get_callbacks()
        allHtml = allHtml + hospitalization_overview.get_html()

        vaccinations_overview = Vaccinations_Overview(self.data)
        callbacks = callbacks + vaccinations_overview.get_callbacks()
        allHtml = allHtml + vaccinations_overview.get_html()

        allHtml = allHtml + Vaccinations_AgeGroup(self.data).get_html()

        self.callbacks = callbacks
        
        self.html = html.Div(
            className="pageWrapper",
            children=[
                html.Div(
                    className="pageContainer",
                    children=allHtml
                ),
                html.Div(
                    className="pageContainer",
                    children=[
                        html.Div(
                            className="container projectdetails",
                            children=[
                                html.H2("About this Dashboard"),
                                html.P("This dashboard was developed as part of a project for Data Science & Society, | Master Business Informatics, Utrecht University."),
                                html.P("Arthur Zylinski (0872377), Tim Smit (6527906), Matthijs Blaauw (4925653)"),
                                html.P("Kouros Pechlivanidis (6527450), Max de Froe (4496655), Martijn Jansen (6457827)"),
                                html.P("For details and more information please visit the project report."),
                                html.Img(src="assets/images/uulogo.svg")
                            ]
                        )
                    ]
                )
            ]
        )

    def run_website(self):
        app = dash.Dash(__name__)
        for c in self.callbacks:
            app.callback(c['output'], c['input'])(c['funct'])
        app.layout = html.Div(children=self.html)
        app.title = 'DSS Dashboard'
        app.run_server(debug=self.debug, host=self.host)
    
    def print_launch(self):
        print('|------------------------------------------------|')
        print('| Data science & society project                 |')
        print('| COVID-19 Dashboard                             |')
        print('| Group 01                                       |')
        print('|------------------------------------------------|')
        print('')
        print('')
        print('Starting dashboard...')