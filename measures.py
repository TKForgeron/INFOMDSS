import pandas as pd
from typing import List
from datetime import datetime, timedelta


def get_measures_df(start_date: datetime = None) -> pd.DataFrame:

    try:
        url = "https://raw.githubusercontent.com/OxCGRT/covid-policy-tracker/master/data/OxCGRT_latest.csv"
        df = pd.read_csv(
            url,
            dtype={
                "RegionName": str,
                "RegionCode": str,
                "CountryName": str,
                "CountryCode": str,
                "Date": str,
                "Jurisdiction": str,
            },
        )
    except:
        df = pd.read_csv("data/OxCGRT_latest.csv")

    df.rename(
        inplace=True,
        columns={
            "Date": "date",
            "ConfirmedCases": "cases",
            "ConfirmedDeaths": "deaths",
        },
    )
    df["date"] = df["date"].apply(lambda x: datetime.strptime(x, "%Y%m%d"))

    if start_date:
        df = df[df["date"] >= start_date]

    return df


def get_measures_df_il_nl_nsw(start_date: datetime = None) -> pd.DataFrame:

    try:
        url = "https://raw.githubusercontent.com/OxCGRT/covid-policy-tracker/master/data/OxCGRT_latest.csv"
        df = pd.read_csv(
            url,
            dtype={
                "RegionName": str,
                "RegionCode": str,
                "CountryName": str,
                "CountryCode": str,
                "Date": str,
                "Jurisdiction": str,
            },
        )
    except:
        df = pd.read_csv("data/OxCGRT_latest.csv")

    df = df[df["CountryCode"].isin(["AUS", "ISR", "NLD"])]
    df.rename(
        inplace=True,
        columns={
            "Date": "date",
            "ConfirmedCases": "cases",
            "ConfirmedDeaths": "deaths",
        },
    )

    df["date"] = df["date"].astype(str).apply(lambda x: datetime.strptime(x, "%Y%m%d"))

    if start_date:
        df = df[df["date"] >= start_date]

    return df


def split_measures_df_into_countries(
    df: pd.DataFrame,
) -> List[pd.DataFrame]:

    unique_countries = list(df["CountryCode"].unique())
    unique_country_dfs = []

    for country in unique_countries:
        mask = df["CountryCode"] == country
        unique_country_dfs.append(df[mask])

    return unique_country_dfs
