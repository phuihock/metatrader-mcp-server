from fastapi import APIRouter, HTTPException, Request

router = APIRouter()

@router.get("/info", response_model=dict)
async def account_info(request: Request):
    """Fetch account information via MCP tool."""
    client = request.app.state.client
    try:
        return client.account.get_trade_statistics()
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
