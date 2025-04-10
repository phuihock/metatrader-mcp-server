# MetaTrader MCP Server Project Structure

## Directory Overview

```
metatrader-mcp-server/
│
├── pyproject.toml           # Project configuration and build settings
│
├── src/
│   └── MetaTraderMCPServer/
│       ├── __init__.py      # Package initialization
│       ├── __main__.py      # Entry point for the package
│       ├── greetings.py     # Potential greeting/utility module
│       │
│       ├── client/          # Client-side modules for MetaTrader interactions
│       │   └── (various client-related Python files)
│       │
│       └── server/          # Server-side modules
│
├── tests/                   # Unit and integration tests
│
├── docs/                    # Project documentation
│
└── references/              # Additional reference materials
```

## Project Purpose
A Model Context Protocol (MCP) server for AI LLMs to trade using the MetaTrader platform.

## Current Development Status
- Work in progress (Road to v1)
- Focus: Developing MetaTrader client module and MCP tools

## Key Components
- `client/`: Handles MetaTrader client interactions
- `server/`: Will handle the MCP server logic
- `tests/`: Ensures code quality and functionality

## Planned Features (from README)
- Account information retrieval
- Market symbol operations
- Trade execution and management
- Historical data retrieval

## Development Stage
- Connect to MetaTrader 5 terminal: ✅ Finished
- Client module development: In Progress (3/7 complete)
- Other features: Planned
