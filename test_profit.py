#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Test script for calculate_profit function
"""
import MetaTrader5 as mt5
from tabulate import tabulate
from MetaTraderMCPServer.client.functions.calculate_profit import calculate_profit

# Initialize connection to MetaTrader 5
if not mt5.initialize():
    print(f"❌ Failed to initialize MT5: {mt5.last_error()}")
    quit()

# Test the calculate_profit function
print("====================")
print("💵 PROFIT CALCULATION")
print("====================\n")

# Parameters for testing
symbols = ["EURUSD", "GBPUSD", "USDJPY", "XAUUSD"]
volume = 0.1
pip_movement = 100  # 100 pips

profit_results = []

for symbol in symbols:
    # Get current price
    tick = mt5.symbol_info_tick(symbol)
    if tick is None:
        print(f"❌ Failed to get tick data for {symbol}")
        continue
    
    # Get symbol info for point value
    symbol_info = mt5.symbol_info(symbol)
    if symbol_info is None:
        print(f"❌ Failed to get symbol info for {symbol}")
        continue
        
    # Calculate pip value (usually 0.0001 for 4-digit symbols, 0.00001 for 5-digit)
    point = symbol_info.point
    pip_size = 10 * point  # 10 points = 1 pip for most forex pairs
    
    # Buy scenario (open at ask, close higher)
    buy_open = tick.ask
    buy_close = buy_open + (pip_movement * pip_size)
    buy_profit = calculate_profit("BUY", symbol, volume, buy_open, buy_close)
    
    # Sell scenario (open at bid, close lower)
    sell_open = tick.bid
    sell_close = sell_open - (pip_movement * pip_size)
    sell_profit = calculate_profit("SELL", symbol, volume, sell_open, sell_close)
    
    # Add results to table
    if buy_profit is not None and sell_profit is not None:
        profit_results.append({
            "Symbol": symbol,
            "Movement": f"{pip_movement} pips",
            "Buy Profit": f"{buy_profit:.2f}",
            "Sell Profit": f"{sell_profit:.2f}",
            "Profit per Pip": f"{(buy_profit/pip_movement):.2f}"
        })

# Display results in a pretty table
print(tabulate(profit_results, headers='keys', tablefmt='fancy_grid'))
print("\nNote: Profit calculations assume the specified pip movement in favorable direction")

# Shutdown connection
mt5.shutdown()
