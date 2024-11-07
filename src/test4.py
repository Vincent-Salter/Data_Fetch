import yfinance as yf
from datetime import datetime, timedelta
from methods import trading_bot_methods
from typing import List, Tuple
import os


# Copyright Vincent Salter 02/12/23 2nd of May 2024



class StockAlgorithm:

    ## main construction of the object
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
                return []

    def add_tickers_to_list(self, ticker: str) -> None:
        """
        Adds a ticker to the list if it's not already present.

        :param ticker: The stock ticker symbol to add.
        """
        if ticker not in self.tickers:
            self.tickers.append(ticker)
            print(f"Ticker {ticker} added to the list.")
        else:
            print(f"'{ticker}' is already in the list.")
          
    def process_all_tickers(self, directory: str) -> None:
        """
        Processes all tickers in the list, performs backtesting, and saves results to CSV.

        :param directory: The directory where to save the CSV files.
        """
        if not self.tickers:
            print("No tickers to process.")
            return

        for ticker in self.tickers:
            print(f"Processing {ticker}...")
            data = self.fetch_stock_data(ticker)
            if data.empty:
                print(f"No data available for {ticker}.")
                continue
            
            trades: List[Tuple[datetime, float, datetime, float, float]] = trading_bot_methods.backtest_strategy(data, self.drawdown_percent, self.day_range)
            if not trades:
                print(f"No qualifying trades found for {ticker}.")
            else:
                total_profit = sum(trade[4] for trade in trades)
                print(f"Total number of trades for {ticker}: {len(trades)}")
                print(f"Total profit for {ticker}: {total_profit:.2f}")
                
                filename = f"{ticker}_{self.drawdown_percent:.0f}%_{self.day_range}.csv"
                try:
                    trading_bot_methods.export_trades_to_csv(trades, directory, filename)
                    print(f"{ticker} data saved in {directory}/{filename}")
                except Exception as e:
                    print(f"Error saving {ticker} data: {e}")
                            

    def clear_all_tickers(self) -> None:
        """
        Clears all tickers from the list.
        """
        self.tickers.clear() 
        print("\nList of tickers cleared.\nPlease choose again.")

def add_tickers(stock_algo: StockAlgorithm) -> None:
    while True:
        ticker = input("Enter ticker symbol (or type 'finish' to stop): ")
        if ticker.lower() == 'finish':
            print("\nChoose again.\n")
            break
        stock_algo.add_tickers_to_list(ticker)

def process_tickers(stock_algo: StockAlgorithm) -> None:
    if not stock_algo.tickers:
        print("No tickers added. Please add tickers first.")
        return
    
    directory = input(r"Enter directory for saving trade data (will be created if it doesn't exist): ")
    if not os.path.exists(directory):
        try:
            os.makedirs(directory)
        except OSError as e:
            print(f"Error creating directory: {e}")
            return

    stock_algo.process_all_tickers(directory)

def exit_program() -> None:
    """Exits the program."""
    print("Exiting the program.")
    exit()

def main():
    print("\nWelcome to Danti.\n")
    
    while True:
        try:
            initial_drawdown_percent = float(input("Enter drawdown percent (e.g., 5 for 5%): "))
            initial_day_range = int(input("\nHow many days until you would like to sell?: "))
            if initial_drawdown_percent <= 0 or initial_day_range <= 0:
                raise ValueError("Drawdown percent must be positive and day range must be a positive integer.")
            break
        except ValueError as e:
            print(f"Invalid input: {e}. Please try again.")

    stock_algo = StockAlgorithm(initial_drawdown_percent, initial_day_range)

    commands = {
        'update': lambda: print("Update function not implemented yet."),
        'add': lambda: add_tickers(stock_algo),
        'clear-list': stock_algo.clear_all_tickers,
        'run': lambda: process_tickers(stock_algo),
        'done': exit_program
    }

    while True:
        print("\nOptions: update, add, clear-list, run, done")
        user_input = input('User choice here: ').lower()

        if user_input in commands:
            if user_input == 'done':
                print("Exiting the program.")
                break
            commands[user_input]()
        else:
            print("Invalid input. Please try again.")



if __name__ == '__main__':
    main()