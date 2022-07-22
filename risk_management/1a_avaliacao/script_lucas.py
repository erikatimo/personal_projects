import pandas as pd
import datetime as dt
#import yfinance as yf
#import pandas_datareader.data as pdr
import matplotlib.pyplot as plt
#import seaborn as sns
#from os import listdir
#from os.path import isfile, join
import numpy as np
#import statsmodels.api as sm
#import plotly.offline as py
#from plotly.offline import iplot, init_notebook_mode
#import plotly.graph_objs as go
#from scipy import stats
#import scipy.optimize as sco
#from plotly import __version__
#from plotly.offline import download_plotlyjs, init_notebook_mode, plot, iplot
#import cufflinks as cf
#from scipy.stats.mstats import gmean


#############################################################################################################
# Import dos ativos
ativos = pd.read_excel("ativos.xlsx")
ativos.set_index('DATA', inplace=True)
asset_returns = ativos.pct_change().dropna()
asset_returns.drop(['DI'], axis = 'columns', inplace = True)
print(asset_returns.head())

# Retorno e Volatilidade
vol = asset_returns.std()*np.sqrt(252)
mean_returns = (asset_returns.mean() + 1)**252 - 1
print(vol,'\n')
print(mean_returns)

# Cálculo da matriz covariância
cov_matrix = asset_returns.cov()
print(cov_matrix)
num_portfolios = 25000
risk_free_rate = 0.02