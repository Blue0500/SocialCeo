from sklearn import linear_model
import math
import numpy as np
import pickle
from matplotlib import pyplot as plt
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import PolynomialFeatures
from sklearn.linear_model import LinearRegression
from sklearn.linear_model import LassoCV
from sklearn.pipeline import make_pipeline
from sklearn.metrics import mean_squared_error, r2_score

TEST_PERCENT = .1

def init(tweet_data):
    item1, item2 = prepare_data(tweet_data)

    #print("Ridge Regression: " + str(ridge_regression(item1, item2)))
    #print("Lasso:            " + str(lasso(item1, item2)))
    #print("Least Squared:    " + str(least_squared(item1, item2))[1])
    #print("Polynomial:       " + str(poly(item1, item2))[1])

    poly_model = least_squared(item1, item2)
    return poly_model

def prepare_data(tweet_data):
    X_data = []
    Y_data = []

    for row in tweet_data:
        Y_data.append(row.pop(0))
        X_data.append(row)

    return (X_data, Y_data)

def ridge_regression(X_data, Y_data):
    X_train, X_test, y_train, y_test = train_test_split(X_data, Y_data, test_size=TEST_PERCENT)

    ridgereg = linear_model.Ridge (alpha = .5)
    ridgereg.fit (X_train, y_train)

    ridge_predict_y = ridgereg.predict(X_test)
    ridge_error = (mean_squared_error(y_test, ridge_predict_y) ** .5) / (max(y_train) - min(y_train))

    #print('Ridge Regression:', ridge_error)
    #print('Ridge Regression Coeff:', ridgereg.coef_)

    return ridge_error    

def lasso(X_data, Y_data):
    X_train, X_test, y_train, y_test = train_test_split(X_data, Y_data, test_size=TEST_PERCENT)

    lassoreg = linear_model.Lasso(alpha = 0.1)
    lassoreg.fit(X_train, y_train)

    lasso_predict_y = lassoreg.predict(X_test)
    lasso_error = (mean_squared_error(y_test, lasso_predict_y) ** .5) / (max(y_train) - min(y_train))

    # print('Lasso Error:', lasso_error)
    # print('Lassor Coef:', lassoreg.coef_)

    return lasso_error

def least_squared(X_data, Y_data):
    X_train, X_test, y_train, y_test = train_test_split(X_data, Y_data, test_size=TEST_PERCENT)

    reg = linear_model.LinearRegression()
    reg.fit(X_train, y_train)
    
    reg_predict_y = reg.predict(X_test)
    reg_error = (mean_squared_error(y_test, reg_predict_y) ** .5) / (max(y_train) - min(y_train))

    # print('Least Squares:', reg_error)
    # print('Least Squares Coeff', reg.coef_)

    return reg

def poly(X_data, Y_data):
    X_train, X_test, y_train, y_test = train_test_split(X_data, Y_data, test_size=TEST_PERCENT)

    lasso_eps = 0.0001
    lasso_nalpha=2
    lasso_iter=5000

    # Min and max degree of polynomials features to consider
    degree_min = 2
    degree_max = 8

    scores = []
    errors = []

    model = make_pipeline(
        PolynomialFeatures(2, interaction_only=False)
    )
    
    trans = model.fit_transform(X_train, y_train)
    model, error = least_squared(trans, y_train)

    return model

