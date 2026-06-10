#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
[LAUNCH] qstock[EMOJI]EasyXT[EMOJI]
=======================================

[EMOJI]qstock[EMOJI]EasyXT[EMOJI]
[EMOJI]qstock[EMOJI]EasyXT[EMOJI]

[EMOJI]
[EMOJI] qstock[EMOJI] ([EMOJI])
[EMOJI] EasyXT[EMOJI] ([EMOJI]A[EMOJI])
[EMOJI] [EMOJI] ([EMOJI]+[EMOJI])
[EMOJI] [EMOJI] ([EMOJI])
[EMOJI] [EMOJI] ([EMOJI])
[EMOJI] [EMOJI] ([EMOJI])

[EMOJI]quant
[EMOJI]2.0.0 ([EMOJI])
[EMOJI]2025-01-26
GitHub: https://github.com/quant-king299/EasyXT
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import os
import sys
import time
import json
import warnings
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Tuple, Any
import threading
import queue
from concurrent.futures import ThreadPoolExecutor, as_completed

warnings.filterwarnings('ignore')

# [EMOJI]
plt.rcParams['font.sans-serif'] = ['SimHei', 'Microsoft YaHei']
plt.rcParams['axes.unicode_minus'] = False
sns.set_style("whitegrid")

print("[LAUNCH] qstock[EMOJI]EasyXT[EMOJI]")
print("=" * 60)

# ==================== [EMOJI] ====================

# 1. qstock[EMOJI]
try:
    import qstock as qs
    QSTOCK_AVAILABLE = True
    print("[OK] qstock[EMOJI]")
    print(f"   [EMOJI]: {getattr(qs, '__version__', '[EMOJI]')}")
    print("   [EMOJI]: [EMOJI]")
except ImportError as e:
    print(f"[X] qstock[EMOJI]: {e}")
    print("[TIP] [EMOJI]: pip install qstock")
    print("[EMOJI] [EMOJI]: https://github.com/tkfy920/qstock")
    QSTOCK_AVAILABLE = False

# 2. EasyXT[EMOJI]
current_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.append(os.path.dirname(current_dir))

try:
    import easy_xt
    from easy_xt.api import EasyXT
    EASYXT_AVAILABLE = True
    print("[OK] EasyXT[EMOJI]")
    print("   [EMOJI]: A[EMOJI]")
    print("   [EMOJI]: [EMOJI]")
except ImportError as e:
    print(f"[X] EasyXT[EMOJI]: {e}")
    print("[TIP] [EMOJI]EasyXT[EMOJI]")
    print("[EMOJI] [EMOJI]: https://github.com/quant-king299/EasyXT")
    EASYXT_AVAILABLE = False

# 3. [EMOJI]
try:
    import talib
    TALIB_AVAILABLE = True
    print("[OK] TA-Lib[EMOJI]")
except ImportError:
    print("[!] TA-Lib[EMOJI]")
    TALIB_AVAILABLE = False

print("=" * 60)

# ==================== [EMOJI] ====================

# [EMOJI]
TRADING_CONFIG = {
    'userdata_path': r'D:\[EMOJI]QMT[EMOJI]\userdata_mini',  # [EMOJI]
    'account_id': '39020958',  # [EMOJI]
    'session_id': 'qstock_easyxt_session',
    'max_position_ratio': 0.8,  # [EMOJI]
    'single_stock_ratio': 0.2,  # [EMOJI]
    'stop_loss_ratio': 0.05,    # [EMOJI]
    'take_profit_ratio': 0.15,  # [EMOJI]
}

# [EMOJI]
STRATEGY_CONFIG = {
    'data_period': 60,           # [EMOJI]([EMOJI])
    'signal_threshold': 70,      # [EMOJI]
    'min_volume': 1000000,       # [EMOJI]
    'price_range': (5, 200),     # [EMOJI]
    'update_interval': 30,       # [EMOJI]([EMOJI])
}

# [EMOJI]
STOCK_POOL = {
    'core_stocks': ['000001', '000002', '600000', '600036', '000858'],  # [EMOJI]
    'growth_stocks': ['300059', '300015', '002415', '000725'],          # [EMOJI]
    'value_stocks': ['600519', '000858', '002304', '600036'],           # [EMOJI]
    'tech_stocks': ['000063', '002230', '300496', '688981'],            # [EMOJI]
}

class QStockEasyXTIntegration:
    """qstock[EMOJI]EasyXT[EMOJI]"""
    
    def __init__(self):
        """[EMOJI]"""
        print("\n[TOOL] [EMOJI]qstock[EMOJI]EasyXT[EMOJI]...")
        
        # [EMOJI]
        self.data_cache = {}
        self.signal_history = []
        self.trade_history = []
        self.performance_metrics = {}
        
        # [EMOJI]
        self.is_trading_enabled = False
        self.is_monitoring = False
        self.last_update_time = None
        
        # [EMOJI]
        self.ensure_directories()
        
        # [EMOJI]
        self.init_data_module()
        
        # [EMOJI]
        self.init_trading_module()
        
        print("[OK] [EMOJI]")
    
    def ensure_directories(self):
        """[EMOJI]"""
        directories = ['data', 'logs', 'reports', 'backtest']
        for directory in directories:
            if not os.path.exists(directory):
                os.makedirs(directory)
                print(f"[EMOJI] [EMOJI]: {directory}")
    
    def init_data_module(self):
        """[EMOJI]qstock[EMOJI]"""
        print("\n[CHART] [EMOJI]qstock[EMOJI]...")
        
        if not QSTOCK_AVAILABLE:
            print("[X] qstock[EMOJI]")
            return
        
        # [EMOJI]qstock[EMOJI]
        try:
            # [EMOJI] - [EMOJI]qstock API[EMOJI]
            end_date = datetime.now().strftime('%Y-%m-%d')
            start_date = (datetime.now() - timedelta(days=5)).strftime('%Y-%m-%d')
            test_data = qs.get_data('000001', start=start_date, end=end_date)
            
            if test_data is not None and not test_data.empty:
                print("[OK] qstock[EMOJI]")
                print(f"   [EMOJI]: {len(test_data)} [EMOJI]")
                print(f"   [EMOJI]: {test_data['close'].iloc[-1]:.2f}")
            else:
                print("[!] qstock[EMOJI]")
        except Exception as e:
            print(f"[!] qstock[EMOJI]: {e}")
            # [EMOJI]
            try:
                test_data = qs.get_data('000001')
                if test_data is not None and not test_data.empty:
                    print("[OK] qstock[EMOJI]")
                    print(f"   [EMOJI]: {len(test_data)}")
                else:
                    print("[!] qstock[EMOJI]")
            except Exception as e2:
                print(f"[!] qstock[EMOJI]: {e2}")
    
    def init_trading_module(self):
        """[EMOJI]EasyXT[EMOJI]"""
        print("\n[EMOJI] [EMOJI]EasyXT[EMOJI]...")
        
        if not EASYXT_AVAILABLE:
            print("[X] EasyXT[EMOJI]")
            return
        
        try:
            # [EMOJI]EasyXT[EMOJI]
            self.trader = EasyXT()
            print("[OK] EasyXT[EMOJI]")
            
            # [EMOJI]
            if self.trader.init_data():
                print("[OK] EasyXT[EMOJI]")
            else:
                print("[!] EasyXT[EMOJI]")
            
            # [EMOJI]
            if self.trader.init_trade(
                TRADING_CONFIG['userdata_path'], 
                TRADING_CONFIG['session_id']
            ):
                print("[OK] EasyXT[EMOJI]")
                
                # [EMOJI]
                if self.trader.add_account(TRADING_CONFIG['account_id'], 'STOCK'):
                    print("[OK] [EMOJI]")
                    self.is_trading_enabled = True
                else:
                    print("[!] [EMOJI]")
            else:
                print("[!] EasyXT[EMOJI]")
                print("[TIP] [EMOJI]:")
                print("   1. [EMOJI]")
                print("   2. userdata[EMOJI]")
                print("   3. [EMOJI]ID[EMOJI]")
                
        except Exception as e:
            print(f"[X] EasyXT[EMOJI]: {e}")
    
    # ==================== qstock[EMOJI] ====================
    
    def get_multi_source_data(self, symbol: str, period: int = 60) -> Dict[str, pd.DataFrame]:
        """
        [EMOJI]qstock[EMOJI]
        
        Args:
            symbol: [EMOJI]
            period: [EMOJI]([EMOJI])
            
        Returns:
            [EMOJI]
        """
        print(f"\n[CHART] [EMOJI]qstock[EMOJI] {symbol} [EMOJI]...")
        
        data_dict = {}
        
        if not QSTOCK_AVAILABLE:
            print("[X] qstock[EMOJI]")
            return data_dict
        
        try:
            # 1. [EMOJI]K[EMOJI] - [EMOJI]qstock API[EMOJI]
            print("  [UP] [EMOJI]K[EMOJI]...")
            try:
                # [EMOJI]1: [EMOJI]
                end_date = datetime.now().strftime('%Y-%m-%d')
                start_date = (datetime.now() - timedelta(days=period)).strftime('%Y-%m-%d')
                kline_data = qs.get_data(symbol, start=start_date, end=end_date)
            except:
                try:
                    # [EMOJI]2: [EMOJI]
                    kline_data = qs.get_data(symbol)
                    if kline_data is not None and not kline_data.empty and len(kline_data) > period:
                        kline_data = kline_data.tail(period)  # [EMOJI]
                except:
                    kline_data = None
            
            if kline_data is not None and not kline_data.empty:
                data_dict['kline'] = self.clean_kline_data(kline_data)
                print(f"    [OK] K[EMOJI]: {len(data_dict['kline'])} [EMOJI]")
            
            # 2. [EMOJI]
            print("  [CHART] [EMOJI]...")
            try:
                # [EMOJI]
                if hasattr(qs, 'get_realtime'):
                    realtime_data = qs.get_realtime([symbol])
                elif hasattr(qs, 'realtime'):
                    realtime_data = qs.realtime([symbol])
                else:
                    realtime_data = None
                    
                if realtime_data is not None and not realtime_data.empty:
                    data_dict['realtime'] = realtime_data
                    print(f"    [OK] [EMOJI]: {len(realtime_data)} [EMOJI]")
                else:
                    print("    [!] [EMOJI]")
            except Exception as e:
                print(f"    [!] [EMOJI]: {e}")
            
            # 3. [EMOJI]
            print("  [MONEY] [EMOJI]...")
            try:
                if hasattr(qs, 'get_fund_flow'):
                    fund_flow = qs.get_fund_flow([symbol])
                elif hasattr(qs, 'fund_flow'):
                    fund_flow = qs.fund_flow([symbol])
                else:
                    fund_flow = None
                    
                if fund_flow is not None and not fund_flow.empty:
                    data_dict['fund_flow'] = fund_flow
                    print(f"    [OK] [EMOJI]: {len(fund_flow)} [EMOJI]")
                else:
                    print("    [!] [EMOJI]")
            except Exception as e:
                print(f"    [!] [EMOJI]: {e}")
            
            # 4. [EMOJI]
            print("  [EMOJI] [EMOJI]...")
            try:
                if hasattr(qs, 'get_financial_data'):
                    financial_data = qs.get_financial_data(symbol)
                elif hasattr(qs, 'financial'):
                    financial_data = qs.financial(symbol)
                else:
                    financial_data = None
                    
                if financial_data is not None and not financial_data.empty:
                    data_dict['financial'] = financial_data
                    print(f"    [OK] [EMOJI]: {len(financial_data)} [EMOJI]")
                else:
                    print("    [!] [EMOJI]")
            except Exception as e:
                print(f"    [!] [EMOJI]: {e}")
            
            # 5. [EMOJI]
            print("  [EMOJI] [EMOJI]...")
            try:
                if hasattr(qs, 'get_news'):
                    news_data = qs.get_news(symbol)
                elif hasattr(qs, 'news'):
                    news_data = qs.news(symbol)
                else:
                    news_data = None
                    
                if news_data is not None and not news_data.empty:
                    data_dict['news'] = news_data
                    print(f"    [OK] [EMOJI]: {len(news_data)} [EMOJI]")
                else:
                    print("    [!] [EMOJI]")
            except Exception as e:
                print(f"    [!] [EMOJI]: {e}")
            
            # [EMOJI]
            self.data_cache[symbol] = {
                'data': data_dict,
                'timestamp': datetime.now(),
                'symbol': symbol
            }
            
            print(f"[OK] {symbol} [EMOJI] {len(data_dict)} [EMOJI]")
            
        except Exception as e:
            print(f"[X] [EMOJI]: {e}")
        
        return data_dict
    
    def clean_kline_data(self, data: pd.DataFrame) -> pd.DataFrame:
        """[EMOJI]K[EMOJI]"""
        if data is None or data.empty:
            return pd.DataFrame()
        
        # [EMOJI]
        column_mapping = {
            'Open': 'open', 'High': 'high', 'Low': 'low', 'Close': 'close', 'Volume': 'volume',
            'open': 'open', 'high': 'high', 'low': 'low', 'close': 'close', 'volume': 'volume'
        }
        
        for old_col, new_col in column_mapping.items():
            if old_col in data.columns:
                data = data.rename(columns={old_col: new_col})
        
        # [EMOJI]
        required_cols = ['open', 'high', 'low', 'close', 'volume']
        missing_cols = [col for col in required_cols if col not in data.columns]
        
        if missing_cols:
            print(f"[!] [EMOJI]: {missing_cols}")
            return pd.DataFrame()
        
        # [EMOJI]
        data = data.dropna()
        data = data[data['volume'] > 0]
        
        # [EMOJI]
        for col in required_cols:
            data[col] = pd.to_numeric(data[col], errors='coerce')
        
        data = data.dropna()
        
        return data
    
    def get_market_overview(self) -> Dict[str, Any]:
        """[EMOJI]"""
        print("\n[EMOJI] [EMOJI]...")
        
        market_data = {}
        
        if not QSTOCK_AVAILABLE:
            return market_data
        
        try:
            # 1. [EMOJI]
            print("  [CHART] [EMOJI]...")
            indices = ['000001', '399001', '399006']  # [EMOJI]
            index_data = {}
            
            for index in indices:
                try:
                    # [EMOJI]
                    if hasattr(qs, 'get_realtime'):
                        data = qs.get_realtime([index])
                    elif hasattr(qs, 'realtime'):
                        data = qs.realtime([index])
                    else:
                        # [EMOJI]
                        data = qs.get_data(index)
                        if data is not None and not data.empty:
                            # [EMOJI]
                            latest = data.iloc[-1]
                            data = pd.DataFrame([{
                                'code': index,
                                'price': latest['close'],
                                'change': latest['close'] - latest['open'],
                                'change_pct': (latest['close'] - latest['open']) / latest['open'] * 100
                            }])
                    
                    if data is not None and not data.empty:
                        index_data[index] = data.iloc[0].to_dict()
                except Exception as e:
                    print(f"    [!] {index} [EMOJI]: {e}")
                    continue
            
            market_data['indices'] = index_data
            print(f"    [OK] [EMOJI]: {len(index_data)} [EMOJI]")
            
            # 2. [EMOJI]
            print("  [UP] [EMOJI]...")
            try:
                limit_stats = {'limit_up_count': 0, 'limit_down_count': 0}
                
                if hasattr(qs, 'get_limit_up'):
                    limit_up = qs.get_limit_up()
                    if limit_up is not None and not limit_up.empty:
                        limit_stats['limit_up_count'] = len(limit_up)
                
                if hasattr(qs, 'get_limit_down'):
                    limit_down = qs.get_limit_down()
                    if limit_down is not None and not limit_down.empty:
                        limit_stats['limit_down_count'] = len(limit_down)
                
                market_data['limit_stats'] = limit_stats
                print(f"    [OK] [EMOJI]: {limit_stats['limit_up_count']} [EMOJI]")
                print(f"    [OK] [EMOJI]: {limit_stats['limit_down_count']} [EMOJI]")
            except Exception as e:
                print(f"    [!] [EMOJI]: {e}")
            
            # 3. [EMOJI]
            print("  [EMOJI] [EMOJI]...")
            try:
                hot_concepts = None
                if hasattr(qs, 'get_hot_concept'):
                    hot_concepts = qs.get_hot_concept()
                elif hasattr(qs, 'hot_concept'):
                    hot_concepts = qs.hot_concept()
                
                if hot_concepts is not None and not hot_concepts.empty:
                    market_data['hot_concepts'] = hot_concepts.head(10)
                    print(f"    [OK] [EMOJI]: {len(market_data['hot_concepts'])} [EMOJI]")
                else:
                    print("    [!] [EMOJI]")
            except Exception as e:
                print(f"    [!] [EMOJI]: {e}")
            
            # 4. [EMOJI]
            print("  [MONEY] [EMOJI]...")
            try:
                market_fund_flow = None
                if hasattr(qs, 'get_market_fund_flow'):
                    market_fund_flow = qs.get_market_fund_flow()
                elif hasattr(qs, 'market_fund_flow'):
                    market_fund_flow = qs.market_fund_flow()
                
                if market_fund_flow is not None:
                    market_data['market_fund_flow'] = market_fund_flow
                    print("    [OK] [EMOJI]")
                else:
                    print("    [!] [EMOJI]")
            except Exception as e:
                print(f"    [!] [EMOJI]: {e}")
            
        except Exception as e:
            print(f"[X] [EMOJI]: {e}")
        
        return market_data
    
    # ==================== [EMOJI] ====================
    
    def calculate_technical_indicators(self, data: pd.DataFrame) -> pd.DataFrame:
        """[EMOJI]"""
        if data is None or data.empty:
            return data
        
        print("[UP] [EMOJI]...")
        
        try:
            # [EMOJI]
            data['MA5'] = data['close'].rolling(window=5).mean()
            data['MA10'] = data['close'].rolling(window=10).mean()
            data['MA20'] = data['close'].rolling(window=20).mean()
            data['MA60'] = data['close'].rolling(window=60).mean()
            
            # EMA[EMOJI]
            data['EMA12'] = data['close'].ewm(span=12).mean()
            data['EMA26'] = data['close'].ewm(span=26).mean()
            
            # MACD
            data['MACD'] = data['EMA12'] - data['EMA26']
            data['MACD_signal'] = data['MACD'].ewm(span=9).mean()
            data['MACD_hist'] = data['MACD'] - data['MACD_signal']
            
            # RSI
            delta = data['close'].diff()
            gain = (delta.where(delta > 0, 0)).rolling(window=14).mean()
            loss = (-delta.where(delta < 0, 0)).rolling(window=14).mean()
            rs = gain / loss
            data['RSI'] = 100 - (100 / (1 + rs))
            
            # [EMOJI]
            data['BB_middle'] = data['close'].rolling(window=20).mean()
            bb_std = data['close'].rolling(window=20).std()
            data['BB_upper'] = data['BB_middle'] + (bb_std * 2)
            data['BB_lower'] = data['BB_middle'] - (bb_std * 2)
            data['BB_width'] = (data['BB_upper'] - data['BB_lower']) / data['BB_middle']
            
            # KDJ
            low_min = data['low'].rolling(window=9).min()
            high_max = data['high'].rolling(window=9).max()
            rsv = (data['close'] - low_min) / (high_max - low_min) * 100
            data['K'] = rsv.ewm(com=2).mean()
            data['D'] = data['K'].ewm(com=2).mean()
            data['J'] = 3 * data['K'] - 2 * data['D']
            
            # [EMOJI]
            data['volume_ma5'] = data['volume'].rolling(window=5).mean()
            data['volume_ma20'] = data['volume'].rolling(window=20).mean()
            data['volume_ratio'] = data['volume'] / data['volume_ma20']
            
            # [EMOJI]
            data['price_strength'] = (data['close'] - data['low']) / (data['high'] - data['low'])
            
            # [EMOJI]
            data['volatility'] = data['close'].rolling(window=20).std() / data['close'].rolling(window=20).mean()
            
            # [EMOJI]TA-Lib[EMOJI]
            if TALIB_AVAILABLE:
                try:
                    import talib
                    # ADX
                    data['ADX'] = talib.ADX(data['high'].values, data['low'].values, data['close'].values, timeperiod=14)
                    # CCI
                    data['CCI'] = talib.CCI(data['high'].values, data['low'].values, data['close'].values, timeperiod=14)
                    # Williams %R
                    data['WILLR'] = talib.WILLR(data['high'].values, data['low'].values, data['close'].values, timeperiod=14)
                    print("  [OK] TA-Lib[EMOJI]")
                except:
                    print("  [!] TA-Lib[EMOJI]")
            
            print(f"[OK] [EMOJI] {len([col for col in data.columns if col not in ['open', 'high', 'low', 'close', 'volume']])} [EMOJI]")
            
        except Exception as e:
            print(f"[X] [EMOJI]: {e}")
        
        return data
    
    def generate_trading_signals(self, symbol: str, data: pd.DataFrame) -> List[Dict]:
        """[EMOJI]"""
        print(f"\n[TARGET] [EMOJI] {symbol} [EMOJI]...")
        
        if data is None or data.empty:
            return []
        
        signals = []
        
        try:
            # [EMOJI]
            if len(data) < 30:
                print("[!] [EMOJI]")
                return signals
            
            latest_data = data.iloc[-1]
            prev_data = data.iloc[-2]
            
            signal_strength = 0
            signal_reasons = []
            
            # [EMOJI]1: [EMOJI]
            trend_signals = self._trend_following_strategy(data)
            signal_strength += trend_signals['strength']
            signal_reasons.extend(trend_signals['reasons'])
            
            # [EMOJI]2: [EMOJI]
            mean_reversion_signals = self._mean_reversion_strategy(data)
            signal_strength += mean_reversion_signals['strength']
            signal_reasons.extend(mean_reversion_signals['reasons'])
            
            # [EMOJI]3: [EMOJI]
            momentum_signals = self._momentum_strategy(data)
            signal_strength += momentum_signals['strength']
            signal_reasons.extend(momentum_signals['reasons'])
            
            # [EMOJI]4: [EMOJI]
            volume_signals = self._volume_confirmation_strategy(data)
            signal_strength += volume_signals['strength']
            signal_reasons.extend(volume_signals['reasons'])
            
            # [EMOJI]5: [EMOJI]
            pattern_signals = self._pattern_recognition_strategy(data)
            signal_strength += pattern_signals['strength']
            signal_reasons.extend(pattern_signals['reasons'])
            
            # [EMOJI]
            confidence = min(95, max(0, 50 + signal_strength * 10))
            
            if abs(signal_strength) >= 0.5:  # [EMOJI]
                signal_type = 'BUY' if signal_strength > 0 else 'SELL'
                
                signal = {
                    'symbol': symbol,
                    'timestamp': datetime.now(),
                    'signal_type': signal_type,
                    'strength': signal_strength,
                    'confidence': confidence,
                    'price': latest_data['close'],
                    'reasons': signal_reasons,
                    'technical_data': {
                        'MA5': latest_data.get('MA5', 0),
                        'MA20': latest_data.get('MA20', 0),
                        'RSI': latest_data.get('RSI', 50),
                        'MACD': latest_data.get('MACD', 0),
                        'volume_ratio': latest_data.get('volume_ratio', 1),
                    }
                }
                
                signals.append(signal)
                print(f"[OK] [EMOJI]{signal_type}[EMOJI]: {signal_strength:.2f}, [EMOJI]: {confidence:.1f}%")
                print(f"   [EMOJI]: {', '.join(signal_reasons[:3])}")
            else:
                print("[TIP] [EMOJI]")
            
        except Exception as e:
            print(f"[X] [EMOJI]: {e}")
        
        return signals
    
    def _trend_following_strategy(self, data: pd.DataFrame) -> Dict:
        """[EMOJI]"""
        strength = 0
        reasons = []
        
        try:
            latest = data.iloc[-1]
            
            # MA[EMOJI]
            if latest['close'] > latest['MA5'] > latest['MA20']:
                strength += 0.3
                reasons.append("[EMOJI]")
            elif latest['close'] < latest['MA5'] < latest['MA20']:
                strength -= 0.3
                reasons.append("[EMOJI]")
            
            # MA[EMOJI]
            if len(data) >= 2:
                prev = data.iloc[-2]
                if latest['MA5'] > latest['MA20'] and prev['MA5'] <= prev['MA20']:
                    strength += 0.4
                    reasons.append("MA[EMOJI]")
                elif latest['MA5'] < latest['MA20'] and prev['MA5'] >= prev['MA20']:
                    strength -= 0.4
                    reasons.append("MA[EMOJI]")
            
            # MACD[EMOJI]
            if latest['MACD'] > latest['MACD_signal'] and latest['MACD'] > 0:
                strength += 0.2
                reasons.append("MACD[EMOJI]")
            elif latest['MACD'] < latest['MACD_signal'] and latest['MACD'] < 0:
                strength -= 0.2
                reasons.append("MACD[EMOJI]")
                
        except Exception as e:
            print(f"[!] [EMOJI]: {e}")
        
        return {'strength': strength, 'reasons': reasons}
    
    def _mean_reversion_strategy(self, data: pd.DataFrame) -> Dict:
        """[EMOJI]"""
        strength = 0
        reasons = []
        
        try:
            latest = data.iloc[-1]
            
            # RSI[EMOJI]
            if latest['RSI'] < 30:
                strength += 0.3
                reasons.append("RSI[EMOJI]")
            elif latest['RSI'] > 70:
                strength -= 0.3
                reasons.append("RSI[EMOJI]")
            
            # [EMOJI]
            if latest['close'] < latest['BB_lower']:
                strength += 0.2
                reasons.append("[EMOJI]")
            elif latest['close'] > latest['BB_upper']:
                strength -= 0.2
                reasons.append("[EMOJI]")
            
            # KDJ[EMOJI]
            if latest['K'] < 20 and latest['D'] < 20:
                strength += 0.2
                reasons.append("KDJ[EMOJI]")
            elif latest['K'] > 80 and latest['D'] > 80:
                strength -= 0.2
                reasons.append("KDJ[EMOJI]")
                
        except Exception as e:
            print(f"[!] [EMOJI]: {e}")
        
        return {'strength': strength, 'reasons': reasons}
    
    def _momentum_strategy(self, data: pd.DataFrame) -> Dict:
        """[EMOJI]"""
        strength = 0
        reasons = []
        
        try:
            if len(data) < 5:
                return {'strength': 0, 'reasons': []}
            
            latest = data.iloc[-1]
            
            # [EMOJI]
            price_change_5d = (latest['close'] - data.iloc[-5]['close']) / data.iloc[-5]['close']
            if price_change_5d > 0.05:
                strength += 0.2
                reasons.append("5[EMOJI]")
            elif price_change_5d < -0.05:
                strength -= 0.2
                reasons.append("5[EMOJI]")
            
            # [EMOJI]
            if latest['volume_ratio'] > 2:
                strength += 0.1
                reasons.append("[EMOJI]")
            elif latest['volume_ratio'] < 0.5:
                strength -= 0.1
                reasons.append("[EMOJI]")
            
            # [EMOJI]
            if latest['price_strength'] > 0.8:
                strength += 0.1
                reasons.append("[EMOJI]")
            elif latest['price_strength'] < 0.2:
                strength -= 0.1
                reasons.append("[EMOJI]")
                
        except Exception as e:
            print(f"[!] [EMOJI]: {e}")
        
        return {'strength': strength, 'reasons': reasons}
    
    def _volume_confirmation_strategy(self, data: pd.DataFrame) -> Dict:
        """[EMOJI]"""
        strength = 0
        reasons = []
        
        try:
            latest = data.iloc[-1]
            
            # [EMOJI]
            price_change = (latest['close'] - data.iloc[-2]['close']) / data.iloc[-2]['close']
            volume_change = (latest['volume'] - data.iloc[-2]['volume']) / data.iloc[-2]['volume']
            
            if price_change > 0.02 and volume_change > 0.5:
                strength += 0.2
                reasons.append("[EMOJI]")
            elif price_change < -0.02 and volume_change > 0.5:
                strength -= 0.2
                reasons.append("[EMOJI]")
            
            # [EMOJI]
            if latest['volume'] > latest['volume_ma20'] * 2:
                strength += 0.1
                reasons.append("[EMOJI]")
                
        except Exception as e:
            print(f"[!] [EMOJI]: {e}")
        
        return {'strength': strength, 'reasons': reasons}
    
    def _pattern_recognition_strategy(self, data: pd.DataFrame) -> Dict:
        """[EMOJI]"""
        strength = 0
        reasons = []
        
        try:
            if len(data) < 10:
                return {'strength': 0, 'reasons': []}
            
            # [EMOJI]
            recent_data = data.tail(10)
            
            # [EMOJI]/[EMOJI]
            consecutive_up = 0
            consecutive_down = 0
            
            for i in range(1, len(recent_data)):
                if recent_data.iloc[i]['close'] > recent_data.iloc[i-1]['close']:
                    consecutive_up += 1
                    consecutive_down = 0
                elif recent_data.iloc[i]['close'] < recent_data.iloc[i-1]['close']:
                    consecutive_down += 1
                    consecutive_up = 0
                else:
                    consecutive_up = 0
                    consecutive_down = 0
            
            if consecutive_up >= 3:
                strength += 0.1
                reasons.append(f"[EMOJI]{consecutive_up}[EMOJI]")
            elif consecutive_down >= 3:
                strength -= 0.1
                reasons.append(f"[EMOJI]{consecutive_down}[EMOJI]")
            
            # [EMOJI]
            latest = data.iloc[-1]
            high_20 = data.tail(20)['high'].max()
            low_20 = data.tail(20)['low'].min()
            
            if latest['close'] > high_20 * 0.99:
                strength += 0.15
                reasons.append("[EMOJI]20[EMOJI]")
            elif latest['close'] < low_20 * 1.01:
                strength -= 0.15
                reasons.append("[EMOJI]20[EMOJI]")
                
        except Exception as e:
            print(f"[!] [EMOJI]: {e}")
        
        return {'strength': strength, 'reasons': reasons}
    
    # ==================== EasyXT[EMOJI] ====================
    
    def execute_trading_signal(self, signal: Dict) -> Dict:
        """[EMOJI]"""
        print(f"\n[EMOJI] [EMOJI]: {signal['symbol']} {signal['signal_type']}")
        
        if not self.is_trading_enabled:
            print("[!] [EMOJI]")
            return {'status': 'disabled', 'message': '[EMOJI]'}
        
        try:
            # [EMOJI]
            account_info = self.get_account_info()
            if not account_info:
                return {'status': 'error', 'message': '[EMOJI]'}
            
            # [EMOJI]
            position_info = self.get_position_info(signal['symbol'])
            
            # [EMOJI]
            risk_check = self.risk_management_check(signal, account_info, position_info)
            if not risk_check['passed']:
                return {'status': 'rejected', 'message': risk_check['reason']}
            
            # [EMOJI]
            quantity = self.calculate_trade_quantity(signal, account_info, position_info)
            if quantity <= 0:
                return {'status': 'error', 'message': '[EMOJI]'}
            
            # [EMOJI]
            if signal['signal_type'] == 'BUY':
                result = self.execute_buy_order(signal['symbol'], quantity, signal['price'])
            else:
                result = self.execute_sell_order(signal['symbol'], quantity, signal['price'])
            
            # [EMOJI]
            trade_record = {
                'timestamp': datetime.now(),
                'symbol': signal['symbol'],
                'signal_type': signal['signal_type'],
                'quantity': quantity,
                'price': signal['price'],
                'confidence': signal['confidence'],
                'result': result
            }
            self.trade_history.append(trade_record)
            
            return result
            
        except Exception as e:
            print(f"[X] [EMOJI]: {e}")
            return {'status': 'error', 'message': str(e)}
    
    def get_account_info(self) -> Dict:
        """[EMOJI]"""
        try:
            if self.is_trading_enabled and hasattr(self, 'trader'):
                account_info = self.trader.get_account_asset(TRADING_CONFIG['account_id'])
                if account_info:
                    print(f"[OK] [EMOJI]: {account_info.get('total_asset', 0):.2f}")
                    print(f"   [EMOJI]: {account_info.get('cash', 0):.2f}")
                    return account_info
            
            # [EMOJI]
            return {
                'total_asset': 100000,
                'cash': 50000,
                'market_value': 50000,
                'profit_loss': 0
            }
            
        except Exception as e:
            print(f"[!] [EMOJI]: {e}")
            return {}
    
    def get_position_info(self, symbol: str) -> Dict:
        """[EMOJI]"""
        try:
            if self.is_trading_enabled and hasattr(self, 'trader'):
                positions = self.trader.get_positions(TRADING_CONFIG['account_id'], symbol)
                if not positions.empty:
                    position = positions.iloc[0]
                    return {
                        'volume': position.get('volume', 0),
                        'can_use_volume': position.get('can_use_volume', 0),
                        'cost_price': position.get('cost_price', 0),
                        'market_value': position.get('market_value', 0)
                    }
            
            return {'volume': 0, 'can_use_volume': 0, 'cost_price': 0, 'market_value': 0}
            
        except Exception as e:
            print(f"[!] [EMOJI]: {e}")
            return {'volume': 0, 'can_use_volume': 0, 'cost_price': 0, 'market_value': 0}
    
    def risk_management_check(self, signal: Dict, account_info: Dict, position_info: Dict) -> Dict:
        """[EMOJI]"""
        try:
            # [EMOJI]1: [EMOJI]
            total_asset = account_info.get('total_asset', 100000)
            current_position_value = position_info.get('market_value', 0)
            max_position_value = total_asset * TRADING_CONFIG['max_position_ratio']
            
            if signal['signal_type'] == 'BUY':
                trade_value = signal['price'] * 100  # [EMOJI]
                if current_position_value + trade_value > max_position_value:
                    return {'passed': False, 'reason': '[EMOJI]'}
            
            # [EMOJI]2: [EMOJI]
            single_stock_max = total_asset * TRADING_CONFIG['single_stock_ratio']
            if signal['signal_type'] == 'BUY' and current_position_value > single_stock_max:
                return {'passed': False, 'reason': '[EMOJI]'}
            
            # [EMOJI]3: [EMOJI]
            if position_info.get('volume', 0) > 0:
                cost_price = position_info.get('cost_price', 0)
                current_price = signal['price']
                loss_ratio = (cost_price - current_price) / cost_price
                
                if loss_ratio > TRADING_CONFIG['stop_loss_ratio']:
                    if signal['signal_type'] == 'BUY':
                        return {'passed': False, 'reason': '[EMOJI]'}
            
            # [EMOJI]4: [EMOJI]
            if signal['confidence'] < STRATEGY_CONFIG['signal_threshold']:
                return {'passed': False, 'reason': '[EMOJI]'}
            
            return {'passed': True, 'reason': '[EMOJI]'}
            
        except Exception as e:
            return {'passed': False, 'reason': f'[EMOJI]: {e}'}
    
    def calculate_trade_quantity(self, signal: Dict, account_info: Dict, position_info: Dict) -> int:
        """[EMOJI]"""
        try:
            if signal['signal_type'] == 'BUY':
                # [EMOJI]
                available_cash = account_info.get('cash', 0)
                trade_amount = available_cash * 0.3  # [EMOJI]30%[EMOJI]
                
                # [EMOJI]
                price_with_fee = signal['price'] * 1.001
                quantity = int(trade_amount / price_with_fee) // 100 * 100
                
                return max(100, quantity)  # [EMOJI]1[EMOJI]
                
            else:
                # [EMOJI]
                can_sell = position_info.get('can_use_volume', 0)
                if can_sell > 0:
                    # [EMOJI]
                    sell_ratio = min(0.5, abs(signal['strength']))
                    quantity = int(can_sell * sell_ratio) // 100 * 100
                    return max(100, min(quantity, can_sell))
                
                return 0
                
        except Exception as e:
            print(f"[!] [EMOJI]: {e}")
            return 0
    
    def execute_buy_order(self, symbol: str, quantity: int, price: float) -> Dict:
        """[EMOJI]"""
        try:
            print(f"[UP] [EMOJI]: {symbol}, [EMOJI]: {quantity}, [EMOJI]: {price:.2f}")
            
            if hasattr(self, 'trader'):
                order_id = self.trader.buy(
                    account_id=TRADING_CONFIG['account_id'],
                    code=symbol,
                    volume=quantity,
                    price=price,
                    price_type='limit'
                )
                
                if order_id:
                    print(f"[OK] [EMOJI]: {order_id}")
                    return {'status': 'success', 'order_id': order_id, 'message': '[EMOJI]'}
                else:
                    return {'status': 'failed', 'message': '[EMOJI]'}
            else:
                print("[!] [EMOJI]")
                return {'status': 'simulated', 'message': '[EMOJI]'}
                
        except Exception as e:
            print(f"[X] [EMOJI]: {e}")
            return {'status': 'error', 'message': str(e)}
    
    def execute_sell_order(self, symbol: str, quantity: int, price: float) -> Dict:
        """[EMOJI]"""
        try:
            print(f"[EMOJI] [EMOJI]: {symbol}, [EMOJI]: {quantity}, [EMOJI]: {price:.2f}")
            
            if hasattr(self, 'trader'):
                order_id = self.trader.sell(
                    account_id=TRADING_CONFIG['account_id'],
                    code=symbol,
                    volume=quantity,
                    price=price,
                    price_type='limit'
                )
                
                if order_id:
                    print(f"[OK] [EMOJI]: {order_id}")
                    return {'status': 'success', 'order_id': order_id, 'message': '[EMOJI]'}
                else:
                    return {'status': 'failed', 'message': '[EMOJI]'}
            else:
                print("[!] [EMOJI]")
                return {'status': 'simulated', 'message': '[EMOJI]'}
                
        except Exception as e:
            print(f"[X] [EMOJI]: {e}")
            return {'status': 'error', 'message': str(e)}
    
    # ==================== [EMOJI] ====================
    
    def start_real_time_monitoring(self):
        """[EMOJI]"""
        print("\n[R] [EMOJI]...")
        
        self.is_monitoring = True
        
        # [EMOJI]
        monitor_thread = threading.Thread(target=self._monitoring_loop, daemon=True)
        monitor_thread.start()
        
        print("[OK] [EMOJI]")
        print("[TIP] [EMOJI] Ctrl+C [EMOJI]")
        
        try:
            while self.is_monitoring:
                time.sleep(1)
        except KeyboardInterrupt:
            print("\n[EMOJI] [EMOJI]...")
            self.is_monitoring = False
    
    def _monitoring_loop(self):
        """[EMOJI]"""
        while self.is_monitoring:
            try:
                print(f"\n{'='*60}")
                print(f"[R] [EMOJI] - {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
                print(f"{'='*60}")
                
                # [EMOJI]
                all_signals = []
                
                for category, stocks in STOCK_POOL.items():
                    print(f"\n[CHART] [EMOJI] {category}...")
                    
                    for stock in stocks[:2]:  # [EMOJI]
                        try:
                            # [EMOJI]
                            data_dict = self.get_multi_source_data(stock, period=30)
                            
                            if 'kline' in data_dict and not data_dict['kline'].empty:
                                # [EMOJI]
                                kline_data = self.calculate_technical_indicators(data_dict['kline'])
                                
                                # [EMOJI]
                                signals = self.generate_trading_signals(stock, kline_data)
                                all_signals.extend(signals)
                                
                                # [EMOJI]
                                latest = kline_data.iloc[-1]
                                print(f"  {stock}: [EMOJI] {latest['close']:.2f}, RSI {latest.get('RSI', 50):.1f}")
                            else:
                                print(f"  [!] {stock}: [EMOJI]K[EMOJI]")
                                
                        except Exception as e:
                            print(f"  [!] {stock} [EMOJI]: {e}")
                
                # [EMOJI]
                if all_signals:
                    print(f"\n[TARGET] [EMOJI] {len(all_signals)} [EMOJI]")
                    
                    for signal in all_signals:
                        if signal['confidence'] >= STRATEGY_CONFIG['signal_threshold']:
                            print(f"  [EMOJI] [EMOJI]: {signal['symbol']} {signal['signal_type']} ([EMOJI]: {signal['confidence']:.1f}%)")
                            
                            # [EMOJI]
                            # result = self.execute_trading_signal(signal)
                else:
                    print("[TIP] [EMOJI]")
                
                # [EMOJI]
                self._display_account_status()
                
                # [EMOJI]
                time.sleep(STRATEGY_CONFIG['update_interval'])
                
            except Exception as e:
                print(f"[X] [EMOJI]: {e}")
                time.sleep(10)
    
    def _display_account_status(self):
        """[EMOJI]"""
        try:
            account_info = self.get_account_info()
            
            print(f"\n[EMOJI] [EMOJI]:")
            print(f"  [EMOJI]: {account_info.get('total_asset', 0):,.2f}")
            print(f"  [EMOJI]: {account_info.get('cash', 0):,.2f}")
            print(f"  [EMOJI]: {account_info.get('market_value', 0):,.2f}")
            print(f"  [EMOJI]: {account_info.get('profit_loss', 0):,.2f}")
            
            if self.trade_history:
                print(f"  [EMOJI]: {len(self.trade_history)} [EMOJI]")
                
        except Exception as e:
            print(f"[!] [EMOJI]: {e}")
    
    # ==================== [EMOJI] ====================
    
    def run_backtest(self, symbol: str, start_date: str, end_date: str) -> Dict:
        """[EMOJI]"""
        print(f"\n[UP] [EMOJI] {symbol} ({start_date} [EMOJI] {end_date})")
        
        try:
            # [EMOJI]
            print("[CHART] [EMOJI]...")
            if QSTOCK_AVAILABLE:
                try:
                    historical_data = qs.get_data(symbol, start=start_date, end=end_date)
                except:
                    try:
                        # [EMOJI]
                        historical_data = qs.get_data(symbol)
                        if historical_data is not None and not historical_data.empty:
                            # [EMOJI]
                            historical_data.index = pd.to_datetime(historical_data.index)
                            start_dt = pd.to_datetime(start_date)
                            end_dt = pd.to_datetime(end_date)
                            historical_data = historical_data[(historical_data.index >= start_dt) & (historical_data.index <= end_dt)]
                    except:
                        historical_data = None
            else:
                print("[X] qstock[EMOJI]")
                return {}
            
            if historical_data is None or historical_data.empty:
                print("[X] [EMOJI]")
                return {}
            
            # [EMOJI]
            historical_data = self.clean_kline_data(historical_data)
            print(f"[OK] [EMOJI] {len(historical_data)} [EMOJI]")
            
            # [EMOJI]
            historical_data = self.calculate_technical_indicators(historical_data)
            
            # [EMOJI]
            backtest_results = self._simulate_trading(symbol, historical_data)
            
            # [EMOJI]
            performance_metrics = self._calculate_performance_metrics(backtest_results)
            
            # [EMOJI]
            self._generate_backtest_report(symbol, backtest_results, performance_metrics)
            
            return {
                'symbol': symbol,
                'period': f"{start_date} [EMOJI] {end_date}",
                'trades': backtest_results,
                'performance': performance_metrics
            }
            
        except Exception as e:
            print(f"[X] [EMOJI]: {e}")
            return {}
    
    def _simulate_trading(self, symbol: str, data: pd.DataFrame) -> List[Dict]:
        """[EMOJI]"""
        print("[R] [EMOJI]...")
        
        trades = []
        position = 0
        cash = 100000
        
        for i in range(30, len(data)):  # [EMOJI]30[EMOJI]
            current_data = data.iloc[:i+1]
            
            # [EMOJI]
            signals = self.generate_trading_signals(symbol, current_data)
            
            if signals:
                signal = signals[0]
                current_price = signal['price']
                
                if signal['signal_type'] == 'BUY' and position == 0 and cash > current_price * 100:
                    # [EMOJI]
                    quantity = int(cash * 0.3 / current_price) // 100 * 100
                    if quantity > 0:
                        position = quantity
                        cash -= quantity * current_price
                        
                        trades.append({
                            'date': data.index[i],
                            'action': 'BUY',
                            'price': current_price,
                            'quantity': quantity,
                            'cash': cash,
                            'position_value': position * current_price,
                            'total_value': cash + position * current_price,
                            'signal_confidence': signal['confidence']
                        })
                
                elif signal['signal_type'] == 'SELL' and position > 0:
                    # [EMOJI]
                    cash += position * current_price
                    
                    trades.append({
                        'date': data.index[i],
                        'action': 'SELL',
                        'price': current_price,
                        'quantity': position,
                        'cash': cash,
                        'position_value': 0,
                        'total_value': cash,
                        'signal_confidence': signal['confidence']
                    })
                    
                    position = 0
        
        print(f"[OK] [EMOJI] {len(trades)} [EMOJI]")
        return trades
    
    def _calculate_performance_metrics(self, trades: List[Dict]) -> Dict:
        """[EMOJI]"""
        if not trades:
            return {}
        
        # [EMOJI]
        total_trades = len(trades)
        buy_trades = [t for t in trades if t['action'] == 'BUY']
        sell_trades = [t for t in trades if t['action'] == 'SELL']
        
        # [EMOJI]
        initial_value = 100000
        final_value = trades[-1]['total_value']
        total_return = (final_value - initial_value) / initial_value
        
        # [EMOJI]
        trade_pairs = []
        for i in range(min(len(buy_trades), len(sell_trades))):
            buy_trade = buy_trades[i]
            sell_trade = sell_trades[i]
            
            profit = (sell_trade['price'] - buy_trade['price']) * buy_trade['quantity']
            profit_rate = profit / (buy_trade['price'] * buy_trade['quantity'])
            
            trade_pairs.append({
                'buy_date': buy_trade['date'],
                'sell_date': sell_trade['date'],
                'buy_price': buy_trade['price'],
                'sell_price': sell_trade['price'],
                'quantity': buy_trade['quantity'],
                'profit': profit,
                'profit_rate': profit_rate
            })
        
        # [EMOJI]
        winning_trades = [tp for tp in trade_pairs if tp['profit'] > 0]
        win_rate = len(winning_trades) / len(trade_pairs) if trade_pairs else 0
        
        # [EMOJI]
        avg_profit = np.mean([tp['profit'] for tp in trade_pairs]) if trade_pairs else 0
        avg_profit_rate = np.mean([tp['profit_rate'] for tp in trade_pairs]) if trade_pairs else 0
        
        return {
            'total_trades': total_trades,
            'trade_pairs': len(trade_pairs),
            'total_return': total_return,
            'win_rate': win_rate,
            'avg_profit': avg_profit,
            'avg_profit_rate': avg_profit_rate,
            'final_value': final_value,
            'max_profit': max([tp['profit'] for tp in trade_pairs]) if trade_pairs else 0,
            'max_loss': min([tp['profit'] for tp in trade_pairs]) if trade_pairs else 0
        }
    
    def _generate_backtest_report(self, symbol: str, trades: List[Dict], metrics: Dict):
        """[EMOJI]"""
        print(f"\n[CHART] {symbol} [EMOJI]")
        print("=" * 50)
        
        if not metrics:
            print("[X] [EMOJI]")
            return
        
        print(f"[EMOJI]: {metrics['total_trades']}")
        print(f"[EMOJI]: {metrics['trade_pairs']}")
        print(f"[EMOJI]: {metrics['total_return']:.2%}")
        print(f"[EMOJI]: {metrics['win_rate']:.2%}")
        print(f"[EMOJI]: {metrics['avg_profit']:.2f}")
        print(f"[EMOJI]: {metrics['avg_profit_rate']:.2%}")
        print(f"[EMOJI]: {metrics['max_profit']:.2f}")
        print(f"[EMOJI]: {metrics['max_loss']:.2f}")
        print(f"[EMOJI]: {metrics['final_value']:.2f}")
        
        # [EMOJI]
        report_file = f"reports/backtest_{symbol}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        with open(report_file, 'w', encoding='utf-8') as f:
            json.dump({
                'symbol': symbol,
                'trades': trades,
                'metrics': metrics,
                'timestamp': datetime.now().isoformat()
            }, f, ensure_ascii=False, indent=2, default=str)
        
        print(f"[EMOJI] [EMOJI]: {report_file}")
    
    # ==================== [EMOJI] ====================
    
    def run_comprehensive_demo(self):
        """[EMOJI]"""
        print("\n[LAUNCH] qstock[EMOJI]EasyXT[EMOJI]")
        print("=" * 60)
        
        try:
            # 1. [EMOJI]
            print("\n[CHART] [EMOJI]: [EMOJI]")
            market_overview = self.get_market_overview()
            
            # 2. [EMOJI]
            print("\n[UP] [EMOJI]: [EMOJI]")
            demo_symbol = '000001'
            multi_data = self.get_multi_source_data(demo_symbol, period=60)
            
            if 'kline' in multi_data and not multi_data['kline'].empty:
                # 3. [EMOJI]
                print("\n[CHART] [EMOJI]: [EMOJI]")
                kline_with_indicators = self.calculate_technical_indicators(multi_data['kline'])
                
                # 4. [EMOJI]
                print("\n[TARGET] [EMOJI]: [EMOJI]")
                signals = self.generate_trading_signals(demo_symbol, kline_with_indicators)
                
                # 5. [EMOJI]
                if signals:
                    print("\n[EMOJI] [EMOJI]: [EMOJI]")
                    account_info = self.get_account_info()
                    position_info = self.get_position_info(demo_symbol)
                    
                    for signal in signals:
                        risk_check = self.risk_management_check(signal, account_info, position_info)
                        print(f"  [EMOJI]: {risk_check}")
                
                # 6. [EMOJI]
                print("\n[UP] [EMOJI]: [EMOJI]")
                end_date = datetime.now().strftime('%Y-%m-%d')
                start_date = (datetime.now() - timedelta(days=90)).strftime('%Y-%m-%d')
                backtest_result = self.run_backtest(demo_symbol, start_date, end_date)
                
                # 7. [EMOJI]
                print("\n[CHART] [EMOJI]: [EMOJI]")
                self.create_visualization(demo_symbol, kline_with_indicators, signals)
                
            else:
                print("[X] [EMOJI]K[EMOJI]")
            
            # 8. [EMOJI]
            print("\n[R] [EMOJI]: [EMOJI]")
            print("[TIP] [EMOJI] start_real_time_monitoring() [EMOJI]")
            
            print("\n[OK] [EMOJI]")
            print("[EMOJI] qstock[EMOJI]EasyXT[EMOJI]")
            
        except Exception as e:
            print(f"[X] [EMOJI]: {e}")
    
    def create_visualization(self, symbol: str, data: pd.DataFrame, signals: List[Dict]):
        """[EMOJI]"""
        try:
            print(f"[CHART] [EMOJI] {symbol} [EMOJI]...")
            
            fig, axes = plt.subplots(3, 1, figsize=(15, 12))
            fig.suptitle(f'{symbol} qstock+EasyXT [EMOJI]', fontsize=16, fontweight='bold')
            
            # [EMOJI]1: [EMOJI]
            ax1 = axes[0]
            ax1.plot(data.index, data['close'], label='[EMOJI]', linewidth=2)
            ax1.plot(data.index, data['MA5'], label='MA5', alpha=0.7)
            ax1.plot(data.index, data['MA20'], label='MA20', alpha=0.7)
            
            # [EMOJI]
            for signal in signals:
                if signal['signal_type'] == 'BUY':
                    ax1.scatter(data.index[-1], signal['price'], color='red', marker='^', s=100, label='[EMOJI]')
                else:
                    ax1.scatter(data.index[-1], signal['price'], color='green', marker='v', s=100, label='[EMOJI]')
            
            ax1.set_title('[EMOJI]')
            ax1.legend()
            ax1.grid(True, alpha=0.3)
            
            # [EMOJI]2: [EMOJI]
            ax2 = axes[1]
            ax2.plot(data.index, data['RSI'], label='RSI', color='purple')
            ax2.axhline(y=70, color='r', linestyle='--', alpha=0.5, label='[EMOJI]')
            ax2.axhline(y=30, color='g', linestyle='--', alpha=0.5, label='[EMOJI]')
            ax2.set_title('RSI[EMOJI]')
            ax2.legend()
            ax2.grid(True, alpha=0.3)
            ax2.set_ylim(0, 100)
            
            # [EMOJI]3: MACD
            ax3 = axes[2]
            ax3.plot(data.index, data['MACD'], label='MACD', color='blue')
            ax3.plot(data.index, data['MACD_signal'], label='Signal', color='red')
            ax3.bar(data.index, data['MACD_hist'], label='Histogram', alpha=0.3)
            ax3.set_title('MACD[EMOJI]')
            ax3.legend()
            ax3.grid(True, alpha=0.3)
            
            plt.tight_layout()
            
            # [EMOJI]
            chart_file = f"reports/{symbol}_analysis_{datetime.now().strftime('%Y%m%d_%H%M%S')}.png"
            plt.savefig(chart_file, dpi=300, bbox_inches='tight')
            print(f"[CHART] [EMOJI]: {chart_file}")
            
            plt.show()
            
        except Exception as e:
            print(f"[!] [EMOJI]: {e}")

def main():
    """[EMOJI] - [EMOJI]qstock[EMOJI]EasyXT[EMOJI]"""
    print("[TARGET] [EMOJI] qstock[EMOJI]EasyXT[EMOJI]")
    print("=" * 60)
    print("[TIP] [EMOJI]qstock[EMOJI]EasyXT[EMOJI]")
    print("[LAUNCH] [EMOJI]qstock[EMOJI]EasyXT[EMOJI]")
    print("=" * 60)
    
    # [EMOJI]
    system = QStockEasyXTIntegration()
    
    # [EMOJI]
    system.run_comprehensive_demo()
    
    print("\n" + "=" * 60)
    print("[EMOJI] [EMOJI]")
    print("[TIP] [EMOJI]qstock[EMOJI]EasyXT[EMOJI]")
    print("[LAUNCH] [EMOJI]")
    print("=" * 60)
    
    # [EMOJI]: [EMOJI]
    while True:
        choice = input("\n[EMOJI]? (y/n): ").lower().strip()
        if choice in ['y', 'yes', '[EMOJI]']:
            system.start_real_time_monitoring()
            break
        elif choice in ['n', 'no', '[EMOJI]']:
            print("[EMOJI] [EMOJI]")
            break
        else:
            print("[EMOJI] y/n")

if __name__ == "__main__":
    main()