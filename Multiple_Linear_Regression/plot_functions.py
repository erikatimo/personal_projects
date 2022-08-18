
import seaborn as sns
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import matplotlib.ticker as mtick
from random import random
import pdb

viridis_palet = ['#440154FF', '#481567FF', '#482677FF', '#453781FF', '#404788FF', '#39568CFF', '#33638DFF', '#2D708EFF', '#287D8EFF', '#238A8DFF', '#1F968BFF', '#20A387FF', '#29AF7FFF', '#3CBB75FF', '#55C667FF', '#73D055FF', '#95D840FF', '#B8DE29FF', '#DCE319FF', '#FDE725FF']

def plot_prices_X_period (Y_date, kwargs, name):
    """
    [Summary]:
    [Args]:
    [Returns]:
    """

    viridis_palette = ['#440154FF', '#481567FF', '#482677FF', '#453781FF', '#404788FF', '#39568CFF', '#33638DFF', '#2D708EFF', '#287D8EFF', '#238A8DFF', '#1F968BFF', '#20A387FF', '#29AF7FFF', '#3CBB75FF', '#55C667FF', '#73D055FF', '#95D840FF', '#B8DE29FF', '#DCE319FF', '#FDE725FF']
    palet_position = 0
    plt.style.use('seaborn')
    plt.figure(figsize=(10, 7))

    for X in kwargs:
        pdb.set_trace()
        plt.plot(Y_date, kwargs[X], color=viridis_palette[palet_position], label=X, linestyle='solid')
        palet_position = int(len(viridis_palet)*random())

    plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m'))
    plt.gca().xaxis.set_major_locator(mdates.MonthLocator(interval=1))
    plt.legend(labelspacing=0.8)
    plt.title("Assets History")
    plt.xlabel('Period')
    plt.ylabel('Closing Price')
    plt.savefig(f'.\plots\{name}.png')

def plot_return_X_period (X_asset, X_Nasdaq, Y_date, asset):
    """
    [Summary]:
    [Args]:
    [Returns]:
    """
    plt.style.use('seaborn')
    plt.clf()
    plt.figure(figsize=(10, 7))
    fig, axs = plt.subplots(1, 2, sharex=False, sharey=True)
    axs[0].plot(Y_date, X_asset, color='#440154FF', label=asset, linestyle='solid') 
    axs[1] = sns.distplot(X_asset, kde=True, color='#440154FF', vertical=True)
    axs[0].plot(Y_date, X_Nasdaq, color='#39568CFF', label='^NDX', linestyle='solid')
    axs[1] = sns.distplot(X_Nasdaq, kde=True, color='#39568CFF', vertical=True)
    axs[0].xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m'))
    axs[0].yaxis.set_major_formatter(mtick.PercentFormatter())
    axs[0].xaxis.set_major_locator(mdates.MonthLocator(interval=1))
    axs[0].tick_params(axis='x', labelrotation=45)
    fig.legend(labelspacing=0.8)
    fig.suptitle("Assets Continuous Return")
    axs[0].set_xlabel('Period')
    axs[0].set_ylabel('Return')
    plt.savefig(f'.\plots\historical_returns_{asset}.png')

def plot_nasdaq_X_asset(Y_asset, X_Nasdaq, asset):
    """
    [Summary]:
    [Args]:
    [Returns]:
    """  
    plt.figure(figsize=(10, 7))
    sns.regplot(x=X_Nasdaq, y=Y_asset)
    plt.title("Linear Regression")
    plt.xlabel('Nasdaq 100 Return')
    plt.ylabel('Asset Return')
    plt.savefig(f'.\plots\linear_regression_{asset}.png')

def plot_residuals_dist(res, asset):
    """
    [Summary]:
    [Args]:
    [Returns]:
    """
    plt.style.use('seaborn')
    plt.clf()
    plt.figure(figsize=(10, 7))
    sns.distplot(res, color='#8FD744FF', label=asset)
    plt.legend(labelspacing=0.8)
    plt.title("Residuals Distribution")
    plt.xlabel('Frequency')
    plt.savefig(f'./plots/residuals_distribution_{asset}.png')
