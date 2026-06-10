# -*- coding: utf-8 -*-
"""
[EMOJI]
[EMOJI]
[EMOJI]EasyXT[EMOJI]

[EMOJI]: [EMOJI]quant
[EMOJI]: 1.0 ([EMOJI])
"""

import sys
import os
import time
import logging
import pandas as pd
import numpy as np
from datetime import datetime, timedelta

# [EMOJI]Python[EMOJI]
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from easy_xt.api import EasyXT

def print_section_header(lesson_num, title, description):
    """[EMOJI]"""
    print("\n" + "=" * 70)
    print(f"[EMOJI]{lesson_num}[EMOJI]: {title}")
    print("=" * 70)
    print(f"[EMOJI] [EMOJI]: {description}")
    print("-" * 70)

def wait_for_user_input(message="[EMOJI]..."):
    """[EMOJI]"""
    if len(sys.argv) > 1 and '--auto' in sys.argv:
        print(f"\n[TIP] {message} (auto skip)")
        return
    input(f"\n[TIP] {message}")

def display_live_strategy_flowchart():
    """[EMOJI]"""
    print("\n[EMOJI] [EMOJI]")
    print("=" * 80)
    
    print("[CHART] [EMOJI]")
    print("[EMOJI] 1. [EMOJI] [EMOJI] [EMOJI]: 600415.XSHG ([EMOJI]-[EMOJI])")
    print("[EMOJI]               [EMOJI] [EMOJI]: 20[EMOJI]+RSI[EMOJI]+[EMOJI]")
    print("[EMOJI]               [EMOJI] [EMOJI]: EasyXT[EMOJI]")
    print("[EMOJI]               [EMOJI] [EMOJI]: (2)[EMOJI]")
    print("[EMOJI]               [EMOJI] [EMOJI]: (2%)[EMOJI]+[EMOJI]")
    print("[EMOJI]               [EMOJI] [EMOJI]: ([EMOJI])")
    print("[EMOJI]")
    print("[EMOJI] 2. [EMOJI] [EMOJI] [EMOJI]:")
    print("                [EMOJI] [EMOJI]: [EMOJI]EMA(EMA/SMA)[EMOJI]RSI(EMA/SMA)")
    print("                [EMOJI] RSI[EMOJI]: [EMOJI]RSI[EMOJI]30[EMOJI]70")
    print("                [EMOJI] [EMOJI]: 2%([EMOJI])")
    print("                [EMOJI] [EMOJI]: 90%([EMOJI])")
    print("                [EMOJI] [EMOJI]: [EMOJI]0.03%[EMOJI]0.1%[EMOJI]0.05%")
    
    print("\n[TOOL] [EMOJI]")
    print("[EMOJI] 1. [EMOJI] [EMOJI] EMA[EMOJI]: [EMOJI]12[EMOJI]26[EMOJI]([EMOJI])")
    print("[EMOJI]                  [EMOJI] [EMOJI]: [EMOJI]>10[EMOJI]20%")
    print("[EMOJI]                  [EMOJI] [EMOJI]: 10:30/11:00/13:15/14:00/14:45(5[EMOJI])")
    print("[EMOJI]                  [EMOJI] [EMOJI]: 10[EMOJI]")
    print("[EMOJI]                  [EMOJI] [EMOJI]: [EMOJI]<10[EMOJI]")
    print("[EMOJI]")
    print("[EMOJI] 2. [EMOJI] [EMOJI] [EMOJI]: [EMOJI]([EMOJI])[EMOJI]([EMOJI])")
    print("[EMOJI]                    [EMOJI] [EMOJI]: 15:00[EMOJI]")
    print("[EMOJI]                    [EMOJI] [EMOJI]: [EMOJI]API[EMOJI]")
    print("[EMOJI]                    [EMOJI] [EMOJI]: [EMOJI](position_date/rm_date/mark/datetime)")
    print("[EMOJI]                    [EMOJI] [EMOJI]: [EMOJI]30[EMOJI]")
    print("[EMOJI]")
    print("[EMOJI] 3. [EMOJI] [EMOJI] RSI[EMOJI]: [EMOJI]EMA([EMOJI])/SMA[EMOJI]")
    print("                    [EMOJI] RSI[EMOJI]: [EMOJI]value[EMOJI]")
    print("                    [EMOJI] [EMOJI]: 10[EMOJI]30[EMOJI]RSI([EMOJI])")
    print("                    [EMOJI] [EMOJI]: [EMOJI]>10[EMOJI]>20%")
    print("                    [EMOJI] [EMOJI]: [EMOJI]>1[EMOJI]")
    print("                    [EMOJI] [EMOJI]: [EMOJI]")
    
    print("\n[CHART] [EMOJI]")
    print("[EMOJI] 1. [EMOJI] [EMOJI] [EMOJI]: EasyXT API")
    print("[EMOJI]                  [EMOJI] [EMOJI]1: qmt[EMOJI]")
    print("[EMOJI]                  [EMOJI] [EMOJI]2: qstock[EMOJI]")
    print("[EMOJI]                  [EMOJI] [EMOJI]3: akshare[EMOJI]")
    print("[EMOJI]")
    print("[EMOJI] 2. [EMOJI] [EMOJI] RSI[EMOJI]: [EMOJI]EMA([EMOJI])/SMA[EMOJI]")
    print("[EMOJI]                  [EMOJI] [EMOJI]: [EMOJI]30[EMOJI]")
    print("[EMOJI]                  [EMOJI] [EMOJI]: [EMOJI]")
    print("[EMOJI]")
    print("[EMOJI] 3. [EMOJI] [EMOJI] RSI[EMOJI]: [EMOJI]value[EMOJI]")
    print("                   [EMOJI] [EMOJI]: 10[EMOJI]30[EMOJI]RSI([EMOJI])")
    print("                   [EMOJI] [EMOJI]: [EMOJI]>10[EMOJI]>20%")
    
    print("\n[TARGET] [EMOJI]")
    print("[EMOJI] 1. [EMOJI] [EMOJI] [EMOJI]: [EMOJI]")
    print("[EMOJI]                  [EMOJI] [EMOJI]: [EMOJI]>[EMOJI]")
    print("[EMOJI]                  [EMOJI] RSI[EMOJI]: RSI[EMOJI](<30)[EMOJI]")
    print("[EMOJI]                  [EMOJI] [EMOJI]: 30[EMOJI]>1%")
    print("[EMOJI]                  [EMOJI] [EMOJI]: [EMOJI]")
    print("[EMOJI]")
    print("[EMOJI] 2. [EMOJI]([EMOJI]) [EMOJI] RSI[EMOJI]: RSI[EMOJI](<30)[EMOJI]")
    print("[EMOJI]                          [EMOJI] [EMOJI]: 30[EMOJI]>1%")
    print("[EMOJI]                          [EMOJI] [EMOJI]: [EMOJI]")
    print("[EMOJI]                          [EMOJI] [EMOJI]: 30[EMOJI]RSI>80[EMOJI]>2%")
    print("[EMOJI]")
    print("[EMOJI] 3. [EMOJI]([EMOJI]) [EMOJI] RSI[EMOJI]: RSI[EMOJI](>70)[EMOJI]")
    print("                          [EMOJI] [EMOJI]: [EMOJI]<[EMOJI]")
    print("                          [EMOJI] [EMOJI]: 30[EMOJI]RSI>80[EMOJI]>2%")
    
    print("\n[EMOJI] [EMOJI]")
    print("[EMOJI] 1. [EMOJI] [EMOJI] [EMOJI](schedule): [EMOJI]+[EMOJI]")
    print("[EMOJI]                  [EMOJI] [EMOJI](9:38): [EMOJI]+[EMOJI]")
    print("[EMOJI]                  [EMOJI] [EMOJI](5[EMOJI]): [EMOJI]+[EMOJI]+[EMOJI]")
    print("[EMOJI]                  [EMOJI] [EMOJI](14:57): [EMOJI]+[EMOJI]")
    print("[EMOJI]                  [EMOJI] [EMOJI](after_close): [EMOJI]+[EMOJI]+[EMOJI]")
    print("[EMOJI]")
    print("[EMOJI] 2. [EMOJI] [EMOJI] [EMOJI]: [EMOJI](order_percent)")
    print("[EMOJI]                  [EMOJI] [EMOJI]: [EMOJI]")
    print("[EMOJI]                  [EMOJI] [EMOJI]: 30[EMOJI]")
    print("[EMOJI]                  [EMOJI] [EMOJI]: [EMOJI]set_order()[EMOJI]/[EMOJI]/[EMOJI]")
    print("[EMOJI]")
    print("[EMOJI] 3. [EMOJI] [EMOJI] [EMOJI]: [EMOJI]")
    print("                   [EMOJI] [EMOJI]: [EMOJI]")
    print("                   [EMOJI] [EMOJI]: [EMOJI]")
    
    print("\n[EMOJI] [EMOJI]")
    print("[EMOJI] 1. [EMOJI] [EMOJI] [EMOJI]: [EMOJI]10[EMOJI](0.5-1.0)")
    print("[EMOJI]                  [EMOJI] [EMOJI]: [EMOJI]([EMOJI]↑)[EMOJI]([EMOJI]↓)")
    print("[EMOJI]                  [EMOJI] [EMOJI]: [EMOJI](1-2%)×[EMOJI]")
    print("[EMOJI]                  [EMOJI] [EMOJI]: [EMOJI]ATR[EMOJI]15[EMOJI]")
    print("[EMOJI]                  [EMOJI] [EMOJI]: [EMOJI]1[EMOJI]")
    print("[EMOJI]")
    print("[EMOJI] 2. [EMOJI] [EMOJI] [EMOJI]: [EMOJI]")
    print("[EMOJI]                  [EMOJI] [EMOJI]: [EMOJI]")
    print("[EMOJI]                  [EMOJI] [EMOJI]: [EMOJI]")
    print("[EMOJI]")
    print("[EMOJI] 3. [EMOJI] [EMOJI] [EMOJI]: [EMOJI]>2%[EMOJI]")
    print("                   [EMOJI] RSI[EMOJI]: 30[EMOJI]RSI>80[EMOJI]>2%[EMOJI]")
    print("                   [EMOJI] [EMOJI]: [EMOJI]15[EMOJI]")
    
    print("\n[CHART] [EMOJI]")
    print("[EMOJI] 1. [EMOJI] [EMOJI] handle_data: [EMOJI]")
    print("[EMOJI]                  [EMOJI] [EMOJI]: [EMOJI]")
    print("[EMOJI]                  [EMOJI] [EMOJI]: [EMOJI]")
    print("[EMOJI]                  [EMOJI] [EMOJI]: [EMOJI]CPU[EMOJI]")
    print("[EMOJI]")
    print("[EMOJI] 2. [EMOJI] [EMOJI] [EMOJI]: [EMOJI]")
    print("[EMOJI]                  [EMOJI] [EMOJI]: [EMOJI]")
    print("[EMOJI]                  [EMOJI] [EMOJI]: [EMOJI]")
    print("[EMOJI]")
    print("[EMOJI] 3. [EMOJI] [EMOJI] [EMOJI]: API[EMOJI]")
    print("                   [EMOJI] [EMOJI]: [EMOJI]")
    print("                   [EMOJI] [EMOJI]: [EMOJI]")
    print("                   [EMOJI] [EMOJI]: [EMOJI]")

class LiveTradingStrategy:
    """
    [EMOJI] - [EMOJI]
    
    [EMOJI]EasyXT[EMOJI]
    [EMOJI]
    """
    
    def __init__(self, account_id, stock_code='600415.XSHG', initial_capital=200000):
        """
        [EMOJI]
        
        Args:
            account_id: [EMOJI]ID
            stock_code: [EMOJI] ([EMOJI]-[EMOJI])
            initial_capital: [EMOJI] (20[EMOJI])
        """
        self.account_id = account_id
        self.stock_code = stock_code
        self.initial_capital = initial_capital
        
        # [EMOJI]
        self.short_ema_period = 12      # [EMOJI]EMA[EMOJI]
        self.long_ema_period = 26       # [EMOJI]EMA[EMOJI]
        self.rsi_period = 14            # RSI[EMOJI]
        self.rsi_oversold = 30          # RSI[EMOJI]
        self.rsi_overbought = 70        # RSI[EMOJI]
        
        # [EMOJI]
        self.stop_loss_pct = 0.02       # [EMOJI] 2%
        self.take_profit_pct = 0.02     # [EMOJI] 2% (30[EMOJI]RSI>80[EMOJI]>2%)
        self.max_position_pct = 0.90    # [EMOJI] 90%
        self.min_volume_ratio = 1.2     # [EMOJI] (>10[EMOJI]20%)
        
        # [EMOJI] (5[EMOJI])
        self.trading_times = [
            '09:38',  # [EMOJI]
            '10:30',  # [EMOJI]1
            '11:00',  # [EMOJI]2
            '13:15',  # [EMOJI]3
            '14:00',  # [EMOJI]4
            '14:45',  # [EMOJI]5
            '14:57'   # [EMOJI]
        ]
        
        # [EMOJI]
        self.commission_rate = 0.0003   # [EMOJI] 0.03%
        self.stamp_tax_rate = 0.001     # [EMOJI] 0.1%
        self.slippage_rate = 0.0005     # [EMOJI] 0.05%
        
        # [EMOJI]
        self.position = 0               # [EMOJI]
        self.entry_price = 0            # [EMOJI]
        self.stop_loss_price = 0        # [EMOJI]
        self.daily_trades = 0           # [EMOJI]
        self.last_trade_date = None     # [EMOJI]
        self.position_date = None       # [EMOJI]
        
        # [EMOJI]
        self.price_history = []         # [EMOJI]
        self.volume_history = []        # [EMOJI]
        self.indicators = {}            # [EMOJI]
        self.order_history = []         # [EMOJI]
        
        # [EMOJI]
        self.performance_metrics = {
            'total_trades': 0,
            'win_trades': 0,
            'lose_trades': 0,
            'total_pnl': 0.0,
            'max_drawdown': 0.0,
            'current_drawdown': 0.0
        }
        
        print(f"[OK] [EMOJI]")
        print(f"  [TARGET] [EMOJI]: {self.stock_code} ([EMOJI]-[EMOJI])")
        print(f"  [MONEY] [EMOJI]: {self.initial_capital:,}[EMOJI]")
        print(f"  [CHART] [EMOJI]: [EMOJI]")
        print(f"  [TOOL] [EMOJI]: EasyXT[EMOJI]")
    
    def get_live_market_data(self):
        """
        [EMOJI] - [EMOJI]
        [EMOJI]: EasyXT API → qmt[EMOJI] → qstock → akshare
        """
        try:
            print(f"[CHART] [EMOJI]...")
            print(f"  [TARGET] [EMOJI]: {self.stock_code}")
            print(f"  [EMOJI] [EMOJI]: EasyXT API → qmt[EMOJI] → qstock → akshare")
            
            # [EMOJI]1[EMOJI]EasyXT[EMOJI]
            try:
                xt = EasyXT()
                
                # [EMOJI]
                if xt.init_data():
                    # [EMOJI]
                    if self.stock_code.endswith('.XSHG'):
                        xt_code = self.stock_code.replace('.XSHG', '.SH')
                    elif self.stock_code.endswith('.XSHE'):
                        xt_code = self.stock_code.replace('.XSHE', '.SZ')
                    else:
                        xt_code = self.stock_code
                    
                    # [EMOJI]
                    current_data = xt.data.get_current_price([xt_code])
                    
                    if current_data is not None and not current_data.empty:
                        data = current_data.iloc[0]
                        market_data = {
                            'datetime': datetime.now(),
                            'open': float(data.get('open', 0)),
                            'high': float(data.get('high', 0)),
                            'low': float(data.get('low', 0)),
                            'close': float(data.get('close', data.get('last_price', 0))),
                            'volume': int(data.get('volume', 0)),
                            'amount': float(data.get('amount', 0))
                        }
                        
                        print(f"[OK] [EMOJI]EasyXT[EMOJI]")
                        print(f"  [MONEY] [EMOJI]: {market_data['close']:.2f}[EMOJI]")
                        print(f"  [CHART] [EMOJI]: {market_data['volume']:,}[EMOJI]")
                        return market_data
                else:
                    print("[!] EasyXT[EMOJI]")
                    
            except Exception as e:
                print(f"[!] EasyXT[EMOJI]: {e}")
            
            # [EMOJI]2[EMOJI]qmt[EMOJI]
            try:
                print("[R] [EMOJI]qmt[EMOJI]...")
                # [EMOJI]qmt[EMOJI]
                # [EMOJI]qmt[EMOJI]
                raise Exception("qmt[EMOJI]")
                
            except Exception as e:
                print(f"[!] qmt[EMOJI]: {e}")
            
            # [EMOJI]3[EMOJI]qstock[EMOJI]
            try:
                import qstock as qs
                
                print("[R] [EMOJI]qstock[EMOJI]...")
                
                # [EMOJI]
                if self.stock_code.endswith('.XSHG'):
                    qs_code = self.stock_code.replace('.XSHG', '')
                elif self.stock_code.endswith('.XSHE'):
                    qs_code = self.stock_code.replace('.XSHE', '')
                else:
                    qs_code = self.stock_code.split('.')[0]
                
                # [EMOJI]qstock[EMOJI] ([EMOJI]API[EMOJI])
                try:
                    # qstock[EMOJI]API[EMOJI]
                    current_data = qs.get_data(qs_code, start='', end='')
                    
                    if current_data is not None and not current_data.empty:
                        # [EMOJI]
                        latest_data = current_data.iloc[-1]
                        market_data = {
                            'datetime': datetime.now(),
                            'open': float(latest_data.get('open', latest_data.get('[EMOJI]', 0))),
                            'high': float(latest_data.get('high', latest_data.get('[EMOJI]', 0))),
                            'low': float(latest_data.get('low', latest_data.get('[EMOJI]', 0))),
                            'close': float(latest_data.get('close', latest_data.get('[EMOJI]', 0))),
                            'volume': int(latest_data.get('volume', latest_data.get('[EMOJI]', 0))),
                            'amount': float(latest_data.get('amount', latest_data.get('[EMOJI]', 0)))
                        }
                        
                        print(f"[OK] [EMOJI]qstock[EMOJI]")
                        print(f"  [MONEY] [EMOJI]: {market_data['close']:.2f}[EMOJI]")
                        return market_data
                except Exception as qstock_error:
                    print(f"[!] qstock API[EMOJI]: {qstock_error}")
                    # [EMOJI]qstock[EMOJI]
                    try:
                        # [EMOJI]
                        realtime_data = qs.realtime(qs_code)
                        if realtime_data is not None:
                            market_data = {
                                'datetime': datetime.now(),
                                'open': float(realtime_data.get('open', 8.50)),
                                'high': float(realtime_data.get('high', 8.60)),
                                'low': float(realtime_data.get('low', 8.40)),
                                'close': float(realtime_data.get('price', 8.50)),
                                'volume': int(realtime_data.get('volume', 1000000)),
                                'amount': float(realtime_data.get('amount', 8500000))
                            }
                            
                            print(f"[OK] [EMOJI]qstock[EMOJI]")
                            print(f"  [MONEY] [EMOJI]: {market_data['close']:.2f}[EMOJI]")
                            return market_data
                    except Exception as realtime_error:
                        print(f"[!] qstock[EMOJI]: {realtime_error}")
                    
            except ImportError:
                print("[!] qstock[EMOJI]")
            except Exception as e:
                print(f"[!] qstock[EMOJI]: {e}")
            
            # [EMOJI]4[EMOJI]akshare[EMOJI]
            try:
                import akshare as ak
                
                print("[R] [EMOJI]akshare[EMOJI]...")
                
                # [EMOJI]
                if self.stock_code.endswith('.XSHG'):
                    ak_code = self.stock_code.replace('.XSHG', '')
                elif self.stock_code.endswith('.XSHE'):
                    ak_code = self.stock_code.replace('.XSHE', '')
                else:
                    ak_code = self.stock_code.split('.')[0]
                
                # [EMOJI]
                current_data = ak.stock_zh_a_spot_em()
                stock_data = current_data[current_data['[EMOJI]'] == ak_code]
                
                if len(stock_data) > 0:
                    row = stock_data.iloc[0]
                    market_data = {
                        'datetime': datetime.now(),
                        'open': float(row['[EMOJI]']),
                        'high': float(row['[EMOJI]']),
                        'low': float(row['[EMOJI]']),
                        'close': float(row['[EMOJI]']),
                        'volume': int(row['[EMOJI]']),
                        'amount': float(row['[EMOJI]'])
                    }
                    
                    print(f"[OK] [EMOJI]akshare[EMOJI]")
                    print(f"  [MONEY] [EMOJI]: {market_data['close']:.2f}[EMOJI]")
                    return market_data
                    
            except ImportError:
                print("[!] akshare[EMOJI]")
            except Exception as e:
                print(f"[!] akshare[EMOJI]: {e}")
            
            # [EMOJI]
            print("[R] [EMOJI]...")
            print("[TIP] [EMOJI]")
            return self.generate_mock_realtime_data()
            
        except Exception as e:
            print(f"[X] [EMOJI]: {e}")
            print("[R] [EMOJI]...")
            return self.generate_mock_realtime_data()
    
    def generate_mock_realtime_data(self):
        """[EMOJI]"""
        import random
        
        # [EMOJI]
        base_price = 8.50
        volatility = 0.02  # 2%[EMOJI]
        
        # [EMOJI]
        current_price = base_price * (1 + random.gauss(0, volatility))
        daily_range = current_price * volatility
        
        market_data = {
            'datetime': datetime.now(),
            'open': round(current_price * random.uniform(0.98, 1.02), 2),
            'high': round(current_price + daily_range * random.uniform(0.3, 0.8), 2),
            'low': round(current_price - daily_range * random.uniform(0.3, 0.8), 2),
            'close': round(current_price, 2),
            'volume': random.randint(800000, 1500000),
            'amount': round(current_price * random.randint(800000, 1500000), 2)
        }
        
        # [EMOJI]OHLC[EMOJI]
        market_data['high'] = max(market_data['high'], market_data['open'], market_data['close'])
        market_data['low'] = min(market_data['low'], market_data['open'], market_data['close'])
        
        print(f"[CHART] [EMOJI]")
        print(f"  [MONEY] [EMOJI]: {market_data['close']:.2f}[EMOJI]")
        print(f"  [CHART] [EMOJI]: {market_data['volume']:,}[EMOJI]")
        
        return market_data
    
    def calculate_technical_indicators(self, market_data):
        """[EMOJI]"""
        # [EMOJI]
        self.price_history.append(market_data['close'])
        self.volume_history.append(market_data['volume'])
        
        # [EMOJI]
        max_history = max(self.long_ema_period, self.rsi_period) + 10
        if len(self.price_history) > max_history:
            self.price_history = self.price_history[-max_history:]
            self.volume_history = self.volume_history[-max_history:]
        
        # [EMOJI]EMA
        if len(self.price_history) >= self.short_ema_period:
            self.indicators['short_ema'] = self.calculate_ema(self.price_history, self.short_ema_period)
        
        if len(self.price_history) >= self.long_ema_period:
            self.indicators['long_ema'] = self.calculate_ema(self.price_history, self.long_ema_period)
        
        # [EMOJI]RSI
        if len(self.price_history) >= self.rsi_period + 1:
            self.indicators['rsi'] = self.calculate_rsi(self.price_history, self.rsi_period)
        
        # [EMOJI]
        if len(self.volume_history) >= 10:
            self.indicators['volume_ratio'] = self.calculate_volume_ratio(self.volume_history)
        
        # [EMOJI]MACD
        if 'short_ema' in self.indicators and 'long_ema' in self.indicators:
            self.indicators['macd'] = self.indicators['short_ema'] - self.indicators['long_ema']
        
        return self.indicators
    
    def calculate_ema(self, prices, period):
        """[EMOJI]"""
        if len(prices) < period:
            return None
        
        multiplier = 2 / (period + 1)
        ema = prices[0]
        
        for price in prices[1:]:
            ema = (price * multiplier) + (ema * (1 - multiplier))
        
        return ema
    
    def calculate_rsi(self, prices, period=14):
        """[EMOJI]RSI[EMOJI]"""
        if len(prices) < period + 1:
            return None
        
        deltas = [prices[i] - prices[i-1] for i in range(1, len(prices))]
        gains = [max(d, 0) for d in deltas]
        losses = [abs(min(d, 0)) for d in deltas]
        
        avg_gain = sum(gains[-period:]) / period
        avg_loss = sum(losses[-period:]) / period
        
        if avg_loss == 0:
            return 100
        
        rs = avg_gain / avg_loss
        rsi = 100 - (100 / (1 + rs))
        return rsi
    
    def calculate_volume_ratio(self, volumes, period=10):
        """[EMOJI]"""
        if len(volumes) < period + 1:
            return 1.0
        
        current_volume = volumes[-1]
        avg_volume = sum(volumes[-period-1:-1]) / period
        
        if avg_volume == 0:
            return 1.0
        
        return current_volume / avg_volume
    
    def check_trading_time(self, current_time):
        """[EMOJI] ([EMOJI])"""
        current_time_str = current_time.strftime('%H:%M')
        
        # [EMOJI] - [EMOJI]
        return True, current_time_str
    
    def generate_trading_signals(self, market_data):
        """[EMOJI]"""
        current_price = market_data['close']
        current_time = market_data['datetime']
        
        # [EMOJI]
        is_trading_time, trading_point = self.check_trading_time(current_time)
        if not is_trading_time:
            return {'buy': False, 'sell': False, 'reason': '[EMOJI]'}
        
        # [EMOJI]
        if not all(key in self.indicators for key in ['short_ema', 'long_ema', 'rsi', 'volume_ratio']):
            return {'buy': False, 'sell': False, 'reason': '[EMOJI]'}
        
        signals = {'buy': False, 'sell': False, 'reason': '', 'trading_point': trading_point}
        
        # [EMOJI] ([EMOJI])
        if self.position == 0:  # [EMOJI]
            buy_conditions = []
            
            # 1. RSI[EMOJI](<30)[EMOJI]
            rsi_oversold = self.indicators['rsi'] < self.rsi_oversold
            buy_conditions.append(('RSI[EMOJI]', rsi_oversold))
            
            # 2. [EMOJI] ([EMOJI])
            ema_bullish = self.indicators['short_ema'] > self.indicators['long_ema']
            buy_conditions.append(('EMA[EMOJI]', ema_bullish))
            
            # 3. [EMOJI]>10[EMOJI]20%
            volume_sufficient = self.indicators['volume_ratio'] > self.min_volume_ratio
            buy_conditions.append(('[EMOJI]', volume_sufficient))
            
            # 4. MACD[EMOJI]
            macd_positive = self.indicators.get('macd', 0) > 0
            buy_conditions.append(('MACD[EMOJI]', macd_positive))
            
            # [EMOJI]
            satisfied_conditions = [name for name, condition in buy_conditions if condition]
            
            if len(satisfied_conditions) >= 3:  # [EMOJI]3[EMOJI]
                signals['buy'] = True
                signals['reason'] = f"[EMOJI]: {', '.join(satisfied_conditions)}"
        
        # [EMOJI] ([EMOJI])
        if self.position > 0:  # [EMOJI]
            sell_conditions = []
            
            # 1. RSI[EMOJI](>70)[EMOJI]
            rsi_overbought = self.indicators['rsi'] > self.rsi_overbought
            sell_conditions.append(('RSI[EMOJI]', rsi_overbought))
            
            # 2. [EMOJI] ([EMOJI]<[EMOJI])
            if self.stop_loss_price > 0:
                stop_loss_triggered = current_price <= self.stop_loss_price
                sell_conditions.append(('[EMOJI]', stop_loss_triggered))
            
            # 3. [EMOJI] (30[EMOJI]RSI>80[EMOJI]>2%)
            if self.entry_price > 0:
                price_gain = (current_price - self.entry_price) / self.entry_price
                take_profit_triggered = (self.indicators['rsi'] > 80 and price_gain > self.take_profit_pct)
                sell_conditions.append(('[EMOJI]', take_profit_triggered))
            
            # 4. [EMOJI] ([EMOJI])
            ema_bearish = self.indicators['short_ema'] < self.indicators['long_ema']
            sell_conditions.append(('EMA[EMOJI]', ema_bearish))
            
            # [EMOJI] ([EMOJI])
            satisfied_conditions = [name for name, condition in sell_conditions if condition]
            
            if len(satisfied_conditions) >= 1:
                signals['sell'] = True
                signals['reason'] = f"[EMOJI]: {', '.join(satisfied_conditions)}"
        
        return signals
    
    def execute_trade(self, signal, market_data):
        """[EMOJI]"""
        current_price = market_data['close']
        current_time = market_data['datetime']
        
        try:
            if signal['buy'] and self.position == 0:
                # [EMOJI] ([EMOJI])
                available_capital = self.initial_capital * self.max_position_pct
                
                # [EMOJI]
                total_cost_rate = self.commission_rate + self.slippage_rate
                effective_capital = available_capital / (1 + total_cost_rate)
                
                shares = int(effective_capital / current_price / 100) * 100  # [EMOJI]
                
                if shares > 0:
                    # [EMOJI]
                    self.position = shares
                    self.entry_price = current_price
                    self.stop_loss_price = current_price * (1 - self.stop_loss_pct)
                    self.position_date = current_time.date()
                    self.daily_trades += 1
                    
                    # [EMOJI]
                    order = {
                        'datetime': current_time,
                        'type': 'BUY',
                        'shares': shares,
                        'price': current_price,
                        'amount': shares * current_price,
                        'reason': signal['reason'],
                        'trading_point': signal.get('trading_point', '')
                    }
                    self.order_history.append(order)
                    
                    print(f"[OK] [EMOJI]")
                    print(f"  [CHART] [EMOJI]: {shares:,}[EMOJI]")
                    print(f"  [MONEY] [EMOJI]: {current_price:.2f}[EMOJI]")
                    print(f"  [EMOJI] [EMOJI]: {shares * current_price:,.2f}[EMOJI]")
                    print(f"  [EMOJI] [EMOJI]: {self.stop_loss_price:.2f}[EMOJI]")
                    print(f"  [TARGET] [EMOJI]: {signal['reason']}")
                    print(f"  [TIME] [EMOJI]: {signal.get('trading_point', '')}")
                    
                    return True, f"[EMOJI]{shares:,}[EMOJI]@{current_price:.2f}[EMOJI]"
            
            elif signal['sell'] and self.position > 0:
                # [EMOJI]
                shares = self.position
                
                # [EMOJI]
                pnl = (current_price - self.entry_price) * shares
                pnl_pct = (current_price - self.entry_price) / self.entry_price * 100
                
                # [EMOJI]
                total_amount = shares * current_price
                total_cost = total_amount * (self.commission_rate + self.stamp_tax_rate + self.slippage_rate)
                net_pnl = pnl - total_cost
                
                # [EMOJI]
                self.position = 0
                self.entry_price = 0
                self.stop_loss_price = 0
                self.position_date = None
                self.daily_trades += 1
                
                # [EMOJI]
                self.performance_metrics['total_trades'] += 1
                self.performance_metrics['total_pnl'] += net_pnl
                
                if net_pnl > 0:
                    self.performance_metrics['win_trades'] += 1
                else:
                    self.performance_metrics['lose_trades'] += 1
                
                # [EMOJI]
                order = {
                    'datetime': current_time,
                    'type': 'SELL',
                    'shares': shares,
                    'price': current_price,
                    'amount': total_amount,
                    'pnl': net_pnl,
                    'pnl_pct': pnl_pct,
                    'reason': signal['reason'],
                    'trading_point': signal.get('trading_point', '')
                }
                self.order_history.append(order)
                
                print(f"[OK] [EMOJI]")
                print(f"  [CHART] [EMOJI]: {shares:,}[EMOJI]")
                print(f"  [MONEY] [EMOJI]: {current_price:.2f}[EMOJI]")
                print(f"  [EMOJI] [EMOJI]: {total_amount:,.2f}[EMOJI]")
                print(f"  [MONEY] [EMOJI]: {net_pnl:+,.2f}[EMOJI] ({pnl_pct:+.2f}%)")
                print(f"  [EMOJI] [EMOJI]: {total_cost:.2f}[EMOJI]")
                print(f"  [TARGET] [EMOJI]: {signal['reason']}")
                print(f"  [TIME] [EMOJI]: {signal.get('trading_point', '')}")
                
                return True, f"[EMOJI]{shares:,}[EMOJI]@{current_price:.2f}[EMOJI]{net_pnl:+,.2f}[EMOJI]"
        
        except Exception as e:
            print(f"[X] [EMOJI]: {e}")
            return False, str(e)
        
        return False, "[EMOJI]"
    
    def monitor_position(self, market_data):
        """[EMOJI]"""
        if self.position == 0:
            return
        
        current_price = market_data['close']
        current_time = market_data['datetime']
        
        # [EMOJI]
        unrealized_pnl = (current_price - self.entry_price) * self.position
        unrealized_pnl_pct = (current_price - self.entry_price) / self.entry_price * 100
        
        # [EMOJI]
        if self.position_date:
            holding_days = (current_time.date() - self.position_date).days
        else:
            holding_days = 0
        
        print(f"\n[CHART] [EMOJI]:")
        print(f"  [TARGET] [EMOJI]: {self.stock_code}")
        print(f"  [CHART] [EMOJI]: {self.position:,}[EMOJI]")
        print(f"  [MONEY] [EMOJI]: {self.entry_price:.2f}[EMOJI]")
        print(f"  [EMOJI] [EMOJI]: {current_price:.2f}[EMOJI]")
        print(f"  [EMOJI] [EMOJI]: {self.stop_loss_price:.2f}[EMOJI]")
        print(f"  [MONEY] [EMOJI]: {unrealized_pnl:+,.2f}[EMOJI] ({unrealized_pnl_pct:+.2f}%)")
        print(f"  [EMOJI] [EMOJI]: {holding_days}[EMOJI]")
        
        # [EMOJI]
        if current_price <= self.stop_loss_price:
            print(f"  [!] [EMOJI]: [EMOJI]!")
        
        if unrealized_pnl_pct < -1.5:
            print(f"  [!] [EMOJI]: [EMOJI]1.5%!")
        
        if holding_days > 5:
            print(f"  [!] [EMOJI]: [EMOJI]!")
    
    def generate_performance_report(self):
        """[EMOJI]"""
        print(f"\n[CHART] [EMOJI]")
        print(f"=" * 50)
        
        metrics = self.performance_metrics
        
        print(f"[UP] [EMOJI]:")
        print(f"  [R] [EMOJI]: {metrics['total_trades']}")
        print(f"  [OK] [EMOJI]: {metrics['win_trades']}")
        print(f"  [X] [EMOJI]: {metrics['lose_trades']}")
        
        if metrics['total_trades'] > 0:
            win_rate = metrics['win_trades'] / metrics['total_trades'] * 100
            print(f"  [TARGET] [EMOJI]: {win_rate:.1f}%")
        
        print(f"\n[MONEY] [EMOJI]:")
        print(f"  [EMOJI] [EMOJI]: {metrics['total_pnl']:+,.2f}[EMOJI]")
        
        if self.initial_capital > 0:
            return_rate = metrics['total_pnl'] / self.initial_capital * 100
            print(f"  [CHART] [EMOJI]: {return_rate:+.2f}%")
        
        print(f"\n[EMOJI] [EMOJI]:")
        for order in self.order_history[-5:]:
            if order['type'] == 'BUY':
                print(f"  [UP] {order['datetime'].strftime('%Y-%m-%d %H:%M')} [EMOJI] {order['shares']:,}[EMOJI]@{order['price']:.2f}[EMOJI]")
            else:
                print(f"  [EMOJI] {order['datetime'].strftime('%Y-%m-%d %H:%M')} [EMOJI] {order['shares']:,}[EMOJI]@{order['price']:.2f}[EMOJI] [EMOJI]{order['pnl']:+,.2f}[EMOJI]")
    
    def run_live_strategy_demo(self, demo_minutes=30):
        """[EMOJI]"""
        print(f"\n[LAUNCH] [EMOJI] ([EMOJI]{demo_minutes}[EMOJI]) - [EMOJI]")
        print(f"=" * 60)
        
        start_time = datetime.now()
        
        for minute in range(demo_minutes):
            current_time = start_time + timedelta(minutes=minute)
            
            # [EMOJI] - [EMOJI]
            
            print(f"\n[TIME] [EMOJI]: {current_time.strftime('%Y-%m-%d %H:%M')}")
            
            # [EMOJI]
            market_data = self.get_live_market_data()
            market_data['datetime'] = current_time  # [EMOJI]
            
            # [EMOJI]
            indicators = self.calculate_technical_indicators(market_data)
            
            # [EMOJI]
            if indicators:
                print(f"[CHART] [EMOJI]: EMA({indicators.get('short_ema', 0):.2f}/{indicators.get('long_ema', 0):.2f}) "
                      f"RSI({indicators.get('rsi', 0):.1f}) [EMOJI]({indicators.get('volume_ratio', 0):.2f})")
            
            # [EMOJI]
            signals = self.generate_trading_signals(market_data)
            
            # [EMOJI]
            if signals['buy'] or signals['sell']:
                success, result = self.execute_trade(signals, market_data)
                if success:
                    print(f"[TARGET] [EMOJI]: {result}")
            else:
                print(f"[CHART] [EMOJI]: {signals['reason']}")
            
            # [EMOJI]
            if self.position > 0:
                self.monitor_position(market_data)
            
            # [EMOJI]10[EMOJI]
            if minute > 0 and minute % 10 == 0:
                self.generate_performance_report()
            
            # [EMOJI]
            time.sleep(0.1)
        
        # [EMOJI]
        print(f"\n[EMOJI] [EMOJI]!")
        self.generate_performance_report()

def demo_live_strategy_development():
    """[EMOJI]"""
    print("\n" + "=" * 80)
    print("[LAUNCH] [EMOJI]")
    print("=" * 80)
    print("[EMOJI]")
    print("[TARGET] [EMOJI]")
    print("[CHART] [EMOJI]EasyXT API → qmt[EMOJI] → qstock → akshare")
    print("[TOOL] [EMOJI]EasyXT[EMOJI]")
    
    wait_for_user_input("[EMOJI]")
    
    # [EMOJI]
    display_live_strategy_flowchart()
    
    wait_for_user_input("[EMOJI]...")
    
    # [EMOJI]
    print_section_header(1, "[EMOJI]", "[EMOJI]")
    
    print("[EMOJI] [EMOJI]")
    print("  [TARGET] [EMOJI]600415.XSHG ([EMOJI]-[EMOJI])")
    print("  [MONEY] [EMOJI]20[EMOJI]+RSI[EMOJI]+[EMOJI]")
    print("  [EMOJI] [EMOJI]EasyXT[EMOJI]")
    print("  [CHART] [EMOJI](2)[EMOJI]")
    print("  [TIME] [EMOJI](2%)[EMOJI]+[EMOJI]")
    print("  [UP] [EMOJI]([EMOJI])")
    
    print("\n[TOOL] [EMOJI]")
    print("  [CHART] [EMOJI]EMA(EMA/SMA)[EMOJI]RSI(EMA/SMA)")
    print("  [UP] RSI[EMOJI]RSI[EMOJI]30[EMOJI]70")
    print("  [TARGET] [EMOJI]2%([EMOJI])")
    print("  [MONEY] [EMOJI]90%([EMOJI])")
    print("  [EMOJI] [EMOJI]0.03%[EMOJI]0.1%[EMOJI]0.05%")
    
    wait_for_user_input("[EMOJI]...")
    
    # [EMOJI]
    print_section_header(2, "[EMOJI]", "[EMOJI]")
    
    print("[EMOJI] 1. [EMOJI]")
    print("  [CHART] EMA[EMOJI]12[EMOJI]26[EMOJI]([EMOJI])")
    print("  [UP] [EMOJI]>10[EMOJI]20%")
    print("  [TIME] [EMOJI]10:30/11:00/13:15/14:00/14:45(5[EMOJI])")
    print("  [R] [EMOJI]10[EMOJI]")
    print("  [CHART] [EMOJI]<10[EMOJI]")
    
    print("\n[MONEY] 2. [EMOJI]")
    print("  [TARGET] [EMOJI]([EMOJI])[EMOJI]([EMOJI])")
    print("  [EMOJI] [EMOJI]15:00[EMOJI]")
    print("  [CHART] [EMOJI]API[EMOJI]")
    print("  [R] [EMOJI](position_date/rm_date/mark/datetime)")
    print("  [UP] [EMOJI]30[EMOJI]")
    
    print("\n[TIME] 3. [EMOJI]")
    print("  [EMOJI] RSI[EMOJI]EMA([EMOJI])/SMA[EMOJI]")
    print("  [CHART] RSI[EMOJI]value[EMOJI]")
    print("  [R] [EMOJI]10[EMOJI]30[EMOJI]RSI([EMOJI])")
    print("  [UP] [EMOJI]>10[EMOJI]>20%")
    print("  [!] [EMOJI]>1[EMOJI]")
    print("  [TARGET] [EMOJI]")
    
    wait_for_user_input("[EMOJI]...")
    
    # [EMOJI]
    print_section_header(3, "[EMOJI]", "[EMOJI]")
    
    strategy = LiveTradingStrategy(
        account_id="LIVE_DEMO",
        stock_code="600415.XSHG",
        initial_capital=200000
    )
    
    wait_for_user_input("[EMOJI]...")
    
    # [EMOJI]
    print_section_header(4, "[EMOJI]", "[EMOJI]")
    
    strategy.run_live_strategy_demo(demo_minutes=20)
    
    wait_for_user_input("[EMOJI]...")
    
    # [EMOJI]
    print_section_header(5, "[EMOJI]", "[EMOJI]")
    
    print("[COURSE] [EMOJI]")
    print("=" * 50)
    
    print("[OK] 1. [EMOJI]")
    print("  -  [EMOJI]")
    print("  -  [EMOJI]")
    print("  -  [EMOJI]")
    print("  -  [EMOJI]")
    
    print("\n[OK] 2. [EMOJI]")
    print("  -  [EMOJI]")
    print("  -  [EMOJI]")
    print("  -  [EMOJI]")
    print("  -  [EMOJI]")
    
    print("\n[OK] 3. [EMOJI]")
    print("  -  [EMOJI]")
    print("  -  [EMOJI]")
    print("  -  [EMOJI]")
    print("  -  [EMOJI]")
    
    print("\n[OK] 4. [EMOJI]")
    print("  -  [EMOJI]")
    print("  -  [EMOJI]")
    print("  -  [EMOJI]")
    print("  -  [EMOJI]")
    
    print("\n[OK] 5. [EMOJI]")
    print("  -  [EMOJI]")
    print("  -  [EMOJI]")
    print("  -  [EMOJI]")
    print("  -  [EMOJI]")
    
    print("\n[LAUNCH] [EMOJI]")
    print("=" * 50)
    print("  -  [CHART] [EMOJI]")
    print("  -  [TOOL] [EMOJI]")
    print("  -  [MONEY] [EMOJI]")
    print("  -  [UP] [EMOJI]")
    print("  -  [EMOJI] [EMOJI]")
    print("  -  [EMOJI] [EMOJI]")
    
    return strategy

def main():
    """[EMOJI] - [EMOJI]"""
    print("[COURSE] [EMOJI]")
    print("[BOOK] [EMOJI]")
    print("[TIP] [EMOJI] → [EMOJI] → [EMOJI] → [EMOJI] → [EMOJI] → [EMOJI] → [EMOJI]")
    
    print("\n[TARGET] [EMOJI]")
    print("  1[EMOJI] [EMOJI]")
    print("  2[EMOJI] [EMOJI]")
    print("  3[EMOJI] [EMOJI]")
    print("  4[EMOJI] [EMOJI]")
    print("  5[EMOJI] [EMOJI]")
    
    wait_for_user_input("[EMOJI]")
    
    # [EMOJI]
    strategy = demo_live_strategy_development()
    
    print("\n" + "=" * 80)
    print("[EMOJI] [EMOJI]")
    print("[BOOK] [EMOJI]")
    print("[LAUNCH] [EMOJI]")
    print("[TIP] [EMOJI]")
    print("[TARGET] [EMOJI]")
    print("=" * 80)
    
    return strategy

if __name__ == "__main__":
    main()