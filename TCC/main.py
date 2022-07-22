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

"""
    Functions
"""

"""
    Execution
"""

start_date = datetime.date(2022,1,1) 
end_date = datetime.date(2022,5,1)

# Inicialmente vamos puxar os dados históricos da Nasdaq
# ^NDX: Nasdaq 100 / ^IXIC: Nasdaq Composite
nasdaq_100_index = Ticker('^NDX')
nasdaq_100_history_df = nasdaq_100_index.history(start=start_date, end=end_date)
nasdaq_100_history_df.reset_index(level=[0,1], inplace=True)
nasdaq_100_history_df['period'] = nasdaq_100_history_df['date'].apply(lambda x: x.strftime('%Y-%m'))

# plot Nasdaq historical values
plt.style.use('seaborn')
plt.figure(figsize=(10, 7))
data = nasdaq_100_history_df
plt.plot(data['date'], data['close'], color='#404788FF', label='Nasdaq-100', linestyle='solid')
plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%Y-%b'))
plt.legend(labelspacing=0.8)
plt.title("NASDAQ-100 - Histórico")
plt.xlabel('Período')
plt.ylabel('Fechamento')
plt.savefig('./plots/Nasdaq-100_historical.png')

# Empresas que encerraram atividades na Russia e fazem parte do Nasdaq 100
# Withdrawal: ABNB, ADSK, AMD, ATVI, BKNG, EBAY, FTNT, NFLX
# Suspension: AAPL, ADBE, ADI, ADP, AMZN, ANSS, COST, CSCO, FB, GOOG, GOOGL, HON, INTC, INTU, MRVL, MU, NVDA, PYPL, QCOM, SBUX, TEAM

tickers = ['ABNB', 'ADSK', 'AMD', 'ATVI', 'BKNG', 'EBAY', 'FTNT', 'NFLX']
portfolio = Ticker(tickers)
portfolio_history_df = portfolio.history(start=start_date, end=end_date)
portfolio_history_df.reset_index(level=[0,1], inplace=True)
portfolio_history_df['period'] = portfolio_history_df['date'].apply(lambda x: x.strftime('%Y-%m'))

# plot Portfolio historical prices
viridis_palet = ['#440154FF', '#481567FF', '#482677FF', '#453781FF', '#404788FF', '#39568CFF', '#33638DFF', '#2D708EFF', '#287D8EFF', '#238A8DFF', '#1F968BFF', '#20A387FF', '#29AF7FFF', '#3CBB75FF', '#55C667FF', '#73D055FF', '#95D840FF', '#B8DE29FF', '#DCE319FF', '#FDE725FF']
palet_position = 0
plt.style.use('seaborn')
plt.figure(figsize=(10, 7))
for ticker in tickers:
    data = portfolio_history_df[portfolio_history_df['symbol']==ticker]
    plt.plot(data['date'], data['close'], color=viridis_palet[palet_position], label=ticker, linestyle='solid')
    if palet_position == 19:
        palet_position = 0
    else:
        palet_position += 1
plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%Y'))
plt.legend(labelspacing=0.8)
plt.title("Empresas selecionadas - Histórico")
plt.xlabel('Período')
plt.ylabel('Fechamento')
plt.savefig('./plots/Portfolio_historical.png')

# Agora vamos calcular os retornos do portfolio de empresas
portfolio_return_df = pd.DataFrame()
for ticker in tickers:
    df = portfolio_history_df[portfolio_history_df['symbol']==ticker][['symbol', 'date', 'close']]
    df['discreet_return'] = round(df['close']/df['close'].shift(1) -1,6)
    df['continuous_return'] = round(np.log(df['close']/df['close'].shift(1)),6)
    df.drop(index=df.index[0], inplace=True) # First row does not have calculated return
    portfolio_return_df = portfolio_return_df.append(df, ignore_index=True)

# E os retornos da Nasdaq
nasdaq_return_df = pd.DataFrame()
for ticker in tickers:
    df = portfolio_history_df[portfolio_history_df['symbol']==ticker][['symbol', 'date', 'close']]
    df['discreet_return'] = round(df['close']/df['close'].shift(1) -1,6)
    df['continuous_return'] = round(np.log(df['close']/df['close'].shift(1)),6)
    df.drop(index=df.index[0], inplace=True) # First row does not have calculated return
    nasdaq_return_df = nasdaq_return_df.append(df, ignore_index=True)

# plot return Nasdaq
plt.clf()
plt.figure(figsize=(10, 7))
fig, axs = plt.subplots(1, 2, sharex=False, sharey=True)
axs[0].plot(nasdaq_return_df['date'], nasdaq_return_df['continuous_return'], color='#B8DE29FF', label=ticker, linestyle='solid')
axs[1] = sns.distplot(nasdaq_return_df['continuous_return'], kde=True, color='#B8DE29FF', vertical=True)
axs[0].xaxis.set_major_formatter(mdates.DateFormatter('%Y-%b'))
axs[0].yaxis.set_major_formatter(mtick.PercentFormatter())
fig.legend(labelspacing=0.8)
fig.suptitle("Retorno Contínuo - Nasdaq 100 index")
axs[0].set_xlabel('Period')
axs[0].set_ylabel('Return')
fig.autofmt_xdate()
fig.savefig('./plots/nasdaq_return'+'.png')



# Linear Regression
#model = LinearRegression()
#X = bovespa_return_df[['continuous_return']]
#Y = simulated_portfolio_return_df[['continuous_return']]
#
#plt.figure(figsize=(10, 7))
#sns.regplot(x=X, y=Y)
#plt.title("Linear Regression")
#plt.xlabel('IBOVESPA Return')
#plt.ylabel('Portfolio Return')
#plt.savefig('linear_regression.png')
#
#model.fit(X, Y)



