#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Final test script for the simplified calculate_price_target function
"""
import MetaTrader5 as mt5
from MetaTraderMCPServer.client.functions.calculate_profit import calculate_profit
from MetaTraderMCPServer.client.functions.calculate_price_targets import calculate_price_target

# Initialize connection to MetaTrader 5
if not mt5.initialize():
    print(f"❌ Failed to initialize MT5: {mt5.last_error()}")
    quit()

print("====================")
print("🎯 FINAL PRICE TARGET TEST")
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

# Define test scenarios
test_scenarios = [
    # Description, Order Type, Entry Price, Target
    ("Take Profit (BUY)", "BUY", buy_entry, 100),      # $100 profit for BUY
    ("Stop Loss (BUY)", "BUY", buy_entry, -50),        # $50 loss limit for BUY
    ("Take Profit (SELL)", "SELL", sell_entry, 100),   # $100 profit for SELL
    ("Stop Loss (SELL)", "SELL", sell_entry, -50),     # $50 loss limit for SELL
]

# Print header
print(f"{'Scenario':<20} {'Target':<10} {'Entry':<10} {'Price':<10} {'Profit':<10} {'Success':<10}")
print("-" * 70)

# Run tests
for description, order_type, entry, target in test_scenarios:
    try:
        # Calculate target price
        target_price = calculate_price_target(order_type, symbol, volume, entry, target)
        
        if target_price is not None:
            # Verify with calculate_profit
            actual_profit = calculate_profit(order_type, symbol, volume, entry, target_price)
            
            # Check if the result meets the target
            success = False
            if target > 0:  # Take profit target
                success = actual_profit >= target * 0.95  # Allow 5% margin of error
            else:  # Stop loss target
                success = actual_profit <= target * 1.05  # Allow 5% margin of error
            
            # Format output
            target_str = f"${target:.2f}"
            entry_str = f"{entry:.5f}"
            price_str = f"{target_price:.5f}"
            profit_str = f"${actual_profit:.2f}"
            success_str = "✅" if success else "❌"
            
            print(f"{description:<20} {target_str:<10} {entry_str:<10} {price_str:<10} {profit_str:<10} {success_str:<10}")
        else:
            print(f"{description:<20} ${target:.2f}      {entry:.5f}   FAILED     N/A         ❌")
    except Exception as e:
        print(f"{description:<20} ${target:.2f}      {entry:.5f}   ERROR      N/A         ❌ ({e})")

# Shutdown connection
mt5.shutdown()
