"""
Tests for the MetaTrader 5 client history module.

This file contains test cases for the MT5History class.
"""
import os
import sys
import unittest
import time
from datetime import datetime, timedelta
from unittest.mock import MagicMock, patch
import warnings
from collections import namedtuple
import pandas as pd
import numpy as np

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
from MetaTraderMCPServer.client.history import MT5History
from MetaTraderMCPServer.client.exceptions import (
    ConnectionError, HistoryError, DealsHistoryError, OrdersHistoryError, StatisticsError
)


class MockHelpers:
    """Helper class for creating mock MT5 history objects."""
    
    @staticmethod
    def create_mock_deal(**kwargs):
        """Create a mock MT5 deal object."""
        # Default values for a trade deal
        defaults = {
            'ticket': 1,
            'time': int(datetime.now().timestamp()),
            'time_msc': int(datetime.now().timestamp() * 1000),
            'type': 0,  # DEAL_TYPE_BUY
            'entry': 0,  # DEAL_ENTRY_IN
            'position_id': 1,
            'symbol': 'EURUSD',
            'volume': 0.1,
            'price': 1.1,
            'profit': 10.0,
            'commission': -1.0,
            'swap': 0.0,
            'fee': 0.0,
            'comment': 'test deal',
            'external_id': '123456'
        }
        
        # Update with provided values
        data = {**defaults, **kwargs}
        
        # Create a custom object that has the attributes and _asdict method
        class MockDeal:
            def __init__(self, **attributes):
                for key, value in attributes.items():
                    setattr(self, key, value)
            
            def _asdict(self):
                return {key: getattr(self, key) for key in data.keys()}
        
        # Return the mock deal
        return MockDeal(**data)
    
    @staticmethod
    def create_mock_order(**kwargs):
        """Create a mock MT5 order object."""
        # Default values for a trade order
        defaults = {
            'ticket': 1,
            'time_setup': int(datetime.now().timestamp()),
            'time_setup_msc': int(datetime.now().timestamp() * 1000),
            'time_done': int(datetime.now().timestamp()) + 60,
            'time_done_msc': (int(datetime.now().timestamp()) + 60) * 1000,
            'type': 0,  # ORDER_TYPE_BUY
            'state': 3,  # ORDER_STATE_FILLED
            'symbol': 'EURUSD',
            'volume_initial': 0.1,
            'volume_current': 0.0,
            'price_open': 1.1,
            'sl': 1.09,
            'tp': 1.11,
            'price_current': 1.1005,
            'position_id': 1,
            'comment': 'test order',
            'external_id': '123456'
        }
        
        # Update with provided values
        data = {**defaults, **kwargs}
        
        # Create a custom object that has the attributes and _asdict method
        class MockOrder:
            def __init__(self, **attributes):
                for key, value in attributes.items():
                    setattr(self, key, value)
            
            def _asdict(self):
                return {key: getattr(self, key) for key in data.keys()}
        
        # Return the mock order
        return MockOrder(**data)
    
    @staticmethod
    def create_mock_deals_list(count=10, include_wins_and_losses=True):
        """Create a list of mock deals."""
        deals = []
        for i in range(count):
            # Alternate between profitable and losing deals if requested
            if include_wins_and_losses:
                profit = 10.0 if i % 2 == 0 else -5.0
            else:
                profit = 10.0
                
            # Create deals with different times to test time-based functions
            time_offset = i * 3600  # hours apart
            deal_time = int((datetime.now() - timedelta(seconds=time_offset)).timestamp())
            
            # Create the deal
            deal = MockHelpers.create_mock_deal(
                ticket=i+1,
                time=deal_time,
                time_msc=deal_time * 1000,
                profit=profit,
                price=1.1 + (i * 0.001),
                volume=0.1 + (i * 0.1)
            )
            deals.append(deal)
            
        return deals
    
    @staticmethod
    def create_mock_orders_list(count=5):
        """Create a list of mock orders."""
        orders = []
        for i in range(count):
            # Create orders with different times
            time_setup = int((datetime.now() - timedelta(hours=i*2)).timestamp())
            time_done = time_setup + (i+1) * 3600  # orders take longer to complete for each one
            
            # Create the order
            order = MockHelpers.create_mock_order(
                ticket=i+1,
                time_setup=time_setup,
                time_setup_msc=time_setup * 1000,
                time_done=time_done,
                time_done_msc=time_done * 1000,
                price_open=1.1 + (i * 0.001),
                volume_initial=0.1 + (i * 0.1)
            )
            orders.append(order)
            
        return orders


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
        
        # Create mock connection
        self.connection = MagicMock()
        self.connection.is_connected.return_value = True
        
        # Create history instance
        self.history = MT5History(self.connection)
        
        # Patch MT5 module
        self.mt5_patcher = patch('MetaTraderMCPServer.client.history.mt5')
        self.mock_mt5 = self.mt5_patcher.start()
        
        # Set up default mock returns
        self.mock_mt5.history_deals_total.return_value = 10
        self.mock_mt5.history_orders_total.return_value = 5
        
        # Setup mock deal/order data
        self.mock_deals = MockHelpers.create_mock_deals_list()
        self.mock_orders = MockHelpers.create_mock_orders_list()
        
        # Set up default returns
        self.mock_mt5.history_deals_get.return_value = self.mock_deals
        self.mock_mt5.history_orders_get.return_value = self.mock_orders
    
    def tearDown(self):
        """Clean up after tests."""
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
        
        # Create history instance
        self.history = MT5History(self.connection)
    
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

class TestMT5HistoryUnit(MockedTestCase):
    """Unit tests for the MT5History class using mocks."""
    
    def test_initialization(self):
        """Test the initialization of MT5History."""
        self.run_test_with_message("Testing MT5History initialization", "🚀")
        
        # Test that history is initialized with connection
        self.assertIsNotNone(self.history)
        self.assertEqual(self.history._connection, self.connection)
        
        if VERBOSITY >= 2:
            print("✅ MT5History initializes correctly")
    
    def test_empty_results(self):
        """Test behavior when no deals or orders are found."""
        self.run_test_with_message("Testing empty results handling", "🔍")
        
        # Set up MT5 to return empty lists
        self.mock_mt5.history_deals_get.return_value = []
        self.mock_mt5.history_orders_get.return_value = []
        self.mock_mt5.history_deals_total.return_value = 0
        self.mock_mt5.history_orders_total.return_value = 0
        
        # Test empty deals list
        deals = self.history.get_deals()
        self.assertEqual(deals, [])
        
        # Test empty orders list
        orders = self.history.get_orders()
        self.assertEqual(orders, [])
        
        if VERBOSITY >= 2:
            print("✅ All methods handle empty results correctly")
    
    def test_connection_required(self):
        """Test that connection is required for all methods."""
        self.run_test_with_message("Testing connection requirement", "🔌")
        
        # Configure mock to simulate not connected
        self.connection.is_connected.return_value = False
        
        # Try to get deals
        with self.assertRaises(ConnectionError):
            self.history.get_deals()
        
        # Try to get orders
        with self.assertRaises(ConnectionError):
            self.history.get_orders()
        
        if VERBOSITY >= 2:
            print("✅ All methods require connection")

    def test_get_deals(self):
        """Test retrieving deals."""
        self.run_test_with_message("Testing deals retrieval", "📊")
        
        # Get deals using the method
        deals = self.history.get_deals()
        
        # Verify the method returned the expected data
        self.assertEqual(len(deals), len(self.mock_deals))
        self.assertEqual(deals[0]['ticket'], self.mock_deals[0].ticket)
        
        # Verify the MT5 function was called correctly
        self.mock_mt5.history_deals_get.assert_called_once()
        
        if VERBOSITY >= 2:
            print(f"✅ Successfully retrieved {len(deals)} deals")
    
    def test_get_deals_with_filters(self):
        """Test retrieving deals with filters."""
        self.run_test_with_message("Testing deals retrieval with filters", "🔍")
        
        # Test 1: Priority filters (ticket and position)
        from_date = datetime(2025, 4, 3, 21, 26, 39, 292720)
        to_date = datetime(2025, 4, 10, 21, 26, 39, 292720)
        ticket = 12345
        position = None  # Test with ticket only
        
        # Call with ticket (which has priority)
        self.history.get_deals(from_date=from_date, to_date=to_date, ticket=ticket)
        
        # Verify MT5 function was called with only the ticket
        self.mock_mt5.history_deals_get.assert_called_once()
        args, kwargs = self.mock_mt5.history_deals_get.call_args
        
        # Should have no positional args, just ticket as keyword
        self.assertEqual(len(args), 0)
        self.assertEqual(kwargs.get('ticket'), ticket)
        
        # Reset mock for next test
        self.mock_mt5.history_deals_get.reset_mock()
        
        # Test 2: Position filter
        position = 67890
        
        # Call with position (which has priority over dates)
        self.history.get_deals(from_date=from_date, to_date=to_date, position=position)
        
        # Verify MT5 function was called with only the position
        self.mock_mt5.history_deals_get.assert_called_once()
        args, kwargs = self.mock_mt5.history_deals_get.call_args
        
        # Should have no positional args, just position as keyword
        self.assertEqual(len(args), 0)
        self.assertEqual(kwargs.get('position'), position)
        
        # Reset mock for next test
        self.mock_mt5.history_deals_get.reset_mock()
        
        # Test 3: Date range with group
        group = "*USD*"
        
        # Call with date range and group
        self.history.get_deals(from_date=from_date, to_date=to_date, group=group)
        
        # Verify MT5 function was called with dates as positional args and group as keyword
        self.mock_mt5.history_deals_get.assert_called_once()
        args, kwargs = self.mock_mt5.history_deals_get.call_args
        
        # Should have 2 positional args (dates) and group as keyword
        self.assertEqual(len(args), 2)
        self.assertEqual(args[0], from_date)
        self.assertEqual(args[1], to_date)
        self.assertEqual(kwargs.get('group'), group)
        
        if VERBOSITY >= 2:
            print(f"✅ Successfully applied filters to deals retrieval")

    def test_get_orders(self):
        """Test retrieving orders."""
        self.run_test_with_message("Testing orders retrieval", "📑")
        
        # Get orders using the method
        orders = self.history.get_orders()
        
        # Verify the method returned the expected data
        self.assertEqual(len(orders), len(self.mock_orders))
        self.assertEqual(orders[0]['ticket'], self.mock_orders[0].ticket)
        
        # Verify the MT5 function was called correctly
        self.mock_mt5.history_orders_get.assert_called_once()
        
        if VERBOSITY >= 2:
            print(f"✅ Successfully retrieved {len(orders)} orders")
    
    def test_get_orders_with_filters(self):
        """Test retrieving orders with filters."""
        self.run_test_with_message("Testing orders retrieval with filters", "🔍")
        
        # Test 1: Ticket filter (has priority)
        from_date = datetime(2025, 4, 3, 21, 26, 39, 302125)
        to_date = datetime(2025, 4, 10, 21, 26, 39, 302125)
        ticket = 12345
        
        # Call with ticket (which has priority)
        self.history.get_orders(from_date=from_date, to_date=to_date, ticket=ticket)
        
        # Verify MT5 function was called with only the ticket
        self.mock_mt5.history_orders_get.assert_called_once()
        args, kwargs = self.mock_mt5.history_orders_get.call_args
        
        # Should have no positional args, just ticket as keyword
        self.assertEqual(len(args), 0)
        self.assertEqual(kwargs.get('ticket'), ticket)
        
        # Reset mock for next test
        self.mock_mt5.history_orders_get.reset_mock()
        
        # Test 2: Date range with group
        group = "*USD*"
        
        # Call with date range and group
        self.history.get_orders(from_date=from_date, to_date=to_date, group=group)
        
        # Verify MT5 function was called with dates as positional args and group as keyword
        self.mock_mt5.history_orders_get.assert_called_once()
        args, kwargs = self.mock_mt5.history_orders_get.call_args
        
        # Should have 2 positional args (dates) and group as keyword
        self.assertEqual(len(args), 2)
        self.assertEqual(args[0], from_date)
        self.assertEqual(args[1], to_date)
        self.assertEqual(kwargs.get('group'), group)
        
        if VERBOSITY >= 2:
            print(f"✅ Successfully applied filters to orders retrieval")
    
    def test_get_total_deals(self):
        """Test getting total deals count."""
        self.run_test_with_message("Testing total deals count", "🔢")
        
        # Set up expected value
        expected_count = 42
        self.mock_mt5.history_deals_total.return_value = expected_count
        
        # Get the total count
        count = self.history.get_total_deals()
        
        # Verify the result
        self.assertEqual(count, expected_count)
        self.mock_mt5.history_deals_total.assert_called_once()
        
        if VERBOSITY >= 2:
            print(f"✅ Successfully retrieved total deals count: {count}")
    
    def test_get_total_orders(self):
        """Test getting total orders count."""
        self.run_test_with_message("Testing total orders count", "🔢")
        
        # Set up expected value
        expected_count = 27
        self.mock_mt5.history_orders_total.return_value = expected_count
        
        # Get the total count
        count = self.history.get_total_orders()
        
        # Verify the result
        self.assertEqual(count, expected_count)
        self.mock_mt5.history_orders_total.assert_called_once()
        
        if VERBOSITY >= 2:
            print(f"✅ Successfully retrieved total orders count: {count}")
    
    def test_connection_error(self):
        """Test behavior when not connected."""
        self.run_test_with_message("Testing connection error handling", "❌")
        
        # Configure mock to simulate not connected
        self.connection.is_connected.return_value = False
        
        # Try to get deals
        with self.assertRaises(ConnectionError):
            self.history.get_deals()
        
        # Try to get orders
        with self.assertRaises(ConnectionError):
            self.history.get_orders()
        
        if VERBOSITY >= 2:
            print("✅ Successfully detected connection error")
    
    def test_deals_retrieval_error(self):
        """Test behavior when deals retrieval fails."""
        self.run_test_with_message("Testing deals retrieval error", "❌")
        
        # Configure mock to simulate retrieval failure
        self.mock_mt5.history_deals_get.return_value = None
        self.mock_mt5.last_error.return_value = (1, "Test error message")
        
        # Try to get deals
        with self.assertRaises(DealsHistoryError):
            self.history.get_deals()
        
        if VERBOSITY >= 2:
            print("✅ Successfully detected deals retrieval error")
    
    def test_orders_retrieval_error(self):
        """Test behavior when orders retrieval fails."""
        self.run_test_with_message("Testing orders retrieval error", "❌")
        
        # Configure mock to simulate retrieval failure
        self.mock_mt5.history_orders_get.return_value = None
        self.mock_mt5.last_error.return_value = (1, "Test error message")
        
        # Try to get orders
        with self.assertRaises(OrdersHistoryError):
            self.history.get_orders()
        
        if VERBOSITY >= 2:
            print("✅ Successfully detected orders retrieval error")

    def test_get_deals_positional_params(self):
        """Test that get_deals uses positional parameters for dates with MT5 API."""
        # Setup test dates
        from_date = datetime(2025, 1, 1)
        to_date = datetime(2025, 2, 1)
        
        # Call the method
        self.history.get_deals(from_date, to_date)
        
        # Verify MT5 API was called with positional arguments
        self.mock_mt5.history_deals_get.assert_called_once()
        args, kwargs = self.mock_mt5.history_deals_get.call_args
        
        # Check that dates were passed as positional arguments
        self.assertEqual(len(args), 2)
        self.assertEqual(args[0], from_date)
        self.assertEqual(args[1], to_date)
        # Ensure no date parameters were passed as keywords
        self.assertNotIn('date_from', kwargs)
        self.assertNotIn('date_to', kwargs)
    
    def test_get_orders_positional_params(self):
        """Test that get_orders uses positional parameters for dates with MT5 API."""
        # Setup test dates
        from_date = datetime(2025, 1, 1)
        to_date = datetime(2025, 2, 1)
        
        # Call the method
        self.history.get_orders(from_date, to_date)
        
        # Verify MT5 API was called with positional arguments
        self.mock_mt5.history_orders_get.assert_called_once()
        args, kwargs = self.mock_mt5.history_orders_get.call_args
        
        # Check that dates were passed as positional arguments
        self.assertEqual(len(args), 2)
        self.assertEqual(args[0], from_date)
        self.assertEqual(args[1], to_date)
        # Ensure no date parameters were passed as keywords
        self.assertNotIn('date_from', kwargs)
        self.assertNotIn('date_to', kwargs)
    
    def test_get_total_deals_positional_params(self):
        """Test that get_total_deals uses positional parameters with MT5 API."""
        # Setup test dates
        from_date = datetime(2025, 1, 1)
        to_date = datetime(2025, 2, 1)
        
        # Call the method
        self.history.get_total_deals(from_date, to_date)
        
        # Verify MT5 API was called with positional arguments
        self.mock_mt5.history_deals_total.assert_called_once()
        args, kwargs = self.mock_mt5.history_deals_total.call_args
        
        # Check that dates were passed as positional arguments
        self.assertEqual(len(args), 2)
        self.assertEqual(args[0], from_date)
        self.assertEqual(args[1], to_date)
        # Ensure NO keyword arguments were used
        self.assertEqual(len(kwargs), 0)
    
    def test_get_total_orders_positional_params(self):
        """Test that get_total_orders uses positional parameters with MT5 API."""
        # Setup test dates
        from_date = datetime(2025, 1, 1)
        to_date = datetime(2025, 2, 1)
        
        # Call the method
        self.history.get_total_orders(from_date, to_date)
        
        # Verify MT5 API was called with positional arguments
        self.mock_mt5.history_orders_total.assert_called_once()
        args, kwargs = self.mock_mt5.history_orders_total.call_args
        
        # Check that dates were passed as positional arguments
        self.assertEqual(len(args), 2)
        self.assertEqual(args[0], from_date)
        self.assertEqual(args[1], to_date)
        # Ensure NO keyword arguments were used
        self.assertEqual(len(kwargs), 0)


# =============================================================================
# Positional Parameter Tests
# =============================================================================

class TestMT5HistoryParameterPassing(unittest.TestCase):
    """Test that MT5History methods use positional parameters correctly with MT5 API."""

    def setUp(self):
        """Set up test environment with minimal mocks."""
        # We only need to mock the mt5 module, no need for full MockedTestCase setup
        self.connection = MagicMock()
        self.connection.is_connected.return_value = True
        
        # Create history instance with our mocked connection
        self.history = MT5History(self.connection)
        
        # Patch MT5 module directly for this test
        self.mt5_patcher = patch('MetaTraderMCPServer.client.history.mt5')
        self.mock_mt5 = self.mt5_patcher.start()
        
        # Mock successful returns
        self.mock_mt5.history_deals_get.return_value = [MockHelpers.create_mock_deal()]
        self.mock_mt5.history_orders_get.return_value = [MockHelpers.create_mock_order()]
        self.mock_mt5.history_deals_total.return_value = 1
        self.mock_mt5.history_orders_total.return_value = 1
    
    def tearDown(self):
        """Clean up the mock."""
        self.mt5_patcher.stop()
    
    def test_get_deals_positional_date_params(self):
        """Test that get_deals uses positional parameters for dates."""
        from_date = datetime(2025, 1, 1)
        to_date = datetime(2025, 2, 1)
        
        # Call the method
        self.history.get_deals(from_date, to_date)
        
        # Verify MT5 API was called with positional arguments
        args, kwargs = self.mock_mt5.history_deals_get.call_args
        
        # Check that dates were passed as positional arguments
        self.assertEqual(len(args), 2)
        self.assertEqual(args[0], from_date)
        self.assertEqual(args[1], to_date)
    
    def test_get_orders_positional_date_params(self):
        """Test that get_orders uses positional parameters for dates."""
        from_date = datetime(2025, 1, 1)
        to_date = datetime(2025, 2, 1)
        
        # Call the method
        self.history.get_orders(from_date, to_date)
        
        # Verify MT5 API was called with positional arguments
        args, kwargs = self.mock_mt5.history_orders_get.call_args
        
        # Check that dates were passed as positional arguments
        self.assertEqual(len(args), 2)
        self.assertEqual(args[0], from_date)
        self.assertEqual(args[1], to_date)
    
    def test_get_total_deals_positional_date_params(self):
        """Test that get_total_deals uses positional parameters only."""
        from_date = datetime(2025, 1, 1)
        to_date = datetime(2025, 2, 1)
        
        # Call the method
        self.history.get_total_deals(from_date, to_date)
        
        # Verify MT5 API was called with positional arguments
        args, kwargs = self.mock_mt5.history_deals_total.call_args
        
        # Check that dates were passed as positional arguments
        self.assertEqual(len(args), 2)
        self.assertEqual(args[0], from_date)
        self.assertEqual(args[1], to_date)
        self.assertEqual(len(kwargs), 0, "Should not use any keyword arguments")
    
    def test_get_total_orders_positional_date_params(self):
        """Test that get_total_orders uses positional parameters only."""
        from_date = datetime(2025, 1, 1)
        to_date = datetime(2025, 2, 1)
        
        # Call the method
        self.history.get_total_orders(from_date, to_date)
        
        # Verify MT5 API was called with positional arguments
        args, kwargs = self.mock_mt5.history_orders_total.call_args
        
        # Check that dates were passed as positional arguments
        self.assertEqual(len(args), 2)
        self.assertEqual(args[0], from_date)
        self.assertEqual(args[1], to_date)
        self.assertEqual(len(kwargs), 0, "Should not use any keyword arguments")


# =============================================================================
# Integration Tests (With Real MT5 Connection)
# =============================================================================

class TestMT5HistoryIntegration(IntegrationTestCase):
    """Integration tests for the MT5History class with real MT5 connection."""
    
    def setUp(self):
        """Set up integration tests."""
        try:
            super().setUp()
            # Skip all tests if no MT5 connection
            if not self.connection.is_connected():
                self.skipTest("No MT5 connection available for integration tests")
        except Exception as e:
            self.skipTest(f"Could not connect to MT5: {str(e)}")
    
    def test_real_deals_retrieval(self):
        """Test retrieving real deals from MT5."""
        self.run_test_with_message("Testing deals retrieval from real MT5", "🔄")
        
        # Use a small date range to avoid too much data
        from_date = datetime.now() - timedelta(days=30)
        
        try:
            deals = self.history.get_deals(from_date=from_date)
            
            # We can only verify that we got a response, not specific data
            self.assertIsInstance(deals, list)
            
            if VERBOSITY >= 2:
                print(f"✅ Successfully retrieved {len(deals)} deals from real MT5")
                
        except Exception as e:
            self.fail(f"Failed to retrieve deals: {str(e)}")
    
    def test_real_orders_retrieval(self):
        """Test retrieving real orders from MT5."""
        self.run_test_with_message("Testing orders retrieval from real MT5", "🔄")
        
        # Use a small date range to avoid too much data
        from_date = datetime.now() - timedelta(days=30)
        
        try:
            orders = self.history.get_orders(from_date=from_date)
            
            # We can only verify that we got a response, not specific data
            self.assertIsInstance(orders, list)
            
            if VERBOSITY >= 2:
                print(f"✅ Successfully retrieved {len(orders)} orders from real MT5")
        
        except Exception as e:
            self.fail(f"Failed to retrieve orders: {str(e)}")


# =============================================================================
# No Connection Tests
# =============================================================================

class TestMT5HistoryNoConnection(BaseTestCase):
    """Edge case tests for when there is no connection."""
    
    def test_no_connection(self):
        """Test behavior when not connected."""
        self.run_test_with_message("Testing behavior with no connection", "🔌")
        
        # Create connection that is not connected
        connection = MagicMock()
        connection.is_connected.return_value = False
        
        # Create history instance with disconnected connection
        history = MT5History(connection)
        
        # Test various methods
        with self.assertRaises(ConnectionError):
            history.get_deals()
        
        with self.assertRaises(ConnectionError):
            history.get_orders()
        
        if VERBOSITY >= 2:
            print("✅ Successfully detected connection errors in all methods")


# =============================================================================
# Simple Test Function
# =============================================================================

def simple_test():
    """Run a simple test of MT5 History functionality."""
    print("\n=== Simple History Module Test ===\n")
    
    # Connect to MT5
    print("Connecting to MT5...")
    try:
        import MetaTrader5 as mt5
        if not mt5.initialize():
            print(f"❌ Failed to connect to MT5: {mt5.last_error()[1]}")
            return
        print("✅ Connected to MT5 successfully!")
        
        # Add some MT5 terminal info for debugging
        print("\nMT5 Terminal Info:")
        terminal_info = mt5.terminal_info()
        if terminal_info is not None:
            terminal_info_dict = terminal_info._asdict()
            print(f"  Community Account: {terminal_info_dict.get('community_account', 'N/A')}")
            print(f"  Community Connection: {terminal_info_dict.get('community_connection', 'N/A')}")
            print(f"  Connected: {terminal_info_dict.get('connected', 'N/A')}")
            print(f"  Trade Allowed: {terminal_info_dict.get('trade_allowed', 'N/A')}")
            print(f"  EA Enabled: {terminal_info_dict.get('ea_enabled', 'N/A')}")
            print(f"  DLL Allowed: {terminal_info_dict.get('dlls_allowed', 'N/A')}")
            print(f"  MT5 Version: {terminal_info_dict.get('version', 'N/A')}")
            print(f"  Balance: {terminal_info_dict.get('balance', 'N/A')}")
        else:
            print("  ❌ Failed to get terminal info")
            
        # Get account info
        print("\nAccount Info:")
        account_info = mt5.account_info()
        if account_info is not None:
            account_info_dict = account_info._asdict()
            print(f"  Login: {account_info_dict.get('login', 'N/A')}")
            print(f"  Server: {account_info_dict.get('server', 'N/A')}")
            print(f"  Balance: {account_info_dict.get('balance', 'N/A')}")
            print(f"  Equity: {account_info_dict.get('equity', 'N/A')}")
            print(f"  Leverage: {account_info_dict.get('leverage', 'N/A')}")
        else:
            print("  ❌ Failed to get account info")
            
        # Check if history functions are available
        print("\nChecking history availability...")
        try:
            # Need BOTH from_date and to_date parameters for history functions
            from_date = datetime.now() - timedelta(days=30)
            to_date = datetime.now()
            print(f"Checking deals from {from_date} to {to_date}")
            
            # Try direct MT5 API call with proper parameters
            deals_count = mt5.history_deals_total(from_date, to_date)
            if deals_count is not None:
                print(f"✅ History deals API available, total deals: {deals_count}")
            else:
                error = mt5.last_error()
                print(f"❌ MT5 API error: {error[1]} (code: {error[0]})")
        except Exception as e:
            print(f"❌ Direct MT5 history deals API error: {str(e)}")
        
        # Create History instance
        print("\nCreating history instance...")
        from MetaTraderMCPServer.client.connection import MT5Connection
        from MetaTraderMCPServer.client.history import MT5History
        
        # Try to get configuration from config.py
        try:
            from tests.config import MT5_CONFIG
            config = MT5_CONFIG
        except (ImportError, ModuleNotFoundError):
            # Fallback configuration
            config = {
                'path': '',  # Path to MT5 terminal executable
                'login': 12345,
                'password': 'password',
                'server': 'Demo',
                'timeout': 60000
            }
        
        connection = MT5Connection(config)
        connection.connect()
        
        if not connection.is_connected():
            print("❌ Failed to connect using MT5Connection!")
            mt5.shutdown()
            return
        print("✅ MT5Connection established successfully")
        
        history = MT5History(connection)
        
        # Try different approaches to retrieve deals
        print("\nAttempting to retrieve deal history...")
        
        # Try with proper date parameters (both from_date and to_date are required by MT5 API)
        try:
            # Use the same date range we verified works with direct API
            from_date = datetime.now() - timedelta(days=30)
            to_date = datetime.now()
            print(f"Retrieving deals from {from_date} to {to_date}")
            
            deals = history.get_deals(from_date, to_date)
            print(f"✅ Retrieved {len(deals)} deals")
            
            if deals:
                print(f"  First deal ticket: {deals[0]['ticket']}")
                print(f"  First deal profit: {deals[0]['profit']}")
        except Exception as e:
            print(f"❌ Error with date parameters: {str(e)}")
            
            # Try with ticket parameter instead
            try:
                # Try a specific ticket number (could work if deals exist)
                ticket = 1  # Just trying a common first ticket
                print(f"Trying with ticket={ticket}")
                deals = history.get_deals(ticket=ticket)
                print(f"✅ Retrieved deals for ticket {ticket}")
            except Exception as e:
                print(f"❌ Error with ticket parameter: {str(e)}")
                
                # Try with specific group pattern (some servers require this)
                try:
                    # Different group patterns to try
                    print("Trying with various group patterns...")
                    for group in ["*", "*USD*", "*EUR*"]:
                        try:
                            print(f"  Testing group pattern: {group}")
                            deals = history.get_deals(from_date, to_date, group=group)
                            print(f"  ✅ Group '{group}' worked! Retrieved {len(deals)} deals")
                            break
                        except Exception as group_e:
                            print(f"  ❌ Group '{group}' failed: {str(group_e)}")
                except Exception as e:
                    print(f"❌ All group patterns failed: {str(e)}")
        
        # Test total counts (should be safe even with no data)
        print("\nGetting total counts...")
        try:
            # MT5 API requires positional arguments, not keyword arguments!
            from_date = datetime.now() - timedelta(days=30)
            to_date = datetime.now()
            
            # Try a direct call to the MT5 API to confirm syntax
            print("Trying direct API call:")
            direct_count = mt5.history_deals_total(from_date, to_date)  # Positional arguments
            print(f"  ✅ Direct API call works: {direct_count} deals")
            
            # Now try our wrapper with positional args (the way our module should implement it)
            print("Trying with our History module:")
            deals_count = history.get_total_deals(from_date, to_date)  # Try positional args
            orders_count = history.get_total_orders(from_date, to_date)  # Try positional args
            print(f"  ✅ Total deals: {deals_count}, Total orders: {orders_count}")
            
        except Exception as e:
            print(f"❌ Error getting counts: {str(e)}")
            # Let's try a fallback approach for diagnostics
            try:
                print("Trying direct API diagnostics:")
                # Use a simple date range and print exact call format
                start_date = datetime(2025, 3, 1)
                end_date = datetime(2025, 4, 10)
                print(f"  Direct API call with: mt5.history_deals_total({start_date}, {end_date})")
                test_count = mt5.history_deals_total(start_date, end_date)
                print(f"  ✅ API result: {test_count}")
            except Exception as debug_e:
                print(f"  ❌ Debug also failed: {str(debug_e)}")
        
        # Disconnect from MT5
        print("\nDisconnecting from MT5...")
        mt5.shutdown()
        print("✅ Disconnected from MT5")
        
    except ImportError:
        print("❌ MetaTrader5 package not installed.")
    except Exception as e:
        print(f"❌ Unexpected error: {str(e)}")
    
    print("\n=== Simple Test Completed ===")


if __name__ == "__main__":
    """Run history tests."""
    if len(sys.argv) > 1:
        # Run with command line arguments
        if sys.argv[1] == "simple":
            # Run simple test function
            simple_test()
            sys.exit(0)
        
        # If arguments are present but not "simple", run unittest with them
        unittest.main()
    else:
        # Check if TEST_MODE is set to override mode
        test_mode = os.environ.get("MT5_TEST_MODE", TEST_MODE).lower()
        
        if test_mode == "simple":
            # Run simple test function
            simple_test()
        elif test_mode == "unit":
            # Run only unit tests
            suite = unittest.TestLoader().loadTestsFromTestCase(TestMT5HistoryUnit)
            unittest.TextTestRunner(verbosity=VERBOSITY).run(suite)
        elif test_mode == "integration":
            # Run only integration tests
            suite = unittest.TestLoader().loadTestsFromTestCase(TestMT5HistoryIntegration)
            unittest.TextTestRunner(verbosity=VERBOSITY).run(suite)
        else:
            # Run all tests
            unittest.main(verbosity=VERBOSITY)
