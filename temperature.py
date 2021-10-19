import pandas as pd
import requests
from datetime import datetime
import json
from io import BytesIO

def get_temperature_df_il() -> pd.DataFrame:
    pass

def get_temperature_df_nl() -> pd.DataFrame:

    """

    Function that consumes the KNMI api to get the most recent weather data. In case an error occurs while making the API requests,
    fall back to base dataset created on 19/10/2021

    """

    try:
        now = datetime.now()
        stations = ['260','240']
        vars = ['TG'] # Mean temperature, add extra variables according to: https://www.daggegevens.knmi.nl/klimatologie/daggegevens
        data = {'stns': ":".join(stations), 
                'vars': ":".join(vars), 
                'byear': '2020', 
                'bmonth': '1', 
                'bday': '1', 
                'eyear': now.year, 
                'emonth': now.month, 
                'eday': now.day}

        endpoint = "https://www.daggegevens.knmi.nl/klimatologie/daggegevens"
        response = requests.get(endpoint, data)
        df = pd.read_csv(BytesIO(response.content), skiprows = 6 + len(stations) + len(vars))
        df.columns = [c.strip() for c in df.columns]
        df['TG'] = df['TG'] / 10 
        df.to_csv('base_temperature_nl.csv',index=False)
    except:
        df = pd.read_csv('data/Netherlands/base_temperature_nl.csv')
    return df

def get_temperature_df_nsw() -> pd.DataFrame:
    pass

