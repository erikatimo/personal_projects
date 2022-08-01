"""
    Created at: 2022-03-29
    Author: Erika Timo de Oliveira
    Description: Analysis of Banking Sector Assets through Markowitz's Portfolio Theory
"""
# source
from cProfile import label
from yahooquery import Ticker
# data transformation
import numpy as np
import pandas as pd
import datetime 
from pandas.tseries.offsets import BDay
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

def get_historical_prices(tickers, start_date, end_date, fig_name):
    """
    [Summary]:
        Request asset prices through yahooquery library a                                                                                                                                                                                                                                                                                                                                                                                                                                 nd save assets_history fig
    [Args]:
        - tickers: list of assets codes according with Yahoo data names
        - start_date: start date of data collection
        - end_date: end date of data collection
        - fig_name: name to save assets history graph figure  
    [Returns]:
        - portfolio_history_df: dataframe containing request response 
          (symbol, date, open, volume, high, low, close, adjclose, dividends, period, ticker)
    """

    # request historical prices
    portfolio = Ticker([ticker + '.SA' for ticker in tickers])
    portfolio_history_df = portfolio.history(start=start_date, end=end_date)
    portfolio_history_df.reset_index(level=[0,1], inplace=True)
    portfolio_history_df['period'] = portfolio_history_df['date'].apply(lambda x: x.strftime('%Y-%m'))
    portfolio_history_df['ticker'] = portfolio_history_df['symbol'].apply(lambda x: x.replace('.SA', ''))
    
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
    plt.savefig(fig_name+'.png')

    return portfolio_history_df


def return_variation(portfolio_history_df, tickers, fig_name):
    """
    [Summary]:
        Calculate return variation of assets 
    [Args]:
        - tickers: list of assets codes according with Yahoo data names
        - portfolio_history_df: dataframe containing 'date', 'close' and 'ticker' information 
        - fig_name: name to save return graph figure  
    [Returns]:
        - portfolio_return_df: dataframe containing daily return of assets
          (date, close, ticker, discreet_return, continuous_return)
    """

    # calculate return variations
    portfolio_return_df = pd.DataFrame()
    for ticker in pd.unique(portfolio_history_df['ticker']):
        df = portfolio_history_df[portfolio_history_df['ticker']==ticker][['date', 'close', 'ticker']]
        df['discreet_return'] = round(df['close']/df['close'].shift(1) -1,6)
        df['continuous_return'] = round(np.log(df['close']/df['close'].shift(1)),6)
        df.drop(index=df.index[0], inplace=True) # First row does not have calculated return
        portfolio_return_df = portfolio_return_df.append(df, ignore_index=True)

    # plot return
    plt.clf()
    plt.figure(figsize=(10, 7))
    viridis_palet = ['#440154FF', '#481567FF', '#482677FF', '#453781FF', '#404788FF', '#39568CFF', '#33638DFF', '#2D708EFF', '#287D8EFF', '#238A8DFF', '#1F968BFF', '#20A387FF', '#29AF7FFF', '#3CBB75FF', '#55C667FF', '#73D055FF', '#95D840FF', '#B8DE29FF', '#DCE319FF', '#FDE725FF']
    palet_position = 0
    fig, axs = plt.subplots(1, 2, sharex=False, sharey=True)
    for ticker in tickers:
        data = portfolio_return_df[portfolio_return_df['ticker']==ticker]
        axs[0].plot(data['date'], data['continuous_return'], color=viridis_palet[palet_position], label=ticker, linestyle='solid')
        axs[1] = sns.distplot(data['continuous_return'], kde=True, color=viridis_palet[palet_position], vertical=True)
        palet_position +=int(round(4.5,0))
    
    axs[0].xaxis.set_major_formatter(mdates.DateFormatter('%Y-%b'))
    axs[0].yaxis.set_major_formatter(mtick.PercentFormatter())

    fig.legend(labelspacing=0.8)
    fig.suptitle("Continuous Assets Return")
    axs[0].set_xlabel('Period')
    axs[0].set_ylabel('Return')
    fig.autofmt_xdate()
    fig.savefig(fig_name+'.png')

    return portfolio_return_df


def return_covariation(portfolio_return_df, fig_name):
    """
    [Summary]:
        Calculate return covariation of assets 
    [Args]:
        - portfolio_return_df: dataframe containing daily return of assets
        - fig_name: name to save covariation return graph figure  
    [Returns]:
        - covariation_df: dataframe containing covariation matrix 
    """
    covariation_df = pd.pivot_table(portfolio_return_df, values='continuous_return',
                                index='date', columns='ticker').cov()
    # Plot Covariation
    plt.figure(figsize=(10, 7))
    mask = np.triu(np.ones_like(covariation_df, dtype=np.bool),1)
    sns.heatmap(covariation_df, mask=mask, vmin=min(covariation_df.min()), \
                vmax=max(covariation_df.max()), annot=True, cmap='viridis', fmt=".2%")
    plt.title("Assets Covariation")
    plt.savefig(fig_name+'.png')

    return covariation_df


def return_correlation(portfolio_return_df, fig_name):
    """
    [Summary]:
        Calculate return correlation of assets 
    [Args]:
        - portfolio_return_df: dataframe containing daily return of assets
        - fig_name: name to save covariation return graph figure  
    [Returns]:
        - correlation_df: dataframe containing covariation matrix 
    """
    correlation_df = pd.pivot_table(portfolio_return_df, values='continuous_return',
                                index='date', columns='ticker').corr()

    # Plot Correlation
    plt.figure(figsize=(10, 7))
    mask = np.triu(np.ones_like(correlation_df, dtype=np.bool))
    sns.heatmap(correlation_df, mask=mask, vmin=-1, vmax=1, annot=True, cmap='viridis')
    plt.title("Assets Correlation")
    plt.savefig(fig_name+'.png')

    return correlation_df

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
    #portfolio_deviation = np.sqrt(portfolio_deviation)

    weights.reset_index(inplace=True)
    df = mean_returns.merge(weights, how='left', left_on='ticker', right_on='index')
    df['weighted_avg_return'] = df['avg_return']*df['weight']
    portfolio_return = np.sum(df['weighted_avg_return']) 

    return portfolio_return, portfolio_deviation

def random_portfolio(n_simulations, assets, mean_returns, cov_matrix, risk_free_rate, fig_name):
    """
    [Summary]:
        This function applies portfolio_performance for n portfolios, using random weights 
    [Args]:
        - n_simulations: number of simulations to be applied
    [Returns]:
        -
    """

    column_names = ['weight ' + asset + ' %' for asset in assets] + ['return', 'deviation', 'sharpie']
    results_df = pd.DataFrame(columns=column_names)
    
    for i in range(n_simulations):
        weights = random_weights(assets)
        portfolio_return, portfolio_deviation = portfolio_performance(weights, mean_returns, cov_matrix, tickers=assets)
        sharpie_index = (portfolio_return-risk_free_rate)/portfolio_deviation
        
        results_df.loc[i] = weights.transpose().values.tolist()[1] + [portfolio_return, portfolio_deviation, sharpie_index]
    
    
    # Maximum Sharpie Index
    portfolio_max_sharpie = results_df.loc[results_df['sharpie'].idxmax()]
    max_sharpie_coordinates = [portfolio_max_sharpie.loc['deviation'], portfolio_max_sharpie.loc['return']]

    # Maximum Return 
    portfolio_max_return = results_df.loc[results_df['return'].idxmax()]
    max_return_coordinates = [portfolio_max_return.loc['deviation'], portfolio_max_return.loc['return']]

    # Minimum Volatility
    portfolio_min_vol = results_df.loc[results_df['deviation'].idxmin()]
    min_vol_coordinates = [portfolio_min_vol.loc['deviation'], portfolio_min_vol.loc['return']]

    best_portfolios_df = pd.DataFrame(columns=['Method']+results_df.columns.tolist())
    best_portfolios_df.loc[0] = ['Maximum Sharpie'] + [round(i*100,2) for i in portfolio_max_sharpie.values.tolist()]
    best_portfolios_df.loc[1] = ['Maximum Return'] + [round(i*100,2) for i in portfolio_max_return.values.tolist()]
    best_portfolios_df.loc[2] = ['Minimum Volatility'] + [round(i*100,2) for i in portfolio_min_vol.values.tolist()]


    #plot
    plt.figure(figsize=(10, 7))
    plt.scatter(results_df['deviation']*100, results_df['return']*100, c=results_df['sharpie'], cmap='viridis')
    plt.colorbar()
    plt.annotate('Maximum Sharpie', xy=(max_sharpie_coordinates[0]*100, max_sharpie_coordinates[1]*100), \
                                    xytext=(max_sharpie_coordinates[0]*100+0.06, max_sharpie_coordinates[1]*100-0.02), \
                                    arrowprops=dict(arrowstyle='->',connectionstyle='arc3', linewidth=1, mutation_scale=20))
    plt.scatter(max_sharpie_coordinates[0]*100, max_sharpie_coordinates[1]*100, marker='.',color='b',s=500, label='Maximum Sharpe')
    plt.scatter(min_vol_coordinates[0]*100,min_vol_coordinates[1]*100, marker='.',color='c',s=500, label='Minimum Volatility')
    #target = np.linspace(min_vol_coordinates[1], max_return_coordinates[1], 50)
    plt.title("Markowitz's Portfolio - Banking Sector Assets Analysis")
    plt.xlabel('Risk (%)')
    plt.ylabel('Return (%)')
    plt.savefig(fig_name+'.png')


    return results_df, best_portfolios_df


"""
    Questão 0 
"""
# Definição dos parâmetros
tickers = ['BPAC11', 'ITUB4', 'SANB11', 'BBAS3', 'BBDC4']
start_date = datetime.date(2021,5,1) 
end_date = datetime.date(2022,4,15)

# Letra A
portfolio_history_df = get_historical_prices(tickers=tickers, start_date=start_date, end_date=end_date, fig_name='assets_history')
portfolio_return_df = return_variation(tickers=tickers, portfolio_history_df=portfolio_history_df, fig_name='assets_return')
portfolio_history_df.to_csv('results/questao_0/0_data.csv')
portfolio_return_df.to_csv('results/questao_0/0_a_results.csv')

# Letra B
portfolio_statistics_df = pd.DataFrame(data={'ticker':tickers})
avg_return_df = pd.DataFrame()
avg_return_df['avg_return'] = round(portfolio_return_df.groupby('ticker')['continuous_return'].mean(),7)
avg_return_df.reset_index(inplace=True)
portfolio_statistics_df = portfolio_statistics_df.merge(avg_return_df, how='left', on='ticker')

std_deviation_df = pd.DataFrame()
std_deviation_df['std_deviation'] = round(portfolio_return_df.groupby('ticker')['continuous_return'].std(),7)
std_deviation_df.reset_index(inplace=True)
portfolio_statistics_df = portfolio_statistics_df.merge(std_deviation_df, how='left', on='ticker')

portfolio_statistics_df.to_csv('results/questao_0/0_b_results.csv')

# Letra C
covariation_df = return_covariation(portfolio_return_df, 'assets_covariation')
correlation_df = return_correlation(portfolio_return_df, 'assets_correlation')

covariation_df.to_csv('results/questao_0/0_c_results.csv')

# Letra D
risk_free_rate=0
results_df, best_portfolios_df = random_portfolio(5000, tickers, portfolio_statistics_df[['ticker', 'avg_return']], \
                                                  covariation_df, risk_free_rate, fig_name='markowits')
best_portfolios_df.to_csv('results/questao_0/0_d_results.csv')

"""
    Questão 1 
"""

# Letra A
ibovespa_history_df = get_historical_prices(tickers=['BOVA11'], start_date=start_date, end_date=end_date, fig_name='ibovespa_history')
bovespa_return_df = return_variation(tickers=['BOVA11'],portfolio_history_df=ibovespa_history_df, fig_name='ibovespa_return')

weights_df = best_portfolios_df.set_index('Method').transpose().reset_index()
weights_df['index'] = weights_df['index'].str.replace('weight ', '')
weights_df['index'] = weights_df['index'].str.replace(' %', '')

portfolio_history_df = portfolio_history_df.merge(weights_df, how='left', left_on='ticker', right_on='index')
portfolio_history_df['weighted_close'] = portfolio_history_df['close']*portfolio_history_df['Maximum Sharpie']/100

simulated_portfolio_history_df = portfolio_history_df.groupby('date')['weighted_close'].sum().reset_index()
simulated_portfolio_history_df.columns = ['date', 'close']
simulated_portfolio_history_df['ticker'] = 'CART'
simulated_portfolio_history_df.to_csv('results/questao_1/1_b_simulated_portfolio.csv')

simulated_portfolio_return_df = return_variation(tickers=['CART'], portfolio_history_df=simulated_portfolio_history_df, fig_name='simulated_portfolio_return')

# plot historical prices
plt.figure(figsize=(10, 7))
plt.plot(simulated_portfolio_history_df['date'], simulated_portfolio_history_df['close'], color='#440154FF', label='CART', linestyle='solid')
plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%Y-%b'))
plt.legend(labelspacing=0.8)
plt.title("Portfolio History")
plt.xlabel('Period')
plt.ylabel('Closing Price')
plt.savefig('simulated_portfolio_history.png')

# Letra B
model = LinearRegression()
X = bovespa_return_df[['continuous_return']]
Y = simulated_portfolio_return_df[['continuous_return']]

plt.figure(figsize=(10, 7))
sns.regplot(x=X, y=Y)
plt.title("Linear Regression")
plt.xlabel('IBOVESPA Return')
plt.ylabel('Portfolio Return')
plt.savefig('linear_regression.png')

model.fit(X, Y)

# Letra c 
regression_results_df = pd.DataFrame({'α': model.intercept_, 'β': model.coef_[0]})      
regression_results_df.to_csv('results/questao_1/1_c_results.csv')