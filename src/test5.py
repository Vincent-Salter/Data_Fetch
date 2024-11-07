import yfinance as yf
from datetime import datetime, timedelta
from methods import trading_bot_methods
from testing_methods import update_stock_algo
import pandas as pd
from flask import Flask, render_template, request, session, jsonify

app = Flask(__name__)
app.secret_key = 'as9d87asdn98dwij9'

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


@app.route('/run_datafetch_page', methods=['POST'])
def run_portfolio():
    return render_template('datafetch_page.html')

@app.route('/run_update', methods=['POST'])
def run_update():
    
    # Retrieve updated values from the form
    update_company = request.form['company']
    update_drawdown = float(request.form['drawdown'])
    update_days = int(request.form['days'])

    # Retrieve the StockAlgorithm object from the session
    stock_algo = session.get('object')

    if stock_algo:
        # Update the stock_algo object with new values
        stock_algo.tickers = []
        stock_algo.drawdown_percent = update_drawdown
        stock_algo.day_range = update_days
        stock_algo.add_tickers_to_list(update_company)
        results = stock_algo.process_all_tickers()

        return render_template('results.html', results=results)
    else:
        return "No existing stock algorithm session found.", 400


@app.route('/run-backtest', methods=['POST'])
def run_backtest():
    company = request.form['company']
    drawdown = float(request.form['drawdown'])
    days = int(request.form['days'])

    print(f"Downloading {company} data...")

    stock_algo = StockAlgorithm(drawdown, days)
    stock_algo.add_tickers_to_list(company)
    results = stock_algo.process_all_tickers()

    session['company'] = company
    session['drawdown'] = drawdown
    session['days'] = days
    session['object'] = stock_algo
    

    return render_template('results.html', results=results)

if __name__ == '__main__':
    app.run(debug=True, port=8080)