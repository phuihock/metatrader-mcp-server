from pandas import DataFrame
from .get_positions import get_positions

def get_positions_by_currency(connection, currency: str) -> DataFrame:
	currency_filter = f"*{currency}*"
	return get_positions(connection, group=currency_filter)