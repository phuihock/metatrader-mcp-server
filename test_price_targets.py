#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Test script for calculate_take_profit and calculate_stop_loss functions
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

print("====================")
print("🎯 PRICE TARGET CALCULATION")
print("====================\n")

# Parameters for testing
symbols = ["EURUSD", "GBPUSD", "USDJPY", "XAUUSD"]
volume = 0.1
positive_target = 100  # $100 profit
negative_target = -50  # $50 loss

# Create results table
results = []

for symbol in symbols:
    # Get current price
    tick = mt5.symbol_info_tick(symbol)
    if tick is None:
        print(f"❌ Failed to get tick data for {symbol}")
        continue
    
    buy_entry = tick.ask
    sell_entry = tick.bid
    
    # Test all 4 combinations for take profit
    buy_tp_profit = calculate_take_profit("BUY", symbol, volume, buy_entry, positive_target)
    buy_tp_loss = calculate_take_profit("BUY", symbol, volume, buy_entry, negative_target)
    sell_tp_profit = calculate_take_profit("SELL", symbol, volume, sell_entry, positive_target)
    sell_tp_loss = calculate_take_profit("SELL", symbol, volume, sell_entry, negative_target)
    
    # Test all 4 combinations for stop loss  
    buy_sl_loss = calculate_stop_loss("BUY", symbol, volume, buy_entry, negative_target)
    buy_sl_profit = calculate_stop_loss("BUY", symbol, volume, buy_entry, positive_target)
    sell_sl_loss = calculate_stop_loss("SELL", symbol, volume, sell_entry, negative_target)
    sell_sl_profit = calculate_stop_loss("SELL", symbol, volume, sell_entry, positive_target)
    
    # Verify calculations (for BUY orders only to keep the output manageable)
    if all(x is not None for x in [buy_tp_profit, buy_tp_loss, buy_sl_loss, buy_sl_profit]):
        # Calculate actual profit/loss for the calculated prices
        actual_tp_profit = calculate_profit("BUY", symbol, volume, buy_entry, buy_tp_profit)
        actual_tp_loss = calculate_profit("BUY", symbol, volume, buy_entry, buy_tp_loss)
        actual_sl_loss = calculate_profit("BUY", symbol, volume, buy_entry, buy_sl_loss)
        actual_sl_profit = calculate_profit("BUY", symbol, volume, buy_entry, buy_sl_profit)
        
        # Add to results table
        results.append({
            "Symbol": symbol,
            "Entry (BUY)": round(buy_entry, 5),
            "TP Price (+$100)": round(buy_tp_profit, 5),
            "Actual TP Profit": f"${round(actual_tp_profit, 2)}",
            "TP Price (-$50)": round(buy_tp_loss, 5),
            "Actual TP Loss": f"${round(actual_tp_loss, 2)}",
            "SL Price (-$50)": round(buy_sl_loss, 5),
            "Actual SL Loss": f"${round(actual_sl_loss, 2)}",
            "SL Price (+$100)": round(buy_sl_profit, 5),
            "Actual SL Profit": f"${round(actual_sl_profit, 2)}"
        })

# Display results in a pretty table
print(tabulate(results, headers='keys', tablefmt='fancy_grid'))
print("\nExplanations:")
print("TP Price (+$100): Take profit price to achieve $100 profit")
print("TP Price (-$50): Take profit price for an early exit limiting loss to $50")
print("SL Price (-$50): Stop loss price to limit potential loss to $50")
print("SL Price (+$100): Stop loss price to lock in $100 of profit")

# Shutdown connection
mt5.shutdown()
