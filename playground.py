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

	# Close pending order
	close_pending_response = send_order(
		client._connection,
		action=TradeRequestActions.REMOVE,
		order=1653847435
	)
	print(close_pending_response)

	# Close an open position
	# close_response = send_order(
	# 	client._connection,
	# 	action=TradeRequestActions.DEAL,
	# 	position=1661367229,
	# 	order_type="SELL",
	# 	symbol="BTCUSD",
	# 	volume=1,
	# )
	# print(close_response)

	# # Modify a pending order
	# modify_response = send_order(
	# 	connection=client._connection,
	# 	action=TradeRequestActions.MODIFY,
	# 	order=1653847435,
	# 	stop_loss=3000,
	# 	take_profit=4000,
	# 	price=3200,
	# )
	# print(modify_response)

	# Modify SL/TP of an open order
	# sltp_response = send_order(
	# 	connection=client._connection,
	# 	action=TradeRequestActions.SLTP,
	# 	position=1661365021,
	# 	stop_loss=83500,
	# 	take_profit=86000,
	# 	symbol=None,
	# 	order_type=None,
	# 	volume=None,
	# )
	# print(sltp_response)

	# Place a pending order
	# pending_response = send_order(
	# 	client._connection,
	# 	action=TradeRequestActions.PENDING,
	# 	order_type="BUY_LIMIT",
	# 	symbol="BTCUSD",
	# 	volume=1,
	# 	price=84000,
	# )
	# print(pending_response)

	# Place a market execution
	# BUY BTCUSD 1 LOT
	# buy_response = send_order(
	# 	client._connection,
	# 	action=TradeRequestActions.DEAL,
	# 	order_type="BUY",
	# 	symbol="BTCUSD",
	# 	volume=1,
	# )
	# print(buy_response)

	client.disconnect()

if __name__ == "__main__":
	main()
