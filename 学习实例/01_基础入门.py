
"""
EasyXT[EMOJI] 01 - [EMOJI]
[EMOJI]EasyXT[EMOJI]
"""

import sys
import os
import pandas as pd
from datetime import datetime

# [EMOJI]Python[EMOJI]
current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)
sys.path.insert(0, parent_dir)

import easy_xt

# [EMOJI]
MOCK_MODE = False

def lesson_01_basic_setup():
    """[EMOJI]1[EMOJI]"""
    print("=" * 60)
    print("[EMOJI]1[EMOJI]EasyXT[EMOJI]")
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
            print("[!] [EMOJI]")
            print("[TIP] [EMOJI]")
            print("[R] [EMOJI]")
            success = True  # [EMOJI]
    except Exception as e:
        print(f"[!] [EMOJI]: {e}")
        print("[R] [EMOJI]")
        success = True  # [EMOJI]
    
    return success

def lesson_02_get_stock_data():
    """[EMOJI]2[EMOJI]"""
    print("\n" + "=" * 60)
    print("[EMOJI]2[EMOJI]")
    print("=" * 60)
    
    api = easy_xt.get_api()
    
    # 1. [EMOJI]
    print("1. [EMOJI](000001.SZ)[EMOJI]10[EMOJI]")
    try:
        data = api.get_price('000001.SZ', count=10)
        print("[OK] [EMOJI]")
        print(f"[EMOJI]: {data.shape}")
        print("[EMOJI]5[EMOJI]:")
        print(data.tail().to_string())
    except Exception as e:
        print(f"[X] [EMOJI]: {e}")
    
    # 2. [EMOJI]
    print("\n2. [EMOJI]")
    try:
        codes = ['000001.SZ', '000002.SZ', '600000.SH']  # [EMOJI]A[EMOJI]
        data = api.get_price(codes, count=5)
        if data is None or data.empty:
            if MOCK_MODE:
                print("[R] [EMOJI]...")
                data = api.mock_get_price(codes, count=5)
            else:
                raise Exception("[EMOJI]")
                
        
        if not data.empty:
            print("[OK] [EMOJI]")
            print(f"[EMOJI]: {data.shape}")
            print("[EMOJI]:")
            print(data.head(10).to_string())
        else:
            print("[X] [EMOJI]")
    except Exception as e:
        print(f"[X] [EMOJI]: {e}")

def lesson_03_different_periods():
    """[EMOJI]3[EMOJI]"""
    print("\n" + "=" * 60)
    print("[EMOJI]3[EMOJI]")
    print("=" * 60)
    
    api = easy_xt.get_api()
    code = '000001.SZ'

    # [EMOJI]
    test_periods = ['1d', '1m', '5m', '15m', '30m', '1h']

    print("[EMOJI]:")
    for period in test_periods:
        print(f"\n[EMOJI] {code} [EMOJI] {period} [EMOJI]:")
        try:
            data = api.get_price(code, period=period, count=5)
            if not data.empty:
                # [EMOJI]
                if 'source' in data.columns:
                    sources = data['source'].unique()
                    source_info = f" ([EMOJI]: {sources[0]})"
                else:
                    source_info = ""

                print(f"[OK] {period} [EMOJI] {len(data)} [EMOJI]{source_info}")
                if 'time' in data.columns:
                    print(f"[EMOJI]: {data['time'].min()} [EMOJI] {data['time'].max()}")
                else:
                    print(f"[EMOJI]: {data.index[0]} [EMOJI] {data.index[-1]}")
                print(f"[EMOJI]: {data['close'].iloc[-1]:.2f}")
            else:
                print(f"[X] {period} [EMOJI]")
        except Exception as e:
            print(f"[X] {period} [EMOJI]: {e}")

    print("\n[TIP] [EMOJI]")
    print("   - [EMOJI] '1d'")
    print("   - [EMOJI] '1m', '5m', '15m', '30m'")
    print("   - [EMOJI] '1h'")
    print("   - [OK] EasyXT [EMOJI]")

def lesson_04_date_range_data():
    """[EMOJI]4[EMOJI]"""
    print("\n" + "=" * 60)
    print("[EMOJI]4[EMOJI]")
    print("=" * 60)
    
    api = easy_xt.get_api()
    code = '000001.SZ'
    
    # 1. [EMOJI]
    print("1. [EMOJI]")
    try:
        from datetime import datetime, timedelta
        end_date = datetime.now()
        start_date = end_date - timedelta(days=7)
        
        start_str = start_date.strftime('%Y-%m-%d')
        end_str = end_date.strftime('%Y-%m-%d')
        
        print(f"[EMOJI] {start_str} [EMOJI] {end_str} [EMOJI]")
        
        data = api.get_price(
            codes=code,
            start=start_str,
            end=end_str,
            period='1d'
        )
        if not data.empty:
            print("[OK] [EMOJI]")
            print(f"[EMOJI]: {len(data)}")
            if 'time' in data.columns:
                print(f"[EMOJI]: {data['time'].min()} [EMOJI] {data['time'].max()}")
            else:
                print(f"[EMOJI]: {data.index[0]} [EMOJI] {data.index[-1]}")
            print("[EMOJI]:")
            print(f"  [EMOJI]: {data['high'].max():.2f}")
            print(f"  [EMOJI]: {data['low'].min():.2f}")
            print(f"  [EMOJI]: {data['close'].mean():.2f}")
        else:
            print("[X] [EMOJI]")
    except Exception as e:
        print(f"[X] [EMOJI]: {e}")
    
    # 2. [EMOJI]
    print("\n2. [EMOJI]")
    try:
        from datetime import datetime, timedelta
        end_date = datetime.now()
        start_date = end_date - timedelta(days=3)
        
        date_formats = [
            (start_date.strftime('%Y-%m-%d'), end_date.strftime('%Y-%m-%d')),  # [EMOJI]
            (start_date.strftime('%Y%m%d'), end_date.strftime('%Y%m%d')),      # [EMOJI]
            (start_date.strftime('%Y/%m/%d'), end_date.strftime('%Y/%m/%d'))   # [EMOJI]
        ]
        
        for start, end in date_formats:
            print(f"[EMOJI]: {start} [EMOJI] {end}")
            try:
                data = api.get_price(code, start=start, end=end)
                if not data.empty:
                    print(f"[OK] [EMOJI] {start} [EMOJI] {len(data)} [EMOJI]")
                else:
                    print(f"[X] [EMOJI] {start} [EMOJI]")
            except Exception as e:
                print(f"[X] [EMOJI] {start} [EMOJI]: {e}")
    except Exception as e:
        print(f"[X] [EMOJI]: {e}")
    
    # 3. [EMOJI]count[EMOJI]
    print("\n3. [EMOJI]count[EMOJI]")
    try:
        data = api.get_price(code, period='1d', count=10)
        if not data.empty:
            print("[OK] count[EMOJI]")
            print(f"[EMOJI]: {len(data)}")
            print("[EMOJI]5[EMOJI]:")
            print(data.tail()[['time', 'code', 'open', 'high', 'low', 'close']].to_string())
        else:
            print("[X] count[EMOJI]")
    except Exception as e:
        print(f"[X] count[EMOJI]: {e}")

def lesson_05_current_price():
    """[EMOJI]5[EMOJI]"""
    print("\n" + "=" * 60)
    print("[EMOJI]5[EMOJI]")
    print("=" * 60)

    api = easy_xt.get_api()

    # 1. [EMOJI]
    print("1. [EMOJI]")
    try:
        current = api.get_current_price('000001.SZ')
        if current is None or current.empty:
            if MOCK_MODE:
                print("[R] [EMOJI]...")
                current = api.mock_get_current_price('000001.SZ')
            else:
                raise Exception("[EMOJI]")

        if not current.empty:
            print("[OK] [EMOJI]")
            print(current.to_string())
        else:
            print("[X] [EMOJI]")
    except Exception as e:
        print(f"[X] [EMOJI]: {e}")

    # 2. [EMOJI]
    print("\n2. [EMOJI]")
    print("[TIP] [EMOJI] get_full_tick [EMOJI]")
    print("[TIP] [EMOJI]")

    try:
        code = '000001.SZ'

        # [EMOJI]easy_xt[EMOJI]get_order_book[EMOJI]
        print(f"\n[EMOJI]easy_xt[EMOJI] {code} [EMOJI]...")
        print("[EMOJI]...")

        order_book = api.get_order_book(code)

        if order_book is not None and not order_book.empty:
            print("[OK] [EMOJI]")

            # [EMOJI]
            data = order_book.iloc[0]

            # [EMOJI]
            has_bid_ask_data = (
                data['bid1'] > 0 or
                data['ask1'] > 0 or
                data['bidVol1'] > 0 or
                data['askVol1'] > 0
            )

            # [EMOJI]
            print("\n" + "="*50)
            print(f"{'[EMOJI]':<10} {data['code']}")
            print(f"{'[EMOJI]':<10} {data['lastPrice']:.2f}")
            print(f"{'[EMOJI]':<10} {data['open']:.2f}")
            print(f"{'[EMOJI]':<10} {data['high']:.2f}")
            print(f"{'[EMOJI]':<10} {data['low']:.2f}")
            print("="*50)

            if has_bid_ask_data:
                # [EMOJI]
                print("\n[EMOJI]")
                print(f"{'[EMOJI]':<8} {'[EMOJI]':<20} {'[EMOJI]':<20}")
                print("-"*50)

                for i in range(1, 6):
                    bid_price = data[f'bid{i}']
                    ask_price = data[f'ask{i}']
                    bid_vol = data[f'bidVol{i}']
                    ask_vol = data[f'askVol{i}']

                    if bid_price > 0 or ask_price > 0:
                        bid_str = f"{bid_price:.2f} ({bid_vol:,.0f} [EMOJI])" if bid_price > 0 else "--"
                        ask_str = f"{ask_price:.2f} ({ask_vol:,.0f} [EMOJI])" if ask_price > 0 else "--"
                        print(f"  {i}[EMOJI]    {bid_str:<20} {ask_str:<20}")
                    else:
                        break

                # [EMOJI]
                bid1 = data['bid1']
                ask1 = data['ask1']
                if bid1 > 0 and ask1 > 0:
                    spread = ask1 - bid1
                    spread_pct = (spread / bid1) * 100
                    print(f"\n[EMOJI]")
                    print(f"[EMOJI]: {spread:.2f} [EMOJI] ({spread_pct:.3f}%)")
                    print(f"[EMOJI]: {(bid1 + ask1) / 2:.2f} [EMOJI]")

                # [EMOJI]
                total_bid_vol = sum(data[f'bidVol{i}'] for i in range(1, 6))
                total_ask_vol = sum(data[f'askVol{i}'] for i in range(1, 6))

                if total_bid_vol > 0 or total_ask_vol > 0:
                    print(f"\n[EMOJI]")
                    print(f"[EMOJI]: {total_bid_vol:,.0f} [EMOJI]")
                    print(f"[EMOJI]: {total_ask_vol:,.0f} [EMOJI]")

                    if total_bid_vol > 0 and total_ask_vol > 0:
                        ratio = total_bid_vol / total_ask_vol
                        print(f"[EMOJI]: {ratio:.2f}")
                        if ratio > 1:
                            print(f"[EMOJI]: {'[EMOJI]' if ratio > 1.2 else '[EMOJI]'}")
                        elif ratio < 1:
                            print(f"[EMOJI]: {'[EMOJI]' if ratio < 0.8 else '[EMOJI]'}")
                        else:
                            print(f"[EMOJI]: [EMOJI]")

                print(f"\n[EMOJI]")
                print(f"[EMOJI]: {', '.join(order_book.columns.tolist())}")

            else:
                # [EMOJI]0[EMOJI]
                print("\n[!] [EMOJI]0[EMOJI]")
                print("\n[EMOJI]")
                print(f"[EMOJI]: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
                print(f"[EMOJI]: {['[EMOJI]', '[EMOJI]', '[EMOJI]', '[EMOJI]', '[EMOJI]', '[EMOJI]', '[EMOJI]'][datetime.now().weekday()]}")

                # [EMOJI]
                current_hour = datetime.now().hour
                current_minute = datetime.now().minute
                current_weekday = datetime.now().weekday()

                is_weekend = current_weekday >= 5  # [EMOJI]
                # [EMOJI]9:30-11:30, 13:00-15:00
                morning = (9 < current_hour < 11) or (current_hour == 9 and current_minute >= 30) or (current_hour == 11 and current_minute <= 30)
                afternoon = (13 <= current_hour < 15)
                is_trading_time = morning or afternoon

                print(f"\n[EMOJI]")
                print(f"[EMOJI]: {'[EMOJI]' if is_weekend else '[EMOJI]'}")
                print(f"[EMOJI]: {'[EMOJI]' if is_trading_time else '[EMOJI]'}")

                if is_weekend:
                    print("\n[TIP] [EMOJI]")
                    print("   [EMOJI]9:30-15:00[EMOJI]")

                elif not is_trading_time:
                    print(f"\n[TIP] [EMOJI]{current_hour:02d}:{current_minute:02d}[EMOJI]")
                    print("   [EMOJI]9:30-15:00[EMOJI]")

                else:
                    print("\n[TIP] [EMOJI]")
                    print("   1. QMT[EMOJI]")
                    print("   2. [EMOJI]")
                    print("   3. [EMOJI]Level2[EMOJI]")
                    print("   4. [EMOJI]3[EMOJI]")
                    print("   5. QMT[EMOJI]tick[EMOJI]")
                    print("\n[EMOJI]")
                    print("   [EMOJI]")
                    print("   1. subscribe_quote() - [EMOJI]")
                    print("   2. QMT[EMOJI]tick[EMOJI]")
                    print("   3. get_full_tick() - [EMOJI]")
                    print("   4. [EMOJI]")

                print("\n[EMOJI]")
                print("   [OK] [EMOJI]9:30-15:00[EMOJI]")
                print("   [OK] [EMOJI]QMT[EMOJI]")
                print("   [OK] [EMOJI]QMT[EMOJI]")
                print("   [OK] [EMOJI]Level2[EMOJI]")
                print("   [OK] [EMOJI]3[EMOJI]2[EMOJI]")

        else:
            print("[!] [EMOJI]")
            print("[TIP] [EMOJI]")
            print("  - QMT[EMOJI]")
            print("  - [EMOJI]")
            print("  - [EMOJI]")

    except Exception as e:
        error_msg = str(e)
        print(f"[!] [EMOJI]: {error_msg}")

        if "xtquant" in error_msg or "xtdata" in error_msg:
            print("\n[TIP] [EMOJI]")
            print("  - xtdata[EMOJI]QMT[EMOJI]")
            print("  - [EMOJI]QMT[EMOJI]")
            print("  - [EMOJI]api.get_current_price()[EMOJI]")
        else:
            print("\n[TIP] [EMOJI]")
            print("  - QMT[EMOJI]")
            print("  - [EMOJI]api.init_data()")
            print("  - [EMOJI]")

    # 3. [EMOJI]
    print("\n3. [EMOJI]")
    try:
        codes = ['000001.SZ', '000002.SZ', '600000.SH', '600036.SH']
        current = api.get_current_price(codes)
        if current is None or current.empty:
            if MOCK_MODE:
                print("[R] [EMOJI]...")
                current = api.mock_get_current_price(codes)
            else:
                raise Exception("[EMOJI]")

        if not current.empty:
            print("[OK] [EMOJI]")
            print("[EMOJI]:")
            # [EMOJI]
            available_columns = ['code', 'price', 'open', 'high', 'low', 'pre_close']
            display_columns = [col for col in available_columns if col in current.columns]
            print(current[display_columns].to_string())

            # [EMOJI]
            if 'price' in current.columns and 'pre_close' in current.columns:
                print("\n[EMOJI]:")
                for _, row in current.iterrows():
                    if row['pre_close'] > 0:
                        change = row['price'] - row['pre_close']
                        change_pct = (change / row['pre_close']) * 100
                        print(f"{row['code']}: {change:+.2f} ({change_pct:+.2f}%)")
        else:
            print("[X] [EMOJI]")
    except Exception as e:
        print(f"[X] [EMOJI]: {e}")

def lesson_06_stock_list():
    """[EMOJI]6[EMOJI]"""
    print("\n" + "=" * 60)
    print("[EMOJI]6[EMOJI]")
    print("=" * 60)

    api = easy_xt.get_api()

    # 1. [EMOJI]A[EMOJI]
    print("1. [EMOJI]A[EMOJI]")
    try:
        stock_list = api.get_stock_list('A[EMOJI]')
        if stock_list:
            print(f"[OK] A[EMOJI] {len(stock_list)} [EMOJI]")
            print("[EMOJI]10[EMOJI]:")
            for i, code in enumerate(stock_list[:10]):
                print(f"  {i+1}. {code}")
        else:
            print("[X] [EMOJI]")
    except Exception as e:
        print(f"[X] [EMOJI]: {e}")
    
    # 2. [EMOJI]300[EMOJI]
    print("\n2. [EMOJI]300[EMOJI]")
    try:
        hs300_list = api.get_stock_list('[EMOJI]300')
        if hs300_list:
            print(f"[OK] [EMOJI]300[EMOJI] {len(hs300_list)} [EMOJI]")
            print("[EMOJI]10[EMOJI]:")
            for i, code in enumerate(hs300_list[:10]):
                print(f"  {i+1}. {code}")
        else:
            print("[X] [EMOJI]300[EMOJI]")
    except Exception as e:
        print(f"[X] [EMOJI]300[EMOJI]: {e}")

def lesson_07_trading_dates():
    """[EMOJI]7[EMOJI]"""
    print("\n" + "=" * 60)
    print("[EMOJI]7[EMOJI]")
    print("=" * 60)
    
    api = easy_xt.get_api()
    
    # 1. [EMOJI]
    print("1. [EMOJI]10[EMOJI]")
    try:
        trading_dates = api.get_trading_dates(market='SH', count=10)
        if trading_dates:
            print("[OK] [EMOJI]")
            print("[EMOJI]10[EMOJI]:")
            for i, date in enumerate(trading_dates[-10:]):
                print(f"  {i+1}. {date}")
        else:
            print("[X] [EMOJI]")
    except Exception as e:
        print(f"[X] [EMOJI]: {e}")
    
    # 2. [EMOJI]
    print("\n2. [EMOJI]")
    try:
        from datetime import datetime
        current_date = datetime.now()
        start_of_month = current_date.replace(day=1)
        
        start_str = start_of_month.strftime('%Y-%m-%d')
        end_str = current_date.strftime('%Y-%m-%d')
        
        print(f"[EMOJI] {start_str} [EMOJI] {end_str} [EMOJI]")
        
        trading_dates = api.get_trading_dates(
            market='SH',
            start=start_str,
            end=end_str
        )
        if trading_dates:
            print(f"[OK] [EMOJI] {len(trading_dates)} [EMOJI]")
            print("[EMOJI]:")
            for date in trading_dates:
                print(f"  {date}")
        else:
            print("[X] [EMOJI]")
    except Exception as e:
        print(f"[X] [EMOJI]: {e}")
    
    # 3. [EMOJI]30[EMOJI]
    print("\n3. [EMOJI]30[EMOJI]")
    try:
        trading_dates = api.get_trading_dates(market='SH', count=30)
        if trading_dates:
            print(f"[OK] [EMOJI]30[EMOJI]")
            print("[EMOJI]10[EMOJI]:")
            for i, date in enumerate(trading_dates[-10:]):
                print(f"  {i+1}. {date}")
            print(f"... [EMOJI] {len(trading_dates)} [EMOJI]")
        else:
            print("[X] [EMOJI]")
    except Exception as e:
        print(f"[X] [EMOJI]: {e}")

def main():
    """[EMOJI]"""
    print("[COURSE] EasyXT[EMOJI]")
    print("[EMOJI]EasyXT[EMOJI]")
    print("[EMOJI]xtquant[EMOJI]")
    
    # [EMOJI]
    lessons = [
        lesson_01_basic_setup,
        lesson_02_get_stock_data,
        lesson_03_different_periods,
        lesson_04_date_range_data,
        lesson_05_current_price,
        lesson_06_stock_list,
        lesson_07_trading_dates
    ]
    
    for lesson in lessons:
        try:
            lesson()
            if not (len(sys.argv) > 1 and '--auto' in sys.argv):
                input("\n[EMOJI]...")
            else:
                print(f"\n[OK] [EMOJI]{lessons.index(lesson)+1}[EMOJI]...")
        except KeyboardInterrupt:
            print("\n\n[EMOJI]")
            break
        except Exception as e:
            print(f"\n[EMOJI]: {e}")
            input("[EMOJI]...")
    
    print("\n[EMOJI] [EMOJI]")
    print("\n[EMOJI]:")
    print("[OK] [EMOJI]1[EMOJI]: [EMOJI]")
    print("[OK] [EMOJI]2[EMOJI]: [EMOJI]")
    print("[OK] [EMOJI]3[EMOJI]: [EMOJI]")
    print("[OK] [EMOJI]4[EMOJI]: [EMOJI]")
    print("[OK] [EMOJI]5[EMOJI]: [EMOJI]")
    print("[OK] [EMOJI]6[EMOJI]: [EMOJI]")
    print("[OK] [EMOJI]7[EMOJI]: [EMOJI]")

    print("\n[EMOJI]")
    print("- 02_[EMOJI].py - [EMOJI]")
    print("- 03_[EMOJI].py - [EMOJI]")
    print("- 04_[EMOJI].py - [EMOJI]")

if __name__ == "__main__":
    main()