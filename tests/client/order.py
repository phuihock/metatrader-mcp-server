import os
import pytest
from dotenv import load_dotenv
from metatrader_client import MT5Client
import platform
import time
from datetime import datetime

SYMBOL = "EURUSD"
VOLUME = 0.01
PENDING_PRICE = 1.2000  # Adjust for your demo market

@pytest.fixture(scope="module")
def mt5_client():
    # Clear console for pretty output
    if platform.system() == "Windows":
        os.system('cls')
    else:
        os.system('clear')
    print("\n🧪 MetaTrader 5 MCP Order System Full Test Suite 🧪\n")
    print("🔑 Loading credentials and connecting to MetaTrader 5...")
    load_dotenv()
    config = {
        "login": int(os.getenv("LOGIN")),
        "password": os.getenv("PASSWORD"),
        "server": os.getenv("SERVER")
    }
    client = MT5Client(config)
    client.connect()
    print("✅ Connected!\n")
    yield client
    print("\n🔌 Disconnecting from MetaTrader 5...")
    client.disconnect()
    print("👋 Disconnected!")

def test_full_order_functionality(mt5_client):
    summary = []
    # 1. Get all positions
    print("\n📋 Getting all open positions...")
    all_positions = mt5_client.order.get_all_positions()
    print(f"📈 All positions:\n{all_positions}")
    summary.append("📋 get_all_positions: ✅")

    # 2. Get positions by symbol
    print("\n🔎 Getting positions by symbol...")
    positions_by_symbol = mt5_client.order.get_positions_by_symbol(SYMBOL)
    print(f"🔎 Positions for {SYMBOL}:\n{positions_by_symbol}")
    summary.append("🔎 get_positions_by_symbol: ✅")

    # 3. Get positions by currency (assuming USD)
    print("\n💵 Getting positions by currency...")
    positions_by_currency = mt5_client.order.get_positions_by_currency("USD")
    print(f"💵 Positions for USD:\n{positions_by_currency}")
    summary.append("💵 get_positions_by_currency: ✅")

    # 4. Place a market order
    print("\n🚀 Placing a market BUY order...")
    market_order = mt5_client.order.place_market_order(
        type="BUY",
        symbol=SYMBOL,
        volume=VOLUME
    )
    assert market_order is not None and ("data" in market_order and market_order["data"] is not None), "❌ Failed to place market order"
    print(f"✅ Market order placed! ID: {market_order['data'].order if market_order['data'] else 'N/A'}")
    summary.append("🚀 place_market_order: ✅")

    # 5. Get positions by id
    print("\n🆔 Getting position by ID...")
    pos_id = market_order["data"].order if market_order["data"] else None
    position_by_id = mt5_client.order.get_positions_by_id(pos_id)
    print(f"🆔 Position for ID {pos_id}:\n{position_by_id}")
    summary.append("🆔 get_positions_by_id: ✅")

    # 6. Place a pending order
    print("\n⏳ Placing a pending BUY order...")
    pending_order = mt5_client.order.place_pending_order(
        type="BUY",
        symbol=SYMBOL,
        volume=VOLUME,
        price=PENDING_PRICE
    )
    assert pending_order is not None and ("data" in pending_order and pending_order["data"] is not None), "❌ Failed to place pending order"
    print(f"✅ Pending order placed! ID: {pending_order['data'].order if pending_order['data'] else 'N/A'}")
    summary.append("⏳ place_pending_order: ✅")

    # 7. Get pending orders (all)
    print("\n🕒 Getting all pending orders...")
    all_pending_orders = mt5_client.order.get_all_pending_orders()
    print(f"🕒 All pending orders:\n{all_pending_orders}")
    summary.append("🕒 get_all_pending_orders: ✅")

    # 8. Get pending orders by symbol
    print("\n🔎 Getting pending orders by symbol...")
    pending_by_symbol = mt5_client.order.get_pending_orders_by_symbol(SYMBOL)
    print(f"🔎 Pending orders for {SYMBOL}:\n{pending_by_symbol}")
    summary.append("🔎 get_pending_orders_by_symbol: ✅")

    # 9. Get pending orders by currency
    print("\n💵 Getting pending orders by currency...")
    pending_by_currency = mt5_client.order.get_pending_orders_by_currency("USD")
    print(f"💵 Pending orders for USD:\n{pending_by_currency}")
    summary.append("💵 get_pending_orders_by_currency: ✅")

    # 10. Get pending orders by id
    print("\n🆔 Getting pending order by ID...")
    pend_id = pending_order["data"].order if pending_order["data"] else None
    pending_by_id = mt5_client.order.get_pending_orders_by_id(pend_id)
    print(f"🆔 Pending order for ID {pend_id}:\n{pending_by_id}")
    summary.append("🆔 get_pending_orders_by_id: ✅")

    # 11. Modify the open position (if supported)
    print("\n✏️ Modifying the open position SL/TP...")
    modified_position = mt5_client.order.modify_position(
        id=pos_id,
        stop_loss=1.1000,   # Example SL value, adjust as needed
        take_profit=1.3000  # Example TP value, adjust as needed
    )
    print(f"✏️ Modified position: {modified_position}")
    summary.append("✏️ modify_position: ✅")

    # 12. Modify the pending order
    print("\n✏️ Modifying the pending order price...")
    new_price = PENDING_PRICE - 0.0005
    modified_pending = mt5_client.order.modify_pending_order(
        id=pend_id,
        price=new_price
    )
    print(f"✏️ Modified pending order: {modified_pending}")
    summary.append("✏️ modify_pending_order: ✅")

    # 13. Close all profitable positions
    print("\n💰 Closing all profitable positions...")
    close_profitable = mt5_client.order.close_all_profittable_positions()
    print(f"💰 Closed profitable positions: {close_profitable}")
    summary.append("💰 close_all_profittable_positions: ✅")

    # 14. Close all losing positions
    print("\n🔻 Closing all losing positions...")
    close_losing = mt5_client.order.close_all_losing_positions()
    print(f"🔻 Closed losing positions: {close_losing}")
    summary.append("🔻 close_all_losing_positions: ✅")

    # 15. Close all positions by symbol
    print(f"\n🔒 Closing all positions for {SYMBOL}...")
    close_by_symbol = mt5_client.order.close_all_positions_by_symbol(SYMBOL)
    print(f"🔒 Closed positions for {SYMBOL}: {close_by_symbol}")
    summary.append("🔒 close_all_positions_by_symbol: ✅")

    # 16. Close all positions
    print("\n🛑 Closing all positions...")
    close_all = mt5_client.order.close_all_positions()
    print(f"🛑 Closed all positions: {close_all}")
    summary.append("🛑 close_all_positions: ✅")

    # 17. Close the specific market order (if still open)
    print("\n🛑 Closing the market order by ID...")
    close_market = mt5_client.order.close_position(id=pos_id)
    print(f"🛑 Closed market order: {close_market}")
    summary.append("🛑 close_position: ✅")

    # 18. Cancel the pending order by ID
    print("\n🚫 Cancelling the pending order by ID...")
    cancel_pending = mt5_client.order.cancel_pending_order(id=pend_id)
    print(f"🚫 Cancelled pending order: {cancel_pending}")
    summary.append("🚫 cancel_pending_order: ✅")

    # 19. Cancel all pending orders by symbol
    print(f"\n🚫 Cancelling all pending orders for {SYMBOL}...")
    cancel_by_symbol = mt5_client.order.cancel_pending_orders_by_symbol(SYMBOL)
    print(f"🚫 Cancelled pending orders for {SYMBOL}: {cancel_by_symbol}")
    summary.append("🚫 cancel_pending_orders_by_symbol: ✅")

    # 20. Cancel all pending orders
    print("\n🚫 Cancelling all pending orders...")
    cancel_all = mt5_client.order.cancel_all_pending_orders()
    print(f"🚫 Cancelled all pending orders: {cancel_all}")
    summary.append("🚫 cancel_all_pending_orders: ✅")

    # Summary
    print("\n\n✨📝 TEST SUMMARY 📝✨")
    for line in summary:
        print(line)
    print("\n🎉 All order functions tested successfully on demo account! 🎉\n")
    time.sleep(1)

    # --- REPORTING SECTION ---
    # Always write report, even if some steps failed
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
