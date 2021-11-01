import pandas as pd

import measures as m
import cases as c
import hospitalizations as h
import vaccinations as v
import temperature as t


def get_prediction_data() -> pd.DataFrame:
    temperatures_il = t.get_temperatures_df_il()
    temperatures_nl = t.get_temperatures_df_nl()
    temperatures_nsw = t.get_temperatures_df_nsw()

    vaccinations_il = v.get_vaccinations_df_il()
    vaccinations_nl = v.get_vaccinations_df_nl()
    vaccinations_nsw = v.get_vaccinations_df_nsw()

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
    cases_stringe_hosp_deaths_vacc_il = pd.merge(
        cases_stringe_deaths_hosp_il, vaccinations_il, how="inner", on="date"
    )
    cases_stringe_hosp_deaths_vacc_temp_il = pd.merge(
        cases_stringe_hosp_deaths_vacc_il, temperatures_il, how="inner", on="date"
    )

    # NETHERLANDS merging cases, deaths, hospitalizations, and stringencyIndex on date
    cases_stringency_deaths_nl = pd.merge(
        stringency_deaths_nl, cases_nl, how="inner", on="date"
    )
    cases_stringe_deaths_hosp_nl = pd.merge(
        cases_stringency_deaths_nl, hospitalizations_nl, how="inner", on="date"
    )
    cases_stringe_hosp_deaths_vacc_nl = pd.merge(
        cases_stringe_deaths_hosp_nl, vaccinations_nl, how="inner", on="date"
    )
    cases_stringe_hosp_deaths_vacc_temp_nl = pd.merge(
        cases_stringe_hosp_deaths_vacc_nl, temperatures_nl, how="inner", on="date"
    )

    # NEW SOUTH WALES merging cases, deaths, hospitalizations, and stringencyIndex on date
    cases_stringency_deaths_nsw = pd.merge(
        stringency_deaths_nsw, cases_nsw, how="inner", on="date"
    )
    cases_stringe_deaths_hosp_nsw = pd.merge(
        cases_stringency_deaths_nsw, hospitalizations_nsw, how="inner", on="date"
    )
    cases_stringe_hosp_deaths_vacc_nsw = pd.merge(
        cases_stringe_deaths_hosp_nsw, vaccinations_nsw, how="inner", on="date"
    )
    cases_stringe_hosp_deaths_vacc_temp_nsw = pd.merge(
        cases_stringe_hosp_deaths_vacc_nsw, temperatures_nsw, how="inner", on="date"
    )

    # concatenating IL, NL, NSW to one dataframe
    cases_stringe_hosp_deaths_vacc_temp = pd.concat(
        [
            cases_stringe_hosp_deaths_vacc_temp_il,
            cases_stringe_hosp_deaths_vacc_temp_nl,
            cases_stringe_hosp_deaths_vacc_temp_nsw,
        ]
    )

    # drop all rows where NaN is present
    df = cases_stringe_hosp_deaths_vacc_temp.dropna()
    # df = df.drop("date", axis=1)
    df = df.sort_values(by="date").set_index("date")

    # all predictor variables: ["deaths", "cases", "hospitalizations", "vaccination_coverage", "temp"]

    return df


def get_measures_data() -> pd.DataFrame:

    df_measures = m.get_measures_df()
    stringency_columns = ["date", "StringencyIndexForDisplay", "deaths", "cases"]
    df_measures = df_measures[stringency_columns]
    df_measures = df_measures.sort_values(by="date")
    df_measures = df_measures.dropna()

    return df_measures
