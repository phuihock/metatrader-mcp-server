#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Simple test script for price target calculation function
"""
import MetaTrader5 as mt5
import pandas as pd
from MetaTraderMCPServer.client.functions.calculate_profit import calculate_profit
from MetaTraderMCPServer.client.functions.calculate_price_targets import calculate_price_target
from MetaTraderMCPServer.client.types import OrderType

# Initialize connection to MetaTrader 5
if not mt5.initialize():
    print(f"❌ Failed to initialize MT5: {mt5.last_error()}")
    quit()

print("====================")
print("🎯 SIMPLE PRICE TARGET TEST")
print("====================\n")

# Test with a single symbol
symbol = "EURUSD"
volume = 0.1

# Get symbol info
symbol_info = mt5.symbol_info(symbol)
if symbol_info is None:
    print(f"Symbol {symbol} not found")
    quit()

# Make sure symbol is visible
if not symbol_info.visible:
    print(f"Symbol {symbol} is not visible, selecting it...")
    if not mt5.symbol_select(symbol, True):
        print(f"Failed to select {symbol}")
        quit()

# Get current price
tick = mt5.symbol_info_tick(symbol)
if tick is None:
    print(f"Failed to get tick data for {symbol}")
    quit()

buy_entry = tick.ask
sell_entry = tick.bid

print(f"Testing {symbol}:")
print(f"Buy Entry: {buy_entry}")
print(f"Sell Entry: {sell_entry}")
print(f"Point: {symbol_info.point}\n")

# Test parameters
targets = [100, 50, 20, -20, -50, -100]
order_types = ["BUY", "SELL"]
target_types = ["profit", "loss"]

# Create a DataFrame to store results
results = []

for order_type in order_types:
    entry = buy_entry if order_type == "BUY" else sell_entry
    
    for target in targets:
        for target_type in target_types:
            try:
                # Calculate target price
                target_price = calculate_price_target(
                    order_type, symbol, volume, entry, target, target_type
                )
                
                if target_price is not None:
                    # Verify with calculate_profit
                    actual_profit = calculate_profit(
                        order_type, symbol, volume, entry, target_price
                    )
                    
                    # Add to results
                    results.append({
                        "Order": order_type,
                        "Target": target,
                        "Type": target_type,
                        "Entry": round(entry, 5),
                        "Target Price": round(target_price, 5),
                        "Actual Profit": round(actual_profit, 2) if actual_profit is not None else None,
                        "Price Move": round(target_price - entry, 5),
                        "Success": actual_profit is not None and (
                            (target > 0 and actual_profit >= target * 0.95) or
                            (target < 0 and actual_profit <= target * 0.95)
                        )
                    })
                else:
                    results.append({
                        "Order": order_type,
                        "Target": target,
                        "Type": target_type,
                        "Entry": round(entry, 5),
                        "Target Price": None,
                        "Actual Profit": None,
                        "Price Move": None,
                        "Success": False
                    })
            except Exception as e:
                print(f"Error for {order_type}, target={target}, type={target_type}: {e}")
                results.append({
                    "Order": order_type,
                    "Target": target,
                    "Type": target_type,
                    "Entry": round(entry, 5),
                    "Target Price": None,
                    "Actual Profit": None,
                    "Price Move": None,
                    "Success": False,
                    "Error": str(e)
                })

# Create a DataFrame for easier display
df = pd.DataFrame(results)

# Display results grouped by order type and target type
for order in order_types:
    for t_type in target_types:
        subset = df[(df["Order"] == order) & (df["Type"] == t_type)]
        if not subset.empty:
            print(f"== {order} with {t_type.upper()} targets ==")
            display_cols = ["Target", "Entry", "Target Price", "Actual Profit", "Success"]
            print(subset[display_cols].to_string(index=False))
            print()

# Shutdown connection
mt5.shutdown()
