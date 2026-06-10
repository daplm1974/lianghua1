"""
EasyFactor [EMOJI] - DuckDB[EMOJI]

[EMOJI]EasyFactor[EMOJI]DuckDB[EMOJI]
[EMOJI]
"""

import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from easy_xt.factor_library import EasyFactor, create_easy_factor, create_duckdb_factor
import pandas as pd

print("=" * 90)
print(" " * 30 + "EasyFactor DuckDB[EMOJI]")
print("=" * 90)

# ============================================================
# [EMOJI]DuckDB[EMOJI]
# ============================================================
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

# ============================================================
# [EMOJI]1[EMOJI]EasyFactor
# ============================================================

print("\n" + "=" * 90)
print("[[EMOJI]1] [EMOJI]EasyFactor")
print("=" * 90)

print("\n[EMOJI]")
print("""
# [EMOJI]1[EMOJI]EasyFactor[EMOJI]
ef = EasyFactor(duckdb_path='D:/StockData/stock_data.ddb')

# [EMOJI]2[EMOJI]
ef = create_easy_factor('D:/StockData/stock_data.ddb')

# [EMOJI]3[EMOJI]
ef = create_duckdb_factor('D:/StockData/stock_data.ddb')
""")

print("\n[EMOJI]")
try:
    ef = create_easy_factor(DUCKDB_PATH)
    print("[OK] EasyFactor[EMOJI]")
except Exception as e:
    print(f"[FAIL] {e}")
    print("\n[[EMOJI]] [EMOJI]DuckDB[EMOJI]DUCKDB_PATH[EMOJI]")
    exit(1)

# ============================================================
# [EMOJI]2[EMOJI]
# ============================================================

print("\n\n" + "=" * 90)
print("[[EMOJI]2] [EMOJI]")
print("=" * 90)

print("\n[EMOJI]")
print("""
# [EMOJI]
all_stocks = ef.get_stock_list()

# [EMOJI]10[EMOJI]
stocks = ef.get_stock_list(limit=10)
""")

print("\n[EMOJI]")
try:
    stocks_df = ef.get_stock_list(limit=10)
    if not stocks_df.empty:
        stock_list = stocks_df['stock_code'].tolist()
        print(f"[OK] [EMOJI]10[EMOJI]: {', '.join(stock_list)}")
    else:
        print("[INFO] [EMOJI]")
except Exception as e:
    print(f"[FAIL] {e}")

# ============================================================
# [EMOJI]3[EMOJI]
# ============================================================

print("\n\n" + "=" * 90)
print("[[EMOJI]3] [EMOJI]")
print("=" * 90)

print("\n[EMOJI]")
print("""
# [EMOJI]
df = ef.get_market_data_ex(
    stock_code='000001.SZ',
    start_time='2024-01-01',
    end_time='2024-11-30',
    period='daily'
)
""")

print("\n[EMOJI]")
try:
    df = ef.get_market_data_ex('000001.SZ', '2024-01-01', '2024-11-30', period='daily')
    if not df.empty:
        print(f"[OK] [EMOJI] {len(df)} [EMOJI]")
        print("\n[EMOJI]3[EMOJI]")
        print(df[['Date', 'Open', 'High', 'Low', 'Close']].tail(3))
    else:
        print("[FAIL] [EMOJI]")
except Exception as e:
    print(f"[FAIL] {e}")

# ============================================================
# [EMOJI]4[EMOJI]
# ============================================================

print("\n\n" + "=" * 90)
print("[[EMOJI]4] [EMOJI]")
print("=" * 90)

print("\n[EMOJI]")
print("""
# [EMOJI]20[EMOJI]
momentum = ef.get_factor('000001.SZ', 'momentum_20d', '2024-01-01', '2024-11-30')

# [EMOJI]RSI
rsi = ef.get_factor('000001.SZ', 'rsi', '2024-01-01', '2024-11-30')

# [EMOJI]
volatility = ef.get_factor('000001.SZ', 'volatility_20d', '2024-01-01', '2024-11-30')
""")

print("\n[EMOJI]")
try:
    # [EMOJI]
    momentum = ef.get_factor('000001.SZ', 'momentum_20d', '2024-01-01', '2024-11-30')
    if not momentum.empty:
        val = momentum['momentum_20d'].iloc[-1]
        print(f"[OK] 20[EMOJI]: {val:+.2%}")

    # RSI
    rsi = ef.get_factor('000001.SZ', 'rsi', '2024-01-01', '2024-11-30')
    if not rsi.empty:
        val = rsi['rsi'].iloc[-1]
        print(f"[OK] RSI[EMOJI]: {val:.2f}")

    # [EMOJI]
    volatility = ef.get_factor('000001.SZ', 'volatility_20d', '2024-01-01', '2024-11-30')
    if not volatility.empty:
        val = volatility['volatility_20d'].iloc[-1]
        print(f"[OK] [EMOJI]: {val:.2%}")

except Exception as e:
    print(f"[FAIL] {e}")

# ============================================================
# [EMOJI]5[EMOJI]
# ============================================================

print("\n\n" + "=" * 90)
print("[[EMOJI]5] [EMOJI]")
print("=" * 90)

print("\n[EMOJI]")
print("""
# [EMOJI]
factors = ef.get_factor_batch(
    stock_list=['000001.SZ', '600000.SH', '600519.SH'],
    factor_names=['momentum_20d', 'rsi', 'volatility_20d'],
    start_date='2024-01-01',
    end_date='2024-11-30'
)
""")

print("\n[EMOJI]")
try:
    factors = ef.get_factor_batch(
        stock_list=['000001.SZ', '600000.SH', '600519.SH'],
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

except Exception as e:
    print(f"[FAIL] {e}")

# ============================================================
# [EMOJI]6[EMOJI]DuckDB[EMOJI]
# ============================================================

print("\n\n" + "=" * 90)
print("[[EMOJI]6] [EMOJI] - DuckDB[EMOJI]")
print("=" * 90)

print("\n[EMOJI]")
print("""
# [EMOJI]
stock_list = ['000001.SZ', '000002.SZ', '600000.SH', '600519.SH']
results = ef.analyze_batch(
    stock_list=stock_list,
    start_date='2024-01-01',
    end_date='2024-11-30',
    factors=['momentum', 'volatility', 'technical', 'score']
)

# [EMOJI]
print(results['score'])
""")

print("\n[EMOJI]")
try:
    stock_list = ['000001.SZ', '000002.SZ', '600000.SH', '600519.SH']
    results = ef.analyze_batch(stock_list, '2024-01-01', '2024-11-30')

    if 'score' in results and not results['score'].empty:
        print("[OK] [EMOJI]\n")
        print("[EMOJI]")
        scores_sorted = results['score'].sort_values('score', ascending=False)
        for stock, row in scores_sorted.iterrows():
            print(f"  {stock:<12} [EMOJI]:{row['score']:>6.2f}/{row['max_score']:.0f}  {row['rating']}[EMOJI]")

except Exception as e:
    print(f"[FAIL] {e}")

# ============================================================
# [EMOJI]7[EMOJI]
# ============================================================

print("\n\n" + "=" * 90)
print("[[EMOJI]7] [EMOJI]")
print("=" * 90)

print("\n[EMOJI]")
print("""
# [EMOJI]
stock_list = ['000001.SZ', '600000.SH', '600519.SH', '000858.SZ']
scores = ef.get_comprehensive_score(stock_list)

# [EMOJI]
print(scores.sort_values('score', ascending=False))
""")

print("\n[EMOJI]")
try:
    stock_list = ['000001.SZ', '600000.SH', '600519.SH', '000858.SZ']
    scores = ef.get_comprehensive_score(stock_list)

    if not scores.empty:
        print("[OK] [EMOJI]\n")
        print("[EMOJI]")
        for idx, (stock, row) in enumerate(scores.sort_values('score', ascending=False).iterrows(), 1):
            rating_stars = "*" * (5 if row['rating'] == 'A' else 4 if row['rating'] == 'B' else 3)
            print(f"  {idx}. {stock:<12} {row['rating']}[EMOJI]  {rating_stars}  [EMOJI]:{row['score']:>6.2f}")

except Exception as e:
    print(f"[FAIL] {e}")

# ============================================================
# [EMOJI]
# ============================================================

print("\n\n" + "=" * 90)
print(" " * 25 + "[EMOJI]50+[EMOJI]")
print("=" * 90)

factor_list = """
[EMOJI]50+[EMOJI]

[EMOJI]
  momentum_5d    - 5[EMOJI]
  momentum_10d   - 10[EMOJI]
  momentum_20d   - 20[EMOJI]
  momentum_60d   - 60[EMOJI]
  momentum_vol   - [EMOJI]

[EMOJI]
  reversal_short - [EMOJI]5[EMOJI]
  reversal_mid   - [EMOJI]20[EMOJI]
  reversal_long  - [EMOJI]60[EMOJI]

[EMOJI]
  volatility_20d   - 20[EMOJI]
  volatility_60d   - 60[EMOJI]
  volatility_120d  - 120[EMOJI]
  max_drawdown     - [EMOJI]

[EMOJI]
  ma5_signal   - 5[EMOJI]
  ma10_signal  - 10[EMOJI]
  ma20_signal  - 20[EMOJI]
  ma60_signal  - 60[EMOJI]
  ma_trend     - [EMOJI]

[EMOJI]
  rsi       - [EMOJI]
  macd      - MACD[EMOJI]
  kdj       - [EMOJI]
  atr       - [EMOJI]
  obv       - [EMOJI]
  bollinger - [EMOJI]

[EMOJI]
  volume_ratio      - [EMOJI]
  turnover_rate     - [EMOJI]
  amplitude         - [EMOJI]
  price_volume_trend - [EMOJI]

[EMOJI]

[EMOJI]
  pe_ttm     - [EMOJI]
  pb         - [EMOJI]
  ps         - [EMOJI]
  pcf        - [EMOJI]
  market_cap - [EMOJI]

[EMOJI]
  roe         - [EMOJI]
  roa         - [EMOJI]
  gross_margin - [EMOJI]
  net_margin   - [EMOJI]
  debt_ratio   - [EMOJI]

[EMOJI]
  revenue_growth - [EMOJI]
  profit_growth  - [EMOJI]
  eps_growth     - EPS[EMOJI]
"""

print(factor_list)

# ============================================================
# [EMOJI]
# ============================================================

print("\n" + "=" * 90)
print(" " * 35 + "[EMOJI]")
print("=" * 90)

best_practices = """
[EMOJI]1[EMOJI]
  ef = EasyFactor(duckdb_path='D:/StockData/stock_data.ddb')

[EMOJI]2[EMOJI]
  momentum = ef.get_factor('000001.SZ', 'momentum_20d', '2024-01-01', '2024-11-30')

[EMOJI]3[EMOJI]
  results = ef.analyze_batch(
      stock_list=['000001.SZ', '600000.SH', ...],
      start_date='2024-01-01',
      end_date='2024-11-30',
      factors=['momentum', 'volatility', 'score']
  )

[EMOJI]4[EMOJI]
  scores = ef.get_comprehensive_score(stock_list)
  a_stocks = scores[scores['rating'] == 'A']

[EMOJI]5[EMOJI]
  all_stocks = ef.get_stock_list()
  results = ef.analyze_batch(all_stocks[:100], '2024-01-01', '2024-11-30')
"""

print(best_practices)

# ============================================================
# [EMOJI]
# ============================================================

print("\n" + "=" * 90)
print(" " * 30 + "[EMOJI]")
print("=" * 90)

summary = """
EasyFactor DuckDB[EMOJI]

1. [EMOJI]
   - [EMOJI]
   - [EMOJI]
   - [EMOJI]

2. [EMOJI]API[EMOJI]
   - [EMOJI]DuckDB[EMOJI]
   - [EMOJI]
   - [EMOJI]

3. [EMOJI]
   - 50+[EMOJI]
   - [EMOJI]
   - [EMOJI]

4. [EMOJI]
   - [EMOJI]get_factor()
   - [EMOJI]analyze_batch()
   - [EMOJI]get_comprehensive_score()

[EMOJI]
- DuckDB[EMOJI]
- [EMOJI]10[EMOJI]
- [EMOJI]analyze_batch()[EMOJI]
"""

print(summary)

print("\n" + "=" * 90)
print(" " * 30 + "[EMOJI]")
print("=" * 90)
