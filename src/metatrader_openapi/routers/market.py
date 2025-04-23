from fastapi import APIRouter, HTTPException, Request, Query
from typing import List, Dict, Any, Optional
# Removed unused import of pandas (pd)
from metatrader_client.exceptions import ConnectionError as MT5ConnectionError

router = APIRouter()

@router.get("/candles/latest", response_model=List[Dict[str, Any]])
async def candles_latest(
    request: Request,
    symbol_name: str = Query(..., description="Symbol name, e.g., 'EURUSD'"),
    timeframe: str = Query(..., description="Timeframe, e.g., 'M1', 'H1'"),
    count: int = Query(100, description="Number of candles to retrieve")
):
    """Get latest candles as a list of records."""
    client = request.app.state.client
    try:
        df = client.market.get_candles_latest(symbol_name=symbol_name, timeframe=timeframe, count=count)
        return df.to_dict(orient="records")
    except MT5ConnectionError as e:
        raise HTTPException(status_code=503, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/price/{symbol_name}", response_model=Dict[str, Any])
async def symbol_price(
    request: Request,
    symbol_name: str
):
    """Get latest symbol price info."""
    client = request.app.state.client
    try:
        return client.market.get_symbol_price(symbol_name=symbol_name)
    except MT5ConnectionError as e:
        raise HTTPException(status_code=503, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/symbols", response_model=List[str])
async def all_symbols(request: Request):
    """Get a list of all market symbols."""
    client = request.app.state.client
    try:
        return client.market.get_symbols()
    except MT5ConnectionError as e:
        raise HTTPException(status_code=503, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/symbols/filter", response_model=List[str])
async def filter_symbols(
    request: Request,
    group: Optional[str] = Query(None, description="Filter pattern, e.g., '*USD*'")
):
    """Get symbols filtered by group pattern."""
    client = request.app.state.client
    try:
        return client.market.get_symbols(group=group)
    except MT5ConnectionError as e:
        raise HTTPException(status_code=503, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
