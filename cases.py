import pandas as pd
from datetime import datetime


def get_cases_trend(df: pd.DataFrame) -> str:
    df["date"] = pd.to_datetime(df["date"])
    df_without_last = df[:-1]
    df = df_without_last[
        df_without_last["date"] > datetime.now() - pd.DateOffset(weeks=1)
    ]
    latest_cases = get_latest_new_cases(df)
    week_average = df["cases"].average()

    growth_percentage = (latest_cases - week_average) / week_average * 100

    if growth_percentage < -30:
        return "strong decrease"
    elif growth_percentage < -10:
        return "decrease"
    elif growth_percentage < 10:
        return "neutral"
    elif growth_percentage < 30:
        return "increase"
    else:
        return "strong increase"


def get_last_month_cases_df_il(df: pd.DataFrame) -> pd.DataFrame:
    df["accumulated_cases"] = (
        df["accumulated_cases"].replace(to_replace="<15", value="0").astype(int)
    )
    df["cases"] = df.groupby(["town_code"])["accumulated_cases"].transform(
        lambda s: s.sub(s.shift().fillna(0)).abs()
    )
    df = df.groupby("date")["cases"].sum().reset_index()
    df["date"] = pd.to_datetime(df["date"])
    df = df[df["date"] > datetime.now() - pd.DateOffset(months=1)]
    df = df.sort_values(by=["date"])
    return df


def get_last_month_cases_df_nsw(df: pd.DataFrame) -> pd.DataFrame:
    df["notification_date"] = pd.to_datetime(df["notification_date"])
    df = df[df["notification_date"] > datetime.now() - pd.DateOffset(months=1)]
    df = df.groupby("notification_date").size().reset_index(name="cases")
    df = df.sort_values(by=["notification_date"])
    return df


def get_last_month_cases_df_nl(df: pd.DataFrame) -> pd.DataFrame:

    df = (
        df.groupby("Date_of_publication").Total_reported.sum().reset_index(name="cases")
    )
    df["Date_of_publication"] = pd.to_datetime(df["Date_of_publication"])
    df = df[df.Date_of_publication > datetime.now() - pd.DateOffset(months=1)]
    df.sort_values(by=["Date_of_publication"])
    return df


def get_latest_new_cases(df: pd.DataFrame) -> int:
    return df["cases"].iloc[-1]
