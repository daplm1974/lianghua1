"""
[EMOJI] - [EMOJI]
[EMOJI]

[EMOJI]
1. qstock[EMOJI] ([EMOJI])
2. [EMOJI]
3. [EMOJI]
4. EasyXT[EMOJI] ([EMOJI])
5. [EMOJI]
6. [EMOJI]
7. [EMOJI]

[EMOJI]quant
[EMOJI]2025-01-11
[EMOJI]
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import os
import sys
from datetime import datetime, timedelta
import warnings
import time
import requests
warnings.filterwarnings('ignore')

# [EMOJI]
REQUIRE_REAL_DATA = True
REQUIRE_REAL_TRADING = True

# [EMOJI]qstock - [EMOJI]
try:
    import qstock as qs
    QSTOCK_AVAILABLE = True
    print("[OK] qstock[EMOJI]")
except ImportError as e:
    if REQUIRE_REAL_DATA:
        print(f"[X] qstock[EMOJI]: {e}")
        print("[TIP] [EMOJI]: pip install qstock")
        print("[EMOJI] [EMOJI]")
        sys.exit(1)
    else:
        QSTOCK_AVAILABLE = False
        print(f"[X] qstock[EMOJI]: {e}")

# [EMOJI]easy_xt[EMOJI] - [EMOJI]
current_dir = os.path.dirname(os.path.abspath(__file__))
easy_xt_path = os.path.join(current_dir, '..', 'easy_xt')
if os.path.exists(easy_xt_path):
    sys.path.append(easy_xt_path)

try:
    from easy_xt import EasyXT
    EASY_XT_AVAILABLE = True
    print("[OK] easy_xt[EMOJI]")
except ImportError as e:
    try:
        # [EMOJI]
        sys.path.append(os.path.join(current_dir, '..'))
        from easy_xt.api import EasyXT
        EASY_XT_AVAILABLE = True
        print("[OK] easy_xt[EMOJI]")
    except ImportError as e2:
        if REQUIRE_REAL_TRADING:
            print(f"[X] easy_xt[EMOJI]: {e}")
            print("[EMOJI] [EMOJI]")
            sys.exit(1)
        else:
            EASY_XT_AVAILABLE = False
            print(f"[!] easy_xt[EMOJI]: {e}")

# [EMOJI]
plt.rcParams['font.sans-serif'] = ['SimHei']
plt.rcParams['axes.unicode_minus'] = False

# [EMOJI] - [EMOJI]
USERDATA_PATH = r'D:\[EMOJI]QMT[EMOJI]\userdata_mini'  # [EMOJI]
DEFAULT_ACCOUNT_ID = "39020958"  # [EMOJI]

class FixedRealTradingQStockStrategy:
    """[EMOJI]qstock[EMOJI]easy_xt[EMOJI] ([EMOJI])"""
    
    def __init__(self):
        """[EMOJI]"""
        self.data_dir = "data"
        self.log_dir = "logs"
        
        # [EMOJI]
        for dir_path in [self.data_dir, self.log_dir]:
            if not os.path.exists(dir_path):
                os.makedirs(dir_path)
        
        # [EMOJI] - [EMOJI]
        self.trader = None
        self.trade_initialized = False
        self.account_id = DEFAULT_ACCOUNT_ID
        
        if EASY_XT_AVAILABLE:
            self._init_trading_service()
        
        # [EMOJI]
        self.position = {}
        self.cash = 100000
        self.trade_log = []
        
        print("[LAUNCH] [EMOJI]QStock[EMOJI]")
    
    def _init_trading_service(self):
        """[EMOJI] - [EMOJI]"""
        try:
            print("[TOOL] [EMOJI]EasyXT[EMOJI]...")
            
            # 1. [EMOJI]EasyXT[EMOJI]
            self.trader = EasyXT()
            print("[OK] EasyXT[EMOJI]")
            
            # 2. [EMOJI]
            print("[CHART] [EMOJI]...")
            data_success = self.trader.init_data()
            if data_success:
                print("[OK] [EMOJI]")
            else:
                print("[!] [EMOJI]")
            
            # 3. [EMOJI]
            print(f"[EMOJI] [EMOJI]: {USERDATA_PATH}")
            trade_success = self.trader.init_trade(USERDATA_PATH, 'qstock_strategy_session')
            
            if trade_success:
                print("[OK] [EMOJI]")
                
                # 4. [EMOJI]
                print(f"[EMOJI] [EMOJI]: {self.account_id}")
                account_success = self.trader.add_account(self.account_id, 'STOCK')
                
                if account_success:
                    print("[OK] [EMOJI]")
                    self.trade_initialized = True
                    print("[EMOJI] EasyXT[EMOJI]")
                else:
                    print("[!] [EMOJI]")
                    self.trade_initialized = True
            else:
                print("[X] [EMOJI]")
                print("[TIP] [EMOJI]:")
                print(f"   1. [EMOJI]")
                print(f"   2. userdata[EMOJI]: {USERDATA_PATH}")
                print(f"   3. [EMOJI]ID[EMOJI]: {self.account_id}")
                
                if REQUIRE_REAL_TRADING:
                    print("[EMOJI] [EMOJI]")
                    sys.exit(1)
                
        except Exception as e:
            print(f"[X] EasyXT[EMOJI]: {e}")
            print("[TIP] [EMOJI]:")
            print("   1. [EMOJI]")
            print("   2. [EMOJI]userdata[EMOJI]")
            print("   3. [EMOJI]")
            
            if REQUIRE_REAL_TRADING:
                print("[EMOJI] [EMOJI]")
                sys.exit(1)
    
    def get_real_stock_data_with_retry(self, stock_code, count=60, max_retries=3):
        """
        [EMOJI]qstock[EMOJI] - [EMOJI]
        
        Args:
            stock_code (str): [EMOJI]
            count (int): [EMOJI]
            max_retries (int): [EMOJI]
            
        Returns:
            pd.DataFrame: [EMOJI]
        """
        print(f"[CHART] [EMOJI]qstock[EMOJI] {stock_code} [EMOJI]...")
        
        for attempt in range(max_retries):
            try:
                print(f"  [EMOJI] {attempt + 1}/{max_retries} [EMOJI]...")
                
                # [EMOJI]1: [EMOJI]get_data ([EMOJI])
                if attempt == 0:
                    print("  [UP] [EMOJI] qs.get_data() [EMOJI]...")
                    data = qs.get_data(stock_code)
                
                # [EMOJI]2: [EMOJI]get_data_sina ([EMOJI])
                elif attempt == 1:
                    print("  [UP] [EMOJI] qs.get_data_sina() [EMOJI]...")
                    try:
                        data = qs.get_data_sina(stock_code)
                    except AttributeError:
                        print("    [!] get_data_sina [EMOJI]")
                        data = qs.get_data(stock_code)
                
                # [EMOJI]3: [EMOJI]
                else:
                    print("  [UP] [EMOJI]...")
                    end_date = datetime.now().strftime('%Y-%m-%d')
                    start_date = (datetime.now() - timedelta(days=count*2)).strftime('%Y-%m-%d')
                    try:
                        data = qs.get_data(stock_code, start=start_date, end=end_date)
                    except:
                        data = qs.get_data(stock_code)
                
                # [EMOJI]
                if data is not None and not data.empty and len(data) >= 10:
                    print(f"  [OK] [EMOJI] {len(data)} [EMOJI]")
                    return self._validate_and_clean_data(data)
                else:
                    print(f"  [!] [EMOJI] {len(data) if data is not None else 0} [EMOJI]")
                    
            except Exception as e:
                print(f"  [X] [EMOJI] {attempt + 1} [EMOJI]: {e}")
                if attempt < max_retries - 1:
                    print(f"  [EMOJI] {(attempt + 1) * 2} [EMOJI]...")
                    time.sleep((attempt + 1) * 2)
        
        print("[X] [EMOJI]")
        return None
    
    def _validate_and_clean_data(self, data):
        """[EMOJI]"""
        if data is None or data.empty:
            return None
        
        print(f"[EMOJI] [EMOJI]:")
        print(f"  [EMOJI]: {data.shape}")
        print(f"  [EMOJI]: {list(data.columns)}")
        
        # [EMOJI]
        column_mapping = {
            'open': 'open',
            'high': 'high',
            'low': 'low',
            'close': 'close',
            'volume': 'volume',
            'Open': 'open',
            'High': 'high',
            'Low': 'low',
            'Close': 'close',
            'Volume': 'volume'
        }
        
        for old_name, new_name in column_mapping.items():
            if old_name in data.columns:
                data = data.rename(columns={old_name: new_name})
        
        # [EMOJI]
        required_columns = ['open', 'high', 'low', 'close', 'volume']
        missing_columns = [col for col in required_columns if col not in data.columns]
        
        if missing_columns:
            print(f"[X] [EMOJI]: {missing_columns}")
            return None
        
        # [EMOJI]
        original_len = len(data)
        data = data.dropna()
        data = data[data['volume'] > 0]
        
        # [EMOJI]
        for col in required_columns:
            data[col] = pd.to_numeric(data[col], errors='coerce')
        
        data = data.dropna()
        
        if len(data) < 10:
            print(f"[X] [EMOJI]: {len(data)} [EMOJI]")
            return None
        
        print(f"[OK] [EMOJI]: {original_len} -> {len(data)} [EMOJI]")
        print(f"  [EMOJI]: {data['close'].min():.2f} - {data['close'].max():.2f}")
        print(f"  [EMOJI]: {data['close'].iloc[-1]:.2f}")
        
        return data
    
    def calculate_technical_indicators(self, data):
        """[EMOJI]"""
        print("[UP] [EMOJI]...")
        
        # [EMOJI]
        data['MA5'] = data['close'].rolling(window=5).mean()
        data['MA10'] = data['close'].rolling(window=10).mean()
        data['MA20'] = data['close'].rolling(window=20).mean()
        
        # RSI
        delta = data['close'].diff()
        gain = (delta.where(delta > 0, 0)).rolling(window=14).mean()
        loss = (-delta.where(delta < 0, 0)).rolling(window=14).mean()
        rs = gain / loss
        data['RSI14'] = 100 - (100 / (1 + rs))
        
        # MACD
        exp1 = data['close'].ewm(span=12).mean()
        exp2 = data['close'].ewm(span=26).mean()
        data['MACD'] = exp1 - exp2
        data['MACD_signal'] = data['MACD'].ewm(span=9).mean()
        data['MACD_hist'] = data['MACD'] - data['MACD_signal']
        
        # [EMOJI]
        data['BB_middle'] = data['close'].rolling(window=20).mean()
        bb_std = data['close'].rolling(window=20).std()
        data['BB_upper'] = data['BB_middle'] + (bb_std * 2)
        data['BB_lower'] = data['BB_middle'] - (bb_std * 2)
        
        # KDJ[EMOJI]
        low_min = data['low'].rolling(window=9).min()
        high_max = data['high'].rolling(window=9).max()
        rsv = (data['close'] - low_min) / (high_max - low_min) * 100
        data['K'] = rsv.ewm(com=2).mean()
        data['D'] = data['K'].ewm(com=2).mean()
        data['J'] = 3 * data['K'] - 2 * data['D']
        
        print("[OK] [EMOJI]")
        return data
    
    def generate_trading_signals(self, data):
        """[EMOJI]"""
        print("[TARGET] [EMOJI]...")
        
        data['signal'] = 0
        data['confidence'] = 0
        data['signal_reason'] = ''
        
        for i in range(1, len(data)):
            signals = []
            reasons = []
            
            # [EMOJI]1: MA[EMOJI]
            if data['MA5'].iloc[i] > data['MA10'].iloc[i] and data['MA5'].iloc[i-1] <= data['MA10'].iloc[i-1]:
                signals.append(1)
                reasons.append("MA[EMOJI]")
            elif data['MA5'].iloc[i] < data['MA10'].iloc[i] and data['MA5'].iloc[i-1] >= data['MA10'].iloc[i-1]:
                signals.append(-1)
                reasons.append("MA[EMOJI]")
            
            # [EMOJI]2: RSI[EMOJI]
            if data['RSI14'].iloc[i] < 30:
                signals.append(1)
                reasons.append("RSI[EMOJI]")
            elif data['RSI14'].iloc[i] > 70:
                signals.append(-1)
                reasons.append("RSI[EMOJI]")
            
            # [EMOJI]3: MACD[EMOJI]
            if (data['MACD'].iloc[i] > data['MACD_signal'].iloc[i] and 
                data['MACD'].iloc[i-1] <= data['MACD_signal'].iloc[i-1]):
                signals.append(1)
                reasons.append("MACD[EMOJI]")
            elif (data['MACD'].iloc[i] < data['MACD_signal'].iloc[i] and 
                  data['MACD'].iloc[i-1] >= data['MACD_signal'].iloc[i-1]):
                signals.append(-1)
                reasons.append("MACD[EMOJI]")
            
            # [EMOJI]4: [EMOJI]
            if data['close'].iloc[i] < data['BB_lower'].iloc[i]:
                signals.append(1)
                reasons.append("[EMOJI]")
            elif data['close'].iloc[i] > data['BB_upper'].iloc[i]:
                signals.append(-1)
                reasons.append("[EMOJI]")
            
            # [EMOJI]5: KDJ[EMOJI]
            if data['K'].iloc[i] < 20 and data['D'].iloc[i] < 20:
                signals.append(1)
                reasons.append("KDJ[EMOJI]")
            elif data['K'].iloc[i] > 80 and data['D'].iloc[i] > 80:
                signals.append(-1)
                reasons.append("KDJ[EMOJI]")
            
            # [EMOJI]
            if signals:
                buy_signals = signals.count(1)
                sell_signals = signals.count(-1)
                
                if buy_signals > sell_signals:
                    data.loc[data.index[i], 'signal'] = 1
                    data.loc[data.index[i], 'confidence'] = min(95, 40 + buy_signals * 15)
                elif sell_signals > buy_signals:
                    data.loc[data.index[i], 'signal'] = -1
                    data.loc[data.index[i], 'confidence'] = min(95, 40 + sell_signals * 15)
                else:
                    data.loc[data.index[i], 'confidence'] = 50
                
                data.loc[data.index[i], 'signal_reason'] = ", ".join(reasons)
        
        signal_count = (data['signal'] != 0).sum()
        print(f"[OK] [EMOJI] {signal_count} [EMOJI]")
        return data
    
    def execute_real_trades(self, data, stock_code):
        """[EMOJI] ([EMOJI] - [EMOJI]EasyXT[EMOJI])"""
        print("[EMOJI] [EMOJI]...")
        
        # [EMOJI]
        if self.trade_initialized:
            print("[OK] EasyXT[EMOJI]")
        else:
            print("[!] [EMOJI]: EasyXT[EMOJI]")
        
        # [EMOJI]
        high_confidence_signals = data[(data['signal'] != 0) & (data['confidence'] >= 70)]
        all_signals = data[data['signal'] != 0]
        
        print(f"[CHART] [EMOJI]:")
        print(f"  [EMOJI]: {len(all_signals)}")
        print(f"  [EMOJI](≥70%): {len(high_confidence_signals)}")
        print(f"  [EMOJI]: {(all_signals['signal'] == 1).sum()}")
        print(f"  [EMOJI]: {(all_signals['signal'] == -1).sum()}")
        
        if not all_signals.empty:
            print(f"\n[EMOJI] [EMOJI]5[EMOJI]:")
            recent_signals = all_signals.tail(5)
            for idx, row in recent_signals.iterrows():
                signal_type = "[EMOJI]" if row['signal'] == 1 else "[EMOJI]"
                print(f"  {idx.strftime('%Y-%m-%d')}: {signal_type} | [EMOJI]: {row['close']:.2f} | [EMOJI]: {row['confidence']:.0f}%")
                print(f"    [NOTE] {row['signal_reason']}")
        
        # [EMOJI] - [EMOJI]
        if len(high_confidence_signals) > 0:
            print(f"\n[EMOJI] [EMOJI] {len(high_confidence_signals)} [EMOJI]")
            
            # [EMOJI]
            latest_signal = high_confidence_signals.iloc[-1]
            signal_type = "[EMOJI]" if latest_signal['signal'] == 1 else "[EMOJI]"
            
            print(f"\n[UP] [EMOJI]:")
            print(f"  [EMOJI]: {stock_code}")
            print(f"  [EMOJI]: {signal_type}")
            print(f"  [EMOJI]: {latest_signal['close']:.2f}")
            print(f"  [EMOJI]: {latest_signal['confidence']:.0f}%")
            print(f"  [EMOJI]: {latest_signal['signal_reason']}")
            print(f"  [EMOJI]: {latest_signal.name.strftime('%Y-%m-%d')}")
            
            if self.trade_initialized:
                # [EMOJI]
                if self._confirm_trade(stock_code, signal_type, latest_signal['close'], latest_signal['confidence']):
                    self._execute_trade_order(stock_code, latest_signal['signal'], latest_signal['close'])
                else:
                    print("[X] [EMOJI]")
            else:
                print("[TIP] [EMOJI]")
        else:
            print(f"\n[TIP] [EMOJI]")
            if len(all_signals) > 0:
                print("[CHART] [EMOJI]")
    
    def _confirm_trade(self, stock_code, signal_type, price, confidence):
        """[EMOJI]"""
        print(f"\n" + "="*60)
        print(f"[EMOJI] [EMOJI]")
        print(f"="*60)
        print(f"[EMOJI]: {stock_code}")
        print(f"[EMOJI]: {signal_type}")
        print(f"[EMOJI]: {price:.2f} [EMOJI]")
        print(f"[EMOJI]: {confidence:.0f}%")
        print(f"[EMOJI]: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print(f"="*60)
        print("[TIP] [EMOJI]EasyXT[EMOJI]")
        print("[!]  [EMOJI]")
        print(f"="*60)
        
        while True:
            confirm = input("[EMOJI]? (y/n): ").lower().strip()
            if confirm in ['y', 'yes', '[EMOJI]', '[EMOJI]']:
                return True
            elif confirm in ['n', 'no', '[EMOJI]', '[EMOJI]']:
                return False
            else:
                print("[EMOJI] y/n [EMOJI] [EMOJI]/[EMOJI]")
    
    def _execute_trade_order(self, stock_code, signal, price):
        """[EMOJI] - [EMOJI]"""
        try:
            # [EMOJI]
            account_info = self._get_account_info()
            position_info = self._get_position_info(stock_code)
            
            # [EMOJI]
            quantity = self._calculate_trade_quantity(signal, price, account_info, position_info)
            
            if quantity <= 0:
                print(f"[X] [EMOJI]")
                return
            
            if signal == 1:  # [EMOJI]
                print(f"[UP] [EMOJI]:")
                print(f"   [EMOJI]: {stock_code}")
                print(f"   [EMOJI]: {quantity} [EMOJI]")
                print(f"   [EMOJI]: {price:.2f} [EMOJI]")
                print(f"   [EMOJI]: {quantity * price:.2f} [EMOJI]")
                
                # [EMOJI]EasyXT[EMOJI] - [EMOJI]
                try:
                    if self.trade_initialized and self.trader:
                        # [EMOJI]API[EMOJI]
                        result = self.trader.buy(
                            account_id=self.account_id,
                            code=stock_code,
                            volume=quantity,
                            price=price,
                            price_type='limit'  # [EMOJI]
                        )
                        
                        if result:
                            print(f"[OK] [EMOJI]")
                            print(f"   [EMOJI]: {result}")
                            status = '[EMOJI]'
                        else:
                            print(f"[!] [EMOJI]")
                            status = '[EMOJI]'
                    else:
                        print(f"[!] [EMOJI]")
                        status = '[EMOJI]'
                        
                except Exception as e:
                    print(f"[X] [EMOJI]: {e}")
                    status = f'[EMOJI]: {str(e)}'
                
            elif signal == -1:  # [EMOJI]
                print(f"[EMOJI] [EMOJI]:")
                print(f"   [EMOJI]: {stock_code}")
                print(f"   [EMOJI]: {quantity} [EMOJI]")
                print(f"   [EMOJI]: {price:.2f} [EMOJI]")
                print(f"   [EMOJI]: {quantity * price:.2f} [EMOJI]")
                
                # [EMOJI]EasyXT[EMOJI] - [EMOJI]
                try:
                    if self.trade_initialized and self.trader:
                        # [EMOJI]API[EMOJI]
                        result = self.trader.sell(
                            account_id=self.account_id,
                            code=stock_code,
                            volume=quantity,
                            price=price,
                            price_type='limit'  # [EMOJI]
                        )
                        
                        if result:
                            print(f"[OK] [EMOJI]")
                            print(f"   [EMOJI]: {result}")
                            status = '[EMOJI]'
                        else:
                            print(f"[!] [EMOJI]")
                            status = '[EMOJI]'
                    else:
                        print(f"[!] [EMOJI]")
                        status = '[EMOJI]'
                        
                except Exception as e:
                    print(f"[X] [EMOJI]: {e}")
                    status = f'[EMOJI]: {str(e)}'
            
            # [EMOJI]
            trade_record = {
                'timestamp': datetime.now(),
                'stock_code': stock_code,
                'action': '[EMOJI]' if signal == 1 else '[EMOJI]',
                'quantity': quantity,
                'price': price,
                'amount': quantity * price,
                'status': status
            }
            self.trade_log.append(trade_record)
            
        except Exception as e:
            print(f"[X] [EMOJI]: {e}")
            # [EMOJI]
            trade_record = {
                'timestamp': datetime.now(),
                'stock_code': stock_code,
                'action': '[EMOJI]' if signal == 1 else '[EMOJI]',
                'quantity': 0,
                'price': price,
                'amount': 0,
                'status': f'[EMOJI]: {str(e)}'
            }
            self.trade_log.append(trade_record)
    
    def _get_account_info(self):
        """[EMOJI] - [EMOJI]"""
        try:
            if self.trade_initialized and self.trader:
                # [EMOJI]API[EMOJI]
                account_info = self.trader.get_account_asset(self.account_id)
                if account_info:
                    print(f"[OK] [EMOJI]")
                    return account_info
            
            print(f"[!] [EMOJI]")
            return {'cash': 100000, 'total_asset': 100000}  # [EMOJI]
            
        except Exception as e:
            print(f"[!] [EMOJI]: {e}")
            return {'cash': 100000, 'total_asset': 100000}  # [EMOJI]
    
    def _get_position_info(self, stock_code):
        """[EMOJI] - [EMOJI]"""
        try:
            if self.trade_initialized and self.trader:
                # [EMOJI]API[EMOJI]
                positions = self.trader.get_positions(self.account_id, stock_code)
                if not positions.empty:
                    print(f"[OK] [EMOJI] {stock_code} [EMOJI]")
                    return positions.iloc[0].to_dict()
                else:
                    print(f"[!] [EMOJI] {stock_code} [EMOJI]")
                    return {'volume': 0, 'can_use_volume': 0}
            
            print(f"[!] [EMOJI]")
            return {'volume': 0, 'can_use_volume': 0}
            
        except Exception as e:
            print(f"[!] [EMOJI]: {e}")
            return {'volume': 0, 'can_use_volume': 0}
    
    def _calculate_trade_quantity(self, signal, price, account_info, position_info):
        """[EMOJI]"""
        try:
            if signal == 1:  # [EMOJI]
                # [EMOJI]
                available_cash = account_info.get('cash', 100000)
                print(f"  [EMOJI]: {available_cash:.2f} [EMOJI]")
                
                # [EMOJI]30%[EMOJI]
                trade_amount = available_cash * 0.3
                print(f"  [EMOJI]: {trade_amount:.2f} [EMOJI] (30%[EMOJI])")
                
                # [EMOJI]0.1%[EMOJI]
                quantity = int(trade_amount / (price * 1.001)) // 100 * 100  # [EMOJI]
                quantity = max(100, quantity)  # [EMOJI]1[EMOJI]
                
                print(f"  [EMOJI]: {quantity} [EMOJI]")
                return quantity
                
            elif signal == -1:  # [EMOJI]
                # [EMOJI]
                can_sell = position_info.get('can_use_volume', 0)
                total_volume = position_info.get('volume', 0)
                
                print(f"  [EMOJI]: {total_volume} [EMOJI]")
                print(f"  [EMOJI]: {can_sell} [EMOJI]")
                
                if can_sell > 0:
                    # [EMOJI]50%[EMOJI]100[EMOJI]
                    quantity = max(100, can_sell // 2)
                    quantity = min(quantity, can_sell)  # [EMOJI]
                    print(f"  [EMOJI]: {quantity} [EMOJI] (50%[EMOJI])")
                    return quantity
                else:
                    print("[!] [EMOJI]")
                    return 100  # [EMOJI]
                    
        except Exception as e:
            print(f"[!] [EMOJI]: {e}")
            return 100  # [EMOJI]1[EMOJI]
    
    def analyze_performance(self, data):
        """[EMOJI]"""
        print("\n" + "=" * 60)
        print("[CHART] [EMOJI]")
        print("=" * 60)
        
        signals = data[data['signal'] != 0].copy()
        
        if signals.empty:
            print("[X] [EMOJI]")
            return
        
        # [EMOJI]
        print(f"[UP] [EMOJI]:")
        print(f"  [EMOJI]: {len(signals)}")
        print(f"  [EMOJI]: {(signals['signal'] == 1).sum()}")
        print(f"  [EMOJI]: {(signals['signal'] == -1).sum()}")
        print(f"  [EMOJI]: {signals['confidence'].mean():.1f}%")
        print(f"  [EMOJI](≥70%): {len(signals[signals['confidence'] >= 70])}")
        print(f"  [EMOJI]: {signals['confidence'].max():.1f}%")
        
        # [EMOJI]
        if len(signals) > 1:
            price_changes = []
            for i in range(len(signals) - 1):
                current_signal = signals.iloc[i]
                next_signal = signals.iloc[i + 1]
                
                if current_signal['signal'] == 1:  # [EMOJI]
                    price_change = (next_signal['close'] - current_signal['close']) / current_signal['close']
                    price_changes.append(price_change)
            
            if price_changes:
                avg_return = np.mean(price_changes) * 100
                win_rate = len([x for x in price_changes if x > 0]) / len(price_changes) * 100
                max_return = max(price_changes) * 100
                min_return = min(price_changes) * 100
                
                print(f"\n[MONEY] [EMOJI]:")
                print(f"  [EMOJI]: {avg_return:.2f}%")
                print(f"  [EMOJI]: {win_rate:.1f}%")
                print(f"  [EMOJI]: {max_return:.2f}%")
                print(f"  [EMOJI]: {min_return:.2f}%")
        
        # [EMOJI]
        latest = data.iloc[-1]
        print(f"\n[CHART] [EMOJI]:")
        print(f"  [EMOJI]: {latest['close']:.2f}")
        print(f"  MA5: {latest['MA5']:.2f}")
        print(f"  MA10: {latest['MA10']:.2f}")
        print(f"  MA20: {latest['MA20']:.2f}")
        print(f"  RSI14: {latest['RSI14']:.1f}")
        print(f"  MACD: {latest['MACD']:.4f}")
        print(f"  K[EMOJI]: {latest['K']:.1f}")
        print(f"  D[EMOJI]: {latest['D']:.1f}")
        
        # [EMOJI]
        if self.trade_log:
            print(f"\n[NOTE] [EMOJI]:")
            print(f"  [EMOJI]: {len(self.trade_log)}")
            successful_trades = [t for t in self.trade_log if '[EMOJI]' in t['status']]
            print(f"  [EMOJI]: {len(successful_trades)}")
            print(f"  [EMOJI]: {len(successful_trades)/len(self.trade_log)*100:.1f}%")
    
    def save_data(self, data, stock_code):
        """[EMOJI]"""
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        
        # [EMOJI]
        filename = f"{self.data_dir}/{stock_code}_fixed_trading_{timestamp}.csv"
        data.to_csv(filename, encoding='utf-8-sig')
        print(f"[EMOJI] [EMOJI]: {filename}")
        
        # [EMOJI]
        if self.trade_log:
            log_filename = f"{self.log_dir}/fixed_trade_log_{timestamp}.csv"
            pd.DataFrame(self.trade_log).to_csv(log_filename, index=False, encoding='utf-8-sig')
            print(f"[NOTE] [EMOJI]: {log_filename}")
        
        # [EMOJI]
        signals = data[data['signal'] != 0]
        if not signals.empty:
            summary_filename = f"{self.data_dir}/{stock_code}_signals_{timestamp}.csv"
            signal_summary = signals[['close', 'signal', 'confidence', 'signal_reason']].copy()
            signal_summary.to_csv(summary_filename, encoding='utf-8-sig')
            print(f"[EMOJI] [EMOJI]: {summary_filename}")
    
    def run_strategy(self, stock_code="000001"):
        """[EMOJI]"""
        print("=" * 60)
        print("[LAUNCH] [EMOJI]")
        print("=" * 60)
        
        # [EMOJI]
        print("\n[EMOJI]")
        print("=" * 40)
        data = self.get_real_stock_data_with_retry(stock_code)
        
        if data is None:
            print("[X] [EMOJI]")
            return
        
        # [EMOJI]
        print("\n[EMOJI]")
        print("=" * 40)
        data = self.calculate_technical_indicators(data)
        
        # [EMOJI]
        print("\n[EMOJI]")
        print("=" * 40)
        data = self.generate_trading_signals(data)
        
        # [EMOJI]
        print("\n[EMOJI]")
        print("=" * 40)
        self.execute_real_trades(data, stock_code)
        
        # [EMOJI]
        print("\n[EMOJI]")
        print("=" * 40)
        self.analyze_performance(data)
        
        # [EMOJI]
        print("\n[EMOJI]")
        print("=" * 40)
        self.save_data(data, stock_code)
        
        return data


def main():
    """[EMOJI] - [EMOJI]QStock[EMOJI]"""
    print("[TARGET] QStock[EMOJI] ([EMOJI])")
    print("[EMOJI]qstock[EMOJI] + EasyXT[EMOJI]")
    print("[!]  [EMOJI]")
    
    print(f"\n[TOOL] [EMOJI]:")
    print(f"  [EMOJI]: {USERDATA_PATH}")
    print(f"  [EMOJI]ID: {DEFAULT_ACCOUNT_ID}")
    print(f"  [EMOJI]: qstock")
    print(f"  [EMOJI]: EasyXT")
    
    # [EMOJI]
    strategy = FixedRealTradingQStockStrategy()
    
    # [EMOJI]
    stock_code = "000001"  # [EMOJI]
    data = strategy.run_strategy(stock_code)
    
    print("\n" + "=" * 60)
    print("[OK] [EMOJI]QStock[EMOJI]")
    print("[EMOJI] [EMOJI]data[EMOJI]")
    print("[TIP] [EMOJI]")
    print("[EMOJI] [EMOJI]qstock[EMOJI] + EasyXT[EMOJI]")
    print("[EMOJI]  [EMOJI]")
    print("[!]  [EMOJI]")
    print("=" * 60)

if __name__ == "__main__":
    main()