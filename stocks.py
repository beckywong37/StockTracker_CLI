"""
Creates the Stock object and Watchlist object
"""
from venv import create

import yfinance as yf
from colorama import init, Fore, Style


def validate_ticker(ticker):
    """Returns True if valid ticker symbol"""
    # Use yahoo finance Ticker functionality to create ticker object for stock
    stock = yf.Ticker(ticker)
    # Use stock.info function from yf to get data
    stock_data = stock.info
    # If valid ticker symbol, it should show current price as a data attribute
    if 'currentPrice' in stock_data:
        return True
    else:
        return False

def create_stock(ticker):
    """Given a ticker, fetches stock info and returns stock object"""
    # Use yahoo finance Ticker functionality to create ticker object for stock
    stock = yf.Ticker(ticker)
    # Use stock.info function from yf to get data
    stock_data = stock.info
    # Calculate % change
    change = (stock_data.get('currentPrice') - stock_data.get('regularMarketPreviousClose')) / stock_data.get('regularMarketPreviousClose') *100
    return Stock(
        ticker,
        stock_data.get('currentPrice'),
        round(change, 2),
        stock_data.get('fiftyTwoWeekHigh'),
        stock_data.get('fiftyTwoWeekLow'),
        stock_data.get('recommendationKey')
    )


class Stock:
    def __init__(self, ticker, price, change, high_52, low_52, recommend):
        """Initialize stock and data"""
        # Create stock object if passes validate_ticker
        self.ticker = ticker
        self.price = price
        self.change = change
        self.high_52 = high_52
        self.low_52 = low_52
        self.recommend = recommend

    def __str__(self):
        """Print stock details"""
        return f"Ticker: {self.ticker}, Price: {self.price}, % Change: {self.change}, 52 Week High: {self.high_52}, 52 Week Low: {self.low_52}"

class Watchlist:
    def __init__(self):
        """Initialize watchlist"""
        self.stock_list = []

    def add_stock(self, ticker, stock_object):
        """Add ticker attribute of stock object to stock list"""
        # If stock already in watchlist, return
        for stock in self.stock_list:
            if stock.ticker == ticker:
                print(f"{ticker} is already in watchlist")
                return
        # If stock is not in watchlist, append
        self.stock_list.append(stock_object)
        print(f"{stock_object.ticker} has been successfully added to your watchlist")

    def remove_stock(self, ticker):
        """Remove ticker attribute of stock object from stock list"""
        for stock in self.stock_list:
            if stock.ticker == ticker:
                self.stock_list.remove(stock)
                print(f"{ticker} has been successfully removed from your watchlist")
                return
        print(f"{ticker} is not in watchlist.")

    def print_stock_list(self):
        """Prints stock objects currently in stock list"""
        for stock in self.stock_list:
            print(stock)

    def display_watchlist(self):
        """Displays watchlist"""
        # If stock_list is empty, print empty table
        if len(self.stock_list) == 0:
            print(Fore.RED +f"""
        Stock Watchlist:
        -----------------------------------------------------------------------------------
        | Ticker  | Price     | % Change  | 52W Low/High   | Recommendation |
        -----------------------------------------------------------------------------------
        [empty]
        -----------------------------------------------------------------------------------
            """)
        # If not empty, print each stock and info into watchlist
        else:
            print(Fore.RED +f"""
        Stock Watchlist:
        -----------------------------------------------------------------------------------
        | Ticker  | Price     | % Change  | 52W Low/High   | Recommendation |
        -----------------------------------------------------------------------------------""")
            for stock in self.stock_list:
                print(Fore.RED + f"        | {stock.ticker:<7} | {stock.price:<9} | {stock.change:<9} | {stock.low_52}/{stock.high_52:<7} | {stock.recommend}")
            print(Fore.RED + "        -----------------------------------------------------------------------------------")

# print(validate_ticker('AAPL'))
# stock1 = create_stock('AAPL')
# # stock2 = create_stock('TSLA')
# watchlist = Watchlist()
# watchlist.add_stock('AAPL', stock1)
# # watchlist.add_stock(stock2)
# watchlist.display_watchlist()
# watchlist.remove_stock(stock1.ticker)
# watchlist.display_watchlist()