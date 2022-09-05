"""
    Created at: 2022-03-29
    Author: Erika Timo de Oliveira
    Description: Event-study Analysis
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

"""
    Parameters
"""

event_date = datetime(2022,2,24)
estimation_window = 30
event_window_left = 5
event_window_right = 10
market_index = '^GSPC' #'^NDX'
status = 'buying_time' # 'withdrawal' 'suspension' 'buying_time' 'scaling_back' 'digging_in' 

"""
    Data
"""

# Prices (dataset) and returns (returns) dataframes
dataset = pd.read_excel(f'data_{status}.xlsx')
assets_list = list(set(dataset.columns) - set(['date', '^NDX']))
returns = pd.DataFrame(columns=assets_list) 
for asset in assets_list:
    returns[asset] = round(np.log(dataset[asset]/dataset[asset].shift(1)),6)
returns['date'] = dataset['date']
returns['date'] = pd.to_datetime(returns['date'], format='%Y-%m-%d')
returns.drop(returns.index[[0]])

# Inserting TAU index
event_index = returns[returns['date'] == datetime.strftime(event_date, '%Y-%m-%d')].index[0] 
returns['tau'] = returns.index - event_index
returns = returns.set_index('tau')
dataset['tau'] = dataset.index - event_index
dataset = dataset.set_index('tau')

# Separating dataframe in 2 parts: window  and estimation sets
window_set = dataset[dataset.index.isin(range(-1 * event_window_left, 1 + event_window_right))]
window_returns = returns[returns.index.isin(range(-1 * event_window_left, 1 + event_window_right))]
estimation_set = dataset[dataset.index.isin(range(-1 * (estimation_window + event_window_left), -1 * event_window_left))]
estimation_returns = returns[returns.index.isin(range(-1 * (estimation_window + event_window_left), -1 * event_window_left))]

def significance (t_stat, coef):
    if t_stat <= 0.1 and t_stat > 0.05:
        return str(round(coef, 4)) + '*'
    elif t_stat <= 0.05 and t_stat > 0.01:
        return str(round(coef, 4)) + '**'
    elif t_stat <= 0.05 and t_stat > 0.01:
        return str(round(coef, 4)) + '***'
    else:
        return str(round(coef, 4))

# Independent variable is the same for all assets
X = estimation_returns[market_index]
X_sm = sm.add_constant(X)

statistics_info = [
    'asset', 
    'rsquared', 
    'rsquared_adj', 
    'alpha', 
    'beta', 
    'f_pvalue', 
    't_pvalue', 
    't_pvalue_analysis',
    'resid_sum'
]

results_df = pd.DataFrame(columns=statistics_info)

cars_info = [
    'asset', 
    '[-5, -1]',
    '[0]',
    '[1, 5]',
    '[0, 5]',
    '[1, 10]',
    '[0, 10]',
    '[-5, 10]'
]

cars_df = pd.DataFrame(columns=cars_info)

for asset in assets_list:

    plot_price_X_period(
        X_asset = estimation_set[asset], 
        X_Market = estimation_set[market_index], 
        Y_date = estimation_set['date'], 
        asset = asset
    )

    Y = estimation_returns[asset]

    plot_return_X_period(
        X_asset = X, 
        X_Market = Y, 
        Y_date = estimation_returns['date'], 
        asset = asset
    )

    plot_market_X_asset(
        Y_asset = X, 
        X_Market = Y, 
        asset = asset
    )

    model = sm.OLS(Y, X_sm)
    results = model.fit()

    outcome = {
        'asset': asset,
        'rsquared': results.rsquared,
        'rsquared_adj': results.rsquared_adj,
        'alpha': results.params[0],
        'beta': results.params[1],
        'f_pvalue': results.f_pvalue,
        't_pvalue': results.pvalues[1],
        't_pvalue_analysis': "", #if results.pvalues[1] <= 0.05: '**'
        'resid_sum': sum(results.resid)
    }

    results_df = results_df.append(outcome, ignore_index = True)

    plot_residuals_dist(
        res = results.resid,
        asset = asset
    )

    print(results.summary())

    X_window = window_returns[market_index]
    Y_window = window_returns[asset]

    #results.get_prediction(np.array([1, X_window[1]]) ).summary_frame(alpha=0.05)['mean'][0]
    Y_predict = outcome['alpha'] + outcome['beta'] * X_window
    
    Y_diff = Y_window - Y_predict

    outcome_cars = {
        'asset': asset, 
        '[-5, -1]': significance(results.pvalues[1], sum(Y_diff[Y_diff.index.isin(range(-5, 0))])),
        '[0]': significance(results.pvalues[1], Y_diff[Y_diff.index == 0][0]),
        '[1, 5]': significance(results.pvalues[1], sum(Y_diff[Y_diff.index.isin(range(1, 6))])),
        '[0, 5]': significance(results.pvalues[1], sum(Y_diff[Y_diff.index.isin(range(0, 6))])),
        '[1, 10]': significance(results.pvalues[1], sum(Y_diff[Y_diff.index.isin(range(1, 11))])),
        '[0, 10]': significance(results.pvalues[1], sum(Y_diff[Y_diff.index.isin(range(0, 11))])),
        '[-5, 10]': significance(results.pvalues[1], sum(Y_diff[Y_diff.index.isin(range(-5, 11))]))
    }
    
    cars_df = cars_df.append(outcome_cars, ignore_index = True)

    #pdb.set_trace()



print('\n Concatenated Results \n')
print(results_df)

writer = pd.ExcelWriter(f'results_{status}.xlsx', engine='xlsxwriter')
results_df.to_excel(writer, sheet_name='regression_results')
window_set.to_excel(writer, sheet_name='window_set')
window_returns.to_excel(writer, sheet_name='window_returns')
estimation_set.to_excel(writer, sheet_name='estimation_set')
estimation_returns.to_excel(writer, sheet_name='estimation_returns')
cars_df.to_excel(writer, sheet_name='cars')
writer.save()

print(cars_df.to_latex(index=False))
