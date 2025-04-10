"""
Main test runner for MetaTrader MCP Server.

This module provides a central place to run all tests for the project.
"""
import os
import sys
import unittest
import time

# Add the project root to the path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Import test configuration
from tests.config import MT5_CONFIG, TEST_MODE, USE_MOCKS, VERBOSITY, print_test_config_help

# Import test modules
from tests.client.connection import TestMT5Connection, TestMT5ConnectionLongRunning, simple_connection_test
from tests.client.account import (
    TestMT5AccountUnit, TestMT5AccountIntegration, 
    TestMT5AccountNoConnection, simple_account_test
)


def run_unit_tests(verbosity=2):
    """
    Run unit tests with mocks.
    """
    print("\n🧪 Running unit tests for MetaTrader MCP Server...")
    
    # Create a test suite
    suite = unittest.TestSuite()
    
    # Add account unit tests with mocks
    account_suite = unittest.TestLoader().loadTestsFromTestCase(TestMT5AccountUnit)
    suite.addTest(account_suite)
    
    # Run the suite
    start_time = time.time()
    result = unittest.TextTestRunner(verbosity=verbosity).run(suite)
    duration = time.time() - start_time
    
    print(f"\n✨ Unit tests completed in {duration:.2f} seconds")
    return result


def run_integration_tests(verbosity=2):
    """
    Run integration tests with real MT5 connection.
    """
    print("\n🌐 Running integration tests for MetaTrader MCP Server...")
    
    # Create a test suite
    suite = unittest.TestSuite()
    
    # Add connection tests
    connection_suite = unittest.TestLoader().loadTestsFromTestCase(TestMT5Connection)
    suite.addTest(connection_suite)
    
    # Add account integration tests
    account_suite = unittest.TestLoader().loadTestsFromTestCase(TestMT5AccountIntegration)
    suite.addTest(account_suite)
    
    # Add no connection test
    no_connection_suite = unittest.TestLoader().loadTestsFromTestCase(TestMT5AccountNoConnection)
    suite.addTest(no_connection_suite)
    
    # Run the suite
    start_time = time.time()
    result = unittest.TextTestRunner(verbosity=verbosity).run(suite)
    duration = time.time() - start_time
    
    print(f"\n✨ Integration tests completed in {duration:.2f} seconds")
    return result


def run_all_tests(verbosity=2):
    """
    Run all tests for the project.
    """
    print("\n🚀 Running all tests for MetaTrader MCP Server...")
    
    # Run unit tests first
    unit_result = run_unit_tests(verbosity)
    
    # Run integration tests if not forced to use mocks
    integration_result = None
    if USE_MOCKS != "always":
        integration_result = run_integration_tests(verbosity)
    
    # Print overall results
    print("\n📊 Test Results Summary:")
    print(f"Unit Tests: {'✅ PASSED' if unit_result.wasSuccessful() else '❌ FAILED'}")
    
    if integration_result:
        print(f"Integration Tests: {'✅ PASSED' if integration_result.wasSuccessful() else '❌ FAILED'}")
    else:
        print("Integration Tests: ⚠️ SKIPPED (Using mocks only)")
    
    # Return whether all tests passed
    if integration_result:
        return unit_result.wasSuccessful() and integration_result.wasSuccessful()
    else:
        return unit_result.wasSuccessful()


def run_connection_tests(verbosity=2):
    """
    Run only connection tests.
    """
    print("\n🔌 Running connection tests for MetaTrader MCP Server...")
    
    # Create a test suite
    suite = unittest.TestSuite()
    
    # Add connection tests
    connection_suite = unittest.TestLoader().loadTestsFromTestCase(TestMT5Connection)
    suite.addTest(connection_suite)
    
    # Run the suite
    start_time = time.time()
    result = unittest.TextTestRunner(verbosity=verbosity).run(suite)
    duration = time.time() - start_time
    
    print(f"\n✨ Connection tests completed in {duration:.2f} seconds")
    return result


def run_account_tests(verbosity=2):
    """
    Run account tests, choosing unit or integration based on settings.
    """
    print("\n💼 Running account tests for MetaTrader MCP Server...")
    
    # Create a test suite
    suite = unittest.TestSuite()
    
    if USE_MOCKS == "always" or USE_MOCKS == "auto":
        # Use unit tests with mocks
        print("Using mocked MT5 connection for account tests...")
        account_suite = unittest.TestLoader().loadTestsFromTestCase(TestMT5AccountUnit)
        suite.addTest(account_suite)
    else:
        # Use integration tests with real connection
        print("Using real MT5 connection for account tests...")
        account_suite = unittest.TestLoader().loadTestsFromTestCase(TestMT5AccountIntegration)
        suite.addTest(account_suite)
        
        # Add no connection test
        no_connection_suite = unittest.TestLoader().loadTestsFromTestCase(TestMT5AccountNoConnection)
        suite.addTest(no_connection_suite)
    
    # Run the suite
    start_time = time.time()
    result = unittest.TextTestRunner(verbosity=verbosity).run(suite)
    duration = time.time() - start_time
    
    print(f"\n✨ Account tests completed in {duration:.2f} seconds")
    return result


def run_long_tests(verbosity=2):
    """
    Run long-running tests that take more time.
    """
    print("\n⏱️ Running long-running tests for MetaTrader MCP Server...")
    
    # Create a test suite
    suite = unittest.TestSuite()
    
    # Add long-running connection tests
    long_suite = unittest.TestLoader().loadTestsFromTestCase(TestMT5ConnectionLongRunning)
    suite.addTest(long_suite)
    
    # Run the suite
    start_time = time.time()
    result = unittest.TextTestRunner(verbosity=verbosity).run(suite)
    duration = time.time() - start_time
    
    print(f"\n✨ Long tests completed in {duration:.2f} seconds")
    return result


def run_simple_tests():
    """
    Run simple tests without the unittest framework.
    This is useful for quick verification without the overhead of unittest.
    """
    print("\n🔍 Running simple tests for MetaTrader MCP Server...")
    
    if USE_MOCKS == "always":
        print("⚠️ Warning: Simple tests require a real MT5 connection.")
        print("Using mock data instead for demonstration purposes.")
        # Only run account test which supports mocks
        print("\n=== Account Tests ===")
        simple_account_test()
    else:
        print("\n=== Connection Tests ===")
        # Run simple connection test
        simple_connection_test()
        
        print("\n=== Account Tests ===")
        # Run simple account test
        simple_account_test()
    
    print("\n✨ Simple tests completed")
    return True


def print_header():
    """Print a nice header for the test runner."""
    print("\n" + "=" * 70)
    print("🚀 MetaTrader MCP Server Test Runner 🚀")
    print("=" * 70)
    print(f"Test Mode: {TEST_MODE}")
    print(f"Use Mocks: {USE_MOCKS}")
    print(f"Verbosity: {VERBOSITY}")
    
    # Show login info only if not in unit test mode and if real connections are used
    if TEST_MODE != "unit" and USE_MOCKS != "always":
        print(f"MT5 Login: {MT5_CONFIG['login']}")
        print(f"MT5 Server: {MT5_CONFIG['server']}")
    
    print("=" * 70 + "\n")


if __name__ == "__main__":
    """
    Main entry point for running tests.
    
    Usage:
        python -m tests.run_tests [mode] [--help]
        
    Modes:
        unit:        Run unit tests with mocks
        integration: Run integration tests with real MT5 connection
        mixed:       Run both unit and integration tests (default)
        account:     Run only account tests (mocked or real based on settings)
        connection:  Run only connection tests (requires real MT5)
        simple:      Run simple tests without unittest framework
        long:        Run long-running tests
        all:         Run all tests (unit, integration, simple, and long)
        --help:      Show help
    """
    # Print test header
    print_header()
    
    # Get the test mode from command line arguments or config
    mode = TEST_MODE
    if len(sys.argv) > 1:
        if sys.argv[1] == "--help":
            print_test_config_help()
            print("\nUsage:")
            print("  python -m tests.run_tests [mode] [--help]")
            print("\nModes:")
            print("  unit:        Run unit tests with mocks")
            print("  integration: Run integration tests with real MT5 connection")
            print("  mixed:       Run both unit and integration tests (default)")
            print("  account:     Run only account tests (mocked or real based on settings)")
            print("  connection:  Run only connection tests (requires real MT5)")
            print("  simple:      Run simple tests without unittest framework")
            print("  long:        Run long-running tests")
            print("  all:         Run all tests (unit, integration, simple, and long)")
            sys.exit(0)
        else:
            mode = sys.argv[1].lower()
    
    # Set success flag to track overall test success
    success = True
    
    # Run tests based on mode
    if mode == "unit":
        success = run_unit_tests(VERBOSITY).wasSuccessful()
    elif mode == "integration":
        if USE_MOCKS == "always":
            print("⚠️ Warning: Cannot run integration tests when USE_MOCKS is set to 'always'.")
            print("Please set USE_MOCKS to 'never' or 'auto' to run integration tests.")
            success = False
        else:
            success = run_integration_tests(VERBOSITY).wasSuccessful()
    elif mode == "mixed":
        success = run_all_tests(VERBOSITY)
    elif mode == "account":
        success = run_account_tests(VERBOSITY).wasSuccessful()
    elif mode == "connection":
        if USE_MOCKS == "always":
            print("⚠️ Warning: Cannot run connection tests when USE_MOCKS is set to 'always'.")
            print("Please set USE_MOCKS to 'never' or 'auto' to run connection tests.")
            success = False
        else:
            success = run_connection_tests(VERBOSITY).wasSuccessful()
    elif mode == "simple":
        success = run_simple_tests()
    elif mode == "long":
        if USE_MOCKS == "always":
            print("⚠️ Warning: Cannot run long tests when USE_MOCKS is set to 'always'.")
            print("Please set USE_MOCKS to 'never' or 'auto' to run long tests.")
            success = False
        else:
            success = run_long_tests(VERBOSITY).wasSuccessful()
    elif mode == "all":
        # Run unit tests
        unit_success = run_unit_tests(VERBOSITY).wasSuccessful()
        success = unit_success
        
        # Run integration tests if not forced to use mocks
        if USE_MOCKS != "always":
            print("\n---")
            integration_success = run_integration_tests(VERBOSITY).wasSuccessful()
            success = success and integration_success
            
            # Run simple tests
            print("\n---")
            simple_success = run_simple_tests()
            success = success and simple_success
            
            # Run long tests
            print("\n---")
            long_success = run_long_tests(VERBOSITY).wasSuccessful()
            success = success and long_success
    else:
        print(f"❌ Unknown test mode: {mode}")
        print("Run with --help for usage information")
        sys.exit(1)
    
    # Print final status
    if success:
        print("\n✅ All tests completed successfully! 🎉")
    else:
        print("\n❌ Some tests failed! Please check the output above for details.")
        sys.exit(1)
