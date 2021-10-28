import pandas as pd
import json
import requests
from datetime import datetime


def get_measures_df_il() -> pd.DataFrame:
    pass


def get_measures_df_nl() -> pd.DataFrame:
    pass


def get_measures_df_nsw() -> pd.DataFrame:
    pass


def get_measures_df(start_date: datetime = None) -> pd.DataFrame:

    try:
        url = "https://raw.githubusercontent.com/OxCGRT/covid-policy-tracker/master/data/OxCGRT_latest.csv"
        df = pd.read_csv(url)
    except:
        df = pd.read_csv("data/OxCGRT_latest.csv")

    df = df[df["CountryCode"].isin(["AUS", "ISR", "NLD"])]

    return df


get_measures_df()
