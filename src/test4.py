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
            filename = f"{ticker}_{self.drawdown_percent}%_{self.day_range}.csv"
            trading_bot_methods.export_trades_to_csv(trades, directory, filename)
            print(f"{ticker} data saved in {directory}") ##here i need to add automation to the process_stock method where if a list is invoked it runs all objects in the list without interuption
                                  ##such as no plotting the data or asking each time where to save the file, they all need to be passed to the same directory
    def need_method_here_to_process_only_list():
        pass
    def process_stock(self, ticker):
        stock_data = self.fetch_stock_data(ticker, self.start_date, self.end_date)
        if stock_data.empty:
            print("No data fetched. Check your stock symbol and date range.")
        else:
            trades = trading_bot_methods.backtest_strategy(stock_data, self.drawdown_percent, self.day_range)
            if not trades:
                print("No qualifying trades found.")
            else:
                total_profit = sum(trade[4] for trade in trades)
                print(f"Total number of trades: {len(trades)}")
                print(f"Total profit: {total_profit}")
                while True:
                    plot_y_n = input("Would you like to plot the data? Please enter yes or no: ")
                    if plot_y_n.lower() == "yes":
                        trading_bot_methods.plot_trades(stock_data, trades) ##add tickers to a list and process them all at once, give a directory for them all to be saved to. Not to be asked to save to a directory multiple times
                        break
                    elif plot_y_n.lower() == "no":
                        break
                    else:
                        print("Incorrect input please try again.")
                
                filename = f"{ticker}_{self.drawdown_percent}%_{self.day_range}.csv"
                directory = input(r"Enter directory here: ")
                trading_bot_methods.export_trades_to_csv(trades, directory, filename)
                print(f"File saved to directory: {directory}")#how do i print a new line above here

print("Welcome to Danti.")
print("Please input your parameters here.\n")
initial_drawdown_percent = float(input("Enter drawdown percent (e.g., 5 for 5%) here: "))
initial_day_range = int(input("How many days until you would like to sell?: "))

#stock_algo is the self, the self. is just changing the propreys or attributes of the object
stock_algo = StockAlgorithm(initial_drawdown_percent, initial_day_range) #how is this row here assigned\\\\ creating an instance of the class to use it in the program
print()
print("If you would like to update your parameters please type 'update' or type 'done' to finish.\n")
print("Also if you would like to add multiple tickers to a list type 'add', then type 'run' to process all.\n")

while True:
    user_input = input('User choice here: ') #assign this user_input object a property

    if user_input.lower() == 'update': #1st thought, check if the object has the property 'update' ##"If what sits inside that object(user_input) is the value 'update' do whats below."
        UpdateData.update_stock_algo(stock_algo)

    elif user_input.lower() == 'add':
        while True:
            tickers_to_add = input("Tickers to add here (type 'finish' to stop.): ")
            if tickers_to_add == 'finish':
                print()
                print("Please choose again what you would like to do.\n")
                break
            else:
                stock_algo.add_tickers_to_list(tickers_to_add)

    elif user_input.lower() == 'run':
        stock_algo.process_all_tickers()

    elif user_input.lower() == 'done':
        break
    
    else:
       stock_algo.process_stock(user_input)

