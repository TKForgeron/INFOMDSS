import pandas as pd
from sklearn.tree import DecisionTreeRegressor

import preprocessing_predictions as prep


def predict_stringency_index(update_progress_function) -> pd.DataFrame:
    """
        Function to retrieved the stringency index. This result is cached when in dev mode.
        Calls the 'update_progress_function' to update the progess, bc this can take a long time
    """

    update_progress_function()
    df = prep.get_prediction_train_data()

    update_progress_function()
    prediction_row = prep.get_data_to_predict_on()
    
    update_progress_function()
    stringency_nl_now = prep.get_latest_stringency_nl()

    update_progress_function()

    # defining training set
    x_train = df[["deaths", "cases", "hospitalizations", "temp"]]
    y_train = df["StringencyIndexForDisplay"]

    prediction_row = prediction_row.iloc[:, -4:]

    regressor = DecisionTreeRegressor(
        criterion="absolute_error", max_depth=20, random_state=32
    )


    update_progress_function()

    regressor.fit(x_train, y_train) # train the model

    update_progress_function()

    stringency_prediction = regressor.predict(prediction_row) # predict on the data
    stringency_prediction = stringency_prediction[0]
    update_progress_function()

    preDICTion = {
        "stringency_nl_now": [stringency_nl_now],
        "stringency_prediction": [stringency_prediction],
    }

    result_df = pd.DataFrame.from_dict(preDICTion)

    return result_df
