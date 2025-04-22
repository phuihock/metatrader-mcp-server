# MetaTrader MCP Server

This is a Model Context Protocol (MCP) server built with Python to enable AI LLMs to trade using MetaTrader platform.

![MetaTrader MCP Server](https://yvkbpmmzjmfqjxusmyop.supabase.co/storage/v1/object/public/github//metatrader-mcp-server-1.png)

## Updates

- April 16, 2025: We have our first minor version release (0.1.0) 🎉🎉🎉

## Project Roadmap

For full version checklist, see [version-checklist.md](docs/roadmap/version-checklist.md).

| Task | Status | Done | Tested |
|------|--------|------|--------|
| Connect to MetaTrader 5 terminal | Finished | ✅ | ✅ |
| Develop MetaTrader client module | Finished | ✅ | ✅ |
| Develop MCP Server module | Done | ✅ | ✅ |
| Implement MCP tools | On progress... | - | - |
| Publish to PyPi | - | - | - |
| Claude Desktop integration | - | - | - |
| Open WebUI integration | - | - | - |

### MCP Tools Test Result (2025-04-22):

1. ✅ `get_account_info`
2. ❌ `get_deals` (Fixed)
3. ❌ `get_orders` (Fixed)
4. ✅ `get_candles_latest`
5. ✅ `get_symbol_price`
6. ✅ `get_all_symbols`
7. ✅ `get_symbols`
8. ✅ `get_all_positions`
9. ✅ `get_positions_by_symbol`
10. ❌ `get_positions_by_id` (Fixed)
11. ✅ `get_all_pending_orders`
12. ✅ `get_pending_orders_by_symbol`
13. ❌ `get_pending_orders_by_id` (Fixed)
14. ✅ `place_market_order`
15. ✅ `place_pending_order`
16. ❌ `modify_position` (Fixed)
17. ❌ `modify_pending_order`
18. ❌ `close_position`
19. ❌ `cancel_pending_order`
20. ✅ `close_all_positions`
21. ✅ `close_all_positions_by_symbol`
22. ✅ `close_all_profittable_positions`
23. ✅ `close_all_losing_positions`
24. ✅ `cancel_all_pending_orders`
25. ✅ `cancel_pending_orders_by_symbol`

Result **68%** (17 success & 8 failed).

## Documentation

For developers, see [Developer's Documentation](docs/README.md).

## Development Instructions

### Creating Virtual Environment

```
uv venv
```

Then, you need to enable the environment in the Terminal.

Linux or macOS:
```
source .venv/bin/activate
```

Windows (PowerShell):
```
.venv\Scripts\Activate.ps1
```

### Installing Package

```
uv pip install -e .
```

### Building Package

```
python -m build
```

The build result will be in `dist/` folder.

### Testing

To run the test suite and generate a comprehensive Markdown report:

```bash
pytest -s tests
```

Test reports will be saved in `tests/reports/` with a timestamped filename.

### Publishing to Test PyPI

```
twine upload --repository-url https://test.pypi.org/legacy/ dist/*
```

Enter credentials when required.
