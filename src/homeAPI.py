import requests
from flask import Flask, render_template

app = Flask(__name__)

stock_symbols = ['AAPL','GOOGL','MSFT','NVDA','TSLA']
stock_data = {}

def fetch_stock_data(symbol):
    api_key = 'UPRXJ0H5LBB4BKLM'
    url = 'https://www.alphavantage.co/query?function=TIME_SERIES_DAILY&symbol={symbol}&apikey={api_key}'
    r = requests.get(url)
    data = r.json()

    if "Time Series (Daily)" in data:
        last_refresh = data["Meta Data"]["3. Last Refreshed"]
        last_day = data["Time Series (Daily)"][last_refresh]
        price = last_day["4. close"]
        return{
            "symbol":symbol,
            "price":price,
            "date":last_refresh
        }
    else:
        return{
            "symbol":symbol,
            "price":"N/A",
            "date":"N/A"
        }

def index():
    stock_data = [fetch_stock_data(stock) for stock in stock_symbols]
    return render_template('index.html', stock_symbols=stock_data)

if __name__ == '__main__':
    app.run(debug=True)