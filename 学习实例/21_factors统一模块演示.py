# -*- coding: utf-8 -*-
"""
factors[EMOJI]

[EMOJI]factors[EMOJI]
- [EMOJI]Fama-French[EMOJI]/[EMOJI]
- [EMOJI]IC/IR[EMOJI]
- [EMOJI]
- [EMOJI]

[EMOJI]
# [EMOJI]factors[EMOJI]
from factors import EasyFactor, FundamentalAnalyzerEnhanced
from factors.pricing import FamaFrenchCalculator
from factors.analysis import ICAnalyzer, GroupBacktester
from factors.custom import SmallCapQualityFactor

# [EMOJI]
from factors.pricing.fama_french import FamaFrenchCalculator
from factors.analysis.ic_analyzer import ICAnalyzer
"""

import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import pandas as pd
import numpy as np
from datetime import datetime, timedelta

print("=" * 90)
print(" " * 25 + "factors[EMOJI]")
print("=" * 90)

# ============================================================
# [EMOJI]factors[EMOJI]
# ============================================================

print("\n[[EMOJI]1] [EMOJI]factors[EMOJI]")
print("-" * 90)

try:
    # [EMOJI]
    from factors import (
        EasyFactor,
        FundamentalAnalyzerEnhanced,
        FamaFrenchCalculator,
        ICAnalyzer,
        GroupBacktester,
        SmallCapQualityFactor
    )
    print("[OK] factors[EMOJI]")
    print("\n[EMOJI]:")
    print("  - EasyFactor: [EMOJI]50+[EMOJI]")
    print("  - FundamentalAnalyzerEnhanced: [EMOJI]29[EMOJI]")
    print("  - FamaFrenchCalculator: Fama-French[EMOJI]")
    print("  - ICAnalyzer: IC/IR[EMOJI]")
    print("  - GroupBacktester: [EMOJI]")
    print("  - SmallCapQualityFactor: [EMOJI]")
except Exception as e:
    print(f"[FAIL] [EMOJI]: {e}")
    exit(1)

# ============================================================
# [EMOJI]1[EMOJI]
# ============================================================

print("\n" + "=" * 90)
print("[[EMOJI]1] [EMOJI]")
print("=" * 90)

import factors

# [EMOJI]
modules = factors.get_available_modules()
print("\n[[EMOJI]]")
for module, available in modules.items():
    status = "[OK]" if available else "[--]"
    print(f"  {status} {module}")

# [EMOJI]
all_factors = factors.list_all_factors()
print("\n[[EMOJI]]")
for category, factors_list in all_factors.items():
    if factors_list:
        print(f"\n{category} ({len(factors_list)}[EMOJI]):")
        for i, factor in enumerate(factors_list[:5]):  # [EMOJI]5[EMOJI]
            print(f"  {i+1}. {factor}")
        if len(factors_list) > 5:
            print(f"  ... [EMOJI] {len(factors_list) - 5} [EMOJI]")

# ============================================================
# [EMOJI]2[EMOJI]Fama-French[EMOJI]
# ============================================================

print("\n" + "=" * 90)
print("[[EMOJI]2] Fama-French[EMOJI]")
print("=" * 90)

print("\n[EMOJI]:")
print("- MKT[EMOJI]: [EMOJI]")
print("- SMB[EMOJI]: [EMOJI] - [EMOJI]")
print("- HML[EMOJI]: [EMOJI]PB[EMOJI] - [EMOJI]PB[EMOJI]")
print("- UMD[EMOJI]: [EMOJI] - [EMOJI]")

print("\n[EMOJI]...")

# [EMOJI]
np.random.seed(42)
n_stocks = 100
stock_codes = [f'{i:06d}.SZ' for i in range(n_stocks)]

mock_stock_data = pd.DataFrame({
    'stock_code': stock_codes,
    'close': np.random.uniform(10, 100, n_stocks),
    'total_mv': np.random.uniform(10, 1000, n_stocks),  # [EMOJI]
    'pb': np.random.uniform(0.5, 10, n_stocks),  # [EMOJI]
})

mock_stock_data['return'] = np.random.normal(0, 0.02, n_stocks)

print(f"[OK] [EMOJI]")
print(f"  [EMOJI]: {len(mock_stock_data)}")
print(f"  [EMOJI]: {mock_stock_data['total_mv'].mean():.2f}[EMOJI]")
print(f"  [EMOJI]PB: {mock_stock_data['pb'].mean():.2f}")

# [EMOJI]Fama-French[EMOJI]
print("\n[EMOJI]Fama-French[EMOJI]...")
ff_calc = FamaFrenchCalculator()
ff_factors = ff_calc.calculate_ff3_factors('2024-01-15', mock_stock_data)

print("\n[OK] [EMOJI]")
print(f"  MKT[EMOJI]: {ff_factors['MKT']:.4f}")
print(f"  SMB[EMOJI]: {ff_factors['SMB']:.4f}")
print(f"  HML[EMOJI]: {ff_factors['HML']:.4f}")
print(f"  [EMOJI]: {ff_factors['N_STOCKS']}")

# [EMOJI]Fama-French[EMOJI]
print("\n[EMOJI]Fama-French[EMOJI]...")
ff_factors_4 = ff_calc.calculate_ff4_factors('2024-01-15', mock_stock_data)

print("\n[OK] [EMOJI]")
print(f"  MKT: {ff_factors_4['MKT']:.4f}")
print(f"  SMB: {ff_factors_4['SMB']:.4f}")
print(f"  HML: {ff_factors_4['HML']:.4f}")
print(f"  UMD[EMOJI]: {ff_factors_4['UMD']:.4f}")

# ============================================================
# [EMOJI]3[EMOJI]IC/IR[EMOJI]
# ============================================================

print("\n" + "=" * 90)
print("[[EMOJI]3] IC/IR[EMOJI]")
print("=" * 90)

print("\n[EMOJI]:")
print("- IC[EMOJI]: [EMOJI]")
print("- IR[EMOJI]: IC[EMOJI] / IC[EMOJI]")
print("- [EMOJI]:")
print("    |IC| > 0.05 : [EMOJI]")
print("    IR > 1.0     : [EMOJI]")

print("\n[EMOJI]...")

# [EMOJI]
n_stocks = 100
n_dates = 50
dates = pd.date_range('2024-01-01', periods=n_dates, freq='D')
stock_codes = [f'{i:06d}.SZ' for i in range(n_stocks)]

# [EMOJI]
factor_values = np.random.randn(n_dates, n_stocks) * 0.1
factor_df = pd.DataFrame(factor_values, index=dates, columns=stock_codes)

# [EMOJI]
returns = factor_values * 0.03 + np.random.randn(n_dates, n_stocks) * 0.02
return_df = pd.DataFrame(returns, index=dates, columns=stock_codes)

print(f"[OK] [EMOJI]")
print(f"  [EMOJI]: {n_stocks}")
print(f"  [EMOJI]: {n_dates}")

# [EMOJI]Rank IC
print("\n[EMOJI]Rank IC...")
ic_analyzer = ICAnalyzer()
ic_series = ic_analyzer.calculate_rank_ic(factor_df, return_df, min_stock_num=10)

print(f"[OK] Rank IC[EMOJI]")
print(f"  IC[EMOJI]: {len(ic_series)}")
print(f"  IC[EMOJI]: {ic_series.mean():.4f}")
print(f"  IC[EMOJI]: {ic_series.std():.4f}")

# [EMOJI]IC[EMOJI]
print("\n[EMOJI]IC[EMOJI]...")
ic_stats = ic_analyzer.calculate_ic_statistics(ic_series)

print("\n[OK] IC[EMOJI]")
print(f"  IC[EMOJI]: {ic_stats['ic_mean']:.4f}")
print(f"  IC[EMOJI]: {ic_stats['ic_std']:.4f}")
print(f"  IR[EMOJI]: {ic_stats['ir']:.4f}")
print(f"  t[EMOJI]: {ic_stats['t_stat']:.4f}")
print(f"  p[EMOJI]: {ic_stats['p_value']:.4f}")
print(f"  IC[EMOJI]: {ic_stats['positive_ratio']:.2%}")

# [EMOJI]
print("\n[[EMOJI]]")
if abs(ic_stats['ic_mean']) > 0.05:
    print("  [[EMOJI]] [EMOJI] (|IC| > 0.05)")
elif abs(ic_stats['ic_mean']) > 0.03:
    print("  [[EMOJI]] [EMOJI] (|IC| > 0.03)")
elif abs(ic_stats['ic_mean']) > 0.02:
    print("  [[EMOJI]] [EMOJI] (|IC| > 0.02)")
else:
    print("  [[EMOJI]] [EMOJI] (|IC| < 0.02)")

if ic_stats['ir'] > 1.0:
    print("  [[EMOJI]] [EMOJI] (IR > 1.0)")
elif ic_stats['ir'] > 0.5:
    print("  [[EMOJI]] [EMOJI] (IR > 0.5)")
elif ic_stats['ir'] > 0.3:
    print("  [[EMOJI]] [EMOJI] (IR > 0.3)")
else:
    print("  [[EMOJI]] [EMOJI] (IR < 0.3)")

# ============================================================
# [EMOJI]4[EMOJI]
# ============================================================

print("\n" + "=" * 90)
print("[[EMOJI]4] [EMOJI]")
print("=" * 90)

print("\n[EMOJI]:")
print("  1. [EMOJI]:")
print("     - [EMOJI]")
print("     - [EMOJI]ST[EMOJI]>100[EMOJI]")
print("  2. [EMOJI]:")
print("     - ROE > 15%")
print("     - ROA > 10%")
print("  3. [EMOJI]:")
print("     - factor_value = -(rank_mv + rank_pb) / 2")
print("     - [EMOJI]+[EMOJI]PB[EMOJI]")

# [EMOJI]
print("\n[EMOJI]...")
factor = SmallCapQualityFactor()

print(f"[OK] [EMOJI]")
print(f"  [EMOJI]: {factor.name}")
print(f"  [EMOJI]: {factor.description}")
print(f"  [EMOJI]: {factor.freq}")

print("\n[[EMOJI]] [EMOJI]data_manager[EMOJI]")
print("      factor_df = factor.calculate('2024-01-15', data_manager)")

# ============================================================
# [EMOJI]
# ============================================================

print("\n" + "=" * 90)
print(" " * 30 + "[EMOJI]")
print("=" * 90)

print("\n[[EMOJI]]")
print("  [OK] factors[EMOJI]")
print("  [OK] [EMOJI]")
print("  [OK] [EMOJI]41[EMOJI]")
print("  [OK] Fama-French[EMOJI]/[EMOJI]")
print("  [OK] IC/IR[EMOJI]")
print("  [OK] [EMOJI]")

print("\n[factors[EMOJI]]")
print("  1. [EMOJI]")
print("  2. [EMOJI]easy_xt[EMOJI]")
print("  3. [EMOJI]")
print("  4. [EMOJI]pricing[EMOJI]analysis[EMOJI]custom[EMOJI]")

print("\n[[EMOJI]]")
print("  1. [EMOJI]DuckDB[EMOJI]")
print("  2. [EMOJI]ICAnalyzer[EMOJI]")
print("  3. [EMOJI]GroupBacktester[EMOJI]")
print("  4. [EMOJI]")

print("\n[[EMOJI]]")
print("  - [EMOJI]: factors/README.md")
print("  - [EMOJI]: test_factors_simple.py")
print("  - [EMOJI]: factors/pricing/fama_french.py")
print("  - IC[EMOJI]: factors/analysis/ic_analyzer.py")
print("  - [EMOJI]: factors/analysis/group_backtest.py")

print("\n" + "=" * 90)
print(" " * 25 + "[EMOJI]")
print("=" * 90)
