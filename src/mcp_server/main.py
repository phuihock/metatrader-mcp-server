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
def account__get_balance():
	"""Get the current account balance."""
	client = mt5_connection.get_mt5_client()
	if client is None:
		return "No MetaTrader 5 connection available"

	return client.account.get_balance()

# This exports the mcp instance for the mcp dev cli tool to use
app = mcp

# Entry point if you want to run directly with uvicorn
if __name__ == "__main__":
	import uvicorn
	mcp_logger.info("Starting server with uvicorn")
	uvicorn.run("src.mcp.main:app", host="0.0.0.0", port=8000)
