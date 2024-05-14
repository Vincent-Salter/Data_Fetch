from datetime import datetime, timedelta
import yfinance as yf
import pandas as pd
from methods import trading_bot_methods

# Copyright Vincent Salter 02/12/23 2nd of May 2024

 
def fetch_forex_data(pair, start_date, end_date):
    forex_data = yf.download(pair, start=start_date, end=end_date)
    return forex_data
# Usage
# this is the method for downloading from yahoo finance, placed here for convinience
# def download(tickers, start=None, end=None, actions=False, threads=True, ignore_tz=None,
#             group_by='column', auto_adjust=False, back_adjust=False, repair=False, keepna=False,
#            progress=True, period="max", show_errors=None, interval="1d", prepost=False,
#            proxy=None, rounding=False, timeout=10, session=None):


def main():
    forex_data = yf.download("EURUSD=X", start="2020-01-01", end="2020-12-31")
    forex_trades = trading_bot_methods.forex_backtest_strategy(forex_data, drawdown_percent=1, day_range=6)
    print(pd.DataFrame(forex_trades, columns=['Buy Date', 'Buy Price', 'Sell Date', 'Sell Price', 'Long Profit']))
