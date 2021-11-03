import pandas as pd
import numpy as np
from statistics import mean
from datetime import datetime
import random

from sklearn.feature_extraction.text import CountVectorizer
from sklearn.model_selection import train_test_split, cross_val_score, KFold
from sklearn.tree import DecisionTreeRegressor

import preprocessing_predictions as prep


def predict_stringency_index() -> dict:

    print("Loading prediction data")
    df = prep.get_prediction_train_data()
    x_train = df[["deaths", "cases", "hospitalizations", "temp"]]  # , 'vaccinations']]
    y_train = df["StringencyIndexForDisplay"]

    # folds = KFold(n_splits=10, shuffle=True, random_state=32)

    x_train = df[["deaths", "cases", "hospitalizations", "temp"]]
    y_train = df["StringencyIndexForDisplay"]

    regressor = DecisionTreeRegressor(
        criterion="absolute_error", max_depth=20, random_state=32
    )

    print("fitting regression tree...")
    regressor.fit(x_train, y_train)

    prediction_data = prep.get_data_to_predict_on()
    stringency_nl_now = prep.get_latest_stringency_nl()
    prediction_data = prediction_data.iloc[:, -4:]

    print("now predicting on: \n", prediction_data)
    stringency_prediction = regressor.predict(prediction_data)
    stringency_prediction = stringency_prediction[0]

    return {
        "stringency_nl_now": stringency_nl_now,
        "stringency_prediction": stringency_prediction,
    }


# print(datetime.now())
# result = predict_stringency_index()
# print(result)
