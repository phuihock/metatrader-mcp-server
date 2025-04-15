# MetaTrader MCP Server

This is a Model Context Protocol (MCP) server built with Python to enable AI LLMs to trade using MetaTrader platform.

## Road to v1

For full version checklist, see [version-checklist.md](roadmap/version-checklist.md).

| Task | Status | Done | Tested |
|------|--------|------|--------|
| Connect to MetaTrader 5 terminal | Finished | ✅ | ✅ |
| Develop MetaTrader client module | Finished | ✅ | - |
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