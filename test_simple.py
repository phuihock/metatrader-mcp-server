#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Simple test script for price target calculation functions
"""
import MetaTrader5 as mt5
from tabulate import tabulate
from MetaTraderMCPServer.client.functions.calculate_profit import calculate_profit
from MetaTraderMCPServer.client.functions.calculate_price_targets import (
    calculate_take_profit,
    calculate_stop_loss
)

# Initialize connection to MetaTrader 5
if not mt5.initialize():
    print(f"❌ Failed to initialize MT5: {mt5.last_error()}")
    quit()

# Pick one test symbol
symbol = "EURUSD"
volume = 0.1
positive_target = 100  # $100 profit
negative_target = -50  # $50 loss

# Get current price
tick = mt5.symbol_info_tick(symbol)
if tick is None:
    print(f"❌ Failed to get tick data for {symbol}")
    quit()

buy_entry = tick.ask
sell_entry = tick.bid

print(f"Testing price targets for {symbol}:")
print(f"Buy Entry Price: {buy_entry}")
print(f"Sell Entry Price: {sell_entry}")
print("\n1. TAKE PROFIT CALCULATIONS:")

# BUY with positive target (standard take profit)
buy_tp_profit = calculate_take_profit("BUY", symbol, volume, buy_entry, positive_target)
if buy_tp_profit:
    actual = calculate_profit("BUY", symbol, volume, buy_entry, buy_tp_profit)
    print(f"BUY TP for +${positive_target} profit: {buy_tp_profit} (Actual profit: ${actual:.2f})")

# BUY with negative target (cut losses)
buy_tp_loss = calculate_take_profit("BUY", symbol, volume, buy_entry, negative_target)
if buy_tp_loss:
    actual = calculate_profit("BUY", symbol, volume, buy_entry, buy_tp_loss)
    print(f"BUY TP for ${negative_target} loss: {buy_tp_loss} (Actual profit: ${actual:.2f})")

# SELL with positive target (standard take profit)
sell_tp_profit = calculate_take_profit("SELL", symbol, volume, sell_entry, positive_target)
if sell_tp_profit:
    actual = calculate_profit("SELL", symbol, volume, sell_entry, sell_tp_profit)
    print(f"SELL TP for +${positive_target} profit: {sell_tp_profit} (Actual profit: ${actual:.2f})")

# SELL with negative target (cut losses)
sell_tp_loss = calculate_take_profit("SELL", symbol, volume, sell_entry, negative_target)
if sell_tp_loss:
    actual = calculate_profit("SELL", symbol, volume, sell_entry, sell_tp_loss)
    print(f"SELL TP for ${negative_target} loss: {sell_tp_loss} (Actual profit: ${actual:.2f})")

print("\n2. STOP LOSS CALCULATIONS:")

# BUY with negative target (standard stop loss)
buy_sl_loss = calculate_stop_loss("BUY", symbol, volume, buy_entry, negative_target)
if buy_sl_loss:
    actual = calculate_profit("BUY", symbol, volume, buy_entry, buy_sl_loss)
    print(f"BUY SL for ${negative_target} loss: {buy_sl_loss} (Actual profit: ${actual:.2f})")

# BUY with positive target (lock in profits)
buy_sl_profit = calculate_stop_loss("BUY", symbol, volume, buy_entry, positive_target)
if buy_sl_profit:
    actual = calculate_profit("BUY", symbol, volume, buy_entry, buy_sl_profit)
    print(f"BUY SL to lock in +${positive_target} profit: {buy_sl_profit} (Actual profit: ${actual:.2f})")

# SELL with negative target (standard stop loss)
sell_sl_loss = calculate_stop_loss("SELL", symbol, volume, sell_entry, negative_target)
if sell_sl_loss:
    actual = calculate_profit("SELL", symbol, volume, sell_entry, sell_sl_loss)
    print(f"SELL SL for ${negative_target} loss: {sell_sl_loss} (Actual profit: ${actual:.2f})")

# SELL with positive target (lock in profits)
sell_sl_profit = calculate_stop_loss("SELL", symbol, volume, sell_entry, positive_target)
if sell_sl_profit:
    actual = calculate_profit("SELL", symbol, volume, sell_entry, sell_sl_profit)
    print(f"SELL SL to lock in +${positive_target} profit: {sell_sl_profit} (Actual profit: ${actual:.2f})")

# Shutdown connection
mt5.shutdown()
