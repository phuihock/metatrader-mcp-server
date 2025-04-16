"""
MetaTrader 5 account operations module.

This module handles account information retrieval and management.
"""
from typing import Dict, Any, Optional
import logging

try:
    import MetaTrader5 as mt5
except ImportError:
    raise ImportError("MetaTrader5 package is not installed. Please install it with: pip install MetaTrader5")

from .exceptions import AccountError, AccountInfoError, TradingNotAllowedError, MarginLevelError, ConnectionError

# Set up logger
logger = logging.getLogger("MT5Account")


class MT5Account:
    """
    Handles MetaTrader 5 account operations.
    
    Provides methods to retrieve account information and status.
    """
    
    def __init__(self, connection):
        """
        Initialize the account operations handler.
        
        Args:
            connection: MT5Connection instance for terminal communication.
        """
        self._connection = connection
        
        # Set up logging level based on connection's debug setting
        if getattr(self._connection, 'debug', False):
            logger.setLevel(logging.DEBUG)
        else:
            logger.setLevel(logging.INFO)
    
    def get_account_info(self) -> Dict[str, Any]:
        """
        Get comprehensive account information.
        
        Returns a dictionary with all account properties including:
        - login: Account number
        - trade_mode: Account trade mode (0-real, 1-demo, 2-contest)
        - leverage: Account leverage
        - balance: Account balance in deposit currency
        - credit: Credit in deposit currency
        - profit: Current profit in deposit currency
        - equity: Equity in deposit currency
        - margin: Margin used in deposit currency
        - margin_free: Free margin in deposit currency
        - margin_level: Margin level as percentage
        - margin_so_call: Margin call level
        - margin_so_so: Margin stop out level
        - currency: Account currency
        - name: Client name
        - server: Trade server name
        - company: Name of company serving the account
        
        Returns:
            Dict[str, Any]: Account information including balance, equity, margin, etc.
            
        Raises:
            AccountInfoError: If account information cannot be retrieved.
            ConnectionError: If not connected to terminal.
        """
        # Check if connected to MT5
        if not self._connection.is_connected():
            raise ConnectionError("Not connected to MetaTrader 5 terminal.")
        
        logger.debug("Retrieving account information...")
        
        # Get account info
        account_info = mt5.account_info()
        
        # Check if retrieval was successful
        if account_info is None:
            error = mt5.last_error()
            msg = f"Failed to retrieve account information: {error[1]}"
            logger.error(msg)
            raise AccountInfoError(msg, error[0])
        
        # Convert named tuple to dictionary
        return account_info._asdict()
    
    def get_balance(self) -> float:
        """
        Get current account balance.
        
        Balance is the amount of money in the account without considering
        open positions.
        
        Returns:
            float: Current account balance.
            
        Raises:
            AccountInfoError: If balance cannot be retrieved.
            ConnectionError: If not connected to terminal.
        """
        account_info = self.get_account_info()
        return account_info["balance"]
    
    def get_equity(self) -> float:
        """
        Get current account equity.
        
        Equity is the balance plus floating profit/loss from open positions.
        
        Returns:
            float: Current account equity.
            
        Raises:
            AccountInfoError: If equity cannot be retrieved.
            ConnectionError: If not connected to terminal.
        """
        account_info = self.get_account_info()
        return account_info["equity"]
    
    def get_margin(self) -> float:
        """
        Get current used margin.
        
        Margin is the amount of money reserved as a deposit to maintain
        open positions.
        
        Returns:
            float: Current used margin.
            
        Raises:
            AccountInfoError: If margin cannot be retrieved.
            ConnectionError: If not connected to terminal.
        """
        account_info = self.get_account_info()
        return account_info["margin"]
    
    def get_free_margin(self) -> float:
        """
        Get current free margin.
        
        Free margin is the amount of money available for opening new positions.
        
        Returns:
            float: Current free margin.
            
        Raises:
            AccountInfoError: If free margin cannot be retrieved.
            ConnectionError: If not connected to terminal.
        """
        account_info = self.get_account_info()
        return account_info["margin_free"]
    
    def get_margin_level(self) -> float:
        """
        Get current margin level.
        
        Margin level is calculated as (Equity / Margin) * 100%.
        
        Returns:
            float: Current margin level in percentage.
            
        Raises:
            AccountInfoError: If margin level cannot be retrieved.
            ConnectionError: If not connected to terminal.
        """
        account_info = self.get_account_info()
        return account_info["margin_level"]
    
    def get_currency(self) -> str:
        """
        Get account currency.
        
        Returns:
            str: Account currency (e.g., "USD", "EUR").
            
        Raises:
            AccountInfoError: If currency cannot be retrieved.
            ConnectionError: If not connected to terminal.
        """
        account_info = self.get_account_info()
        return account_info["currency"]
    
    def get_leverage(self) -> int:
        """
        Get account leverage.
        
        Returns:
            int: Account leverage (e.g., 100 for 1:100 leverage).
            
        Raises:
            AccountInfoError: If leverage cannot be retrieved.
            ConnectionError: If not connected to terminal.
        """
        account_info = self.get_account_info()
        return account_info["leverage"]
    
    def get_account_type(self) -> str:
        """
        Get account type (real, demo, or contest).
        
        Returns:
            str: Account type ("real", "demo", or "contest").
            
        Raises:
            AccountInfoError: If account type cannot be retrieved.
            ConnectionError: If not connected to terminal.
        """
        account_info = self.get_account_info()
        trade_mode = account_info["trade_mode"]
        
        if trade_mode == 0:
            return "real"
        elif trade_mode == 1:
            return "demo"
        elif trade_mode == 2:
            return "contest"
        else:
            return f"unknown ({trade_mode})"
    
    def is_trade_allowed(self) -> bool:
        """
        Check if trading is allowed for this account.
        
        Returns:
            bool: True if trading is allowed, False otherwise.
            
        Raises:
            AccountInfoError: If trading permission cannot be determined.
            ConnectionError: If not connected to terminal.
        """
        # Check if connected to MT5
        if not self._connection.is_connected():
            raise ConnectionError("Not connected to MetaTrader 5 terminal.")
        
        logger.debug("Checking if trading is allowed...")
        
        # Check trade allowed status using MT5 function
        trade_allowed = mt5.terminal_info().trade_allowed
        
        logger.debug(f"Trading allowed: {trade_allowed}")
        
        return bool(trade_allowed)
    
    def check_margin_level(self, min_level: float = 100.0) -> bool:
        """
        Check if margin level is above the specified minimum level.
        
        Args:
            min_level: Minimum margin level in percentage (default: 100.0).
        
        Returns:
            bool: True if margin level is above the minimum, False otherwise.
            
        Raises:
            MarginLevelError: If margin level is below the minimum.
            AccountInfoError: If margin level cannot be retrieved.
            ConnectionError: If not connected to terminal.
        """
        margin_level = self.get_margin_level()
        
        if margin_level < min_level:
            msg = f"Margin level too low: {margin_level}% (minimum: {min_level}%)"
            logger.warning(msg)
            raise MarginLevelError(msg)
        
        return True
    
    def get_trade_statistics(self) -> Dict[str, Any]:
        """
        Get basic trade statistics for the account.
        
        Returns:
            Dict[str, Any]: Dictionary with trade statistics:
                - balance: Current balance
                - equity: Current equity
                - profit: Current floating profit/loss
                - margin_level: Current margin level
                - free_margin: Available margin for trading
                - account_type: Account type (real, demo, contest)
                - leverage: Account leverage
                - currency: Account currency
                
        Raises:
            AccountInfoError: If statistics cannot be retrieved.
            ConnectionError: If not connected to terminal.
        """
        account_info = self.get_account_info()
        
        # Create trade statistics dictionary
        stats = {
            "balance": account_info["balance"],
            "equity": account_info["equity"],
            "profit": account_info["profit"],
            "margin_level": account_info["margin_level"],
            "free_margin": account_info["margin_free"],
            "account_type": self.get_account_type(),
            "leverage": account_info["leverage"],
            "currency": account_info["currency"],
        }
        
        return stats
