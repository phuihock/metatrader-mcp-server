# MetaTraderMCPServer Project – LLM Overview

This document provides a concise, LLM-friendly summary of the MetaTraderMCPServer project to help LLMs understand the architecture and main concepts without deep file traversal.

## Project Purpose
Implements a MetaTrader 5 (MT5) Multi-Component Platform (MCP) server and client. It provides programmatic access to MT5 order, market, and account operations, with a modular, extensible design.

## Key Modules & Structure

- **src/MetaTraderMCPServer/**
  - **client/**: Main client logic for interacting with MT5.
    - **order/**: Contains individual order-related functions (one per file), e.g., placing, modifying, canceling, and querying orders. All are exposed via `__init__.py` for easy import.
    - **orders.py**: Defines `MT5Orders` class, a high-level wrapper that delegates to functions in `order/`.
    - **market.py**: Market operations (quotes, symbols, etc.).
    - **account.py**: Account management and queries.
    - **connection.py**: Handles MT5 connection lifecycle.
    - **types.py** and **types/**: Custom types (enums, classes) for orders, timeframes, actions, etc. Used throughout the client.
    - **utils.py**: Utility functions.
    - **exceptions.py**: Custom exceptions for error handling.
  - **server/**: (Not detailed here; likely implements MCP server logic.)

## Design Patterns & Conventions
- **Order Logic**: Each order operation is a standalone function in `order/`, imported in `order/__init__.py` and used by `MT5Orders`.
- **Imports**:
  - Inside `order/`: Use relative imports (e.g., `from .get_pending_orders import get_pending_orders`).
  - From outside `order/`: Use `from .order import ...`.
  - Types: Import as `from ..types import ...` when inside `order/`.
- **Extensibility**: Add new order logic by creating a new file in `order/` and exposing it in `__init__.py`.
- **Type Safety**: All major operations use custom types from `types.py` and `types/` for clarity and safety.

## Notable Types
- **Timeframe**: Maps string representations (e.g., "M1", "H1") to MT5 constants.
- **Order/Trade Enums**: Define states, types, actions, and result codes for robust order handling.

## Usage Example
```python
from metatrader_client.orders import MT5Orders
orders = MT5Orders(...)
orders.place_market_order(...)
```

---
This summary is designed for LLMs to quickly grasp the project layout, main abstractions, and extension points. For details, see the respective module docstrings or README.md.
