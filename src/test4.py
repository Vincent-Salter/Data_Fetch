import yfinance as yf
from datetime import datetime, timedelta
from methods import trading_bot_methods
from testing_methods import update_stock_algo
from pycoingecko import CoinGeckoAPI
import pandas as pd

# Copyright Vincent Salter 02/12/23 2nd of May 2024

class StockAlgorithm:

    ## main construction of the object
    def __init__(self, drawdown_percent, day_range):
        self.drawdown_percent = drawdown_percent
        self.day_range = day_range
        self.start_date = (datetime.now() - timedelta(days=365)).strftime('%Y-%m-%d')
        self.end_date = datetime.now().strftime('%Y-%m-%d')
        self.tickers = []
        self.cg = CoinGeckoAPI()

    def fetch_data(self, ticker):
        if ticker.lower() in ['bitcoin', 'ethereum', 'solana', 'bnb', 'xrp', 'usdc']:  # You can expand this list
            return self.fetch_crypto_data(ticker)
        else:
            return self.fetch_stock_data(ticker, self.start_date, self.end_date)

    def fetch_stock_data(self, stock_symbol, start_date, end_date):
        try:
            stock_data = yf.download(stock_symbol, start=start_date, end=end_date)
            return stock_data
        except Exception as e:
            print(f"Error fetching data for {stock_symbol}: {e}")
            return []
        
    ## beginning to test these methods
    ## unlikely to be compatible until the dataframe is the same as fetching stock data 
    
    def fetch_crypto_data(self, crypto):
        try:
            crypto_data = self.cg.get_coin_market_chart_by_id(id=crypto.lower(), vs_currency='usd', days='30')
            # Transform the list of prices into a DataFrame
            df = pd.DataFrame(crypto_data['prices'], columns=['timestamp', 'Close'])
            df['timestamp'] = pd.to_datetime(df['timestamp'], unit='ms')
            df.set_index('timestamp', inplace=True)
            
            df['Open'] = df['Close']
            df['High'] = df['Close']
            df['Low'] = df['Close']
            df['Volume'] = 0  # Volume information may not be available in this dataset
            
            trades_df = pd.DataFrame(columns=['Buy Date', 'Buy Price', 'Sell Date', 'Sell Price', 'Long Profit'])
            return df, trades_df
        except Exception as e:
            print(f"Error fetching data for {crypto}: {e}")
            return pd.DataFrame(), pd.DataFrame()
        
        
    def set_drawdown_percent(self, new_drawdown_percent):
        try:
            new_drawdown_percent = float(new_drawdown_percent)
            if new_drawdown_percent <= 0:
                print("Drawdown percent must be greater than 0.")
            else:
                self.drawdown_percent = new_drawdown_percent
        except ValueError:
            print("Invalid input for drawdown percent. Please enter a valid number.")

    def set_day_range(self, new_day_range):
        try:
            new_day_range = int(new_day_range)
            if new_day_range <= 0:
                print("Day range must be a positive integer.")
            else:
                self.day_range = new_day_range
        except ValueError:
            print("Invalid input for day range. Please enter a valid integer.")

    def set_date_range(self, new_start_date, new_end_date):
            try:
                new_start_date = datetime.strptime(new_start_date, '%Y-%m-%d')
                new_end_date = datetime.strptime(new_end_date, '%Y-%m-%d')
                if new_start_date > new_end_date:
                    print("Start date cannot be after end date.")
                else:
                    self.start_date = new_start_date.strftime('%Y-%m-%d')
                    self.end_date = new_end_date.strftime('%Y-%m-%d')
                    print("\nDate range updated successfully.")
            except ValueError:
                print("Invalid date format. Please use YYYY-MM-DD format.")

    def add_tickers_to_list(self, ticker):
        if ticker not in self.tickers:
            self.tickers.append(ticker)
        else:
            print(f'{ticker} is already in the list.')
          
    def process_all_tickers(self, directory):
        for ticker in self.tickers:
            print(f"Processing {ticker}...")
            data = self.fetch_stock_data(ticker)  # Currently only fetching stock data while developing fetching crypto and forex
            if data.empty:
                print("No data fetched or no qualifying trades found.")
                continue
            trades = trading_bot_methods.backtest_strategy(data, self.drawdown_percent, self.day_range)
            if not trades:
                print("No qualifying trades found.")
            else:
                total_profit = sum(trade[4] for trade in trades)
                print(f"Total number of trades: {len(trades)}")
                print(f"Total profit: {total_profit}")
            filename = f"{ticker}_{self.drawdown_percent}%_{self.day_range}.csv"
            trading_bot_methods.export_trades_to_csv(trades, directory, filename)
            print(f"{ticker} data saved in {directory}") ##here i need to add automation to the process_stock method where if a list is invoked it runs all objects in the list without interuption
                                  ##such as no plotting the data or asking each time where to save the file, they all need to be passed to the same directory

    def clear_all_tickers(self):
        self.tickers = []
        print("\nList of tickers cleared...\n")
        print("Please choose again.")

def main():
    print("\nWelcome to Danti.\n")
    initial_drawdown_percent = trading_bot_methods.get_float_input("Enter drawdown percent (e.g., 5 for 5%): ")
    initial_day_range = trading_bot_methods.get_int_input("\nHow many days until you would like to sell?: ")
    stock_algo = StockAlgorithm(initial_drawdown_percent, initial_day_range)
    

    while True:
        print("\nOptions: 'update', 'add', 'clear-list', 'run', 'done'")
        user_input = input('\nUser choice here: ').lower()

        if user_input == 'update':
            update_stock_algo(stock_algo)

        elif user_input == 'add':
            tickers = input("Enter tickers (Forex format: 'EURUSD=X', Stock format: 'AAPL', Crypto format: 'bitcoin') separated by only a comma (press 'enter' to add): ")
            if tickers.strip():
                tickers_to_add = [ticker.strip().upper() for ticker in tickers.split(',')]
            for ticker in tickers_to_add:
                if not (ticker.isalnum() and 1 <= len(ticker) <= 10):
                    print(f"Invalid ticker format: {ticker}. Tickers should be alphabetic and up to 5 characters long.")
                elif ticker in stock_algo.tickers:
                    print(f"{ticker} is already in the list.")
                else:
                    stock_algo.add_tickers_to_list(ticker)
                    print(f"{ticker} added to the list.")

        elif user_input == 'run':
            if not stock_algo.tickers:
                print("No tickers added. Please add tickers first.")
            else:
                print("\nEnter and existing directory or simply provide a new one and it will be created for you.")
                directory = input(r"Directory for saving all trade data: ")
                stock_algo.process_all_tickers(directory)

        elif user_input == 'clear-list':
            stock_algo.clear_all_tickers()

        elif user_input == 'done':
            print("Exiting the program.")
            break
        else:
            print("Invalid input.")


if __name__ == '__main__':
    main()