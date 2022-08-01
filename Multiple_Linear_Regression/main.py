"""
    Created at: 2022-03-29
    Author: Erika Timo de Oliveira
    Description: Multiple Linear Regression between Nasdaq Assets 
"""

import numpy as np
import pandas as pd
import datetime 
from sklearn.linear_model import LinearRegression
import statsmodels.api as sm
import pdb

from plot_functions import *

# Janela de estimação (150 dias): 15/06/21 a 20/01/22
# Janela do evento (25 dias): 20/01/22 a 04/04/22
# Evento: 24/02/22

dataset = pd.read_excel('database.xlsx',sheet_name='data')
dataset['date'] = pd.to_datetime(dataset['date'], format='%Y-%m-%d')
dataset = dataset.query("date >= '2021-06-15' and date < '2022-01-20'")

dataset.info()

# Independent variable is the same for all assets
X = round(np.log(dataset['^NDX']/dataset['^NDX'].shift(1)),6)
X = X.reset_index(drop=True)
del(X[0])
X_sm = sm.add_constant(X)

# Loop beginning

asset = 'AAPL'

plot_price_X_period(
    X_asset = dataset[asset], 
    X_Nasdaq = dataset['^NDX'], 
    Y_date = dataset['date'], 
    asset = asset
)

Y = round(np.log(dataset[asset]/dataset[asset].shift(1)),6)
Y = Y.reset_index(drop=True)
del(Y[0])

plot_return_X_period(
    X_asset = X, 
    X_Nasdaq = Y, 
    Y_date = dataset['date'][1:], 
    asset = asset
)

plot_nasdaq_X_asset(
    Y_asset = X, 
    X_Nasdaq = Y, 
    asset = asset
)

results = sm.OLS(Y, X_sm).fit()

rsquared = results.rsquared
rsquared_adj = results.rsquared_adj
beta_const = results.params[0]
NDX_const =  results.params[1]
f_pvalue = results.f_pvalue
t_pvalue = results.pvalues[1]
resid_sum = sum(results.resid)

plot_residuals_dist(
    res = results.resid,
    asset = asset
)

print(results.summary())