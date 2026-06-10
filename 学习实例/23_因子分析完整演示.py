# -*- coding: utf-8 -*-
"""
[EMOJI]DuckDB[EMOJI]
==============================================

[EMOJI]DuckDB[EMOJI]

[EMOJI]
-----------
1. [EMOJI] - [EMOJI]DuckDB[EMOJI]
2. IC/IR[EMOJI] - [EMOJI]
3. [EMOJI] - [EMOJI]
4. [EMOJI] - [EMOJI]
5. [EMOJI] - [EMOJI]
6. [EMOJI] - [EMOJI]6[EMOJI]

[EMOJI]
-----------
- [EMOJI]DuckDB[EMOJI]stock_data.ddb[EMOJI]
- [EMOJI]: D:/StockData/, C:/StockData/, E:/StockData/
- [EMOJI]

[EMOJI]101[EMOJI]
"""

import sys
import os

# ============================================================
# [EMOJI]
# ============================================================

script_dir = os.path.dirname(os.path.abspath(__file__))

# [EMOJI]
possible_roots = [
    os.path.normpath(os.path.join(script_dir, '..', '101[EMOJI]', '101[EMOJI]')),
    os.path.normpath(script_dir),
    os.path.normpath(os.path.join(script_dir, '101[EMOJI]', '101[EMOJI]')),
    os.path.normpath(os.path.join(os.path.dirname(script_dir), '101[EMOJI]', '101[EMOJI]')),
]

project_root = None
for root in possible_roots:
    if os.path.exists(os.path.join(root, 'src', 'analysis')):
        project_root = os.path.abspath(root)
        break

# [EMOJI]
if project_root is None:
    current = script_dir
    for _ in range(3):
        current = os.path.dirname(current)
        if os.path.exists(os.path.join(current, 'src', 'analysis')):
            project_root = os.path.abspath(current)
            break

# [EMOJI]
if project_root is None:
    project_root = os.path.abspath('.')

# [EMOJI]sys.path[EMOJI]
if project_root not in sys.path:
    sys.path.insert(0, project_root)

# ============================================================
# [EMOJI]
# ============================================================

import pandas as pd
import numpy as np
import matplotlib
# [EMOJI]matplotlib[EMOJI]Windows[EMOJI]TkAgg[EMOJI]
import matplotlib.pyplot as plt

# [EMOJI]
plt.rcParams['font.sans-serif'] = ['Microsoft YaHei', 'SimHei', 'Arial Unicode MS', 'DejaVu Sans']
plt.rcParams['axes.unicode_minus'] = False  # [EMOJI]

# [EMOJI]
try:
    plt.figure(figsize=(1, 1))
    plt.text(0.5, 0.5, '[EMOJI]', fontsize=12)
    plt.close()
    print("[OK] [EMOJI]")
except Exception as e:
    print(f"[WARN] [EMOJI]: {e}")
    # [EMOJI]
    USE_CHINESE = False
else:
    USE_CHINESE = True

print("=" * 80)
print(" " * 20 + "[EMOJI]DuckDB[EMOJI]")
print("=" * 80)
print("\n[[EMOJI]] [EMOJI]")

print("=" * 80)
print(" " * 20 + "[EMOJI]DuckDB[EMOJI]")
print("=" * 80)

# [EMOJI]
print("\n[[EMOJI]...]")
missing_deps = []

try:
    import duckdb
    print("  [OK] duckdb")
except ImportError:
    missing_deps.append("duckdb")
    print("  [[EMOJI]] duckdb - [EMOJI]: pip install duckdb")

try:
    from src.analysis.group_backtest import GroupBacktestEngine
    from src.analysis.visualization import FactorAnalysisVisualizer
    print("  [OK] src.analysis")
except ImportError as e:
    print(f"  [[EMOJI]] [EMOJI]: {e}")

try:
    from src.analysis.enhanced_performance import EnhancedPerformanceAnalyzer
    print("  [OK] src.analysis.enhanced_performance")
except ImportError:
    print("  [[EMOJI]] enhanced_performance[EMOJI]")

try:
    from src.factor_engine.specific_volatility import SpecificVolatilityCalculator
    print("  [OK] src.factor_engine.specific_volatility")
except ImportError:
    print("  [[EMOJI]] specific_volatility[EMOJI]")

if missing_deps:
    print(f"\n[[EMOJI]] [EMOJI]: {', '.join(missing_deps)}")
    print("\n[EMOJI]:")
    print(f"  pip install {' '.join(missing_deps)}")
    sys.exit(1)

print("  [OK] [EMOJI]")

# ============================================================
# [EMOJI]DuckDB[EMOJI]
# ============================================================

print("\n[[EMOJI]1] [EMOJI] - [EMOJI]DuckDB[EMOJI]")
print("-" * 80)

# [EMOJI]DuckDB[EMOJI]
def detect_duckdb_path():
    """[EMOJI]DuckDB[EMOJI]"""
    candidates = [
        'D:/StockData/stock_data.ddb',
        'C:/StockData/stock_data.ddb',
        'E:/StockData/stock_data.ddb',
        './data/stock_data.ddb',
        os.path.join(project_root, 'data', 'stock_data.ddb'),
    ]

    for path in candidates:
        if os.path.exists(path):
            return path

    # [EMOJI]
    env = os.environ.get('DUCKDB_PATH')
    if env and os.path.exists(env):
        return env

    return None

# [EMOJI]
duckdb_path = detect_duckdb_path()

if duckdb_path is None:
    print("\n[[EMOJI]] [EMOJI]DuckDB[EMOJI]")
    print("\n" + "="*80)
    print("[EMOJI]DuckDB")
    print("="*80)

    print("\n[EMOJI]1: [EMOJI]QMT/xtquant[EMOJI]")
    print("-"*80)
    print("1. [EMOJI]QMT[EMOJI]")
    print("2. [EMOJI]: python scripts/download_stocks.py")
    print("3. [EMOJI]DuckDB[EMOJI]")

    print("\n[EMOJI]2: [EMOJI]")
    print("-"*80)
    print("[EMOJI]Python[EMOJI]:")
    print("""
    import pandas as pd
    import duckdb
    import numpy as np

    # [EMOJI]
    dates = pd.date_range('2023-01-01', periods=500, freq='D')
    stocks = ['000001.SZ', '000002.SZ', '600000.SH', '600036.SH', '600519.SH']

    data = []
    np.random.seed(42)
    for stock in stocks:
        for date in dates:
            price = 10 + np.random.randn() * 2
            data.append({
                'date': date,
                'stock_code': stock,
                'open': price * (1 + np.random.randn() * 0.01),
                'high': price * (1 + abs(np.random.randn() * 0.02)),
                'low': price * (1 - abs(np.random.randn() * 0.02)),
                'close': price,
                'volume': np.random.randint(1000000, 10000000)
            })

    df = pd.DataFrame(data)
    conn = duckdb.connect('data/stock_data.ddb')
    conn.execute('CREATE TABLE stock_daily AS SELECT * FROM df')
    conn.close()
    print("[EMOJI]: data/stock_data.ddb")
    """)

    print("\n[EMOJI]3: [EMOJI]Tushare[EMOJI]")
    print("-"*80)
    print("1. [EMOJI]: https://tushare.pro")
    print("2. [EMOJI]API Token")
    print("3. [EMOJI]Tushare[EMOJI]")

    print("\n" + "="*80)
    print("[EMOJI]")
    print("="*80)
    sys.exit(1)

print(f"[OK] [EMOJI]DuckDB[EMOJI]: {duckdb_path}")

# [EMOJI]DuckDB[EMOJI]
print("\n[EMOJI]DuckDB[EMOJI]...")

try:
    conn = duckdb.connect(duckdb_path)

    # [EMOJI]
    stats_query = """
    SELECT COUNT(*) as total,
           MIN(date) as start_date,
           MAX(date) as end_date,
           COUNT(DISTINCT stock_code) as n_stocks
    FROM stock_daily
    WHERE date >= '2023-01-01' AND date <= '2023-12-31'
    """
    stats = conn.execute(stats_query).fetchdf()

    n_stocks_total = stats['n_stocks'].iloc[0]
    total_records = stats['total'].iloc[0]
    start_date = stats['start_date'].iloc[0]
    end_date = stats['end_date'].iloc[0]

    print(f"[[EMOJI]] [EMOJI] {n_stocks_total:,.0f} [EMOJI]")
    print(f"           [EMOJI]: 2023[EMOJI]")
    print(f"           [EMOJI]: {total_records:,.0f}")

    # [EMOJI]100[EMOJI]
    print("\n[EMOJI]100[EMOJI]...")

    # [EMOJI] - [EMOJI]2023[EMOJI]
    data_query = """
    SELECT date, stock_code, close,
           LAG(close, 1) OVER (PARTITION BY stock_code ORDER BY date) as prev_close
    FROM (
        SELECT * FROM stock_daily
        WHERE stock_code IN (
            SELECT DISTINCT stock_code FROM stock_daily
            WHERE date >= '2023-01-01' AND date <= '2023-12-31'
            LIMIT 100
        )
        AND date >= '2023-01-01' AND date <= '2023-12-31'
    )
    QUALIFY prev_close IS NOT NULL
    ORDER BY stock_code, date
    """

    df_raw = conn.execute(data_query).fetchdf()
    conn.close()

    if df_raw.empty:
        print("[[EMOJI]] [EMOJI]")
        sys.exit(1)

    # [EMOJI]
    df_raw['return'] = df_raw['close'] / df_raw['prev_close'] - 1

    # [EMOJI]5[EMOJI]1[EMOJI]
    # [EMOJI]
    df_raw['factor'] = df_raw.groupby('stock_code')['close'].transform(
        lambda x: x.pct_change(5)  # [EMOJI]5[EMOJI]20[EMOJI]
    )

    # [EMOJI]
    df_raw = df_raw.dropna()
    df = df_raw[['date', 'stock_code', 'factor', 'return']].copy()

    # [EMOJI]
    correlation = df['factor'].corr(df['return'])
    print(f"\n[[EMOJI]] [EMOJI]: {correlation:.4f}")
    if abs(correlation) > 0.95:
        print(f"[[EMOJI]] [EMOJI]({correlation:.4f})[EMOJI]")
        print(f"        [EMOJI]IC[EMOJI]")

    # [EMOJI]
    n_dates = df['date'].nunique()
    if n_dates < 20:
        print(f"[[EMOJI]] [EMOJI]({n_dates}[EMOJI])[EMOJI]IC[EMOJI]")
        print(f"        [EMOJI]60[EMOJI]3[EMOJI]")

    print(f"[OK] [EMOJI]: {len(df):,} [EMOJI]")
    print(f"  [EMOJI]: {df['stock_code'].nunique()}")
    print(f"  [EMOJI]: {df['date'].min()} [EMOJI] {df['date'].max()}")
    print(f"  [EMOJI]: {df['return'].mean():.4%}")

    # [EMOJI]
    print(f"\n[DEBUG] [EMOJI]:")
    print(f"  [EMOJI]: [{df['factor'].min():.4f}, {df['factor'].max():.4f}]")
    print(f"  [EMOJI]: [{df['return'].min():.4f}, {df['return'].max():.4f}]")
    print(f"  [EMOJI]: {df['factor'].std():.4f}")
    print(f"  [EMOJI]: {df['return'].std():.4f}")
    print(f"  [EMOJI]: {df['date'].nunique()}")
    print(f"  [EMOJI]: {len(df) / df['stock_code'].nunique():.1f}")

    # [EMOJI]
    if df['factor'].std() < 1e-10 or df['return'].std() < 1e-10:
        print("\n[[EMOJI]] [EMOJI]0[EMOJI]IC[EMOJI]")
        print(f"  [EMOJI]")

    # [EMOJI]
    if df['date'].nunique() < 10:
        print(f"\n[[EMOJI]] [EMOJI]{df['date'].nunique()}[EMOJI]IC[EMOJI]")
        print("        [EMOJI]20[EMOJI]")
        sys.exit(1)

except Exception as e:
    print(f"[[EMOJI]] DuckDB[EMOJI]: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)

# ============================================================
# [EMOJI]IC/IR[EMOJI]
# ============================================================

print("\n" + "=" * 80)
print("[[EMOJI]2] IC/IR[EMOJI] - [EMOJI]")
print("=" * 80)

from src.analysis.group_backtest import GroupBacktestEngine
from src.analysis.visualization import FactorAnalysisVisualizer

# [EMOJI]
engine = GroupBacktestEngine()
visualizer = FactorAnalysisVisualizer()

print("\n[EMOJI]IC[EMOJI]...")

# [EMOJI]
factor_df = df[['date', 'stock_code', 'factor']].copy()
returns_df = df[['date', 'stock_code', 'return']].copy()
returns_df = returns_df.rename(columns={'return': 'ret'})  # [EMOJI]ret

print(f"[DEBUG] [EMOJI]: {factor_df.shape}, [EMOJI]: [{factor_df['factor'].min():.4f}, {factor_df['factor'].max():.4f}]")
print(f"[DEBUG] [EMOJI]: {returns_df.shape}, [EMOJI]: [{returns_df['ret'].min():.4f}, {returns_df['ret'].max():.4f}]")

ic_result = engine.quick_ic_test(factor_df, returns_df)

# [EMOJI]IC[EMOJI]
print("\n[IC[EMOJI]]")
abs_ic = abs(ic_result['ic_mean'])
ic_ir = ic_result['ic_ir']

print(f"  IC[EMOJI]:     {ic_result['ic_mean']:.4f}", end="")
if abs_ic > 0.05:
    print("  [[EMOJI]] [EMOJI]")
elif abs_ic > 0.03:
    print("  [[EMOJI]] [EMOJI]")
elif abs_ic > 0.02:
    print("  [[EMOJI]] [EMOJI]")
else:
    print("  [[EMOJI]] [EMOJI]")

print(f"  IC[EMOJI]:   {ic_result['ic_std']:.4f}")
print(f"  IC_IR:      {ic_result['ic_ir']:.4f}", end="")
if ic_ir > 1.0:
    print("  [[EMOJI]] [EMOJI]")
elif ic_ir > 0.5:
    print("  [[EMOJI]] [EMOJI]")
elif ic_ir > 0.3:
    print("  [[EMOJI]] [EMOJI]")
else:
    print("  [[EMOJI]] [EMOJI]")

print(f"  IC[EMOJI]: {ic_result['ic_abs_mean']:.4f}")
print(f"  t[EMOJI]:    {ic_result['t_stat']:.4f}")
print(f"  p[EMOJI]:        {ic_result['p_value']:.4f}")
print(f"  IC[EMOJI]:  {ic_result['ic_positive_ratio']:.2%}")

# [EMOJI]IC[EMOJI]
print("\n[EMOJI]IC[EMOJI]...")

# [EMOJI]1: IC[EMOJI]
print("  [1/2] [EMOJI]IC[EMOJI]...")
fig_ic = visualizer.plot_ic_analysis(
    ic_result['ic_series'],
    factor_name="[EMOJI]20[EMOJI]"
)
fig_ic.savefig('demo_ic_analysis.png', dpi=150, bbox_inches='tight')
print("       [OK] [EMOJI]: demo_ic_analysis.png")
print("       [[EMOJI]] [EMOJI]...")
plt.show()

# [EMOJI]2: IC[EMOJI]4[EMOJI]
print("  [2/2] [EMOJI]IC[EMOJI]...")
fig_stats, axes = plt.subplots(2, 2, figsize=(14, 10))

ic_clean = ic_result['ic_series'].dropna()

# [EMOJI]1: IC[EMOJI]
axes[0, 0].hist(ic_clean, bins=40, density=True, alpha=0.7,
                color='steelblue', edgecolor='black')
axes[0, 0].axvline(x=ic_result['ic_mean'], color='red',
                   linestyle='--', linewidth=2, label=f"[EMOJI]={ic_result['ic_mean']:.4f}")
axes[0, 0].axvline(x=0, color='black', linestyle='-', linewidth=0.5)
axes[0, 0].set_title('IC[EMOJI]', fontsize=12, fontweight='bold')
axes[0, 0].set_xlabel('IC[EMOJI]')
axes[0, 0].set_ylabel('[EMOJI]')
axes[0, 0].legend()
axes[0, 0].grid(True, alpha=0.3)

# [EMOJI]2: IC[EMOJI]
axes[0, 1].plot(ic_clean.index, ic_clean.values, linewidth=1,
                color='steelblue', alpha=0.8)
axes[0, 1].axhline(y=0, color='black', linestyle='-', linewidth=0.5)
axes[0, 1].axhline(y=ic_result['ic_mean'], color='red',
                   linestyle='--', linewidth=1.5, label=f"[EMOJI]={ic_result['ic_mean']:.4f}")
axes[0, 1].fill_between(ic_clean.index, 0, ic_clean.values,
                        where=ic_clean.values >= 0, color='red', alpha=0.3, label='[EMOJI]IC')
axes[0, 1].fill_between(ic_clean.index, 0, ic_clean.values,
                        where=ic_clean.values < 0, color='green', alpha=0.3, label='[EMOJI]IC')
axes[0, 1].set_title('IC[EMOJI]', fontsize=12, fontweight='bold')
axes[0, 1].set_ylabel('IC[EMOJI]')
axes[0, 1].legend(loc='upper left', fontsize=8)
axes[0, 1].grid(True, alpha=0.3)

# [EMOJI]3: [EMOJI]IC[EMOJI]
cumulative_ic = ic_clean.cumsum()
axes[1, 0].plot(cumulative_ic.index, cumulative_ic.values,
                linewidth=2, color='darkblue')
axes[1, 0].axhline(y=0, color='black', linestyle='-', linewidth=0.5)
axes[1, 0].set_title('[EMOJI]IC', fontsize=12, fontweight='bold')
axes[1, 0].set_ylabel('[EMOJI]IC')
axes[1, 0].grid(True, alpha=0.3)

# [EMOJI]4: IC[EMOJI]
# [EMOJI]
plt.rcParams['font.sans-serif'] = ['Microsoft YaHei', 'SimHei', 'Arial Unicode MS', 'DejaVu Sans']
plt.rcParams['axes.unicode_minus'] = False

# [EMOJI]
stats_text = f"""
IC Statistics Summary
[EMOJI]
IC Mean:     {ic_result['ic_mean']:.4f}
IC Std Dev:  {ic_result['ic_std']:.4f}
IC IR:       {ic_result['ic_ir']:.4f}
IC Abs Mean: {ic_result['ic_abs_mean']:.4f}
t-statistic: {ic_result['t_stat']:.2f}
p-value:     {ic_result['p_value']:.4f}
IC>0 Ratio:  {ic_result['ic_positive_ratio']:.1%}

[EMOJI]
Prediction: {'Excellent' if abs_ic > 0.05 else 'Good' if abs_ic > 0.03 else 'Fair'}
Stability:  {'Excellent' if ic_ir > 1.0 else 'Good' if ic_ir > 0.5 else 'Fair'}
"""
axes[1, 1].text(0.1, 0.5, stats_text, fontsize=11,
                verticalalignment='center', family='monospace',
                bbox=dict(boxstyle='round', facecolor='wheat', alpha=0.5))
axes[1, 1].axis('off')
axes[1, 1].set_title('IC Statistics Summary', fontsize=12, fontweight='bold')

plt.tight_layout()
fig_stats.savefig('demo_ic_statistics.png', dpi=150, bbox_inches='tight')
print("       [OK] [EMOJI]: demo_ic_statistics.png")
print("       [[EMOJI]] [EMOJI]...")
plt.show()

# ============================================================
# [EMOJI]
# ============================================================

print("\n" + "=" * 80)
print("[[EMOJI]3] [EMOJI]")
print("=" * 80)

try:
    from src.factor_engine.specific_volatility import SpecificVolatilityCalculator

    calculator = SpecificVolatilityCalculator(window=20)

    # [EMOJI]
    market_returns = df.groupby('date')['return'].mean()

    # [EMOJI]
    demo_stocks = df['stock_code'].unique()[:5]
    print(f"\n[EMOJI] {len(demo_stocks)} [EMOJI]:")

    for stock in demo_stocks:
        stock_returns = df[df['stock_code'] == stock].set_index('date')['return']
        spec_vol = calculator.calculate_specific_volatility(
            stock_returns,
            market_returns,
            window=20
        )

        if not spec_vol.empty:
            avg_vol = spec_vol.mean()
            print(f"  {stock}: {avg_vol:.2%} ([EMOJI])")
        else:
            print(f"  {stock}: [EMOJI]")

except Exception as e:
    print(f"[[EMOJI]] [EMOJI]: {e}")

# ============================================================
# [EMOJI]
# ============================================================

print("\n" + "=" * 80)
print("[[EMOJI]4] [EMOJI] - [EMOJI]")
print("=" * 80)

# [EMOJI]
factor_df = df[['date', 'stock_code', 'factor']].copy()
returns_df = df[['date', 'stock_code', 'return']].copy()

print("\n[EMOJI]...")
print("  [EMOJI]: 5")
print("  [EMOJI]: [EMOJI]")
print("  [EMOJI]: 0.025%")
print("  [EMOJI]: 0.1%")

backtest_result = engine.run_backtest(
    factor_data=factor_df,
    returns_data=returns_df,
    n_groups=5,
    freq='monthly',
    commission=0.00025,
    slippage=0.001
)

n_periods = backtest_result['backtest_results']['n_periods']
print(f"\n[OK] [EMOJI] {n_periods} [EMOJI]")

# [EMOJI]
if 'group_returns' in backtest_result['backtest_results']:
    group_returns = backtest_result['backtest_results']['group_returns']

    if not group_returns.empty:
        print("\n[[EMOJI]]")

        # [EMOJI]
        cumulative = (1 + group_returns).cumprod()

        print("\n[EMOJI]:")
        print(f"{'[EMOJI]':<8} {'[EMOJI]':<12} {'[EMOJI]':<12}")
        print("-" * 35)

        for col in cumulative.columns:
            final_value = cumulative[col].iloc[-1]
            annual_ret = group_returns[col].mean() * 252
            print(f"{col:<8} {final_value:>10.2%}     {annual_ret:>10.2%}")

        # [EMOJI]
        print("\n[[EMOJI]]")
        group_annual = [group_returns[col].mean() * 252 for col in cumulative.columns]
        is_monotonic = all(group_annual[i] <= group_annual[i+1] for i in range(len(group_annual)-1))

        if is_monotonic:
            print("  [OK] [EMOJI]")
        else:
            print("  [INFO] [EMOJI]")

# ============================================================
# [EMOJI]
# ============================================================

print("\n" + "=" * 80)
print("[[EMOJI]5] [EMOJI] - [EMOJI]")
print("=" * 80)

try:
    from src.analysis.enhanced_performance import EnhancedPerformanceAnalyzer

    analyzer = EnhancedPerformanceAnalyzer()

    # [EMOJI]
    print("\n[EMOJI]...")

    # [EMOJI]
    high_factor_stocks = df.groupby('stock_code')['factor'].mean().nlargest(10).index
    low_factor_stocks = df.groupby('stock_code')['factor'].mean().nsmallest(10).index

    # [EMOJI]
    long_short_returns = []
    for date in df['date'].unique():
        daily_data = df[df['date'] == date]
        long_ret = daily_data[daily_data['stock_code'].isin(high_factor_stocks)]['return'].mean()
        short_ret = daily_data[daily_data['stock_code'].isin(low_factor_stocks)]['return'].mean()
        long_short_returns.append(long_ret - short_ret)

    ls_series = pd.Series(long_short_returns, index=df['date'].unique())

    # [EMOJI]
    benchmark_returns = df.groupby('date')['return'].mean()

    # [EMOJI]
    metrics = analyzer.calculate_performance_metrics(ls_series, benchmark_returns)

    print("\n[[EMOJI]]")
    print(f"{'[EMOJI]':<20} {'[EMOJI]'}")
    print("-" * 35)
    print(f"{'[EMOJI]':<20} {metrics['total_return']:>12.2%}")
    print(f"{'[EMOJI]':<20} {metrics['annual_return']:>12.2%}")
    print(f"{'[EMOJI]':<20} {metrics['annual_volatility']:>12.2%}")
    print(f"{'[EMOJI]':<20} {metrics['sharpe_ratio']:>12.4f}")
    print(f"{'Sortino[EMOJI]':<20} {metrics['sortino_ratio']:>12.4f}")
    print(f"{'Calmar[EMOJI]':<20} {metrics['calmar_ratio']:>12.4f}")
    print(f"{'[EMOJI]':<20} {metrics['max_drawdown']:>12.2%}")
    print(f"{'[EMOJI]':<20} {metrics['win_rate']:>12.2%}")

    # [EMOJI]
    print("\n[[EMOJI]]")
    if metrics['sharpe_ratio'] > 2:
        print("  [[EMOJI]] [EMOJI]>2[EMOJI]")
    elif metrics['sharpe_ratio'] > 1:
        print("  [[EMOJI]] [EMOJI]>1[EMOJI]")
    elif metrics['sharpe_ratio'] > 0.5:
        print("  [[EMOJI]] [EMOJI]>0.5[EMOJI]")
    else:
        print("  [[EMOJI]] [EMOJI]<0.5[EMOJI]")

    if metrics['max_drawdown'] < 0.1:
        print("  [[EMOJI]] [EMOJI]<10%[EMOJI]")
    elif metrics['max_drawdown'] < 0.2:
        print("  [[EMOJI]] [EMOJI]<20%[EMOJI]")
    else:
        print("  [WARN] [EMOJI]>20%[EMOJI]")

except Exception as e:
    print(f"[[EMOJI]] [EMOJI]: {e}")
    # [EMOJI]
    high_factor_stocks = df.groupby('stock_code')['factor'].mean().nlargest(10).index
    low_factor_stocks = df.groupby('stock_code')['factor'].mean().nsmallest(10).index

    long_short_returns = []
    for date in df['date'].unique():
        daily_data = df[df['date'] == date]
        long_ret = daily_data[daily_data['stock_code'].isin(high_factor_stocks)]['return'].mean()
        short_ret = daily_data[daily_data['stock_code'].isin(low_factor_stocks)]['return'].mean()
        long_short_returns.append(long_ret - short_ret)

    ls_series = pd.Series(long_short_returns, index=df['date'].unique())
    benchmark_returns = df.groupby('date')['return'].mean()

    # [EMOJI]
    total_return = (1 + ls_series).prod() - 1
    annual_return = ls_series.mean() * 252
    annual_vol = ls_series.std() * np.sqrt(252)
    sharpe = annual_return / annual_vol if annual_vol > 0 else 0

    cumulative = (1 + ls_series).cumprod()
    running_max = cumulative.expanding().max()
    drawdown = (cumulative - running_max) / running_max
    max_dd = drawdown.min()

    metrics = {
        'total_return': total_return,
        'annual_return': annual_return,
        'annual_volatility': annual_vol,
        'sharpe_ratio': sharpe,
        'max_drawdown': max_dd,
        'win_rate': (ls_series > 0).mean()
    }

    print("\n[[EMOJI]]")
    print(f"  [EMOJI]: {metrics['total_return']:.2%}")
    print(f"  [EMOJI]: {metrics['annual_return']:.2%}")
    print(f"  [EMOJI]: {metrics['sharpe_ratio']:.4f}")
    print(f"  [EMOJI]: {metrics['max_drawdown']:.2%}")

# ============================================================
# [EMOJI]
# ============================================================

print("\n" + "=" * 80)
print("[[EMOJI]6] [EMOJI] - [EMOJI]")
print("=" * 80)

# [EMOJI]1: [EMOJI]
print("\n[EMOJI]...")
fig_nav, ax = plt.subplots(figsize=(14, 7))

# [EMOJI]
cumulative_ls = (1 + ls_series).cumprod()
cumulative_bench = (1 + benchmark_returns).cumprod()

# [EMOJI]
ax.plot(cumulative_ls.index, cumulative_ls.values,
        label='[EMOJI]', linewidth=2.5, color='#2E86AB')
ax.plot(cumulative_bench.index, cumulative_bench.values,
        label='[EMOJI]', linewidth=2, color='#A23B72', linestyle='--')

# [EMOJI]
running_max = cumulative_ls.expanding().max()
drawdown = (cumulative_ls - running_max) / running_max
max_dd_idx = drawdown.idxmin()
peak_idx = cumulative_ls[:max_dd_idx].idxmax()

ax.scatter([peak_idx, max_dd_idx],
           [cumulative_ls.loc[peak_idx], cumulative_ls.loc[max_dd_idx]],
           color='red', s=100, zorder=5)
ax.annotate('', xy=(max_dd_idx, cumulative_ls.loc[max_dd_idx]),
            xytext=(peak_idx, cumulative_ls.loc[peak_idx]),
            arrowprops=dict(arrowstyle='->', color='red', lw=1.5))

# [EMOJI]
ax.set_title('[EMOJI]', fontsize=16, fontweight='bold', pad=15)
ax.set_xlabel('[EMOJI]', fontsize=12)
ax.set_ylabel('[EMOJI]', fontsize=12)
ax.legend(loc='best', fontsize=11)
ax.grid(True, alpha=0.3)

# [EMOJI]
info_text = f"""
[EMOJI]
[EMOJI]
[EMOJI]: {metrics['annual_return']:.2%}
[EMOJI]: {metrics['sharpe_ratio']:.2f}
[EMOJI]: {metrics['max_drawdown']:.2%}
"""
ax.text(0.02, 0.98, info_text, transform=ax.transAxes,
        fontsize=10, verticalalignment='top',
        bbox=dict(boxstyle='round', facecolor='wheat', alpha=0.5))

plt.tight_layout()
fig_nav.savefig('demo_nav_curve.png', dpi=150, bbox_inches='tight')
print("  [OK] [EMOJI]: demo_nav_curve.png")
print("  [[EMOJI]] [EMOJI]...")
plt.show()

# [EMOJI]2: [EMOJI]
if 'group_returns' in backtest_result['backtest_results']:
    group_returns = backtest_result['backtest_results']['group_returns']
    if not group_returns.empty:
        print("\n[EMOJI]...")
        fig_groups = visualizer.plot_group_backtest(
            group_returns,
            None,
            factor_name="[EMOJI]"
        )
        fig_groups.savefig('demo_group_returns.png', dpi=150, bbox_inches='tight')
        print("  [OK] [EMOJI]: demo_group_returns.png")
        print("  [[EMOJI]] [EMOJI]...")
        plt.show()

# [EMOJI]3: [EMOJI]
print("\n[EMOJI]...")
fig_dd, ax = plt.subplots(figsize=(14, 6))

# [EMOJI]
cumulative = (1 + ls_series).cumprod()
running_max = cumulative.expanding().max()
drawdown = (cumulative - running_max) / running_max

# [EMOJI]
ax.fill_between(drawdown.index, drawdown.values, 0,
                where=drawdown.values < 0, color='red', alpha=0.3)
ax.plot(drawdown.index, drawdown.values, color='darkred', linewidth=1.5)

# [EMOJI]
ax.scatter([max_dd_idx], [drawdown.loc[max_dd_idx]],
           color='darkred', s=150, zorder=5, marker='v')
ax.annotate(f'[EMOJI]: {metrics["max_drawdown"]:.2%}',
            xy=(max_dd_idx, drawdown.loc[max_dd_idx]),
            xytext=(10, 10), textcoords='offset points',
            fontsize=11, fontweight='bold',
            bbox=dict(boxstyle='round', facecolor='yellow', alpha=0.7),
            arrowprops=dict(arrowstyle='->', color='black', lw=1.5))

ax.set_title('[EMOJI]', fontsize=16, fontweight='bold', pad=15)
ax.set_xlabel('[EMOJI]', fontsize=12)
ax.set_ylabel('[EMOJI]', fontsize=12)
ax.grid(True, alpha=0.3)
ax.axhline(y=0, color='black', linestyle='-', linewidth=0.5)

plt.tight_layout()
fig_dd.savefig('demo_drawdown.png', dpi=150, bbox_inches='tight')
print("  [OK] [EMOJI]: demo_drawdown.png")
print("  [[EMOJI]] [EMOJI]...")
plt.show()

# ============================================================
# [EMOJI]
# ============================================================

print("\n" + "=" * 80)
print("[[EMOJI]7] [EMOJI]")
print("=" * 80)

# [EMOJI]
score = 0
if abs_ic > 0.05: score += 25
elif abs_ic > 0.03: score += 15
elif abs_ic > 0.02: score += 5

if ic_ir > 1.0: score += 25
elif ic_ir > 0.5: score += 15
elif ic_ir > 0.3: score += 5

if metrics['sharpe_ratio'] > 2: score += 25
elif metrics['sharpe_ratio'] > 1: score += 15
elif metrics['sharpe_ratio'] > 0.5: score += 5

if metrics['max_drawdown'] < 0.1: score += 25
elif metrics['max_drawdown'] < 0.2: score += 15
elif metrics['max_drawdown'] < 0.3: score += 5

report = f"""
{'='*80}
                    [EMOJI]
{'='*80}

[EMOJI]: DuckDB[EMOJI]
[EMOJI]: {pd.Timestamp.now().strftime('%Y-%m-%d %H:%M:%S')}

[EMOJI]
{'[EMOJI]'*80}
  [EMOJI]: {df['stock_code'].nunique()}
  [EMOJI]: {len(df):,}
  [EMOJI]: {df['date'].min()} [EMOJI] {df['date'].max()}
  [EMOJI]: {duckdb_path}

[EMOJI]IC/IR[EMOJI]
{'[EMOJI]'*80}
IC[EMOJI]:        {ic_result['ic_mean']:.4f}  {'[[EMOJI]]' if abs_ic > 0.05 else '[[EMOJI]]' if abs_ic > 0.03 else '[[EMOJI]]'}
IC[EMOJI]:      {ic_result['ic_std']:.4f}
IC_IR:         {ic_result['ic_ir']:.4f}  {'[[EMOJI]]' if ic_ir > 1.0 else '[[EMOJI]]' if ic_ir > 0.5 else '[[EMOJI]]'}
IC[EMOJI]:  {ic_result['ic_abs_mean']:.4f}
t[EMOJI]:       {ic_result['t_stat']:.2f}
p[EMOJI]:           {ic_result['p_value']:.4f}
IC[EMOJI]:    {ic_result['ic_positive_ratio']:.1%}

[EMOJI]
{'[EMOJI]'*80}
[EMOJI]:      {metrics['annual_return']:.2%}
[EMOJI]:    {metrics['annual_volatility']:.2%}
[EMOJI]:      {metrics['sharpe_ratio']:.4f}
[EMOJI]:      {metrics['max_drawdown']:.2%}
[EMOJI]:          {metrics['win_rate']:.2%}

[EMOJI]
{'[EMOJI]'*80}
"""

if 'group_returns' in backtest_result['backtest_results']:
    group_returns = backtest_result['backtest_results']['group_returns']
    if not group_returns.empty:
        report += "\n[EMOJI]:\n"
        for col in group_returns.columns:
            annual_ret = group_returns[col].mean() * 252
            report += f"  {col}: {annual_ret:.2%}\n"

report += f"""
[EMOJI]
{'[EMOJI]'*80}
[EMOJI]: {score}/100

"""

if score >= 80:
    report += "[EMOJI]: [[EMOJI]] [EMOJI]\n"
elif score >= 60:
    report += "[EMOJI]: [[EMOJI]] [EMOJI]\n"
elif score >= 40:
    report += "[EMOJI]: [[EMOJI]] [EMOJI]\n"
else:
    report += "[EMOJI]: [[EMOJI]] [EMOJI]\n"

report += f"""
{'='*80}
101[EMOJI]
[EMOJI]: {pd.Timestamp.now().strftime('%Y-%m-%d %H:%M:%S')}
{'='*80}
"""

print(report)

# [EMOJI]
with open('factor_analysis_report.txt', 'w', encoding='utf-8') as f:
    f.write(report)
print("\n[OK] [EMOJI]: factor_analysis_report.txt")

# ============================================================
# [EMOJI]
# ============================================================

print("\n" + "=" * 80)
print(" " * 30 + "[EMOJI]")
print("=" * 80)

print("\n[[EMOJI]]")
print("  1. demo_ic_analysis.png    - IC[EMOJI]")
print("  2. demo_ic_statistics.png  - IC[EMOJI]4[EMOJI]")
print("  3. demo_nav_curve.png      - [EMOJI]")
print("  4. demo_group_returns.png  - [EMOJI]")
print("  5. demo_drawdown.png       - [EMOJI]")
print("  6. factor_analysis_report.txt - [EMOJI]")

print("\n[[EMOJI]]")
print(f"  1. [EMOJI]: IC={ic_result['ic_mean']:.4f} ({'[EMOJI]' if abs_ic > 0.05 else '[EMOJI]' if abs_ic > 0.03 else '[EMOJI]'})")
print(f"  2. [EMOJI]: IR={ic_result['ic_ir']:.4f} ({'[EMOJI]' if ic_ir > 1.0 else '[EMOJI]' if ic_ir > 0.5 else '[EMOJI]'})")
print(f"  3. [EMOJI]: {metrics['annual_return']:.2%}")
print(f"  4. [EMOJI]: {metrics['sharpe_ratio']:.4f}")
print(f"  5. [EMOJI]: {metrics['max_drawdown']:.2%}")
print(f"  6. [EMOJI]: {score}/100")

print("\n[[EMOJI]]")
print()
print("[EMOJI]DuckDB[EMOJI]")
print()
print("[EMOJI]1: [EMOJI]QMT/xtquant[EMOJI]")
print("  1. [EMOJI]QMT[EMOJI]")
print("  2. [EMOJI]: python scripts/download_stocks.py")
print("  3. [EMOJI]DuckDB[EMOJI]")
print()
print("[EMOJI]2: [EMOJI]Tushare[EMOJI]")
print("  1. [EMOJI]: https://tushare.pro")
print("  2. [EMOJI]scripts/[EMOJI]Tushare[EMOJI]")
print("  3. [EMOJI]DuckDB")
print()
print("[EMOJI]3: [EMOJI]CSV[EMOJI]")
print("  1. [EMOJI]CSV[EMOJI]:")
print("     - date: [EMOJI]")
print("     - stock_code: [EMOJI]")
print("     - open, high, low, close, volume: OHLCV[EMOJI]")
print()
print("  2. [EMOJI]DuckDB:")
print("     ```python")
print("     import pandas as pd")
print("     import duckdb")
print()
print("     df = pd.read_csv('your_data.csv')")
print("     conn = duckdb.connect('data/stock_data.ddb')")
print("     conn.execute('CREATE TABLE stock_daily AS SELECT * FROM df')")
print("     conn.close()")
print("     ```")
print()
print("  4. [EMOJI]")
print()
print("[EMOJI]:")
print("  - [EMOJI]: [EMOJI]1[EMOJI]")
print("  - [EMOJI]: [EMOJI]20[EMOJI]")
print("  - [EMOJI]: [EMOJI]")
print("  - [EMOJI]: date, stock_code, close")

print("\n[[EMOJI]]")
print("  - IC[EMOJI]: docs/ic_integration_guide.md")
print("  - [EMOJI]: src/analysis/group_backtest.py")
print("  - [EMOJI]: src/factor_engine/specific_volatility.py")
print("  - [EMOJI]: src/analysis/enhanced_performance.py")

print("\n" + "=" * 80)
