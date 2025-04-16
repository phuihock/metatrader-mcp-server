# MetaTrader MCP Server Documentation 📚

Welcome to the MetaTrader MCP Server documentation! This guide will help you understand how to use our library to connect AI Large Language Models (LLMs) with MetaTrader 5 for automated trading.

## Project Overview 🌟

MetaTrader MCP Server implements a Model Context Protocol (MCP) server that enables AI LLMs to interact with and trade using the MetaTrader platform. The project bridges the gap between advanced AI models and the powerful trading capabilities of MetaTrader 5.

## Module Structure 🏗️

The project is organized into two main modules:

### Client Module 🖥️

The client module provides a unified Python interface for MetaTrader 5 automation—connect, trade, analyze, and manage your MT5 terminal with a single, easy-to-use client. Perfect for algo trading, analytics, and robust trading automation! 🚀

**Key Features:**
- Unified `MT5Client` class to manage all MetaTrader 5 operations
- Submodules for account info, market data, trading/order management, historical data, and connection handling
- Simple initialization and configuration
- Designed for both beginners and advanced users

For a detailed guide and usage examples, see the [Client Module Documentation](metatrader_client/README.md).


### Server Module 🌐

The server module implements the Model Context Protocol interface:

- **MCP Server** (Coming Soon) - Implements the MCP protocol for AI model communication
- **Tools** (Coming Soon) - Implements MCP tools for trading operations
- **Security** (Coming Soon) - Authentication and authorization for the MCP server


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

- Windows 10 or higher
- Python 3.13 or higher
- MetaTrader 5 terminal installed

## License 📄

This project is licensed under the MIT License - see the [LICENSE](../LICENSE) file for details.

---

*This documentation was last updated on April 16, 2025.*
