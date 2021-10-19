import pandas as pd
from datetime import datetime

def get_latest_kpi_value(df: pd.DataFrame, kpi_col: str) -> int:

    """
    Function that returns the passed kpi for the last record in the dataframe

    """

    return df[kpi_col].iloc[-1]

def get_kpi_trend(df: pd.DataFrame, kpi_col: str) -> str:

    """
    Function that returns the trend for the passed KPI, based on last recorded value, and average of 7 records before recorded value

    """

    latest_cases = get_latest_kpi_value(df, kpi_col)

    df_without_last = df[:-1]
    df_without_last = df_without_last.iloc[-7:]
    week_average = df_without_last[kpi_col].mean()

    growth_percentage = (latest_cases - week_average) / week_average * 100

    if growth_percentage < -30:
        return "Strong decrease"
    elif growth_percentage < -10:
        return "Decrease"
    elif growth_percentage < 10:
        return "Neutral"
    elif growth_percentage < 30:
        return "Increase"
    else:
        return "Strong increase"
