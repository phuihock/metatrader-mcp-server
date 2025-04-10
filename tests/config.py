"""
Test configuration for MetaTrader MCP Server.

This module contains configuration settings for tests.
These can be overridden by environment variables.
"""
import os


# MetaTrader 5 connection configuration
MT5_CONFIG = {
    "path": os.environ.get("MT5_PATH", "C:\\Program Files\\MetaTrader 5\\terminal64.exe"),
    "login": int(os.environ.get("MT5_LOGIN", "240294046")),
    "password": os.environ.get("MT5_PASSWORD", "ExnessDemo123!"),
    "server": os.environ.get("MT5_SERVER", "Exness-MT5Trial6"),
    "timeout": int(os.environ.get("MT5_TIMEOUT", "60000")),
    "portable": os.environ.get("MT5_PORTABLE", "False").lower() == "true",
    "debug": os.environ.get("MT5_DEBUG", "True").lower() == "true",
}

# Test modes
# - unit: Only run unit tests with mocks
# - integration: Only run integration tests with real MT5 connection
# - mixed: Run both unit and integration tests
# - simple: Run simple test function for quick verification
# - all: Run all tests (unit, integration, and simple)
TEST_MODE = os.environ.get("MT5_TEST_MODE", "mixed")

# Mock configuration
# - always: Always use mocks even if MT5 is available
# - never: Never use mocks, always try to connect to MT5
# - auto: Use mocks if MT5 is not available, otherwise connect to MT5
USE_MOCKS = os.environ.get("MT5_USE_MOCKS", "auto")

# Demo account details (for mocking)
DEMO_ACCOUNT = {
    "login": 240294046,
    "trade_mode": 1,  # demo
    "leverage": 200,
    "balance": 1530.25,
    "equity": 1530.25,
    "margin": 0.0,
    "margin_free": 1530.25,
    "margin_level": 0.0,
    "currency": "USD",
    "profit": 0.0,
    "name": "Test Trader",
    "server": "Exness-MT5Trial6",
    "company": "Exness",
    "credit": 0.0,
    "limit_orders": 0,
    "margin_so_call": 80.0,
    "margin_so_mode": 0,
    "margin_so_so": 40.0,
    "assets": 1530.25,
    "liabilities": 0.0,
    "commission_blocked": 0.0,
    "trade_allowed": True,
    "trade_expert": True,
    "trade_time_limit": 0
}

# Test settings
# Verbosity levels:
# 0 = minimal output
# 1 = normal output
# 2 = verbose output with test messages
# 3 = extra verbose with detailed output
VERBOSITY = int(os.environ.get("MT5_TEST_VERBOSITY", "2"))

# Test data directory for mock testing
TEST_DATA_DIR = os.path.join(os.path.dirname(__file__), "data")

# Create test data directory if it doesn't exist
if not os.path.exists(TEST_DATA_DIR):
    os.makedirs(TEST_DATA_DIR)

# Test configuration help
def print_test_config_help():
    """Print help information about test configuration."""
    print("\n📋 Test Configuration Help 📋")
    print("=" * 50)
    print("Environment Variables:")
    print("  MT5_PATH     - Path to MetaTrader 5 terminal")
    print("  MT5_LOGIN    - MetaTrader 5 account login")
    print("  MT5_PASSWORD - MetaTrader 5 account password")
    print("  MT5_SERVER   - MetaTrader 5 server")
    print("  MT5_TIMEOUT  - Connection timeout in milliseconds")
    print("  MT5_DEBUG    - Enable debug logging (True/False)")
    print("  MT5_TEST_MODE - Test mode (unit/integration/mixed/simple/all)")
    print("  MT5_USE_MOCKS - When to use mocks (always/never/auto)")
    print("  MT5_TEST_VERBOSITY - Verbosity level (0-3)")
    print("\nTest Modes:")
    print("  unit        - Only run unit tests with mocks")
    print("  integration - Only run integration tests with real MT5 connection")
    print("  mixed       - Run both unit and integration tests (default)")
    print("  simple      - Run simple test function for quick verification")
    print("  all         - Run all tests (unit, integration, and simple)")
    print("\nMock Settings:")
    print("  always - Always use mocks even if MT5 is available")
    print("  never  - Never use mocks, always try to connect to MT5")
    print("  auto   - Use mocks if MT5 is not available (default)")
    print("=" * 50)


if __name__ == "__main__":
    # Print test configuration help when this module is run directly
    print_test_config_help()
    
    # Print current configuration
    print("\n🔧 Current Configuration 🔧")
    print(f"Test Mode: {TEST_MODE}")
    print(f"Use Mocks: {USE_MOCKS}")
    print(f"Verbosity: {VERBOSITY}")
    print(f"MT5 Login: {MT5_CONFIG['login']}")
    print(f"MT5 Server: {MT5_CONFIG['server']}")
    print(f"Debug Mode: {'Enabled' if MT5_CONFIG['debug'] else 'Disabled'}")
