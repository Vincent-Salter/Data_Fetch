import pandas as pd
import yfinance as yf

# Copyright Vincent Salter 02/12/23 2nd of May 2024


class ForexData():


    def __init__(self, pair):
        self.pair = pair
        pass

    def fetch_data(self, start_date, end_date):
        data = yf.download(self.pair, start_date, end_date)
        return data
    
    def process_data(self):
        forex_data = self.fetch_data(self.pair)
        return forex_data



forex_input = input("Input forex pair here: ")
fd = ForexData(forex_input)


# trying to simulate the way we fetch stock data