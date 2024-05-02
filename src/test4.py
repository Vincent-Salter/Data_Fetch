import yfinance as yf
from datetime import datetime, timedelta
from methods import trading_bot_methods
from testing_methods import UpdateData

# Copyright Vincent Salter 02/12/23 2nd of December 2023

class StockAlgorithm:

    def __init__(self, drawdown_percent, day_range):
        self.drawdown_percent = drawdown_percent
        self.day_range = day_range
        self.start_date = (datetime.now() - timedelta(days=365)).strftime('%Y-%m-%d')
        self.end_date = datetime.now().strftime('%Y-%m-%d')
        self.tickers = []

    def fetch_stock_data(self, stock_symbol, start_date, end_date):
        stock_data = yf.download(stock_symbol, start=start_date, end=end_date)
        return stock_data
    
    def set_drawdown_percent(self, new_drawdown_percent):
        self.drawdown_percent = new_drawdown_percent

    def set_day_range(self, new_day_range):
        self.day_range = new_day_range

    def set_date_range(self, new_start_date, new_end_date):
        self.start_date = new_start_date
        self.end_date = new_end_date

    def add_tickers_to_list(self, ticker):
        if ticker not in self.tickers:
            self.tickers.append(ticker)
        else:
            print(f'{ticker} is already in the list.')
            #can i add here a method that would add a list to the object if you wanted to pull multiple tickers add them to a list then process them all

    def process_all_tickers(self, directory):
        for ticker in self.tickers:
            print(f"Processing {ticker}...")
            stock_data = self.fetch_stock_data(ticker, self.start_date, self.end_date)
            trades = trading_bot_methods.backtest_strategy(stock_data, self.drawdown_percent, self.day_range)
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


def main():
    print("\nWelcome to Danti.")
    print("Please input your parameters.\n")
    initial_drawdown_percent = trading_bot_methods.get_float_input("Enter drawdown percent (e.g., 5 for 5%): ")
    initial_day_range = trading_bot_methods.get_int_input("How many days until you would like to sell?: ")
    stock_algo = StockAlgorithm(initial_drawdown_percent, initial_day_range)
    print("\nOptions: 'update', 'add', 'run', 'done'")

    while True:
        user_input = input('\nUser choice here: ').lower()

        if user_input == 'update':
            UpdateData.update_stock_algo(stock_algo)
        elif user_input == 'add':
            tickers = input("Enter tickers separated by comma (press 'enter' to stop): ")
            if tickers.lower() == 'finish':
                continue
            tickers_to_add = [ticker.strip().upper() for ticker in tickers.split(',')]
            for ticker in tickers_to_add:
                stock_algo.add_tickers_to_list(ticker)
        elif user_input == 'run':
            if not stock_algo.tickers:
                print("No tickers added. Please add tickers first.")
            else:
                directory = input(r"Enter directory for saving all trade data: ")
                stock_algo.process_all_tickers(directory)
        elif user_input == 'done':
            print("Exiting the program.")
            break
        else:
            print("Invalid input. Available commands: 'update', 'add', 'run', 'done'.")

if __name__ == '__main__':
    main()