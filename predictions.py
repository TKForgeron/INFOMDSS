import pandas as pd
from datetime import datetime

# from sklearn.preprocessing import PolynomialFeatures
# from sklearn.pipeline import make_pipeline
# from sklearn.linear_model import LinearRegression
from sklearn.tree import DecisionTreeRegressor

import preprocessing_predictions as prep


def predict_stringency_index() -> pd.DataFrame:

    print("Loading prediction data")
    df = prep.get_prediction_train_data()
    prediction_row = prep.get_data_to_predict_on()
    stringency_nl_now = prep.get_latest_stringency_nl()

    # defining training set
    x_train = df[["deaths", "cases", "hospitalizations", "temp"]]
    y_train = df["StringencyIndexForDisplay"]

    prediction_row = prediction_row.iloc[:, -4:]

    regressor = DecisionTreeRegressor(
        criterion="absolute_error", max_depth=20, random_state=32
    )

    # degree = len(list(x_train.columns))
    # regressor = make_pipeline(PolynomialFeatures(degree), LinearRegression())

    print("fitting regression tree...")
    regressor.fit(x_train, y_train)

    print("now predicting on: \n", prediction_row)
    stringency_prediction = regressor.predict(prediction_row)
    stringency_prediction = stringency_prediction[0]

    preDICTion = {
        "stringency_nl_now": [stringency_nl_now],
        "stringency_prediction": [stringency_prediction],
    }

    result_df = pd.DataFrame.from_dict(preDICTion)

    return result_df


print(datetime.now())
result = predict_stringency_index()
print(result)
