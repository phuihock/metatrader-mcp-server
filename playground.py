"""
MT5 Connection Playground
A simple script to demonstrate connecting to and disconnecting from MetaTrader 5
"""
import sys
import io
import os
from dotenv import load_dotenv

# Backup the original stdout
original_stdout = sys.stdout

# Redirect stdout to suppress output temporarily
sys.stdout = io.StringIO()

from MetaTraderMCPServer.client import MT5Client
from tabulate import tabulate

# Restore the original stdout
sys.stdout = original_stdout

def init():
    load_dotenv()
    config = {
        "login": int(os.getenv("LOGIN")),
        "password": os.getenv("PASSWORD"),
        "server": os.getenv("SERVER")
    }
    try:
        client = MT5Client(config)
        client.connect()
    except Exception as e:
        print(f"❌ Error: {e}")
    return client

def main():

    os.system('cls')

    # Open connection to MetaTrader 5 Terminal
    client = init()

    # Get list of open positions
    print("\n\n🪿 LIST ALL OPEN POSITIONS \n")
    open_positions = client.orders.get_all_positions()
    print(tabulate(open_positions, headers="keys", tablefmt="psql"))

    # Get list of pending orders
    print("\n\n🦢 LIST ALL PENDING ORDERS \n")
    pending_orders = client.orders.get_all_pending_orders()
    print(tabulate(pending_orders, headers="keys", tablefmt="psql"))

    # Place new market order
    print("\n\n🐶 PLACE NEW MARKET ORDERS \n")
    print("> Placing market order (BUY EURUSD 0.1 LOT)...")
    new_market_order_1 = client.orders.place_market_order(
        type="BUY",
        symbol="EURUSD",
        volume=0.1,
    )
    print(new_market_order_1["message"])
    print("\n")
    print("> Placing market order (SELL USDJPY 0.1 LOT)...")
    new_market_order_2 = client.orders.place_market_order(
        type="SELL",
        symbol="USDJPY",
        volume=0.1,
    )
    print(new_market_order_2["message"])
    print("\n")
    open_positions = client.orders.get_all_positions()
    print(tabulate(open_positions, headers="keys", tablefmt="psql"))


    # Place new pending orders
    print("\n\n🐱 PLACE NEW PENDING ORDERS \n")
    print("> Placing pending order (SELL GBPUSD 0.1 LOT at 1.32400)...")
    new_pending_order_1 = client.orders.place_pending_order(
        type="SELL",
        symbol="GBPUSD",
        volume=0.1,
        price=1.32400,
    )
    print(new_pending_order_1["message"])
    print("\n")
    print("> Placing pending order (BUY GBPUSD 0.1 LOT at 1.32100)...")
    new_pending_order_2 = client.orders.place_pending_order(
        type="BUY",
        symbol="GBPUSD",
        volume=0.1,
        price=1.32100,
    )
    print(new_pending_order_2["message"])
    print("\n")
    pending_orders = client.orders.get_all_pending_orders()
    print(tabulate(pending_orders, headers="keys", tablefmt="psql"))


    # Close MetaTrader 5 connection
    client.disconnect()

if __name__ == "__main__":
    main()
