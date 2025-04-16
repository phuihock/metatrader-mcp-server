from typing import Dict, Any, List, Optional
from datetime import datetime, timedelta
import logging

try:
    import MetaTrader5 as mt5
except ImportError:
    raise ImportError("MetaTrader5 package is not installed. Please install it with: pip install MetaTrader5")

from ..exceptions import OrdersHistoryError, ConnectionError

logger = logging.getLogger("MT5History")

def get_orders(
    connection,
    from_date: Optional[datetime] = None,
    to_date: Optional[datetime] = None,
    group: Optional[str] = None,
    ticket: Optional[int] = None
) -> List[Dict[str, Any]]:
    """
    Get historical orders.
    """
    if not connection.is_connected():
        raise ConnectionError("Not connected to MetaTrader 5 terminal.")
    orders = None
    logger.debug(f"Retrieving orders with parameters: from_date={from_date}, to_date={to_date}, group={group}, ticket={ticket}")
    try:
        if ticket is not None:
            logger.debug(f"Retrieving orders by ticket: {ticket}")
            orders = mt5.history_orders_get(ticket=ticket)
        else:
            if from_date is None:
                from_date = datetime.now() - timedelta(days=30)
            if to_date is None:
                to_date = datetime.now()
            logger.debug(f"Retrieving orders by date range: {from_date} to {to_date}")
            if group is not None:
                orders = mt5.history_orders_get(from_date, to_date, group=group)
            else:
                orders = mt5.history_orders_get(from_date, to_date)
    except Exception as e:
        error_code = -1
        if hasattr(mt5, 'last_error'):
            error = mt5.last_error()
            if error and len(error) > 1:
                error_code = error[0]
        msg = f"Failed to retrieve orders history: {str(e)}"
        logger.error(msg)
        raise OrdersHistoryError(msg, error_code)
    if orders is None:
        error = mt5.last_error()
        msg = f"Failed to retrieve orders history: {error[1]}"
        logger.error(msg)
        raise OrdersHistoryError(msg, error[0])
    if len(orders) == 0:
        logger.info("No orders found with the specified parameters.")
        return []
    result = [order._asdict() for order in orders]
    logger.debug(f"Retrieved {len(result)} orders.")
    return result
