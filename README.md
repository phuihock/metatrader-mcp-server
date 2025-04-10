# MetaTrader MCP Server

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