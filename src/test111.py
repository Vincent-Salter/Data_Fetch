from datetime import timedelta
import yfinance as yf
import pandas as pd

# modify if i need for forex
def backtest_strategy(stock_data, drawdown_percent, day_range):
    trades = []
    for index, row in stock_data.iterrows():
        open_price = row['Open']
        low_price = row['Low']
        if low_price <= open_price * (1 - drawdown_percent / 100):
            buy_price = low_price
            sell_date = index + timedelta(days=day_range)

            # Adjust sell_date if it falls on a weekend (Forex market closed)
            while sell_date.weekday() > 4:  # 5 = Saturday, 6 = Sunday
                sell_date += timedelta(days=1)

            if sell_date in stock_data.index:
                sell_price = stock_data.loc[sell_date]['Close']
                profit = (sell_price - buy_price) / buy_price * 100  # profit as percentage
                trades.append((index, buy_price, sell_date, sell_price, profit))
            else:
                print(f"Target sell date is out of range for the data: {sell_date}")
    return trades

# Usage
# this is the method for downloading from yahoo finance, placed here for convinience
# def download(tickers, start=None, end=None, actions=False, threads=True, ignore_tz=None,
#             group_by='column', auto_adjust=False, back_adjust=False, repair=False, keepna=False,
#            progress=True, period="max", show_errors=None, interval="1d", prepost=False,
#            proxy=None, rounding=False, timeout=10, session=None):
forex_data = yf.download("EURUSD=X", start="2020-01-01", end="2020-12-31")
forex_trades = backtest_strategy(forex_data, drawdown_percent=1, day_range=2)
print(pd.DataFrame(forex_trades, columns=['Buy Date', 'Buy Price', 'Sell Date', 'Sell Price', 'Long Profit']))
