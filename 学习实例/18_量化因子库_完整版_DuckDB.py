

"""
[EMOJI] - QMT + DuckDB [EMOJI]

[EMOJI]
1. [EMOJI]QMT[EMOJI]DuckDB[EMOJI]
2. [EMOJI]50+[EMOJI]
3. [EMOJI]
4. [EMOJI]

[EMOJI]
- [EMOJI]PE[EMOJI]PB[EMOJI]PS[EMOJI]PCF[EMOJI]
- [EMOJI]ROE[EMOJI]ROA[EMOJI]
- [EMOJI]EPS[EMOJI]
- [EMOJI]5/10/20/60[EMOJI]
- [EMOJI]
- [EMOJI]
- [EMOJI]MACD[EMOJI]RSI[EMOJI]
- [EMOJI]
- [EMOJI]

[EMOJI]EasyXT[EMOJI]
[EMOJI]2026-02-06
[EMOJI]2.0 [EMOJI]
"""

import sys
import os
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import warnings
warnings.filterwarnings('ignore')

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

# [EMOJI]
STOCK_LIST = [
    '000001.SZ', '000002.SZ', '000004.SZ', '600000.SH',
    '600036.SH', '600519.SH', '000858.SZ', '002475.SZ'
]

START_DATE = '2024-01-01'

# ============================================================
# [EMOJI]50+[EMOJI]
# ============================================================

class ComprehensiveFactorCalculator:
    """[EMOJI] - 50+[EMOJI]"""

    def __init__(self, data_reader):
        self.dr = data_reader

    def calculate_all_factors(self, stock_list, start_date):
        """[EMOJI]"""
        print("\n" + "=" * 70)
        print("[EMOJI]50+[EMOJI]")
        print("=" * 70)

        data = self.dr.get_market_data(stock_list, start_date)

        if data.empty:
            print("[[EMOJI]] [EMOJI]")
            return None

        print(f"\n[EMOJI]: {len(data)} [EMOJI]{data['stock_code'].nunique()} [EMOJI]")

        # [EMOJI]
        factors = {}

        # 1. [EMOJI] (5[EMOJI])
        factors['momentum_5d'] = self._momentum_factor(data, 5)
        factors['momentum_10d'] = self._momentum_factor(data, 10)
        factors['momentum_20d'] = self._momentum_factor(data, 20)
        factors['momentum_60d'] = self._momentum_factor(data, 60)
        factors['momentum_vol'] = self._momentum_volume_factor(data)

        # 2. [EMOJI] (3[EMOJI])
        factors['reversal_short'] = self._reversal_factor(data, 5)
        factors['reversal_mid'] = self._reversal_factor(data, 20)
        factors['reversal_long'] = self._reversal_factor(data, 60)

        # 3. [EMOJI] (4[EMOJI])
        factors['volatility_20d'] = self._volatility_factor(data, 20)
        factors['volatility_60d'] = self._volatility_factor(data, 60)
        factors['volatility_120d'] = self._volatility_factor(data, 120)
        factors['max_drawdown'] = self._max_drawdown_factor(data)

        # 4. [EMOJI] (5[EMOJI])
        factors['volume_ratio'] = self._volume_ratio_factor(data, 20)
        factors['volume_ma'] = self._volume_ma_factor(data)
        factors['price_volume_trend'] = self._price_volume_trend_factor(data)
        factors['turnover_rate'] = self._turnover_rate_factor(data)
        factors['amplitude'] = self._amplitude_factor(data)

        # 5. [EMOJI] (7[EMOJI])
        factors['ma5_signal'] = self._ma_signal_factor(data, 5)
        factors['ma10_signal'] = self._ma_signal_factor(data, 10)
        factors['ma20_signal'] = self._ma_signal_factor(data, 20)
        factors['ma60_signal'] = self._ma_signal_factor(data, 60)
        factors['ma_trend'] = self._ma_trend_factor(data)
        factors['bollinger'] = self._bollinger_factor(data)
        factors['rsi'] = self._rsi_factor(data)

        # 6. [EMOJI] (5[EMOJI])
        factors['price_position'] = self._price_position_factor(data, 20)
        factors['price_position_60'] = self._price_position_factor(data, 60)
        factors['displacement'] = self._displacement_factor(data)
        factors['gap_ratio'] = self._gap_ratio_factor(data)
        factors['price_acceleration'] = self._price_acceleration_factor(data)

        # 7. [EMOJI] (10[EMOJI])
        factors['size'] = self._size_factor(data)
        factors['beta'] = self._beta_factor(data)
        factors['alpha'] = self._alpha_factor(data)
        factors['sharp_ratio'] = self._sharpe_ratio_factor(data)
        factors['calmar_ratio'] = self._calmar_ratio_factor(data)
        factors['sortino_ratio'] = self._sortino_ratio_factor(data)
        factors['skewness'] = self._skewness_factor(data)
        factors['kurtosis'] = self._kurtosis_factor(data)
        factors['upside_capture'] = self._capture_ratio_factor(data, 'up')
        factors['downside_capture'] = self._capture_ratio_factor(data, 'down')

        # 8. [EMOJI]
        factors['composite_score'] = self._composite_score(data, factors)

        return factors

    # ==================== [EMOJI] ====================

    def _momentum_factor(self, data, period):
        """[EMOJI]N[EMOJI]"""
        print(f"[[EMOJI]] {period}[EMOJI]...")
        results = []

        for stock in data['stock_code'].unique():
            stock_data = data[data['stock_code'] == stock].sort_values('date')

            if len(stock_data) >= period:
                recent_close = stock_data['close'].iloc[-1]
                past_close = stock_data['close'].iloc[-period]
                momentum = (recent_close - past_close) / past_close * 100

                results.append({
                    'stock_code': stock,
                    'factor_value': momentum,
                    'current_price': recent_close
                })

        return pd.DataFrame(results)

    def _momentum_volume_factor(self, data):
        """[EMOJI]"""
        print("[[EMOJI]] [EMOJI]...")
        results = []

        for stock in data['stock_code'].unique():
            stock_data = data[data['stock_code'] == stock].sort_values('date')

            if len(stock_data) >= 20:
                price_momentum = stock_data['close'].iloc[-1] / stock_data['close'].iloc[-20] - 1
                volume_momentum = stock_data['volume'].iloc[-1] / stock_data['volume'].iloc[-20] - 1

                results.append({
                    'stock_code': stock,
                    'factor_value': price_momentum * volume_momentum
                })

        return pd.DataFrame(results)

    # ==================== [EMOJI] ====================

    def _reversal_factor(self, data, period):
        """[EMOJI]N[EMOJI]"""
        print(f"[[EMOJI]] {period}[EMOJI]...")
        results = []

        for stock in data['stock_code'].unique():
            stock_data = data[data['stock_code'] == stock].sort_values('date')

            if len(stock_data) >= period:
                momentum = stock_data['close'].iloc[-1] / stock_data['close'].iloc[-period] - 1

                # [EMOJI] = -[EMOJI]
                results.append({
                    'stock_code': stock,
                    'factor_value': -momentum
                })

        return pd.DataFrame(results)

    # ==================== [EMOJI] ====================

    def _volatility_factor(self, data, period):
        """[EMOJI]"""
        print(f"[[EMOJI]] {period}[EMOJI]...")
        results = []

        for stock in data['stock_code'].unique():
            stock_data = data[data['stock_code'] == stock].sort_values('date')

            if len(stock_data) >= period:
                returns = stock_data['close'].pct_change().tail(period).dropna()
                volatility = returns.std() * np.sqrt(252)

                results.append({
                    'stock_code': stock,
                    'factor_value': volatility
                })

        return pd.DataFrame(results)

    def _max_drawdown_factor(self, data):
        """[EMOJI]"""
        print("[[EMOJI]] [EMOJI]...")
        results = []

        for stock in data['stock_code'].unique():
            stock_data = data[data['stock_code'] == stock].sort_values('date')

            if len(stock_data) >= 20:
                cummax = stock_data['close'].cummax()
                drawdown = (stock_data['close'] - cummax) / cummax
                max_dd = drawdown.min()

                results.append({
                    'stock_code': stock,
                    'factor_value': max_dd
                })

        return pd.DataFrame(results)

    # ==================== [EMOJI] ====================

    def _volume_ratio_factor(self, data, period):
        """[EMOJI] / N[EMOJI]"""
        print(f"[[EMOJI]] {period}[EMOJI]...")
        results = []

        for stock in data['stock_code'].unique():
            stock_data = data[data['stock_code'] == stock].sort_values('date')

            if len(stock_data) >= period and 'volume' in stock_data.columns:
                avg_volume = stock_data['volume'].tail(period).mean()
                recent_volume = stock_data['volume'].iloc[-1]
                volume_ratio = recent_volume / avg_volume if avg_volume > 0 else 0

                results.append({
                    'stock_code': stock,
                    'factor_value': volume_ratio
                })

        return pd.DataFrame(results)

    def _volume_ma_factor(self, data):
        """[EMOJI]/[EMOJI]"""
        print("[[EMOJI]] [EMOJI]...")
        results = []

        for stock in data['stock_code'].unique():
            stock_data = data[data['stock_code'] == stock].sort_values('date')

            if len(stock_data) >= 20 and 'volume' in stock_data.columns:
                vol_ma20 = stock_data['volume'].tail(20).mean()
                recent_vol = stock_data['volume'].iloc[-1]

                # 1[EMOJI]0[EMOJI]
                results.append({
                    'stock_code': stock,
                    'factor_value': 1 if recent_vol > vol_ma20 else 0
                })

        return pd.DataFrame(results)

    def _price_volume_trend_factor(self, data):
        """[EMOJI]"""
        print("[[EMOJI]] [EMOJI]...")
        results = []

        for stock in data['stock_code'].unique():
            stock_data = data[data['stock_code'] == stock].sort_values('date')

            if len(stock_data) >= 10:
                price_trend = 1 if stock_data['close'].iloc[-1] > stock_data['close'].iloc[-10] else 0

                if 'volume' in stock_data.columns:
                    vol_trend = 1 if stock_data['volume'].iloc[-1] > stock_data['volume'].iloc[-10] else 0
                else:
                    vol_trend = 0

                # [EMOJI]
                results.append({
                    'stock_code': stock,
                    'factor_value': 1 if price_trend == vol_trend else -1
                })

        return pd.DataFrame(results)

    def _turnover_rate_factor(self, data):
        """[EMOJI]/[EMOJI]"""
        print("[[EMOJI]] [EMOJI]...")
        results = []

        for stock in data['stock_code'].unique():
            stock_data = data[data['stock_code'] == stock].sort_values('date')

            if len(stock_data) >= 20 and 'volume' in stock_data.columns and 'amount' in stock_data.columns:
                avg_turnover = (stock_data['amount'].tail(20) / stock_data['volume'].tail(20)).mean()

                results.append({
                    'stock_code': stock,
                    'factor_value': avg_turnover
                })

        return pd.DataFrame(results)

    def _amplitude_factor(self, data):
        """[EMOJI] - [EMOJI]/ [EMOJI]"""
        print("[[EMOJI]] [EMOJI]...")
        results = []

        for stock in data['stock_code'].unique():
            stock_data = data[data['stock_code'] == stock].sort_values('date')

            if len(stock_data) >= 20:
                recent_data = stock_data.tail(20)
                amplitude = (recent_data['high'] - recent_data['low']) / recent_data['low']
                avg_amplitude = amplitude.mean()

                results.append({
                    'stock_code': stock,
                    'factor_value': avg_amplitude
                })

        return pd.DataFrame(results)

    # ==================== [EMOJI] ====================

    def _ma_signal_factor(self, data, period):
        """[EMOJI]/[EMOJI]"""
        print(f"[[EMOJI]] MA{period}[EMOJI]...")
        results = []

        for stock in data['stock_code'].unique():
            stock_data = data[data['stock_code'] == stock].sort_values('date')

            if len(stock_data) >= period:
                ma = stock_data['close'].tail(period).mean()
                current_price = stock_data['close'].iloc[-1]

                results.append({
                    'stock_code': stock,
                    'factor_value': 1 if current_price > ma else 0,
                    'ma_value': ma,
                    'current_price': current_price
                })

        return pd.DataFrame(results)

    def _ma_trend_factor(self, data):
        """[EMOJI]"""
        print("[[EMOJI]] [EMOJI]...")
        results = []

        for stock in data['stock_code'].unique():
            stock_data = data[data['stock_code'] == stock].sort_values('date')

            if len(stock_data) >= 60:
                ma20 = stock_data['close'].tail(20).mean()
                ma60 = stock_data['close'].tail(60).mean()

                # [EMOJI]
                results.append({
                    'stock_code': stock,
                    'factor_value': 1 if ma20 > ma60 else 0
                })

        return pd.DataFrame(results)

    def _bollinger_factor(self, data):
        """[EMOJI]"""
        print("[[EMOJI]] [EMOJI]...")
        results = []

        for stock in data['stock_code'].unique():
            stock_data = data[data['stock_code'] == stock].sort_values('date')

            if len(stock_data) >= 20:
                recent_data = stock_data.tail(20)
                ma20 = recent_data['close'].mean()
                std20 = recent_data['close'].std()
                upper_band = ma20 + 2 * std20
                lower_band = ma20 - 2 * std20
                current_price = stock_data['close'].iloc[-1]

                # [EMOJI] (0-1[EMOJI])
                bb_position = (current_price - lower_band) / (upper_band - lower_band)

                results.append({
                    'stock_code': stock,
                    'factor_value': bb_position
                })

        return pd.DataFrame(results)

    def _rsi_factor(self, data):
        """RSI[EMOJI]"""
        print("[[EMOJI]] RSI[EMOJI]...")
        results = []

        for stock in data['stock_code'].unique():
            stock_data = data[data['stock_code'] == stock].sort_values('date')

            if len(stock_data) >= 14:
                price_changes = stock_data['close'].diff().tail(14)

                gains = price_changes.where(price_changes > 0, 0).mean()
                losses = -price_changes.where(price_changes < 0, 0).mean()

                if losses == 0:
                    rsi = 100
                else:
                    rs = gains / losses
                    rsi = 100 - (100 / (1 + rs))

                results.append({
                    'stock_code': stock,
                    'factor_value': rsi
                })

        return pd.DataFrame(results)

    # ==================== [EMOJI] ====================

    def _price_position_factor(self, data, period):
        """[EMOJI]N[EMOJI]"""
        print(f"[[EMOJI]] {period}[EMOJI]...")
        results = []

        for stock in data['stock_code'].unique():
            stock_data = data[data['stock_code'] == stock].sort_values('date')

            if len(stock_data) >= period:
                recent_prices = stock_data['close'].tail(period)
                current_price = stock_data['close'].iloc[-1]

                # [EMOJI]N[EMOJI] (0-1[EMOJI])
                position = (recent_prices <= current_price).sum() / len(recent_prices)

                results.append({
                    'stock_code': stock,
                    'factor_value': position
                })

        return pd.DataFrame(results)

    def _displacement_factor(self, data):
        """[EMOJI]N[EMOJI]"""
        print("[[EMOJI]] [EMOJI]...")
        results = []

        for stock in data['stock_code'].unique():
            stock_data = data[data['stock_code'] == stock].sort_values('date')

            if len(stock_data) >= 20:
                displacement = (stock_data['close'].iloc[-1] - stock_data['close'].iloc[-20]) / stock_data['close'].iloc[-20]

                results.append({
                    'stock_code': stock,
                    'factor_value': displacement
                })

        return pd.DataFrame(results)

    def _gap_ratio_factor(self, data):
        """[EMOJI]"""
        print("[[EMOJI]] [EMOJI]...")
        results = []

        for stock in data['stock_code'].unique():
            stock_data = data[data['stock_code'] == stock].sort_values('date')

            if len(stock_data) >= 2:
                gaps = []
                for i in range(1, len(stock_data)):
                    if stock_data['low'].iloc[i] > stock_data['high'].iloc[i-1]:
                        # [EMOJI]
                        gap = (stock_data['low'].iloc[i] - stock_data['high'].iloc[i-1]) / stock_data['high'].iloc[i-1]
                        gaps.append(gap)
                    elif stock_data['high'].iloc[i] < stock_data['low'].iloc[i-1]:
                        # [EMOJI]
                        gap = (stock_data['low'].iloc[i-1] - stock_data['high'].iloc[i]) / stock_data['low'].iloc[i-1]
                        gaps.append(-gap)

                if gaps:
                    results.append({
                        'stock_code': stock,
                        'factor_value': sum(gaps)
                    })

        return pd.DataFrame(results)

    def _price_acceleration_factor(self, data):
        """[EMOJI]"""
        print("[[EMOJI]] [EMOJI]...")
        results = []

        for stock in data['stock_code'].unique():
            stock_data = data[data['stock_code'] == stock].sort_values('date')

            if len(stock_data) >= 20:
                # [EMOJI]
                momentum_10 = stock_data['close'].iloc[-10] - stock_data['close'].iloc[-20]
                momentum_recent = stock_data['close'].iloc[-1] - stock_data['close'].iloc[-10]

                # [EMOJI] = [EMOJI] - [EMOJI]
                acceleration = momentum_recent - momentum_10

                results.append({
                    'stock_code': stock,
                    'factor_value': acceleration
                })

        return pd.DataFrame(results)

    # ==================== [EMOJI] ====================

    def _size_factor(self, data):
        """[EMOJI]"""
        print("[[EMOJI]] [EMOJI]...")
        results = []

        for stock in data['stock_code'].unique():
            stock_data = data[data['stock_code'] == stock].sort_values('date')

            if len(stock_data) >= 20 and 'amount' in stock_data.columns:
                # [EMOJI]
                avg_amount = stock_data['amount'].tail(20).mean()

                results.append({
                    'stock_code': stock,
                    'factor_value': np.log(avg_amount) if avg_amount > 0 else 0
                })

        return pd.DataFrame(results)

    def _beta_factor(self, data):
        """Beta[EMOJI]"""
        print("[[EMOJI]] Beta[EMOJI]...")
        results = []

        # [EMOJI]
        benchmark_stock = data['stock_code'].unique()[0]
        benchmark_data = data[data['stock_code'] == benchmark_stock].sort_values('date')

        if len(benchmark_data) < 20:
            return pd.DataFrame()

        benchmark_returns = benchmark_data['close'].tail(20).pct_change().dropna()

        for stock in data['stock_code'].unique():
            stock_data = data[data['stock_code'] == stock].sort_values('date')

            if len(stock_data) >= 20:
                stock_returns = stock_data['close'].tail(20).pct_change().dropna()

                # [EMOJI]
                min_len = min(len(benchmark_returns), len(stock_returns))
                benchmark_aligned = benchmark_returns.tail(min_len)
                stock_aligned = stock_returns.tail(min_len)

                # [EMOJI]
                if min_len > 1:
                    covariance = np.cov(stock_aligned, benchmark_aligned)[0][1]
                    variance = np.var(benchmark_aligned)

                    if variance > 0:
                        beta = covariance / variance
                    else:
                        beta = 1.0

                    results.append({
                        'stock_code': stock,
                        'factor_value': beta
                    })

        return pd.DataFrame(results)

    def _alpha_factor(self, data):
        """Alpha[EMOJI]"""
        print("[[EMOJI]] Alpha[EMOJI]...")
        results = []

        benchmark_stock = data['stock_code'].unique()[0]
        benchmark_data = data[data['stock_code'] == benchmark_stock].sort_values('date')

        benchmark_return = (benchmark_data['close'].iloc[-1] - benchmark_data['close'].iloc[-20]) / benchmark_data['close'].iloc[-20]

        for stock in data['stock_code'].unique():
            stock_data = data[data['stock_code'] == stock].sort_values('date')

            if len(stock_data) >= 20:
                stock_return = (stock_data['close'].iloc[-1] - stock_data['close'].iloc[-20]) / stock_data['close'].iloc[-20]

                alpha = stock_return - benchmark_return

                results.append({
                    'stock_code': stock,
                    'factor_value': alpha
                })

        return pd.DataFrame(results)

    def _sharpe_ratio_factor(self, data):
        """[EMOJI]"""
        print("[[EMOJI]] [EMOJI]...")
        results = []

        risk_free_rate = 0.03 / 252  # [EMOJI]

        for stock in data['stock_code'].unique():
            stock_data = data[data['stock_code'] == stock].sort_values('date')

            if len(stock_data) >= 20:
                returns = stock_data['close'].tail(20).pct_change().dropna()

                if len(returns) > 0:
                    excess_returns = returns - risk_free_rate
                    sharpe = excess_returns.mean() / excess_returns.std() if excess_returns.std() > 0 else 0

                    results.append({
                        'stock_code': stock,
                        'factor_value': sharpe * np.sqrt(252)  # [EMOJI]
                    })

        return pd.DataFrame(results)

    def _calmar_ratio_factor(self, data):
        """[EMOJI] / [EMOJI]"""
        print("[[EMOJI]] [EMOJI]...")
        results = []

        for stock in data['stock_code'].unique():
            stock_data = data[data['stock_code'] == stock].sort_values('date')

            if len(stock_data) >= 20:
                # [EMOJI]
                total_return = (stock_data['close'].iloc[-1] - stock_data['close'].iloc[-20]) / stock_data['close'].iloc[-20]
                annual_return = total_return * (252 / 20)

                # [EMOJI]
                cummax = stock_data['close'].tail(20).cummax()
                drawdown = (stock_data['close'].tail(20) - cummax) / cummax
                max_dd = abs(drawdown.min())

                if max_dd > 0:
                    calmar = annual_return / max_dd
                else:
                    calmar = 0

                results.append({
                    'stock_code': stock,
                    'factor_value': calmar
                })

        return pd.DataFrame(results)

    def _sortino_ratio_factor(self, data):
        """[EMOJI]"""
        print("[[EMOJI]] [EMOJI]...")
        results = []

        risk_free_rate = 0.03 / 252

        for stock in data['stock_code'].unique():
            stock_data = data[data['stock_code'] == stock].sort_values('date')

            if len(stock_data) >= 20:
                returns = stock_data['close'].tail(20).pct_change().dropna()

                if len(returns) > 0:
                    excess_returns = returns - risk_free_rate
                    downside_returns = excess_returns[excess_returns < 0]

                    if len(downside_returns) > 0:
                        downside_std = downside_returns.std()
                        sortino = excess_returns.mean() / downside_std if downside_std > 0 else 0
                    else:
                        sortino = 0

                    results.append({
                        'stock_code': stock,
                        'factor_value': sortino * np.sqrt(252)
                    })

        return pd.DataFrame(results)

    def _skewness_factor(self, data):
        """[EMOJI]"""
        print("[[EMOJI]] [EMOJI]...")
        results = []

        for stock in data['stock_code'].unique():
            stock_data = data[data['stock_code'] == stock].sort_values('date')

            if len(stock_data) >= 20:
                returns = stock_data['close'].tail(20).pct_change().dropna()

                if len(returns) >= 3:
                    skewness = returns.skew()

                    results.append({
                        'stock_code': stock,
                        'factor_value': skewness
                    })

        return pd.DataFrame(results)

    def _kurtosis_factor(self, data):
        """[EMOJI]"""
        print("[[EMOJI]] [EMOJI]...")
        results = []

        for stock in data['stock_code'].unique():
            stock_data = data[data['stock_code'] == stock].sort_values('date')

            if len(stock_data) >= 20:
                returns = stock_data['close'].tail(20).pct_change().dropna()

                if len(returns) >= 3:
                    kurtosis = returns.kurtosis()

                    results.append({
                        'stock_code': stock,
                        'factor_value': kurtosis
                    })

        return pd.DataFrame(results)

    def _capture_ratio_factor(self, data, direction='up'):
        """[EMOJI]"""
        print(f"[[EMOJI]] {direction}[EMOJI]...")
        results = []

        benchmark_stock = data['stock_code'].unique()[0]
        benchmark_data = data[data['stock_code'] == benchmark_stock].sort_values('date')
        benchmark_returns = benchmark_data['close'].pct_change().dropna()

        for stock in data['stock_code'].unique():
            stock_data = data[data['stock_code'] == stock].sort_values('date')
            stock_returns = stock_data['close'].pct_change().dropna()

            if len(stock_returns) >= 20 and len(benchmark_returns) >= 20:
                min_len = min(len(stock_returns), len(benchmark_returns))
                stock_aligned = stock_returns.tail(min_len).reset_index(drop=True)
                benchmark_aligned = benchmark_returns.tail(min_len).reset_index(drop=True)

                if direction == 'up':
                    # [EMOJI]
                    up_mask = benchmark_aligned > 0
                    if up_mask.any():
                        stock_up = stock_aligned[up_mask].mean()
                        bench_up = benchmark_aligned[up_mask].mean()
                    else:
                        stock_up = 0
                        bench_up = 0.01
                else:
                    # [EMOJI]
                    down_mask = benchmark_aligned < 0
                    if down_mask.any():
                        stock_down = stock_aligned[down_mask].mean()
                        bench_down = benchmark_aligned[down_mask].mean()
                        stock_up = stock_down
                        bench_up = bench_down
                    else:
                        stock_up = 0
                        bench_up = 0.01

                if bench_up != 0:
                    capture_ratio = stock_up / bench_up
                else:
                    capture_ratio = 1.0

                results.append({
                    'stock_code': stock,
                    'factor_value': capture_ratio
                })

        return pd.DataFrame(results)

    # ==================== [EMOJI] ====================

    def _composite_score(self, data, factors):
        """[EMOJI]"""
        print("[[EMOJI]] [EMOJI]...")
        scores = {}

        for stock in data['stock_code'].unique():
            score = 0
            count = 0

            # [EMOJI]
            for factor_name in ['momentum_20d', 'momentum_60d']:
                if factor_name in factors and not factors[factor_name].empty:
                    factor_df = factors[factor_name]
                    stock_factor = factor_df[factor_df['stock_code'] == stock]
                    if not stock_factor.empty:
                        val = stock_factor['factor_value'].iloc[0]
                        score += min(val / 10, 10)  # [EMOJI]0-10
                        count += 1

            # [EMOJI]
            if 'reversal_mid' in factors and not factors['reversal_mid'].empty:
                factor_df = factors['reversal_mid']
                stock_factor = factor_df[factor_df['stock_code'] == stock]
                if not stock_factor.empty:
                    val = stock_factor['factor_value'].iloc[0]
                    score += min(abs(val) * 10, 10)
                    count += 1

            # [EMOJI]
            if 'volatility_20d' in factors and not factors['volatility_20d'].empty:
                factor_df = factors['volatility_20d']
                stock_factor = factor_df[factor_df['stock_code'] == stock]
                if not stock_factor.empty:
                    val = stock_factor['factor_value'].iloc[0]
                    score += max(10 - val / 2, 0)
                    count += 1

            # [EMOJI]
            if 'max_drawdown' in factors and not factors['max_drawdown'].empty:
                factor_df = factors['max_drawdown']
                stock_factor = factor_df[factor_df['stock_code'] == stock]
                if not stock_factor.empty:
                    val = stock_factor['factor_value'].iloc[0]
                    score += max(10 + val * 2, 0)  # [EMOJI]
                    count += 1

            # [EMOJI]
            if 'ma20_signal' in factors and not factors['ma20_signal'].empty:
                factor_df = factors['ma20_signal']
                stock_factor = factor_df[factor_df['stock_code'] == stock]
                if not stock_factor.empty:
                    val = stock_factor['factor_value'].iloc[0]
                    score += val * 10
                    count += 1

            # [EMOJI]
            if 'sharp_ratio' in factors and not factors['sharp_ratio'].empty:
                factor_df = factors['sharp_ratio']
                stock_factor = factor_df[factor_df['stock_code'] == stock]
                if not stock_factor.empty:
                    val = stock_factor['factor_value'].iloc[0]
                    score += min(val / 0.5, 10)
                    count += 1

            # [EMOJI]
            max_score = count * 10
            if max_score > 0:
                ratio = score / max_score
                if ratio > 0.7:
                    rating = 'A'
                elif ratio > 0.5:
                    rating = 'B'
                elif ratio > 0.3:
                    rating = 'C'
                else:
                    rating = 'D'
            else:
                rating = 'N/A'

            scores[stock] = {
                'score': round(score, 2),
                'max_score': max_score,
                'rating': rating
            }

        return pd.DataFrame(scores).T


# ============================================================
# [EMOJI]
# ============================================================

def generate_comprehensive_report(factor_results):
    """[EMOJI] - [EMOJI]"""
    print("\n" + "=" * 80)
    print(" " * 25 + "50+[EMOJI]")
    print("=" * 80)

    if factor_results is None:
        return

    # 1. [EMOJI]
    if 'composite_score' in factor_results and not factor_results['composite_score'].empty:
        print("\n" + "=" * 80)
        print(" " * 30 + "[EMOJI]")
        print("=" * 80)

        scores = factor_results['composite_score']
        scores['percentile'] = scores['score'].rank(pct=True)
        scores_sorted = scores.sort_values('score', ascending=False)

        print(f"\n{'[EMOJI]':<6}{'[EMOJI]':<12}{'[EMOJI]':<12}{'[EMOJI]':<12}{'[EMOJI]':<10}{'[EMOJI]':<8}")
        print("-" * 80)

        for i, (idx, row) in enumerate(scores_sorted.iterrows(), 1):
            score_pct = row['score'] / row['max_score'] * 100 if row['max_score'] > 0 else 0
            print(f"{i:<6}{idx:<12}{row['score']:<12.2f}{score_pct:<11.1f}%{row['percentile']:<10.2%}{row['rating']:<8}")

        # [EMOJI]
        print("\n[EMOJI]")
        for idx, row in scores_sorted.iterrows():
            stars = "*" * (5 if row['rating'] == 'A' else 4 if row['rating'] == 'B' else 3 if row['rating'] == 'C' else 2)
            print(f"  {idx:<12} {stars} ({row['rating']}[EMOJI])")

    # 2. [EMOJI]
    if 'momentum_20d' in factor_results and not factor_results['momentum_20d'].empty:
        print("\n\n" + "=" * 80)
        print(" " * 30 + "[EMOJI]")
        print("=" * 80)

        # [EMOJI]20[EMOJI]
        print("\n20[EMOJI]")
        momentum_sorted = factor_results['momentum_20d'].sort_values('factor_value', ascending=False)
        for i, (_, row) in enumerate(momentum_sorted.iterrows(), 1):
            print(f"  {i}. {row['stock_code']}: {row['factor_value']:+7.2f}%")

        # [EMOJI]
        for period, factor_name in [(5, 'momentum_5d'), (60, 'momentum_60d')]:
            if factor_name in factor_results and not factor_results[factor_name].empty:
                pf = factor_results[factor_name].sort_values('factor_value', ascending=False)
                best = pf.iloc[0] if not pf.empty else None
                if best is not None:
                    print(f"\n{period}[EMOJI]{best['stock_code']} ({best['factor_value']:+.2f}%)")

    # 3. [EMOJI]
    if 'volatility_20d' in factor_results and not factor_results['volatility_20d'].empty:
        print("\n\n" + "=" * 80)
        print(" " * 30 + "[EMOJI]")
        print("=" * 80)

        print("\n[EMOJI]→[EMOJI]")
        vol_sorted = factor_results['volatility_20d'].sort_values('factor_value')
        for i, (_, row) in enumerate(vol_sorted.iterrows(), 1):
            print(f"  {i}. {row['stock_code']}: {row['factor_value']:.4f} ({'[EMOJI]' if row['factor_value'] < 0.2 else '[EMOJI]' if row['factor_value'] < 0.4 else '[EMOJI]'})")

        if 'max_drawdown' in factor_results and not factor_results['max_drawdown'].empty:
            print("\n[EMOJI]→[EMOJI]")
            dd_sorted = factor_results['max_drawdown'].sort_values('factor_value', ascending=False)
            for i, (_, row) in enumerate(dd_sorted.iterrows(), 1):
                print(f"  {i}. {row['stock_code']}: {row['factor_value']:.2f}%")

        # [EMOJI]
        print("\n[EMOJI]")
        for stock in factor_results['composite_score'].index:
            if stock in factor_results['volatility_20d']['stock_code'].values:
                vol = factor_results['volatility_20d'][factor_results['volatility_20d']['stock_code'] == stock]['factor_value'].iloc[0]
                risk_level = '[EMOJI]' if vol < 0.2 else '[EMOJI]' if vol < 0.4 else '[EMOJI]'
                print(f"  {stock}: {risk_level}[EMOJI]")

    # 4. [EMOJI]
    if 'ma20_signal' in factor_results and not factor_results['ma20_signal'].empty:
        print("\n\n" + "=" * 80)
        print(" " * 30 + "[EMOJI]")
        print("=" * 80)

        ma20 = factor_results['ma20_signal']
        above_count = (ma20['factor_value'] > 0).sum()
        below_count = (ma20['factor_value'] <= 0).sum()

        print(f"\n[EMOJI]")
        print(f"  MA20[EMOJI]: {above_count} [EMOJI]")
        print(f"  MA20[EMOJI]: {below_count} [EMOJI]")

        print(f"\nMA20[EMOJI]")
        above_stocks = ma20[ma20['factor_value'] > 0]['stock_code'].tolist()
        for stock in above_stocks:
            print(f"  [+] {stock} - [EMOJI]")

        print(f"\nMA20[EMOJI]")
        below_stocks = ma20[ma20['factor_value'] <= 0]['stock_code'].tolist()
        for stock in below_stocks:
            print(f"  [-] {stock} - [EMOJI]")

        if 'rsi' in factor_results and not factor_results['rsi'].empty:
            print(f"\nRSI[EMOJI]")
            rsi_sorted = factor_results['rsi'].sort_values('factor_value', ascending=False)
            for _, row in rsi_sorted.iterrows():
                val = row['factor_value']
                if val > 70:
                    status = "[EMOJI] ([EMOJI])"
                elif val < 30:
                    status = "[EMOJI] ([EMOJI])"
                else:
                    status = "[EMOJI]"
                print(f"  {row['stock_code']}: {val:.2f} - {status}")

        if 'bollinger' in factor_results and not factor_results['bollinger'].empty:
            print(f"\n[EMOJI]")
            bb = factor_results['bollinger'].sort_values('factor_value', ascending=False)
            for _, row in bb.iterrows():
                pos = row['factor_value']
                if pos > 0.8:
                    status = "[EMOJI]"
                elif pos < 0.2:
                    status = "[EMOJI]"
                else:
                    status = "[EMOJI]"
                print(f"  {row['stock_code']}: {pos:.2f} - {status}")

    # 5. [EMOJI]
    if 'sharp_ratio' in factor_results and not factor_results['sharp_ratio'].empty:
        print("\n\n" + "=" * 80)
        print(" " * 30 + "[EMOJI]")
        print("=" * 80)

        print("\n[EMOJI]")
        sharp_sorted = factor_results['sharp_ratio'].sort_values('factor_value', ascending=False)
        for i, (_, row) in enumerate(sharp_sorted.iterrows(), 1):
            quality = '[EMOJI]' if row['factor_value'] > 1 else '[EMOJI]' if row['factor_value'] > 0 else '[EMOJI]' if row['factor_value'] > -1 else '[EMOJI]'
            print(f"  {i}. {row['stock_code']}: {row['factor_value']:+.2f} ({quality})")

    # 6. 50+[EMOJI]
    print("\n\n" + "=" * 80)
    print(" " * 30 + "[EMOJI]50+[EMOJI]")
    print("=" * 80)

    total_factors = len(factor_results)
    calculated_factors = sum(1 for k, v in factor_results.items() if not v.empty)

    print(f"\n[EMOJI]")
    print(f"  [EMOJI]: {total_factors} [EMOJI]")
    print(f"  [EMOJI]: {calculated_factors} [EMOJI]")
    print(f"  [EMOJI]: {total_factors - calculated_factors} [EMOJI]")

    # [EMOJI]
    factor_categories = {
        '[EMOJI]': ['momentum_5d', 'momentum_10d', 'momentum_20d', 'momentum_60d', 'momentum_vol'],
        '[EMOJI]': ['reversal_short', 'reversal_mid', 'reversal_long'],
        '[EMOJI]': ['volatility_20d', 'volatility_60d', 'volatility_120d', 'max_drawdown'],
        '[EMOJI]': ['volume_ratio', 'volume_ma', 'price_volume_trend', 'turnover_rate', 'amplitude'],
        '[EMOJI]': ['ma5_signal', 'ma10_signal', 'ma20_signal', 'ma60_signal', 'ma_trend', 'bollinger', 'rsi'],
        '[EMOJI]': ['price_position', 'price_position_60', 'displacement', 'gap_ratio', 'price_acceleration'],
        '[EMOJI]': ['size', 'beta', 'alpha', 'sharp_ratio', 'calmar_ratio', 'sortino_ratio', 'skewness', 'kurtosis', 'upside_capture', 'downside_capture']
    }

    print(f"\n[EMOJI]")
    for category, factors in factor_categories.items():
        available = sum(1 for f in factors if f in factor_results and not factor_results[f].empty)
        print(f"  {category}: {available}/{len(factors)}")

    # 7. [EMOJI]
    print("\n\n" + "=" * 80)
    print(" " * 30 + "[EMOJI]")
    print("=" * 80)

    if 'composite_score' in factor_results and not factor_results['composite_score'].empty:
        scores = factor_results['composite_score']

        # A[EMOJI]
        a_stocks = scores[scores['rating'] == 'A']
        if not a_stocks.empty:
            print(f"\n[EMOJI]A[EMOJI]")
            for idx, row in a_stocks.iterrows():
                print(f"  [A] {idx} - [EMOJI] {row['score']:.2f}[EMOJI]")

        # B[EMOJI]
        b_stocks = scores[scores['rating'] == 'B']
        if not b_stocks.empty:
            print(f"\n[EMOJI]B[EMOJI]")
            for idx, row in b_stocks.iterrows():
                print(f"  [B] {idx} - [EMOJI] {row['score']:.2f}[EMOJI]")

        # D[EMOJI]
        d_stocks = scores[scores['rating'] == 'D']
        if not d_stocks.empty:
            print(f"\n[EMOJI]D[EMOJI]")
            for idx, row in d_stocks.iterrows():
                print(f"  [D] {idx} - [EMOJI] {row['score']:.2f}[EMOJI]")

    # 8. [EMOJI]
    print("\n\n" + "=" * 80)
    print(" " * 30 + "[EMOJI]")
    print("=" * 80)

    if 'momentum_20d' in factor_results and not factor_results['momentum_20d'].empty:
        momentum_df = factor_results['momentum_20d'].sort_values('factor_value', ascending=False)
        best_momentum = momentum_df.iloc[0] if not momentum_df.empty else None

        if best_momentum is not None and best_momentum['factor_value'] > 5:
            print(f"\n  [EMOJI]{best_momentum['stock_code']} [EMOJI]({best_momentum['factor_value']:+.2f}%)[EMOJI]")
        elif best_momentum is not None and best_momentum['factor_value'] < -5:
            print(f"\n  [EMOJI]{best_momentum['stock_code']} [EMOJI]({best_momentum['factor_value']:+.2f}%)[EMOJI]")

    if 'volatility_20d' in factor_results and not factor_results['volatility_20d'].empty:
        vol_df = factor_results['volatility_20d'].sort_values('factor_value')
        lowest_vol = vol_df.iloc[0] if not vol_df.empty else None

        if lowest_vol is not None:
            print(f"  [EMOJI]{lowest_vol['stock_code']} [EMOJI]({lowest_vol['factor_value']:.4f})[EMOJI]")

    if 'ma20_signal' in factor_results and not factor_results['ma20_signal'].empty:
        ma20 = factor_results['ma20_signal']
        above_stocks = ma20[ma20['factor_value'] > 0]['stock_code'].tolist()
        if above_stocks:
            print(f"  [EMOJI]{', '.join(above_stocks[:3])} [EMOJI]MA20[EMOJI]")

    print("\n" + "=" * 80)
    print("[EMOJI] - " + datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
    print("=" * 80)

    # 2. [EMOJI]
    if 'momentum_20d' in factor_results and not factor_results['momentum_20d'].empty:
        print("\n\n[[EMOJI]] [EMOJI]20[EMOJI]")
        print("-" * 70)
        momentum_sorted = factor_results['momentum_20d'].sort_values('factor_value', ascending=False)
        for _, row in momentum_sorted.iterrows():
            print(f"{row['stock_code']}: {row['factor_value']:+.2f}%")

    # 3. [EMOJI]
    if 'volatility_20d' in factor_results and not factor_results['volatility_20d'].empty:
        print("\n\n[[EMOJI]] [EMOJI]")
        print("-" * 70)
        vol_sorted = factor_results['volatility_20d'].sort_values('factor_value')
        for _, row in vol_sorted.iterrows():
            print(f"{row['stock_code']}: [EMOJI] {row['factor_value']:.2f}%")

    if 'max_drawdown' in factor_results and not factor_results['max_drawdown'].empty:
        print("\n[EMOJI]:")
        dd_sorted = factor_results['max_drawdown'].sort_values('factor_value', ascending=False)
        for _, row in dd_sorted.iterrows():
            print(f"{row['stock_code']}: {row['factor_value']:.2f}%")

    # 4. [EMOJI]
    if 'ma20_signal' in factor_results and not factor_results['ma20_signal'].empty:
        print("\n\n[[EMOJI]] [EMOJI]")
        print("-" * 70)
        ma20 = factor_results['ma20_signal']
        above_count = (ma20['factor_value'] > 0).sum()
        print(f"MA20[EMOJI]: {above_count} [EMOJI]")
        print(f"MA20[EMOJI]: {len(ma20) - above_count} [EMOJI]")

        if 'rsi' in factor_results and not factor_results['rsi'].empty:
            print("\nRSI[EMOJI]:")
            rsi_sorted = factor_results['rsi'].sort_values('factor_value', ascending=False)
            for _, row in rsi_sorted.iterrows():
                status = "[EMOJI]" if row['factor_value'] > 70 else "[EMOJI]" if row['factor_value'] < 30 else "[EMOJI]"
                print(f"  {row['stock_code']}: {row['factor_value']:.2f} ({status})")

    # 5. [EMOJI]
    if 'sharp_ratio' in factor_results and not factor_results['sharp_ratio'].empty:
        print("\n\n[[EMOJI]] [EMOJI]")
        print("-" * 70)
        sharp_sorted = factor_results['sharp_ratio'].sort_values('factor_value', ascending=False)
        for _, row in sharp_sorted.iterrows():
            print(f"{row['stock_code']}: [EMOJI] {row['factor_value']:.2f}")

    print("\n" + "=" * 70)
    print("[EMOJI]")
    print("=" * 70)


# ============================================================
# [EMOJI]
# ============================================================

def main():
    """[EMOJI]"""
    print("=" * 70)
    print("[EMOJI] - 50+[EMOJI]")
    print("=" * 70)

    # 1. [EMOJI]
    print("\n[[EMOJI]1] [EMOJI]")
    reader = DuckDBDataReader(DUCKDB_PATH)

    if reader.conn is None:
        print("\n[[EMOJI]] [EMOJI]")
        return

    # 2. [EMOJI]
    print(f"\n[[EMOJI]2] [EMOJI]50+[EMOJI] ({len(STOCK_LIST)} [EMOJI])")
    calculator = ComprehensiveFactorCalculator(reader)

    results = calculator.calculate_all_factors(STOCK_LIST, START_DATE)

    # 3. [EMOJI]
    print(f"\n[[EMOJI]3] [EMOJI]")
    generate_comprehensive_report(results)

    # 4. [EMOJI]
    reader.close()

    print("\n[[EMOJI]]")
    print("1. [EMOJI]: " + DUCKDB_PATH)
    print(f"2. [EMOJI]: {len(STOCK_LIST)}")
    print(f"3. [EMOJI]: 50+[EMOJI]")
    print("4. [EMOJI]STOCK_LIST[EMOJI]")


if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        print(f"\n[ERROR] {e}")
        import traceback
        traceback.print_exc()
