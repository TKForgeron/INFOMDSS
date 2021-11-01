import pandas as pd
from statistics import mean

from sklearn.feature_extraction.text import CountVectorizer
from sklearn.model_selection import (
    train_test_split,
    cross_val_score,
    KFold,
)
from sklearn.linear_model import LogisticRegression, LinearRegression
from sklearn.metrics import confusion_matrix, classification_report
from sklearn.preprocessing import LabelEncoder
from sklearn.ensemble import RandomForestRegressor
from sklearn.tree import DecisionTreeClassifier

import preprocessing_predictions as prep

# Loading the data
df = prep.get_prediction_data()

folds = KFold(n_splits=5, shuffle=True, random_state=32)

x_train = df[["deaths", "cases", "hospitalizations", "vaccination_coverage", "temp"]]
y_train = df["StringencyIndexForDisplay"]

scores_dt = cross_val_score(DecisionTreeClassifier(), x_train, y_train, cv=folds)
print("Accuracy decision tree:", mean(scores_dt))

scores_linear = cross_val_score(LinearRegression(), x_train, y_train, cv=folds)
print("Accuracy linear regression:", mean(scores_linear))

scores_logistic = cross_val_score(LogisticRegression(), x_train, y_train, cv=folds)
print("Accuracy logistic:", mean(scores_logistic))


random_forest_regressor = RandomForestRegressor(
    n_jobs=-1,
    n_estimators=12,
    min_samples_split=5,
    max_depth=21,
    max_features="log2",
    criterion="absolute_error",
)
