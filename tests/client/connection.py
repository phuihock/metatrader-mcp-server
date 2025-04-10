"""
Tests for the MetaTrader 5 client connection module.

This file contains test cases for the MT5Connection class.
"""
import os
import sys
import unittest
import time
import random
from datetime import datetime
import threading

# Add src directory to path to import the client package
sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..', 'src'))

# Add tests directory to path to handle running the file directly
sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..'))

# Import test configuration (try both ways to handle direct or indirect running)
try:
    # First try relative import (when run through run_tests.py)
    from tests.config import MT5_CONFIG, TEST_MODE, USE_MOCKS, DEMO_ACCOUNT, VERBOSITY
except ModuleNotFoundError:
    # Fall back to direct import (when run directly)
    from config import MT5_CONFIG, TEST_MODE, USE_MOCKS, DEMO_ACCOUNT, VERBOSITY

from MetaTraderMCPServer.client.connection import MT5Connection
from MetaTraderMCPServer.client.exceptions import ConnectionError, InitializationError, LoginError


class TestMT5Connection(unittest.TestCase):
    """Test cases for the MT5Connection class."""

    def setUp(self):
        """Set up the test environment."""
        self.config = {
            "path": "C:\\Program Files\\MetaTrader 5\\terminal64.exe",
            "login": 240294046,
            "password": "ExnessDemo123!",
            "server": "Exness-MT5Trial6",
            "timeout": 60000,  # 60 seconds
            "portable": False
        }
        self.connection = MT5Connection(self.config)
    
    def tearDown(self):
        """Clean up the test environment."""
        # Ensure disconnection even if tests fail
        try:
            self.connection.disconnect()
        except:
            pass

    def test_connect(self):
        """Test the connect method."""
        print("\n\n🔄 Testing connection to MetaTrader 5 terminal...")
        try:
            result = self.connection.connect()
            self.assertTrue(result)
            self.assertTrue(self.connection.is_connected())
            print("✅ Connection successful!")
        except Exception as e:
            self.fail(f"❌ Connection failed with error: {str(e)}")
    
    def test_get_terminal_info(self):
        """Test the get_terminal_info method."""
        print("\n\n🔄 Testing get_terminal_info...")
        try:
            self.connection.connect()
            info = self.connection.get_terminal_info()
            self.assertIsNotNone(info)
            print(f"✅ Terminal info retrieved successfully!")
            print(f"📊 Terminal details:")
            for key, value in sorted(info.items()):
                print(f"   {key}: {value}")
        except Exception as e:
            self.fail(f"❌ Failed to get terminal info: {str(e)}")
    
    def test_get_version(self):
        """Test the get_version method."""
        print("\n\n🔄 Testing get_version...")
        try:
            self.connection.connect()
            version = self.connection.get_version()
            self.assertIsNotNone(version)
            self.assertEqual(len(version), 4)
            print(f"✅ Terminal version: {version[0]}.{version[1]}.{version[2]}.{version[3]}")
        except Exception as e:
            self.fail(f"❌ Failed to get version: {str(e)}")
    
    def test_disconnect(self):
        """Test the disconnect method."""
        print("\n\n🔄 Testing disconnect...")
        try:
            self.connection.connect()
            result = self.connection.disconnect()
            self.assertTrue(result)
            self.assertFalse(self.connection.is_connected())
            print("✅ Disconnection successful!")
        except Exception as e:
            self.fail(f"❌ Disconnection failed with error: {str(e)}")
    
    def test_invalid_credentials(self):
        """Test connection with invalid credentials."""
        print("\n\n🔄 Testing connection with invalid credentials...")
        bad_config = self.config.copy()
        bad_config["password"] = "WrongPassword"
        bad_connection = MT5Connection(bad_config)
        
        try:
            bad_connection.connect()
            self.fail("❌ Should have raised LoginError but didn't")
        except LoginError as e:
            print(f"✅ Expected error caught: {str(e)}")
        except Exception as e:
            self.fail(f"❌ Unexpected error type: {type(e).__name__}")
        finally:
            try:
                bad_connection.disconnect()
            except:
                pass
    
    # === EDGE CASE TESTS ===
    
    def test_invalid_path(self):
        """Test connection with an invalid terminal path."""
        print("\n\n🔄 Testing connection with invalid path...")
        bad_config = self.config.copy()
        bad_config["path"] = "C:\\NonExistentPath\\terminal64.exe"
        bad_connection = MT5Connection(bad_config)
        
        try:
            bad_connection.connect()
            self.fail("❌ Should have raised InitializationError but didn't")
        except InitializationError as e:
            print(f"✅ Expected error caught: {str(e)}")
        except Exception as e:
            self.fail(f"❌ Unexpected error type: {type(e).__name__}")
    
    def test_invalid_login_format(self):
        """Test connection with invalid login format (non-integer)."""
        print("\n\n🔄 Testing connection with invalid login format...")
        bad_config = self.config.copy()
        bad_config["login"] = "not-an-integer"
        bad_connection = MT5Connection(bad_config)
        
        try:
            bad_connection.connect()
            self.fail("❌ Should have raised InitializationError but didn't")
        except InitializationError as e:
            print(f"✅ Expected error caught: {str(e)}")
            self.assertIn("Invalid login format", str(e))
        except Exception as e:
            self.fail(f"❌ Unexpected error type: {type(e).__name__}")
    
    def test_reconnection(self):
        """Test multiple connect/disconnect cycles."""
        print("\n\n🔄 Testing multiple connect/disconnect cycles...")
        cycles = 3
        
        for i in range(cycles):
            print(f"\nCycle {i+1}/{cycles}:")
            try:
                print("  Connecting...")
                self.connection.connect()
                self.assertTrue(self.connection.is_connected())
                print("  ✅ Connection successful")
                
                print("  Getting terminal info...")
                info = self.connection.get_terminal_info()
                self.assertIsNotNone(info)
                print("  ✅ Terminal info retrieved")
                
                print("  Disconnecting...")
                self.connection.disconnect()
                self.assertFalse(self.connection.is_connected())
                print("  ✅ Disconnection successful")
                
                # Small delay between cycles
                time.sleep(1)
            except Exception as e:
                self.fail(f"❌ Cycle {i+1} failed with error: {str(e)}")
        
        print(f"✅ Successfully completed {cycles} connect/disconnect cycles")
    
    def test_short_timeout(self):
        """Test connection with a very short timeout."""
        print("\n\n🔄 Testing connection with short timeout...")
        
        # Very short timeout (1ms)
        short_config = self.config.copy()
        short_config["timeout"] = 1
        short_connection = MT5Connection(short_config)
        
        try:
            short_connection.connect()
            self.fail("❌ Should have failed with timeout but didn't")
        except Exception as e:
            print(f"✅ Expected timeout-related error caught: {str(e)}")
        finally:
            try:
                short_connection.disconnect()
            except:
                pass
    
    # === STRESS TESTS ===
    
    def test_rapid_connect_disconnect(self):
        """Test rapid connect/disconnect cycles."""
        print("\n\n🔄 Testing rapid connect/disconnect cycles...")
        
        # Only do a few cycles to avoid hammering the terminal
        cycles = 5
        connection = MT5Connection(self.config)
        
        try:
            for i in range(cycles):
                print(f"Cycle {i+1}/{cycles}... ", end="")
                connection.connect()
                self.assertTrue(connection.is_connected())
                connection.disconnect()
                self.assertFalse(connection.is_connected())
                print("✅")
            
            print(f"✅ Successfully completed {cycles} rapid connect/disconnect cycles")
        except Exception as e:
            self.fail(f"❌ Rapid connect/disconnect failed: {str(e)}")
    
    # === SECURITY TESTS ===
    
    def test_no_credentials_in_errors(self):
        """Test that credentials don't appear in error messages."""
        print("\n\n🔄 Testing credential security in errors...")
        
        # Create connection with bad server to force error
        bad_server_config = self.config.copy()
        bad_server_config["server"] = "NonexistentServer"
        
        sensitive_info = [self.config["password"], str(self.config["login"])]
        
        try:
            connection = MT5Connection(bad_server_config)
            connection.connect()
            self.fail("❌ Should have raised an error but didn't")
        except Exception as e:
            error_msg = str(e)
            print(f"Error message: {error_msg}")
            
            # Check if sensitive info appears in error message
            for info in sensitive_info:
                self.assertNotIn(info, error_msg, 
                                f"❌ Sensitive info '{info}' appears in error message")
            
            print("✅ No credentials leaked in error messages")
    
    def test_connection_after_abnormal_termination(self):
        """Test connection behavior after abnormal termination."""
        print("\n\n🔄 Testing connection recovery after abnormal termination...")
        
        # First establish a normal connection
        try:
            self.connection.connect()
            self.assertTrue(self.connection.is_connected())
            print("✅ Initial connection successful")
            
            # Now simulate abnormal termination by not calling disconnect
            print("Simulating abnormal termination (skipping disconnect)...")
            self._reset_connection()
            
            # Try to connect again
            print("Attempting to reconnect...")
            self.connection.connect()
            self.assertTrue(self.connection.is_connected())
            print("✅ Reconnection after abnormal termination successful")
            
        except Exception as e:
            self.fail(f"❌ Connection recovery test failed: {str(e)}")
        finally:
            try:
                self.connection.disconnect()
            except:
                pass
    
    def _reset_connection(self):
        """Reset the connection object without calling disconnect."""
        self.connection._connected = False
        self.connection = MT5Connection(self.config)


class TestMT5ConnectionLongRunning(unittest.TestCase):
    """Long-running tests for the MT5Connection class that should be run separately."""
    
    def setUp(self):
        """Set up the test environment."""
        self.config = {
            "path": "C:\\Program Files\\MetaTrader 5\\terminal64.exe",
            "login": 240294046,
            "password": "ExnessDemo123!",
            "server": "Exness-MT5Trial6",
            "timeout": 60000,
            "portable": False
        }
    
    def test_extended_connection(self):
        """Test keeping connection open for an extended period (30 seconds)."""
        print("\n\n🔄 Testing extended connection...")
        
        connection = MT5Connection(self.config)
        try:
            # Connect
            connection.connect()
            self.assertTrue(connection.is_connected())
            print("✅ Connection established")
            
            # Keep open for 30 seconds
            duration = 30
            print(f"Keeping connection open for {duration} seconds...")
            for i in range(duration):
                time.sleep(1)
                # Every 5 seconds, check if still connected
                if (i + 1) % 5 == 0:
                    still_connected = connection.is_connected()
                    print(f"  [{i+1}s] Connection status: {'✅ Connected' if still_connected else '❌ Disconnected'}")
                    self.assertTrue(still_connected)
            
            print("✅ Connection remained stable for the test period")
            
            # Try to get terminal info to verify connection is still working
            info = connection.get_terminal_info()
            self.assertIsNotNone(info)
            print("✅ Terminal info retrieved after extended connection")
            
        except Exception as e:
            self.fail(f"❌ Extended connection test failed: {str(e)}")
        finally:
            # Clean up
            try:
                connection.disconnect()
                print("✅ Disconnection successful")
            except Exception as e:
                print(f"❌ Error during disconnection: {str(e)}")


def simple_connection_test():
    """A simple test function to test the connection outside of unittest framework."""
    print("🚀 Starting simple connection test...")
    
    # Configuration
    config = {
        "path": "C:\\Program Files\\MetaTrader 5\\terminal64.exe",
        "login": 240294046,
        "password": "ExnessDemo123!",
        "server": "Exness-MT5Trial6",
    }
    
    # Create connection
    connection = MT5Connection(config)
    
    try:
        # Try to connect
        print("🔄 Connecting to MetaTrader 5 terminal...")
        connection.connect()
        print("✅ Connection successful!")
        
        # Get terminal info
        print("\n📊 Getting terminal info...")
        info = connection.get_terminal_info()
        print("Terminal info:")
        for key, value in sorted(info.items()):
            print(f"   {key}: {value}")
        
        # Get version
        print("\n📊 Getting version...")
        version = connection.get_version()
        print(f"Terminal version: {version[0]}.{version[1]}.{version[2]}.{version[3]}")
        
        # Test is_connected
        print("\n🔍 Testing connection status...")
        if connection.is_connected():
            print("✅ Connection is active!")
        else:
            print("❌ Connection is not active!")
        
    except Exception as e:
        print(f"❌ Error: {str(e)}")
    finally:
        # Clean up
        print("\n🔄 Disconnecting...")
        try:
            connection.disconnect()
            print("✅ Disconnection successful!")
        except Exception as e:
            print(f"❌ Error during disconnection: {str(e)}")


if __name__ == "__main__":
    """Run connection tests."""
    mode = "simple"  # Default: run simple test
    
    if len(sys.argv) > 1:
        mode = sys.argv[1]  # Get mode from command line
        
    runner = unittest.TextTestRunner(verbosity=VERBOSITY)
    
    if mode == "unittest" or mode == "all":
        # Run unit tests
        print("\n🧪 Running unit tests for MT5Connection...")
        conn_suite = unittest.TestLoader().loadTestsFromTestCase(TestMT5Connection)
        runner.run(conn_suite)
    
    if mode == "extended" or mode == "all":
        # Run extended tests
        print("\n⏱️ Running extended connection tests...")
        ext_suite = unittest.TestLoader().loadTestsFromTestCase(TestMT5ConnectionLongRunning)
        runner.run(ext_suite)
    
    if mode == "simple" or mode == "all":
        # Run simple test
        print("\n🔄 Running simple connection test...")
        simple_connection_test()
