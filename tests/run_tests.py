"""
Main test runner for MetaTrader MCP Server.

This module provides a central place to run all tests for the project.
"""
import os
import sys
import unittest

# Add the project root to the path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Import test modules
from tests.client.connection import TestMT5Connection, TestMT5ConnectionLongRunning, simple_connection_test


def run_all_tests():
    """
    Run all unit tests for the project.
    """
    print("🚀 Running all tests for MetaTrader MCP Server...")
    
    # Create a test suite
    suite = unittest.TestSuite()
    
    # Add all connection tests
    connection_suite = unittest.TestLoader().loadTestsFromTestCase(TestMT5Connection)
    suite.addTest(connection_suite)
    
    # Run the suite
    result = unittest.TextTestRunner().run(suite)
    return result


def run_long_tests():
    """
    Run long-running tests that take more time.
    """
    print("🚀 Running long-running tests for MetaTrader MCP Server...")
    
    # Create a test suite
    suite = unittest.TestSuite()
    
    # Add long-running connection tests
    long_suite = unittest.TestLoader().loadTestsFromTestCase(TestMT5ConnectionLongRunning)
    suite.addTest(long_suite)
    
    # Run the suite
    result = unittest.TextTestRunner().run(suite)
    return result


def run_simple_tests():
    """
    Run simple tests without the unittest framework.
    """
    print("🚀 Running simple tests for MetaTrader MCP Server...")
    
    # Connection simple test
    simple_connection_test()


if __name__ == "__main__":
    """
    Main entry point for running tests.
    
    Usage:
        python -m tests.run_tests [mode]
        
    Modes:
        all: Run all unit tests (default)
        simple: Run simple tests without unittest framework
        long: Run long-running tests
    """
    # Get the test mode from command line arguments
    mode = "all"
    if len(sys.argv) > 1:
        mode = sys.argv[1].lower()
    
    # Run tests based on mode
    if mode == "simple":
        run_simple_tests()
    elif mode == "long":
        run_long_tests()
    else:
        run_all_tests()
