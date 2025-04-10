# MetaTrader MCP Server

This is a Model Context Protocol (MCP) server built with Python to enable AI LLMs to trade using MetaTrader platform.

## Road to v1

### MCP Tools List

| Function | Description | Implemented | Tested |
|----------|-------------|-------------|--------|
| `account_info()` | Get account information such as balance, equity, margin, etc | - | - |
| `market_symbol_list()` | Get list of available market symbols | - | - |
| `market_symbol_info()` | Get information about a specific market symbol | - | - |
| `market_symbol_price()` | Get current price of a market symbol | - | - |
| `market_symbol_history()` | Get historical price data of a market symbol | - | - |
| `trade_execute()` | Execute a buy or sell trade order | - | - |
| `trade_pending()` | Create a pending trade order (limit or stop) | - | - |
| `trade_modify()` | Modify an existing trade order | - | - |
| `trade_close()` | Close an existing trade order | - | - |
| `trade_list()` | Get list of all open trade orders | - | - |
| `history_deals()` | Get list of all executed deals | - | - |
| `history_orders()` | Get list of all executed orders | - | - |
| `history_statistics()` | Get statistics of executed orders | - | - |

### Backlog

| Task | Status | Done | Tested |
|------|--------|------|--------|
| Connect to MetaTrader 5 terminal | - | - | - |
| Develop MetaTrader client module | - | - | - |
| Develop MCP Server module | - | - | - |
| Implement MCP tools | - | - | - |
| Windsurf integration | - | - | - |
| Claude Desktop integration | - | - | - |
| Publish to PyPi | - | - | - |

## Development Instructions

### Installing Package

```
pip install -e .
```

### Building Package

```
python -m build
```

The build result will be in `dist/` folder.

### Publishing to Test PyPI

```
twine upload --repository-url https://test.pypi.org/legacy/ dist/*
```

Enter credentials when required.