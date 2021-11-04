import numpy as np
from dash import html

meaure_description = ['''
    The current measures is overlaid on the graph is based on data tracked by the''', html.A('Oxford Covid-19 Government Response Tracker', href="https://github.com/OxCGRT/covid-policy-tracker"),]

strictness_description = ['''
The stringency index ranges between 0 - 100 and indicates the combined strictness of the measures in a country. The higher the index value, the more stricter the measures. This stringency index is calculated by taking a weighted average of the following measures: School closing, Workplace closing, cancel public events, restrictions on gatherings, close public transport, stay at home requirements, restrictions on internal movement, international travel controls, and testing policy. This stringency index is provided by the
''', html.A('Oxford Covid-19 Government Response Tracker', href="https://github.com/OxCGRT/covid-policy-tracker"), ' project']

temp_description = ['''
    Overlaid on the graph is the average temperature for each day.
''']

keys = [
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
    {
    'key_name': 'C1_School closing',
    'value_range': [0, 3],
    'steps': None,
    'colors': 'norm',
    'label': 'Schools closing',
    'labels_desc':
    ''' 0 - no measures
        1 - recommend closing or all schools open with alterations resulting in significant differences compared to non-Covid-19 operations
        2 - require closing (only some levels or categories, eg just high school, or just public schools)
        3 - require closing all levels
        Blank - no data  ''',
    'data_type': 'measures',
    'description': meaure_description
    },
    {
        'key_name': 'C2_Workplace closing',
        'value_range': [0, 3],
        'steps': None, 'colors': 'norm',
        'label': 'Workplace closing',
        'labels_desc':
            ''' 0 - no measures
                1 - recommend closing (or recommend work from home) or all businesses open with alterations resulting in significant differences compared to non-Covid-19 operation
                2 - require closing (or work from home) for some sectors or categories of workers
                3 - require closing (or work from home) for all-but-essential workplaces (eg grocery stores, doctors)
                Blank - no data ''',
        'data_type': 'measures',
        'description': meaure_description
    },
    {
        'key_name': 'C3_Cancel public events',
        'value_range': [0, 2], 'steps': None,
        'colors': 'norm',
        'label': 'Cancel public events closing',
        'labels_desc':
            '''0 - no measures
               1 - recommend cancelling
               2 - require cancelling ''',
        'data_type': 'measures',
        'description': meaure_description
    },
    {
        'key_name': 'C4_Restrictions on gatherings',
        'value_range': [0, 4], 'steps': None,
        'colors': 'norm',
        'label': 'Cancel public events closing',
        'labels_desc':
            '''	0 - no restrictions
                1 - restrictions on very large gatherings (the limit is above 1000 people)
                2 - restrictions on gatherings between 101-1000 people
                3 - restrictions on gatherings between 11-100 people
                4 - restrictions on gatherings of 10 people or less
                Blank - no data''',
        'data_type': 'measures',
        'description': meaure_description
    },
    {
        'key_name': 'C5_Close public transport',
        'value_range': [0, 2], 'steps': None,
        'colors': 'norm',
        'label': 'Close public transport',
        'labels_desc':
            '''	0 - no measures
                1 - recommend closing (or significantly reduce volume/route/means of transport available)
                2 - require closing (or prohibit most citizens from using it)
                Blank - no data''',
        'data_type': 'measures',
        'description': meaure_description
    },
    {
        'key_name': 'C6_Stay at home requirements',
        'value_range': [0, 3], 'steps': None,
        'colors': 'norm',
        'label': 'Stay at home requirements',
        'labels_desc':
            '''0 - no measures
                1 - recommend not leaving house
                2 - require not leaving house with exceptions for daily exercise, grocery shopping, and 'essential' trips
                3 - require not leaving house with minimal exceptions (eg allowed to leave once a week, or only one person can leave at a time, etc)
                Blank - no data''',
        'data_type': 'measures',
        'description': meaure_description
    },
    {
        'key_name': 'C7_Restrictions on internal movement',
        'value_range': [0, 2], 'steps': None,
        'colors': 'norm',
        'label': 'Restrictions on internal movement',
        'labels_desc':
            '''0 - no measures
                1 - recommend not to travel between regions/cities
                2 - internal movement restrictions in place
                Blank - no data''',
        'data_type': 'measures',
        'description': meaure_description
    },
    {
        'key_name': 'C8_International travel controls',
        'value_range': [0, 4], 'steps': None,
        'colors': 'norm',
        'label': 'International travel controls',
        'labels_desc':
            '''0 - no restrictions
                1 - screening arrivals
                2 - quarantine arrivals from some or all regions
                3 - ban arrivals from some regions
                4 - ban on all regions or total border closure
                Blank - no data''',
        'data_type': 'measures',
        'description': meaure_description
    },
    {
        'key_name': 'H7_Vaccination policy',
        'value_range': [0, 5], 'steps': None,
        'colors': 'norm',
        'label': 'Vaccination policy',
        'labels_desc':
            '''0 - No availability
                1 - Availability for ONE of following: key workers/ clinically vulnerable groups (non elderly) / elderly groups
                2 - Availability for TWO of following: key workers/ clinically vulnerable groups (non elderly) / elderly groups
                3 - Availability for ALL of following: key workers/ clinically vulnerable groups (non elderly) / elderly groups
                4 - Availability for all three plus partial additional availability (select broad groups/ages)
                5 - Universal availability''',
        'data_type': 'measures',
        'description': meaure_description
    },
    {
        'key_name': 'H8_Protection of elderly people',
        'value_range': [0, 5], 'steps': None,
        'colors': 'norm',
        'label': 'Protection of elderly people',
        'labels_desc':
            '''0 - No availability
                1 - Availability for ONE of following: key workers/ clinically vulnerable groups (non elderly) / elderly groups
                2 - Availability for TWO of following: key workers/ clinically vulnerable groups (non elderly) / elderly groups
                3 - Availability for ALL of following: key workers/ clinically vulnerable groups (non elderly) / elderly groups
                4 - Availability for all three plus partial additional availability (select broad groups/ages)
                5 - Universal availability''',
        'data_type': 'measures',
        'description': meaure_description
    },
    {
        'key_name': 'H6_Facial Coverings',
        'value_range': [0, 4], 'steps': None,
        'colors': 'norm',
        'label': 'Protection of elderly people',
        'labels_desc':
            '''0 - No policy
            1 - Recommended
            2 - Required in some specified shared/public spaces outside the home with other people present, or some situations when social distancing not possible
            3 - Required in all shared/public spaces outside the home with other people present or all situations when social distancing not possible
            4 - Required outside the home at all times regardless of location or presence of other people''',
        'data_type': 'measures',
        'description': meaure_description
    },
    {
        'key_name': 'H3_Contact tracing',
        'value_range': [0, 2], 'steps': None,
        'colors': 'norm',
        'label': 'Contact tracing',
        'labels_desc':
            '''0 - no contact tracing
                1 - limited contact tracing; not done for all cases
                2 - comprehensive contact tracing; done for all identified cases''',
        'data_type': 'measures',
        'description': meaure_description
    },
    {
        'key_name': 'H2_Testing policy',
        'value_range': [0, 3], 'steps': None,
        'colors': 'norm',
        'label': 'Testing Policy',
        'labels_desc':
            '''0 - no testing policy
                1 - only those who both (a) have symptoms AND (b) meet specific criteria (eg key workers, admitted to hospital, came into contact with a known case, returned from overseas)
                2 - testing of anyone showing Covid-19 symptoms
                3 - open public testing (eg "drive through" testing available to asymptomatic people)
                Blank - no data''',
        'data_type': 'measures',
        'description': meaure_description
    },
    {
        'key_name': 'H1_Public information campaigns',
        'value_range': [0, 2], 'steps': None,
        'colors': 'norm',
        'label': 'Public information campaigns',
        'labels_desc':
            '''	0 - no Covid-19 public information campaign
                1 - public officials urging caution about Covid-19
                2- coordinated public information campaign (eg across traditional and social media)
                Blank - no data''',
        'data_type': 'measures',
        'description': meaure_description
    },
]