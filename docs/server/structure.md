# MCP Server Project Structure

```
/src/mcp/
├── __init__.py
├── main.py                     # FastAPI app instance & main entry point
├── api/                        # FastAPI routers and dependencies
│   ├── __init__.py
│   ├── endpoints.py            # Combined API endpoints for /mcp (POST) and /events (GET SSE)
│   └── deps.py                 # Dependencies (e.g., security, getting managers)
├── core/                       # Core logic (config, security, logging)
│   ├── __init__.py
│   ├── config.py
│   ├── security.py
│   └── logging_config.py
├── logic/                      # Core MCP logic handlers
│   ├── __init__.py
│   ├── tool_registry.py
│   ├── resource_manager.py
│   ├── connection_manager.py   # For SSE
│   ├── models.py               # Pydantic models
│   └── errors.py
├── tools/                      # Tool implementations
│   ├── __init__.py
│   └── metatrader_tools.py     # Example tool specific to your domain
└── transports/                 # Handlers for specific transport details
    ├── __init__.py
    ├── http_handler.py
    └── sse_handler.py
```