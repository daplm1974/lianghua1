"""
[EMOJI] - DuckDB[EMOJI]

[EMOJI]
1. [EMOJI]DuckDB[EMOJI]
2. [EMOJI]
3. [EMOJI]

[EMOJI]
1. [EMOJI]DuckDB[EMOJI]: D:/StockData/stock_data.ddb
2. [EMOJI]
3. [EMOJI]

[EMOJI]EasyXT[EMOJI]
[EMOJI]2026-02-06
"""

import sys
import os
import pandas as pd
import numpy as np
from datetime import datetime, timedelta

easy_xt_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'easy_xt'))
if easy_xt_dir not in sys.path:
    sys.path.insert(0, easy_xt_dir)

# [EMOJI]DuckDBDataReader
from easy_xt.data_api import DuckDBDataReader

# ============================================================
# [EMOJI]
# ============================================================

# DuckDB[EMOJI]
def _detect_duckdb_path():
    """[EMOJI]DuckDB[EMOJI]"""
    candidates = [
        'D:/StockData/stock_data.ddb',
        'C:/StockData/stock_data.ddb',
        'E:/StockData/stock_data.ddb',
        './data/stock_data.ddb',
    ]
    for path in candidates:
        if os.path.exists(path):
            return path
    # [EMOJI]
    env = os.environ.get('DUCKDB_PATH')
    if env:
        return env
    # [EMOJI]
    return candidates[0]

DUCKDB_PATH = _detect_duckdb_path()

# [EMOJI]
# [EMOJI]
# SELECT DISTINCT stock_code FROM stock_daily ORDER BY stock_code LIMIT 100;
STOCK_LIST = [
    '000001.SZ',  # [EMOJI]
    '000002.SZ',  # [EMOJI]A
    '000004.SZ',  # [EMOJI]
    '600000.SH',  # [EMOJI]
    '600036.SH',  # [EMOJI]
    '600519.SH',  # [EMOJI]
    '000858.SZ',  # [EMOJI]
    '002475.SZ',  # [EMOJI]
]

# [EMOJI]
START_DATE = '2024-01-01'
END_DATE = None  # None[EMOJI]

# ============================================================
# [EMOJI]
# ============================================================

class FactorCalculator:
    """[EMOJI]"""

    def __init__(self, data_reader):
        self.dr = data_reader

    def calculate_all_factors(self, stock_list, start_date, end_date=None):
        """[EMOJI]"""
        print("\n" + "=" * 70)
        print("[EMOJI]")
        print("=" * 70)

        # [EMOJI]
        print(f"\n[[EMOJI]] {len(stock_list)} [EMOJI]")
        data = self.dr.get_market_data(stock_list, start_date, end_date)

        if data.empty:
            print("[[EMOJI]] [EMOJI]")
            return None

        # [EMOJI]
        results = {}

        # 1. [EMOJI]
        results['momentum'] = self._calculate_momentum(data)

        # 2. [EMOJI]
        results['volatility'] = self._calculate_volatility(data)

        # 3. [EMOJI]
        results['volume_price'] = self._calculate_volume_price(data)

        # 4. [EMOJI]
        results['technical'] = self._calculate_technical(data)

        # 5. [EMOJI]
        results['scores'] = self._calculate_composite_score(data, results)

        return results

    def _calculate_momentum(self, data):
        """[EMOJI]"""
        print("\n[[EMOJI]] [EMOJI]...")
        results = []

        for stock in data['stock_code'].unique():
            stock_data = data[data['stock_code'] == stock].sort_values('date')

            if len(stock_data) >= 20:
                recent_close = stock_data['close'].iloc[-1]

                for period in [5, 10, 20, 60]:
                    if len(stock_data) >= period:
                        past_close = stock_data['close'].iloc[-period]
                        momentum = (recent_close - past_close) / past_close * 100

                        results.append({
                            'stock_code': stock,
                            'period': f'{period}[EMOJI]',
                            'momentum_pct': round(momentum, 2),
                            'current_price': round(recent_close, 2)
                        })

        return pd.DataFrame(results)

    def _calculate_volatility(self, data):
        """[EMOJI]"""
        print("\n[[EMOJI]] [EMOJI]...")
        results = []

        for stock in data['stock_code'].unique():
            stock_data = data[data['stock_code'] == stock].sort_values('date')

            if len(stock_data) >= 20:
                recent_data = stock_data.tail(20)
                returns = recent_data['close'].pct_change().dropna()

                if len(returns) > 0:
                    volatility = returns.std() * np.sqrt(252) * 100
                    max_drawdown = self._calculate_max_drawdown(recent_data['close'])

                    results.append({
                        'stock_code': stock,
                        'volatility_pct': round(volatility, 2),
                        'max_drawdown_pct': round(max_drawdown, 2),
                        'price_range': round(recent_data['high'].max() / recent_data['low'].min() - 1, 4)
                    })

        return pd.DataFrame(results)

    def _calculate_max_drawdown(self, price_series):
        """[EMOJI]"""
        cummax = price_series.cummax()
        drawdown = (price_series - cummax) / cummax
        return drawdown.min() * 100

    def _calculate_volume_price(self, data):
        """[EMOJI]"""
        print("\n[[EMOJI]] [EMOJI]...")
        results = []

        for stock in data['stock_code'].unique():
            stock_data = data[data['stock_code'] == stock].sort_values('date')

            if len(stock_data) >= 20 and 'volume' in stock_data.columns:
                recent_data = stock_data.tail(20)
                avg_volume = recent_data['volume'].mean()
                recent_volume = recent_data['volume'].iloc[-1]
                volume_ratio = recent_volume / avg_volume if avg_volume > 0 else 0

                # [EMOJI]
                price_change = stock_data['close'].pct_change().iloc[-1]
                volume_change = stock_data['volume'].pct_change().iloc[-1]
                trend = 'positive' if (price_change > 0 and volume_change > 0) or (price_change < 0 and volume_change < 0) else 'negative'

                results.append({
                    'stock_code': stock,
                    'volume_ratio': round(volume_ratio, 2),
                    'trend': trend
                })

        return pd.DataFrame(results)

    def _calculate_technical(self, data):
        """[EMOJI]"""
        print("\n[[EMOJI]] [EMOJI]...")
        results = []

        for stock in data['stock_code'].unique():
            stock_data = data[data['stock_code'] == stock].sort_values('date')

            if len(stock_data) >= 60:
                current_price = stock_data['close'].iloc[-1]

                for period in [5, 10, 20, 60]:
                    if len(stock_data) >= period:
                        ma = stock_data['close'].tail(period).mean()

                        results.append({
                            'stock_code': stock,
                            'period': f'MA{period}',
                            'ma_value': round(ma, 2),
                            'price_vs_ma_pct': round((current_price - ma) / ma * 100, 2),
                            'signal': 'above' if current_price > ma else 'below'
                        })

        return pd.DataFrame(results)

    def _calculate_composite_score(self, data, factor_results):
        """[EMOJI]"""
        print("\n[[EMOJI]] [EMOJI]...")
        scores = {}

        momentum_20 = factor_results['momentum']
        volatility = factor_results['volatility']
        volume_price = factor_results['volume_price']
        technical = factor_results['technical']

        for stock in data['stock_code'].unique():
            score = 0
            count = 0

            # [EMOJI]
            if not momentum_20.empty:
                stock_mom = momentum_20[momentum_20['period'] == '20[EMOJI]']
                if not stock_mom.empty and stock in stock_mom['stock_code'].values:
                    mom_val = stock_mom[stock_mom['stock_code'] == stock]['momentum_pct'].iloc[0]
                    score += min(mom_val / 5, 10)
                    count += 1

            # [EMOJI]
            if not volatility.empty:
                stock_vol = volatility[volatility['stock_code'] == stock]
                if not stock_vol.empty:
                    vol_val = stock_vol['volatility_pct'].iloc[0]
                    score += max(10 - vol_val / 3, 0)
                    count += 1

            # [EMOJI]
            if not volume_price.empty:
                stock_vp = volume_price[volume_price['stock_code'] == stock]
                if not stock_vp.empty and stock_vp['trend'].iloc[0] == 'positive':
                    score += 5
                    count += 1

            # [EMOJI]
            if not technical.empty:
                stock_tech = technical[(technical['stock_code'] == stock) & (technical['period'] == 'MA20')]
                if not stock_tech.empty and stock_tech['signal'].iloc[0] == 'above':
                    score += 5
                    count += 1

            scores[stock] = {
                'total_score': round(score, 2),
                'max_score': count * 10,
                'rating': self._get_rating(score, count * 10)
            }

        return pd.DataFrame(scores).T

    def _get_rating(self, score, max_score):
        """[EMOJI]"""
        ratio = score / max_score if max_score > 0 else 0
        if ratio > 0.7:
            return 'A ([EMOJI])'
        elif ratio > 0.5:
            return 'B ([EMOJI])'
        elif ratio > 0.3:
            return 'C ([EMOJI])'
        else:
            return 'D ([EMOJI])'


# ============================================================
# [EMOJI]
# ============================================================

def generate_report(factor_results):
    """[EMOJI]"""
    print("\n" + "=" * 70)
    print("[EMOJI]")
    print("=" * 70)

    if factor_results is None:
        print("\n[[EMOJI]] [EMOJI]")
        return

    # 1. [EMOJI]
    if 'scores' in factor_results and not factor_results['scores'].empty:
        print("\n[1] [EMOJI]")
        print("-" * 70)
        scores_sorted = factor_results['scores'].sort_values('total_score', ascending=False)
        for idx, row in scores_sorted.iterrows():
            print(f"\n[EMOJI]: {idx}")
            print(f"  [EMOJI]: {row['total_score']:.2f} / {row['max_score']:.2f}")
            print(f"  [EMOJI]: {row['rating']}")

    # 2. [EMOJI]
    if 'momentum' in factor_results and not factor_results['momentum'].empty:
        print("\n\n[2] [EMOJI]20[EMOJI]")
        print("-" * 70)
        momentum_20 = factor_results['momentum'][factor_results['momentum']['period'] == '20[EMOJI]']
        print(momentum_20.sort_values('momentum_pct', ascending=False).to_string(index=False))

    # 3. [EMOJI]
    if 'volatility' in factor_results and not factor_results['volatility'].empty:
        print("\n\n[3] [EMOJI]")
        print("-" * 70)
        print(factor_results['volatility'].sort_values('volatility_pct').to_string(index=False))

    # 4. [EMOJI]
    if 'volume_price' in factor_results and not factor_results['volume_price'].empty:
        print("\n\n[4] [EMOJI]")
        print("-" * 70)
        print(factor_results['volume_price'].to_string(index=False))

    # 5. [EMOJI]
    if 'technical' in factor_results and not factor_results['technical'].empty:
        print("\n\n[5] [EMOJI]MA20[EMOJI]")
        print("-" * 70)
        ma20 = factor_results['technical'][factor_results['technical']['period'] == 'MA20']
        print(ma20[['stock_code', 'ma_value', 'signal']].to_string(index=False))

    print("\n" + "=" * 70)
    print("[EMOJI]")
    print("=" * 70)


# ============================================================
# [EMOJI]
# ============================================================

def main():
    """[EMOJI]"""
    print("=" * 70)
    print("[EMOJI] - DuckDB[EMOJI]")
    print("=" * 70)

    # 1. [EMOJI]
    print("\n[[EMOJI]1] [EMOJI]")
    print("-" * 70)
    reader = DuckDBDataReader(DUCKDB_PATH)

    if reader.conn is None:
        print("\n[[EMOJI]] [EMOJI]")
        return

    # 2. [EMOJI]
    print("\n[[EMOJI]2] [EMOJI]")
    print("-" * 70)
    all_stocks = reader.get_stock_list(limit=20)
    print(f"[OK] [EMOJI]: {len(all_stocks)} [EMOJI]20[EMOJI]")
    print(f"  {', '.join(all_stocks)}")

    # [EMOJI]
    print(f"\n[[EMOJI]]")
    for stock in STOCK_LIST[:3]:
        info = reader.get_stock_info(stock)
        if info is not None:
            print(f"  {stock}: {info['first_date']} [EMOJI] {info['last_date']}, {info['data_count']} [EMOJI]")

    # 3. [EMOJI]
    print(f"\n[[EMOJI]3] [EMOJI] ({len(STOCK_LIST)} [EMOJI])")
    print("-" * 70)
    calculator = FactorCalculator(reader)

    results = calculator.calculate_all_factors(STOCK_LIST, START_DATE, END_DATE)

    # 4. [EMOJI]
    print(f"\n[[EMOJI]4] [EMOJI]")
    print("-" * 70)
    generate_report(results)

    # 5. [EMOJI]
    reader.close()

    print(f"\n[[EMOJI]]")
    print(f"1. [EMOJI]: {DUCKDB_PATH}")
    print(f"2. [EMOJI]: {len(STOCK_LIST)}")
    print(f"3. [EMOJI]: {START_DATE} [EMOJI]")
    print(f"4. [EMOJI] STOCK_LIST [EMOJI]")


if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        print(f"\n[ERROR] [EMOJI]: {e}")
        import traceback
        traceback.print_exc()
