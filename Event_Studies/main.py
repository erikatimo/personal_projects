"""
    Created at: 2022-03-29
    Author: Erika Timo de Oliveira
    Description: Multiple Linear Regression between Nasdaq Assets 
"""

import numpy as np
import pandas as pd
from datetime import datetime 
from sklearn.linear_model import LinearRegression
import statsmodels.api as sm
import warnings
warnings.filterwarnings("ignore")
import pdb

from plot_functions import *

event_date = datetime(2022,2,24)
estimation_window = 150
event_window = 25

dataset = pd.read_excel('database.xlsx',sheet_name='data')
dataset['date'] = pd.to_datetime(dataset['date'], format='%Y-%m-%d')

event_window_start_idx = dataset[dataset['date'] == datetime.strftime(event_date, '%Y-%m-%d')].index[0] - 25 
event_window_end_idx = dataset[dataset['date'] == datetime.strftime(event_date, '%Y-%m-%d')].index[0] + 26 
estimation_window_end_idx = dataset[dataset['date'] == datetime.strftime(event_date, '%Y-%m-%d')].index[0] - 25  
estimation_window_start_idx = dataset[dataset['date'] == datetime.strftime(event_date, '%Y-%m-%d')].index[0] - 25 - 1 - 150 

window_set = dataset[event_window_start_idx:event_window_end_idx]
estimation_set = dataset[estimation_window_start_idx:estimation_window_end_idx]

estimation_set.info()

# Independent variable is the same for all assets
X = round(np.log(estimation_set['^NDX']/estimation_set['^NDX'].shift(1)),6)
X = X.reset_index(drop=True)
del(X[0])
X_sm = sm.add_constant(X)

assets = dataset.columns[3:]

statistics_info = [
    'asset', 
    'rsquared', 
    'rsquared_adj', 
    'beta_const', 
    'NDX_const', 
    'f_pvalue', 
    't_pvalue', 
    'resid_sum'
]

results_df = pd.DataFrame(columns=statistics_info)

for asset in assets:

    plot_price_X_period(
        X_asset = estimation_set[asset], 
        X_Nasdaq = estimation_set['^NDX'], 
        Y_date = estimation_set['date'], 
        asset = asset
    )

    Y = round(np.log(estimation_set[asset]/estimation_set[asset].shift(1)),6)
    Y = Y.reset_index(drop=True)
    del(Y[0])

    plot_return_X_period(
        X_asset = X, 
        X_Nasdaq = Y, 
        Y_date = estimation_set['date'][1:], 
        asset = asset
    )

    plot_nasdaq_X_asset(
        Y_asset = X, 
        X_Nasdaq = Y, 
        asset = asset
    )

    results = sm.OLS(Y, X_sm).fit()

    outcome = {
        'asset': asset,
        'rsquared': results.rsquared,
        'rsquared_adj': results.rsquared_adj,
        'beta_const': results.params[0],
        'NDX_const': results.params[1],
        'f_pvalue': results.f_pvalue,
        't_pvalue': results.pvalues[1],
        'resid_sum': sum(results.resid)
    }

    results_df = results_df.append(outcome, ignore_index = True)

    plot_residuals_dist(
        res = results.resid,
        asset = asset
    )

    print(results.summary())

print('\n Concatenated Results \n')
print(results_df)

results_df.to_excel('results_df.xlsx')

