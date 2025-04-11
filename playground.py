#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
MT5 Connection Playground
A simple script to demonstrate connecting to and disconnecting from MetaTrader 5
"""
import sys
import io

# Backup the original stdout
original_stdout = sys.stdout

# Redirect stdout to suppress output temporarily
sys.stdout = io.StringIO()

import MetaTrader5 as mt5
import time
from MetaTraderMCPServer.client.client import MT5Client
from MetaTraderMCPServer.client.connection import MT5Connection
from tabulate import tabulate

# Restore the original stdout
sys.stdout = original_stdout

def init():
    config = { "login": 240294046, "password": "ExnessDemo123!", "server": "Exness-MT5Trial6" }
    try:
        client = MT5Client(config)
        client.connect()
    except Exception as e:
        print(f"❌ Error: {e}")
    return client

def main():
    client = init()
  
    # gold = client.market.get_candles_by_date("XAUUSD", "D1", "2025-04-10 00:00", "2025-01-10 23:59")
    # print(gold)

    print("\n\n")

    # Get all pending orders
    all_orders = client.orders.get_all_pending_orders()
    print(tabulate(all_orders, headers='keys', tablefmt='fancy_grid'))

    # Get pending orders for a specific symbol
    xauusd_orders = client.orders.get_pending_orders_by_symbol("XAUUSD")
    print(tabulate(xauusd_orders, headers='keys', tablefmt='fancy_grid'))

    # Get pending orders for a specific currency
    usd_orders = client.orders.get_pending_orders_by_currency("USD")
    print(tabulate(usd_orders, headers='keys', tablefmt='fancy_grid'))

    # Get a specific pending order by ID
    order = client.orders.get_pending_orders_by_id(1642078070)
    print(tabulate(order, headers='keys', tablefmt='fancy_grid'))

    # all_positions = client.orders.get_all_positions()
    # print(tabulate(all_positions, headers='keys', tablefmt='fancy_grid'))

    # print("\n\n")

    # xauusd_positions = client.orders.get_positions_by_symbol("XAUUSD")
    # print(tabulate(xauusd_positions, headers='keys', tablefmt='fancy_grid'))

    # print("\n\n")

    # position = client.orders.get_position_by_id(1651409559)
    # print(tabulate(position, headers='keys', tablefmt='fancy_grid'))

    # print("==============")
    # print("OPEN POSITIONS")
    # print("==============\n")
    # orders = client.orders.get_positions()
    # print(tabulate(orders, headers='keys', tablefmt='fancy_grid'))

    # print("\n")

    # print("==============")
    # print("PENDING ORDERS")
    # print("==============\n")
    # orders = client.orders.get_pending_orders(symbol_name="XAUUSD")
    # print(tabulate(orders, headers='keys', tablefmt='fancy_grid'))
    
    
    print("\n\n")
    
    client.disconnect()

if __name__ == "__main__":
    main()
