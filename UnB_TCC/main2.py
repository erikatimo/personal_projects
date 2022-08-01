"""
    Created at: 2022-03-29
    Author: Erika Timo de Oliveira
    Description: 
"""

# source
from yahooquery import Ticker
# data transformation
import numpy as np
import pandas as pd
import datetime 

from sklearn.linear_model import LinearRegression

# plots
import seaborn as sns
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import matplotlib.ticker as mtick

# Ignorar avisos
import warnings
warnings.filterwarnings("ignore")
import pdb


start_date = datetime.date(2021,1,1) 
end_date = datetime.date(2022,5,15)

companies_df = pd.read_excel('companies.xlsx')

assets_list = list(companies_df[companies_df.Status.isin(['suspension', 'withdrawal'])]['Symbol'].reset_index(drop=True))
assets_list.append('^NDX')

wallet = Ticker(assets_list)
history_df = wallet.history(start=start_date, end=end_date)
history_df.reset_index(level=[0,1], inplace=True)

history_df = pd.pivot_table(history_df[['symbol', 'date', 'close']], values = 'close', index=['date'], columns = 'symbol').reset_index()
history_df['period'] = history_df['date'].apply(lambda x: x.strftime('%Y-%m'))

history_df.to_csv('wallet.csv')

print(history_df.head())