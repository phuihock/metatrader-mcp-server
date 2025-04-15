from pandas import DataFrame
from .get_positions import get_positions

def get_positions_by_symbol(connection, symbol: str) -> DataFrame:
	return get_positions(connection, symbol_name=symbol)