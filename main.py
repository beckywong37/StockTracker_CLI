"""
This will display the welcome screen when the app is launched f
"""
# Import modules
from colorama import init, Fore, Style
from stocks import *

# Initialize colorama
init(autoreset=True)

# Create watchlist object that is global
watchlist = Watchlist()

def display_logo():
    print(Fore.GREEN +"""
     $$$$$$\    $$\                         $$\    $$$$$$$$\                           $$\                           
    $$  __$$\   $$ |                        $$ |   \__$$  __|                          $$ |                          
    $$ /  \__|$$$$$$\    $$$$$$\   $$$$$$$\ $$ |  $$\ $$ | $$$$$$\  $$$$$$\   $$$$$$$\ $$ |  $$\  $$$$$$\   $$$$$$\  
    \$$$$$$\  \_$$  _|  $$  __$$\ $$  _____|$$ | $$  |$$ |$$  __$$\ \____$$\ $$  _____|$$ | $$  |$$  __$$\ $$  __$$\ 
     \____$$\   $$ |    $$ /  $$ |$$ /      $$$$$$  / $$ |$$ |  \__|$$$$$$$ |$$ /      $$$$$$  / $$$$$$$$ |$$ |  \__|
    $$\   $$ |  $$ |$$\ $$ |  $$ |$$ |      $$  _$$<  $$ |$$ |     $$  __$$ |$$ |      $$  _$$<  $$   ____|$$ |      
    \$$$$$$  |  \$$$$  |\$$$$$$  |\$$$$$$$\ $$ | \$$\ $$ |$$ |     \$$$$$$$ |\$$$$$$$\ $$ | \$$\ \$$$$$$$\ $$ |      
     \______/    \____/  \______/  \_______|\__|  \__|\__|\__|      \_______| \_______|\__|  \__| \_______|\__|                                                                                                                                                             
    """+ Style.RESET_ALL)

def display_welcome_page():
    """Displays welcome page with title and description of application"""
    display_logo()
    # Title and description
    print(Fore.GREEN+"""
    ========================================================
          Welcome to Your Personalized Stock Tracker!
    ========================================================
        """+Fore.LIGHTBLUE_EX+"""
    Add stocks to your watchlist to keep track of them.
    Stay up to date with real time stock data."""+ Fore.YELLOW+"""
    --------------------------------------------------------
    [1] Proceed to your Dashboard
    [q] Enter ‘q’ to exit
    --------------------------------------------------------
    """)
    # User input to proceed or exit application
    cmd = input("Please enter a command: ").strip()
    # Process user input
    if cmd == "1":
        display_dashboard()
    elif cmd == "q":
        print("Exiting program.")
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
        ================================================================================== """ + Fore.LIGHTBLUE_EX + """
        To add stocks to your watchlist, enter 1 into the CLI.""")
    watchlist.display_watchlist()
    print(Fore.YELLOW + """
        ----------------------------------------------------------------------------------
        [1] Edit your watchlist
        [q] Enter ‘q’ to exit
        ----------------------------------------------------------------------------------""")
    # Get user input
    cmd = input("Please enter a command: ").strip()
    # Process user input
    if cmd == "1":
        display_watchlist()
    elif cmd == "q":
        print("Exiting program.")
    else:
        print("Invalid command. Please enter either 1 or q")
        display_dashboard()


def display_watchlist():
    """Display page to edit watchlist"""
    # Start with default display
    show_commands = True
    while True:
        # Start with default display
        if show_commands:
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
                    confirm = input(f"Are you sure you want to remove {ticker} to your watchlist? If removed, you can always re-add the stock back to your watchlist. (Y/N):")
                    if confirm == "Y":
                        watchlist.remove_stock(ticker)
                    elif confirm == "N":
                        print(f"{ticker} was not removed from your watchlist.")
                    else:
                        print(f"Invalid command. Enter Y/N")
            else:
                print("Invalid command. Use either add or remove followed by ticker symbol")
        else:
            print("Invalid command. Refer to list of commands for help")


def clean_watchlist_display(watchlist):
    """When user enters H, commands are hidden to provide cleaner display"""
    print(Fore.GREEN + """
        ==================================================================================
                                Welcome to Your Watchlist!
        ================================================================================== """ + Fore.LIGHTBLUE_EX + """
        To add or remove stocks from your watchlist, enter:
        add [ticker] | remove [ticker]
        Example: add AAPL | remove AAPL""")
    watchlist.display_watchlist()
    print(Fore.YELLOW + """
        [Commands are currently hidden. Enter ‘S’ to show commands.]
        ----------------------------------------------------------------------------------""")

def inform_watchlist_display(watchlist):
    """Default display """
    print(Fore.GREEN + """
        ==================================================================================
                                Welcome to Your Watchlist!
        ================================================================================== """ + Fore.LIGHTBLUE_EX + """
        To add or remove stocks from your watchlist, enter:
        add [ticker] | remove [ticker]
        Example: add AAPL | remove AAPL""")
    watchlist.display_watchlist()
    print(Fore.YELLOW + """
        Commands (Enter ‘H’ to hide commands)
        ----------------------------------------------------------------------------------
        add [ticker] : to add stock to watchlist 
        remove [ticker] : to remove stock from watchlist
        [1] : to return to dashboard 
        [H] : Hide list of commands
        [S] : Show list of commands
        ----------------------------------------------------------------------------------""")

# display_welcome_page()
display_watchlist()