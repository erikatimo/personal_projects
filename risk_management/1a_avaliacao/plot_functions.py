import seaborn as sns
import matplotlib.ticker as ticker
import matplotlib.pyplot as plt

def plot_prices(dataframe, x, y, hue): 
    """
    [Summary]:
        Essa função retorna o plot de preços por periodo
    [Args]:
        dataframe: conjunto de dados de preço por tempo
        atenção ao nome das colunas
    [Returns]:
        plot figure file: "Prices Visualization.png" 
    """
    sns.set_style('whitegrid')
    prices_plot = sns.lineplot(data=dataframe, x=x, y=y, hue=hue,
                            palette='magma') # viridis, rocket_r, magma, mako
    prices_plot.xaxis.set_major_locator(ticker.LinearLocator(10))
    prices_plot.xaxis.set_label_text('Monthly Period')
    prices_plot.yaxis.set_label_text('Closing Price')
    prices_plot.figure.savefig('Prices Visualization.png')


def plot_histograms(dataframe): 
    """
    [Summary]:
        Essa função retorna o plot de preços por periodo
    [Args]:
        dataframe: conjunto de dados de preço por tempo
        atenção ao nome das colunas
    [Returns]:
        plot figure file: "Prices Visualization.png" 
    """
    sns.set_style('whitegrid')
    fig, axs = plt.subplots(2, 2, figsize=(7, 7))
    dataframe[dataframe['ticker']==ticker]
    sns.histplot(data=dataframe[dataframe['ticker']=='BPAC11'], x='continuous_return', kde=True, color='#94D24B', ax=axs[0, 0])
    sns.histplot(data=dataframe[dataframe['ticker']=='ITUB4'],  x='continuous_return', kde=True, color="#469B89", ax=axs[0, 1])
    sns.histplot(data=dataframe[dataframe['ticker']=='BBAS3'],  x='continuous_return', kde=True, color="#3E5E8C", ax=axs[1, 0])
    sns.histplot(data=dataframe[dataframe['ticker']=='BBDC4'],  x='continuous_return', kde=True, color="#41105C", ax=axs[1, 1])
    plt.savefig('Return Dispersion.png')

