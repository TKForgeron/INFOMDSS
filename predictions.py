from datetime import datetime
import pandas as pd

from sklearn.feature_extraction.text import CountVectorizer
from sklearn.model_selection import train_test_split, StratifiedKFold, cross_val_score
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import confusion_matrix, classification_report
from sklearn.preprocessing import LabelEncoder
from sklearn.ensemble import RandomForestClassifier
from sklearn.tree import DecisionTreeClassifier

import measures as m
import cases as c
import hospitalizations as h

cases_columns = ["date", "cases"]
cases_il = c.get_cases_df_il()[cases_columns]
cases_nl = c.get_cases_df_nl()[cases_columns]
cases_nsw = c.get_cases_df_nsw()[cases_columns]

hospitalizations_il = h.get_hospitalizations_df_il()
hospitalizations_nl = h.get_hospitalizations_df_nl()
hospitalizations_nsw = h.get_hospitalizations_df_nsw()

stringency_columns = ["date", "StringencyIndexForDisplay", "deaths"]
df_measures = m.get_measures_df_il_nl_nsw()
unique_country_dfs = m.split_measures_df_into_countries(df_measures)
stringency_nsw = unique_country_dfs[0][stringency_columns]
stringency_il = unique_country_dfs[1][stringency_columns]
stringency_nl = unique_country_dfs[2][stringency_columns]

# ISRAEL merging cases, deaths, hospitalizations, and stringencyIndex on date
cases_stringency_il = pd.merge(stringency_il, cases_il, how="outer", on="date")
cases_stringe_hosp_il = pd.merge(
    cases_stringency_il, hospitalizations_il, how="outer", on="date"
)

# NETHERLANDS merging cases, deaths, hospitalizations, and stringencyIndex on date
cases_stringency_nl = pd.merge(stringency_nl, cases_nl, how="outer", on="date")
cases_stringe_hosp_nl = pd.merge(
    cases_stringency_nl, hospitalizations_nl, how="outer", on="date"
)

# NEW SOUTH WALES merging cases, deaths, hospitalizations, and stringencyIndex on date
cases_stringency_nsw = pd.merge(stringency_nsw, cases_nsw, how="outer", on="date")
cases_stringe_hosp_nsw = pd.merge(
    cases_stringency_nsw, hospitalizations_nsw, how="outer", on="date"
)

# concatenating IL, NL, NSW to one dataframe
cases_stringe_hosp_deaths = pd.concat(
    [cases_stringe_hosp_il, cases_stringe_hosp_nl, cases_stringe_hosp_nsw]
)

folds = StratifiedKFold(n_splits=10)

# cases_stringe_hosp_deaths.to_excel(
#     "data/cases_stringe_hosp_deaths.xlsx", sheet_name="IL_NL_AUS"
# )
