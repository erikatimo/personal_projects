"""
    Created at: 2022-08-17
    Author: Erika Timo de Oliveira
    Description: Collecting yahoo finance data via yahooquery library
"""

import pandas as pd
from yahooquery import Ticker
import pdb
import warnings
warnings.filterwarnings("ignore")
import datetime 

end_date = datetime.date(2022,6,1) 
start_date = datetime.date(2021,6,1) 

companies = pd.read_excel('companies.xlsx', sheet_name='data')

for status in companies.Status.unique():
    selected_companies = companies[companies.Country == 'United States'][companies.Status == status][companies.stock_symbol != '-']
    selected_companies.describe()
    portfolio = Ticker(['^GSPC', '^NDX'] + selected_companies['stock_symbol'].to_list())
    stocks_data = portfolio.history(start=start_date, end=end_date)
    if type(stocks_data) == dict:
        pdb.set_trace()
        print(pd.DataFrame.from_dict(stocks_data))
        pass
    else:
        pass
    stocks_data['status'] = status
    stocks_data.reset_index(level=[0,1], inplace=True)
    stocks_data = stocks_data.pivot(index='date', columns = 'symbol', values = 'close')
    stocks_data.to_excel(f'data_{status}.xlsx')
    print(f'{status} loaded')


