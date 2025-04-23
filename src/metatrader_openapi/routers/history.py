from fastapi import APIRouter, HTTPException, Request, Query
from typing import List, Dict, Any, Optional
from datetime import datetime

router = APIRouter()

@router.get("/deals", response_model=List[Dict[str, Any]])
async def history_deals(
    request: Request,
    from_date: Optional[datetime] = Query(None, description="Start date (ISO format)"),
    to_date: Optional[datetime] = Query(None, description="End date (ISO format)"),
    symbol: Optional[str] = Query(None, description="Symbol filter, e.g., 'EURUSD'")
):
    """Get historical deals via MCP tool."""
    client = request.app.state.client
    try:
        df = client.history.get_deals_as_dataframe(from_date=from_date, to_date=to_date, group=symbol)
        return df.to_dict(orient='records')
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/orders", response_model=List[Dict[str, Any]])
async def history_orders(
    request: Request,
    from_date: Optional[datetime] = Query(None, description="Start date (ISO format)"),
    to_date: Optional[datetime] = Query(None, description="End date (ISO format)"),
    symbol: Optional[str] = Query(None, description="Symbol filter, e.g., 'EURUSD'")
):
    """Get historical orders via MCP tool."""
    client = request.app.state.client
    try:
        df = client.history.get_orders_as_dataframe(from_date=from_date, to_date=to_date, group=symbol)
        return df.to_dict(orient='records')
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
