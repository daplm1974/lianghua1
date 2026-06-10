"""
EasyXT[EMOJI] 21 - xqshare[EMOJI]Mac/Linux[EMOJI]
[EMOJI]xqshare[EMOJI]Mac/Linux[EMOJI]EasyXT

[EMOJI]
- macOS [EMOJI] EasyXT
- Linux [EMOJI]
- Windows [EMOJI]QMT[EMOJI]

[EMOJI]
1. [EMOJI] xqshare: pip install xqshare
2. [EMOJI] .env [EMOJI]
   export XQSHARE_REMOTE_HOST="your-server-ip"
   export XQSHARE_REMOTE_PORT="18812"

[EMOJI]@jasonhu - [EMOJI]xqshare[EMOJI]
"""

import sys
import os
import pandas as pd
from datetime import datetime, timedelta

# [EMOJI]Python[EMOJI]
current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)
sys.path.insert(0, parent_dir)

# [EMOJI]
from core.path_manager import init_paths
init_paths()

import easy_xt

# ============================================================================
# [EMOJI]1[EMOJI]
# ============================================================================

def lesson_01_environment_setup():
    """[EMOJI]1[EMOJI]"""
    print("=" * 80)
    print("[EMOJI]1[EMOJI]xqshare [EMOJI]")
    print("=" * 80)

    # 1. [EMOJI]
    print("\n1[EMOJI]⃣ [EMOJI] xqshare [EMOJI]")
    print("-" * 80)

    xqshare_host = os.environ.get('XQSHARE_REMOTE_HOST')
    xqshare_port = os.environ.get('XQSHARE_REMOTE_PORT')

    if xqshare_host:
        print(f"[OK] XQSHARE_REMOTE_HOST: {xqshare_host}")
        print(f"[OK] XQSHARE_REMOTE_PORT: {xqshare_port or '18812'}")
    else:
        print("[!]  [EMOJI] XQSHARE_REMOTE_HOST [EMOJI]")
        print("[TIP] [EMOJI]")
        print("   [EMOJI]1[EMOJI]")
        print("   export XQSHARE_REMOTE_HOST='your-server-ip'")
        print("   export XQSHARE_REMOTE_PORT='18812'")
        print()
        print("   [EMOJI]2[EMOJI] .env [EMOJI]")
        print("   echo 'XQSHARE_REMOTE_HOST=your-server-ip' >> .env")
        print("   echo 'XQSHARE_REMOTE_PORT=18812' >> .env")
        print()
        return False

    # 2. [EMOJI]API[EMOJI]
    print("\n2[EMOJI]⃣ [EMOJI] EasyXT API [EMOJI]")
    print("-" * 80)
    api = easy_xt.get_api()
    print("[OK] API[EMOJI]")

    # 3. [EMOJI] xqshare[EMOJI]
    print("\n3[EMOJI]⃣ [EMOJI]")
    print("-" * 80)
    print("[EMOJI]")
    print("  1[EMOJI]⃣  QMT ([EMOJI])")
    print("  2[EMOJI]⃣  xqshare ([EMOJI]) ← Mac/Linux [EMOJI]")
    print("  3[EMOJI]⃣  TDX ([EMOJI])")
    print("  4[EMOJI]⃣  Eastmoney ([EMOJI])")
    print()

    try:
        success = api.init_data()
        if success:
            print("[OK] [EMOJI]")

            # [EMOJI]
            active_source = api.data.get_active_source()
            print(f"[OK] [EMOJI]: {active_source}")

            if active_source == 'xqshare':
                print("[OK] [EMOJI] xqshare [EMOJI]")
                print("[EMOJI] [EMOJI]")

            return True
        else:
            print("[X] [EMOJI]")
            return False
    except Exception as e:
        print(f"[X] [EMOJI]: {e}")
        return False


# ============================================================================
# [EMOJI]2[EMOJI]K[EMOJI]
# ============================================================================

def lesson_02_query_daily_kline():
    """[EMOJI]2[EMOJI]K[EMOJI]"""
    print("\n" + "=" * 80)
    print("[EMOJI]2[EMOJI]K[EMOJI]")
    print("=" * 80)

    api = easy_xt.get_api()

    # 1. [EMOJI]K[EMOJI]
    print("\n1[EMOJI]⃣ [EMOJI]K[EMOJI]")
    print("-" * 80)

    stock_code = '000001.SZ'  # [EMOJI]
    print(f"[EMOJI]: {stock_code}")
    print(f"[EMOJI]: [EMOJI]30[EMOJI]")
    print()

    try:
        # [EMOJI]30[EMOJI]K[EMOJI]
        df = api.data.get_price(
            codes=[stock_code],
            count=30,
            period='1d',  # 1d=[EMOJI], 1w=[EMOJI], 1m=[EMOJI]
            fields=['open', 'high', 'low', 'close', 'volume', 'amount']
        )

        if df is not None and not df.empty:
            print("[OK] [EMOJI]")
            print(f"[EMOJI]: {df.shape}")
            print()
            print("[EMOJI]5[EMOJI]:")
            print("-" * 80)
            print(df.tail().to_string())
            print()

            # [EMOJI]
            print("[EMOJI]:")
            print(f"  [EMOJI]: {df['close'].iloc[-1]:.2f}")
            print(f"  [EMOJI]: {df['high'].max():.2f}")
            print(f"  [EMOJI]: {df['low'].min():.2f}")
            print(f"  [EMOJI]: {df['volume'].mean():,.0f}")

        else:
            print("[X] [EMOJI]")
            return False

    except Exception as e:
        print(f"[X] [EMOJI]: {e}")
        return False

    # 2. [EMOJI]K[EMOJI]
    print("\n2[EMOJI]⃣ [EMOJI]K[EMOJI]")
    print("-" * 80)

    stock_list = ['000001.SZ', '000002.SZ', '600000.SH']
    print(f"[EMOJI]: {stock_list}")
    print()

    try:
        df = api.data.get_price(
            codes=stock_list,
            count=10,
            period='1d'
        )

        if df is not None and not df.empty:
            print("[OK] [EMOJI]")
            print(f"[EMOJI]: {df.shape}")
            print()
            print("[EMOJI]:")
            print("-" * 80)

            # [EMOJI]
            for code in stock_list:
                stock_data = df[df['code'] == code]
                if not stock_data.empty:
                    latest = stock_data.iloc[-1]
                    print(f"{code}: {latest['close']:.2f}")

        else:
            print("[X] [EMOJI]")

    except Exception as e:
        print(f"[X] [EMOJI]: {e}")

    return True


# ============================================================================
# [EMOJI]3[EMOJI]K[EMOJI]
# ============================================================================

def lesson_03_query_date_range():
    """[EMOJI]3[EMOJI]K[EMOJI]"""
    print("\n" + "=" * 80)
    print("[EMOJI]3[EMOJI]K[EMOJI]")
    print("=" * 80)

    api = easy_xt.get_api()

    # [EMOJI]2024[EMOJI]
    print("\n1[EMOJI]⃣ [EMOJI]2024[EMOJI]K[EMOJI]")
    print("-" * 80)

    stock_code = '511090.SH'  # 30[EMOJI]ETF
    start_date = '20240101'
    end_date = '20241231'

    print(f"[EMOJI]: {stock_code}")
    print(f"[EMOJI]: {start_date} ~ {end_date}")
    print()

    try:
        df = api.data.get_price(
            codes=[stock_code],
            start=start_date,
            end=end_date,
            period='1d'
        )

        if df is not None and not df.empty:
            print("[OK] [EMOJI]")
            print(f"[EMOJI]: {df.shape} ([EMOJI] {len(df)} [EMOJI])")
            print()
            print("[EMOJI]:")
            print("-" * 80)
            year_start = df.iloc[0]
            year_end = df.iloc[-1]

            print(f"[EMOJI] ({year_start['time']}):")
            print(f"  [EMOJI]: {year_start['open']:.3f}")
            print(f"  [EMOJI]: {year_start['close']:.3f}")
            print()
            print(f"[EMOJI] ({year_end['time']}):")
            print(f"  [EMOJI]: {year_end['open']:.3f}")
            print(f"  [EMOJI]: {year_end['close']:.3f}")
            print()

            # [EMOJI]
            annual_return = (year_end['close'] - year_start['close']) / year_start['close'] * 100
            print(f"[EMOJI]: {annual_return:+.2f}%")

        else:
            print("[X] [EMOJI]")

    except Exception as e:
        print(f"[X] [EMOJI]: {e}")


# ============================================================================
# [EMOJI]4[EMOJI]
# ============================================================================

def lesson_04_query_account_assets():
    """[EMOJI]4[EMOJI]"""
    print("\n" + "=" * 80)
    print("[EMOJI]4[EMOJI]")
    print("=" * 80)

    # [!] [EMOJI]
    print("\n[!]  [EMOJI]")
    print("-" * 80)
    print("[EMOJI]")
    print("1. [EMOJI] QMT [EMOJI] xqshare [EMOJI]")
    print("2. [EMOJI] QMT [EMOJI]")
    print("3. [EMOJI] ID [EMOJI]")
    print()

    # [EMOJI]
    QMT_PATH = os.environ.get('QMT_PATH', r'D:\[EMOJI]QMT[EMOJI]\userdata_mini')
    ACCOUNT_ID = os.environ.get('QMT_ACCOUNT_ID', '39020958')

    print(f"QMT [EMOJI]: {QMT_PATH}")
    print(f"[EMOJI] ID: {ACCOUNT_ID}")
    print()

    api = easy_xt.get_api()

    # 1. [EMOJI]
    print("1[EMOJI]⃣ [EMOJI]")
    print("-" * 80)

    try:
        # xqshare [EMOJI]
        success = api.init_trade(QMT_PATH, 'xqshare_session')

        if success:
            print("[OK] [EMOJI]")

            # [EMOJI] xqshare
            if os.environ.get('XQSHARE_REMOTE_HOST'):
                print("[OK] [EMOJI] xqshare [EMOJI]")

        else:
            print("[X] [EMOJI]")
            print("[TIP] [EMOJI]")
            print("   1. QMT [EMOJI]")
            print("   2. [EMOJI]")
            print("   3. [EMOJI]")
            print("   4. xqshare [EMOJI]")
            return False

    except Exception as e:
        print(f"[X] [EMOJI]: {e}")
        return False

    # 2. [EMOJI]
    print("\n2[EMOJI]⃣ [EMOJI]")
    print("-" * 80)

    try:
        success = api.trade.add_account(ACCOUNT_ID, 'STOCK')
        if success:
            print(f"[OK] [EMOJI] {ACCOUNT_ID} [EMOJI]")
        else:
            print(f"[X] [EMOJI] {ACCOUNT_ID} [EMOJI]")
            return False
    except Exception as e:
        print(f"[X] [EMOJI]: {e}")
        return False

    # 3. [EMOJI]
    print("\n3[EMOJI]⃣ [EMOJI]")
    print("-" * 80)

    try:
        assets = api.trade.get_account_asset(ACCOUNT_ID)

        if assets:
            print("[OK] [EMOJI]")
            print()
            print("[EMOJI]:")
            print("-" * 80)

            # [EMOJI]
            total_asset = assets.get('[EMOJI]', 0)
            cash = assets.get('[EMOJI]', 0)
            market_value = assets.get('[EMOJI]', 0)
            frozen_cash = assets.get('[EMOJI]', 0)
            position_pnl = assets.get('[EMOJI]', 0)

            print(f"[EMOJI]: ¥{total_asset:,.2f}")
            print(f"[EMOJI]: ¥{cash:,.2f}")
            print(f"[EMOJI]: ¥{market_value:,.2f}")
            print(f"[EMOJI]: ¥{frozen_cash:,.2f}")
            print(f"[EMOJI]: ¥{position_pnl:,.2f}")

            # [EMOJI]
            if total_asset > 0:
                cash_ratio = cash / total_asset * 100
                stock_ratio = market_value / total_asset * 100
                print()
                print("[EMOJI]:")
                print(f"  [EMOJI]: {cash_ratio:.2f}%")
                print(f"  [EMOJI]: {stock_ratio:.2f}%")

            return True

        else:
            print("[X] [EMOJI]")
            return False

    except Exception as e:
        print(f"[X] [EMOJI]: {e}")
        print("[TIP] [EMOJI]")
        print("   1. [EMOJI] ID [EMOJI]")
        print("   2. [EMOJI]")
        print("   3. xqshare [EMOJI]")
        return False


# ============================================================================
# [EMOJI]5[EMOJI]
# ============================================================================

def lesson_05_query_positions():
    """[EMOJI]5[EMOJI]"""
    print("\n" + "=" * 80)
    print("[EMOJI]5[EMOJI]")
    print("=" * 80)

    api = easy_xt.get_api()
    ACCOUNT_ID = os.environ.get('QMT_ACCOUNT_ID', '39020958')

    try:
        positions = api.trade.get_positions(ACCOUNT_ID)

        if positions is not None and not positions.empty:
            print("[OK] [EMOJI]")
            print(f"[EMOJI]: {len(positions)} [EMOJI]")
            print()
            print("[EMOJI]:")
            print("-" * 80)
            print(positions.to_string())

            # [EMOJI]
            if len(positions) > 0:
                print()
                print("[EMOJI]:")
                print(f"  [EMOJI]: {len(positions)}")
                if '[EMOJI]' in positions.columns:
                    total_market_value = positions['[EMOJI]'].sum()
                    print(f"  [EMOJI]: ¥{total_market_value:,.2f}")
                if '[EMOJI]' in positions.columns:
                    total_pnl = positions['[EMOJI]'].sum()
                    print(f"  [EMOJI]: ¥{total_pnl:,.2f}")

        else:
            print("[OK] [EMOJI]")

    except Exception as e:
        print(f"[X] [EMOJI]: {e}")


# ============================================================================
# [EMOJI]
# ============================================================================

def main():
    """[EMOJI]"""
    print("\n" + "=" * 80)
    print(" " * 15 + "xqshare [EMOJI]")
    print(" " * 20 + "Mac/Linux [EMOJI]")
    print("=" * 80)
    print()
    print("[EMOJI] @jasonhu [EMOJI] xqshare [EMOJI]")
    print()

    # [EMOJI]1[EMOJI]
    if not lesson_01_environment_setup():
        print("\n[!]  [EMOJI] xqshare [EMOJI]")
        return

    input("\n[EMOJI]2[EMOJI]...")

    # [EMOJI]2[EMOJI]K[EMOJI]
    if not lesson_02_query_daily_kline():
        return

    input("\n[EMOJI]3[EMOJI]...")

    # [EMOJI]3[EMOJI]
    lesson_03_query_date_range()

    input("\n[EMOJI]4[EMOJI]...")

    # [EMOJI]4[EMOJI]
    if not lesson_04_query_account_assets():
        print("\n[TIP] [EMOJI]5[EMOJI]")
    else:
        input("\n[EMOJI]5[EMOJI]...")
        # [EMOJI]5[EMOJI]
        lesson_05_query_positions()

    # [EMOJI]
    print("\n" + "=" * 80)
    print("[OK] [EMOJI]")
    print("=" * 80)
    print()
    print("[EMOJI]")
    print("[OK] xqshare [EMOJI]")
    print("[OK] [EMOJI] xqshare[EMOJI]")
    print("[OK] [EMOJI]K[EMOJI]")
    print("[OK] [EMOJI]")
    print("[OK] [EMOJI]")
    print()
    print("[TIPS] [EMOJI]")
    print("- [EMOJI] 02_[EMOJI].py [EMOJI]")
    print("- [EMOJI] 03_[EMOJI].py [EMOJI]")
    print("- [EMOJI] strategies/ [EMOJI]")
    print()
    print("[SUCCESS] [EMOJI]")
    print()


if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n[!]  [EMOJI]")
    except Exception as e:
        print(f"\n\n[X] [EMOJI]: {e}")
        import traceback
        traceback.print_exc()
    finally:
        print("\n" + "=" * 80)
        print("[EMOJI]")
        print("=" * 80)
        input("\n[EMOJI]...")
