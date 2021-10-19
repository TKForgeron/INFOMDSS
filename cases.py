import pandas as pd
from datetime import datetime
import requests
import json

def get_cases_df_il(df: pd.DataFrame, months: int = None) -> pd.DataFrame:

    """
    Function that cleans the cases dataframe for Israel, and calculates daily cases from accumulated cases
    
    Parameters:
    df: raw cases_df for israel
    months: int, how many months of historical data to show, default: entire history

    Returns: sorted pd.Dataframe with case count in cases column, filtered on last nmonths (based on value of months parameter)
    """

    df["accumulated_cases"] = (
        df["accumulated_cases"].replace(to_replace="<15", value="0").astype(int)
    )
    df["cases"] = df.groupby(["town_code"])["accumulated_cases"].transform(
        lambda s: s.sub(s.shift().fillna(0)).abs()
    )
    df = df.groupby("date")["cases"].sum().reset_index()
    df["date"] = pd.to_datetime(df["date"])
    
    if months:
        df = df[df["date"] > datetime.now() - pd.DateOffset(months=months)]
    try:
        response = requests.get("https://apis.cbs.gov.il/series/data/list?id=3763&startperiod=01-2021&format=json&download=false&lang=en")
        country_population = json.loads(response.content)['DataSet']['Series'][0]['obs'][0]['Value'] * 1000
    except:
        country_population = 9217000

    df['cases_per_100k'] = round(df['cases'] / country_population * 100000, 1)

    df = df.sort_values(by=["date"])
    return df


def get_cases_df_nsw(df: pd.DataFrame, months: int = None) -> pd.DataFrame:

    """
    Function that cleans the cases dataframe for NSW, and calculates daily cases from amount of rows
    
    Parameters:
    df: raw cases_df for nsw
    months: int, how many months of historical data to show, default: entire history

    Returns: sorted pd.Dataframe with case count in cases column, filtered on last nmonths (based on value of months parameter)
    """


    df = df.rename({"notification_date": "date"}, axis='columns')
    df["date"] = pd.to_datetime(df["date"])
    if months:
        df = df[df["date"] > datetime.now() - pd.DateOffset(months=1)]
    df = df.groupby("date").size().reset_index(name="cases")


    try:
        response = requests.get("https://stat.data.abs.gov.au/sdmx-json/data/ERP_QUARTERLY/1.1.3.TT.Q/all?startTime=2021-Q1")
        observations = json.loads(response.content)['dataSets'][0]['series']["0:0:0:0:0"]['observations']
        latest_observation_key = sorted(observations.keys())[-1]
        country_population = observations[latest_observation_key][0]
    except:
        country_population = 8176369

    df['cases_per_100k'] = round(df['cases'] / country_population * 100000, 1)
    df = df.sort_values(by=["date"])
    return df


def get_cases_df_nl(df: pd.DataFrame, months: int = None) -> pd.DataFrame:
    
    """
    Function that cleans the cases dataframe for the Netherlands, and calculates daily cases from the sum of reported cases per muncipality
    
    Parameters:
    df: raw cases_df for the Netherlands
    months: int, how many months of historical data to show, default: entire history

    Returns: sorted pd.Dataframe with case count in cases column, filtered on last nmonths (based on value of months parameter)
    """

    df = df.rename({"Date_of_publication": "date"},axis='columns')
    
    df = (
        df.groupby("date")['Total_reported'].sum().reset_index(name="cases")
    )
    df["date"] = pd.to_datetime(df["date"])
    if months:
        df = df[df['date'] > datetime.now() - pd.DateOffset(months=1)]

    try:
        response = requests.get("https://opendata.cbs.nl/ODataApi/odata/37296ned/TypedDataSet")
        country_population = json.loads(response.content)['value'][-1]['TotaleBevolking_1']
    except:
        country_population = 17183583

    df['cases_per_100k'] = round(df['cases'] / country_population * 100000, 1)

    df.sort_values(by=["date"])
    return df


