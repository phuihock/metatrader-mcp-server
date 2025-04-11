#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Utility functions for MetaTrader MCP Server.

This module provides helper functions for common operations.
"""

import pandas as pd
import pytz
from datetime import datetime
from typing import List, Dict, Any, Optional, Union, Tuple


def convert_positions_to_dataframe(
    positions: Any,
    columns_mapping: Optional[Dict[str, str]] = None,
    sort_by: Optional[str] = "time",
    ascending: bool = False,
    enhance_order_types: bool = True
) -> pd.DataFrame:
    """
    Convert MetaTrader5 positions to a pandas DataFrame with selected fields.
    
    Args:
        positions: MetaTrader5 positions (tuple of named tuples)
        columns_mapping: Dictionary mapping original column names to new names
                        Default mapping handles common position fields
        sort_by: Column name to sort by (after renaming)
        ascending: Sort order (True for ascending, False for descending)
        enhance_order_types: Whether to convert numeric order types to human-readable strings
        
    Returns:
        pd.DataFrame: DataFrame with selected and renamed columns
    """
    # Return empty DataFrame if positions is None or empty
    if positions is None or len(positions) == 0:
        # Create empty DataFrame with expected columns
        default_columns = ['id', 'time', 'symbol', 'type', 'volume', 
                          'open', 'stop_loss', 'take_profit', 'profit']
        return pd.DataFrame(columns=default_columns)
    
    # Default columns mapping if not provided
    if columns_mapping is None:
        columns_mapping = {
            'ticket': 'id',
            'time': 'time',
            'symbol': 'symbol',
            'type': 'type',
            'volume': 'volume',
            'price_open': 'open',
            'sl': 'stop_loss',
            'tp': 'take_profit',
            'profit': 'profit'
        }
    
    # Convert named tuples to list of dictionaries
    positions_list = [position._asdict() for position in positions]
    
    # Create DataFrame from positions list
    df = pd.DataFrame(positions_list)
    
    # If DataFrame is empty, return empty DataFrame with expected columns
    if df.empty:
        return pd.DataFrame(columns=list(columns_mapping.values()))
    
    # Create a new DataFrame with only available columns
    result = pd.DataFrame()
    
    # Check each column and add it if available
    for original_col, new_col in columns_mapping.items():
        if original_col in df.columns:
            result[new_col] = df[original_col]
        else:
            # Add empty column for missing data
            result[new_col] = None
    
    # Convert time from MT5 time integer to DataFrame suitable time format
    if 'time' in result.columns and result['time'].notna().any():
        # Convert to datetime from Unix timestamp (seconds)
        result['time'] = pd.to_datetime(result['time'], unit='s')
        
        # Convert from UTC to local timezone
        # Get the local timezone
        local_tz = datetime.now().astimezone().tzinfo
        
        # Convert UTC time to local timezone
        result['time'] = result['time'].dt.tz_localize('UTC').dt.tz_convert(local_tz)
    
    # Sort the DataFrame if sort_by is provided
    if sort_by is not None and sort_by in result.columns:
        result = result.sort_values(by=sort_by, ascending=ascending)
    
    # Enhance order types if requested
    if enhance_order_types and 'type' in result.columns and not result.empty:
        result = enhance_dataframe_order_types(result)
    
    return result


def enhance_dataframe_order_types(
    df: pd.DataFrame,
    type_column: str = 'type',
    preserve_original: bool = True,
    original_column: str = 'type_code'
) -> pd.DataFrame:
    """
    Enhance a DataFrame by converting numeric order type codes to human-readable strings.
    
    Args:
        df: DataFrame containing order type codes
        type_column: Name of the column containing order type codes
        preserve_original: Whether to preserve the original numeric codes
        original_column: Name of the column to store original numeric codes if preserved
        
    Returns:
        pd.DataFrame: Enhanced DataFrame with human-readable order types
    """
    from .types import OrderType
    
    # Return original DataFrame if it's empty or doesn't have the type column
    if df.empty or type_column not in df.columns:
        return df
    
    # Create a copy to avoid modifying the original DataFrame
    result = df.copy()
    
    # Store original values if requested
    if preserve_original:
        result[original_column] = result[type_column]
    
    # Convert numeric codes to human-readable strings using our enhanced OrderType Enum
    result[type_column] = result[type_column].map(
        lambda x: OrderType.to_string(x) if pd.notna(x) else x
    )
    
    return result
