from pycoingecko import CoinGeckoAPI
import pandas as pd
import numpy as np
# Copyright Vincent Salter 02/12/23 2nd of May 2024

# testing how to pull bitcoin data in line with the dataframe made for pulling stocks.
cg = CoinGeckoAPI()

data = {
    'prices': [
        [1715177079152, 62485.480734804514], [1715180437232, 62657.19648842473], 

    ],
    'market_caps': [
        [1715177079152, 1226488648070.1135], [1715180437232, 1233908666612.9546],

    ],
    'total_volumes': [
        [1715177079152, 25179675104.09246], [1715180437232, 25391596875.028748],
      
    ]
}

# Create DataFrames from the lists
prices_df = pd.DataFrame(data['prices'], columns=['timestamp', 'Close'])
volumes_df = pd.DataFrame(data['total_volumes'], columns=['timestamp', 'Volume'])

# Convert timestamps from milliseconds to a datetime format
prices_df['timestamp'] = pd.to_datetime(prices_df['timestamp'], unit='ms')
volumes_df['timestamp'] = pd.to_datetime(volumes_df['timestamp'], unit='ms')

# Set the timestamp as the index
prices_df.set_index('timestamp', inplace=True)
volumes_df.set_index('timestamp', inplace=True)

# Since we don't have separate Open, High, Low prices, use Close for all
prices_df['Open'] = prices_df['Close']
prices_df['High'] = prices_df['Close']
prices_df['Low'] = prices_df['Close']

# Merge prices and volumes data
crypto_df = prices_df.join(volumes_df)

# Assuming `crypto_df` is your DataFrame
crypto_df['SMA30'] = crypto_df['Close'].rolling(window=30, min_periods=1).mean()  # 30-tick SMA
crypto_df['SMA90'] = crypto_df['Close'].rolling(window=90, min_periods=1).mean()  # 90-tick SMA
# Generate buy/sell signals
crypto_df['Position'] = 0
crypto_df['Position'][crypto_df['SMA30'] > crypto_df['SMA90']] = 1  # Buy signal
crypto_df['Position'][crypto_df['SMA30'] < crypto_df['SMA90']] = -1  # Sell signal

# Take the first difference of the Position column to get buy/sell trigger points
crypto_df['Signal'] = crypto_df['Position'].diff()
buy_signals = crypto_df[crypto_df['Signal'] == 1]
sell_signals = crypto_df[crypto_df['Signal'] == -1]

# Ensure all trades are closed by discarding unmatched buys/sells
min_length = min(len(buy_signals), len(sell_signals))
buy_signals = buy_signals.iloc[:min_length]
sell_signals = sell_signals.iloc[:min_length]


trades = pd.DataFrame({
    'Buy Date': buy_signals.index,
    'Buy Price': buy_signals['Close'],
    'Sell Date': sell_signals.index,
    'Sell Price': sell_signals['Close']
})


print(trades)
