import pandas as pd

import measures as m
import cases as c
import hospitalizations as h
import vaccinations as v
import temperature as t


def get_prediction_train_data() -> pd.DataFrame:

    # VACCINATIONS ARE EXCLUDED AS PREDICTOR VARIABLE
    # bc NSW has only one week (last) of vaccination data
    # vaccinations_il = v.get_vaccinations_df_il()
    # vaccinations_nl = v.get_vaccinations_df_nl()
    # vaccinations_nsw = v.get_vaccinations_df_nsw()

    temperatures_il = t.get_temperatures_df_il()
    temperatures_nl = t.get_temperatures_df_nl()
    temperatures_nsw = t.get_temperatures_df_nsw()

    cases_columns = ["date", "cases"]
    cases_il = c.get_cases_df_il()[cases_columns]
    cases_nl = c.get_cases_df_nl()[cases_columns]
    cases_nsw = c.get_cases_df_nsw()[cases_columns]

    hospitalizations_il = h.get_hospitalizations_df_il()
    hospitalizations_nl = h.get_hospitalizations_df_nl()
    hospitalizations_nsw = h.get_hospitalizations_df_nsw()

    stringency_columns = ["date", "StringencyIndexForDisplay", "deaths", "CountryName"]
    df_measures = m.get_measures_df_il_nl_nsw()
    unique_country_dfs = m.split_measures_df_into_countries(df_measures)
    stringency_deaths_nsw = unique_country_dfs[0][stringency_columns]
    stringency_deaths_il = unique_country_dfs[1][stringency_columns]
    stringency_deaths_nl = unique_country_dfs[2][stringency_columns]

    # ISRAEL merging cases, deaths, hospitalizations, and stringencyIndex on date
    cases_stringency_deaths_il = pd.merge(
        stringency_deaths_il, cases_il, how="inner", on="date"
    )
    cases_stringe_deaths_hosp_il = pd.merge(
        cases_stringency_deaths_il, hospitalizations_il, how="inner", on="date"
    )
    cases_stringe_hosp_deaths_temp_il = pd.merge(
        cases_stringe_deaths_hosp_il, temperatures_il, how="inner", on="date"
    )
    # cases_stringe_hosp_deaths_temp_vacc_il = pd.merge(
    #     cases_stringe_hosp_deaths_temp_il, vaccinations_il, how="inner", on="date"
    # )

    # NETHERLANDS merging cases, deaths, hospitalizations, and stringencyIndex on date
    cases_stringency_deaths_nl = pd.merge(
        stringency_deaths_nl, cases_nl, how="inner", on="date"
    )
    cases_stringe_deaths_hosp_nl = pd.merge(
        cases_stringency_deaths_nl, hospitalizations_nl, how="inner", on="date"
    )
    cases_stringe_hosp_deaths_temp_nl = pd.merge(
        cases_stringe_deaths_hosp_nl, temperatures_nl, how="inner", on="date"
    )
    # cases_stringe_hosp_deaths_temp_vacc_nl = pd.merge(
    #     cases_stringe_hosp_deaths_temp_nl, vaccinations_nl, how="inner", on="date"
    # )

    # NEW SOUTH WALES merging cases, deaths, hospitalizations, and stringencyIndex on date
    cases_stringency_deaths_nsw = pd.merge(
        stringency_deaths_nsw, cases_nsw, how="inner", on="date"
    )
    cases_stringe_deaths_hosp_nsw = pd.merge(
        cases_stringency_deaths_nsw, hospitalizations_nsw, how="inner", on="date"
    )
    cases_stringe_hosp_deaths_temp_nsw = pd.merge(
        cases_stringe_deaths_hosp_nsw, temperatures_nsw, how="inner", on="date"
    )
    # cases_stringe_hosp_deaths_temp_vacc_nsw = pd.merge(
    #     cases_stringe_hosp_deaths_temp_nsw, vaccinations_nsw, how="inner", on="date"
    # )

    # DROP last week from training data
    n = max(
        [
            cases_stringe_hosp_deaths_temp_il.shape[0],
            cases_stringe_hosp_deaths_temp_nl.shape[0],
            cases_stringe_hosp_deaths_temp_nsw.shape[0],
        ]
    )
    # concatenating IL, NL, NSW to one dataframe
    predictors = pd.concat(
        [
            cases_stringe_hosp_deaths_temp_il.head(n - 7),
            cases_stringe_hosp_deaths_temp_nl.head(n - 7),
            cases_stringe_hosp_deaths_temp_nsw.head(n - 7),
        ]
    )

    # drop all rows where NaN is present
    predictors = predictors.dropna()
    # df = df.drop("date", axis=1)
    predictors = predictors.sort_values(by="date").set_index("date")

    # all predictor variables: ["deaths", "cases", "hospitalizations", "temp"]

    return predictors


def get_data_to_predict_on():
    temperatures_nl = t.get_temperatures_df_nl()
    cases_columns = ["date", "cases"]
    cases_nl = c.get_cases_df_nl()[cases_columns]
    hospitalizations_nl = h.get_hospitalizations_df_nl()

    stringency_columns = ["date", "StringencyIndexForDisplay", "deaths", "CountryName"]
    df_measures = m.get_measures_df_il_nl_nsw()
    unique_country_dfs = m.split_measures_df_into_countries(df_measures)
    stringency_deaths_nl = unique_country_dfs[2][stringency_columns]

    # NETHERLANDS merging cases, deaths, hospitalizations, and stringencyIndex on date
    cases_stringency_deaths_nl = pd.merge(
        stringency_deaths_nl, cases_nl, how="inner", on="date"
    )
    cases_stringe_deaths_hosp_nl = pd.merge(
        cases_stringency_deaths_nl, hospitalizations_nl, how="inner", on="date"
    )
    cases_stringe_hosp_deaths_temp_nl = pd.merge(
        cases_stringe_deaths_hosp_nl, temperatures_nl, how="inner", on="date"
    )

    latest_week = cases_stringe_hosp_deaths_temp_nl.tail(7)
    # mean_latest_week = pd.DataFrame(latest_week.mean(axis=0).T)
    mean_latest_week = pd.DataFrame(latest_week.mean(axis=0)).T

    return mean_latest_week


def get_measures_data() -> pd.DataFrame:

    df_measures = m.get_measures_df()
    stringency_columns = ["date", "StringencyIndexForDisplay", "deaths", "cases"]
    df_measures = df_measures[stringency_columns]
    df_measures = df_measures.sort_values(by="date")
    df_measures = df_measures.dropna()

    return df_measures
