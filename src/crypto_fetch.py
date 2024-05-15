import pandas as pd
import yfinance as yf
import requests

# Copyright Vincent Salter 02/12/23 2nd of May 2024

class CryptoData():
    def __init__(self, pair):
        self.pair = pair

    def fetch_data(self):
        url = f"https://api.coingecko.com/api/v3/simple/price?ids={self.pair}&vs_currencies=usd"
        response = requests.get(url)
        data = response.json()
        return data

    def process_data(self):
        crypto_data = self.fetch_data()
        return crypto_data

    def fetch_historical_data(self):
        ticker = yf.Ticker(self.pair)
        historical_data = ticker.history(period="6mo")
        return historical_data

cg = CryptoData("bitcoin")

print(cg.process_data())
print(cg.fetch_historical_data())