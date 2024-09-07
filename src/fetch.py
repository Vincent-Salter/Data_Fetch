import yfinance as yf
import pandas as pd





def fetch_stock_data(x):
    data = yf.download(x)
    print(data)

def fetch_open_price(x):
    data = yf.download(x)
    data = pd.DataFrame




fetch_stock_data("TSLA")