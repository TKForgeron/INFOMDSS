import pandas as pd
from datetime import datetime
import requests
import json
import populations


def get_cases_df_il(start_date: datetime = None) -> pd.DataFrame:

    """
    Function that cleans the cases dataframe for Israel, and calculates daily cases from accumulated cases

    Parameters:
        start_date: if given the function returns a df with temps from that date onwards

    Returns:
        df with columns [date, cases, cases_per_100k]
    """

    df = pd.read_csv(
        "data/Israel/Israel_COVIDandVaccinated/geographic-sum-per-day-ver_00536_DS4.csv"
    )

    df["accumulated_cases"] = (
        df["accumulated_cases"].replace(to_replace="<15", value="0").astype(int)
    )

    df = df.groupby("date").sum("accumulated_cases").reset_index()

    df["cases"] = df.groupby(["town_code"])["accumulated_cases"].transform(
        lambda s: s.sub(s.shift().fillna(0)).abs()
    )

    df["date"] = pd.to_datetime(df["date"])

    if start_date:
        df = df[df["date"] >= start_date]

    country_population = populations.get_population_il()

    df["cases_per_100k"] = round(df["cases"] / country_population * 100000, 1)

    df = df.sort_values(by=["date"])
    df = df[["date", "cases", "cases_per_100k"]]
    return df


def get_cases_df_nsw(start_date: datetime = None) -> pd.DataFrame:

    """
    Function that cleans the cases dataframe for NSW, and calculates daily cases from amount of rows

    Parameters:
        start_date: if given the function returns a df with temps from that date onwards

    Returns:
        df with columns [date, cases, cases_per_100k]
    """

    df = pd.read_csv("data/NSW/confirmed_cases_table2_age_group_DS6.csv")

    df = df.rename({"notification_date": "date"}, axis="columns")
    df["date"] = pd.to_datetime(df["date"])

    if start_date:
        df = df[df["date"] >= start_date]

    df = df.groupby("date").size().reset_index(name="cases")

    country_population = populations.get_population_nsw()

    df["cases_per_100k"] = round(df["cases"] / country_population * 100000, 1)
    df = df.sort_values(by=["date"])
    df = df[["date", "cases", "cases_per_100k"]]
    return df


def get_cases_df_nl(start_date: datetime = None) -> pd.DataFrame:

    """
    Function that cleans the cases dataframe for the Netherlands, and calculates daily cases from the sum of reported cases per muncipality

    Parameters:
        start_date: if given the function returns a df with temps from that date onwards

    Returns:
        df with columns [date, cases, cases_per_100k]
    """

    df = pd.read_csv(
        "data/Netherlands/COVID-19_aantallen_gemeente_per_dag.csv", sep=";"
    )

    df = df.rename({"Date_of_publication": "date"}, axis="columns")

    df = df.groupby("date")["Total_reported"].sum().reset_index(name="cases")
    df["date"] = pd.to_datetime(df["date"])

    if start_date:
        df = df[df["date"] >= start_date]

    country_population = populations.get_population_nl()

    df["cases_per_100k"] = round(df["cases"] / country_population * 100000, 1)

    df.sort_values(by=["date"])
    df = df[["date", "cases", "cases_per_100k"]]

    return df
