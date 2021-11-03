import pandas as pd
from datetime import datetime
import requests
import json
import populations


def get_hospitalizations_df_il(start_date: datetime = None) -> pd.DataFrame:

    """

    Function that reads hospitalization data from IL. It returns a dataframe with the hospitalizations per date.

    Parameters:
        start_date: if given the function returns a df with hospitalizations from that date onwards

    Returns:
        df with columns [date, hospitalizations]

    """

    try:
        endpoint = "https://data.gov.il/api/3/action/datastore_search?resource_id=d07c0771-01a8-43b2-96cc-c6154e7fa9bd&limit=1000000"
        response = requests.get(endpoint)
        records = json.loads(response.content)["result"]["records"]
        df = pd.DataFrame(records)
    except:
        df = pd.read_csv(
            "data/Israel/Israel_COVIDandVaccinated/geographic-sum-per-day-ver_00536_DS4.csv"
        )

    df["accumulated_hospitalized"] = (
        df["accumulated_hospitalized"]
        .replace(to_replace="<15", value="0")
        .astype(float)
        .astype(int)
    )

    df = df.groupby("date").sum("accumulated_hospitalized").reset_index()
    df["hospitalizations"] = df["accumulated_hospitalized"].transform(
        lambda s: s.sub(s.shift().fillna(0)).abs()
    )

    df["date"] = pd.to_datetime(df["date"])

    if start_date:
        df = df[df["date"] >= start_date]

    country_population = populations.get_population_nsw()

    df["hospitalizations_per_100k"] = round(df["hospitalizations"] / country_population * 100000, 1)

    df.sort_values(by=["date"])
    df = df[["date", "hospitalizations", "hospitalizations_per_100k"]]

    return df


def get_hospitalizations_df_nl(start_date: datetime = None) -> pd.DataFrame:

    """

    Function that reads hospitalization data from NL. It returns a dataframe with the hospitalizations per date.

    Parameters:
        start_date: if given the function returns a df with temps from that date onwards

    Returns:
        df with columns [date, hospitalizations]

    """
    try:
        df = pd.read_csv(
            "https://data.rivm.nl/covid-19/COVID-19_aantallen_gemeente_per_dag.csv",
            sep=";",
        )
    except:
        df = pd.read_csv(
            "data/Netherlands/COVID-19_aantallen_gemeente_per_dag.csv", sep=";"
        )

    df = (
        df.groupby("Date_of_publication")["Hospital_admission"]
        .sum()
        .reset_index(name="hospitalizations")
    )

    df["Date_of_publication"] = pd.to_datetime(df["Date_of_publication"])

    df = df.rename(columns={"Date_of_publication": "date"})

    if start_date:
        df = df[df["date"] >= start_date]

    country_population = populations.get_population_nl()

    df["hospitalizations_per_100k"] = round(df["hospitalizations"] / country_population * 100000, 1)

    df.sort_values(by=["date"])
    df = df[["date", "hospitalizations", "hospitalizations_per_100k"]]

    return df


def get_hospitalizations_df_nsw(start_date: datetime = None) -> pd.DataFrame:

    """

    Function that reads hospitalization data from NSW (using third party source: https://infogram.com/1p3ezk3xj239mwh0gg9v3vg0lqtdyyknzmx?live/).
    It returns a dataframe with the hospitalizations per date. Base dataframe last updated on 25/10/2021

    Parameters:
        start_date: if given the function returns a df with temps from that date onwards

    Returns:
        df with columns [date, hospitalizations]

    """

    # Try to get data from api, else read base dataframe
    try:
        endpoint = (
            "https://atlas.jifo.co/api/connectors/fc0400d2-2ddc-428c-b4ae-375bdfbeefb8"
        )
        response = requests.get(endpoint)
        records = json.loads(response.content)["data"][0]

        df = pd.DataFrame(records)
        df.columns = df.iloc[0]
        df = df[1:]
        df = df[["Date", "NSW"]]
    except:
        df = pd.read_csv("data/NSW/base_hospitalizations.csv")

    # The data only contains data from 15/3, in order to determine to which year an observation belongs, we need to fill the series
    datelist = [
        f"{str(date.day).zfill(2)}/{str(date.month).zfill(2)}"
        for date in pd.date_range(start="1/1/2020", end="14/3/2020").tolist()
    ]

    missing_dates_df = pd.DataFrame({"Date": datelist})
    missing_dates_df["NSW"] = ""

    df = pd.concat([missing_dates_df, df])
    df = df.reset_index()

    # If we have the same date twice (e.g 15/4), we need to determine to which year the observation belongs, starting in 2020
    df["year"] = (
        df.sort_values(["index"], ascending=[True]).groupby(["Date"]).cumcount() + 2020
    )

    df = df[df["NSW"] != ""]

    df["Date"] = df["Date"] + "/" + df["year"].astype(str)
    df["Date"] = pd.to_datetime(df["Date"])

    df = df[["Date", "NSW"]]
    df = df.rename(columns={"Date": "date", "NSW": "hospitalizations"})
    try:
        df["hospitalizations"] = (
            df["hospitalizations"]
            .dropna()
            .apply(lambda x: x.translate(str.maketrans("", "", "!@#$,")))
        )
    except:
        df["hospitalizations"] = df["hospitalizations"].dropna()

    df["hospitalizations"] = df["hospitalizations"].dropna().astype(int)

    if start_date:
        df = df[df["date"] >= start_date]
    
    # Clean ',' used to indicate thousands so change '1,164' to '1164' and convert them as int 
    df["hospitalizations"] = df["hospitalizations"].str.replace(',', '')
    df["hospitalizations"] = df["hospitalizations"].astype(int)

    country_population = populations.get_population_nsw()

    df["hospitalizations_per_100k"] = round(df["hospitalizations"] / country_population * 100000, 1)

    df.sort_values(by=["date"])
    df = df[["date", "hospitalizations", "hospitalizations_per_100k"]]

    return df
