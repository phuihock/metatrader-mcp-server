"""
Tests for the MetaTrader 5 client account module.

This file contains test cases for the MT5Account class.
"""
import os
import sys
import unittest
import time
from datetime import datetime
from unittest.mock import MagicMock, patch
import warnings

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

# Import the modules to test
from MetaTraderMCPServer.client.connection import MT5Connection
from MetaTraderMCPServer.client.account import MT5Account
from MetaTraderMCPServer.client.exceptions import (
    AccountError, AccountInfoError, ConnectionError, 
    MarginLevelError, TradingNotAllowedError
)


class MockHelpers:
    """Helper class for creating mock MT5 objects."""
    
    @staticmethod
    def create_account_info_mock(data=None):
        """Create a mock MT5 account_info object."""
        if data is None:
            data = DEMO_ACCOUNT.copy()
        
        mock = MagicMock()
        mock._asdict.return_value = data
        return mock


class BaseTestCase(unittest.TestCase):
    """Base class for all test cases with common utilities."""
    
    def setUp(self):
        """Base setup for all tests."""
        self.config = MT5_CONFIG.copy()
        
        # Suppress ResourceWarning about unclosed socket
        warnings.simplefilter("ignore", ResourceWarning)
    
    def run_test_with_message(self, message, icon="🧪"):
        """Print a nice formatted message before test."""
        if VERBOSITY >= 2:
            print(f"\n\n{icon} {message}...")


class MockedTestCase(BaseTestCase):
    """Base class for tests that use mocks instead of real MT5 connection."""
    
    def setUp(self):
        """Set up mocked tests."""
        super().setUp()
        
        self.connection = MagicMock()
        self.connection.is_connected.return_value = True
        self.account = MT5Account(self.connection)
        
        # Patch MT5 module
        self.mt5_patcher = patch('MetaTraderMCPServer.client.account.mt5')
        self.mock_mt5 = self.mt5_patcher.start()
        
        # Set up default account info mock
        self.mock_mt5.account_info.return_value = MockHelpers.create_account_info_mock()
        
        # Set up default terminal info mock
        terminal_info_mock = MagicMock()
        terminal_info_mock.trade_allowed = True
        self.mock_mt5.terminal_info.return_value = terminal_info_mock
    
    def tearDown(self):
        """Clean up mocked tests."""
        self.mt5_patcher.stop()


class IntegrationTestCase(BaseTestCase):
    """Base class for tests that connect to real MT5 terminal."""
    
    def setUp(self):
        """Set up integration tests with real MT5 connection."""
        super().setUp()
        
        # Set up a real connection
        self.connection = MT5Connection(self.config)
        
        # Connect to MT5
        self.connection.connect()
        
        # Create account instance
        self.account = MT5Account(self.connection)
    
    def tearDown(self):
        """Clean up integration tests."""
        # Ensure disconnection even if tests fail
        try:
            self.connection.disconnect()
        except:
            pass


# =============================================================================
# Unit Tests (With Mocks)
# =============================================================================

class TestMT5AccountUnit(MockedTestCase):
    """Unit tests for the MT5Account class using mocks."""
    
    def test_get_account_info(self):
        """Test retrieving account information."""
        self.run_test_with_message("Testing account information retrieval", "📊")
        
        # Configure the mock
        expected_data = {
            "login": 12345,
            "balance": 1000.0,
            "equity": 1050.0,
            "margin": 200.0,
            "margin_free": 850.0,
            "margin_level": 525.0,
            "currency": "USD",
            "trade_mode": 1
        }
        self.mock_mt5.account_info.return_value = MockHelpers.create_account_info_mock(expected_data)
        
        # Get account info
        result = self.account.get_account_info()
        
        # Verify result
        self.assertEqual(result, expected_data)
        self.mock_mt5.account_info.assert_called_once()
        
        if VERBOSITY >= 2:
            print(f"✅ Account info successfully retrieved for {result['login']}")
            print(f"   Balance: {result['balance']} {result['currency']}")
    
    def test_get_account_info_connection_error(self):
        """Test behavior when not connected."""
        self.run_test_with_message("Testing connection error handling", "❌")
        
        # Configure mock to simulate not connected
        self.connection.is_connected.return_value = False
        
        # Try to get account info
        with self.assertRaises(ConnectionError):
            self.account.get_account_info()
        
        if VERBOSITY >= 2:
            print("✅ Successfully detected connection error")
    
    def test_get_account_info_retrieval_error(self):
        """Test behavior when account info retrieval fails."""
        self.run_test_with_message("Testing account info retrieval error", "❌")
        
        # Configure mock to simulate retrieval failure
        self.mock_mt5.account_info.return_value = None
        self.mock_mt5.last_error.return_value = (1, "Test error message")
        
        # Try to get account info
        with self.assertRaises(AccountInfoError):
            self.account.get_account_info()
        
        if VERBOSITY >= 2:
            print("✅ Successfully detected account info retrieval error")
    
    def test_property_getters(self):
        """Test the property getter methods."""
        self.run_test_with_message("Testing account property getters", "💰")
        
        # Configure the mock
        expected_data = {
            "login": 12345,
            "balance": 1000.0,
            "equity": 1050.0,
            "margin": 200.0,
            "margin_free": 850.0,
            "margin_level": 525.0,
            "currency": "USD",
            "leverage": 100,
            "trade_mode": 1
        }
        self.mock_mt5.account_info.return_value = MockHelpers.create_account_info_mock(expected_data)
        
        # Test each getter
        self.assertEqual(self.account.get_balance(), 1000.0)
        self.assertEqual(self.account.get_equity(), 1050.0)
        self.assertEqual(self.account.get_margin(), 200.0)
        self.assertEqual(self.account.get_free_margin(), 850.0)
        self.assertEqual(self.account.get_margin_level(), 525.0)
        self.assertEqual(self.account.get_currency(), "USD")
        self.assertEqual(self.account.get_leverage(), 100)
        
        if VERBOSITY >= 2:
            print("✅ All property getters working correctly")
    
    def test_account_type(self):
        """Test the account type determination."""
        self.run_test_with_message("Testing account type determination", "🏦")
        
        # Test demo account (trade_mode = 1)
        account_data = {"trade_mode": 1}
        self.mock_mt5.account_info.return_value = MockHelpers.create_account_info_mock(account_data)
        self.assertEqual(self.account.get_account_type(), "demo")
        
        # Test real account (trade_mode = 0)
        account_data = {"trade_mode": 0}
        self.mock_mt5.account_info.return_value = MockHelpers.create_account_info_mock(account_data)
        self.assertEqual(self.account.get_account_type(), "real")
        
        # Test contest account (trade_mode = 2)
        account_data = {"trade_mode": 2}
        self.mock_mt5.account_info.return_value = MockHelpers.create_account_info_mock(account_data)
        self.assertEqual(self.account.get_account_type(), "contest")
        
        # Test unknown account type
        account_data = {"trade_mode": 999}
        self.mock_mt5.account_info.return_value = MockHelpers.create_account_info_mock(account_data)
        self.assertTrue(self.account.get_account_type().startswith("unknown"))
        
        if VERBOSITY >= 2:
            print("✅ Account type determination working correctly")
    
    def test_trade_allowed(self):
        """Test if trading is allowed check."""
        self.run_test_with_message("Testing trade allowed status", "🛒")
        
        # Test trading allowed
        terminal_info_mock = MagicMock()
        terminal_info_mock.trade_allowed = True
        self.mock_mt5.terminal_info.return_value = terminal_info_mock
        
        self.assertTrue(self.account.is_trade_allowed())
        
        # Test trading not allowed
        terminal_info_mock.trade_allowed = False
        self.assertFalse(self.account.is_trade_allowed())
        
        if VERBOSITY >= 2:
            print("✅ Trade allowed check working correctly")
    
    def test_margin_level_check(self):
        """Test margin level check function."""
        self.run_test_with_message("Testing margin level check", "⚠️")
        
        # Test with sufficient margin level
        account_data = {"margin_level": 150.0}
        self.mock_mt5.account_info.return_value = MockHelpers.create_account_info_mock(account_data)
        
        result = self.account.check_margin_level(min_level=100.0)
        self.assertTrue(result)
        
        # Test with insufficient margin level
        account_data = {"margin_level": 50.0}
        self.mock_mt5.account_info.return_value = MockHelpers.create_account_info_mock(account_data)
        
        with self.assertRaises(MarginLevelError):
            self.account.check_margin_level(min_level=100.0)
        
        # Test with zero margin level (no positions)
        account_data = {"margin_level": 0.0}
        self.mock_mt5.account_info.return_value = MockHelpers.create_account_info_mock(account_data)
        
        # Should pass with min_level=0
        result = self.account.check_margin_level(min_level=0.0)
        self.assertTrue(result)
        
        # Should fail with min_level>0
        with self.assertRaises(MarginLevelError):
            self.account.check_margin_level(min_level=0.1)
        
        if VERBOSITY >= 2:
            print("✅ Margin level checks working correctly")
    
    def test_trade_statistics(self):
        """Test trade statistics retrieval."""
        self.run_test_with_message("Testing trade statistics", "📈")
        
        # Configure the mock
        expected_data = {
            "login": 12345,
            "balance": 1000.0,
            "equity": 1050.0,
            "profit": 50.0,
            "margin": 200.0,
            "margin_free": 850.0,
            "margin_level": 525.0,
            "currency": "USD",
            "leverage": 100,
            "trade_mode": 1
        }
        self.mock_mt5.account_info.return_value = MockHelpers.create_account_info_mock(expected_data)
        
        # Get trade statistics
        stats = self.account.get_trade_statistics()
        
        # Verify expected keys
        expected_keys = [
            "balance", "equity", "profit", "margin_level", 
            "free_margin", "account_type", "leverage", "currency"
        ]
        for key in expected_keys:
            self.assertIn(key, stats)
        
        # Verify key values
        self.assertEqual(stats["balance"], 1000.0)
        self.assertEqual(stats["equity"], 1050.0)
        self.assertEqual(stats["profit"], 50.0)
        self.assertEqual(stats["account_type"], "demo")
        
        if VERBOSITY >= 2:
            print("✅ Trade statistics retrieved correctly")


# =============================================================================
# Integration Tests (With Real MT5 Connection)
# =============================================================================

class TestMT5AccountIntegration(IntegrationTestCase):
    """Integration tests for the MT5Account class using real MT5 connection."""
    
    def test_get_account_info(self):
        """Test retrieving account information."""
        self.run_test_with_message("Testing real account information retrieval", "📊")
        
        account_info = self.account.get_account_info()
        
        # Verify we got a dictionary with expected keys
        self.assertIsInstance(account_info, dict)
        self.assertIn("login", account_info)
        self.assertIn("balance", account_info)
        self.assertIn("equity", account_info)
        self.assertIn("margin", account_info)
        self.assertIn("margin_free", account_info)
        self.assertIn("margin_level", account_info)
        self.assertIn("currency", account_info)
        
        # Verify login matches our config
        self.assertEqual(account_info["login"], self.config["login"])
        
        if VERBOSITY >= 2:
            print(f"✅ Account info successfully retrieved for {account_info['login']}")
            print(f"   Balance: {account_info['balance']} {account_info['currency']}")
            print(f"   Equity: {account_info['equity']} {account_info['currency']}")
    
    def test_get_property_methods(self):
        """Test the individual property getter methods with real connection."""
        self.run_test_with_message("Testing real account property getters", "💰")
        
        # Test each property getter
        balance = self.account.get_balance()
        self.assertIsInstance(balance, float)
        
        equity = self.account.get_equity()
        self.assertIsInstance(equity, float)
        
        margin = self.account.get_margin()
        self.assertIsInstance(margin, float)
        
        free_margin = self.account.get_free_margin()
        self.assertIsInstance(free_margin, float)
        
        margin_level = self.account.get_margin_level()
        self.assertIsInstance(margin_level, float)
        
        currency = self.account.get_currency()
        self.assertIsInstance(currency, str)
        
        leverage = self.account.get_leverage()
        self.assertIsInstance(leverage, int)
        
        if VERBOSITY >= 2:
            print(f"✅ Balance: {balance}")
            print(f"✅ Equity: {equity}")
            print(f"✅ Margin: {margin}")
            print(f"✅ Free Margin: {free_margin}")
            print(f"✅ Margin Level: {margin_level}%")
            print(f"✅ Currency: {currency}")
            print(f"✅ Leverage: 1:{leverage}")
    
    def test_account_type(self):
        """Test the account type determination with real connection."""
        self.run_test_with_message("Testing real account type", "🏦")
        
        account_type = self.account.get_account_type()
        self.assertIsInstance(account_type, str)
        self.assertIn(account_type, ["real", "demo", "contest", "unknown"])
        
        if VERBOSITY >= 2:
            print(f"✅ Account type: {account_type}")
    
    def test_trade_allowed(self):
        """Test if trading is allowed with real connection."""
        self.run_test_with_message("Testing real trade allowed status", "🛒")
        
        trade_allowed = self.account.is_trade_allowed()
        self.assertIsInstance(trade_allowed, bool)
        
        if VERBOSITY >= 2:
            print(f"✅ Trading allowed: {'Yes' if trade_allowed else 'No'}")
    
    def test_margin_level_check(self):
        """Test margin level check function with real connection."""
        self.run_test_with_message("Testing real margin level check", "⚠️")
        
        # Get current margin level
        margin_level = self.account.get_margin_level()
        
        if VERBOSITY >= 2:
            print(f"Current margin level: {margin_level}%")
        
        # If we have no open positions, margin level can be 0
        # In this case, we'll test with a minimum level of 0
        if margin_level == 0:
            if VERBOSITY >= 2:
                print("No open positions detected (margin level is 0%)")
            
            result = self.account.check_margin_level(min_level=0.0)
            self.assertTrue(result)
            
            if VERBOSITY >= 2:
                print("✅ Successfully verified margin level with minimum = 0")
            
            # Test with a higher requirement (should fail)
            try:
                self.account.check_margin_level(min_level=0.1)
                self.fail("Should have raised MarginLevelError")
            except MarginLevelError:
                if VERBOSITY >= 2:
                    print("✅ Successfully detected too low margin level")
        else:
            # Normal case - we have open positions
            result = self.account.check_margin_level(min_level=margin_level * 0.5)
            self.assertTrue(result)
            
            if VERBOSITY >= 2:
                print(f"✅ Current margin level ({margin_level}%) passes check")
            
            # Test with a very high requirement (should fail)
            try:
                self.account.check_margin_level(min_level=margin_level * 10)
                self.fail("Should have raised MarginLevelError")
            except MarginLevelError:
                if VERBOSITY >= 2:
                    print("✅ Successfully detected too low margin level")
    
    def test_trade_statistics(self):
        """Test trade statistics retrieval with real connection."""
        self.run_test_with_message("Testing real trade statistics", "📈")
        
        stats = self.account.get_trade_statistics()
        
        # Verify we got a dictionary with expected keys
        self.assertIsInstance(stats, dict)
        self.assertIn("balance", stats)
        self.assertIn("equity", stats)
        self.assertIn("profit", stats)
        self.assertIn("margin_level", stats)
        self.assertIn("free_margin", stats)
        self.assertIn("account_type", stats)
        self.assertIn("leverage", stats)
        self.assertIn("currency", stats)
        
        if VERBOSITY >= 2:
            print(f"✅ Trade statistics successfully retrieved")
            print(f"   Account type: {stats['account_type']}")
            print(f"   Balance: {stats['balance']} {stats['currency']}")
            print(f"   Profit: {stats['profit']} {stats['currency']}")


class TestMT5AccountNoConnection(BaseTestCase):
    """Edge case tests for when there is no connection."""
    
    def test_no_connection(self):
        """Test behavior when not connected."""
        self.run_test_with_message("Testing account with no connection", "❌")
        
        # Create connection but don't connect
        connection = MT5Connection({"debug": True})
        
        # Create account instance
        account = MT5Account(connection)
        
        # Attempt to get account info should raise ConnectionError
        with self.assertRaises(ConnectionError):
            account.get_account_info()
        
        if VERBOSITY >= 2:
            print("✅ Successfully detected no connection")


def simple_account_test():
    """A simple test function to test the account module outside of unittest framework."""
    print("\n📊 Simple Account Test 📊")
    print("=" * 40)
    
    # Use values from config
    config = MT5_CONFIG.copy()
    print(f"Setting up connection to {config['server']}...")
    
    # Create a connection with cleaner error handling
    connection = MT5Connection(config)
    
    try:
        # Connect to MT5
        print("Connecting to MetaTrader 5...")
        connection.connect()
        print("✓ Connected successfully")
        
        # Create account instance
        print("Creating account instance...")
        account = MT5Account(connection)
        
        # Get account info
        print("Retrieving account information...")
        info = account.get_account_info()
        print(f"✓ Account: {info['login']} ({account.get_account_type()})")
        print(f"✓ Balance: {info['balance']} {info['currency']}")
        print(f"✓ Equity: {info['equity']} {info['currency']}")
        print(f"✓ Margin level: {info['margin_level']}%")
        print(f"✓ Leverage: 1:{info['leverage']}")
        
        # Check if trading is allowed
        print("Checking if trading is allowed...")
        can_trade = account.is_trade_allowed()
        print(f"✓ Trading allowed: {'Yes' if can_trade else 'No'}")
        
        # Get trade statistics
        print("Retrieving trade statistics...")
        stats = account.get_trade_statistics()
        print(f"✓ Account type: {stats['account_type']}")
        print(f"✓ Profit: {stats['profit']} {stats['currency']}")
        
        print("\n✅ All account tests passed!")
        
    except Exception as e:
        print(f"❌ Error: {str(e)}")
    finally:
        # Disconnect from MT5
        print("Disconnecting from MetaTrader 5...")
        try:
            connection.disconnect()
            print("✓ Disconnected")
        except:
            print("✗ Failed to disconnect properly")
    
    print("=" * 40)


if __name__ == "__main__":
    """Run account tests."""
    if len(sys.argv) > 1:
        mode = sys.argv[1]  # Get mode from command line
    else:
        mode = "mixed"  # Default: run both unit and integration tests
    
    # Set test mode based on USE_MOCKS setting
    use_mocks = USE_MOCKS
    if use_mocks == "auto":
        try:
            # Try to import MetaTrader5 to see if it's available
            import MetaTrader5
            use_mocks = "never"  # We can connect to MT5
        except ImportError:
            use_mocks = "always"  # We can't connect to MT5
    
    # Create runner with proper verbosity
    runner = unittest.TextTestRunner(verbosity=VERBOSITY)
    
    if mode == "unit" or mode == "all" or mode == "mixed":
        # Run unit tests
        print("\n🧪 Running unit tests for MT5Account...")
        unit_suite = unittest.TestLoader().loadTestsFromTestCase(TestMT5AccountUnit)
        runner.run(unit_suite)
    
    if (mode == "integration" or mode == "all" or mode == "mixed") and use_mocks != "always":
        # Run integration tests only if we're not forced to use mocks
        print("\n🧪 Running integration tests for MT5Account...")
        integration_suite = unittest.TestLoader().loadTestsFromTestCase(TestMT5AccountIntegration)
        runner.run(integration_suite)
        
        # Run no connection test
        print("\n🧪 Running no connection test for MT5Account...")
        no_conn_suite = unittest.TestLoader().loadTestsFromTestCase(TestMT5AccountNoConnection)
        runner.run(no_conn_suite)
    
    if mode == "simple" or mode == "all":
        # Run simple test
        if use_mocks != "always":
            simple_account_test()
        else:
            print("\n⚠️ Simple account test skipped - no MT5 connection available")
