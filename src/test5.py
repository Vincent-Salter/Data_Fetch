import yfinance as yf
from datetime import datetime, timedelta
from methods import trading_bot_methods
from testing_methods import update_stock_algo
import pandas as pd
from flask import Flask, render_template, request, jsonify

app = Flask(__name__)

class StockAlgorithm:

    def __init__(self, drawdown_percent, day_range):
        self.drawdown_percent = drawdown_percent
        self.day_range = day_range
        self.start_date = (datetime.now() - timedelta(days=365)).strftime('%Y-%m-%d')
        self.end_date = datetime.now().strftime('%Y-%m-%d')
        self.tickers = []

    def fetch_stock_data(self, stock_symbol):
        try:
            stock_data = yf.download(stock_symbol, self.start_date, self.end_date)
            return stock_data
        except Exception as e:
            print(f"Error fetching data for {stock_symbol}: {e}")
            return pd.DataFrame()

    def add_tickers_to_list(self, ticker):
        if ticker not in self.tickers:
            self.tickers.append(ticker)
        else:
            print(f'{ticker} is already in the list.')

    def process_all_tickers(self):
        results = []
        for ticker in self.tickers:
            data = self.fetch_stock_data(ticker)
            if data.empty:
                continue
            trades = trading_bot_methods.backtest_strategy(data, self.drawdown_percent, self.day_range)
            if not trades:
                continue
            total_profit = sum(trade[4] for trade in trades)
            results.append({
                'ticker': ticker,
                'total_trades': len(trades),
                'total_profit': total_profit
            })
        return results

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/run-backtest', methods=['POST'])
def run_backtest():
    
    company = request.form['company']
    drawdown = float(request.form['drawdown'])
    days = int(request.form['days'])

    print(f"Downloading {company} data...")

    stock_algo = StockAlgorithm(drawdown, days)
    stock_algo.add_tickers_to_list(company)
    results = stock_algo.process_all_tickers()

    return render_template('results.html', results=results)

@app.route('/update-algo_object', methods=['POST'])
def update_algo_object():

    company = request.form['company']
    drawdown = float(request.form['drawdown'])
    days = int(request.form['days'])

    print("Updating algo object...")

    update_stock_algo()





if __name__ == '__main__':
    app.run(debug=True, port=8080)