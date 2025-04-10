"""
Tests for the MetaTrader 5 market operations module.

This file contains test cases for the MT5Market class.
"""
import os
import sys
import unittest
import time
from datetime import datetime, timezone, timedelta
import pandas as pd

# Add src directory to path to import the client package
sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..', 'src'))

# Add tests directory to path to handle running the file directly
sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..'))

# Import test configuration
try:
    # First try relative import (when run through run_tests.py)
    from tests.config import MT5_CONFIG, TEST_MODE, USE_MOCKS, DEMO_ACCOUNT, VERBOSITY
except ModuleNotFoundError:
    # Fall back to direct import (when run directly)
    from config import MT5_CONFIG, TEST_MODE, USE_MOCKS, DEMO_ACCOUNT, VERBOSITY

from MetaTraderMCPServer.client.market import MT5Market
from MetaTraderMCPServer.client.connection import MT5Connection
from MetaTraderMCPServer.client.exceptions import (
    SymbolNotFoundError, InvalidTimeframeError, MarketDataError
)
from MetaTraderMCPServer.client.types import Timeframe


class TestMT5Market(unittest.TestCase):
    """Test cases for the MT5Market class."""

    def setUp(self):
        """Set up the test environment."""
        self.config = MT5_CONFIG
        self.connection = MT5Connection(self.config)
        self.connection.connect()
        self.market = MT5Market(self.connection)
        
        # Common test symbols (major forex pairs that should be available on most platforms)
        self.test_symbols = ["EURUSD", "GBPUSD", "USDJPY"]
        
        # Common timeframes for testing
        self.test_timeframes = ["M1", "M5", "M15", "H1", "D1"]
    
    def tearDown(self):
        """Clean up the test environment."""
        # Ensure disconnection even if tests fail
        try:
            self.connection.disconnect()
        except:
            pass
            
    def test_get_symbols(self):
        """Test retrieving available market symbols."""
        print("\n\n🔄 Testing get_symbols method...")
        try:
            # Get all symbols
            all_symbols = self.market.get_symbols()
            self.assertIsNotNone(all_symbols)
            self.assertIsInstance(all_symbols, list)
            self.assertTrue(len(all_symbols) > 0)
            print(f"✅ Retrieved {len(all_symbols)} symbols")
            
            # Check if common test symbols are available
            for symbol in self.test_symbols:
                self.assertIn(symbol, all_symbols)
                print(f"✅ Verified symbol {symbol} is available")
            
            # Test with filter
            usd_symbols = self.market.get_symbols("*USD*")
            self.assertIsNotNone(usd_symbols)
            self.assertIsInstance(usd_symbols, list)
            self.assertTrue(len(usd_symbols) > 0)
            print(f"✅ Retrieved {len(usd_symbols)} USD symbols")
            
            # All USD symbols should contain "USD"
            for symbol in usd_symbols:
                self.assertIn("USD", symbol)
            
            # Test with multiple filters
            eur_gbp_symbols = self.market.get_symbols("EUR*,GBP*")
            self.assertIsNotNone(eur_gbp_symbols)
            self.assertIsInstance(eur_gbp_symbols, list)
            print(f"✅ Retrieved {len(eur_gbp_symbols)} EUR/GBP symbols")
            
            # All symbols should start with EUR or GBP
            for symbol in eur_gbp_symbols:
                self.assertTrue(symbol.startswith("EUR") or symbol.startswith("GBP"))
                
        except Exception as e:
            self.fail(f"❌ Failed to get symbols: {str(e)}")
    
    def test_get_symbol_info(self):
        """Test retrieving detailed symbol information."""
        print("\n\n🔄 Testing get_symbol_info method...")
        
        # Test with a valid symbol (EURUSD)
        try:
            symbol_info = self.market.get_symbol_info("EURUSD")
            self.assertIsNotNone(symbol_info)
            self.assertIsInstance(symbol_info, dict)
            
            # Check essential fields
            essential_fields = [
                "name", "bid", "ask", "point", "digits", 
                "spread", "trade_contract_size", "currency_base", 
                "currency_profit", "trade_mode"
            ]
            
            for field in essential_fields:
                self.assertIn(field, symbol_info)
                self.assertIsNotNone(symbol_info[field])
            
            # Verify symbol name matches
            self.assertEqual(symbol_info["name"], "EURUSD")
            
            # Verify bid and ask are reasonable (bid < ask)
            self.assertLess(symbol_info["bid"], symbol_info["ask"])
            
            # Print some key information
            print(f"✅ Symbol info retrieved for EURUSD")
            print(f"📊 EURUSD details:")
            print(f"   Bid: {symbol_info['bid']}")
            print(f"   Ask: {symbol_info['ask']}")
            print(f"   Spread: {symbol_info['spread']} points")
            print(f"   Digits: {symbol_info['digits']}")
            print(f"   Contract size: {symbol_info['trade_contract_size']}")
            print(f"   Base currency: {symbol_info['currency_base']}")
            print(f"   Profit currency: {symbol_info['currency_profit']}")
            
        except Exception as e:
            self.fail(f"❌ Failed to get symbol info for EURUSD: {str(e)}")
        
        # Test with an invalid symbol
        try:
            self.market.get_symbol_info("INVALID_SYMBOL_NAME")
            self.fail("❌ Should have raised SymbolNotFoundError but didn't")
        except SymbolNotFoundError as e:
            print(f"✅ Expected error caught for invalid symbol: {str(e)}")
        except Exception as e:
            self.fail(f"❌ Unexpected error type: {type(e).__name__}")

    def test_get_symbol_price(self):
        """Test retrieving current price for a symbol."""
        print("\n\n🔄 Testing get_symbol_price method...")
        
        # Test with valid symbols
        for symbol in self.test_symbols:
            try:
                price_data = self.market.get_symbol_price(symbol)
                self.assertIsNotNone(price_data)
                self.assertIsInstance(price_data, dict)
                
                # Check essential fields
                essential_fields = ["bid", "ask", "last", "volume", "time"]
                for field in essential_fields:
                    self.assertIn(field, price_data)
                    self.assertIsNotNone(price_data[field])
                
                # Verify bid and ask are reasonable (bid < ask)
                self.assertLess(price_data["bid"], price_data["ask"])
                
                # Verify time is a datetime object with UTC timezone
                self.assertIsInstance(price_data["time"], datetime)
                self.assertEqual(price_data["time"].tzinfo, timezone.utc)
                
                # Verify time is recent (within the last minute)
                time_diff = datetime.now(timezone.utc) - price_data["time"]
                self.assertLess(time_diff.total_seconds(), 60)
                
                print(f"✅ Price data retrieved for {symbol}")
                print(f"📊 {symbol} current prices:")
                print(f"   Bid: {price_data['bid']}")
                print(f"   Ask: {price_data['ask']}")
                print(f"   Last: {price_data['last']}")
                print(f"   Time: {price_data['time'].strftime('%Y-%m-%d %H:%M:%S %Z')}")
                
            except Exception as e:
                self.fail(f"❌ Failed to get price data for {symbol}: {str(e)}")
        
        # Test with an invalid symbol
        try:
            self.market.get_symbol_price("INVALID_SYMBOL_NAME")
            self.fail("❌ Should have raised SymbolNotFoundError but didn't")
        except SymbolNotFoundError as e:
            print(f"✅ Expected error caught for invalid symbol: {str(e)}")
        except Exception as e:
            self.fail(f"❌ Unexpected error type: {type(e).__name__}")
            
    def test_get_candles_latest(self):
        """Test retrieving latest candles for a symbol."""
        print("\n\n🔄 Testing get_candles_latest method...")
        
        symbol = "EURUSD"  # Use EURUSD for candle tests
        
        # Test with different timeframes
        for timeframe in self.test_timeframes:
            try:
                # Get default number of candles (100)
                candles = self.market.get_candles_latest(symbol, timeframe)
                self.assertIsNotNone(candles)
                self.assertIsInstance(candles, pd.DataFrame)
                
                # Check if we got the expected number of candles
                self.assertEqual(len(candles), 100)
                
                # Check essential columns
                essential_columns = ["time", "open", "high", "low", "close", "tick_volume", "spread"]
                for column in essential_columns:
                    self.assertIn(column, candles.columns)
                
                # Verify time column is datetime with UTC timezone
                self.assertTrue(pd.api.types.is_datetime64_dtype(candles["time"]))
                self.assertTrue(all(ts.tzinfo == timezone.utc for ts in candles["time"]))
                
                # Verify data is sorted by time (newest first)
                self.assertTrue(candles["time"].iloc[0] > candles["time"].iloc[-1])
                
                # Verify OHLC values are reasonable (high >= open, close, low)
                self.assertTrue(all(candles["high"] >= candles["open"]))
                self.assertTrue(all(candles["high"] >= candles["close"]))
                self.assertTrue(all(candles["high"] >= candles["low"]))
                self.assertTrue(all(candles["low"] <= candles["open"]))
                self.assertTrue(all(candles["low"] <= candles["close"]))
                
                print(f"✅ Retrieved {len(candles)} {timeframe} candles for {symbol}")
                print(f"📊 Latest candle ({timeframe}):")
                latest = candles.iloc[0]
                print(f"   Time: {latest['time'].strftime('%Y-%m-%d %H:%M:%S %Z')}")
                print(f"   Open: {latest['open']}")
                print(f"   High: {latest['high']}")
                print(f"   Low: {latest['low']}")
                print(f"   Close: {latest['close']}")
                print(f"   Volume: {latest['tick_volume']}")
                
                # Test with custom count
                custom_count = 50
                candles_custom = self.market.get_candles_latest(symbol, timeframe, custom_count)
                self.assertEqual(len(candles_custom), custom_count)
                print(f"✅ Successfully retrieved {custom_count} {timeframe} candles")
                
            except Exception as e:
                self.fail(f"❌ Failed to get {timeframe} candles for {symbol}: {str(e)}")
        
        # Test with invalid symbol
        try:
            self.market.get_candles_latest("INVALID_SYMBOL_NAME", "H1")
            self.fail("❌ Should have raised SymbolNotFoundError but didn't")
        except SymbolNotFoundError as e:
            print(f"✅ Expected error caught for invalid symbol: {str(e)}")
        except Exception as e:
            self.fail(f"❌ Unexpected error type: {type(e).__name__}")
        
        # Test with invalid timeframe
        try:
            self.market.get_candles_latest(symbol, "INVALID_TIMEFRAME")
            self.fail("❌ Should have raised InvalidTimeframeError but didn't")
        except InvalidTimeframeError as e:
            print(f"✅ Expected error caught for invalid timeframe: {str(e)}")
        except Exception as e:
            self.fail(f"❌ Unexpected error type: {type(e).__name__}")

    def test_get_candles_by_date(self):
        """Test retrieving historical candles for a symbol by date range."""
        print("\n\n🔄 Testing get_candles_by_date method...")
        
        symbol = "EURUSD"  # Use EURUSD for candle tests
        timeframe = "H1"  # Use hourly timeframe for date tests
        
        # Get current time in UTC
        now = datetime.now(timezone.utc)
        
        # Test case 1: Both from_date and to_date provided (last 24 hours)
        try:
            from_date = (now - timedelta(days=1)).strftime("%Y-%m-%d %H:%M")
            to_date = now.strftime("%Y-%m-%d %H:%M")
            
            candles = self.market.get_candles_by_date(symbol, timeframe, from_date, to_date)
            self.assertIsNotNone(candles)
            self.assertIsInstance(candles, pd.DataFrame)
            
            # Should have ~24 hourly candles (might be slightly less due to weekends/holidays)
            self.assertGreaterEqual(len(candles), 1)
            self.assertLessEqual(len(candles), 24)
            
            # Check essential columns
            essential_columns = ["time", "open", "high", "low", "close", "tick_volume", "spread"]
            for column in essential_columns:
                self.assertIn(column, candles.columns)
            
            print(f"✅ Retrieved {len(candles)} candles for date range: {from_date} to {to_date}")
            
        except Exception as e:
            self.fail(f"❌ Failed to get candles with both dates: {str(e)}")
        
        # Test case 2: Only from_date provided (last week)
        try:
            from_date = (now - timedelta(days=7)).strftime("%Y-%m-%d %H:%M")
            
            candles = self.market.get_candles_by_date(symbol, timeframe, from_date)
            self.assertIsNotNone(candles)
            self.assertIsInstance(candles, pd.DataFrame)
            
            # Should have candles from the last week (up to 1000)
            self.assertGreater(len(candles), 1)
            self.assertLessEqual(len(candles), 1000)
            
            # Verify oldest candle is after from_date
            oldest_time = candles["time"].min()
            from_datetime = datetime.strptime(from_date, "%Y-%m-%d %H:%M").replace(tzinfo=timezone.utc)
            self.assertGreaterEqual(oldest_time, from_datetime)
            
            print(f"✅ Retrieved {len(candles)} candles from date: {from_date}")
            
        except Exception as e:
            self.fail(f"❌ Failed to get candles with only from_date: {str(e)}")
        
        # Test case 3: Only to_date provided (30 days before specified date)
        try:
            to_date = (now - timedelta(days=7)).strftime("%Y-%m-%d %H:%M")
            
            candles = self.market.get_candles_by_date(symbol, timeframe, to_date=to_date)
            self.assertIsNotNone(candles)
            self.assertIsInstance(candles, pd.DataFrame)
            
            # Should have candles from 30 days before to_date
            self.assertGreater(len(candles), 1)
            
            # Verify newest candle is before or equal to to_date
            newest_time = candles["time"].max()
            to_datetime = datetime.strptime(to_date, "%Y-%m-%d %H:%M").replace(tzinfo=timezone.utc)
            self.assertLessEqual(newest_time, to_datetime)
            
            print(f"✅ Retrieved {len(candles)} candles up to date: {to_date}")
            
        except Exception as e:
            self.fail(f"❌ Failed to get candles with only to_date: {str(e)}")
        
        # Test case 4: No dates provided (recent 1000 candles)
        try:
            candles = self.market.get_candles_by_date(symbol, timeframe)
            self.assertIsNotNone(candles)
            self.assertIsInstance(candles, pd.DataFrame)
            
            # Should have up to 1000 recent candles
            self.assertGreater(len(candles), 1)
            self.assertLessEqual(len(candles), 1000)
            
            print(f"✅ Retrieved {len(candles)} recent candles with no date parameters")
            
        except Exception as e:
            self.fail(f"❌ Failed to get candles with no dates: {str(e)}")
        
        # Test with invalid date format
        try:
            self.market.get_candles_by_date(symbol, timeframe, "2023/01/01", "2023/01/02")
            self.fail("❌ Should have raised ValueError but didn't")
        except ValueError as e:
            print(f"✅ Expected error caught for invalid date format: {str(e)}")
        except Exception as e:
            self.fail(f"❌ Unexpected error type: {type(e).__name__}")
            
        # Test with invalid symbol
        try:
            self.market.get_candles_by_date("INVALID_SYMBOL_NAME", timeframe)
            self.fail("❌ Should have raised SymbolNotFoundError but didn't")
        except SymbolNotFoundError as e:
            print(f"✅ Expected error caught for invalid symbol: {str(e)}")
        except Exception as e:
            self.fail(f"❌ Unexpected error type: {type(e).__name__}")
            
        # Test with invalid timeframe
        try:
            self.market.get_candles_by_date(symbol, "INVALID_TIMEFRAME")
            self.fail("❌ Should have raised InvalidTimeframeError but didn't")
        except InvalidTimeframeError as e:
            print(f"✅ Expected error caught for invalid timeframe: {str(e)}")
        except Exception as e:
            self.fail(f"❌ Unexpected error type: {type(e).__name__}")


class TestMT5MarketLongRunning(unittest.TestCase):
    """Long-running tests for the MT5Market class that should be run separately."""

    def setUp(self):
        """Set up the test environment."""
        self.config = MT5_CONFIG
        self.connection = MT5Connection(self.config)
        self.connection.connect()
        self.market = MT5Market(self.connection)
    
    def tearDown(self):
        """Clean up the test environment."""
        try:
            self.connection.disconnect()
        except:
            pass
    
    def test_market_data_consistency(self):
        """Test market data consistency over time."""
        print("\n\n🔄 Testing market data consistency over time...")
        
        symbol = "EURUSD"
        timeframe = "M1"
        iterations = 5
        delay = 2  # seconds between checks
        
        prices = []
        candles = []
        
        try:
            for i in range(iterations):
                print(f"\nIteration {i+1}/{iterations}:")
                
                # Get current price
                price = self.market.get_symbol_price(symbol)
                prices.append(price)
                print(f"  Price: Bid={price['bid']}, Ask={price['ask']}")
                
                # Get latest candle
                candle_data = self.market.get_candles_latest(symbol, timeframe, 1)
                candles.append(candle_data.iloc[0])
                print(f"  Latest candle: Open={candle_data.iloc[0]['open']}, Close={candle_data.iloc[0]['close']}")
                
                # Wait before next check
                if i < iterations - 1:
                    print(f"  Waiting {delay} seconds...")
                    time.sleep(delay)
            
            # Verify price consistency
            for i in range(1, len(prices)):
                # Prices should be reasonably close (not drastically different)
                bid_diff = abs(prices[i]['bid'] - prices[i-1]['bid'])
                ask_diff = abs(prices[i]['ask'] - prices[i-1]['ask'])
                
                # For major pairs, a reasonable threshold might be 0.01 (100 pips)
                # This is very conservative and would catch only major inconsistencies
                self.assertLess(bid_diff, 0.01, "Bid price changed drastically")
                self.assertLess(ask_diff, 0.01, "Ask price changed drastically")
            
            print("\n✅ Market data consistency verified over time")
            
        except Exception as e:
            self.fail(f"❌ Market data consistency test failed: {str(e)}")


def simple_market_test():
    """A simple test function to test the market module outside of unittest framework."""
    print("\n" + "="*50)
    print("🧪 SIMPLE MARKET MODULE TEST")
    print("="*50)
    
    try:
        # Create connection
        print("\n📡 Connecting to MetaTrader 5...")
        config = MT5_CONFIG
        connection = MT5Connection(config)
        connected = connection.connect()
        
        if not connected:
            print("❌ Failed to connect to MetaTrader 5")
            return False
        
        print("✅ Connected to MetaTrader 5")
        
        # Create market instance
        market = MT5Market(connection)
        
        # Get symbols
        symbols = market.get_symbols("*USD*")
        print(f"\n📊 Found {len(symbols)} USD symbols")
        print(f"First 5 symbols: {', '.join(symbols[:5])}")
        
        # Get EURUSD info
        symbol_info = market.get_symbol_info("EURUSD")
        print(f"\n📈 EURUSD info:")
        print(f"  Bid: {symbol_info['bid']}")
        print(f"  Ask: {symbol_info['ask']}")
        print(f"  Spread: {symbol_info['spread']} points")
        
        # Get current price
        price = market.get_symbol_price("EURUSD")
        print(f"\n💰 Current EURUSD price:")
        print(f"  Bid: {price['bid']}")
        print(f"  Ask: {price['ask']}")
        print(f"  Time: {price['time'].strftime('%Y-%m-%d %H:%M:%S %Z')}")
        
        # Get latest candles
        candles = market.get_candles_latest("EURUSD", "H1", 5)
        print(f"\n📊 Latest 5 hourly candles for EURUSD:")
        for i, candle in candles.iterrows():
            print(f"  {candle['time'].strftime('%Y-%m-%d %H:%M')}: Open={candle['open']}, Close={candle['close']}")
        
        # Disconnect
        connection.disconnect()
        print("\n✅ Disconnected from MetaTrader 5")
        print("\n✅ Simple market test completed successfully")
        return True
        
    except Exception as e:
        print(f"\n❌ Simple market test failed: {str(e)}")
        return False


if __name__ == "__main__":
    """Run market tests."""
    
    mode = "simple"  # Default: run simple test
    
    if len(sys.argv) > 1:
        mode = sys.argv[1].lower()
    
    if mode == "unittest":
        # Run unit tests
        unittest.main(argv=['first-arg-is-ignored'])
    elif mode == "long":
        # Run long-running tests
        suite = unittest.TestLoader().loadTestsFromTestCase(TestMT5MarketLongRunning)
        unittest.TextTestRunner(verbosity=VERBOSITY).run(suite)
    elif mode == "all":
        # Run all tests
        unittest.main(argv=['first-arg-is-ignored'])
        simple_market_test()
    else:
        # Run simple test
        simple_market_test()
