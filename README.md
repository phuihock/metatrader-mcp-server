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
