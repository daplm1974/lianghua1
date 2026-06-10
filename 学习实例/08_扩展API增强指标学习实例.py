#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
EasyXT[EMOJI]API[EMOJI] - [EMOJI]
[EMOJI]API[EMOJI]
[EMOJI]
"""

import sys
import os
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import warnings
import time
import sqlite3
warnings.filterwarnings('ignore')

# [EMOJI]Python[EMOJI]
current_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.dirname(current_dir)
if project_root not in sys.path:
    sys.path.insert(0, project_root)

def print_status(message, status="info"):
    """[EMOJI]"""
    if status == "success":
        print(f"[OK] {message}")
    elif status == "error":
        print(f"[X] {message}")
    elif status == "warning":
        print(f"[!] {message}")
    else:
        print(f"ℹ[EMOJI] {message}")

def print_separator(title="", length=60):
    """[EMOJI]"""
    if title:
        print(f"\n{'='*length}")
        print(f"{title}")
        print(f"{'='*length}")
    else:
        print("="*length)

def wait_for_continue(lesson_name=""):
    """[EMOJI]"""
    if lesson_name:
        input(f"\n[BOOK] {lesson_name} [EMOJI]...")
    else:
        input(f"\n[EMOJI]...")
    print()

def print_course_header(course_num, course_name, description=""):
    """[EMOJI]"""
    print_separator()
    print(f"[EMOJI]{course_num}[EMOJI]{course_name}")
    if description:
        print(f"[EMOJI] {description}")
    print_separator()

try:
    # [EMOJI]xtquant
    print_status("[EMOJI]xtquant[EMOJI]...")
    import xtquant.xtdata as xt
    print_status("xtquant.xtdata [EMOJI]", "success")
    
    import xtquant.xttrader as trader
    print_status("xtquant.xttrader [EMOJI]", "success")
    
except ImportError as e:
    print_status(f"[EMOJI]xtquant[EMOJI]: {e}", "error")
    print("[EMOJI]xtquant")
    sys.exit(1)

try:
    from easy_xt.extended_api import ExtendedAPI
    print_status("ExtendedAPI [EMOJI]", "success")
except ImportError as e:
    print_status(f"[EMOJI]ExtendedAPI[EMOJI]: {e}", "error")
    sys.exit(1)

print_separator("EasyXT[EMOJI]API[EMOJI] - [EMOJI]")
print("[TARGET] [EMOJI]API[EMOJI]")
print("[BOOK] [EMOJI]")
print("⏰ [EMOJI]")
print_separator()

# ================================
# [EMOJI]
# ================================

class DataManager:
    """[EMOJI] - [EMOJI]"""
    
    def __init__(self):
        self.cache = {}
        self.quality_threshold = 0.8  # [EMOJI]
    
    def get_clean_data(self, stock_code, period='1d', count=100, show_details=True):
        """[EMOJI]"""
        try:
            if show_details:
                print(f"  [SEARCH] [EMOJI]{stock_code}[EMOJI]{period}[EMOJI]...")
            
            # [EMOJI]1: [EMOJI]get_market_data_ex
            data = xt.get_market_data_ex(
                stock_list=[stock_code],
                period=period,
                count=count,
                dividend_type='front_ratio',  # [EMOJI]
                fill_data=True
            )
            
            if stock_code not in data or len(data[stock_code]) == 0:
                if show_details:
                    print(f"  [X] [EMOJI]{stock_code}[EMOJI]")
                return None
            
            df = data[stock_code].copy()
            
            # [EMOJI]
            valid_close = df['close'].notna().sum()
            quality_ratio = valid_close / len(df)
            
            if quality_ratio < self.quality_threshold:
                if show_details:
                    print(f"  [!] [EMOJI]: {valid_close}/{len(df)} ({quality_ratio:.1%})")
                return None
            
            # [EMOJI]
            df = self._clean_dataframe(df, show_details)
            
            if df is not None and len(df) > 0:
                if show_details:
                    print(f"  [OK] [EMOJI]{len(df)}[EMOJI] ([EMOJI]: {quality_ratio:.1%})")
                return df
            else:
                if show_details:
                    print(f"  [X] [EMOJI]")
                return None
                
        except Exception as e:
            if show_details:
                print(f"  [X] [EMOJI]: {e}")
            return None
    
    def _clean_dataframe(self, df, show_details=False):
        """[EMOJI]DataFrame[EMOJI]"""
        try:
            if df is None or len(df) == 0:
                return None
            
            original_len = len(df)
            
            # 1. [EMOJI]
            if 'time' in df.columns:
                try:
                    time_col = df['time']
                    sample_time = str(time_col.iloc[0])
                    
                    if len(sample_time) == 13 and sample_time.isdigit():
                        df.index = pd.to_datetime(time_col, unit='ms')
                    elif len(sample_time) == 10 and sample_time.isdigit():
                        df.index = pd.to_datetime(time_col, unit='s')
                    elif len(sample_time) == 8 and sample_time.isdigit():
                        df.index = pd.to_datetime(time_col, format='%Y%m%d')
                    else:
                        df.index = pd.to_datetime(time_col)
                    
                    df = df.drop('time', axis=1)
                except:
                    pass  # [EMOJI]
            
            # 2. [EMOJI]
            if 'close' in df.columns:
                valid_mask = (df['close'] > 0) & df['close'].notna()
                df = df[valid_mask]
            
            # 3. [EMOJI]NaN[EMOJI]
            price_cols = ['open', 'high', 'low', 'close', 'preClose']
            for col in price_cols:
                if col in df.columns:
                    df[col] = df[col].fillna(method='ffill').fillna(method='bfill')
            
            # 4. [EMOJI]
            if 'volume' in df.columns:
                df['volume'] = df['volume'].fillna(0)
                df.loc[df['volume'] < 0, 'volume'] = 0
            
            if 'amount' in df.columns:
                df['amount'] = df['amount'].fillna(0)
                df.loc[df['amount'] < 0, 'amount'] = 0
            
            # 5. [EMOJI]OHLC[EMOJI]
            if all(col in df.columns for col in ['open', 'high', 'low', 'close']):
                for idx in df.index:
                    row = df.loc[idx]
                    if all(pd.notna(row[col]) for col in ['open', 'high', 'low', 'close']):
                        prices = [row['open'], row['close']]
                        df.loc[idx, 'high'] = max(row['high'], max(prices))
                        df.loc[idx, 'low'] = min(row['low'], min(prices))
            
            final_len = len(df)
            if show_details and final_len < original_len:
                print(f"    [EMOJI]: {original_len}→{final_len}[EMOJI]")
            
            return df if final_len > 0 else None
            
        except Exception as e:
            if show_details:
                print(f"    [EMOJI]: {e}")
            return df
    
    def check_data_quality(self, stock_codes, periods=['1d']):
        """[EMOJI]"""
        print("[SEARCH] [EMOJI]...")
        
        quality_report = {}
        
        for period in periods:
            print(f"\n[CHART] [EMOJI]{period}[EMOJI]:")
            period_report = {}
            
            for stock_code in stock_codes:
                print(f"  [EMOJI] {stock_code}...")
                
                df = self.get_clean_data(stock_code, period, count=50, show_details=False)
                
                if df is not None:
                    # [EMOJI]
                    score = self._calculate_quality_score(df)
                    period_report[stock_code] = {
                        'status': 'success',
                        'data_count': len(df),
                        'quality_score': score,
                        'latest_price': df['close'].iloc[-1] if len(df) > 0 else 0
                    }
                    print(f"    [OK] [EMOJI]: {score:.1f}/10.0, [EMOJI]: {len(df)}[EMOJI]")
                else:
                    period_report[stock_code] = {
                        'status': 'failed',
                        'data_count': 0,
                        'quality_score': 0,
                        'latest_price': 0
                    }
                    print(f"    [X] [EMOJI]")
            
            quality_report[period] = period_report
        
        return quality_report
    
    def _calculate_quality_score(self, df):
        """[EMOJI]"""
        score = 10.0
        
        if len(df) == 0:
            return 0
        
        # [EMOJI]NaN[EMOJI]
        nan_ratio = df.isnull().sum().sum() / (len(df) * len(df.columns))
        score -= nan_ratio * 5  # NaN[EMOJI]
        
        # [EMOJI]
        if 'volume' in df.columns:
            zero_volume_ratio = (df['volume'] == 0).sum() / len(df)
            if zero_volume_ratio > 0.5:  # [EMOJI]50%[EMOJI]
                score -= 2
        
        # [EMOJI]
        if 'close' in df.columns and len(df) > 1:
            price_changes = df['close'].pct_change().abs()
            extreme_changes = (price_changes > 0.2).sum()  # [EMOJI]20%[EMOJI]
            if extreme_changes > len(df) * 0.1:  # [EMOJI]10%[EMOJI]
                score -= 1
        
        return max(0, score)

# ================================
# [EMOJI]
# ================================

class TechnicalIndicators:
    """[EMOJI]"""
    
    @staticmethod
    def calculate_macd(df, fast=12, slow=26, signal=9):
        """[EMOJI]MACD[EMOJI]"""
        try:
            if len(df) < slow + signal:
                return None
            
            close = df['close']
            
            # [EMOJI]EMA
            ema_fast = close.ewm(span=fast).mean()
            ema_slow = close.ewm(span=slow).mean()
            
            # MACD[EMOJI]
            macd_line = ema_fast - ema_slow
            
            # [EMOJI]
            signal_line = macd_line.ewm(span=signal).mean()
            
            # [EMOJI]
            histogram = macd_line - signal_line
            
            # [EMOJI]
            latest_macd = macd_line.iloc[-1]
            latest_signal = signal_line.iloc[-1]
            latest_hist = histogram.iloc[-1]
            
            # [EMOJI]
            if len(macd_line) > 1:
                macd_trend = "[EMOJI]" if latest_macd > macd_line.iloc[-2] else "[EMOJI]"
            else:
                macd_trend = "[EMOJI]"
            
            # [EMOJI]
            if len(macd_line) > 1:
                prev_diff = macd_line.iloc[-2] - signal_line.iloc[-2]
                curr_diff = latest_macd - latest_signal
                
                if prev_diff <= 0 and curr_diff > 0:
                    cross_signal = "[EMOJI]"  # [EMOJI]
                elif prev_diff >= 0 and curr_diff < 0:
                    cross_signal = "[EMOJI]"   # [EMOJI]
                else:
                    cross_signal = "[EMOJI]"
            else:
                cross_signal = "[EMOJI]"
            
            return {
                'macd': latest_macd,
                'signal': latest_signal,
                'histogram': latest_hist,
                'trend': macd_trend,
                'cross': cross_signal,
                'buy_signal': cross_signal == "[EMOJI]",
                'sell_signal': cross_signal == "[EMOJI]"
            }
            
        except Exception as e:
            print(f"    MACD[EMOJI]: {e}")
            return None
    
    @staticmethod
    def calculate_kdj(df, n=9, m1=3, m2=3):
        """[EMOJI]KDJ[EMOJI]"""
        try:
            if len(df) < n:
                return None
            
            high = df['high']
            low = df['low']
            close = df['close']
            
            # [EMOJI]RSV
            lowest_low = low.rolling(window=n).min()
            highest_high = high.rolling(window=n).max()
            
            rsv = (close - lowest_low) / (highest_high - lowest_low) * 100
            rsv = rsv.fillna(50)  # [EMOJI]NaN[EMOJI]50
            
            # [EMOJI]K[EMOJI]D[EMOJI]J
            k_values = []
            d_values = []
            
            k_prev = 50  # [EMOJI]K[EMOJI]
            d_prev = 50  # [EMOJI]D[EMOJI]
            
            for rsv_val in rsv:
                if pd.notna(rsv_val):
                    k_curr = (2/3) * k_prev + (1/3) * rsv_val
                    d_curr = (2/3) * d_prev + (1/3) * k_curr
                    
                    k_values.append(k_curr)
                    d_values.append(d_curr)
                    
                    k_prev = k_curr
                    d_prev = d_curr
                else:
                    k_values.append(k_prev)
                    d_values.append(d_prev)
            
            k_series = pd.Series(k_values, index=df.index)
            d_series = pd.Series(d_values, index=df.index)
            j_series = 3 * k_series - 2 * d_series
            
            # [EMOJI]
            latest_k = k_series.iloc[-1]
            latest_d = d_series.iloc[-1]
            latest_j = j_series.iloc[-1]
            
            # [EMOJI]
            if len(k_series) > 1:
                k_trend = "[EMOJI]" if latest_k > k_series.iloc[-2] else "[EMOJI]"
                d_trend = "[EMOJI]" if latest_d > d_series.iloc[-2] else "[EMOJI]"
            else:
                k_trend = d_trend = "[EMOJI]"
            
            # [EMOJI]
            if latest_k > 80 and latest_d > 80:
                signal = "[EMOJI]"
                buy_signal = False
                sell_signal = True
            elif latest_k < 20 and latest_d < 20:
                signal = "[EMOJI]"
                buy_signal = True
                sell_signal = False
            else:
                signal = "[EMOJI]"
                buy_signal = False
                sell_signal = False
            
            return {
                'k': latest_k,
                'd': latest_d,
                'j': latest_j,
                'k_trend': k_trend,
                'd_trend': d_trend,
                'signal': signal,
                'buy_signal': buy_signal,
                'sell_signal': sell_signal
            }
            
        except Exception as e:
            print(f"    KDJ[EMOJI]: {e}")
            return None
    
    @staticmethod
    def calculate_rsi(df, period=14):
        """[EMOJI]RSI[EMOJI]"""
        try:
            if len(df) < period + 1:
                return None
            
            close = df['close']
            delta = close.diff()
            
            gain = (delta.where(delta > 0, 0)).rolling(window=period).mean()
            loss = (-delta.where(delta < 0, 0)).rolling(window=period).mean()
            
            rs = gain / loss
            rsi = 100 - (100 / (1 + rs))
            
            latest_rsi = rsi.iloc[-1]
            
            # [EMOJI]
            if len(rsi) > 1:
                rsi_trend = "[EMOJI]" if latest_rsi > rsi.iloc[-2] else "[EMOJI]"
            else:
                rsi_trend = "[EMOJI]"
            
            # [EMOJI]
            if latest_rsi > 70:
                signal = "[EMOJI]"
                overbought = True
                oversold = False
                buy_signal = False
                sell_signal = True
            elif latest_rsi < 30:
                signal = "[EMOJI]"
                overbought = False
                oversold = True
                buy_signal = True
                sell_signal = False
            else:
                signal = "[EMOJI]"
                overbought = False
                oversold = False
                buy_signal = False
                sell_signal = False
            
            # [EMOJI]
            divergence = False
            if len(rsi) > 10 and len(close) > 10:
                recent_price_trend = close.iloc[-5:].is_monotonic_increasing
                recent_rsi_trend = rsi.iloc[-5:].is_monotonic_increasing
                divergence = recent_price_trend != recent_rsi_trend
            
            return {
                'rsi': latest_rsi,
                'trend': rsi_trend,
                'signal': signal,
                'overbought': overbought,
                'oversold': oversold,
                'divergence': divergence,
                'buy_signal': buy_signal,
                'sell_signal': sell_signal
            }
            
        except Exception as e:
            print(f"    RSI[EMOJI]: {e}")
            return None
    
    @staticmethod
    def calculate_bollinger_bands(df, period=20, std_dev=2):
        """[EMOJI]"""
        try:
            if len(df) < period:
                return None
            
            close = df['close']
            
            # [EMOJI]
            middle_band = close.rolling(window=period).mean()
            
            # [EMOJI]
            std = close.rolling(window=period).std()
            
            # [EMOJI]
            upper_band = middle_band + (std * std_dev)
            lower_band = middle_band - (std * std_dev)
            
            # [EMOJI]
            latest_close = close.iloc[-1]
            latest_upper = upper_band.iloc[-1]
            latest_middle = middle_band.iloc[-1]
            latest_lower = lower_band.iloc[-1]
            
            # [EMOJI]
            bandwidth = ((latest_upper - latest_lower) / latest_middle) * 100
            
            # %B[EMOJI]
            percent_b = (latest_close - latest_lower) / (latest_upper - latest_lower)
            
            # [EMOJI]
            if latest_close > latest_upper:
                position = "[EMOJI]"
                buy_signal = False
                sell_signal = True
            elif latest_close < latest_lower:
                position = "[EMOJI]"
                buy_signal = True
                sell_signal = False
            elif latest_close > latest_middle:
                position = "[EMOJI]"
                buy_signal = False
                sell_signal = False
            else:
                position = "[EMOJI]"
                buy_signal = False
                sell_signal = False
            
            # [EMOJI]
            if latest_close > latest_upper:
                signal = "[EMOJI]"
            elif latest_close < latest_lower:
                signal = "[EMOJI]"
            else:
                signal = "[EMOJI]"
            
            return {
                'upper': latest_upper,
                'middle': latest_middle,
                'lower': latest_lower,
                'current_price': latest_close,
                'bandwidth': bandwidth,
                'percent_b': percent_b,
                'position': position,
                'signal': signal,
                'buy_signal': buy_signal,
                'sell_signal': sell_signal
            }
            
        except Exception as e:
            print(f"    [EMOJI]: {e}")
            return None

# ================================
# [EMOJI]
# ================================

class ComprehensiveAnalyzer:
    """[EMOJI]"""
    
    def __init__(self):
        self.data_manager = DataManager()
        self.indicators = TechnicalIndicators()
    
    def analyze_stock(self, stock_code, period='1d', count=60):
        """[EMOJI]"""
        print(f"[CHART] [EMOJI] {stock_code}...")
        
        # [EMOJI]
        df = self.data_manager.get_clean_data(stock_code, period, count)
        if df is None:
            print(f"  [X] [EMOJI]{stock_code}[EMOJI]")
            return None
        
        # [EMOJI]
        macd_result = self.indicators.calculate_macd(df)
        kdj_result = self.indicators.calculate_kdj(df)
        rsi_result = self.indicators.calculate_rsi(df)
        boll_result = self.indicators.calculate_bollinger_bands(df)
        
        # [EMOJI]
        buy_signals = 0
        sell_signals = 0
        
        if macd_result and macd_result['buy_signal']:
            buy_signals += 2  # MACD[EMOJI]
        if macd_result and macd_result['sell_signal']:
            sell_signals += 2
        
        if kdj_result and kdj_result['buy_signal']:
            buy_signals += 1
        if kdj_result and kdj_result['sell_signal']:
            sell_signals += 1
        
        if rsi_result and rsi_result['buy_signal']:
            buy_signals += 1
        if rsi_result and rsi_result['sell_signal']:
            sell_signals += 1
        
        if boll_result and boll_result['buy_signal']:
            buy_signals += 1
        if boll_result and boll_result['sell_signal']:
            sell_signals += 1
        
        # [EMOJI]
        signal_strength = buy_signals - sell_signals
        
        if signal_strength >= 3:
            final_signal = "[EMOJI]"
            signal_emoji = "[EMOJI]"
        elif signal_strength >= 1:
            final_signal = "[EMOJI]"
            signal_emoji = "[EMOJI]"
        elif signal_strength <= -3:
            final_signal = "[EMOJI]"
            signal_emoji = "[EMOJI]"
        elif signal_strength <= -1:
            final_signal = "[EMOJI]"
            signal_emoji = "[EMOJI]"
        else:
            final_signal = "[EMOJI]"
            signal_emoji = "[EMOJI]"
        
        return {
            'stock_code': stock_code,
            'data_length': len(df),
            'latest_price': df['close'].iloc[-1],
            'macd': macd_result,
            'kdj': kdj_result,
            'rsi': rsi_result,
            'bollinger': boll_result,
            'final_signal': final_signal,
            'signal_strength': signal_strength,
            'signal_emoji': signal_emoji,
            'buy_signals': buy_signals,
            'sell_signals': sell_signals
        }

# ================================
# [EMOJI]
# ================================

class DatabaseManager:
    """[EMOJI]"""
    
    def __init__(self, db_path="market_analysis.db"):
        self.db_path = db_path
        self.init_database()
    
    def init_database(self):
        """[EMOJI]"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            # [EMOJI]
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS analysis_results (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    stock_code TEXT NOT NULL,
                    analysis_date TEXT NOT NULL,
                    latest_price REAL,
                    macd_signal TEXT,
                    kdj_signal TEXT,
                    rsi_signal TEXT,
                    boll_signal TEXT,
                    final_signal TEXT,
                    signal_strength INTEGER,
                    created_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            ''')
            
            conn.commit()
            conn.close()
            print("[OK] [EMOJI]")
            
        except Exception as e:
            print(f"[X] [EMOJI]: {e}")
    
    def save_analysis_result(self, result):
        """[EMOJI]"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            cursor.execute('''
                INSERT INTO analysis_results 
                (stock_code, analysis_date, latest_price, macd_signal, kdj_signal, 
                 rsi_signal, boll_signal, final_signal, signal_strength)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
            ''', (
                result['stock_code'],
                datetime.now().strftime('%Y-%m-%d'),
                result['latest_price'],
                result['macd']['signal'] if result['macd'] else None,
                result['kdj']['signal'] if result['kdj'] else None,
                result['rsi']['signal'] if result['rsi'] else None,
                result['bollinger']['signal'] if result['bollinger'] else None,
                result['final_signal'],
                result['signal_strength']
            ))
            
            conn.commit()
            conn.close()
            return True
            
        except Exception as e:
            print(f"[EMOJI]: {e}")
            return False

# ================================
# [EMOJI]
# ================================

def main():
    """[EMOJI]"""
    
    # [EMOJI]ExtendedAPI
    try:
        extended_api = ExtendedAPI()
        print_status("ExtendedAPI[EMOJI]", "success")
        print_status("[EMOJI]", "success")
    except Exception as e:
        print_status(f"ExtendedAPI[EMOJI]: {e}", "error")
        return
    
    # [EMOJI]
    recommended_stocks = ['000001.SZ', '600000.SH', '000002.SZ']
    
    # [EMOJI]
    data_manager = DataManager()
    analyzer = ComprehensiveAnalyzer()
    db_manager = DatabaseManager()
    
    # [EMOJI]1[EMOJI]
    print_course_header(1, "[EMOJI]", "[EMOJI]")
    
    print("[EMOJI] [EMOJI]:")
    print("  • [EMOJI]")
    print("  • [EMOJI]")
    print("  • [EMOJI]")
    print()
    
    quality_report = data_manager.check_data_quality(recommended_stocks, ['1d'])
    
    print("\n[CHART] [EMOJI]:")
    for period, stocks in quality_report.items():
        print(f"\n{period}[EMOJI]:")
        for stock_code, info in stocks.items():
            if info['status'] == 'success':
                print(f"  [OK] {stock_code}: [EMOJI]{info['quality_score']:.1f}/10.0, [EMOJI]{info['latest_price']:.2f}[EMOJI]")
            else:
                print(f"  [X] {stock_code}: [EMOJI]")
    
    wait_for_continue("[EMOJI]")
    
    # [EMOJI]2[EMOJI]MACD[EMOJI]
    print_course_header(2, "MACD[EMOJI]", "[EMOJI]MACD[EMOJI]")
    
    print("[EMOJI] [EMOJI]:")
    print("  • MACD[EMOJI]")
    print("  • [EMOJI]")
    print("  • MACD[EMOJI]")
    print()
    
    for i, stock_code in enumerate(recommended_stocks[:2]):
        print(f"\n[CHART] [EMOJI] {stock_code} [EMOJI]MACD[EMOJI]:")
        
        df = data_manager.get_clean_data(stock_code, period='1d', count=60)
        if df is not None:
            macd_result = TechnicalIndicators.calculate_macd(df)
            
            if macd_result:
                print(f"  [UP] [EMOJI]: {len(df)}[EMOJI]")
                print(f"  [CHART] MACD[EMOJI]: {macd_result['macd']:.4f}")
                print(f"  [CHART] [EMOJI]: {macd_result['signal']:.4f}")
                print(f"  [CHART] [EMOJI]: {macd_result['histogram']:.4f}")
                print(f"  [UP] [EMOJI]: {macd_result['trend']}")
                print(f"  [TARGET] [EMOJI]: {macd_result['cross']}")
                
                if macd_result['cross'] == '[EMOJI]':
                    print(f"  [EMOJI] [EMOJI]")
                elif macd_result['cross'] == '[EMOJI]':
                    print(f"  [EMOJI] [EMOJI]")
                else:
                    print(f"  [EMOJI] [EMOJI]")
                
                # [EMOJI]
                if macd_result['buy_signal']:
                    print(f"  [TIP] [EMOJI]: [EMOJI]")
                elif macd_result['sell_signal']:
                    print(f"  [TIP] [EMOJI]: [EMOJI]")
                else:
                    print(f"  [TIP] [EMOJI]: [EMOJI]")
            else:
                print(f"  [X] MACD[EMOJI]")
        
        if i < len(recommended_stocks[:2]) - 1:
            print()
    
    wait_for_continue("MACD[EMOJI]")
    
    # [EMOJI]3[EMOJI]KDJ[EMOJI]
    print_course_header(3, "KDJ[EMOJI]", "[EMOJI]KDJ[EMOJI]")
    
    print("[EMOJI] [EMOJI]:")
    print("  • KDJ[EMOJI]K[EMOJI]D[EMOJI]J[EMOJI]")
    print("  • [EMOJI]")
    print("  • KDJ[EMOJI]")
    print()
    
    for i, stock_code in enumerate(recommended_stocks[:2]):
        print(f"\n[CHART] [EMOJI] {stock_code} [EMOJI]KDJ[EMOJI]:")
        
        df = data_manager.get_clean_data(stock_code, period='1d', count=60)
        if df is not None:
            kdj_result = TechnicalIndicators.calculate_kdj(df)
            
            if kdj_result:
                print(f"  [UP] K[EMOJI]: {kdj_result['k']:.2f} ([EMOJI]: {kdj_result['k_trend']})")
                print(f"  [UP] D[EMOJI]: {kdj_result['d']:.2f} ([EMOJI]: {kdj_result['d_trend']})")
                print(f"  [UP] J[EMOJI]: {kdj_result['j']:.2f}")
                print(f"  [TARGET] [EMOJI]: {kdj_result['signal']}")
                
                if kdj_result['signal'] == '[EMOJI]':
                    print(f"  [EMOJI] [EMOJI]")
                    print(f"  [TIP] [EMOJI]: [EMOJI]")
                elif kdj_result['signal'] == '[EMOJI]':
                    print(f"  [EMOJI] [EMOJI]")
                    print(f"  [TIP] [EMOJI]: [EMOJI]")
                else:
                    print(f"  [EMOJI] [EMOJI]")
                    print(f"  [TIP] [EMOJI]: [EMOJI]")
            else:
                print(f"  [X] KDJ[EMOJI]")
        
        if i < len(recommended_stocks[:2]) - 1:
            print()
    
    wait_for_continue("KDJ[EMOJI]")
    
    # [EMOJI]4[EMOJI]RSI[EMOJI]
    print_course_header(4, "RSI[EMOJI]", "[EMOJI]RSI[EMOJI]")
    
    print("[EMOJI] [EMOJI]:")
    print("  • RSI[EMOJI]")
    print("  • [EMOJI]")
    print("  • [EMOJI]RSI[EMOJI]")
    print()
    
    for stock_code in recommended_stocks[:1]:  # [EMOJI]
        print(f"\n[CHART] [EMOJI] {stock_code} [EMOJI]RSI[EMOJI]:")
        
        df = data_manager.get_clean_data(stock_code, period='1d', count=60)
        if df is not None:
            rsi_result = TechnicalIndicators.calculate_rsi(df)
            
            if rsi_result:
                print(f"  [UP] RSI[EMOJI]: {rsi_result['rsi']:.2f}")
                print(f"  [UP] [EMOJI]: {rsi_result['trend']}")
                print(f"  [TARGET] [EMOJI]: {rsi_result['signal']}")
                print(f"  [CHART] [EMOJI]: {'[EMOJI]' if rsi_result['overbought'] else '[EMOJI]'}")
                print(f"  [CHART] [EMOJI]: {'[EMOJI]' if rsi_result['oversold'] else '[EMOJI]'}")
                print(f"  [SEARCH] [EMOJI]: {'[EMOJI]' if rsi_result['divergence'] else '[EMOJI]'}")
                
                # [EMOJI]
                if rsi_result['rsi'] > 70:
                    print(f"\n  [BOOK] RSI[EMOJI]:")
                    print(f"    RSI > 70[EMOJI]")
                    print(f"    [EMOJI]")
                    print(f"  [TIP] [EMOJI]: [EMOJI]")
                elif rsi_result['rsi'] < 30:
                    print(f"\n  [BOOK] RSI[EMOJI]:")
                    print(f"    RSI < 30[EMOJI]")
                    print(f"    [EMOJI]")
                    print(f"  [TIP] [EMOJI]: [EMOJI]")
                else:
                    print(f"\n  [BOOK] RSI[EMOJI]:")
                    print(f"    RSI[EMOJI]30-70[EMOJI]")
                    print(f"    [EMOJI]")
                    print(f"  [TIP] [EMOJI]: [EMOJI]")
                
                if rsi_result['divergence']:
                    print(f"\n  [!] [EMOJI]:")
                    print(f"    [EMOJI]RSI[EMOJI]")
                    print(f"    [EMOJI]")
            else:
                print(f"  [X] RSI[EMOJI]")
    
    wait_for_continue("RSI[EMOJI]")
    
    # [EMOJI]5[EMOJI]
    print_course_header(5, "[EMOJI]", "[EMOJI]%B[EMOJI]")
    
    print("[EMOJI] [EMOJI]:")
    print("  • [EMOJI]")
    print("  • %B[EMOJI]")
    print("  • [EMOJI]")
    print()
    
    for stock_code in recommended_stocks[:1]:
        print(f"\n[CHART] [EMOJI] {stock_code} [EMOJI]:")
        
        df = data_manager.get_clean_data(stock_code, period='1d', count=60)
        if df is not None:
            boll_result = TechnicalIndicators.calculate_bollinger_bands(df)
            
            if boll_result:
                print(f"  [UP] [EMOJI]: {boll_result['current_price']:.2f}[EMOJI]")
                print(f"  [CHART] [EMOJI]: {boll_result['upper']:.2f}[EMOJI]")
                print(f"  [CHART] [EMOJI]: {boll_result['middle']:.2f}[EMOJI]")
                print(f"  [CHART] [EMOJI]: {boll_result['lower']:.2f}[EMOJI]")
                print(f"  [EMOJI] [EMOJI]: {boll_result['bandwidth']:.2f}%")
                print(f"  [EMOJI] %B[EMOJI]: {boll_result['percent_b']:.2f}")
                print(f"  [TARGET] [EMOJI]: {boll_result['position']}")
                print(f"  [TARGET] [EMOJI]: {boll_result['signal']}")
                
                # [EMOJI]
                print(f"\n  [BOOK] [EMOJI]:")
                if boll_result['position'] == '[EMOJI]':
                    print(f"    [EMOJI]")
                    print(f"    [EMOJI]")
                    print(f"  [TIP] [EMOJI]: [EMOJI]")
                elif boll_result['position'] == '[EMOJI]':
                    print(f"    [EMOJI]")
                    print(f"    [EMOJI]")
                    print(f"  [TIP] [EMOJI]: [EMOJI]")
                elif boll_result['position'] == '[EMOJI]':
                    print(f"    [EMOJI]")
                    print(f"  [TIP] [EMOJI]: [EMOJI]")
                else:
                    print(f"    [EMOJI]")
                    print(f"  [TIP] [EMOJI]: [EMOJI]")
                
                # %B[EMOJI]
                print(f"\n  [CHART] %B[EMOJI]:")
                if boll_result['percent_b'] > 1:
                    print(f"    %B > 1[EMOJI]")
                elif boll_result['percent_b'] < 0:
                    print(f"    %B < 0[EMOJI]")
                elif boll_result['percent_b'] > 0.8:
                    print(f"    %B > 0.8[EMOJI]")
                elif boll_result['percent_b'] < 0.2:
                    print(f"    %B < 0.2[EMOJI]")
                else:
                    print(f"    %B[EMOJI]")
            else:
                print(f"  [X] [EMOJI]")
    
    wait_for_continue("[EMOJI]")
    
    # [EMOJI]6[EMOJI]
    print_course_header(6, "[EMOJI]", "[EMOJI]")
    
    print("[EMOJI] [EMOJI]:")
    print("  • [EMOJI]")
    print("  • [EMOJI]")
    print("  • [EMOJI]")
    print()
    
    print("[SEARCH] [EMOJI]...")
    
    analysis_results = []
    
    for stock_code in recommended_stocks:
        result = analyzer.analyze_stock(stock_code)
        if result:
            analysis_results.append(result)
            
            print(f"\n[CHART] {stock_code} [EMOJI]:")
            print(f"  [MONEY] [EMOJI]: {result['latest_price']:.2f}[EMOJI]")
            print(f"  [CHART] [EMOJI]: {result['data_length']}[EMOJI]")
            
            print(f"\n  [SEARCH] [EMOJI]:")
            if result['macd']:
                print(f"    MACD: {result['macd']['cross']} ([EMOJI]: {result['macd']['trend']})")
            if result['kdj']:
                print(f"    KDJ: {result['kdj']['signal']} (K: {result['kdj']['k']:.1f}, D: {result['kdj']['d']:.1f})")
            if result['rsi']:
                print(f"    RSI: {result['rsi']['signal']} ([EMOJI]: {result['rsi']['rsi']:.1f})")
            if result['bollinger']:
                print(f"    [EMOJI]: {result['bollinger']['signal']} ([EMOJI]: {result['bollinger']['position']})")
            
            print(f"\n  [TARGET] [EMOJI]:")
            print(f"    [EMOJI]: {result['signal_emoji']} {result['final_signal']}")
            print(f"    [EMOJI]: {result['signal_strength']} ([EMOJI]: {result['buy_signals']}, [EMOJI]: {result['sell_signals']})")
            
            # [EMOJI]
            print(f"\n  [TIP] [EMOJI]:")
            if result['final_signal'] in ['[EMOJI]', '[EMOJI]']:
                print(f"    [EMOJI]")
                print(f"    [EMOJI]")
            elif result['final_signal'] in ['[EMOJI]', '[EMOJI]']:
                print(f"    [EMOJI]")
                print(f"    [EMOJI]")
            else:
                print(f"    [EMOJI]")
                print(f"    [EMOJI]")
            
            # [EMOJI]
            db_manager.save_analysis_result(result)
    
    wait_for_continue("[EMOJI]")
    
    # [EMOJI]7[EMOJI]
    print_course_header(7, "[EMOJI]", "[EMOJI]")
    
    print("[EMOJI] [EMOJI]:")
    print("  • [EMOJI]")
    print("  • [EMOJI]")
    print("  • [EMOJI]")
    print()
    
    if analysis_results:
        print("[CHART] [EMOJI]:")
        print("=" * 60)
        
        # [EMOJI]
        sorted_results = sorted(analysis_results, key=lambda x: x['signal_strength'], reverse=True)
        
        buy_candidates = []
        sell_candidates = []
        hold_candidates = []
        
        for result in sorted_results:
            print(f"\n{result['stock_code']} - {result['latest_price']:.2f}[EMOJI]")
            print(f"  [EMOJI]: {result['signal_emoji']} {result['final_signal']} ([EMOJI]: {result['signal_strength']})")
            
            if result['final_signal'] in ['[EMOJI]', '[EMOJI]']:
                buy_candidates.append(result)
                print(f"  [TIP] [EMOJI]: [EMOJI]")
            elif result['final_signal'] in ['[EMOJI]', '[EMOJI]']:
                sell_candidates.append(result)
                print(f"  [TIP] [EMOJI]: [EMOJI]")
            else:
                hold_candidates.append(result)
                print(f"  [TIP] [EMOJI]: [EMOJI]")
        
        # [EMOJI]
        print(f"\n[EMOJI] [EMOJI]:")
        print("=" * 40)
        
        if buy_candidates:
            print(f"\n[EMOJI] [EMOJI] ({len(buy_candidates)}[EMOJI]):")
            for candidate in buy_candidates:
                print(f"  • {candidate['stock_code']}: {candidate['final_signal']} ([EMOJI]: {candidate['signal_strength']})")
            
            print(f"\n[TIP] [EMOJI]:")
            print(f"  • [EMOJI]")
            print(f"  • [EMOJI]30%")
            print(f"  • [EMOJI]5-10%")
        
        if sell_candidates:
            print(f"\n[EMOJI] [EMOJI] ({len(sell_candidates)}[EMOJI]):")
            for candidate in sell_candidates:
                print(f"  • {candidate['stock_code']}: {candidate['final_signal']} ([EMOJI]: {candidate['signal_strength']})")
        
        if hold_candidates:
            print(f"\n[EMOJI] [EMOJI] ({len(hold_candidates)}[EMOJI]):")
            for candidate in hold_candidates:
                print(f"  • {candidate['stock_code']}: [EMOJI]")
        
        # [EMOJI]
        print(f"\n[!] [EMOJI]:")
        print(f"  • [EMOJI]")
        print(f"  • [EMOJI]")
        print(f"  • [EMOJI]")
        print(f"  • [EMOJI]")
    
    wait_for_continue("[EMOJI]")
    
    # [EMOJI]8[EMOJI]
    print_course_header(8, "[EMOJI]", "[EMOJI]")
    
    print("[EMOJI] [EMOJI]:")
    print("  • [EMOJI]")
    print("  • [EMOJI]")
    print("  • [EMOJI]")
    print()
    
    try:
        conn = sqlite3.connect(db_manager.db_path)
        cursor = conn.cursor()
        
        # [EMOJI]
        today = datetime.now().strftime('%Y-%m-%d')
        cursor.execute('''
            SELECT stock_code, latest_price, final_signal, signal_strength, created_time
            FROM analysis_results 
            WHERE analysis_date = ?
            ORDER BY signal_strength DESC
        ''', (today,))
        
        results = cursor.fetchall()
        conn.close()
        
        if results:
            print(f"[CHART] [EMOJI] ({len(results)}[EMOJI]):")
            print("=" * 50)
            
            for result in results:
                stock_code, price, signal, strength, created_time = result
                print(f"{stock_code}: {price:.2f}[EMOJI] - {signal} ([EMOJI]: {strength}) [{created_time}]")
            
            print(f"\n[EMOJI] [EMOJI]: {db_manager.db_path}")
            print(f"[UP] [EMOJI]")
        else:
            print(f"[CHART] [EMOJI]")
        
    except Exception as e:
        print(f"[X] [EMOJI]: {e}")
    
    wait_for_continue("[EMOJI]")
    
    # [EMOJI]
    print_separator("[EMOJI]")
    print("[EMOJI] [EMOJI]EasyXT[EMOJI]API[EMOJI]")
    print()
    print("[BOOK] [EMOJI]:")
    print("  [OK] [EMOJI]")
    print("  [OK] MACD[EMOJI]")
    print("  [OK] KDJ[EMOJI]")
    print("  [OK] RSI[EMOJI]")
    print("  [OK] [EMOJI]")
    print("  [OK] [EMOJI]")
    print("  [OK] [EMOJI]")
    print("  [OK] [EMOJI]")
    print()
    print("[TIP] [EMOJI]:")
    print("  • [EMOJI]")
    print("  • [EMOJI]")
    print("  • [EMOJI]")
    print("  • [EMOJI]")
    print()
    print("[TOOL] [EMOJI]:")
    print("  • [EMOJI]")
    print("  • [EMOJI]")
    print("  • [EMOJI]")
    print("  • [EMOJI]")
    print()
    print("[!] [EMOJI]:")
    print("  [EMOJI]")
    print("  [EMOJI]")
    print()
    print("[EMOJI] [EMOJI]")

if __name__ == "__main__":
    main()