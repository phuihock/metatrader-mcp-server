# 🧪 Developer Guide: Writing Tests for MetaTrader MCP Server Client

**Last Updated: April 16, 2025**

Welcome! This guide will help you write clear, robust, and maintainable tests for the MetaTrader MCP Server client. You’ll learn about the project structure, test conventions, and best practices—complete with code samples, edge case handling, and pro tips for all submodules.

---

## 📁 Project & Test Structure

- **Source code:**  
  `src/metatrader_client/`
- **Tests:**  
  `tests/metatrader_client/`
  - `test_account.py` - Account module tests
  - `test_order.py` - Order module tests
  - `test_market.py` - Market module tests
  - `test_history.py` - History module tests
  - `test_connection.py` - Connection module tests
- **Test reports:**  
  `tests/reports/`

Each submodule (`account`, `order`, `market`, `history`) is tested in its own file following the pytest naming convention (`test_*.py`). Comprehensive test runs are summarized in Markdown reports.

---

## 🏋️ Running the Tests

The tests are written using pytest and follow standard naming conventions for automatic discovery. Here are different ways to run the tests:

### Running All Tests

```bash
# Run all tests with verbose output
pytest -v tests/metatrader_client

# Run all tests with console output (see print statements)
pytest -v -s tests/metatrader_client
```

### Running Specific Test Files

```bash
# Run only account tests
pytest -v tests/metatrader_client/test_account.py

# Run only order tests
pytest -v tests/metatrader_client/test_order.py

# Run only market tests
pytest -v tests/metatrader_client/test_market.py

# Run only history tests
pytest -v tests/metatrader_client/test_history.py

# Run only connection tests
pytest -v tests/metatrader_client/test_connection.py
```

### Running Specific Test Functions

```bash
# Run a specific test by name
pytest -v tests/metatrader_client/test_account.py::test_get_account_info
```

### Additional pytest options

```bash
# Run tests with JUnit XML report
pytest -v tests/metatrader_client --junitxml=report.xml

# Run tests with code coverage
pytest -v tests/metatrader_client --cov=metatrader_client

# Run tests in parallel (speeds up test execution)
pytest -v tests/metatrader_client -n auto
```

> **Note**: Ensure you have a valid `.env` file with your MetaTrader credentials before running tests. Tests may be skipped if credentials are missing.

---

## 🏗️ Test File Layout & Submodule Access

> **Important**: All test files must follow the pytest naming convention: `test_*.py`. Tests not following this pattern will not be discovered by pytest.

- Use `pytest` as the test runner.
- Use fixtures for client/session setup.
- Use clear, emoji-enhanced print statements for step-by-step feedback.
- Collect results in a `summary` list for reporting.
- **Access submodules via MT5Client attributes:**
  - `client.account`
  - `client.order`
  - `client.market`
  - `client.history`

### Example Unified Fixture

```python
import os
import pytest
from dotenv import load_dotenv
from metatrader_client import MT5Client
import platform

def print_header(title):
    if platform.system() == "Windows":
        os.system('cls')
    else:
        os.system('clear')
    print(f"\n🧪 {title} Full Test Suite 🧪\n")

@pytest.fixture(scope="module")
def mt5_submodule(request):
    print_header(f"MetaTrader 5 MCP {request.param.capitalize()}")
    load_dotenv()
    login = os.getenv("LOGIN")
    password = os.getenv("PASSWORD")
    server = os.getenv("SERVER")
    if not login or not password or not server:
        print("❌ Error: Missing required environment variables!")
        print("Please create a .env file with LOGIN, PASSWORD, and SERVER variables.")
        pytest.skip("Missing environment variables for MetaTrader 5 connection")
    config = {"login": int(login), "password": password, "server": server}
    client = MT5Client(config)
    client.connect()
    print("✅ Connected!\n")
    submodule = getattr(client, request.param)
    yield submodule
    print("\n🔌 Disconnecting from MetaTrader 5...")
    client.disconnect()
    print("👋 Disconnected!")
```

---

## 📚 Submodule Example Usage

### Account
```python
@pytest.mark.parametrize('mt5_submodule', ['account'], indirect=True)
def test_get_account_info(mt5_submodule):
    info = mt5_submodule.get_account_info()
    print(f"Account info: {info}")
    assert isinstance(info, dict)
    assert "login" in info
```

### Order
```python
@pytest.mark.parametrize('mt5_submodule', ['order'], indirect=True)
def test_place_order(mt5_submodule):
    result = mt5_submodule.place_market_order(type="BUY", symbol="EURUSD", volume=0.01)
    print(f"Order result: {result}")
    assert "error" in result
```

### Market
```python
@pytest.mark.parametrize('mt5_submodule', ['market'], indirect=True)
def test_get_symbols(mt5_submodule):
    symbols = mt5_submodule.get_symbols()
    print(f"Symbols: {symbols[:5]}")
    assert isinstance(symbols, list)
```

### History
```python
from datetime import datetime, timedelta
@pytest.mark.parametrize('mt5_submodule', ['history'], indirect=True)
def test_get_deals(mt5_submodule):
    today = datetime.now()
    yesterday = today - timedelta(days=1)
    deals = mt5_submodule.get_deals(from_date=yesterday, to_date=today)
    print(f"Deals: {deals}")
    assert isinstance(deals, list)
```

---

## 📝 Writing Comprehensive Tests

1. **Naming convention:** Create test files with the `test_` prefix (e.g., `test_account.py`).
2. **Setup:** Use fixtures and load environment variables from `.env`.
3. **Define test steps:** Test happy path, edge cases (empty results, invalid input), and error handling.
4. **Friendly logging:** Print with emojis for traceability and developer happiness.
5. **Skip gracefully:** If credentials are missing, use `pytest.skip()` with a helpful message.
6. **Test data:** Use environment variables for symbols, timeframes, and credentials. Use demo accounts for safety.
7. **Reporting:** Write Markdown reports for integration tests in `tests/reports/`.

---

---

## 📝 Writing a Comprehensive Test

### 1. **Setup**
- Use a fixture to connect to MetaTrader 5.
- Ensure environment variables are loaded securely.

### 2. **Define Test Steps**
- Each step should test a single order function (e.g., place, modify, close).
- Use clear print statements and append results to `summary`.

```python
def test_full_order_functionality(mt5_client):
    summary = []
    print("🚀 Placing a market BUY order...")
    result = mt5_client.order.place_market_order(type="BUY", symbol=SYMBOL, volume=VOLUME)
    assert not result["error"], f"Order placement failed: {result['message']}"
    summary.append("🚀 place_market_order: ✅")
    # ...more steps...
```

### 3. **Handle Errors Gracefully**
- Use `try/except` or `assert` statements.
- If a step fails, record it in `summary` with a ❌.

```python
try:
    # test step
    summary.append("Some step: ✅")
except Exception as e:
    summary.append(f"Some step: ❌ {e}")
```

### 4. **Reporting**
- At the end of the test, always write a Markdown report to `tests/reports/`.
- The filename format is [(yyyy-MM-dd_HH-mm-ss)_client_order.md].
- The report includes the date, module, test steps, and a final status.

```python
from datetime import datetime

now = datetime.now()
timestamp = now.strftime('%Y-%m-%d_%H-%M-%S')
report_dir = os.path.join(os.path.dirname(__file__), '../reports')
os.makedirs(report_dir, exist_ok=True)
filename = f"{timestamp}_client_order.md"
filepath = os.path.join(report_dir, filename)
all_passed = all('✅' in s for s in summary)
status = '✅ SUCCESS' if all_passed else '❌ FAILURE'
with open(filepath, 'w', encoding='utf-8') as f:
    f.write(f"# 🧪 MetaTrader 5 MCP Order System Test Report\n\n")
    f.write(f"**Date:** {now.strftime('%Y-%m-%d %H:%M:%S')}\n\n")
    f.write(f"**Module:** Client Order\n\n")
    f.write(f"## Test Steps and Results\n\n")
    for s in summary:
        f.write(f"- {s}\n")
    f.write("\n---\n")
    f.write(f"**Status:** {status}\n")
print(f"\n📄 Test report written to: {filepath}\n")
```

---

## 💡 Best Practices & Tips

- **Follow naming conventions** - All test files must be named `test_*.py` for pytest to discover them.
- **Use named parameters** (e.g., `id=...`) for clarity and to avoid argument mismatches.
- **Patch DataFrame operations** with `errors="ignore"` when dropping columns that may not exist.
- **Print with emojis** for easy scanning of logs and results.
- **Document each step** in the report for traceability.
- **Keep credentials secure**—never hardcode them; always use environment variables.
- **Test on a demo account** to avoid real financial risk.
- **Use pytest marks** - Use `@pytest.mark.parametrize` for test parametrization and `@pytest.mark.xfail` for tests expected to fail.

---

## 🧩 Example: Full Test Flow

```python
def test_full_order_functionality(mt5_client):
    summary = []
    try:
        # 1. Place order
        ...
        summary.append("🚀 place_market_order: ✅")
        # 2. Modify order
        ...
        summary.append("✏️ modify_order: ✅")
        # ... more steps ...
    except Exception as e:
        summary.append(f"❌ Test failed: {e}")
    finally:
        # Write report (see reporting section above)
        ...
```

---

## 🏁 Running the Tests

From your project root, you can run tests for any submodule or for all modules:

### Run a Specific Submodule

```bash
pytest -v -s tests/metatrader_client/test_account.py    # Account tests
pytest -v -s tests/metatrader_client/test_order.py      # Order tests
pytest -v -s tests/metatrader_client/test_market.py     # Market tests
pytest -v -s tests/metatrader_client/test_history.py    # History tests
```

### Run All Tests

```bash
pytest -v -s tests/metatrader_client/
```

- The `-v` flag gives verbose output. The `-s` flag allows print statements (including emojis!) to appear in the console.
- To stop after the first failure, add `--maxfail=1`.
- To see full tracebacks, add `--tb=long`.

### Generate a Markdown Report (Integration Tests)
If your test writes a Markdown report (see previous examples), the report will be saved in `tests/reports/` with a timestamped filename.

### Troubleshooting
- If you see errors about missing environment variables, ensure your `.env` file is present and contains `LOGIN`, `PASSWORD`, and `SERVER`.
- If you get import errors, check that you are running from the project root and your `PYTHONPATH` is set correctly (if needed).
- Use a demo account for all integration tests to avoid real financial risk.

### Continuous Integration (CI)
- For CI pipelines, set environment variables securely in your CI system.
- You can run all tests with:
  ```bash
  pytest -v --tb=short
  ```

---

## 📦 Summary

- Follow the structure and conventions above for clear, robust, and maintainable tests.
- Always generate a report for every test run.
- Use the provided patterns for error handling and reporting.

---

Happy testing, and may your trades always be green! 🌱✨
