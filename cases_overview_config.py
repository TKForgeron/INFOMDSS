import numpy as np

meaure_description = '''
    Hallo 
'''

strictness_description = '''
    Hallo 1223132123
'''

temp_description = '''
    Hallo aasdfasfd
'''

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
]