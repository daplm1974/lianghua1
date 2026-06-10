"""
EasyFactor [EMOJI]

[EMOJI]EasyFactor[EMOJI]

[EMOJI]qstock[EMOJI]
- [EMOJI]/[EMOJI]90[EMOJI]+387[EMOJI]
- [EMOJI]
- [EMOJI]5175[EMOJI]

[EMOJI]DuckDB[EMOJI]
- 767[EMOJI]2015-2026[EMOJI]
- [EMOJI]29[EMOJI]
- [EMOJI]

[EMOJI]factors[EMOJI]
- [EMOJI]Fama-French[EMOJI]/[EMOJI]
- [EMOJI]IC/IR[EMOJI]
- [EMOJI]

[EMOJI]
# [EMOJI]1[EMOJI]easy_xt[EMOJI]
from easy_xt.factor_library import create_easy_factor
from easy_xt.fundamental_enhanced import FundamentalAnalyzerEnhanced

# [EMOJI]2[EMOJI]factors[EMOJI]
from factors import EasyFactor, FundamentalAnalyzerEnhanced
from factors.pricing import FamaFrenchCalculator
from factors.analysis import ICAnalyzer, GroupBacktester
from factors.custom import SmallCapQualityFactor
"""

import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

# [EMOJI]
from easy_xt.factor_library import create_easy_factor
from easy_xt.fundamental_enhanced import FundamentalAnalyzerEnhanced, get_enhanced_fundamental_factors, get_batch_enhanced_factors

# [EMOJI]
# from factors import EasyFactor, FundamentalAnalyzerEnhanced

import pandas as pd

print("=" * 90)
print(" " * 20 + "EasyFactor [EMOJI]")
print("=" * 90)

# [EMOJI]
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
print("\n[[EMOJI]1] [EMOJI]EasyFactor...")
print("-" * 90)

try:
    ef = create_easy_factor(DUCKDB_PATH, enable_extended_modules=True)
    print("[OK] EasyFactor[EMOJI]\n")
except Exception as e:
    print(f"[FAIL] {e}")
    exit(1)

# ============================================================
# [EMOJI]1[EMOJI]/[EMOJI]qstock[EMOJI]
# ============================================================

print("\n" + "=" * 90)
print("[[EMOJI]1] [EMOJI]/[EMOJI]")
print("=" * 90)

print("\n[EMOJI]")
print("- [EMOJI]90[EMOJI]")
print("- [EMOJI]387[EMOJI]")
print("- [EMOJI]200-400x[EMOJI]")

print("\n[EMOJI]")
print("""
# [EMOJI]TOP20
industry_flow = ef.get_ths_industry_money_flow(top_n=20, use_cache=True)
print(industry_flow)

# [EMOJI]TOP20
concept_flow = ef.get_ths_concept_money_flow(top_n=20, use_cache=True)
print(concept_flow)

# [EMOJI]
# result = ef.update_ths_money_flow()
# print(result)
""")

print("\n[EMOJI]")
try:
    # [EMOJI]
    industry_flow = ef.get_ths_industry_money_flow(top_n=10, use_cache=True)
    if not industry_flow.empty:
        print(f"[OK] [EMOJI] {len(industry_flow)} [EMOJI]")
        print("\n[EMOJI]TOP10[EMOJI]")
        print(industry_flow.to_string(index=False))
    else:
        print("[INFO] [EMOJI]")
except Exception as e:
    print(f"[INFO] {e}")

try:
    # [EMOJI]
    concept_flow = ef.get_ths_concept_money_flow(top_n=10, use_cache=True)
    if not concept_flow.empty:
        print(f"\n[OK] [EMOJI] {len(concept_flow)} [EMOJI]")
        print("\n[EMOJI]TOP10[EMOJI]")
        print(concept_flow.to_string(index=False))
except Exception as e:
    print(f"[INFO] {e}")

# ============================================================
# [EMOJI]2[EMOJI]qstock[EMOJI]
# ============================================================

print("\n\n" + "=" * 90)
print("[[EMOJI]2] [EMOJI]")
print("=" * 90)

print("\n[EMOJI]")
print("- [EMOJI]2,616[EMOJI]")
print("- [EMOJI]86[EMOJI]")
print("- [EMOJI]2,767[EMOJI]")

print("\n[EMOJI]")
print("""
# [EMOJI]30[EMOJI]
north_flow = ef.get_north_money_flow(days=30, use_cache=True)
print(north_flow)

# [EMOJI]TOP20
north_sector = ef.get_north_money_sector(top_n=20)
print(north_sector)

# [EMOJI]TOP20
north_stock = ef.get_north_money_stock(top_n=20)
print(north_stock)

# [EMOJI]
north_single = ef.get_north_money_stock(stock_code='600050')
print(north_single)
""")

print("\n[EMOJI]")
try:
    # [EMOJI]
    north_flow = ef.get_north_money_flow(days=10, use_cache=True)
    if not north_flow.empty:
        print(f"[OK] [EMOJI] {len(north_flow)} [EMOJI]")
        print("\n[EMOJI]10[EMOJI]")
        print(north_flow.to_string(index=False))
    else:
        print("[INFO] [EMOJI]")
except Exception as e:
    print(f"[INFO] {e}")

try:
    # [EMOJI]
    north_sector = ef.get_north_money_sector(top_n=10)
    if not north_sector.empty:
        print(f"\n[OK] [EMOJI] {len(north_sector)} [EMOJI]")
        print("\n[EMOJI]TOP10[EMOJI]")
        print(north_sector.to_string(index=False))
except Exception as e:
    print(f"[INFO] {e}")

try:
    # [EMOJI]
    north_stock = ef.get_north_money_stock(top_n=10)
    if not north_stock.empty:
        print(f"\n[OK] [EMOJI] {len(north_stock)} [EMOJI]")
        print("\n[EMOJI]TOP10[EMOJI]")
        print(north_stock.to_string(index=False))
except Exception as e:
    print(f"[INFO] {e}")

# ============================================================
# [EMOJI]3[EMOJI]qstock[EMOJI]
# ============================================================

print("\n\n" + "=" * 90)
print("[[EMOJI]3] [EMOJI]")
print("=" * 90)

print("\n[EMOJI]")
print("- [EMOJI]5,175[EMOJI]")
print("- [EMOJI]")
print("- [EMOJI]")

print("\n[EMOJI]")
print("""
# [EMOJI]TOP20
stock_flow = ef.get_ths_stock_money_flow(top_n=20, use_cache=True)
print(stock_flow)

# [EMOJI]
single_flow = ef.get_ths_stock_money_flow(stock_code='000001', use_cache=True)
print(single_flow)
""")

print("\n[EMOJI]")
try:
    # [EMOJI]
    stock_flow = ef.get_ths_stock_money_flow(top_n=10, use_cache=True)
    if not stock_flow.empty:
        print(f"[OK] [EMOJI] {len(stock_flow)} [EMOJI]")
        print("\n[EMOJI]TOP10[EMOJI]")
        print(stock_flow.to_string(index=False))
    else:
        print("[INFO] [EMOJI]")
except Exception as e:
    print(f"[INFO] {e}")

try:
    # [EMOJI]
    single_flow = ef.get_ths_stock_money_flow(stock_code='000001', use_cache=True)
    if not single_flow.empty:
        print(f"\n[OK] [EMOJI]000001[EMOJI]")
        print(single_flow.to_string(index=False))
except Exception as e:
    print(f"[INFO] {e}")

# ============================================================
# [EMOJI]4[EMOJI]DuckDB[EMOJI]
# ============================================================

print("\n\n" + "=" * 90)
print("[[EMOJI]4] [EMOJI]")
print("=" * 90)

print("\n[EMOJI]")
print("- [EMOJI]DuckDB[EMOJI]767[EMOJI]")
print("- [EMOJI]2015-10-26 [EMOJI] 2026-02-02")
print("- [EMOJI]5,190[EMOJI]")
print("- [EMOJI]29[EMOJI]5[EMOJI]")

print("\n[EMOJI]")
print("""
# [EMOJI]
analyzer = FundamentalAnalyzerEnhanced(ef.duckdb_reader)

# [EMOJI]29[EMOJI]
df = analyzer.get_all_fundamental_factors('000001.SZ')
print(df)

# [EMOJI]
stock_list = ['000001.SZ', '000002.SZ', '600000.SH', '600036.SH']
df_batch = analyzer.get_batch_fundamental_factors(stock_list)
print(df_batch)

# [EMOJI]
df = get_enhanced_fundamental_factors('000001.SZ', ef.duckdb_reader)
df_batch = get_batch_enhanced_factors(stock_list, ef.duckdb_reader)
""")

print("\n[EMOJI]")
try:
    # [EMOJI]
    analyzer = FundamentalAnalyzerEnhanced(ef.duckdb_reader)

    # [EMOJI]
    df = analyzer.get_all_fundamental_factors('000001.SZ')
    if not df.empty:
        print(f"[OK] [EMOJI] {len(df.columns)} [EMOJI]\n")

        # [EMOJI]
        print("[[EMOJI]]")
        valuation_cols = [col for col in df.columns if any(k in col for k in ['price_to', 'percentile', 'dist_from'])]
        if valuation_cols:
            print(df[valuation_cols].to_string())

        print("\n[[EMOJI]]")
        momentum_cols = [col for col in df.columns if 'momentum' in col or 'rsi' in col]
        if momentum_cols:
            print(df[momentum_cols].to_string())

        print("\n[[EMOJI]]")
        volatility_cols = [col for col in df.columns if 'volatility' in col or 'atr' in col]
        if volatility_cols:
            print(df[volatility_cols].to_string())

    else:
        print("[INFO] [EMOJI]")
except Exception as e:
    print(f"[INFO] {e}")
    import traceback
    traceback.print_exc()

try:
    # [EMOJI]
    stock_list = ['000001.SZ', '000002.SZ', '600000.SH', '600036.SH']
    df_batch = analyzer.get_batch_fundamental_factors(stock_list)
    if not df_batch.empty:
        print(f"\n[OK] [EMOJI] {len(df_batch)} [EMOJI]")

        # [EMOJI]
        key_factors = [
            'momentum_20d', 'momentum_60d', 'momentum_252d',
            'volatility_20d', 'volatility_60d',
            'price_to_ma60', 'price_percentile',
            'rsi_14'
        ]
        available_factors = [f for f in key_factors if f in df_batch.columns]

        if available_factors:
            print("\n[EMOJI]")
            print(df_batch[available_factors].to_string())
except Exception as e:
    print(f"[INFO] {e}")

# ============================================================
# [EMOJI]5[EMOJI]
# ============================================================

print("\n\n" + "=" * 90)
print("[[EMOJI]5] [EMOJI] + [EMOJI]")
print("=" * 90)

print("\n[EMOJI]")
print("[EMOJI]")
print("[EMOJI]")

print("\n[EMOJI]")
print("""
# 1. [EMOJI]TOP20
stock_flow = ef.get_ths_stock_money_flow(top_n=20, use_cache=True)

# 2. [EMOJI]
stock_list = stock_flow['[EMOJI]'].tolist()
df_factors = get_batch_enhanced_factors(stock_list, ef.duckdb_reader)

# 3. [EMOJI]
#    - [EMOJI]>0[EMOJI]20[EMOJI]
#    - RSI < 70[EMOJI]
#    - [EMOJI] < 0.3[EMOJI]

df_selected = df_factors[
    (df_factors['momentum_20d'] > 0) &
    (df_factors['rsi_14'] < 70) &
    (df_factors['volatility_20d'] < 0.3)
]

print("[EMOJI]")
print(df_selected)
""")

print("\n[EMOJI]")
try:
    # [EMOJI]
    stock_flow = ef.get_ths_stock_money_flow(top_n=20, use_cache=True)
    if not stock_flow.empty:
        # [EMOJI]
        stock_list = stock_flow['[EMOJI]'].tolist()[:10]  # [EMOJI]10[EMOJI]
        df_factors = get_batch_enhanced_factors(stock_list, ef.duckdb_reader)

        if not df_factors.empty and all(col in df_factors.columns for col in ['momentum_20d', 'rsi_14', 'volatility_20d']):
            # [EMOJI]
            df_selected = df_factors[
                (df_factors['momentum_20d'] > 0) &
                (df_factors['rsi_14'] < 70) &
                (df_factors['volatility_20d'] < 0.3)
            ]

            if not df_selected.empty:
                print(f"[OK] [EMOJI] {len(df_selected)} [EMOJI]")
                print("([EMOJI] + 20[EMOJI]>0 + RSI<70 + [EMOJI]<0.3)")
                print(df_selected[['momentum_20d', 'rsi_14', 'volatility_20d']].to_string())
            else:
                print("[INFO] [EMOJI]")
        else:
            print("[INFO] [EMOJI]")
    else:
        print("[INFO] [EMOJI]")
except Exception as e:
    print(f"[INFO] {e}")

# ============================================================
# [EMOJI]6[EMOJI]
# ============================================================

print("\n\n" + "=" * 90)
print("[[EMOJI]6] [EMOJI]")
print("=" * 90)

print("\n[EMOJI]")
print("[EMOJI]")
print("[EMOJI] - [EMOJI]")

print("\n[EMOJI]")
print("""
# 1. [EMOJI]
stock_list = ['000001.SZ', '000002.SZ', '600000.SH', '600036.SH', '600519.SH']
df_factors = get_batch_enhanced_factors(stock_list, ef.duckdb_reader)

# 2. [EMOJI]
#    - [EMOJI]>0[EMOJI]20[EMOJI]
#    - [EMOJI]>0[EMOJI]60[EMOJI]
#    - RSI < 70[EMOJI]

df_selected = df_factors[
    (df_factors['momentum_20d'] > 0) &
    (df_factors['momentum_60d'] > 0) &
    (df_factors['rsi_14'] < 70)
]

print("[EMOJI]")
print(df_selected)
""")

print("\n[EMOJI]")
try:
    stock_list = ['000001.SZ', '000002.SZ', '600000.SH', '600036.SH', '600519.SH']
    df_factors = get_batch_enhanced_factors(stock_list, ef.duckdb_reader)

    if not df_factors.empty and all(col in df_factors.columns for col in ['momentum_20d', 'momentum_60d', 'rsi_14']):
        df_selected = df_factors[
            (df_factors['momentum_20d'] > 0) &
            (df_factors['momentum_60d'] > 0) &
            (df_factors['rsi_14'] < 70)
        ]

        if not df_selected.empty:
            print(f"[OK] [EMOJI] {len(df_selected)} [EMOJI]")
            print("(20[EMOJI]>0 + 60[EMOJI]>0 + RSI<70)")
            print(df_selected[['momentum_20d', 'momentum_60d', 'rsi_14']].to_string())
        else:
            print("[INFO] [EMOJI]")
    else:
        print("[INFO] [EMOJI]")
except Exception as e:
    print(f"[INFO] {e}")

# ============================================================
# [EMOJI]
# ============================================================

print("\n\n" + "=" * 90)
print(" " * 30 + "[EMOJI]")
print("=" * 90)

summary = """
EasyFactor [EMOJI]

[EMOJI]

1. qstock[EMOJI]
   - [EMOJI]90[EMOJI]
   - [EMOJI]387[EMOJI]
   - [EMOJI]2,616[EMOJI]
   - [EMOJI]86[EMOJI]
   - [EMOJI]2,767[EMOJI]
   - [EMOJI]5,175[EMOJI]

2. DuckDB[EMOJI]
   - 767[EMOJI]2015-2026[EMOJI]
   - 5,190[EMOJI]
   - [EMOJI]

[EMOJI]29[EMOJI]

1. [EMOJI]3[EMOJI]
   - price_to_ma20/60: [EMOJI]
   - price_percentile: [EMOJI]
   - dist_from_high_252: [EMOJI]52[EMOJI]

2. [EMOJI]8[EMOJI]
   - momentum_1/5/10/20/60/120/252d: [EMOJI]
   - momentum_accel: [EMOJI]
   - rsi_14: [EMOJI]

3. [EMOJI]6[EMOJI]
   - volatility_20/60/120d: [EMOJI]
   - atr_14: [EMOJI]
   - volatility_percentile: [EMOJI]

4. [EMOJI]5[EMOJI]
   - price_cv_60d: [EMOJI]
   - trend_strength_60d: [EMOJI]
   - consecutive_up/down_days: [EMOJI]
   - price_position_52w: 52[EMOJI]

5. [EMOJI]7[EMOJI]
   - avg_volume_5/20/60d: [EMOJI]
   - volume_ratio: [EMOJI]
   - turnover_5/20d: [EMOJI]

[EMOJI]API[EMOJI]

# [EMOJI]
ef.get_ths_industry_money_flow(top_n=20, use_cache=True)      # [EMOJI]
ef.get_ths_concept_money_flow(top_n=20, use_cache=True)       # [EMOJI]
ef.get_north_money_flow(days=30, use_cache=True)              # [EMOJI]
ef.get_north_money_sector(top_n=20)                           # [EMOJI]
ef.get_north_money_stock(stock_code=None, top_n=20)           # [EMOJI]
ef.get_ths_stock_money_flow(stock_code=None, top_n=20, use_cache=True)  # [EMOJI]
ef.update_ths_money_flow()                                     # [EMOJI]

# [EMOJI]
get_enhanced_fundamental_factors('000001.SZ', ef.duckdb_reader)           # [EMOJI]
get_batch_enhanced_factors(stock_list, ef.duckdb_reader)                  # [EMOJI]

[EMOJI]

1. [EMOJI]qstock[EMOJI]
2. [EMOJI]200-400x[EMOJI]
3. [EMOJI]29[EMOJI] + 6[EMOJI]
4. [EMOJI]767[EMOJI]
5. [EMOJI]

[EMOJI]

1. [EMOJI]DuckDB
2. [EMOJI]
3. [EMOJI] use_cache=False [EMOJI]
4. [EMOJI]
5. [EMOJI]
"""

print(summary)

print("\n" + "=" * 90)
print(" " * 30 + "[EMOJI]")
print("=" * 90)

print("\n[EMOJI]")
print("1. qstock[EMOJI]")
print("2. DuckDB[EMOJI]767[EMOJI]")
print("3. [EMOJI]29[EMOJI]")
print("4. [EMOJI]")
