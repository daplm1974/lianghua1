"""
EasyXT[EMOJI] 02 - [EMOJI]
[EMOJI]
[EMOJI]
"""

import sys
import os
import pandas as pd
import time
from datetime import datetime

# [EMOJI]Python[EMOJI]
current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)
sys.path.insert(0, parent_dir)

import easy_xt

# [EMOJI]
try:
    exec(open(os.path.join(parent_dir, 'generate_mock_data.py')).read())
    exec(open(os.path.join(parent_dir, 'mock_trade_functions.py')).read())
    mock_mode = True
    print("[R] [EMOJI]")
except:
    mock_mode = False

# [EMOJI]
USERDATA_PATH = r'D:\[EMOJI]QMT[EMOJI]\userdata_mini' #[EMOJI]
ACCOUNT_ID = "39020958"  # [EMOJI]
TEST_CODE = "000001.SZ"  # [EMOJI]

def lesson_01_trade_setup():
    """[EMOJI]1[EMOJI]"""
    print("=" * 60)
    print("[EMOJI]1[EMOJI]")
    print("=" * 60)

    # 1. [EMOJI]API[EMOJI]
    print("1. [EMOJI]API[EMOJI]")
    api = easy_xt.get_api()
    print("[OK] API[EMOJI]")

    # 2. [EMOJI]
    print("\n2. [EMOJI]")
    try:
        success = api.init_data()
        if success:
            print("[OK] [EMOJI]")
        else:
            if mock_mode:
                print("[!] [EMOJI]")
                success = True
            else:
                print("[X] [EMOJI]")
                return None
    except Exception as e:
        if mock_mode:
            print(f"[!] [EMOJI]: {e}")
            print("[R] [EMOJI]")
            success = True
        else:
            print(f"[X] [EMOJI]: {e}")
            return None

    # 3. [EMOJI]
    print("\n3. [EMOJI]")
    print(f"[EMOJI]: {USERDATA_PATH}")
    try:
        success = api.init_trade(USERDATA_PATH, 'learning_session')
        if success:
            print("[OK] [EMOJI]")
        else:
            if mock_mode:
                print("[!] [EMOJI]")
                success = api.mock_init_trade(USERDATA_PATH, 'learning_session')
                print("[OK] [EMOJI]")
            else:
                print("[X] [EMOJI]")
                print("[EMOJI]")
                print("- [EMOJI]")
                print("- userdata[EMOJI]")
                return None
    except Exception as e:
        if mock_mode:
            print(f"[!] [EMOJI]: {e}")
            print("[R] [EMOJI]")
            success = api.mock_init_trade(USERDATA_PATH, 'learning_session')
            print("[OK] [EMOJI]")
        else:
            print(f"[X] [EMOJI]: {e}")
            return None

    # 4. [EMOJI]
    print(f"\n4. [EMOJI]: {ACCOUNT_ID}")
    try:
        success = api.add_account(ACCOUNT_ID, 'STOCK')
        if success:
            print("[OK] [EMOJI]")
        else:
            if mock_mode:
                print("[!] [EMOJI]")
                success = api.mock_add_account(ACCOUNT_ID, 'STOCK')
                print("[OK] [EMOJI]")
            else:
                print("[X] [EMOJI]")
                print("[EMOJI]")
                return None
    except Exception as e:
        if mock_mode:
            print(f"[!] [EMOJI]: {e}")
            print("[R] [EMOJI]")
            success = api.mock_add_account(ACCOUNT_ID, 'STOCK')
            print("[OK] [EMOJI]")
        else:
            print(f"[X] [EMOJI]: {e}")
            return None

    return api

def lesson_02_account_info(api):
    """[EMOJI]2[EMOJI]"""
    print("\n" + "=" * 60)
    print("[EMOJI]2[EMOJI]")
    print("=" * 60)

    # 1. [EMOJI]
    print("1. [EMOJI]")
    try:
        asset = api.get_account_asset(ACCOUNT_ID)
        if asset:
            print("[OK] [EMOJI]")
            print(f"[EMOJI]: {asset.get('total_asset', 0):,.2f}")
            print(f"[EMOJI]: {asset.get('cash', 0):,.2f}")
            print(f"[EMOJI]: {asset.get('frozen_cash', 0):,.2f}")
            print(f"[EMOJI]: {asset.get('market_value', 0):,.2f}")
        else:
            print("[X] [EMOJI]")
    except Exception as e:
        print(f"[X] [EMOJI]: {e}")

    # 2. [EMOJI]
    print("\n2. [EMOJI]")
    try:
        positions = api.get_positions(ACCOUNT_ID)
        if not positions.empty:
            print("[OK] [EMOJI]")
            print(f"[EMOJI]: {len(positions)}")
            print("[EMOJI]:")
            print(positions[['code', 'volume', 'can_use_volume', 'market_value']].to_string())
        else:
            print("[OK] [EMOJI]")
    except Exception as e:
        print(f"[X] [EMOJI]: {e}")

    # 3. [EMOJI]
    print("\n3. [EMOJI]")
    try:
        orders = api.get_orders(ACCOUNT_ID)
        if not orders.empty:
            print("[OK] [EMOJI]")
            print(f"[EMOJI]: {len(orders)}")
            print("[EMOJI]:")
            # [EMOJI]
            available_columns = ['code', 'order_type', 'volume', 'status']
            display_columns = [col for col in available_columns if col in orders.columns]
            if display_columns:
                print(orders[display_columns].to_string())
            else:
                print("[EMOJI]:")
                print(orders.columns.tolist())
                print(orders.to_string())
        else:
            print("[OK] [EMOJI]")
    except Exception as e:
        print(f"[X] [EMOJI]: {e}")

    # 4. [EMOJI]
    print("\n4. [EMOJI]")
    try:
        trades = api.get_trades(ACCOUNT_ID)
        if not trades.empty:
            print("[OK] [EMOJI]")
            print(f"[EMOJI]: {len(trades)}")
            print("[EMOJI]:")
            print(trades[['stock_code', 'traded_volume', 'traded_price', 'traded_time']].to_string())
        else:
            print("[OK] [EMOJI]")
    except Exception as e:
        print(f"[X] [EMOJI]: {e}")

def lesson_03_market_order(api):
    """[EMOJI]3[EMOJI]"""
    print("\n" + "=" * 60)
    print("[EMOJI]3[EMOJI]")
    print("=" * 60)

    print("[!]  [EMOJI]")
    print("[EMOJI]")

    confirm = input("[EMOJI]([EMOJI] 'yes' [EMOJI] 'y' [EMOJI]): ")
    if confirm.lower() not in ['yes', 'y']:
        print("[EMOJI]")
        return

    # 1. [EMOJI]
    print(f"\n1. [EMOJI] {TEST_CODE} [EMOJI]")
    try:
        current = api.get_current_price(TEST_CODE)
        if not current.empty:
            current_price = current.iloc[0]['price']
            print(f"[OK] [EMOJI]: {current_price:.2f}")
        else:
            print("[X] [EMOJI]")
            return
    except Exception as e:
        print(f"[X] [EMOJI]: {e}")
        return

    # 2. [EMOJI]
    print(f"\n2. [EMOJI] {TEST_CODE} 100[EMOJI]")
    try:
        order_id = api.buy(
            account_id=ACCOUNT_ID,
            code=TEST_CODE,
            volume=100,
            price=0,  # [EMOJI]0
            price_type='market'
        )

        if order_id:
            print(f"[OK] [EMOJI]: {order_id}")

            # [EMOJI]
            print("[EMOJI]3[EMOJI]...")
            time.sleep(3)

            orders = api.get_orders(ACCOUNT_ID)
            if not orders.empty:
                order_info = orders[orders['order_id'] == order_id]
                if not order_info.empty:
                    status = order_info.iloc[0]['status']
                    print(f"[EMOJI]: {status}")
        else:
            print("[X] [EMOJI]")
    except Exception as e:
        print(f"[X] [EMOJI]: {e}")

    # 3. [EMOJI]T+1[EMOJI]
    print(f"\n3. [EMOJI] {TEST_CODE} [EMOJI]")
    try:
        positions = api.get_positions(ACCOUNT_ID, TEST_CODE)
        if not positions.empty:
            total_volume = positions.iloc[0]['volume']  # [EMOJI]
            available_volume = positions.iloc[0]['can_use_volume']  # [EMOJI]

            print(f"[EMOJI]: {total_volume}[EMOJI]")
            print(f"[EMOJI]: {available_volume}[EMOJI]")

            if available_volume >= 100:
                print("[EMOJI]100[EMOJI]")
                order_id = api.sell(
                    account_id=ACCOUNT_ID,
                    code=TEST_CODE,
                    volume=100,
                    price=0,
                    price_type='market'
                )

                if order_id:
                    print(f"[OK] [EMOJI]: {order_id}")
                else:
                    print("[X] [EMOJI]")
            else:
                print("[TIP] T+1[EMOJI]")
                print("   - [EMOJI]")
                print("   - [EMOJI]0[EMOJI]")
                print("   - [EMOJI]")
                print("   [EMOJI]")
        else:
            print("[EMOJI]")
    except Exception as e:
        print(f"[X] [EMOJI]: {e}")

def lesson_04_limit_order(api):
    """[EMOJI]4[EMOJI]"""
    print("\n" + "=" * 60)
    print("[EMOJI]4[EMOJI]")
    print("=" * 60)

    print("[!]  [EMOJI]")
    confirm = input("[EMOJI]([EMOJI] 'yes' [EMOJI] 'y' [EMOJI]): ")
    if confirm.lower() not in ['yes', 'y']:
        print("[EMOJI]")
        return

    # 1. [EMOJI]
    print(f"\n1. [EMOJI] {TEST_CODE} [EMOJI]")
    try:
        current = api.get_current_price(TEST_CODE)
        if not current.empty:
            current_price = current.iloc[0]['price']
            print(f"[OK] [EMOJI]: {current_price:.2f}")
        else:
            print("[X] [EMOJI]")
            return
    except Exception as e:
        print(f"[X] [EMOJI]: {e}")
        return

    # 2. [EMOJI]
    buy_price = round(current_price * 0.99, 2)  # [EMOJI]1%
    print(f"\n2. [EMOJI] {TEST_CODE} 100[EMOJI]: {buy_price}")

    try:
        order_id = api.buy(
            account_id=ACCOUNT_ID,
            code=TEST_CODE,
            volume=100,
            price=buy_price,
            price_type='limit'
        )

        if order_id:
            print(f"[OK] [EMOJI]: {order_id}")

            # [EMOJI]
            time.sleep(2)
            orders = api.get_orders(ACCOUNT_ID)
            if not orders.empty:
                order_info = orders[orders['order_id'] == order_id]
                if not order_info.empty:
                    status = order_info.iloc[0]['status']
                    print(f"[EMOJI]: {status}")

            # [EMOJI]
            print(f"\n3. [EMOJI] {order_id}")
            cancel_result = api.cancel_order(ACCOUNT_ID, order_id)
            if cancel_result:
                print("[OK] [EMOJI]")
            else:
                print("[X] [EMOJI]")
        else:
            print("[X] [EMOJI]")
    except Exception as e:
        print(f"[X] [EMOJI]: {e}")

    # 4. [EMOJI]
    print(f"\n4. [EMOJI]")
    try:
        positions = api.get_positions(ACCOUNT_ID, TEST_CODE)
        if not positions.empty:
            available_volume = positions.iloc[0]['can_use_volume']
            if available_volume >= 100:
                sell_price = round(current_price * 1.01, 2)  # [EMOJI]1%
                print(f"[EMOJI]100[EMOJI]: {sell_price}")

                order_id = api.sell(
                    account_id=ACCOUNT_ID,
                    code=TEST_CODE,
                    volume=100,
                    price=sell_price,
                    price_type='limit'
                )

                if order_id:
                    print(f"[OK] [EMOJI]: {order_id}")

                    # [EMOJI]
                    time.sleep(1)
                    print("[EMOJI]")
                    cancel_result = api.cancel_order(ACCOUNT_ID, order_id)
                    if cancel_result:
                        print("[OK] [EMOJI]")
                else:
                    print("[X] [EMOJI]")
            else:
                print(f"[EMOJI]: {available_volume}[EMOJI]")
        else:
            print("[EMOJI]")
    except Exception as e:
        print(f"[X] [EMOJI]: {e}")

def lesson_05_quick_buy(api):
    """[EMOJI]5[EMOJI]"""
    print("\n" + "=" * 60)
    print("[EMOJI]5[EMOJI]")
    print("=" * 60)

    print("[!]  [EMOJI]")
    confirm = input("[EMOJI]([EMOJI] 'yes' [EMOJI] 'y' [EMOJI]): ")
    if confirm.lower() not in ['yes', 'y']:
        print("[EMOJI]")
        return

    # [EMOJI]
    print(f"\n[EMOJI] {TEST_CODE} [EMOJI]...")
    try:
        price_data = api.get_current_price(TEST_CODE)
        if not price_data.empty:
            current_price = price_data.iloc[0]['price']
            print(f"[EMOJI]: {current_price:.2f} [EMOJI]/[EMOJI]")

            # [EMOJI]1[EMOJI]100[EMOJI]
            min_amount = current_price * 100
            print(f"[EMOJI]1[EMOJI](100[EMOJI])[EMOJI]: {min_amount:.2f} [EMOJI]")

            # [EMOJI]100[EMOJI]
            suggested_amount = int(min_amount / 100) * 100 + 200
            print(f"[EMOJI]: {suggested_amount} [EMOJI]{int(suggested_amount/current_price/100)*100}[EMOJI]")

            # [EMOJI]
            user_input = input(f"\n[EMOJI] {suggested_amount} [EMOJI]: ").strip()
            if user_input:
                buy_amount = float(user_input)
            else:
                buy_amount = suggested_amount

            print(f"[EMOJI]: {buy_amount} [EMOJI]")
        else:
            print("[!] [EMOJI]")
            buy_amount = 1000
    except Exception as e:
        print(f"[!] [EMOJI]: {e}[EMOJI]")
        buy_amount = 1000

    print(f"\n1. [EMOJI] {TEST_CODE}[EMOJI]: {buy_amount}[EMOJI]")

    try:
        order_id = api.quick_buy(
            account_id=ACCOUNT_ID,
            code=TEST_CODE,
            amount=buy_amount,
            price_type='market'
        )

        if order_id:
            print(f"[OK] [EMOJI]: {order_id}")

            # [EMOJI]
            time.sleep(2)
            orders = api.get_orders(ACCOUNT_ID)
            if not orders.empty:
                order_info = orders[orders['order_id'] == order_id]
                if not order_info.empty:
                    volume = order_info.iloc[0]['volume']
                    price = order_info.iloc[0]['price']
                    print(f"[EMOJI]: {volume}[EMOJI]")
                    print(f"[EMOJI]: {price:.2f}")
        else:
            print("[X] [EMOJI]")
    except Exception as e:
        print(f"[X] [EMOJI]: {e}")

def lesson_06_split_order(api):
    """[EMOJI]6[EMOJI]"""
    print("\n" + "=" * 60)
    print("[EMOJI]6[EMOJI]")
    print("=" * 60)

    print("[TIP] [EMOJI]")
    print("[EMOJI]/[EMOJI]")

    # [EMOJI]01_[EMOJI] Lesson 8[EMOJI]
    def split_order(volume: int, max_single_volume: int = 10000,
                   split_strategy: str = 'equal') -> list:
        """
        [EMOJI]

        Args:
            volume: [EMOJI]
            max_single_volume: [EMOJI]
            split_strategy: [EMOJI]
                - 'equal': [EMOJI]
                - 'decreasing': [EMOJI]
                - 'increasing': [EMOJI]

        Returns:
            list: [EMOJI]
        """
        if volume <= max_single_volume:
            return [volume]

        num_splits = (volume + max_single_volume - 1) // max_single_volume

        if split_strategy == 'equal':
            base_volume = volume // num_splits
            remainder = volume % num_splits
            result = [base_volume + 1] * remainder + [base_volume] * (num_splits - remainder)
            return result
        elif split_strategy == 'decreasing':
            result = []
            remaining = volume
            while remaining > 0:
                current = min(max_single_volume, remaining)
                result.append(current)
                remaining -= current
            return result
        elif split_strategy == 'increasing':
            result = []
            remaining = volume
            while remaining > 0:
                current = min(max_single_volume, remaining)
                result.insert(0, current)
                remaining -= current
            return result
        else:
            return split_order(volume, max_single_volume, 'equal')

    # [EMOJI]
    print("\n1. [EMOJI]")
    print("-" * 40)

    print("[!]  [EMOJI]")
    confirm = input("[EMOJI]([EMOJI] 'yes' [EMOJI] 'y' [EMOJI]): ")
    if confirm.lower() not in ['yes', 'y']:
        print("[EMOJI]")
        return

    # [EMOJI]
    total_volume = 30000  # [EMOJI]30000[EMOJI]
    max_single = 5000     # [EMOJI]5000[EMOJI]
    strategy = 'equal'    # [EMOJI]

    print(f"\n[EMOJI]")
    print(f"  [EMOJI]: {TEST_CODE}")
    print(f"  [EMOJI]: {total_volume} [EMOJI]")
    print(f"  [EMOJI]: {max_single} [EMOJI]")
    print(f"  [EMOJI]: {strategy}")

    # [EMOJI]
    splits = split_order(total_volume, max_single, strategy)
    print(f"\n[EMOJI]")
    print(f"  [EMOJI]: {len(splits)} [EMOJI]")
    print(f"  [EMOJI]: {splits}")

    # [EMOJI]
    print(f"\n[EMOJI]...")
    order_ids = []
    success_count = 0
    fail_count = 0

    for i, volume in enumerate(splits, 1):
        print(f"\n[EMOJI] {i}/{len(splits)} [EMOJI]: {volume} [EMOJI]")

        try:
            # [EMOJI]
            order_id = api.buy(
                account_id=ACCOUNT_ID,
                code=TEST_CODE,
                volume=volume,
                price=0,  # [EMOJI]
                price_type='market'
            )

            if order_id:
                order_ids.append(order_id)
                success_count += 1
                print(f"  [OK] [EMOJI]: {order_id}")
            else:
                fail_count += 1
                print(f"  [X] [EMOJI]")

        except Exception as e:
            fail_count += 1
            print(f"  [X] [EMOJI]: {e}")

        # [EMOJI]
        if i < len(splits):  # [EMOJI]
            time.sleep(0.5)

    # [EMOJI]
    print(f"\n[EMOJI]")
    print(f"  [EMOJI]: {success_count} [EMOJI]")
    print(f"  [EMOJI]: {fail_count} [EMOJI]")
    print(f"  [EMOJI]: {order_ids}")

    # [EMOJI]
    if order_ids:
        print(f"\n[EMOJI]...")
        time.sleep(2)

        try:
            orders = api.get_orders(ACCOUNT_ID)
            if not orders.empty:
                print(f"\n[EMOJI]")
                for order_id in order_ids:
                    order_info = orders[orders['order_id'] == order_id]
                    if not order_info.empty:
                        status = order_info.iloc[0].get('status', '[EMOJI]')
                        volume = order_info.iloc[0].get('volume', 0)
                        price = order_info.iloc[0].get('price', 0)
                        print(f"  [EMOJI] {order_id}: {status}, {volume}[EMOJI], {price:.2f}[EMOJI]")
        except Exception as e:
            print(f"[EMOJI]: {e}")

    # [EMOJI]
    print("\n\n2. [EMOJI]")
    print("-" * 40)

    print("[EMOJI]")
    example_code = '''
def split_and_sell(api, account_id, code, total_volume, max_single=5000):
    """[EMOJI]"""

    # 1. [EMOJI]
    splits = split_order(total_volume, max_single, 'decreasing')  # [EMOJI]
    print(f"[EMOJI]: {total_volume}, [EMOJI] {len(splits)} [EMOJI]")

    # 2. [EMOJI]
    order_ids = []
    for i, volume in enumerate(splits, 1):
        print(f"[EMOJI] {i}/{len(splits)} [EMOJI]: {volume} [EMOJI]")

        # [EMOJI]
        order_id = api.sell(
            account_id=account_id,
            code=code,
            volume=volume,
            price=0,  # [EMOJI]
            price_type='market'
        )

        if order_id:
            order_ids.append(order_id)
            print(f"  [OK] [EMOJI]: {order_id}")
        else:
            print(f"  [X] [EMOJI]")

        # [EMOJI]
        time.sleep(0.5)

    return order_ids

# [EMOJI]
# order_ids = split_and_sell(api, ACCOUNT_ID, TEST_CODE, 10000, 5000)
'''
    print(example_code)

    print("\n[TIP] [EMOJI]")
    print("  • [EMOJI]")
    print("  • [EMOJI]")
    print("  • [EMOJI]")
    print("  • [EMOJI]")

def lesson_07_order_monitoring(api):
    """[EMOJI]7[EMOJI]"""
    print("\n" + "=" * 60)
    print("[EMOJI]7[EMOJI]")
    print("=" * 60)

    print("1. [EMOJI]")
    try:
        orders = api.get_orders(ACCOUNT_ID)
        if not orders.empty:
            print(f"[OK] [EMOJI] {len(orders)} [EMOJI]")
            print("\n[EMOJI]:")
            for _, order in orders.iterrows():
                print(f"[EMOJI]: {order['order_id']}")
                print(f"[EMOJI]: {order['code']}")
                print(f"[EMOJI]: {order['order_type']}")
                print(f"[EMOJI]: {order['volume']}")
                print(f"[EMOJI]: {order['price']:.2f}")
                print(f"[EMOJI]: {order['status']}")
                print("-" * 30)
        else:
            print("[OK] [EMOJI]")
    except Exception as e:
        print(f"[X] [EMOJI]: {e}")

    # 2. [EMOJI]
    print("\n2. [EMOJI]")
    try:
        cancelable_orders = api.get_orders(ACCOUNT_ID, cancelable_only=True)
        if not cancelable_orders.empty:
            print(f"[OK] [EMOJI] {len(cancelable_orders)} [EMOJI]")
            for _, order in cancelable_orders.iterrows():
                print(f"[EMOJI]: {order['order_id']} - {order['stock_code']}")
        else:
            print("[OK] [EMOJI]")
    except Exception as e:
        print(f"[X] [EMOJI]: {e}")

    # 3. [EMOJI]
    print("\n3. [EMOJI]")
    try:
        trades = api.get_trades(ACCOUNT_ID)
        if not trades.empty:
            print(f"[OK] [EMOJI] {len(trades)} [EMOJI]")
            print("\n[EMOJI]:")
            for _, trade in trades.iterrows():
                print(f"[EMOJI]: {trade.get('trade_id', 'N/A')}")
                print(f"[EMOJI]: {trade.get('code', trade.get('stock_code', 'N/A'))}")
                print(f"[EMOJI]: {trade.get('volume', trade.get('traded_volume', 'N/A'))}")
                print(f"[EMOJI]: {trade.get('price', trade.get('traded_price', 0)):.2f}")
                print(f"[EMOJI]: {trade.get('time', trade.get('traded_time', 'N/A'))}")
                print("-" * 30)
        else:
            print("[OK] [EMOJI]")
    except Exception as e:
        print(f"[X] [EMOJI]: {e}")

def lesson_08_practice_summary(api):
    """[EMOJI]8[EMOJI]"""
    print("\n" + "=" * 60)
    print("[EMOJI]8[EMOJI]")
    print("=" * 60)

    print("[EMOJI]")
    print("1. [OK] [EMOJI]")
    print("2. [OK] [EMOJI]")
    print("3. [OK] [EMOJI]")
    print("4. [OK] [EMOJI]")
    print("5. [OK] [EMOJI]")
    print("6. [OK] [EMOJI]")
    print("7. [OK] [EMOJI]")

    print("\n[EMOJI]")
    print("• [EMOJI]")
    print("• [EMOJI]")
    print("• [EMOJI]price=0, price_type='market'")
    print("• [EMOJI]price=[EMOJI], price_type='limit'")
    print("• [EMOJI]get_orders()[EMOJI]")
    print("• [EMOJI]cancel_order()[EMOJI]")
    print("• quick_buy()[EMOJI]")

    print("\n[EMOJI]")
    try:
        # [EMOJI]
        asset = api.get_account_asset(ACCOUNT_ID)
        if asset:
            print(f"[EMOJI]: {asset.get('total_asset', 0):,.2f}")
            print(f"[EMOJI]: {asset.get('cash', 0):,.2f}")

        # [EMOJI]
        positions = api.get_positions(ACCOUNT_ID)
        if not positions.empty:
            print(f"[EMOJI]: {len(positions)}")
        else:
            print("[EMOJI]: 0")

        # [EMOJI]
        orders = api.get_orders(ACCOUNT_ID)
        if not orders.empty:
            print(f"[EMOJI]: {len(orders)}")
        else:
            print("[EMOJI]: 0")

    except Exception as e:
        print(f"[EMOJI]: {e}")

def main():
    """[EMOJI]"""
    print("[COURSE] EasyXT[EMOJI]")
    print("[EMOJI]EasyXT[EMOJI]")
    print("\n[!]  [EMOJI]")
    print("1. [EMOJI]")
    print("2. [EMOJI]USERDATA_PATH[EMOJI]ACCOUNT_ID[EMOJI]")
    print("3. [EMOJI]")
    print("4. [EMOJI]")

    # [EMOJI]
    confirm = input("\n[EMOJI]([EMOJI] 'yes' [EMOJI] 'y' [EMOJI]): ")
    if confirm.lower() not in ['yes', 'y']:
        print("[EMOJI]")
        return

    # [EMOJI]1[EMOJI]
    api = lesson_01_trade_setup()
    if not api:
        print("[EMOJI]")
        return

    # [EMOJI]
    lessons = [
        lambda: lesson_02_account_info(api),
        lambda: lesson_03_market_order(api),
        lambda: lesson_04_limit_order(api),
        lambda: lesson_05_quick_buy(api),
        lambda: lesson_06_split_order(api),
        lambda: lesson_07_order_monitoring(api),
        lambda: lesson_08_practice_summary(api)
    ]

    for i, lesson in enumerate(lessons, 2):
        try:
            lesson()
            if i < len(lessons) + 1:  # [EMOJI]
                input(f"\n[EMOJI]{i+1}[EMOJI]...")
        except KeyboardInterrupt:
            print("\n\n[EMOJI]")
            break
        except Exception as e:
            print(f"\n[EMOJI]: {e}")
            input("[EMOJI]...")

    print("\n[EMOJI] [EMOJI]")
    print("[EMOJI]")
    print("- 03_[EMOJI].py - [EMOJI]")
    print("- 04_[EMOJI].py - [EMOJI]")
    print("- 05_[EMOJI].py - [EMOJI]")

if __name__ == "__main__":
    main()
