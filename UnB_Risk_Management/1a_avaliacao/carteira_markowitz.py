"""
    Created at: 2022-02-05
    Author: Erika Timo de Oliveira
    Description: Analysis of Banking Sector Assets through Markowitz's Portfolio Theory
"""

# Dúvidas
# Desvio padrão populacional ou amostral? Grau de liberdade na fórmula do desvio padrão (T-1)
# Média do retorno é a média simples mesmo do retorno contínuo já calculado?
# Entender melhor o fator de decaimento λ do método EWMA
# Como ficam os dividendos?

from audioop import avg
from yahooquery import Ticker
import numpy as np
import pandas as pd
from datetime import datetime
from pandas.tseries.offsets import BDay
from pandas_datareader import data as pdr
import seaborn as sns


stock_portfolio = {
    'stocks': ['BTG PACTUAL','ITAÚ UNIBANCO'],
    'tickers': ['BPAC11','ITUB4'],
    'tickers_yf': ['BPAC11.SA', 'ITUB4.SA']# Code used on Yahoo Finance
}


stock_portfolio = {
    'btg_pactual': {
        'name': 'BTG PACTUAL',
        'ticker': 'BPAC11',
        'ticker_yf': 'BPAC11.SA' # Code used on Yahoo Finance
    },
    'itau': {
        'name': 'ITAÚ UNIBANCO',
        'ticker': 'ITUB4',
        'ticker_yf': 'ITUB4.SA'
    },
    'santander': {
        'name': 'SANTANDER',
        'ticker': 'SANB11',
        'ticker_yf': 'SANB11.SA'
    },
    'banco_do_brasil': {
        'name': 'BANCO DO BRASIL',
        'ticker': 'BBAS3',
        'ticker_yf': 'BBAS3.SA'
    },
    'bradesco': {
        'name': 'BRADESCO',
        'ticker': 'BBDC4',
        'ticker_yf': 'BBDC4.SA'
    }
}

end_date = datetime.date(datetime.today() - BDay(1))
start_date = datetime.date(end_date - BDay(40))

#0 Plot de ativos 


for stock in stock_portfolio:
    stock_portfolio[stock]['info_yq'] = Ticker(stock_portfolio[stock]['ticker_yf'])
    stock_portfolio[stock]['history'] = stock_portfolio[stock]['info_yq'].history(start=start_date, end=end_date)

# A) Calculate the daily continuous return Ln(Pt/Pt-1) for each ticket
for stock in stock_portfolio:
    stock_df = stock_portfolio[stock]['history']
    stock_df['discreet_return'] = round(stock_df['close']/stock_df['close'].shift(1) -1,6)
    stock_df['continuous_return'] = round(np.log(stock_df['close']/stock_df['close'].shift(1)),6)


# B) Calculate the average return and risk (standard deviation) for each ticket
for stock in stock_portfolio:
    stock_df = stock_portfolio[stock]['history']
    stock_portfolio[stock]['avg_return'] = np.mean(stock_df['continuous_return'])
    stock_portfolio[stock]['std_deviation'] = np.std(stock_df['continuous_return'], ddof=1) # Delta Degrees of Freedom =1


#C) Calculate the correlation matrix  of the return of the assets in the period
correlation_df = pd.DataFrame()
labels = []
for stock in stock_portfolio:
    return_df_single = pd.DataFrame(stock_portfolio[stock]['history']['continuous_return'].droplevel(0).drop(start_date))
    correlation_df = pd.concat([correlation_df, return_df_single], ignore_index=False, axis=1)
    labels.append(stock)
correlation_df.columns = labels
correlation_results = correlation_df.corr()

# Seaborn
# Themes: darkgrid, whitegrid, dark, white, ticks

sns.set_theme(style="whitegrid") 
sns.color_palette("ch:s=.25,rot=-.25", as_cmap=True)
sns.palplot(sns.color_palette("Blues"))

plot = sns.heatmap(correlation_results, annot = True, ) #, fmt=".1f", linewidths=.6)

plot.figure.savefig('Matriz de Correlação.png')  

print(stock_portfolio)




