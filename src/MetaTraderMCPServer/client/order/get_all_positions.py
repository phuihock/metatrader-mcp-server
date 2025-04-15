from pandas import DataFrame
from .get_positions import get_positions

def get_all_positions(connection) -> DataFrame:
	return get_positions(connection)