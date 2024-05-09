from pycoingecko import CoinGeckoAPI
import pandas as pd

# Copyright Vincent Salter 02/12/23 2nd of May 2024

# testing how to pull bitcoin data in line with the dataframe made for pulling stocks.
cg = CoinGeckoAPI()

crypto = 'bitcoin'
crypto_data = cg.get_coin_market_chart_by_id(id=crypto.lower(), vs_currency='usd', days='30')

# this gives empty dataframe.
df = pd.DataFrame(crypto_data, columns=['Buy Date', 'Buy Price', 'Sell Date', 'Sell Price', 'Long Profit'])



print(df)