"""
    Created at: 2022-02-05
    Author: Erika Timo de Oliveira
    Description: Analysis of Banking Sector Assets through Markowitz's Portfolio Theory
"""
# source
from cProfile import label
from yahooquery import Ticker
# functions
import plot_functions as pl
# data transformation
import numpy as np
import pandas as pd
import datetime 
from pandas.tseries.offsets import BDay
# plots
import seaborn as sns
import matplotlib.ticker as ticker
import matplotlib.pyplot as plt
import matplotlib.dates as mdates

# selected portfolio according with Yahoo data names 
tickers = ['BPAC11', 'ITUB4', 'SANB11', 'BBAS3', 'BBDC4']

# selected risk free rate
risk_free_rate = 0.02

# selected period 
business_days_range = 200 
end_date = datetime.date(2022,3,1) #datetime.datetime.date(datetime.datetime.today() - BDay(1))  
start_date = datetime.date(2022,1,1) #datetime.datetime.date(end_date - BDay(business_days_range)) 

# get historical prices 
portfolio = Ticker([ticker + '.SA' for ticker in tickers])
portfolio_history_df = portfolio.history(start=start_date, end=end_date)
portfolio_history_df.reset_index(level=[0,1], inplace=True)
portfolio_history_df['period'] = portfolio_history_df['date'].apply(lambda x: x.strftime('%Y-%m'))
portfolio_history_df['ticker'] = portfolio_history_df['symbol'].apply(lambda x: x.replace('.SA', ''))

print("Portfolio History")
print(portfolio_history_df.head())
print(type(portfolio_history_df['date'][0]))
print("\n\n")

# plot historical prices
viridis_palet = ['#440154FF', '#481567FF', '#482677FF', '#453781FF', '#404788FF', '#39568CFF', '#33638DFF', '#2D708EFF', '#287D8EFF', '#238A8DFF', '#1F968BFF', '#20A387FF', '#29AF7FFF', '#3CBB75FF', '#55C667FF', '#73D055FF', '#95D840FF', '#B8DE29FF', '#DCE319FF', '#FDE725FF']
palet_position = 0
plt.style.use('seaborn')
plt.figure(figsize=(10, 7))
for ticker in tickers:
    data = portfolio_history_df[portfolio_history_df['ticker']==ticker]
    plt.plot(data['date'], data['close'], color=viridis_palet[palet_position], label=ticker, linestyle='solid')
    palet_position +=int(round(4.5,0))
plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%Y'))
plt.legend(labelspacing=0.8)
plt.title("Assets History")
plt.xlabel('Period')
plt.ylabel('Closing Price')
plt.savefig('Assets History.png')

# calculate return variations
portfolio_return_df = pd.DataFrame()
for ticker in pd.unique(portfolio_history_df['ticker']):
    df = portfolio_history_df[portfolio_history_df['ticker']==ticker][['date', 'close', 'ticker']]
    df['discreet_return'] = round(df['close']/df['close'].shift(1) -1,6)
    df['continuous_return'] = round(np.log(df['close']/df['close'].shift(1)),6)
    df.drop(index=df.index[0], inplace=True) # First row does not have calculated return
    portfolio_return_df = portfolio_return_df.append(df, ignore_index=True)
print("Portfolio Returns")
print(portfolio_return_df.head())
print("\n\n")

# plot return
plt.clf()
plt.figure(figsize=(10, 7))
palet_position = 0
fig, axs = plt.subplots(1, 2, sharex=False, sharey=True)
for ticker in tickers:
    data = portfolio_return_df[portfolio_return_df['ticker']==ticker]
    axs[0].plot(data['date'], data['continuous_return'], color=viridis_palet[palet_position], label=ticker, linestyle='solid')
    axs[1] = sns.distplot(data['continuous_return'], kde=True, color=viridis_palet[palet_position], vertical=True)
    #axs[1].hist(data['continuous_return'], color=viridis_palet[palet_position], label=ticker)
    palet_position +=int(round(4.5,0))
axs[0].xaxis.set_major_formatter(mdates.DateFormatter('%Y-%b'))
fig.legend(labelspacing=0.8)
fig.suptitle("Continuous Assets Return")
axs[0].set_xlabel('Period')
axs[0].set_ylabel('Return')
fig.autofmt_xdate()
fig.savefig('Continuous Assets Return.png')

########################
# Portfolio Performance 
########################

portfolio_statistics_df = pd.DataFrame(pd.unique(portfolio_history_df['ticker']))
portfolio_statistics_df.columns=['ticker']

avg_return_df = pd.DataFrame()
avg_return_df['avg_return'] = portfolio_return_df.groupby('ticker')['continuous_return'].mean()
avg_return_df.reset_index(inplace=True)
portfolio_statistics_df = portfolio_statistics_df.merge(avg_return_df, how='left', on='ticker')

std_deviation_df = pd.DataFrame()
std_deviation_df['std_deviation'] = portfolio_return_df.groupby('ticker')['continuous_return'].std()
std_deviation_df.reset_index(inplace=True)
portfolio_statistics_df = portfolio_statistics_df.merge(std_deviation_df, how='left', on='ticker')
print("Portfolio Statistics")
print(portfolio_statistics_df)
print("\n\n")

correlation_df = pd.pivot_table(portfolio_return_df, values='continuous_return',
                                index='date', columns='ticker').corr()
print("Portfolio Correlation")
print(correlation_df)
print("\n\n")

# Plot Correlation
plt.figure(figsize=(10, 7))
mask = np.triu(np.ones_like(correlation_df, dtype=np.bool))
sns.heatmap(correlation_df, mask=mask, vmin=-1, vmax=1, annot=True, cmap='viridis')
plt.title("Assets Correlation")
plt.savefig('Assets Correlation.png')

covariation_df = pd.pivot_table(portfolio_return_df, values='continuous_return',
                                index='date', columns='ticker').cov()
print("Portfolio Covariation")
print(covariation_df)
print("\n\n")

# Plot Covariation
plt.figure(figsize=(10, 7))
mask = np.triu(np.ones_like(covariation_df, dtype=np.bool))
sns.heatmap(np.sqrt(covariation_df), vmin=-1, vmax=1, annot=True, cmap='viridis')
plt.title("Assets Covariation")
plt.savefig('Assets Covariation.png')

print(min(covariation_df.min()))


# Calcular mãximo drawdown ; downside risk

def random_weights(assets):
    """
    [Summary]:
        This function calculates weights to be used in the distribution of assets in the portfolio
    [Args]:
        - n: int required number of weights 
    [Returns]:
        - weights: list with n random weights [w1, w2,..., wn], such that the sum of these weights is 1
    """
    n = len(assets)
    random_numbers = np.random.random(n)
    weights = random_numbers/np.sum(random_numbers)
    
    return pd.DataFrame(weights, index=assets, columns=['weight'])

def portfolio_performance_internet(weights, mean_returns, cov_matrix, n_sample):
    """
    [Summary]:
        This function calculates the return and the risk (deviation) of the portfolio
    [Args]:
        - weights: list containing the weight of each asset in the portfolio, meaning the percentage attribuited to the stocks
        - mean_returns: list containing the historical returns of the stocks
        - cov_matrix: matrix containing the covariance rates between the stocks
        - n_sample: int number of samples (periods) used to calculate the mean returns 
    [Returns]:
        - portfolio_return: float, weighted sum of assets mean returns 
        - portfolio_deviation: float, portfolio volatility, according to the formula proposed by Markowits
    """
    
    portfolio_return = np.sum(mean_returns * weights) * n_sample
    portfolio_deviation = np.sqrt(np.dot(weights.T, np.dot(cov_matrix, weights))) * np.sqrt(n_sample)
    
    return portfolio_return, portfolio_deviation


def portfolio_performance(weights, mean_returns, cov_matrix, tickers):
    """
    [Summary]:
        This function calculates the return and the risk (deviation) of the portfolio
    [Args]:
        - weights: list containing the weight of each asset in the portfolio, meaning the percentage attribuited to the stocks
        - mean_returns: list containing the historical returns of the stocks
        - cov_matrix: dataframe containing the covariance rates between the stocks
        - n_sample: int number of samples (periods) used to calculate the mean returns 
    [Returns]:
        - portfolio_return: float, weighted sum of assets mean returns 
        - portfolio_deviation: float, portfolio volatility, according to the formula proposed by Markowits
    """

    portfolio_deviation = 0
    for i in tickers:
        for j in tickers:
            portfolio_deviation += weights['weight'][i]*weights['weight'][j]*cov_matrix[i][j]
    portfolio_deviation = np.sqrt(portfolio_deviation)

    weights.reset_index(inplace=True)
    df = mean_returns.merge(weights, how='left', left_on='ticker', right_on='index')
    df['weighted_avg_return'] = df['avg_return']*df['weight']
    portfolio_return = np.sum(df['weighted_avg_return']) 

    return portfolio_return, portfolio_deviation


# Ampliando a simulação para 25000 portfolios
def random_portfolio(n_simulations, assets, mean_returns, cov_matrix, risk_free_rate):
    """
    [Summary]:
        This function applies portfolio_performance for n portfolios, using random weights 
    [Args]:
        - n_simulations: number of simulations to be applied
    [Returns]:
        -
    """

    column_names = ['weight_' + asset for asset in assets] + ['return', 'deviation', 'sharpie']
    results_df = pd.DataFrame(columns=column_names)
    
    for i in range(n_simulations):
        weights = random_weights(assets)
        portfolio_return, portfolio_deviation = portfolio_performance(weights, mean_returns, cov_matrix, tickers=assets)
        sharpie_index = (portfolio_return-risk_free_rate)/portfolio_deviation
        
        results_df.loc[i] = weights.transpose().values.tolist()[1] + [portfolio_return, portfolio_deviation, sharpie_index]
    
    return results_df


result = random_portfolio(5000, tickers, portfolio_statistics_df[['ticker', 'avg_return']], covariation_df, risk_free_rate=0)
print(result)

# Maximum Sharpie Index
portfolio_max_sharpie = result.loc[result['sharpie'].idxmax()]
max_sharpie_coordinates = [portfolio_max_sharpie.loc['deviation'], portfolio_max_sharpie.loc['return']]

# Maximum Return 
portfolio_max_return = result.loc[result['return'].idxmax()]
max_return_coordinates = [portfolio_max_return.loc['deviation'], portfolio_max_return.loc['return']]

# Minimum Volatility
portfolio_min_vol = result.loc[result['deviation'].idxmin()]
min_vol_coordinates = [portfolio_min_vol.loc['deviation'], portfolio_min_vol.loc['return']]

Best_portfolios = pd.DataFrame(columns=['Method']+result.columns.tolist())
Best_portfolios.loc[0] = ['Maximum Sharpie'] + portfolio_max_sharpie.values.tolist()
Best_portfolios.loc[1] = ['Maximum Return'] + portfolio_max_return.values.tolist()
Best_portfolios.loc[2] = ['Minimum Volatility'] + portfolio_min_vol.values.tolist()

# Plot
plt.figure(figsize=(10, 7))
plt.scatter(result['deviation']*100, result['return']*100, c=result['sharpie'], cmap='viridis')
plt.colorbar()
plt.annotate('Maximum Sharpie', xy=(max_sharpie_coordinates[0]*100, max_sharpie_coordinates[1]*100), \
                                xytext=(max_sharpie_coordinates[0]*100+0.06, max_sharpie_coordinates[1]*100-0.02), \
                                arrowprops=dict(arrowstyle='->',connectionstyle='arc3', linewidth=1, mutation_scale=20))
plt.scatter(max_sharpie_coordinates[0]*100, max_sharpie_coordinates[1]*100, marker='.',color='b',s=500, label='Maximum Sharpe')
plt.scatter(min_vol_coordinates[0]*100,min_vol_coordinates[1]*100, marker='.',color='c',s=500, label='Minimum Volatility')
target = np.linspace(min_vol_coordinates[1], max_return_coordinates[1], 50)
plt.title("Markowitz's Portfolio - Banking Sector Assets Analysis")
plt.xlabel('Risk (%)')
plt.ylabel('Return (%)')
plt.savefig('Markowits- 2017 a 2020.png')

# Export results 
writer = pd.ExcelWriter(path = 'Output - 2017 a 2020.xlsx', engine='xlsxwriter')
# Portfolio History
portfolio_history_df.to_excel(writer, sheet_name = 'Portfolio History', index=True, encoding='UTF-8')
# Portfolio Daily Return
portfolio_return_df.to_excel(writer, sheet_name = 'Portfolio Daily Return', index=True, encoding='UTF-8')
# Portfolio Statistics
portfolio_statistics_df.to_excel(writer, sheet_name = 'Portfolio Statistics', index=True, encoding='UTF-8')
# Correlation
correlation_df.to_excel(writer, sheet_name = 'Correlation', index=True, encoding='UTF-8')
# Covariation
covariation_df.to_excel(writer, sheet_name = 'Covariation', index=True, encoding='UTF-8')
# Result
result.to_excel(writer, sheet_name = 'All Random Portfolios', index=True, encoding='UTF-8')
# Best choices
Best_portfolios.to_excel(writer, sheet_name = 'Optimizations', index=True, encoding='UTF-8')
writer.save()
