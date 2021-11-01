import pandas as pd
import numpy as np
from statistics import mean
import random

from sklearn.feature_extraction.text import CountVectorizer
from sklearn.model_selection import (
    train_test_split,
    cross_val_score,
    KFold,
)
from sklearn.neighbors import KNeighborsRegressor, RadiusNeighborsRegressor
from sklearn.linear_model import (
    LinearRegression,
    SGDRegressor,
    HuberRegressor,
    Perceptron,
    BayesianRidge,
)
from sklearn.model_selection import GridSearchCV
from sklearn.metrics import confusion_matrix, classification_report
from sklearn.preprocessing import LabelEncoder
from sklearn.ensemble import RandomForestRegressor, AdaBoostRegressor
from sklearn.tree import DecisionTreeRegressor
from sklearn.gaussian_process import GaussianProcessRegressor
from sklearn.cross_decomposition import PLSRegression
from sklearn.neural_network import MLPRegressor
from sklearn.isotonic import IsotonicRegression

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

regressors = [
    KNeighborsRegressor(),
    RadiusNeighborsRegressor(),
    LinearRegression(),
    SGDRegressor(),
    HuberRegressor(),
    Perceptron(),
    BayesianRidge(),
    IsotonicRegression(),
    DecisionTreeRegressor(),
    GaussianProcessRegressor(),
    PLSRegression(),
    MLPRegressor(),
    RandomForestRegressor(),
    AdaBoostRegressor(),
]
