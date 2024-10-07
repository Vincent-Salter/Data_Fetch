import yfinance as yf

# Download the data
def fetch_stock_data(x):
    data = yf.download(x)
    return data

def fetch_open_price(y, n):  
    for index, row in y.head(n).iterrows():
        clean_date = index.strftime('%Y-%m-%d')
        print(f"{clean_date} {row['Open']}")

def fetch_close_price(close, n):  
    for index, row in close.head(n).iterrows():
        clean_date = index.strftime('%Y-%m-%d')
        print(f"{clean_date} {row['Close']}")

def fetch_open_close_price(open_close, n):  # Add n to specify the number of rows
    print("Open Prices:")
    fetch_open_price(open_close, n)  
    print("\nClose Prices:")
    fetch_close_price(open_close, n)  

# Fetch the stock data and store it in data_object1
data_object1 = fetch_stock_data("TSLA")

# Fetch and print the first few open and close prices
fetch_open_close_price(data_object1, n=10)  # Specify how many rows to print (e.g., 3)
