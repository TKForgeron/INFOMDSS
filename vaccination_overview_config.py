import numpy as np
from dash import html

meaure_description = ['''
    The current policy which is overlaid on the graph is based on data tracked by the ''', html.A('Oxford Covid-19 Government Response Tracker', href="https://github.com/OxCGRT/covid-policy-tracker"),]

strictness_description = ['''
The stringency index ranges between 0 - 100 and indicates the combined strictness of the measures in a country. The higher the index value, the more stricter the measures. This stringency index is provided by the 
''', html.A('Oxford Covid-19 Government Response Tracker', href="https://github.com/OxCGRT/covid-policy-tracker"), ' project']

temp_description = ['''
    Overlaid on the graph is the average temperature for each day.
''']

keys = [
    {
    'key_name': 'H7_Vaccination policy',
    'value_range': [0, 5],
    'steps': None,
    'colors': 'norm',
    'label': 'Vaccination policy',
    'labels_desc':
        ''' 0 - No availability
            1 - Availability for ONE of following: key workers/ clinically vulnerable groups (non elderly) / elderly groups
            2 - Availability for TWO of following: key workers/ clinically vulnerable groups (non elderly) / elderly groups
            3 - Availability for ALL of following: key workers/ clinically vulnerable groups (non elderly) / elderly groups
            4 - Availability for all three plus partial additional availability (select broad groups/ages)
            5 - Universal availability ''',
    'data_type': 'measures',
    'description': meaure_description
    },
    {
        'key_name': 'StringencyIndex',
        'value_range': [0, 100],
        'steps': 5,
        'colors': 'norm',
        'label': 'Strictness measures',
        'labels_desc':
            ''' 0 - no measures
                1 - recommend closing or all schools open with alterations resulting in significant differences compared to non-Covid-19 operations
                2 - require closing (only some levels or categories, eg just high school, or just public schools)
                3 - require closing all levels
                Blank - no data''',
        'legend_items':
            [
                '0 - 20',
                '20 - 40',
                '40 - 60',
                '60 - 80',
                '80 - 100'
            ],
        'data_type': 'measures',
        'description': strictness_description
    },
    {
        'key_name': 'temp',
        'bins': [-np.inf, 0, 10, 20, 30, np.inf],
        'colors': 'norm',
        'label': 'Temperature',
        'labels_desc':
            ''' ''',
        'legend_items': ['< 0', '0 - 10', '10 - 20', '20 - 30', '30+'],
        'data_type': 'temperature',
        'description': temp_description
    },
    
]