"""
Creates the Stock object and Watchlist object
"""

import yfinance as yf
from colorama import init, Fore, Style
import requests


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

    def conv_dict(self):
        """Convert stock to dictionary format for microservice A"""
        return {
            "ticker": self.ticker,
            "price": self.price,
            "change": self.change,
            "high_52": self.high_52,
            "low_52": self.low_52,
            "recommend": self.recommend
        }

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
        self.save_watchlist()

    def remove_stock(self, ticker):
        """Remove ticker attribute of stock object from stock list"""
        for stock in self.stock_list:
            if stock.ticker == ticker:
                self.stock_list.remove(stock)
                print(f"{ticker} has been successfully removed from your watchlist")
                self.save_watchlist()
                return
        print(f"{ticker} is not in watchlist.")

    def get_json(self):
        """Converts stock list into a JSON object. Use for Microservice A"""
        return [stock.conv_dict() for stock in self.stock_list]

    def sort_list(self, sortBy, sortOrder):
        """Sorts stock list by 'sortBy' and 'sortOrder' """
        url = "https://stocksortingservice.onrender.com/stocksort"
        data = {
            "sortBy" : sortBy,
            "sortOrder" : sortOrder,
            "stocks" : self.get_json()
        }
        response = requests.post(url, json=data)
        if response.status_code == 200:
            sort_list = response.json()
            return sort_list
        else:
            print("error")

    def save_watchlist(self):
        """Saves watchlist to Microservice D"""
        url = 'http://127.0.0.1:5003/save_watchlist'
        # Converts stock list to json format
        data = {"watchlist": self.get_json()}
        response = requests.post(url, json=data)
        if response.status_code == 200:
            print("Watchlist saved successfully")
        else:
            print("Save unsuccessful")

    def load_watchlist(self):
        """Loads watchlist saved in Microservice D"""
        url = 'http://127.0.0.1:5003/load_watchlist'
        # Gets watchlist from microservice
        response = requests.get(url)
        if response.status_code == 200:
            watchlist_data = response.json()
            # Create stock object and add to stock_list
            for stock_data in watchlist_data:
                stock = Stock(ticker=stock_data['ticker'],
                              price=stock_data['price'],
                              change=stock_data['change'],
                              high_52=stock_data['high_52'],
                              low_52=stock_data['low_52'],
                              recommend=stock_data['recommend'])
                self.stock_list.append(stock)

    def print_stock_list(self):
        """Prints stock objects currently in stock list"""
        for stock in self.stock_list:
            print(stock)

    def display_watchlist(self, sort_list=None):
        """Displays watchlist"""
        # If sort_list is not None, display sort_list
        if sort_list is None:
            stock_to_display = self.stock_list
        else:
            stock_to_display = sort_list
        # If stock_list is empty, print empty table
        if len(self.stock_list) == 0:
            print(Fore.RED +f"""
        Stock Watchlist:
        ----------------------------------------------------------------------------------------
        | Ticker  | Price     | % Change  | 52W Low/High   | Recommendation |
        ----------------------------------------------------------------------------------------
        [empty]
        ----------------------------------------------------------------------------------------
            """)
        # If not empty, print each stock and info into watchlist
        else:
            print(Fore.RED +f"""
        Stock Watchlist:
        -----------------------------------------------------------------------------------
        | Ticker    | Price      | % Change   | 52W Low/High      | Recommendation |
        -----------------------------------------------------------------------------------""")
            for stock in stock_to_display:
                # If stock is a dictionary, use this format
                if isinstance(stock, dict):
                    print(
                        Fore.RED + f"        | {stock['ticker']:<9} | {stock['price']:<10} | {stock['change']:<10} | {stock['low_52']}/{stock['high_52']:<9} | {stock['recommend']}")
                # If stock is an object, use this format
                else:
                    print(Fore.RED + f"        | {stock.ticker:<9} | {stock.price:<10} | {stock.change:<10} | {stock.low_52}/{stock.high_52:<10} | {stock.recommend}")
            print(Fore.RED + "        -----------------------------------------------------------------------------------")


# stock1 = create_stock('AAPL')
# stock2 = create_stock('TSLA')
# watchlist = Watchlist()
# watchlist.add_stock('AAPL', stock1)
# watchlist.add_stock('TSLA', stock2)
# watchlist.save_watchlist()
# watchlist.load_watchlist()
# watchlist.display_watchlist()
# watchlist.get_json()
# watchlist.sort_list('price', 'dsc')
# # watchlist.add_stock(stock2)
# watchlist.display_watchlist()
# watchlist.remove_stock(stock1.ticker)
# watchlist.display_watchlist()