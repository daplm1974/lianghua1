# -*- coding: utf-8 -*-
"""
[EMOJI] - [EMOJI]

[EMOJI] easyxt_backtest [EMOJI]
[EMOJI]

[EMOJI]: [EMOJI]quant
[EMOJI]: 5.0 ([EMOJI] easyxt_backtest [EMOJI])
[EMOJI]: 2025-03-06
"""

import sys
import os
from pathlib import Path
from datetime import datetime

# [EMOJI]Python[EMOJI]
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

print("=" * 70)
print("[COURSE] [EMOJI] easyxt_backtest [EMOJI]")
print("=" * 70)
print()

# [EMOJI] easyxt_backtest [EMOJI]
try:
    from easyxt_backtest import DataManager, BacktestEngine
    from easyxt_backtest.strategies import SmallCapStrategy
    print("[OK] easyxt_backtest [EMOJI]")
    EASYXT_AVAILABLE = True
except ImportError as e:
    print(f"[!] easyxt_backtest [EMOJI]: {e}")
    print("[TIP] [EMOJI]pip install -r requirements.txt")
    EASYXT_AVAILABLE = False


def print_section_header(num, title, description=""):
    """[EMOJI]"""
    print("\n" + "=" * 70)
    print(f"[EMOJI]{num}[EMOJI]: {title}")
    if description:
        print(f"[EMOJI] {description}")
    print("=" * 70)


def wait_for_user(message="[EMOJI]..."):
    """[EMOJI]"""
    input(f"\n[TIP] {message}")


# ============================================================================
# [EMOJI]1[EMOJI]
# ============================================================================

def lesson_1_framework_intro():
    """[EMOJI]1[EMOJI]"""
    print_section_header(1, "easyxt_backtest [EMOJI]",
                         "[EMOJI]")

    print("\n[EMOJI] [EMOJI]")
    print("""
    [EMOJI]
    [EMOJI]                  easyxt_backtest                 [EMOJI]
    [EMOJI]
    [EMOJI]                                                 [EMOJI]
    [EMOJI]  [CHART] DataManager ([EMOJI])                     [EMOJI]
    [EMOJI]    [EMOJI] DuckDB ([EMOJI])                [EMOJI]
    [EMOJI]    [EMOJI] QMT ([EMOJI])                       [EMOJI]
    [EMOJI]    [EMOJI] Tushare ([EMOJI]API)                        [EMOJI]
    [EMOJI]                                                 [EMOJI]
    [EMOJI]  [TARGET] BacktestEngine ([EMOJI])                   [EMOJI]
    [EMOJI]    [EMOJI] [EMOJI]              [EMOJI]
    [EMOJI]    [EMOJI] [EMOJI]            [EMOJI]
    [EMOJI]    [EMOJI] [EMOJI]                   [EMOJI]
    [EMOJI]                                                 [EMOJI]
    [EMOJI]  [UP] Strategy ([EMOJI])                          [EMOJI]
    [EMOJI]    [EMOJI] SmallCapStrategy ([EMOJI])            [EMOJI]
    [EMOJI]    [EMOJI] [EMOJI]...                            [EMOJI]
    [EMOJI]    [EMOJI] [EMOJI] StrategyBase [EMOJI]                   [EMOJI]
    [EMOJI]                                                 [EMOJI]
    [EMOJI]  [CHART] PerformanceAnalyzer ([EMOJI])              [EMOJI]
    [EMOJI]    [EMOJI] [EMOJI]                               [EMOJI]
    [EMOJI]    [EMOJI] [EMOJI]                                 [EMOJI]
    [EMOJI]    [EMOJI] [EMOJI]                                 [EMOJI]
    [EMOJI]                                                 [EMOJI]
    [EMOJI]
    """)

    print("\n[TARGET] [EMOJI]")
    print("  [OK] [EMOJI]")
    print("  [OK] [EMOJI]")
    print("  [OK] [EMOJI]")
    print("  [OK] [EMOJI]")
    print("  [OK] [EMOJI]")

    print("\n[EMOJI] [EMOJI]")
    print("  [EMOJI]1[EMOJI]101[EMOJI]")
    print("  [EMOJI]2[EMOJI]")

    wait_for_user()


# ============================================================================
# [EMOJI]2[EMOJI]
# ============================================================================

def lesson_2_metrics_explanation():
    """[EMOJI]2[EMOJI]"""
    print_section_header(2, "[EMOJI]",
                         "[EMOJI]")

    metrics = {
        "[EMOJI]": {
            "[EMOJI]": "[EMOJI]",
            "[EMOJI]": "([EMOJI] - [EMOJI]) / [EMOJI]",
            "[EMOJI]": "[EMOJI]",
            "[EMOJI]": "15.92% [EMOJI]100[EMOJI]15.92[EMOJI]"
        },
        "[EMOJI]": {
            "[EMOJI]": "[EMOJI]",
            "[EMOJI]": "[EMOJI]",
            "[EMOJI]": ">15%[EMOJI]8-15%[EMOJI]",
            "[EMOJI]": "15.92% [EMOJI]"
        },
        "[EMOJI]": {
            "[EMOJI]": "[EMOJI]",
            "[EMOJI]": "max(([EMOJI] - [EMOJI]) / [EMOJI])",
            "[EMOJI]": "<10%[EMOJI]10-20%[EMOJI]",
            "[EMOJI]": "-25.33% [EMOJI]25.33%"
        },
        "[EMOJI]": {
            "[EMOJI]": "[EMOJI]",
            "[EMOJI]": "([EMOJI] - [EMOJI]) / [EMOJI]",
            "[EMOJI]": ">1[EMOJI]0.5-1[EMOJI]",
            "[EMOJI]": "0.68 [EMOJI]1[EMOJI]0.68[EMOJI]"
        },
        "[EMOJI]": {
            "[EMOJI]": "[EMOJI]",
            "[EMOJI]": "std([EMOJI]) * sqrt(252)",
            "[EMOJI]": "[EMOJI]",
            "[EMOJI]": "20% [EMOJI]"
        },
        "[EMOJI]": {
            "[EMOJI]": "[EMOJI]",
            "[EMOJI]": "[EMOJI] / |[EMOJI]|",
            "[EMOJI]": ">1[EMOJI]>0.5[EMOJI]",
            "[EMOJI]": "0.63 [EMOJI]1%[EMOJI]0.63%[EMOJI]"
        }
    }

    for metric_name, info in metrics.items():
        print(f"\n[EMOJI] {metric_name}")
        print(f"  • [EMOJI]{info['[EMOJI]']}")
        print(f"  • [EMOJI]{info['[EMOJI]']}")
        print(f"  • [EMOJI]{info['[EMOJI]']}")
        print(f"  • [EMOJI]{info['[EMOJI]']}")

    print("\n[CHART] [EMOJI]")
    print("""
    [EMOJI]
    [EMOJI]   [EMOJI]        [EMOJI]  [EMOJI]  [EMOJI]  [EMOJI]  [EMOJI]  [EMOJI]  [EMOJI]  [EMOJI]  [EMOJI]
    [EMOJI]
    [EMOJI] [EMOJI]    [EMOJI] >15%   [EMOJI] 8-15%  [EMOJI] 3-8%   [EMOJI] <3%    [EMOJI]
    [EMOJI] [EMOJI]      [EMOJI] <5%    [EMOJI] 5-10%  [EMOJI] 10-20% [EMOJI] >20%   [EMOJI]
    [EMOJI] [EMOJI]      [EMOJI] >1.0   [EMOJI] 0.5-1.0[EMOJI] 0.2-0.5[EMOJI] <0.2   [EMOJI]
    [EMOJI] [EMOJI]      [EMOJI] >1.0   [EMOJI] 0.5-1.0[EMOJI] 0.3-0.5[EMOJI] <0.3   [EMOJI]
    [EMOJI]
    """)

    wait_for_user()


# ============================================================================
# [EMOJI]3[EMOJI]
# ============================================================================

def lesson_3_practical_demo():
    """[EMOJI]3[EMOJI]"""
    print_section_header(3, "[EMOJI]",
                         "[EMOJI] easyxt_backtest [EMOJI]")

    if not EASYXT_AVAILABLE:
        print("\n[!] [EMOJI]")
        print("[TIP] [EMOJI]")
        return

    print("\n[NOTE] [EMOJI]")
    print("  • [EMOJI]")
    print("  • [EMOJI]N[EMOJI]")
    print("  • [EMOJI]")
    print("  • [EMOJI]")
    print("  • [EMOJI]A[EMOJI]")

    print("\n[EMOJI] [EMOJI]")
    start_date = "20240101"
    end_date = "20241231"
    initial_cash = 1000000
    select_num = 5
    universe_size = 500

    print(f"  • [EMOJI]{start_date} ~ {end_date}")
    print(f"  • [EMOJI]{initial_cash:,} [EMOJI]")
    print(f"  • [EMOJI]{select_num} [EMOJI]")
    print(f"  • [EMOJI]{universe_size} [EMOJI]")

    wait_for_user("[EMOJI]...")

    # [EMOJI]
    print("\n[CHART] [EMOJI]1[EMOJI]...")
    dm = DataManager()
    print("  [OK] [EMOJI]")

    # [EMOJI]
    print("\n[TARGET] [EMOJI]2[EMOJI]...")
    strategy = SmallCapStrategy(
        index_code='399101.SZ',  # [EMOJI]
        select_num=select_num,
        rebalance_freq='monthly'
    )
    strategy.data_manager = dm
    print(f"  [OK] [EMOJI]{select_num}[EMOJI]")

    # [EMOJI]
    print("\n[LAUNCH] [EMOJI]3[EMOJI]...")
    engine = BacktestEngine(
        data_manager=dm,
        initial_cash=initial_cash,
        commission=0.001  # 0.1% [EMOJI]
    )
    print(f"  [OK] [EMOJI]{initial_cash:,} [EMOJI]")

    # [EMOJI]
    print(f"\n[TIME] [EMOJI]4[EMOJI]{start_date} ~ {end_date}[EMOJI]...")
    print("  [EMOJI]...")

    try:
        results = engine.run_backtest(strategy, start_date, end_date)
        print("  [OK] [EMOJI]")

        # [EMOJI]
        display_backtest_results(results, initial_cash)

    except Exception as e:
        print(f"  [X] [EMOJI]{e}")
        print("\n[TIP] [EMOJI]")
        print("  1. [EMOJI]")
        print("  2. [EMOJI]")
        print("  3. [EMOJI]")

        print("\n[EMOJI] [EMOJI]")
        print("  [EMOJI]GUI[EMOJI]")
        print("  cd \"C:\\Users\\Administrator\\Desktop\\miniqmt[EMOJI]\"")
        print("  python run_gui.py")
        print("  [EMOJI] '[EMOJI] Tushare[EMOJI]' → '[MONEY] [EMOJI]'")


def display_backtest_results(results, initial_cash):
    """[EMOJI]"""
    print("\n" + "=" * 70)
    print("[CHART] [EMOJI]")
    print("=" * 70)

    # [EMOJI]
    perf = results.performance
    print(f"\n[MONEY] [EMOJI]")
    print(f"  • [EMOJI]{perf['total_return'] * 100:.2f}%")
    print(f"  • [EMOJI]{perf['annual_return'] * 100:.2f}%")
    print(f"  • [EMOJI]{initial_cash * (1 + perf['total_return']):,.2f} [EMOJI]")

    print(f"\n[!] [EMOJI]")
    print(f"  • [EMOJI]{perf['max_drawdown'] * 100:.2f}%")
    if 'volatility' in perf:
        print(f"  • [EMOJI]{perf['volatility'] * 100:.2f}%")
    print(f"  • [EMOJI]{perf['sharpe_ratio']:.2f}")
    if 'calmar_ratio' in perf:
        print(f"  • [EMOJI]{perf['calmar_ratio']:.2f}")

    print(f"\n[UP] [EMOJI]")
    print(f"  • [EMOJI]{len(results.trades)} [EMOJI]")
    print(f"  • [EMOJI]{len(results.returns)} [EMOJI]")

    if len(results.trades) > 0:
        buy_count = len(results.trades[results.trades['direction'] == 'buy'])
        sell_count = len(results.trades[results.trades['direction'] == 'sell'])
        print(f"  • [EMOJI]{buy_count} [EMOJI]")
        print(f"  • [EMOJI]{sell_count} [EMOJI]")

    # [EMOJI]
    if len(results.trades) > 0:
        print(f"\n[EMOJI] [EMOJI]5[EMOJI]")
        print(results.trades.head().to_string())


# ============================================================================
# [EMOJI]4[EMOJI]
# ============================================================================

def lesson_4_custom_strategy():
    """[EMOJI]4[EMOJI]"""
    print_section_header(4, "[EMOJI]",
                         "[EMOJI]")

    print("\n[NOTE] [EMOJI]")
    print("""
# 1. [EMOJI]
from easyxt_backtest.strategy_base import StrategyBase

# 2. [EMOJI]
class MyCustomStrategy(StrategyBase):
    \"\"\"[EMOJI]\"\"\"

    def __init__(self, param1, param2, **kwargs):
        super().__init__(**kwargs)
        self.param1 = param1
        self.param2 = param2

    def generate_signals(self, date):
        \"\"\"
        [EMOJI]

        [EMOJI]:
            date: [EMOJI] (YYYYMMDD)

        [EMOJI]:
            list: [EMOJI]
                [{'symbol': '000001.SZ', 'action': 'buy', 'weight': 0.5},
                 {'symbol': '000002.SZ', 'action': 'sell', 'weight': 0.5}]
        \"\"\"
        signals = []

        # [EMOJI]
        symbols = self.get_universe(date)  # [EMOJI]
        for symbol in symbols:
            # [EMOJI]
            data = self.data_manager.get_price_data(
                symbol,
                start_date=date,
                end_date=date,
                fields=['open', 'close', 'volume']
            )

            # [EMOJI]
            if self._check_golden_cross(symbol):
                signals.append({
                    'symbol': symbol,
                    'action': 'buy',
                    'weight': 1.0 / len(symbols)  # [EMOJI]
                })

        return signals

    def _check_golden_cross(self, symbol):
        \"\"\"[EMOJI]\"\"\"
        # [EMOJI]
        data = self.data_manager.get_price_data(
            symbol,
            start_date='20230101',
            end_date=datetime.now().strftime('%Y%m%d'),
            fields=['close']
        )

        if data is None or len(data) < 20:
            return False

        # [EMOJI]
        ma5 = data['close'].rolling(5).mean()
        ma20 = data['close'].rolling(20).mean()

        # [EMOJI]
        return ma5.iloc[-1] > ma20.iloc[-1] and ma5.iloc[-2] <= ma20.iloc[-2]


# 3. [EMOJI]
from easyxt_backtest import DataManager, BacktestEngine

dm = DataManager()
strategy = MyCustomStrategy(param1=10, param2=20, data_manager=dm)
engine = BacktestEngine(data_manager=dm, initial_cash=1000000)
results = engine.run_backtest(strategy, '20240101', '20241231')
    """)

    print("\n[TIP] [EMOJI]")
    print("  1. [EMOJI] StrategyBase [EMOJI]")
    print("  2. [EMOJI] generate_signals() [EMOJI]")
    print("  3. [EMOJI]")
    print("  4. [EMOJI] data_manager [EMOJI]")
    print("  5. [EMOJI]")

    print("\n[TARGET] [EMOJI]")
    print("  • [EMOJI]")
    print("  • [EMOJI]")
    print("  • [EMOJI]")
    print("  • [EMOJI]")
    print("  • [EMOJI]")

    wait_for_user()


# ============================================================================
# [EMOJI]5[EMOJI]101[EMOJI]
# ============================================================================

def lesson_5_platform_usage():
    """[EMOJI]5[EMOJI]101[EMOJI]"""
    print_section_header(5, "101[EMOJI]",
                         "[EMOJI]")

    print("\n[LAUNCH] [EMOJI]101[EMOJI]")
    print("""
[EMOJI]
[EMOJI]          [EMOJI]1[EMOJI]                   [EMOJI]
[EMOJI]

[EMOJI]
1[EMOJI]⃣ [EMOJI]
   C:\\Users\\Administrator\\Desktop\\miniqmt[EMOJI]\\101[EMOJI]\\101[EMOJI]

2[EMOJI]⃣ [EMOJI]
   [EMOJI].bat

3[EMOJI]⃣ [EMOJI]
   - [EMOJI]
   - [EMOJI]

[EMOJI]

[EMOJI]
[EMOJI]          [EMOJI]2[EMOJI]                               [EMOJI]
[EMOJI]

# Windows [EMOJI]
cd "C:\\Users\\Administrator\\Desktop\\miniqmt[EMOJI]\\101[EMOJI]\\101[EMOJI]"
python main_app.py

# [EMOJI] Git Bash
cd /c/Users/Administrator/Desktop/miniqmt[EMOJI]/101[EMOJI]/101[EMOJI]
python main_app.py
    """)

    print("\n[EMOJI] [EMOJI]")
    print("""
   [EMOJI]http://127.0.0.1:8510

   [EMOJI]
   http://127.0.0.1:8510
    """)

    print("\n[CHART] [EMOJI]")
    print("""
[EMOJI]
[EMOJI]  [TARGET] [EMOJI] - 101[EMOJI]                         [EMOJI]
[EMOJI]
[EMOJI]          [EMOJI]                                              [EMOJI]
[EMOJI] [EMOJI]   [EMOJI]         [EMOJI]                [EMOJI]
[EMOJI]          [EMOJI]                                              [EMOJI]
[EMOJI] • [EMOJI]   [EMOJI]   [EMOJI]      [EMOJI]
[EMOJI] • [EMOJI]   [EMOJI]   [EMOJI] [EMOJI] [EMOJI]                      [EMOJI]      [EMOJI]
[EMOJI]   [EMOJI]   [EMOJI]   [EMOJI] • [EMOJI]: [2024-01-01]         [EMOJI]      [EMOJI]
[EMOJI] • [EMOJI]   [EMOJI]   [EMOJI] • [EMOJI]: [2024-12-31]         [EMOJI]      [EMOJI]
[EMOJI]   [EMOJI] [EMOJI]   [EMOJI]      [EMOJI]
[EMOJI] • [EMOJI]   [EMOJI]                                              [EMOJI]
[EMOJI]   [EMOJI]   [EMOJI]   [EMOJI]      [EMOJI]
[EMOJI]          [EMOJI]   [EMOJI] [CHART] [EMOJI]                      [EMOJI]      [EMOJI]
[EMOJI]          [EMOJI]   [EMOJI] • [EMOJI]: [5[EMOJI]]               [EMOJI]      [EMOJI]
[EMOJI]          [EMOJI]   [EMOJI] • [EMOJI]: [500[EMOJI]]               [EMOJI]      [EMOJI]
[EMOJI]          [EMOJI]   [EMOJI]      [EMOJI]
[EMOJI]          [EMOJI]                                              [EMOJI]
[EMOJI]          [EMOJI]   [EMOJI]      [EMOJI]
[EMOJI]          [EMOJI]   [EMOJI] [MONEY] [EMOJI]                      [EMOJI]      [EMOJI]
[EMOJI]          [EMOJI]   [EMOJI] • [EMOJI]: [1000000[EMOJI]]          [EMOJI]      [EMOJI]
[EMOJI]          [EMOJI]   [EMOJI]      [EMOJI]
[EMOJI]          [EMOJI]                                              [EMOJI]
[EMOJI]          [EMOJI]   [  [LAUNCH] [EMOJI]  ]                         [EMOJI]
[EMOJI]          [EMOJI]                                              [EMOJI]
[EMOJI]
    """)

    print("\n[NOTE] [EMOJI]")
    print("""
[EMOJI]

[EMOJI]1[EMOJI]
[EMOJI]
• [EMOJI] "[TARGET] [EMOJI]"
• [EMOJI]

[EMOJI]

[EMOJI]2[EMOJI]
[EMOJI]

[EMOJI] [EMOJI]
  • [EMOJI] 2024-01-01
  • [EMOJI] 2024-12-31
  [TIP] [EMOJI]3[EMOJI]

[CHART] [EMOJI]
  • [EMOJI] 5[EMOJI]5[EMOJI]
  • [EMOJI] 500[EMOJI]500[EMOJI]
  [TIP] [EMOJI]

[MONEY] [EMOJI]
  • [EMOJI] 1000000[EMOJI]100[EMOJI]
  [TIP] [EMOJI]

[EMOJI]

[EMOJI]3[EMOJI]
[EMOJI]
• [EMOJI] "[LAUNCH] [EMOJI]" [EMOJI]
• [EMOJI]1-3[EMOJI]
• [EMOJI]

[EMOJI]

[EMOJI]4[EMOJI]
[EMOJI]
[EMOJI]5[EMOJI]

[CHART] [EMOJI]
  • [EMOJI]
  • [EMOJI]
  • [EMOJI]

[UP] [EMOJI]
  • [EMOJI]
  • [EMOJI]

[EMOJI] [EMOJI]
  • [EMOJI]
  • [EMOJI]

[EMOJI] [EMOJI]
  • [EMOJI]
  • [EMOJI]

[EMOJI] [EMOJI]
  • JSON[EMOJI]
  • [EMOJI]

[EMOJI]
    """)

    print("\n[TIP] [EMOJI]")
    print("""
  [OK] [EMOJI]
     • [EMOJI]
     • [EMOJI]
     • [EMOJI]

  [OK] [EMOJI]
     • [EMOJI]
     • [EMOJI]
     • [EMOJI]

  [OK] [EMOJI]
     • [EMOJI]
     • [EMOJI]
     - [EMOJI]

  [OK] [EMOJI]
     • [EMOJI]
     • [EMOJI]
     • [EMOJI]
    """)

    print("\n[!] [EMOJI]")
    print("""
1. [EMOJI]
   • [EMOJI]
   • [EMOJI]"[EMOJI]"[EMOJI]API[EMOJI]

2. [EMOJI]
   • [EMOJI]3-6[EMOJI]
   • [EMOJI]

3. [EMOJI]
   • [EMOJI]
   • [EMOJI]"[EMOJI]"[EMOJI]

4. [EMOJI]
   • [EMOJI]
   • [EMOJI]JSON[EMOJI]
    """)

    print("\n[TARGET] [EMOJI]")
    print("""
[EMOJI]

  • [EMOJI]2024-01-01
  • [EMOJI]2024-03-31
  • [EMOJI]3[EMOJI]
  • [EMOJI]100[EMOJI]
  • [EMOJI]100000[EMOJI]

[EMOJI]1[EMOJI]
    """)

    wait_for_user()


# ============================================================================
# [EMOJI]6[EMOJI]
# ============================================================================

def lesson_6_data_preparation():
    """[EMOJI]6[EMOJI]"""
    print_section_header(6, "[EMOJI]",
                         "[EMOJI]")

    print("\n[EMOJI] [EMOJI]")

    print("\n[EMOJI]1[EMOJI]GUI[EMOJI]")
    print("""
# 1. [EMOJI]GUI
cd "C:\\Users\\Administrator\\Desktop\\miniqmt[EMOJI]"
python run_gui.py

# 2. [EMOJI]
[EMOJI] "[EMOJI] Tushare[EMOJI]" → "[MONEY] [EMOJI]"

# 3. [EMOJI]
Token[EMOJI] .env [EMOJI]
[EMOJI] "2024[EMOJI]" [EMOJI]

# 4. [EMOJI]
[EMOJI] "[LAUNCH] [EMOJI]A[EMOJI]"
[EMOJI] 5-10 [EMOJI]

# 5. [EMOJI]
[EMOJI]
    """)

    print("\n[EMOJI]2[EMOJI]API[EMOJI]")
    print("""
[EMOJI]
1. [EMOJI] Tushare API [EMOJI]
2. [EMOJI]
3. [EMOJI] TUSHARE_TOKEN
    """)

    print("\n[CHART] [EMOJI]")
    print("""
1. [EMOJI] DuckDB[EMOJI]
   • [EMOJI]
   • [EMOJI]
   • [EMOJI]

2. [EMOJI] Tushare[EMOJI]API[EMOJI]
   • [EMOJI]
   • [EMOJI]
   • [EMOJI]

3. [!] QMT[EMOJI]
   • [EMOJI]
   • [EMOJI]QMT
   • [EMOJI]
    """)

    print("\n[TIP] [EMOJI]")
    print("""
# [EMOJI]
from easyxt_backtest import DataManager

dm = DataManager()
# [EMOJI]
# [EMOJI]
    """)

    wait_for_user()


# ============================================================================
# [EMOJI]
# ============================================================================

def main():
    """[EMOJI]"""
    print("\n[TARGET] [EMOJI]")
    print("  1[EMOJI]⃣ [EMOJI] - [EMOJI]")
    print("  2[EMOJI]⃣ [EMOJI] - [EMOJI]")
    print("  3[EMOJI]⃣ [EMOJI] - [EMOJI]")
    print("  4[EMOJI]⃣ [EMOJI] - [EMOJI]")
    print("  5[EMOJI]⃣ [EMOJI] - [EMOJI]")
    print("  6[EMOJI]⃣ [EMOJI] - [EMOJI]")

    wait_for_user("[EMOJI]")

    # [EMOJI]
    lesson_1_framework_intro()
    lesson_2_metrics_explanation()

    if EASYXT_AVAILABLE:
        lesson_3_practical_demo()
    else:
        print("\n[!] [EMOJI]")

    lesson_4_custom_strategy()
    lesson_5_platform_usage()
    lesson_6_data_preparation()

    # [EMOJI]
    print("\n" + "=" * 70)
    print("[EMOJI] [EMOJI]")
    print("=" * 70)

    print("\n[OK] [EMOJI]")
    print("  • easyxt_backtest [EMOJI]")
    print("  • [EMOJI]")
    print("  • [EMOJI]")
    print("  • [EMOJI]")
    print("  • 101[EMOJI]")
    print("  • [EMOJI]")

    print("\n[LAUNCH] [EMOJI]")
    print("  1. [EMOJI]")
    print("     cd \"101[EMOJI]/101[EMOJI]\"")
    print("     python main_app.py")
    print("\n  2. [EMOJI]")
    print("     - [EMOJI]-3[EMOJI].md")
    print("     - [EMOJI]-[EMOJI].md")
    print("\n  3. [EMOJI]")
    print("     [EMOJI] easyxt_backtest/examples/")
    print("     [EMOJI] StrategyBase [EMOJI]")

    print("\n[BOOK] [EMOJI]")
    print("  • 101[EMOJI]101[EMOJI]/101[EMOJI]/")
    print("  • [EMOJI]easyxt_backtest/")
    print("  • [EMOJI]easyxt_backtest/examples/")

    print("\n[TIP] [EMOJI]")
    print("  [EMOJI]")
    print("  [EMOJI]")

    print("\n" + "=" * 70)


if __name__ == "__main__":
    main()
