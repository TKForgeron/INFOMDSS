import pandas as pd
from datetime import datetime


def get_last_month_hosp_df_il(df: pd.DataFrame) -> pd.DataFrame:
    df["accumulated_hospitalized"] = (
        df["accumulated_hospitalized"].replace(to_replace="<15", value="0").astype(int)
    )
    df["hospitalized"] = df.groupby(["town_code"])[
        "accumulated_hospitalized"
    ].transform(lambda s: s.sub(s.shift().fillna(0)).abs())
    df = df.groupby("date")["hospitalized"].sum().reset_index()
    df["date"] = pd.to_datetime(df["date"])
    df = df[df["date"] > datetime.now() - pd.DateOffset(months=1)]
    df = df.sort_values(by=["date"])
    return df


def get_last_month_hosp_df_nl(df: pd.DataFrame) -> pd.DataFrame:

    df = (
        df.groupby("Date_of_publication")["Hospital_admission"]
        .sum()
        .reset_index(name="cases")
    )
    df["Date_of_publication"] = pd.to_datetime(df["Date_of_publication"])
    df = df[df.Date_of_publication > datetime.now() - pd.DateOffset(months=1)]
    df.sort_values(by=["Date_of_publication"])
    return df
