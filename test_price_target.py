#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Test script for calculate_price_target function
"""
import MetaTrader5 as mt5
from tabulate import tabulate
from MetaTraderMCPServer.client.functions.calculate_profit import calculate_profit
from MetaTraderMCPServer.client.functions.calculate_price_targets import calculate_price_target

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
targets = [100, 50, -50, -100]  # Different profit/loss targets to test

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
    
    symbol_results = {
        "Symbol": symbol,
        "Entry (BUY)": round(buy_entry, 5),
        "Entry (SELL)": round(sell_entry, 5)
    }
    
    # Test different combinations for BUY orders
    for target in targets:
        # Calculate take profit price
        tp_price = calculate_price_target("BUY", symbol, volume, buy_entry, target, "profit")
        if tp_price:
            actual_profit = calculate_profit("BUY", symbol, volume, buy_entry, tp_price)
            symbol_results[f"BUY TP ${target}"] = round(tp_price, 5)
            symbol_results[f"BUY TP ${target} (Actual)"] = f"${round(actual_profit, 2)}"
        
        # Calculate stop loss price
        sl_price = calculate_price_target("BUY", symbol, volume, buy_entry, target, "loss")
        if sl_price:
            actual_profit = calculate_profit("BUY", symbol, volume, buy_entry, sl_price)
            symbol_results[f"BUY SL ${target}"] = round(sl_price, 5)
            symbol_results[f"BUY SL ${target} (Actual)"] = f"${round(actual_profit, 2)}"
    
    # Test different combinations for SELL orders
    for target in targets:
        # Calculate take profit price
        tp_price = calculate_price_target("SELL", symbol, volume, sell_entry, target, "profit")
        if tp_price:
            actual_profit = calculate_profit("SELL", symbol, volume, sell_entry, tp_price)
            symbol_results[f"SELL TP ${target}"] = round(tp_price, 5)
            symbol_results[f"SELL TP ${target} (Actual)"] = f"${round(actual_profit, 2)}"
        
        # Calculate stop loss price
        sl_price = calculate_price_target("SELL", symbol, volume, sell_entry, target, "loss")
        if sl_price:
            actual_profit = calculate_profit("SELL", symbol, volume, sell_entry, sl_price)
            symbol_results[f"SELL SL ${target}"] = round(sl_price, 5)
            symbol_results[f"SELL SL ${target} (Actual)"] = f"${round(actual_profit, 2)}"
    
    results.append(symbol_results)

# Display results in a more focused way to prevent table from being too wide
print("TESTING BUY ORDERS WITH TAKE PROFIT:")
buy_tp_results = []
for r in results:
    row = {"Symbol": r["Symbol"], "Entry": r["Entry (BUY)"]}
    for target in targets:
        if f"BUY TP ${target}" in r:
            row[f"TP ${target}"] = r[f"BUY TP ${target}"] 
            row[f"Actual"] = r[f"BUY TP ${target} (Actual)"]
    buy_tp_results.append(row)
print(tabulate(buy_tp_results, headers='keys', tablefmt='fancy_grid'))

print("\nTESTING BUY ORDERS WITH STOP LOSS:")
buy_sl_results = []
for r in results:
    row = {"Symbol": r["Symbol"], "Entry": r["Entry (BUY)"]}
    for target in targets:
        if f"BUY SL ${target}" in r:
            row[f"SL ${target}"] = r[f"BUY SL ${target}"] 
            row[f"Actual"] = r[f"BUY SL ${target} (Actual)"]
    buy_sl_results.append(row)
print(tabulate(buy_sl_results, headers='keys', tablefmt='fancy_grid'))

print("\nTESTING SELL ORDERS WITH TAKE PROFIT:")
sell_tp_results = []
for r in results:
    row = {"Symbol": r["Symbol"], "Entry": r["Entry (SELL)"]}
    for target in targets:
        if f"SELL TP ${target}" in r:
            row[f"TP ${target}"] = r[f"SELL TP ${target}"] 
            row[f"Actual"] = r[f"SELL TP ${target} (Actual)"]
    sell_tp_results.append(row)
print(tabulate(sell_tp_results, headers='keys', tablefmt='fancy_grid'))

print("\nTESTING SELL ORDERS WITH STOP LOSS:")
sell_sl_results = []
for r in results:
    row = {"Symbol": r["Symbol"], "Entry": r["Entry (SELL)"]}
    for target in targets:
        if f"SELL SL ${target}" in r:
            row[f"SL ${target}"] = r[f"SELL SL ${target}"] 
            row[f"Actual"] = r[f"SELL SL ${target} (Actual)"]
    sell_sl_results.append(row)
print(tabulate(sell_sl_results, headers='keys', tablefmt='fancy_grid'))

print("\nExplanations:")
print("TP $100/$50: Take profit price to achieve $100/$50 profit")
print("TP $-50/$-100: Take profit price for an early exit limiting loss to $50/$100")
print("SL $-50/$-100: Stop loss price to limit potential loss to $50/$100")
print("SL $100/$50: Stop loss price to lock in $100/$50 of profit")

# Shutdown connection
mt5.shutdown()
