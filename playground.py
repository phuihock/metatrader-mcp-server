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
  
    orders = client.orders._getPositions(ticket="1650804616")
    print(tabulate(orders, headers='keys', tablefmt='fancy_grid'))

    client.disconnect()

if __name__ == "__main__":
    main()

