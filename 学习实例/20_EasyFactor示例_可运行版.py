"""
EasyFactor [EMOJI] - [EMOJI] (DuckDB[EMOJI])

[EMOJI]EasyFactor[EMOJI]

[EMOJI]
# [EMOJI]1[EMOJI]easy_xt[EMOJI]
from easy_xt.factor_library import EasyFactor, create_easy_factor

# [EMOJI]2[EMOJI]factors[EMOJI]
from factors import EasyFactor, create_easy_factor

# [EMOJI]
from factors.pricing import FamaFrenchCalculator
from factors.analysis import ICAnalyzer, GroupBacktester
from factors.custom import SmallCapQualityFactor
"""

import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

# [EMOJI]
from easy_xt.factor_library import EasyFactor, create_easy_factor

# [EMOJI]
# from factors.pricing import FamaFrenchCalculator
# from factors.analysis import ICAnalyzer
# from factors.custom import SmallCapQualityFactor

import pandas as pd

print("=" * 90)
print(" " * 30 + "EasyFactor [EMOJI] (DuckDB[EMOJI])")
print("=" * 90)

# [EMOJI]DuckDB[EMOJI]
# DuckDB[EMOJI]
def _detect_duckdb_path():
    candidates = [
        'D:/StockData/stock_data.ddb',
        'C:/StockData/stock_data.ddb',
        'E:/StockData/stock_data.ddb',
        './data/stock_data.ddb',
    ]
    for path in candidates:
        if os.path.exists(path):
            return path
    env = os.environ.get('DUCKDB_PATH')
    return env if env else candidates[0]

DUCKDB_PATH = _detect_duckdb_path()

# [EMOJI]EasyFactor[EMOJI]
print("\n[[EMOJI]1] [EMOJI]EasyFactor[EMOJI]...")
try:
    ef = create_easy_factor(DUCKDB_PATH)
    print("[OK] EasyFactor[EMOJI]\n")
except Exception as e:
    print(f"[FAIL] EasyFactor[EMOJI]: {e}")
    print("\n[[EMOJI]] [EMOJI]DUCKDB_PATH[EMOJI]")
    exit(1)

# [EMOJI]1[EMOJI]
print("=" * 90)
print("[[EMOJI]2] [EMOJI]")
print("=" * 90)
try:
    df = ef.get_market_data_ex(
        stock_code='000001.SZ',
        start_time='2024-01-01',
        end_time='2024-11-30',
        period='daily'
    )

    if not df.empty:
        print(f"[OK] [EMOJI] {len(df)} [EMOJI]\n")
        print("[EMOJI]5[EMOJI]")
        # [EMOJI]
        print(df[['date', 'open', 'high', 'low', 'close', 'volume']].tail())
    else:
        print("[FAIL] [EMOJI]")
except Exception as e:
    print(f"[FAIL] [EMOJI]: {e}")

# [EMOJI]2[EMOJI]
print("\n" + "=" * 90)
print("[[EMOJI]3] [EMOJI]")
print("=" * 90)
try:
    momentum = ef.get_factor('000001.SZ', 'momentum_20d', '2024-01-01', '2024-11-30')

    if not momentum.empty:
        val = momentum['momentum_20d'].iloc[-1]
        print(f"[OK] 20[EMOJI]: {val:+.2%}")
        if val > 0:
            print(f"     [EMOJI]")
        else:
            print(f"     [EMOJI]\n")
    else:
        print("[FAIL] [EMOJI]\n")
except Exception as e:
    print(f"[FAIL] [EMOJI]: {e}\n")

# [EMOJI]3[EMOJI]RSI
print("=" * 90)
print("[[EMOJI]4] [EMOJI]RSI[EMOJI]")
print("=" * 90)
try:
    rsi = ef.get_factor('000001.SZ', 'rsi', '2024-01-01', '2024-11-30')

    if not rsi.empty:
        val = rsi['rsi'].iloc[-1]
        print(f"[OK] RSI[EMOJI]: {val:.2f}")
        if val > 70:
            print(f"     [EMOJI]\n")
        elif val < 30:
            print(f"     [EMOJI]\n")
        else:
            print(f"     [EMOJI]\n")
    else:
        print("[FAIL] RSI[EMOJI]\n")
except Exception as e:
    print(f"[FAIL] [EMOJI]RSI[EMOJI]: {e}\n")

# [EMOJI]4[EMOJI]
print("=" * 90)
print("[[EMOJI]5] [EMOJI]")
print("=" * 90)
try:
    volatility = ef.get_factor('000001.SZ', 'volatility_20d', '2024-01-01', '2024-11-30')

    if not volatility.empty:
        val = volatility['volatility_20d'].iloc[-1]
        print(f"[OK] [EMOJI]: {val:.2%}")
        if val < 0.2:
            print(f"     [EMOJI]\n")
        elif val < 0.4:
            print(f"     [EMOJI]\n")
        else:
            print(f"     [EMOJI]\n")
    else:
        print("[FAIL] [EMOJI]\n")
except Exception as e:
    print(f"[FAIL] [EMOJI]: {e}\n")

# [EMOJI]5[EMOJI]
print("=" * 90)
print("[[EMOJI]6] [EMOJI]")
print("=" * 90)
try:
    test_stocks = ['000001.SZ', '600000.SH', '600519.SH']
    factors = ef.get_factor_batch(
        stock_list=test_stocks,
        factor_names=['momentum_20d', 'rsi', 'volatility_20d'],
        start_date='2024-01-01',
        end_date='2024-11-30'
    )

    if 'momentum_20d' in factors and not factors['momentum_20d'].empty:
        print("[OK] [EMOJI]\n")
        print("20[EMOJI]")
        momentum_df = factors['momentum_20d'].sort_values('momentum_20d', ascending=False)
        for _, row in momentum_df.iterrows():
            print(f"  {row['stock_code']}: {row['momentum_20d']:+.2%}")
        print()
    else:
        print("[FAIL] [EMOJI]\n")
except Exception as e:
    print(f"[FAIL] [EMOJI]: {e}\n")

# [EMOJI]6[EMOJI]
print("=" * 90)
print("[[EMOJI]7] [EMOJI]")
print("=" * 90)
try:
    stocks = ef.get_stock_list()

    if not stocks.empty:
        print(f"[OK] [EMOJI] {len(stocks)} [EMOJI]\n")
        print("[EMOJI]")
        print(stocks)
    else:
        print("[FAIL] [EMOJI]\n")
except Exception as e:
    print(f"[FAIL] [EMOJI]: {e}\n")

# [EMOJI]
print("\n" + "=" * 90)
print(" " * 35 + "[EMOJI]")
print("=" * 90)

print("""
EasyFactor DuckDB[EMOJI] [EMOJI]

1. get_market_data_ex()  - [EMOJI]
   [EMOJI]/[EMOJI]/[EMOJI]
   [EMOJI]stock_code, start_time, end_time, period
   [EMOJI] YYYY-MM-DD[EMOJI]2024-01-01[EMOJI]

2. get_factor()          - [EMOJI]
   [EMOJI]
   - [EMOJI]momentum_5d, momentum_10d, momentum_20d, momentum_60d
   - [EMOJI]reversal_short, reversal_mid, reversal_long
   - [EMOJI]volatility_20d, volatility_60d, volatility_120d
   - [EMOJI]rsi, macd, kdj, atr, obv, bollinger
   - [EMOJI]volume_ratio, turnover_rate, amplitude

3. get_factor_batch()    - [EMOJI]
   [EMOJI]stock_list, factor_names, start_date, end_date

4. analyze_batch()       - [EMOJI]
   [EMOJI]stock_list, start_date, end_date, factors

5. get_stock_list()      - [EMOJI]

6. get_comprehensive_score() - [EMOJI]
   [EMOJI]score[EMOJI]rating[EMOJI]A/B/C/D[EMOJI]rank[EMOJI]

[EMOJI]
    # [EMOJI]
    ef = EasyFactor(duckdb_path='D:/StockData/stock_data.ddb')

    # [EMOJI]YYYY-MM-DD[EMOJI]
    df = ef.get_market_data_ex('000001.SZ', '2024-01-01', '2024-12-31')

    # [EMOJI]
    momentum = ef.get_factor('000001.SZ', 'momentum_20d', '2024-01-01', '2024-12-31')
    rsi = ef.get_factor('000001.SZ', 'rsi', '2024-01-01', '2024-12-31')

    # [EMOJI]
    results = ef.analyze_batch(
        stock_list=['000001.SZ', '600000.SH'],
        start_date='2024-01-01',
        end_date='2024-12-31'
    )

[EMOJI]
- [EMOJI]DuckDB[EMOJI]
- [EMOJI]
- [EMOJI]50+[EMOJI]
- [EMOJI]
""")

print("=" * 90)
print(" " * 30 + "[EMOJI]")
print("=" * 90)
