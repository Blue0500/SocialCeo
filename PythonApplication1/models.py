from sklearn import linear_model
import math
import numpy as np
from matplotlib import pyplot as plt
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import PolynomialFeatures
from sklearn.linear_model import LinearRegression
from sklearn.linear_model import LassoCV
from sklearn.pipeline import make_pipeline
from sklearn.metrics import mean_squared_error, r2_score




X_data = [[0, 0], [1, 1], [2, 2], [3, 3], [4, 4], [5, 5], [6, 6]]
Y_data = [0, 1, 4, 9, 16, 25, 36];

X_train, X_test, y_train, y_test = train_test_split(X_data, Y_data,test_size=0.2)

reg = linear_model.LinearRegression()

reg.fit (X_train, y_train)

reg.coef_

reg_predict_y = reg.predict(X_test)

reg_error = mean_squared_error(y_test, reg_predict_y)

print('Least Squares:', reg_error)


ridgereg = linear_model.Ridge (alpha = .5)
ridgereg.fit (X_train, y_train)


ridgereg.coef_

ridgereg.intercept_

ridge_predict_y = ridgereg.predict(X_test)

ridge_error = mean_squared_error(y_test, ridge_predict_y)

print('Ridge Regression:', ridge_error)

lassoreg = linear_model.Lasso(alpha = 0.1)
lassoreg.fit(X_train, y_train)

lasso_predict_y = lassoreg.predict(X_test)

lasso_error = mean_squared_error(y_test, lasso_predict_y)

print('Lasso Error:', lasso_error)


# Alpha (regularization strength) of LASSO regression
lasso_eps = 0.0001
lasso_nalpha=20
lasso_iter=5000

# Min and max degree of polynomials features to consider
degree_min = 2
degree_max = 8


scores = []
errors = []
# Make a pipeline model with polynomial transformation and LASSO regression with cross-validation, run it for increasing degree of polynomial (complexity of the model)

for degree in range(degree_min,degree_max+1):
    model = make_pipeline(PolynomialFeatures(degree, interaction_only=False), LassoCV(eps=lasso_eps,n_alphas=lasso_nalpha,max_iter=lasso_iter,
    normalize=True,cv=5))
    model.fit(X_train,y_train)
    test_pred = np.array(model.predict(X_test))
    RMSE=np.sqrt(np.sum(np.square(test_pred-y_test)))
    test_score = model.score(X_test,y_test)
    scores.append(test_score)
    errors.append(RMSE)

print(scores)
print(errors)

#plt.plot([2, 3, 4, 5, 6, 7, 8], scores)
#plt.plot([2, 3, 4, 5, 6, 7, 8], errors)
#plt.show()
