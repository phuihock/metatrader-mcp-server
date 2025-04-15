from typing import Union
from pandas import DataFrame
from .get_positions import get_positions

def get_positions_by_id(connection, id: Union[int, str]) -> DataFrame:
	return get_positions(connection, ticket=id)