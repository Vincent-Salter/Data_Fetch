import os
import pandas as pd
from datetime import timedelta, datetime
import logging
from typing import List, Tuple

# Copyright Vincent Salter 02/12/23 2nd of May 2024

class trading_bot_methods(): ## get rid of class, just use methods

    def export_trades_to_csv(trades, directory, filename):
            if not filename.endswith(".csv"):
                filename += ".csv"
            filepath = os.path.join(directory, filename)
            if not os.path.exists(directory):
                os.makedirs(directory)
            trades_df = pd.DataFrame(trades, columns=['Buy Date', 'Buy Price', 'Sell Date', 'Sell Price', 'Long Profit'])
            trades_df.to_csv(filepath, index=False)

    def backtest_strategy(stock_data: pd.DataFrame, drawdown_percent: float, day_range: int) -> List[Tuple[datetime, float, datetime, float, float]]:
        """
        Backtest a trading strategy where stocks are bought on a drawdown and sold after a specified number of days.

        ... [Full docstring as above]
        """
        logger = logging.getLogger(__name__)
        required_columns = ['Open', 'Low', 'Close']
        
        if not all(col in stock_data.columns for col in required_columns):
            raise ValueError(f"Missing required columns: {', '.join([col for col in required_columns if col not in stock_data.columns])}")
        
        if not isinstance(stock_data.index, pd.DatetimeIndex):
            raise TypeError("The index of stock_data must be a DatetimeIndex.")
        
        trades = []
        drawdowns = stock_data[stock_data['Low'] <= stock_data['Open'] * (1 - drawdown_percent / 100)]
        
        for index, row in drawdowns.iterrows():
            buy_price = row['Low']
            sell_date = index + timedelta(days=day_range)
            
            try:
                sell_index = stock_data.index.get_indexer([sell_date], method='nearest')[0]
                sell_price = stock_data.iloc[sell_index]['Close']
                profit = sell_price - buy_price
                
                trades.append((index, buy_price, sell_date, sell_price, profit))
                logger.debug(f"Trade: Bought at {buy_price} on {index}, Sold at {sell_price} on {sell_date}")
            except KeyError:
                logger.info(f"Target sell date {sell_date} not found in the dataset or too far in the future.")
        
        return trades