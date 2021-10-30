import pandas as pd
from datetime import datetime, timedelta
import populations
import json
import requests


def get_vaccinations_df_il(start_date: datetime = None) -> pd.DataFrame:

    """

    Function that sums list of vaccination columns, aggregates on town code and creates incremental vaccination count based on cummulative data
    Returns: sorted pd.DataFrame with columns [date, vaccination_coverage]

    """
    # Try to get data from api, else read base dataframe
    try:
        endpoint = "https://data.gov.il/api/3/action/datastore_search?resource_id=12c9045c-1bf4-478a-a9e1-1e876cc2e182&limit=1000000"
        response = requests.get(endpoint)
        records = json.loads(response.content)["result"]["records"]

        df = pd.DataFrame(records)
    except:
        df = pd.read_csv("data/Israel/vaccinated_city_table_ver_00218_DS5.csv")

    df.columns = [x.lower() for x in df.columns]
    age_groups = [
        "0-19",
        "20-29",
        "30-39",
        "40-49",
        "50-59",
        "60-69",
        "70-79",
        "80-89",
        "90+",
    ]
    vaccination_columns = [[f"second_dose_{age_group}"] for age_group in age_groups]
    vaccination_columns = [item for sublist in vaccination_columns for item in sublist]

    df[vaccination_columns] = (
        df[vaccination_columns].replace(to_replace="<15", value="0").astype(float)
    )

    df["accumulated_vaccinations"] = df[vaccination_columns].sum(axis=1)

    df = df.groupby("date")["accumulated_vaccinations"].sum().reset_index()

    df["vaccination_coverage"] = (
        df["accumulated_vaccinations"] / populations.get_population_il() * 100
    )

    df["date"] = pd.to_datetime(df["date"])

    if start_date:
        df = df[df["date"] >= start_date]

    df = df.sort_values(by=["date"])
    df = df[["date", "vaccination_coverage"]]

    return df


def get_vaccinations_df_nl(start_date: datetime = None) -> pd.DataFrame:

    """

    Function that sums list of vaccination columns, aggregates on town code and creates incremental vaccination count based on cummulative data
    Returns: sorted pd.DataFrame with the total vaccinations in the Netherlands per date with columns [date, vaccination_coverage]

    """

    df = get_vaccinations_per_age_group_nl(start_date)

    df_leeftijden = pd.read_csv(
        "data/Netherlands/Leeftijdsopbouw Nederland 2021 (prognose).csv", sep=";"
    )

    df_leeftijden["Leeftijd"] = df_leeftijden["Leeftijd"].str.replace("jaar", "")
    df_leeftijden = df_leeftijden[2:].reset_index(drop=True)
    df_leeftijden["Mannen"] = df_leeftijden["Mannen"].str.replace(" ", "").astype(int)
    df_leeftijden["Vrouwen"] = df_leeftijden["Vrouwen"].str.replace(" ", "").astype(int)
    df_leeftijden["Total"] = df_leeftijden["Mannen"] + df_leeftijden["Vrouwen"]
    df_leeftijden["Geboortejaar"] = 2021 - df_leeftijden["Leeftijd"].astype(int)
    df_leeftijden = df_leeftijden[["Total", "Geboortejaar"]]

    age_range = [1800] + list(range(1930, 1996, 5)) + [2003] + [2009]
    df_leeftijden["range"] = pd.cut(df_leeftijden["Geboortejaar"], bins=age_range)
    df_leeftijden = df_leeftijden.dropna()
    df_leeftijden = df_leeftijden.groupby("range").sum("Total").reset_index()
    df_leeftijden = df_leeftijden[["range", "Total"]]
    df_leeftijden = df_leeftijden.T

    for column in df.drop("date", axis=1):
        index = df.columns.get_loc(column)
        df[column] = (
            df[df.columns[index]]
            * df_leeftijden[df_leeftijden.columns[-index]]["Total"]
            * 0.01
        )

    df["vaccination_coverage"] = (
        df.drop("date", axis=1).sum(axis=1) / populations.get_population_nl() * 100
    )
    df = df[["date", "vaccination_coverage"]]

    return df


def get_vaccinations_df_nsw(start_date: datetime = None) -> pd.DataFrame:
    yesterday = datetime.today() - timedelta(days=1)
    current_week = yesterday.isocalendar().week
    current_year = yesterday.year
    year_week = f"{current_year}-W{current_week}"
    last_monday = datetime.strptime(year_week + "-1", "%Y-W%W-%w")

    date_string = last_monday.strftime("%d-%B-%Y").lower()
    date_month = str(last_monday.month).zfill(2)

    path = f"https://www.health.gov.au/sites/default/files/documents/2021/{date_month}/covid-19-vaccination-geographic-vaccination-rates-sa3-{date_string}.xlsx"
    df = pd.read_excel(path, usecols=[0, 2, 4])
    df = df[df[df.columns[0]] == "New South Wales"]
    df["date"] = last_monday
    df.columns = ["state", "population", "vaccination_coverage", "date"]
    df["vaccination_coverage"] = df["vaccination_coverage"].apply(
        lambda x: 0.95 if x == ">95%" else x
    )
    df["vaccination_coverage"] = df["vaccination_coverage"].astype(float)

    df["vaccination_absolutes"] = df["vaccination_coverage"] * df["population"]

    vaccination_coverage = df["vaccination_absolutes"].sum() / df["population"].sum()
    df = df[["date", "vaccination_coverage"]].iloc[[0]]
    df["vaccination_coverage"] = vaccination_coverage

    return df


def get_vaccinations_per_age_group_nl(start_date: datetime = None) -> pd.DataFrame:

    df = pd.read_csv(
        "data/Netherlands/cumulative-vaccination-coverage-for-full-covid-19-vaccination-by-birth-year-and-week_DS3.csv",
        sep=";",
    )
    df["date"] = df.apply(
        lambda x: pd.to_datetime("2020-12-28")
        + pd.offsets.DateOffset(weeks=int(x["Weeknumber"])),
        1,
    )
    if start_date:
        df = df[df["date"] >= start_date]
    df = df.drop("Weeknumber", axis=1)
    return df
