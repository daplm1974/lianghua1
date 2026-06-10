"""
EasyXT[EMOJI] 08 - [EMOJI]
[EMOJI]xtquant[EMOJI]

[EMOJI]
1. [EMOJI]
2. [EMOJI]
3. [EMOJI]
4. [EMOJI] vs [EMOJI]
"""

import sys
import os
import pandas as pd
from datetime import datetime
import time

# [EMOJI]Python[EMOJI]
current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)
sys.path.insert(0, parent_dir)

import xtquant.xtdata as xt
import easy_xt


def print_section(title):
    """[EMOJI]"""
    print("\n" + "=" * 70)
    print(title)
    print("=" * 70)


def print_subsection(title):
    """[EMOJI]"""
    print("\n" + "-" * 70)
    print(title)
    print("-" * 70)


def lesson_01_subscription_concept():
    """[EMOJI]1[EMOJI]"""
    print_section("[EMOJI]1[EMOJI]")

    print("""
[BOOK] [EMOJI]

[EMOJI]xtquant[EMOJI]

[EMOJI]
  - [EMOJI] → [EMOJI] → [EMOJI] → [EMOJI]
  - [EMOJI]
  - [EMOJI]

[EMOJI]
  - [EMOJI] → [EMOJI] → [EMOJI]
  - [EMOJI]
  - [EMOJI]

[EMOJI]
  1. subscribe_quote() - [EMOJI]
  2. QMT[EMOJI]
  3. [EMOJI]
  4. [EMOJI]
  5. get_full_tick() - [EMOJI]

[EMOJI]
  [!] [EMOJI]
  [!] [EMOJI]
  [!] [EMOJI]
    """)

    print("\n[TIP] [EMOJI]")
    print("  [EMOJI]")
    print("    - [EMOJI]")
    print("    - [EMOJI]")
    print("    - [EMOJI]")


def lesson_02_subscribe_vs_active():
    """[EMOJI]2[EMOJI] vs [EMOJI]"""
    print_section("[EMOJI]2[EMOJI] vs [EMOJI]")

    api = easy_xt.get_api()
    api.init_data()

    code = '000001.SZ'

    print(f"\n[EMOJI]{code}[EMOJI]")

    # [EMOJI]1[EMOJI]
    print_subsection("[EMOJI]1[EMOJI]")
    print("[EMOJI] get_full_tick()[EMOJI]")

    tick_data = xt.get_full_tick([code])
    if tick_data and code in tick_data:
        tick = tick_data[code]
        print(f"  [EMOJI]: {tick.get('lastPrice', 0):.2f}")
        print(f"  [X] [EMOJI]")

        # [EMOJI]
        ask_price = tick.get('askPrice', 0)
        if ask_price and hasattr(ask_price, '__len__') and len(ask_price) > 0:
            print(f"  [EMOJI]: {ask_price[0]:.2f}")
        else:
            print(f"  [EMOJI]: [EMOJI]")

    # [EMOJI]2[EMOJI]
    print_subsection("[EMOJI]2[EMOJI]")
    print("1. [EMOJI] subscribe_quote() [EMOJI]")
    print("2. [EMOJI]2-3[EMOJI]")
    print("3. [EMOJI] get_full_tick() [EMOJI]")

    xt.subscribe_quote(code, period='tick')
    print("  [OK] [EMOJI]...")
    time.sleep(2.0)

    tick_data = xt.get_full_tick([code])
    if tick_data and code in tick_data:
        tick = tick_data[code]
        print(f"  [EMOJI]: {tick.get('lastPrice', 0):.2f}")

        # [EMOJI]
        ask_price = tick.get('askPrice', 0)
        bid_price = tick.get('bidPrice', 0)

        if ask_price and hasattr(ask_price, '__len__') and len(ask_price) > 0:
            print(f"  [OK] [EMOJI]: {ask_price[0]:.2f}")
            print(f"  [OK] [EMOJI]: {bid_price[0]:.2f}")
            print(f"  [OK] [EMOJI]")

    print("\n[EMOJI]")
    print("  [EMOJI]")
    print("  [EMOJI]")


def lesson_03_callback_function():
    """[EMOJI]3[EMOJI]"""
    print_section("[EMOJI]3[EMOJI]")

    # ==================== [EMOJI]1[EMOJI] ====================
    print_subsection("[EMOJI]1[EMOJI]")

    code = '000001.SZ'

    print(f"\n[TIP] [EMOJI]sleep[EMOJI]")
    print(f"[EMOJI]{code}")

    # [EMOJI]
    counter = {'count': 0, 'max': 5}

    def on_tick_data(data):
        """
        tick[EMOJI]

        [!] [EMOJI]
        [EMOJI]xtquant[EMOJI]

        Args:
            data: dict {[EMOJI]: tick[EMOJI]}
        """
        if code in data:
            tick = data[code]
            counter['count'] += 1

            # [EMOJI]
            print(f"\n[EMOJI] [[EMOJI] #{counter['count']}] {datetime.now().strftime('%H:%M:%S.%f')[:-3]}")
            print(f"   [EMOJI]")
            print(f"   [EMOJI]: {tick.get('lastPrice', 0):.2f}")

            # [EMOJI]
            ask_price = tick.get('askPrice', 0)
            bid_price = tick.get('bidPrice', 0)

            if ask_price and hasattr(ask_price, '__len__') and len(ask_price) > 0:
                print(f"   [EMOJI]: {bid_price[0]:.2f}  [EMOJI]: {ask_price[0]:.2f}")

    print("\n[EMOJI]5[EMOJI]...")
    print("([EMOJI])\n")

    # [EMOJI]
    xt.subscribe_whole_quote(code_list=[code], callback=on_tick_data)

    # [EMOJI]
    start_time = time.time()
    while counter['count'] < counter['max'] and (time.time() - start_time) < 30:
        time.sleep(0.01)  # [EMOJI]CPU[EMOJI]

    if counter['count'] >= counter['max']:
        print(f"\n[OK] [EMOJI] {counter['count']} [EMOJI]")
    else:
        print(f"\n[!] 30[EMOJI] {counter['count']} [EMOJI]")

    # ==================== [EMOJI]2[EMOJI] ====================
    print_subsection("[EMOJI]2[EMOJI]")

    code = '600000.SH'
    last_price = {'value': None}
    alert_count = {'value': 0}

    def on_tick_with_logic(data):
        """[EMOJI]"""
        if code in data:
            tick = data[code]
            current_price = tick.get('lastPrice', 0)

            # [EMOJI]
            if last_price['value'] is None:
                last_price['value'] = current_price
                print(f"\n[CHART] [{datetime.now().strftime('%H:%M:%S')}] "
                      f"[EMOJI]: {code}, [EMOJI]: {current_price:.2f}")
                return

            # [EMOJI]
            price_change = current_price - last_price['value']
            change_pct = (price_change / last_price['value']) * 100

            # [EMOJI]0.01[EMOJI]
            if abs(price_change) >= 0.01:
                direction = "[UP] [EMOJI]" if price_change > 0 else "[EMOJI] [EMOJI]"
                print(f"\n{direction} | {datetime.now().strftime('%H:%M:%S.%f')[:-3]} | "
                      f"{last_price['value']:.2f} → {current_price:.2f} | "
                      f"[EMOJI]: {price_change:+.2f} ({change_pct:+.2f}%)")
                last_price['value'] = current_price
                alert_count['value'] += 1

    print(f"\n[EMOJI]: {code}")
    print("[EMOJI]: [EMOJI]0.01[EMOJI]")
    print("[EMOJI]\n")

    xt.subscribe_whole_quote(code_list=[code], callback=on_tick_with_logic)

    # [EMOJI]10[EMOJI]
    start_time = time.time()
    while time.time() - start_time < 10:
        time.sleep(0.01)

    print(f"\n[OK] 10[EMOJI] {alert_count['value']} [EMOJI]")

    # ==================== [EMOJI]3[EMOJI] ====================
    print_subsection("[EMOJI]3[EMOJI]")

    codes = ['000001.SZ', '000002.SZ']
    push_count = {'value': 0}

    def on_multi_tick(data):
        """[EMOJI]"""
        timestamp = datetime.now().strftime('%H:%M:%S.%f')[:-3]
        print(f"\n[EMOJI] [{timestamp}] [EMOJI]:")

        for code in codes:
            if code in data:
                tick_list = data[code]
                # subscribe_whole_quote[EMOJI]tick[EMOJI]
                if isinstance(tick_list, list) and len(tick_list) > 0:
                    tick = tick_list[-1]  # [EMOJI]tick
                else:
                    tick = tick_list

                price = tick.get('lastPrice', 0)
                print(f"   {code}: {price:.2f} [EMOJI]", end='  ')

        push_count['value'] += 1

    print(f"\n[EMOJI]: {codes}")
    print(f"[EMOJI]: [EMOJI] 3 [EMOJI]\n")

    xt.subscribe_whole_quote(code_list=codes, callback=on_multi_tick)

    start_time = time.time()
    while push_count['value'] < 3 and (time.time() - start_time) < 30:
        time.sleep(0.01)

    print(f"\n[OK] [EMOJI]")

    print("\n[EMOJI]")
    print("  1. [OK] [EMOJI]")
    print("  2. [OK] [EMOJI]sleep[EMOJI]")
    print("  3. [OK] [EMOJI]")
    print("  4. [OK] [EMOJI]")
    print("  5. [OK] [EMOJI]")


def lesson_04_order_book_data():
    """[EMOJI]4[EMOJI]"""
    print_section("[EMOJI]4[EMOJI]")

    print("""
[!] [EMOJI] vs [EMOJI]

[EMOJI]1[EMOJI] [OK] ([EMOJI]3[EMOJI])
  - [EMOJI]
  - [EMOJI]
  - [EMOJI]
  - [EMOJI]

[EMOJI]2[EMOJI] [!]
  - subscribe_quote() [EMOJI]
  - get_full_tick() [EMOJI]
  - [EMOJI]
  - [!] [EMOJI]

[EMOJI]
  [X] [EMOJI]A[EMOJI] (time.sleep(2)) - [EMOJI]
  [OK] [EMOJI]B[EMOJI] - [EMOJI]

[EMOJI]
    """)

    api = easy_xt.get_api()
    api.init_data()

    code = '000001.SZ'

    print(f"\n[EMOJI]{code}")
    print("[EMOJI]5[EMOJI] + [EMOJI]5[EMOJI]")

    # [EMOJI]
    print("\n[EMOJI]1: [EMOJI]tick[EMOJI]")
    xt.subscribe_quote(code, period='tick')
    print("  [OK] [EMOJI]")

    # [EMOJI]
    print("\n[EMOJI]2: [EMOJI]")
    print("       [EMOJI]")

    def wait_for_tick(code, timeout=3.0, interval=0.1):
        """
        [EMOJI]tick[EMOJI]

        Args:
            code: [EMOJI]
            timeout: [EMOJI]
            interval: [EMOJI]

        Returns:
            tick[EMOJI]None
        """
        import time
        start_time = time.time()

        while time.time() - start_time < timeout:
            tick_data = xt.get_full_tick([code])

            if tick_data and code in tick_data:
                tick = tick_data[code]

                # [EMOJI]
                ask_price = tick.get('askPrice', [])
                if ask_price and len(ask_price) > 0 and ask_price[0] > 0:
                    elapsed = time.time() - start_time
                    print(f"  [OK] [EMOJI] {elapsed:.3f} [EMOJI]")
                    return tick

            time.sleep(interval)

        print("  [!] [EMOJI]")
        return None

    # [EMOJI]
    tick = wait_for_tick(code, timeout=3.0, interval=0.1)

    if tick is not None:
        print("\n[EMOJI]3: [EMOJI]tick[EMOJI]")
        print_subsection("[EMOJI]")

        print("\n[EMOJI]")
        print("  askPrice  - [EMOJI] [[EMOJI]1, [EMOJI]2, [EMOJI]3, [EMOJI]4, [EMOJI]5]")
        print("  bidPrice  - [EMOJI] [[EMOJI]1, [EMOJI]2, [EMOJI]3, [EMOJI]4, [EMOJI]5]")
        print("  askVol    - [EMOJI] [[EMOJI]1, [EMOJI]2, ...]")
        print("  bidVol    - [EMOJI] [[EMOJI]1, [EMOJI]2, ...]")

        print_subsection("[EMOJI]")

        ask_price = tick.get('askPrice', [])
        bid_price = tick.get('bidPrice', [])
        ask_vol = tick.get('askVol', [])
        bid_vol = tick.get('bidVol', [])

        print(f"\n  askPrice  = {ask_price}")
        print(f"  bidPrice  = {bid_price}")
        print(f"  askVol    = {ask_vol}")
        print(f"  bidVol    = {bid_vol}")

        print_subsection("[EMOJI]")

        print(f"\n{'[EMOJI]':<8} {'[EMOJI]':<25} {'[EMOJI]':<25}")
        print("-" * 70)

        # [EMOJI]
        for i in range(5):
            # [EMOJI]
            idx = 4 - i  # [EMOJI]5[EMOJI]5[EMOJI]

            ask_p = ask_price[idx] if idx < len(ask_price) else 0
            ask_v = ask_vol[idx] if idx < len(ask_vol) else 0
            bid_p = bid_price[idx] if idx < len(bid_price) else 0
            bid_v = bid_vol[idx] if idx < len(bid_vol) else 0

            if ask_p > 0 or bid_p > 0:
                ask_str = f"{ask_p:.2f} ({ask_v:.0f})" if ask_p > 0 else "--"
                bid_str = f"{bid_p:.2f} ({bid_v:.0f})" if bid_p > 0 else "--"
                print(f"  {i+1}[EMOJI]    {ask_str:<25} {bid_str:<25}")

        print_subsection("[EMOJI]")

        if len(ask_price) > 0 and len(bid_price) > 0:
            spread = ask_price[0] - bid_price[0]
            spread_pct = (spread / bid_price[0]) * 100 if bid_price[0] > 0 else 0
            mid_price = (ask_price[0] + bid_price[0]) / 2

            print(f"\n  [EMOJI]: {spread:.2f} [EMOJI] ({spread_pct:.3f}%)")
            print(f"  [EMOJI]: {mid_price:.2f} [EMOJI]")

            # [EMOJI]
            total_bid_vol = sum(bid_vol) if isinstance(bid_vol, list) else 0
            total_ask_vol = sum(ask_vol) if isinstance(ask_vol, list) else 0

            print(f"  [EMOJI]: {total_bid_vol:.0f} [EMOJI]")
            print(f"  [EMOJI]: {total_ask_vol:.0f} [EMOJI]")

            if total_bid_vol > 0 and total_ask_vol > 0:
                ratio = total_bid_vol / total_ask_vol
                print(f"  [EMOJI]: {ratio:.2f}")

                if ratio > 1.2:
                    print(f"  [EMOJI]: [EMOJI] [UP]")
                elif ratio < 0.8:
                    print(f"  [EMOJI]: [EMOJI] [EMOJI]")
                else:
                    print(f"  [EMOJI]: [EMOJI] [EMOJI]")

    else:
        print("\n[!] [EMOJI]")
        print("   [EMOJI]")
        print("   - [EMOJI]")
        print("   - [EMOJI]")
        print("   - QMT[EMOJI]")

    print("\n[EMOJI]")
    print("  1. [EMOJI]")
    print("  2. askPrice/bidPrice [EMOJI]")
    print("  3. [EMOJI]0[EMOJI]/[EMOJI]")
    print("  4. [EMOJI]")
    print("  5. [EMOJI]")
    print("     - [EMOJI]: time.sleep(2) - [EMOJI]")
    print("     - [EMOJI]: [EMOJI] - [EMOJI] [OK]")


def lesson_05_easy_xt_wrapper():
    """[EMOJI]5[EMOJI]EasyXT[EMOJI]"""
    print_section("[EMOJI]5[EMOJI]EasyXT[EMOJI]")

    api = easy_xt.get_api()
    api.init_data()

    code = '000001.SZ'

    print(f"\nEasyXT[EMOJI]")
    print(f"[EMOJI]api.get_order_book('{code}')")

    print_subsection("[EMOJI]EasyXT[EMOJI]")

    order_book = api.get_order_book(code)

    if order_book is not None and not order_book.empty:
        print(f"\n[OK] [EMOJI]")
        print(f"\n[EMOJI]: {type(order_book)}")
        print(f"[EMOJI]: {order_book.shape}")
        print(f"[EMOJI]: {', '.join(order_book.columns)}")

        print_subsection("[EMOJI]")

        data = order_book.iloc[0]

        print(f"\n[EMOJI]: {data['code']}")
        print(f"[EMOJI]: {data['lastPrice']:.2f}")

        print(f"\n{'[EMOJI]':<8} {'[EMOJI]':<25} {'[EMOJI]':<25}")
        print("-" * 70)

        for i in range(1, 6):
            bid_p = data[f'bid{i}']
            ask_p = data[f'ask{i}']
            bid_v = data[f'bidVol{i}']
            ask_v = data[f'askVol{i}']

            if bid_p > 0 or ask_p > 0:
                bid_str = f"{bid_p:.2f} ({bid_v:.0f})" if bid_p > 0 else "--"
                ask_str = f"{ask_p:.2f} ({ask_v:.0f})" if ask_p > 0 else "--"
                print(f"  {i}[EMOJI]    {bid_str:<25} {ask_str:<25}")

    print("\n[EMOJI]EasyXT[EMOJI]")
    print("  [OK] [EMOJI]")
    print("  [OK] [EMOJI]")
    print("  [OK] [EMOJI]3[EMOJI]")
    print("  [OK] [EMOJI]DataFrame[EMOJI]")
    print("  [OK] [EMOJI]bid1-5, ask1-5[EMOJI]")


def lesson_05_5_easy_xt_subscribe():
    """[EMOJI]5.5[EMOJI]EasyXT[EMOJI]"""
    print_section("[EMOJI]5.5[EMOJI]EasyXT[EMOJI]")

    api = easy_xt.get_api()
    api.init_data()

    print("""
[EMOJI] [EMOJI]EasyXT[EMOJI]

[EMOJI]
  1. api.subscribe()       - [EMOJI]
  2. api.subscribe_whole()  - [EMOJI]
  3. api.unsubscribe()     - [EMOJI]
  4. api.run_forever()     - [EMOJI]
    """)

    # [EMOJI]1[EMOJI]
    print_subsection("[EMOJI]1[EMOJI]")

    code = '000001.SZ'

    print(f"\n[EMOJI]: {code}")

    # [EMOJI]
    def on_tick(data):
        """tick[EMOJI]"""
        if code in data:
            tick_list = data[code]
            # subscribe_whole_quote[EMOJI]tick[EMOJI]
            # [EMOJI]
            if isinstance(tick_list, list) and len(tick_list) > 0:
                tick = tick_list[-1]
            else:
                tick = tick_list

            print(f"  [[EMOJI]] {datetime.now().strftime('%H:%M:%S')} "
                  f"[EMOJI]: {tick.get('lastPrice', 0):.2f}")

    print("\n[EMOJI]5[EMOJI]...")

    # [EMOJI]
    seq = api.subscribe(code, callback=on_tick)

    if seq > 0:
        print(f"[OK] [EMOJI]: {seq}")

        # [EMOJI]5[EMOJI]
        for i in range(5):
            time.sleep(1)

        # [EMOJI]
        api.unsubscribe(seq)
        print("[OK] [EMOJI]")
    else:
        print("[X] [EMOJI]")

    # [EMOJI]2[EMOJI]
    print_subsection("[EMOJI]2[EMOJI]subscribe_whole[EMOJI]")

    codes = ['000001.SZ', '000002.SZ', '600000.SH']

    print(f"\n[EMOJI]: {codes}")

    # [EMOJI]
    counter = {'count': 0, 'max': 3}

    def on_multi_tick(data):
        """[EMOJI]tick[EMOJI]"""
        for code in codes:
            if code in data:
                tick_list = data[code]
                # subscribe_whole_quote[EMOJI]tick[EMOJI]
                if isinstance(tick_list, list) and len(tick_list) > 0:
                    tick = tick_list[-1]
                else:
                    tick = tick_list
                print(f"  {code}: {tick.get('lastPrice', 0):.2f}  ", end='')
        print()  # [EMOJI]
        counter['count'] += 1

    print("\n[EMOJI] subscribe_whole() [EMOJI]...")

    seq = api.subscribe_whole(codes, callback=on_multi_tick)

    if seq > 0:
        print(f"[OK] [EMOJI]: {seq}")

        # [EMOJI]3[EMOJI]
        start = time.time()
        while counter['count'] < counter['max'] and (time.time() - start) < 10:
            time.sleep(0.5)

        api.unsubscribe(seq)
        print("[OK] [EMOJI]")
    else:
        print("[X] [EMOJI]")

    print("\n[EMOJI]EasyXT[EMOJI]")
    print("  [OK] [EMOJI]API[EMOJI]xtdata")
    print("  [OK] [EMOJI]")
    print("  [OK] [EMOJI]")
    print("  [OK] [EMOJI]")
    print("  [OK] [EMOJI]")

    print("\n[EMOJI]")
    print("  [EMOJI]1[EMOJI] → [EMOJI] api.subscribe()")
    print("  [EMOJI]2[EMOJI]     → [EMOJI] api.subscribe_whole()")
    print("  [EMOJI]3[EMOJI]     → [EMOJI] api.run_forever()")


def lesson_06_common_pitfalls():
    """[EMOJI]6[EMOJI]"""
    print_section("[EMOJI]6[EMOJI]")

    print("""
[EMOJI] [EMOJI]1[EMOJI]

[EMOJI]
  - [EMOJI]
  - [EMOJI]askPrice/bidPrice[EMOJI]bid1/ask1[EMOJI]
  - [EMOJI]

[EMOJI]
  [OK] [EMOJI]A[EMOJI]
    def wait_for_tick(code, timeout=3.0):
        start = time.time()
        while time.time() - start < timeout:
            tick_data = xt.get_full_tick([code])
            if tick_data and code in tick_data:
                ask_price = tick_data[code].get('askPrice', [])
                if ask_price and len(ask_price) > 0:
                    return tick_data[code]
            time.sleep(0.1)
        return None

  [OK] [EMOJI]B[EMOJI]
    time.sleep(2.0)  # [EMOJI]

  [OK] [EMOJI]
    ask_price[0]  # [EMOJI]

[TIP] [EMOJI]
  - [EMOJI]
  - [EMOJI]3[EMOJI]

---

[EMOJI] [EMOJI]2[EMOJI]

[EMOJI]
  - [EMOJI](time.sleep(2))[EMOJI]
  - [EMOJI]

[EMOJI]
  [EMOJI]           | [EMOJI]     | [EMOJI] | [EMOJI]
  ---------------|-------------|-----------|--------
  [EMOJI]2[EMOJI]    | 2[EMOJI]  | [EMOJI]      | [EMOJI]
  [EMOJI]0.5[EMOJI]  | 0.5[EMOJI]       | [EMOJI]      | [EMOJI]
  [EMOJI]       | 0.1-0.3[EMOJI]   | [EMOJI]      | [EMOJI]
  [EMOJI]       | 0[EMOJI] | [EMOJI]      | [EMOJI]

[TIP] [EMOJI]
  - [EMOJI] → [EMOJI]
  - [EMOJI]   → [EMOJI]

---

[EMOJI] [EMOJI]3[EMOJI]

[EMOJI]
  - [EMOJI]0[EMOJI]
  - QMT[EMOJI]

[EMOJI]
  [OK] [EMOJI]9:30-15:00[EMOJI]
  [OK] [EMOJI]QMT[EMOJI]
  [OK] [EMOJI]

---

[EMOJI] [EMOJI]4[EMOJI]

[EMOJI]
  - [EMOJI]
  - [EMOJI]
  - [EMOJI]

[EMOJI]
  [OK] [EMOJI] subscribe_whole_quote() [EMOJI]
  [OK] [EMOJI]
  [OK] [EMOJI]

---

[EMOJI] [EMOJI]5[EMOJI]

[EMOJI]
  - [EMOJI]
  - [EMOJI]

[EMOJI]
  [OK] [EMOJI]
  [OK] [EMOJI]
    """)


def lesson_07_practical_exercise():
    """[EMOJI]7[EMOJI]"""
    print_section("[EMOJI]7[EMOJI]")

    api = easy_xt.get_api()
    api.init_data()

    print("\n[EMOJI]1[EMOJI]")
    print("-" * 70)

    code = '000001.SZ'
    print(f"[EMOJI]: {code}[EMOJI]")
    print("[EMOJI]: [EMOJI]\n")

    # [EMOJI]
    xt.subscribe_quote(code, period='tick')

    # [EMOJI]5[EMOJI]
    for i in range(5):
        time.sleep(1)

        tick_data = xt.get_full_tick([code])
        if tick_data and code in tick_data:
            tick = tick_data[code]
            last_price = tick.get('lastPrice', 0)

            ask_price = tick.get('askPrice', [])
            bid_price = tick.get('bidPrice', [])

            if len(ask_price) > 0 and len(bid_price) > 0:
                spread = ask_price[0] - bid_price[0]
                print(f"[{i+1}] {datetime.now().strftime('%H:%M:%S')} "
                      f"[EMOJI]: {last_price:.2f}  [EMOJI]: {spread:.3f}")

    print("\n[OK] [EMOJI]1[EMOJI]")

    print("\n\n[EMOJI]2[EMOJI]")
    print("-" * 70)

    codes = ['000001.SZ', '000002.SZ', '600000.SH']
    print(f"[EMOJI]: {codes}")
    print("[EMOJI]: [EMOJI]\n")

    # [EMOJI]
    for code in codes:
        xt.subscribe_quote(code, period='tick')
    print("[OK] [EMOJI]")

    # [EMOJI]
    time.sleep(2.0)

    # [EMOJI]
    order_books = api.get_order_book(codes)

    if order_books is not None and not order_books.empty:
        print(f"\n{'[EMOJI]':<12} {'[EMOJI]':<10} {'[EMOJI]':<10} {'[EMOJI]':<10} {'[EMOJI]':<10}")
        print("-" * 70)

        for _, row in order_books.iterrows():
            code = row['code']
            last_price = row['lastPrice']
            bid1 = row['bid1']
            ask1 = row['ask1']
            spread = ask1 - bid1 if bid1 > 0 and ask1 > 0 else 0

            print(f"{code:<12} {last_price:<10.2f} {bid1:<10.2f} {ask1:<10.2f} {spread:<10.3f}")

    print("\n[OK] [EMOJI]2[EMOJI]")

    print("\n\n[EMOJI]3[EMOJI]")
    print("-" * 70)

    code = '000001.SZ'
    print(f"[EMOJI]: {code}")
    print("[EMOJI]: [EMOJI]")
    print("\n[EMOJI]3[EMOJI]")
    print("[EMOJI]")

    example_code = '''
def monitor_stock_with_callback(code='000001.SZ', duration=10):
    """[EMOJI]"""

    price_history = []

    def on_tick(data):
        if code in data:
            tick = data[code]
            price = tick.get('lastPrice', 0)

            price_history.append(price)

            print(f"[[EMOJI]] {datetime.now().strftime('%H:%M:%S')} [EMOJI]: {price:.2f}")

    # [EMOJI]
    xt.subscribe_whole_quote(code_list=[code], callback=on_tick)

    # [EMOJI]
    start_time = time.time()
    while time.time() - start_time < duration:
        time.sleep(0.1)

    # [EMOJI]
    if len(price_history) > 0:
        max_price = max(price_history)
        min_price = min(price_history)
        print(f"\\n[EMOJI]: [EMOJI] {max_price:.2f}, [EMOJI] {min_price:.2f}")

# [EMOJI]: monitor_stock_with_callback('000001.SZ', duration=10)
'''

    print(example_code)

    print("\n[OK] [EMOJI]")


def main():
    """[EMOJI]"""
    print("[COURSE] EasyXT[EMOJI]")
    print("=" * 70)
    print("[EMOJI]xtquant[EMOJI]")
    print("\n[EMOJI]")
    print("  1. [EMOJI]")
    print("  2. [EMOJI]")
    print("  3. [EMOJI]")

    # [EMOJI]
    lessons = [
        ("[EMOJI]1[EMOJI]", lesson_01_subscription_concept),
        ("[EMOJI]2[EMOJI] vs [EMOJI]", lesson_02_subscribe_vs_active),
        ("[EMOJI]3[EMOJI]", lesson_03_callback_function),
        ("[EMOJI]4[EMOJI]", lesson_04_order_book_data),
        ("[EMOJI]5[EMOJI]EasyXT[EMOJI]", lesson_05_easy_xt_wrapper),
        ("[EMOJI]5.5[EMOJI]EasyXT[EMOJI]", lesson_05_5_easy_xt_subscribe),
        ("[EMOJI]6[EMOJI]", lesson_06_common_pitfalls),
        ("[EMOJI]7[EMOJI]", lesson_07_practical_exercise),
    ]

    for title, lesson_func in lessons:
        try:
            lesson_func()

            # [EMOJI]
            if not (len(sys.argv) > 1 and '--auto' in sys.argv):
                input("\n[EMOJI]...")
            else:
                print(f"\n[OK] {title} [EMOJI]...")
                time.sleep(1)

        except KeyboardInterrupt:
            print("\n\n[EMOJI]")
            break
        except Exception as e:
            print(f"\n[X] [EMOJI]: {e}")
            import traceback
            traceback.print_exc()

            if not (len(sys.argv) > 1 and '--auto' in sys.argv):
                input("[EMOJI]...")

    print("\n" + "=" * 70)
    print("[EMOJI] [EMOJI]")
    print("\n[EMOJI]")
    print("  [OK] [EMOJI]1[EMOJI]: [EMOJI]")
    print("  [OK] [EMOJI]2[EMOJI]: [EMOJI] vs [EMOJI]")
    print("  [OK] [EMOJI]3[EMOJI]: [EMOJI]")
    print("  [OK] [EMOJI]4[EMOJI]: [EMOJI]")
    print("  [OK] [EMOJI]5[EMOJI]: [EMOJI]EasyXT[EMOJI]")
    print("  [OK] [EMOJI]5.5[EMOJI]: [EMOJI]EasyXT[EMOJI]")
    print("  [OK] [EMOJI]6[EMOJI]: [EMOJI]")
    print("  [OK] [EMOJI]7[EMOJI]: [EMOJI]")

    print("\n[EMOJI]")
    print("  - [EMOJI] 01_[EMOJI].py - [EMOJI]")
    print("  - [EMOJI] 02_[EMOJI].py - [EMOJI]")
    print("  - [EMOJI] 03_[EMOJI].py - [EMOJI]")
    print("  - [EMOJI] tools/[EMOJI]tick[EMOJI].py - [EMOJI]")

    print("\n[TIP] [EMOJI]")
    print("  - [EMOJI]")
    print("  - [EMOJI]")
    print("  - [EMOJI] askPrice/bidPrice [EMOJI]")
    print("  - [EMOJI]EasyXT[EMOJI]")


if __name__ == "__main__":
    main()
