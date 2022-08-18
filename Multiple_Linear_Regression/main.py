"""
    Created at: 2022-03-29
    Author: Erika Timo de Oliveira
    Description: Multiple Linear Regression between Nasdaq Assets 
"""

#from statistics import linear_regression
import numpy as np
import pandas as pd
from datetime import datetime 
from sklearn.linear_model import LinearRegression
import statsmodels.api as sm
import warnings
warnings.filterwarnings("ignore")
import pdb

from plot_functions import *

dataset = pd.read_excel('database.xlsx',sheet_name='data')
dataset['date'] = pd.to_datetime(dataset['date'], format='%Y-%m-%d')
classification = pd.read_excel('database.xlsx',sheet_name='companies')

pdb.set_trace()

assets_dict = {}

for status in classification['Status'].unique():
    assets_dict[status] = classification.query(f"Status == '{status}'")['Symbol'].to_list()

del(assets_dict['not_applicable']) 
del(assets_dict['digging_in']) 
del(assets_dict['buying_time']) 
del(assets_dict['scaling_back']) 

returns_dict = {}

for key in assets_dict.keys():
    returns_dict[key] = {}
    for asset in assets_dict[key]:
        returns_dict[key][asset] = round(np.log(dataset[asset]/dataset[asset].shift(1)),6).to_list()
        del(returns_dict[key][asset][0])

import json
with open ('./returns_dict.json', 'w') as file:
    json.dump(returns_dict, file, indent=4, ensure_ascii=True)





for key in returns_dict.keys():
    plot_prices_X_period(
        Y_date = dataset['date'][1:],
        kwargs = returns_dict[key], 
        name = f'historical_returns_{key}'
    )
