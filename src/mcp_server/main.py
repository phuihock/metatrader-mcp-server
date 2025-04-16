import random
from contextlib import asynccontextmanager
from mcp.server.fastmcp import FastMCP
from mcp_server.core.config import settings
from mcp_server.core.logging_config import setup_logging, mcp_logger, tools_logger, mt5_logger
from mcp_server.logic import mt5_connection

# Setup logging first
setup_logging()

# Define Lifespan Context Manager
@asynccontextmanager
async def lifespan(app: FastMCP):
    # Startup: Initialize MT5 connection
    mcp_logger.info("Server starting up - initializing MT5 connection...")
    mt5_available = mt5_connection.initialize_mt5_client()
    if not mt5_available:
        if settings.ENABLE_DEMO_TOOLS:
            mcp_logger.warning("MetaTrader connection not available - will use demo tools")
        else:
            # Handle critical failure if needed
            mcp_logger.error("MetaTrader connection not available and demo tools disabled.")
            # You might want to raise an exception here if MT5 is critical
            # raise RuntimeError("MT5 connection failed and is required.")
    else:
        mcp_logger.info("MT5 connection initialized successfully.")
    # You could store status in app state if needed: app.state.mt5_available = mt5_available
    
    yield # Application runs here
    
    # Shutdown: Disconnect from MT5
    mt5_logger.info("Server shutting down - disconnecting from MT5")
    mt5_connection.disconnect()
    mcp_logger.info("Server shutdown complete.")

# Initialize the FastMCP server with lifespan manager
mcp = FastMCP(name=settings.SERVER_NAME, lifespan=lifespan) # Pass lifespan here
mcp_logger.info(f"Initialized FastMCP server: {settings.SERVER_NAME}")

# Register account tools
@mcp.tool()
def get_balance() -> float:
    """Get user's account balance."""
    tools_logger.debug("get_balance tool called")
    
    # Try to get real balance from MT5 if available
    if mt5_connection.get_mt5_client() and settings.ENABLE_TRADING_TOOLS:
        client = mt5_connection.get_mt5_client()
        if client:
            try:
                balance = client.account.get_balance()
                tools_logger.info(f"Retrieved actual balance: {balance}")
                return balance
            except Exception as e:
                tools_logger.error(f"Error getting balance: {str(e)}")
    
    # Fallback to demo data
    if settings.ENABLE_DEMO_TOOLS:
        demo_balance = random.randint(100_000, 400_000)
        tools_logger.debug(f"Using demo balance: {demo_balance}")
        return float(demo_balance)
    else:
        tools_logger.warning("Neither MT5 nor demo tools available")
        return 0.0

@mcp.tool()
def get_account_info() -> dict:
    """Get detailed information about the trading account."""
    tools_logger.debug("get_account_info tool called")
    
    # Try to get real info from MT5 if available
    if mt5_connection.get_mt5_client() and settings.ENABLE_TRADING_TOOLS:
        client = mt5_connection.get_mt5_client()
        if client:
            try:
                info = client.account.get_account_info()
                return dict(info._asdict()) if info else {}
            except Exception as e:
                tools_logger.error(f"Error getting account info: {str(e)}")
    
    # Fallback to demo data
    if settings.ENABLE_DEMO_TOOLS:
        return {
            "balance": random.randint(100_000, 400_000),
            "equity": random.randint(100_000, 400_000),
            "margin": random.randint(1000, 10000),
            "margin_level": random.uniform(100, 1000),
            "leverage": 100,
            "currency": "USD"
        }
    else:
        return {}

# This exports the mcp instance for the mcp dev cli tool to use
app = mcp

# Entry point if you want to run directly with uvicorn
if __name__ == "__main__":
    import uvicorn
    mcp_logger.info("Starting server with uvicorn")
    uvicorn.run("src.mcp.main:app", host="0.0.0.0", port=8000)
