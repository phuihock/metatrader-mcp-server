from fastapi import FastAPI
from mcp.core.config import settings
from mcp.core.logging_config import setup_logging

setup_logging()
app = FastAPI(title="MetaTrader MCP Server")

@app.get("/health")
def health_check():
    return {"status": "ok"}
