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
from sklearn.ensemble import RandomForestClassifier
from sklearn.tree import DecisionTreeClassifier

import preprocessing_predictions as prep

# Loading the data
df = prep.get_prediction_data()

folds = KFold()

x_train = df[["deaths", "cases", "hospitalizations", "vaccination_coverage", "temp"]]
y_train = df["StringencyIndexForDisplay"]

scores_dt = cross_val_score(DecisionTreeClassifier(), x_train, y_train, cv=folds)
print("Accuracy decision tree:", mean(scores_dt))

scores_linear = cross_val_score(LinearRegression(), x_train, y_train, cv=folds)
print("Accuracy linear regression:", mean(scores_linear))

scores_logistic = cross_val_score(LogisticRegression(), x_train, y_train, cv=folds)
print("Accuracy logistic:", mean(scores_logistic))

scores_rf = cross_val_score(RandomForestClassifier(), x_train, y_train, cv=folds)
print("Accuracy random forest:", mean(scores_rf))
