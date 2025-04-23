# OpenAPI Server Plan

This document outlines the steps to integrate a FastAPI-based OpenAPI server into the MetaTrader MCP project.

## 1. Add dependencies

- Install `fastapi` and `uvicorn`
- Add `pydantic` for settings management
- Install `pytest` and `httpx` for API tests

## 2. Define configuration via Pydantic Settings

- Create a `Settings` class (e.g., in `src/metatrader_openapi/config.py`) with fields:
  - `openapi_url`
  - `docs_url`
  - `redoc_url`
  - `title`
  - `version`
- Load settings from environment variables for environment-specific toggling
- Import and instantiate `Settings()` in `src/metatrader_openapi/main.py` (e.g., `settings = Settings()`)

## 3. Boilerplate FastAPI app

- Create `src/metatrader_openapi/main.py`
- Initialize `FastAPI` with settings:
  ```python
  app = FastAPI(
      title=settings.title,
      version=settings.version,
      openapi_url=settings.openapi_url,
      docs_url=settings.docs_url,
      redoc_url=settings.redoc_url,
  )
  ```
- Mount routers under `/api/v1`
- Create a `src/metatrader_openapi/routers` package and define endpoint modules (e.g., `orders.py`, `accounts.py`) for grouping routes

## 4. Expose existing MCP Tools via REST endpoints

- **Accounts**
  - `GET /api/v1/accounts/info` → `get_account_info`

- **History**
  - `GET /api/v1/history/deals?from_date=&to_date=&symbol=` → `get_deals`
  - `GET /api/v1/history/orders?from_date=&to_date=&symbol=` → `get_orders`

- **Market**
  - `GET /api/v1/market/candles/latest?symbol_name=&timeframe=&count=` → `get_candles_latest`
  - `GET /api/v1/market/price/{symbol_name}` → `get_symbol_price`
  - `GET /api/v1/market/symbols` → `get_all_symbols`
  - `GET /api/v1/market/symbols/filter?group=` → `get_symbols`

- **Positions**
  - `GET /api/v1/positions` → `get_all_positions`
  - `GET /api/v1/positions/symbol/{symbol}` → `get_positions_by_symbol`
  - `GET /api/v1/positions/{id}` → `get_positions_by_id`
  - `PUT /api/v1/positions/{id}` → `modify_position`
  - `DELETE /api/v1/positions/{id}` → `close_position`
  - `DELETE /api/v1/positions` → `close_all_positions`
  - `DELETE /api/v1/positions/symbol/{symbol}` → `close_all_positions_by_symbol`
  - `DELETE /api/v1/positions/profitable` → `close_all_profittable_positions`
  - `DELETE /api/v1/positions/losing` → `close_all_losing_positions`

- **Pending Orders**
  - `GET /api/v1/orders/pending` → `get_all_pending_orders`
  - `GET /api/v1/orders/pending/symbol/{symbol}` → `get_pending_orders_by_symbol`
  - `GET /api/v1/orders/pending/{id}` → `get_pending_orders_by_id`
  - `PUT /api/v1/orders/pending/{id}` → `modify_pending_order`
  - `DELETE /api/v1/orders/pending/{id}` → `cancel_pending_order`
  - `DELETE /api/v1/orders/pending` → `cancel_all_pending_orders`
  - `DELETE /api/v1/orders/pending/symbol/{symbol}` → `cancel_pending_orders_by_symbol`

- **New Order Placement**
  - `POST /api/v1/orders/market` → `place_market_order`
  - `POST /api/v1/orders/pending` → `place_pending_order`

## 5. Customize metadata & examples

- Set `info.title`, `info.version`, `description` in the constructor
- Use `@router.post(..., openapi_examples=...)` to provide sample payloads

## 6. Conditional docs

- Control OpenAPI and Swagger UI URLs via env vars (disable docs in production by setting `openapi_url=None`)

## 7. Testing & CI

- Write `pytest` tests using `TestClient(app)` from `fastapi.testclient`
- Assert the `/openapi.json` schema and endpoint behaviors
- Validate `/openapi.json` schema using a tool like `spectral` or `openapi-cli lint` in CI
- Integrate tests into CI pipeline

## 8. Documentation & README

- Update `README.md` with:
  - Installation steps
  - Env var configuration
  - How to run the server (`uvicorn src.metatrader_openapi.main:app --reload`)
  - Sample curl commands & screenshots

## 9. Future enhancements

- Add security (OAuth2, API keys)
- Versioning and router grouping
- Rate-limiting, CORS, monitoring (Prometheus)
