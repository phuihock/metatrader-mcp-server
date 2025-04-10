"""
MetaTrader 5 account operations module.

This module handles account information retrieval and management.
"""
from typing import Dict, Any, Optional
from .exceptions import AccountError


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
            AccountError: If account information cannot be retrieved.
            ConnectionError: If not connected to terminal.
        """
        pass
    
    def get_balance(self) -> float:
        """
        Get current account balance.
        
        Balance is the amount of money in the account without considering
        open positions.
        
        Returns:
            float: Current account balance.
            
        Raises:
            AccountError: If balance cannot be retrieved.
            ConnectionError: If not connected to terminal.
        """
        pass
    
    def get_equity(self) -> float:
        """
        Get current account equity.
        
        Equity is the balance plus floating profit/loss from open positions.
        
        Returns:
            float: Current account equity.
            
        Raises:
            AccountError: If equity cannot be retrieved.
            ConnectionError: If not connected to terminal.
        """
        pass
    
    def get_margin(self) -> float:
        """
        Get current used margin.
        
        Margin is the amount of money reserved as a deposit to maintain
        open positions.
        
        Returns:
            float: Current used margin.
            
        Raises:
            AccountError: If margin cannot be retrieved.
            ConnectionError: If not connected to terminal.
        """
        pass
    
    def get_free_margin(self) -> float:
        """
        Get current free margin.
        
        Free margin is the amount of money available for opening new positions.
        
        Returns:
            float: Current free margin.
            
        Raises:
            AccountError: If free margin cannot be retrieved.
            ConnectionError: If not connected to terminal.
        """
        pass
    
    def get_margin_level(self) -> float:
        """
        Get current margin level.
        
        Margin level is calculated as (Equity / Margin) * 100%.
        
        Returns:
            float: Current margin level in percentage.
            
        Raises:
            AccountError: If margin level cannot be retrieved.
            ConnectionError: If not connected to terminal.
        """
        pass
    
    def get_currency(self) -> str:
        """
        Get account currency.
        
        Returns:
            str: Account currency (e.g., "USD", "EUR").
            
        Raises:
            AccountError: If currency cannot be retrieved.
            ConnectionError: If not connected to terminal.
        """
        pass
    
    def is_trade_allowed(self) -> bool:
        """
        Check if trading is allowed for this account.
        
        Returns:
            bool: True if trading is allowed, False otherwise.
            
        Raises:
            AccountError: If trading permission cannot be determined.
            ConnectionError: If not connected to terminal.
        """
        pass
