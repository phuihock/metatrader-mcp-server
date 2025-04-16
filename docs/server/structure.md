# MCP Server Project Structure

```
/src/mcp_server/
├── __init__.py
├── main.py                     # FastMCP server instance & main entry point
├── core/                       # Core config, security, logging (as needed)
│   ├── __init__.py
│   ├── config.py
│   └── logging_config.py  
├── logic/                      # Business logic & models
│   ├── __init__.py
│   ├── models.py               # Pydantic models (as needed)
│   └── errors.py               # Error handling
└── tools/                      # MCP tool implementations
    ├── __init__.py
    └── metatrader_tools.py     # MetaTrader-specific tools
```