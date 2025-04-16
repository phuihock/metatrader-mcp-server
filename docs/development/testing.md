# 🧪 Developer Guide: Writing Tests for MetaTrader MCP Server Client

Welcome! This guide will help you write clear, robust, and maintainable tests for the MetaTrader MCP Server client. You’ll learn about the project structure, test conventions, and best practices—complete with code samples and pro tips.

---

## 📁 Project & Test Structure

- **Source code:**  
  `src/metatrader_client/`
- **Tests:**  
  `tests/metatrader_client/`
- **Test reports:**  
  `tests/reports/`

Each order-related function (e.g., place, modify, close) is tested in its own logical step, and comprehensive test runs are summarized in Markdown reports.

---

## 🏗️ Test File Layout

- Use `pytest` as the test runner.
- Use fixtures for client/session setup.
- Use clear, emoji-enhanced print statements for step-by-step feedback.
- Collect results in a `summary` list for reporting.

### Example Test Skeleton

```python
import os
import pytest
from dotenv import load_dotenv
from metatrader_client import MT5Client
from datetime import datetime

SYMBOL = "EURUSD"
VOLUME = 0.01

@pytest.fixture(scope="module")
def mt5_client():
    load_dotenv()
    # Check if environment variables are set
    login = os.getenv("LOGIN")
    password = os.getenv("PASSWORD")
    server = os.getenv("SERVER")
    
    if not login or not password or not server:
        print("❌ Error: Missing required environment variables!")
        print("Please create a .env file with LOGIN, PASSWORD, and SERVER variables.")
        pytest.skip("Missing environment variables for MetaTrader 5 connection")
        
    config = {
        "login": int(login),
        "password": password,
        "server": server
    }
    client = MT5Client(config)
    assert client.connected, "Failed to connect to MetaTrader 5"
    yield client
    client.disconnect()
```

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

- **Use named parameters** (e.g., `id=...`) for clarity and to avoid argument mismatches.
- **Patch DataFrame operations** with `errors="ignore"` when dropping columns that may not exist.
- **Print with emojis** for easy scanning of logs and results.
- **Document each step** in the report for traceability.
- **Keep credentials secure**—never hardcode them; always use environment variables.
- **Test on a demo account** to avoid real financial risk.

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

From your project root, run:

```bash
pytest -s tests/metatrader_client/order.py
```

---

## 📦 Summary

- Follow the structure and conventions above for clear, robust, and maintainable tests.
- Always generate a report for every test run.
- Use the provided patterns for error handling and reporting.

---

Happy testing, and may your trades always be green! 🌱✨
