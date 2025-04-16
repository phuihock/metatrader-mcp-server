from typing import Optional
import pandas as pd
from datetime import datetime, timezone, timedelta
import MetaTrader5 as mt5
from ..types import Timeframe
from ..exceptions import SymbolNotFoundError, InvalidTimeframeError, MarketDataError
from .get_symbols import get_symbols

def get_candles_by_date(
    connection,
    symbol_name: str,
    timeframe: str,
    from_date: Optional[str] = None,
    to_date: Optional[str] = None,
) -> pd.DataFrame:
    if not get_symbols(connection, symbol_name):
        raise SymbolNotFoundError(f"Symbol '{symbol_name}' not found")
    tf = Timeframe.get(timeframe)
    if tf is None:
        raise InvalidTimeframeError(f"Invalid timeframe: '{timeframe}'")
    from_datetime = None
    to_datetime = None
    if from_date:
        try:
            from_datetime = datetime.strptime(from_date, "%Y-%m-%d %H:%M").replace(tzinfo=timezone.utc)
        except ValueError:
            raise ValueError(f"Invalid from_date format: {from_date}. Expected format: 'yyyy-MM-dd HH:mm'")
    if to_date:
        try:
            to_datetime = datetime.strptime(to_date, "%Y-%m-%d %H:%M").replace(tzinfo=timezone.utc)
        except ValueError:
            raise ValueError(f"Invalid to_date format: {to_date}. Expected format: 'yyyy-MM-dd HH:mm'")
    if from_datetime and to_datetime and from_datetime > to_datetime:
        from_datetime, to_datetime = to_datetime, from_datetime
    candles = None
    if from_datetime and to_datetime:
        candles = mt5.copy_rates_range(symbol_name, tf, from_datetime, to_datetime)
    elif from_datetime:
        candles = mt5.copy_rates_from(symbol_name, tf, from_datetime, 1000)
    elif to_datetime:
        lookback_days = 30
        start_date = to_datetime - timedelta(days=lookback_days)
        candles = mt5.copy_rates_range(symbol_name, tf, start_date, to_datetime)
    else:
        candles = mt5.copy_rates_from_pos(symbol_name, tf, 0, 1000)
    if candles is None or len(candles) == 0:
        raise MarketDataError(f"Failed to retrieve historical data for symbol '{symbol_name}' with timeframe '{timeframe}'")
    df = pd.DataFrame(candles)
    df['time'] = pd.to_datetime(df['time'], unit='s', utc=True)
    df = df.sort_values('time', ascending=False)
    return df
