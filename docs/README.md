# MetaTrader MCP Server Documentation 📚

Welcome to the MetaTrader MCP Server documentation! This guide will help you understand how to use our library to connect AI Large Language Models (LLMs) with MetaTrader 5 for automated trading.

## Project Overview 🌟

MetaTrader MCP Server implements a Model Context Protocol (MCP) server that enables AI LLMs to interact with and trade using the MetaTrader platform. The project bridges the gap between advanced AI models and the powerful trading capabilities of MetaTrader 5.

## Module Structure 🏗️

The project is organized into two main modules:

### Client Module 🖥️

The client module handles all communication with the MetaTrader 5 terminal:

- [**Connection**](client/connection.md) - Establish and manage connections to the MetaTrader 5 terminal
- [**Account**](client/account.md) - Access account information and trading status
- **Market** (Coming Soon) - Retrieve market data and symbol information
- **Orders** (Coming Soon) - Execute trades and manage orders
- [**History**](client/history.md) - Access historical trade data and statistics

### Server Module 🌐

The server module implements the Model Context Protocol interface:

- **MCP Server** (Coming Soon) - Implements the MCP protocol for AI model communication
- **Tools** (Coming Soon) - Implements MCP tools for trading operations
- **Security** (Coming Soon) - Authentication and authorization for the MCP server

## Quick Start Guide 🚀

```python
from metatrader_client.connection import MT5Connection

# Set up configuration
config = {
    "login": 12345678,
    "password": "your-password",
    "server": "Your-Broker-Server"
}

# Connect to MetaTrader 5
connection = MT5Connection(config)
connection.connect()

# Check connection status
print(f"Connected: {connection.is_connected()}")
print(f"Terminal info: {connection.get_terminal_info()}")

# Disconnect when done
connection.disconnect()
```

## Installation 💿

```bash
# Install from PyPI
pip install metatrader-mcp-server

# Or install from source
git clone https://github.com/ariadng/metatrader-mcp-server.git
cd metatrader-mcp-server
pip install -e .
```

## Requirements 📋

- Python 3.13 or higher
- MetaTrader 5 terminal installed
- `MetaTrader5` Python package (automatically installed as a dependency)

## Contributing 🤝

Contributions are welcome! Please check out our [contributing guidelines](../CONTRIBUTING.md) for details.

## Testing 🧪

We have comprehensive tests for all modules. Run them using:

```bash
# Run all tests
python tests/run_tests.py

# Run specific module tests
python tests/client/connection.py
```

## License 📄

This project is licensed under the MIT License - see the [LICENSE](../LICENSE) file for details.

---

*This documentation was last updated on April 10, 2025.*
