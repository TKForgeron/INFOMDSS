import pandas as pd
import requests
from datetime import datetime
import json
from zipfile import ZipFile
from io import BytesIO
import urllib.request as urllib2


def get_temperature_df_il(start_date: datetime = None) -> pd.DataFrame:

    """

    Function that reads temperature data from Israel. It returns the average temperature on each day from October 2019 onwards.
    Parameters:
        start_date: if given the function returns a df with temps from that date onwards

    Returns:
        df with columns [date, temp]

    """

    df = pd.read_csv(
        "data/Israel/ims_data_DS13.csv", usecols=[2, 3, 4], encoding="ISO-8859-8"
    )
    df.columns = ["date", "temp_max", "temp_min"]
    df = df[df["temp_max"] != "-"]
    df["temp_max"] = df["temp_max"].astype(float)
    df["temp"] = df[["temp_max", "temp_min"]].mean(axis=1)
    df = df[["date", "temp"]]
    df["date"] = pd.to_datetime(df["date"])

    if start_date:
        df = df[df["date"] >= start_date]

    return df


def get_temperature_df_nl(start_date: datetime = None) -> pd.DataFrame:

    """

    Function that consumes the KNMI api to get the most recent weather data. In case an error occurs while making the API requests,
    fall back to base dataset created on 25/10/2021
    Parameters:
        start_date: if given the function returns a df with temps from that date onwards

    Returns:
        df with columns [date, temp]

    """

    if start_date:
        byear = start_date.year
        bmonth = start_date.month
        bday = start_date.day
    else:
        byear = 2020
        bmonth = 1
        bday = 1

    try:
        now = datetime.now()
        stations = ["260"]
        vars = [
            "TG"
        ]  # Mean temperature, add extra variables according to: https://www.daggegevens.knmi.nl/klimatologie/daggegevens
        data = {
            "stns": ":".join(stations),
            "vars": ":".join(vars),
            "byear": byear,
            "bmonth": bmonth,
            "bday": bday,
            "eyear": now.year,
            "emonth": now.month,
            "eday": now.day,
        }

        endpoint = "https://www.daggegevens.knmi.nl/klimatologie/daggegevens"
        response = requests.get(endpoint, data)
        df = pd.read_csv(
            BytesIO(response.content), skiprows=6 + len(stations) + len(vars)
        )
        df.columns = [c.strip() for c in df.columns]
        df["TG"] = df["TG"] / 10
    except:
        df = pd.read_csv("data/Netherlands/base_temperature_nl.csv")

    df = df[["YYYYMMDD", "TG"]]
    df = df.rename(columns={"TG": "temp", "YYYYMMDD": "date"})
    df["date"] = pd.to_datetime(df["date"], format="%Y%m%d")
    return df


def get_temperature_df_nsw(start_date: datetime = None) -> pd.DataFrame:

    """

    Function that reads temperature data from NSW. It returns the average temperature on each day from October 19th 2017 onwards.
    Parameters:
        start_date: if given the function returns a df with temps from that date onwards

    Returns:
        df with columns [date, temp]

    """

    df_max = pd.read_csv("data/NSW/IDCJAC0010_066214_1800_Data_MAX_DS15.csv")
    df_min = pd.read_csv("data/NSW/IDCJAC0011_066214_1800_MIN_DS15.csv")

    df_min = df_min[["Year", "Month", "Day", "Minimum temperature (Degree C)"]]
    df_max = df_max[["Year", "Month", "Day", "Maximum temperature (Degree C)"]]

    df = df_min.merge(df_max, on=["Year", "Month", "Day"]).dropna()
    df["temp"] = df[
        ["Maximum temperature (Degree C)", "Minimum temperature (Degree C)"]
    ].mean(axis=1)
    df["date"] = pd.to_datetime(df[["Year", "Month", "Day"]])
    df = df[["date", "temp"]]
    if start_date:
        df = df[df["date"] >= start_date]

    return df


get_temperature_df_nsw()
