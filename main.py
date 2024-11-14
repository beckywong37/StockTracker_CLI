"""
Provides UI design and major functionalities of the Stock Tracker CLI-based application
"""
# Import modules
import sys
from stocks import *

# Initialize colorama
init(autoreset=True)

# Create watchlist object that is global
watchlist = Watchlist()

def display_logo():
    print(Fore.GREEN+"""
            ____________            ______      ________                   ______              
        __  ___/_  /_______________  /__    ___  __/____________ _________  /______________
        _____ \_  __/  __ \  ___/_  //_/    __  /  __  ___/  __ `/  ___/_  //_/  _ \_  ___/
        ____/ // /_ / /_/ / /__ _  ,<       _  /   _  /   / /_/ // /__ _  ,<  /  __/  /    
        /____/ \__/ \____/\___/ /_/|_|      /_/    /_/    \__,_/ \___/ /_/|_| \___//_/                                                                                                                                                   
    """+ Style.RESET_ALL)

def display_welcome_page():
    """Displays welcome page with title and description of application"""
    display_logo()
    # Title and description
    print(Fore.GREEN+"""
        ==================================================================================
                       Welcome to Your Personalized Stock Tracker!
        ==================================================================================
            """+Fore.LIGHTBLUE_EX+"""
        Add stocks to your watchlist to keep track of them.
        Stay up to date with real time stock data.
        Disclaimer: This application is for informational purposes only and is not 
        intended to be personal financial advice. """+ Fore.YELLOW+"""
        Commands:
        -----------------------------------------------------------------------------------
        [1] Proceed to your Dashboard
        [q] Enter ‘q’ to exit
        -----------------------------------------------------------------------------------
    """)
    # User input to proceed or exit application
    cmd = input("Please enter a command: ").strip()
    # Process user input
    if cmd == "1":
        # Load watchlist from previous session
        watchlist.load_watchlist()
        display_dashboard()
    elif cmd == "q":
        exit_program()
    else:
        print("Invalid command. Please enter either 1 or q")
        display_welcome_page()

def display_dashboard():
    """Displays dashboard which includes watchlist"""
    display_logo()
    # Title
    print(Fore.GREEN + """
        ==================================================================================
                                Welcome to Your Dashboard!
        ================================================================================== """)
    display_major_market()
    print(Fore.LIGHTBLUE_EX + """
        To add stocks to your watchlist, enter 1 into the CLI.""")
    watchlist.display_watchlist()
    print(Fore.YELLOW + """
        Commands
        ----------------------------------------------------------------------------------
        [1] Edit your watchlist
        [2] View news articles
        [q] Enter ‘q’ to exit
        ----------------------------------------------------------------------------------""")
    # Get user input
    cmd = input("Please enter a command: ").strip()
    # Process user input
    if cmd == "1":
        display_watchlist()
    elif cmd == "2":
        display_news_page()
    elif cmd == "q":
        exit_program()
    else:
        print("Invalid command.")
        display_dashboard()

def display_watchlist():
    """Display page to edit watchlist"""
    # Start with default display
    show_commands = True
    sort_list = None
    while True:
        # Display sort_list and show commands
        if sort_list and show_commands:
            inform_watchlist_display(watchlist, sort_list)
        elif sort_list and not show_commands:
            clean_watchlist_display(watchlist, sort_list)
        elif show_commands:
            inform_watchlist_display(watchlist)
        else:
            clean_watchlist_display(watchlist)
        # Get user input
        cmd = input("Please enter a command: ").strip()
        # Return to dashboard if command = 1
        if cmd == "1":
            display_dashboard()
        # Toggle clean display (H to hide commands, S to show them again)
        elif cmd == "H":
            show_commands = False  # Hide commands
        elif cmd == "S":
            show_commands = True  # Show commands
        # If command length is 2, split into two variables
        elif len(cmd.split()) == 2:
            action, ticker = cmd.split()
            ticker = ticker.upper()
            # Validate ticker symbol
            if not validate_ticker(ticker):
                print(f"{ticker} is an invalid ticker symbol")
                continue
            # Process user input
            if action == "add":
                confirm = input(f"Are you sure you want to add {ticker} to your watchlist? You can always remove the stock if you change your mind! (Y/N):")
                if confirm == "Y":
                    # Fetch stock data and create stock object
                    stock_object = create_stock(ticker)
                    # Add to stock_object to watchlist
                    watchlist.add_stock(ticker, stock_object)
                elif confirm == "N":
                    print(f"{ticker} was not added to your watchlist.")
                else:
                    print(f"Invalid command. Enter Y/N")
            elif action == "remove":
                    confirm = input(f"Are you sure you want to remove {ticker} to your watchlist? "
                                    f"If removed, you can always re-add the stock back to your watchlist. (Y/N):")
                    if confirm == "Y":
                        watchlist.remove_stock(ticker)
                    elif confirm == "N":
                        print(f"{ticker} was not removed from your watchlist.")
                    else:
                        print(f"Invalid command. Enter Y/N")
            else:
                print("Invalid command. Use either add or remove followed by ticker symbol")
        elif len(cmd.split()) == 3:
            action, sortBy, sortOrder = cmd.split()
            sort_list = watchlist.sort_list(sortBy, sortOrder)
        else:
            print("Invalid command. Refer to list of commands for help")

def display_news_page():
    """News articles page"""
    # Title
    print(Fore.GREEN + """
        =======================================================================================================
                                                  Top News Articles
        ======================================================================================================= """)
    print(Fore.LIGHTBLUE_EX + """
        Enter '1' or '2' to view the top news articles today.""")
    print(Fore.YELLOW + """
        Commands
        --------------------------------------------------------------------------------------------------------
        [1] View top 3 business news articles
        [2] View top 3 articles from BBC News
        [3] Return to dashboard
        --------------------------------------------------------------------------------------------------------""")
    while True:
    # Get user input
        cmd = input("Please enter a command: ").strip()
        # Process user input
        url = ""
        if cmd == "1":
            url = 'http://127.0.0.1:5002/get_business_news'
        elif cmd == "2":
            url = 'http://127.0.0.1:5002/get_bbc_news'
        elif cmd == '3':
            display_dashboard()
        else:
            print("Invalid command.")
            display_news_page()
        # Get articles
        response = requests.post(url).json()
        for article in response:
            title = response[article]['title']
            date = response[article]['publishedAt']
            url = response[article]['url']
            print(Fore.LIGHTBLUE_EX + f"""
            Title: {title}
            Date: {date}
            Url: {url}""")

def clean_watchlist_display(watchlist, sort_list=None):
    """When user enters H, commands are hidden to provide cleaner display"""
    print(Fore.GREEN + """
        ===================================================================================
                                    Welcome to Your Watchlist!
        =================================================================================== """ + Fore.LIGHTBLUE_EX + """
        To add or remove stocks from your watchlist, enter:
        add [ticker] | remove [ticker]
        Example: add AAPL | remove AAPL""")
    if sort_list is None:
        watchlist.display_watchlist()
    else:
        watchlist.display_watchlist(sort_list)
    print(Fore.YELLOW + """
        [Commands are currently hidden. Enter ‘S’ to show commands.]
        ----------------------------------------------------------------------------------""")

def inform_watchlist_display(watchlist, sort_list=None):
    """Default display """
    print(Fore.GREEN + """
        ===================================================================================
                                    Welcome to Your Watchlist!
        =================================================================================== """ + Fore.LIGHTBLUE_EX + """
        To add or remove stocks from your watchlist, enter:
        add [ticker] | remove [ticker]
        Example: add AAPL | remove AAPL""")
    if sort_list is None:
        watchlist.display_watchlist()
    else:
        watchlist.display_watchlist(sort_list)
    print(Fore.YELLOW + """
        Commands (Enter ‘H’ to hide commands)
        ----------------------------------------------------------------------------------
        add [ticker] : to add stock to watchlist 
        remove [ticker] : to remove stock from watchlist
        sort [sortBy] [sortOrder] : sortBy opt (ticker, price), sortOrder (asc, dsc)
        [1] : to return to dashboard 
        [H] : Hide list of commands
        [S] : Show list of commands
        ---------------------------------------------------------------------------------""")

def display_major_market():
    """Creates display for major market indices. Intended to be displayed on the dashboard"""
    # Post request to Microservice B
    url = 'http://127.0.0.1:5001/get_stock_data'
    # Request includes url
    response = requests.post(url)
    data = response.json()
    # Store data in variables
    sp500_change = data['^GSPC']['change']
    sp500_open = data['^GSPC']['open']
    dow_change = data['^DJI']['change']
    dow_open = data['^DJI']['open']
    nasdaq_change = data['^IXIC']['change']
    nasdaq_open = data['^IXIC']['open']
    # Display
    print(Fore.CYAN + f"""
        Major Stock Indices:
        ----------------------------------------------------------------------------------
        |        S&P 500          |            NASDAQ          |        Dow Jones        |
        | Open Price: {sp500_open:<11} | Open Price: {nasdaq_open:<14} | Open Price: {dow_open:<11} |
        | Percent Change: {sp500_change:<7} | Percent Change: {nasdaq_change:<10} | Percent Change: {dow_change:<7} |
        ----------------------------------------------------------------------------------
        """)

def exit_program():
    """Exits program"""
    print("Exiting program.")
    sys.exit(0)
