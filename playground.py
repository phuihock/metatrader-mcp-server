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
from MetaTraderMCPServer.client.functions.calculate_margin import calculate_margin
from MetaTraderMCPServer.client.functions.calculate_profit import calculate_profit
from MetaTraderMCPServer.client.functions.send_order import send_order
from MetaTraderMCPServer.client.types import OrderType, TradeRequestActions
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

	# Place an order
	# BUY BTCUSD 1 LOT
	buy_response = send_order(
		client._connection,
		action=TradeRequestActions.DEAL,
		order_type="BUY",
		symbol="BTCUSD",
		volume=1,
	)
	print(buy_response)

	client.disconnect()

if __name__ == "__main__":
	main()
