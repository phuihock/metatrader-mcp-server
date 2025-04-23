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

## 4. Expose existing MCP Tools via REST endpoints

- Define corresponding routes for each MCP tools defined in `src/metatrader_mcp/server.py` (e.g. `GET /api/v1/get_account_info`)
- Use async endpoints and proper Pydantic models for request/response schemas

## 5. Customize metadata & examples

- Set `info.title`, `info.version`, `description` in the constructor
- Use `@router.post(..., openapi_examples=...)` to provide sample payloads

## 6. Conditional docs

- Control OpenAPI and Swagger UI URLs via env vars (disable docs in production by setting `openapi_url=None`)

## 7. Testing & CI

- Write `pytest` tests using `TestClient(app)` from `fastapi.testclient`
- Assert the `/openapi.json` schema and endpoint behaviors
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
