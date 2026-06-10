"""
[EMOJI] - [EMOJI]
[EMOJI]

[EMOJI]
1. [EMOJI]DataManager[EMOJI]
2. [EMOJI]
3. [EMOJI]
4. [EMOJI]
5. [EMOJI]
6. [EMOJI]

[EMOJI]
- QMT[EMOJI]
- Tushare[EMOJI]token[EMOJI]
- DuckDB[EMOJI]

[EMOJI]quant
[EMOJI]2025-01-09
[EMOJI]2025-03-10[EMOJI]

=====================================================================
[EMOJI] [EMOJI] - [EMOJI] [EMOJI]
=====================================================================

[EMOJI]

# [EMOJI]1[EMOJI]
USE_REAL_DATA = True      # True=[EMOJI](QMT/Tushare/DuckDB)  False=[EMOJI]
                          # [EMOJI]True[EMOJI]

# [EMOJI]2[EMOJI]
USE_REAL_TRADING = True  # False=[EMOJI]([EMOJI])  True=[EMOJI]([EMOJI])
                          # [!] [EMOJI]True[EMOJI]
                          # [EMOJI]False

[EMOJI]
- [EMOJI]USE_REAL_DATA=True, USE_REAL_TRADING=False[EMOJI]+[EMOJI]
- [EMOJI]USE_REAL_DATA=False, USE_REAL_TRADING=False[EMOJI]+[EMOJI]
- [EMOJI]USE_REAL_DATA=True, USE_REAL_TRADING=True[EMOJI]+[EMOJI]
           [!] [EMOJI]QMT[EMOJI]

[EMOJI]
[EMOJI]1[EMOJI]
  python [EMOJI]/10_[EMOJI].py --real-trading

[EMOJI]2[EMOJI]
  USE_REAL_TRADING = False  # [EMOJI] True

[EMOJI]
- [EMOJI]
- [EMOJI]
- [EMOJI]
- [EMOJI]

=====================================================================
"""

# ==================== [EMOJI]====================
USE_REAL_DATA = True       # [EMOJI]True=[EMOJI]False=[EMOJI]
USE_REAL_TRADING = True   # [EMOJI]False=[EMOJI]True=[EMOJI][!]
# ===============================================================

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import os
import sys
import argparse
from datetime import datetime, timedelta
import warnings
warnings.filterwarnings('ignore')

# [EMOJI]
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
if project_root not in sys.path:
    sys.path.insert(0, project_root)

# [EMOJI]
try:
    from easyxt_backtest import DataManager
    DATA_MANAGER_AVAILABLE = True
    print("[OK] DataManager[EMOJI]")
except ImportError as e:
    DATA_MANAGER_AVAILABLE = False
    print(f"[!] DataManager[EMOJI]: {e}")

# [EMOJI]API[EMOJI]
try:
    import easy_xt
    EASY_XT_AVAILABLE = True
    print("[OK] easy_xt[EMOJI]")
except ImportError as e:
    EASY_XT_AVAILABLE = False
    print(f"[WARNING] easy_xt[EMOJI]: {e}")

# [EMOJI]
plt.rcParams['font.sans-serif'] = ['SimHei']
plt.rcParams['axes.unicode_minus'] = False

class TradingStrategy:
    """[EMOJI] - [EMOJI]"""

    def __init__(self, use_real_trading=False, use_real_data=True):
        """
        [EMOJI]

        Args:
            use_real_trading (bool): [EMOJI]False[EMOJI]
            use_real_data (bool): [EMOJI]True
        """
        self.use_real_trading = use_real_trading
        self.use_real_data = use_real_data and DATA_MANAGER_AVAILABLE
        self.data_dir = "data"
        self.log_dir = "logs"

        # [EMOJI]
        for dir_path in [self.data_dir, self.log_dir]:
            if not os.path.exists(dir_path):
                os.makedirs(dir_path)

        # [EMOJI]
        if self.use_real_data:
            try:
                self.data_manager = DataManager()
                print("[OK] DataManager[EMOJI]")
            except Exception as e:
                print(f"[X] DataManager[EMOJI]: {e}")
                self.use_real_data = False
                print("[NOTE] [EMOJI]")

        # [EMOJI]
        if self.use_real_trading and EASY_XT_AVAILABLE:
            try:
                # [EMOJI]API[EMOJI]easy_xt[EMOJI]API[EMOJI]
                self.trader = RealTradeAdapter()
                print("  [[EMOJI]] [EMOJI]")
            except Exception as e:
                print(f"  [[EMOJI]] [EMOJI]: {e}")
                self.use_real_trading = False
                print("  [[EMOJI]] [EMOJI]")

        if not self.use_real_trading:
            self.trader = MockTrader()
            print("  [[EMOJI]] [EMOJI]")

        # [EMOJI]
        self.position = {}  # [EMOJI]
        self.cash = 100000  # [EMOJI]
        self.trade_log = []  # [EMOJI]

        data_mode = "[EMOJI]" if self.use_real_data else "[EMOJI]"
        trade_mode = "[EMOJI]" if self.use_real_trading else "[EMOJI]"
        print(f"[LAUNCH] [EMOJI] - {data_mode}/{trade_mode}[EMOJI]")
    
    def load_sample_data(self, stock_code='000001', start_date=None, end_date=None):
        """
        [EMOJI]

        Args:
            stock_code (str): [EMOJI]
            start_date (str): [EMOJI]YYYYMMDD[EMOJI]60[EMOJI]
            end_date (str): [EMOJI]YYYYMMDD[EMOJI]

        Returns:
            pd.DataFrame: [EMOJI]
        """
        try:
            # [EMOJI]
            if self.use_real_data:
                print(f"[CHART] [EMOJI]DataManager[EMOJI]...")

                # [EMOJI]
                if end_date is None:
                    end_date = datetime.now().strftime('%Y%m%d')
                if start_date is None:
                    start_date = (datetime.now() - timedelta(days=90)).strftime('%Y%m%d')

                # [EMOJI]
                data = self.data_manager.get_price(
                    codes=stock_code,
                    start_date=start_date,
                    end_date=end_date
                )

                if data is not None and not data.empty:
                    # [EMOJI]MultiIndex
                    if isinstance(data.index, pd.MultiIndex):
                        data = data.reset_index()

                    # [EMOJI]
                    if 'date' in data.columns:
                        # [EMOJI]date[EMOJI]
                        if pd.api.types.is_integer_dtype(data['date']):
                            # [EMOJI]QMT[EMOJI]
                            # [EMOJI]10000000000[EMOJI]
                            first_timestamp = data['date'].iloc[0]
                            if first_timestamp > 10000000000:  # [EMOJI]
                                data['date'] = pd.to_datetime(data['date'], unit='ms')
                            else:  # [EMOJI]
                                data['date'] = pd.to_datetime(data['date'], unit='s')
                        else:
                            data['date'] = pd.to_datetime(data['date'])

                        # [EMOJI]
                        data.set_index('date', inplace=True)

                    # [EMOJI]
                    required_columns = ['open', 'high', 'low', 'close', 'volume']
                    missing_columns = [col for col in required_columns if col not in data.columns]

                    if missing_columns:
                        print(f"[!] [EMOJI]: {missing_columns}")
                        return self._generate_sample_data(stock_code)

                    print(f"[OK] [EMOJI]: {len(data)} [EMOJI]")
                    print(f"[EMOJI] [EMOJI]: {data.index[0].strftime('%Y-%m-%d')} [EMOJI] {data.index[-1].strftime('%Y-%m-%d')}")
                    return data
                else:
                    print(f"[!] [EMOJI]")

            # [EMOJI]
            print("[CHART] [EMOJI]...")
            return self._generate_sample_data(stock_code)

        except Exception as e:
            print(f"[X] [EMOJI]: {e}")
            print("[CHART] [EMOJI]...")
            return self._generate_sample_data(stock_code)
    
    def _generate_sample_data(self, stock_code, days=60):
        """
        [EMOJI]

        [!] [EMOJI]
        [EMOJI]
        """
        print(f"[!] [EMOJI] {days} [EMOJI]")

        # [EMOJI]
        dates = pd.date_range(end=datetime.now(), periods=days * 7 // 5, freq='B')

        # [EMOJI] ([EMOJI])
        np.random.seed(42)  # [EMOJI]

        initial_price = 10.0
        returns = np.random.normal(0.001, 0.02, len(dates))  # [EMOJI]
        prices = [initial_price]

        for ret in returns[1:]:
            prices.append(prices[-1] * (1 + ret))

        # [EMOJI]OHLC[EMOJI]
        data = []
        for i, (date, close) in enumerate(zip(dates, prices)):
            high = close * (1 + abs(np.random.normal(0, 0.01)))
            low = close * (1 - abs(np.random.normal(0, 0.01)))
            open_price = prices[i-1] if i > 0 else close
            volume = np.random.randint(1000000, 10000000)

            data.append({
                'open': open_price,
                'high': max(open_price, high, close),
                'low': min(open_price, low, close),
                'close': close,
                'volume': volume
            })

        df = pd.DataFrame(data, index=dates)

        # [EMOJI]
        filename = f"{self.data_dir}/{stock_code}_sample_data.csv"
        df.to_csv(filename)
        print(f"[OK] [EMOJI] {filename}")
        print("[!] [EMOJI]")

        return df
    
    def calculate_indicators(self, data):
        """
        [EMOJI]
        
        Args:
            data (pd.DataFrame): [EMOJI]
            
        Returns:
            pd.DataFrame: [EMOJI]
        """
        print("[UP] [EMOJI]...")
        
        try:
            # [EMOJI]
            data['MA5'] = data['close'].rolling(window=5).mean()
            data['MA10'] = data['close'].rolling(window=10).mean()
            data['MA20'] = data['close'].rolling(window=20).mean()
            
            # RSI[EMOJI]
            delta = data['close'].diff()
            gain = (delta.where(delta > 0, 0)).rolling(window=14).mean()
            loss = (-delta.where(delta < 0, 0)).rolling(window=14).mean()
            rs = gain / loss
            data['RSI'] = 100 - (100 / (1 + rs))
            
            # MACD[EMOJI]
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
            
            # [EMOJI]
            data['VOL_MA5'] = data['volume'].rolling(window=5).mean()
            
            print("[OK] [EMOJI]")
            return data
            
        except Exception as e:
            print(f"[X] [EMOJI]: {e}")
            return data
    
    def generate_signals(self, data):
        """
        [EMOJI]
        
        Args:
            data (pd.DataFrame): [EMOJI]
            
        Returns:
            pd.DataFrame: [EMOJI]
        """
        print("[TARGET] [EMOJI]...")
        
        try:
            # [EMOJI]
            data['signal'] = 0  # 0: [EMOJI], 1: [EMOJI], -1: [EMOJI]
            data['signal_strength'] = 0  # [EMOJI] 0-100
            
            # [EMOJI]1: [EMOJI]
            ma_cross_buy = (data['MA5'] > data['MA10']) & (data['MA5'].shift(1) <= data['MA10'].shift(1))
            ma_cross_sell = (data['MA5'] < data['MA10']) & (data['MA5'].shift(1) >= data['MA10'].shift(1))
            
            # [EMOJI]2: RSI[EMOJI]
            rsi_oversold = data['RSI'] < 30
            rsi_overbought = data['RSI'] > 70
            
            # [EMOJI]3: MACD[EMOJI]
            macd_golden = (data['MACD'] > data['MACD_signal']) & (data['MACD'].shift(1) <= data['MACD_signal'].shift(1))
            macd_death = (data['MACD'] < data['MACD_signal']) & (data['MACD'].shift(1) >= data['MACD_signal'].shift(1))
            
            # [EMOJI]4: [EMOJI]
            bb_break_up = data['close'] > data['BB_upper']
            bb_break_down = data['close'] < data['BB_lower']
            
            # [EMOJI]
            buy_signals = ma_cross_buy | (rsi_oversold & macd_golden) | bb_break_down
            sell_signals = ma_cross_sell | (rsi_overbought & macd_death) | bb_break_up
            
            # [EMOJI]
            data.loc[buy_signals, 'signal'] = 1
            data.loc[sell_signals, 'signal'] = -1
            
            # [EMOJI]
            for idx in data.index:
                if data.loc[idx, 'signal'] != 0:
                    strength = 0
                    
                    # MA[EMOJI]
                    if ma_cross_buy.loc[idx] or ma_cross_sell.loc[idx]:
                        strength += 25
                    
                    # RSI[EMOJI]
                    if rsi_oversold.loc[idx] or rsi_overbought.loc[idx]:
                        strength += 25
                    
                    # MACD[EMOJI]
                    if macd_golden.loc[idx] or macd_death.loc[idx]:
                        strength += 25
                    
                    # [EMOJI]
                    if bb_break_up.loc[idx] or bb_break_down.loc[idx]:
                        strength += 25
                    
                    data.loc[idx, 'signal_strength'] = min(strength, 100)
            
            # [EMOJI]
            buy_count = (data['signal'] == 1).sum()
            sell_count = (data['signal'] == -1).sum()
            
            print(f"[OK] [EMOJI]: [EMOJI] {buy_count} [EMOJI], [EMOJI] {sell_count} [EMOJI]")
            return data
            
        except Exception as e:
            print(f"[X] [EMOJI]: {e}")
            return data
    
    def execute_trades(self, data, stock_code):
        """
        [EMOJI]
        
        Args:
            data (pd.DataFrame): [EMOJI]
            stock_code (str): [EMOJI]
        """
        print("[EMOJI] [EMOJI]...")
        
        executed_trades = 0
        
        for idx, row in data.iterrows():
            if row['signal'] != 0:
                try:
                    if row['signal'] == 1:  # [EMOJI]
                        result = self._execute_buy(stock_code, row['close'], row['signal_strength'], idx)
                        if result:
                            executed_trades += 1
                    
                    elif row['signal'] == -1:  # [EMOJI]
                        result = self._execute_sell(stock_code, row['close'], row['signal_strength'], idx)
                        if result:
                            executed_trades += 1
                            
                except Exception as e:
                    print(f"[X] [EMOJI] {idx}: {e}")
                    continue
        
        print(f"[OK] [EMOJI] {executed_trades} [EMOJI]")
        self._save_trade_log()
    
    def _execute_buy(self, stock_code, price, strength, date):
        """[EMOJI]"""
        try:
            # [EMOJI] ([EMOJI])
            max_position_value = self.cash * 0.3  # [EMOJI]30%[EMOJI]
            position_ratio = strength / 100 * 0.5  # [EMOJI]
            buy_value = max_position_value * position_ratio
            quantity = int(buy_value / price / 100) * 100  # [EMOJI]
            
            if quantity < 100 or buy_value > self.cash:
                return False
            
            # [EMOJI]
            if self.use_real_trading:
                # [EMOJI]
                success = self.trader.buy(stock_code, price, quantity)
            else:
                # [EMOJI]
                success = self.trader.buy(stock_code, price, quantity)
            
            if success:
                # [EMOJI]
                if stock_code not in self.position:
                    self.position[stock_code] = {'quantity': 0, 'avg_price': 0}
                
                old_quantity = self.position[stock_code]['quantity']
                old_avg_price = self.position[stock_code]['avg_price']
                
                new_quantity = old_quantity + quantity
                new_avg_price = ((old_quantity * old_avg_price) + (quantity * price)) / new_quantity
                
                self.position[stock_code]['quantity'] = new_quantity
                self.position[stock_code]['avg_price'] = new_avg_price
                self.cash -= quantity * price
                
                # [EMOJI]
                trade_record = {
                    'date': date,
                    'stock_code': stock_code,
                    'action': 'BUY',
                    'price': price,
                    'quantity': quantity,
                    'amount': quantity * price,
                    'signal_strength': strength,
                    'cash_after': self.cash
                }
                self.trade_log.append(trade_record)
                
                print(f"  [OK] [EMOJI] {stock_code}: {quantity}[EMOJI] @ {price:.2f}, [EMOJI]: {strength}")
                return True
            
            return False
            
        except Exception as e:
            print(f"[X] [EMOJI]: {e}")
            return False
    
    def _execute_sell(self, stock_code, price, strength, date):
        """[EMOJI]"""
        try:
            if stock_code not in self.position or self.position[stock_code]['quantity'] <= 0:
                return False
            
            # [EMOJI] ([EMOJI])
            current_quantity = self.position[stock_code]['quantity']
            sell_ratio = strength / 100 * 0.8  # [EMOJI]
            quantity = int(current_quantity * sell_ratio / 100) * 100  # [EMOJI]
            
            if quantity < 100:
                quantity = current_quantity  # [EMOJI]
            
            # [EMOJI]
            if self.use_real_trading:
                # [EMOJI]
                success = self.trader.sell(stock_code, price, quantity)
            else:
                # [EMOJI]
                success = self.trader.sell(stock_code, price, quantity)
            
            if success:
                # [EMOJI]
                self.position[stock_code]['quantity'] -= quantity
                self.cash += quantity * price
                
                # [EMOJI]
                trade_record = {
                    'date': date,
                    'stock_code': stock_code,
                    'action': 'SELL',
                    'price': price,
                    'quantity': quantity,
                    'amount': quantity * price,
                    'signal_strength': strength,
                    'cash_after': self.cash
                }
                self.trade_log.append(trade_record)
                
                print(f"  [OK] [EMOJI] {stock_code}: {quantity}[EMOJI] @ {price:.2f}, [EMOJI]: {strength}")
                return True
            
            return False
            
        except Exception as e:
            print(f"[X] [EMOJI]: {e}")
            return False
    
    def _save_trade_log(self):
        """[EMOJI]"""
        if self.trade_log:
            df = pd.DataFrame(self.trade_log)
            filename = f"{self.log_dir}/trade_log_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"
            df.to_csv(filename, index=False)
            print(f"[EMOJI] [EMOJI] {filename}")
    
    def analyze_performance(self):
        """[EMOJI]"""
        print("\n" + "=" * 50)
        print("[CHART] [EMOJI]")
        print("=" * 50)
        
        if not self.trade_log:
            print("[X] [EMOJI]")
            return
        
        df = pd.DataFrame(self.trade_log)
        
        # [EMOJI]
        total_trades = len(df)
        buy_trades = len(df[df['action'] == 'BUY'])
        sell_trades = len(df[df['action'] == 'SELL'])
        
        print(f"[UP] [EMOJI]: {total_trades}")
        print(f"[UP] [EMOJI]: {buy_trades}")
        print(f"[UP] [EMOJI]: {sell_trades}")
        
        # [EMOJI]
        initial_cash = 100000
        final_cash = self.cash
        total_position_value = sum([pos['quantity'] * pos['avg_price'] for pos in self.position.values()])
        total_value = final_cash + total_position_value
        
        print(f"[MONEY] [EMOJI]: {initial_cash:,.2f}")
        print(f"[MONEY] [EMOJI]: {final_cash:,.2f}")
        print(f"[MONEY] [EMOJI]: {total_position_value:,.2f}")
        print(f"[MONEY] [EMOJI]: {total_value:,.2f}")
        print(f"[CHART] [EMOJI]: {((total_value - initial_cash) / initial_cash * 100):+.2f}%")
        
        # [EMOJI]
        if self.position:
            print(f"\n[EMOJI] [EMOJI]:")
            for stock, pos in self.position.items():
                if pos['quantity'] > 0:
                    print(f"  {stock}: {pos['quantity']}[EMOJI], [EMOJI]: {pos['avg_price']:.2f}")
    
    def visualize_results(self, data, stock_code):
        """[EMOJI]"""
        print("[UP] [EMOJI]...")
        
        try:
            fig, ((ax1, ax2), (ax3, ax4)) = plt.subplots(2, 2, figsize=(15, 12))
            
            # 1. [EMOJI]
            ax1.plot(data.index, data['close'], label='[EMOJI]', linewidth=2, color='blue')
            ax1.plot(data.index, data['MA5'], label='MA5', alpha=0.7, color='orange')
            ax1.plot(data.index, data['MA20'], label='MA20', alpha=0.7, color='red')
            
            # [EMOJI]
            buy_signals = data[data['signal'] == 1]
            sell_signals = data[data['signal'] == -1]
            
            ax1.scatter(buy_signals.index, buy_signals['close'], 
                       color='green', marker='^', s=100, label='[EMOJI]', zorder=5)
            ax1.scatter(sell_signals.index, sell_signals['close'], 
                       color='red', marker='v', s=100, label='[EMOJI]', zorder=5)
            
            ax1.set_title(f'{stock_code} [EMOJI]', fontsize=14)
            ax1.set_ylabel('[EMOJI] ([EMOJI])')
            ax1.legend()
            ax1.grid(True, alpha=0.3)
            
            # 2. RSI[EMOJI]
            ax2.plot(data.index, data['RSI'], color='purple', label='RSI')
            ax2.axhline(y=70, color='r', linestyle='--', alpha=0.7, label='[EMOJI](70)')
            ax2.axhline(y=30, color='g', linestyle='--', alpha=0.7, label='[EMOJI](30)')
            ax2.set_title('RSI[EMOJI]')
            ax2.set_ylabel('RSI')
            ax2.set_ylim(0, 100)
            ax2.legend()
            ax2.grid(True, alpha=0.3)
            
            # 3. MACD[EMOJI]
            ax3.plot(data.index, data['MACD'], color='blue', label='MACD')
            ax3.plot(data.index, data['MACD_signal'], color='red', label='Signal')
            ax3.bar(data.index, data['MACD_hist'], alpha=0.6, color='green', label='Histogram')
            ax3.axhline(y=0, color='black', linestyle='-', alpha=0.3)
            ax3.set_title('MACD[EMOJI]')
            ax3.set_ylabel('MACD')
            ax3.legend()
            ax3.grid(True, alpha=0.3)
            
            # 4. [EMOJI]
            if self.trade_log:
                trade_df = pd.DataFrame(self.trade_log)
                trade_df['date'] = pd.to_datetime(trade_df['date'])
                
                # [EMOJI]
                daily_trades = trade_df.groupby(trade_df['date'].dt.date)['amount'].sum()
                ax4.bar(daily_trades.index, daily_trades.values, alpha=0.7, color='skyblue')
                ax4.set_title('[EMOJI]')
                ax4.set_ylabel('[EMOJI] ([EMOJI])')
                ax4.tick_params(axis='x', rotation=45)
            else:
                ax4.text(0.5, 0.5, '[EMOJI]', ha='center', va='center', transform=ax4.transAxes)
                ax4.set_title('[EMOJI]')
            
            ax4.grid(True, alpha=0.3)
            
            plt.tight_layout()
            
            # [EMOJI]
            chart_filename = f"{self.data_dir}/{stock_code}_trading_results.png"
            plt.savefig(chart_filename, dpi=300, bbox_inches='tight')
            plt.show()
            
            print(f"[OK] [EMOJI] {chart_filename}")
            
        except Exception as e:
            print(f"[X] [EMOJI]: {e}")


class RealTradeAdapter:
    """[EMOJI]API[EMOJI] - [EMOJI]easy_xt[EMOJI]API[EMOJI]02_[EMOJI].py[EMOJI]"""

    def __init__(self):
        self.api = None
        self.connected = False
        self.account_id = None

        try:
            import json
            from pathlib import Path

            # [EMOJI]easy_xt API[EMOJI]02_[EMOJI].py[EMOJI]
            self.api = easy_xt.get_api()
            print("  [API] API[EMOJI]")

            # [EMOJI]
            project_root = Path(__file__).parent.parent
            config_path = project_root / 'config' / 'unified_config.json'

            userdata_path = None
            if config_path.exists():
                with open(config_path, 'r', encoding='utf-8') as f:
                    config = json.load(f)
                    userdata_path = config.get('settings', {}).get('account', {}).get('qmt_path')
                    self.account_id = config.get('settings', {}).get('account', {}).get('account_id')

            if not userdata_path:
                userdata_path = r'D:\[EMOJI]QMT[EMOJI]\userdata_mini'

            print(f"  [[EMOJI]] QMT[EMOJI]: {userdata_path}")
            print(f"  [[EMOJI]] [EMOJI]ID: {self.account_id}")

            # [EMOJI]
            try:
                data_success = self.api.init_data()
                if data_success:
                    print("  [[EMOJI]] [EMOJI]")
                else:
                    print("  [[EMOJI]] [EMOJI]")
            except Exception as e:
                print(f"  [[EMOJI]] [EMOJI]: {e}")

            # [EMOJI]02_[EMOJI].py[EMOJI]
            try:
                trade_success = self.api.init_trade(userdata_path, 'learning_session')
                if trade_success:
                    print("  [[EMOJI]] [EMOJI]")
                    self.connected = True
                else:
                    print("  [[EMOJI]] [EMOJI]")
                    print("  [[EMOJI]] [EMOJI]QMT[EMOJI]")
                    return
            except Exception as e:
                print(f"  [[EMOJI]] [EMOJI]: {e}")
                print("  [[EMOJI]] [EMOJI]QMT[EMOJI]")
                return

            # [EMOJI]02_[EMOJI].py[EMOJI]
            if self.account_id:
                try:
                    add_success = self.api.add_account(self.account_id, 'STOCK')
                    if add_success:
                        print(f"  [[EMOJI]] [EMOJI]: {self.account_id}")
                    else:
                        print(f"  [[EMOJI]] [EMOJI]")
                except Exception as e:
                    print(f"  [[EMOJI]] [EMOJI]: {e}")

            # [EMOJI]02_[EMOJI].py[EMOJI]
            try:
                from datetime import datetime
                now = datetime.now()
                current_hour = now.hour
                current_minute = now.minute
                current_weekday = now.weekday()

                is_weekend = current_weekday >= 5  # [EMOJI]
                morning = (9 < current_hour < 11) or (current_hour == 9 and current_minute >= 30) or (current_hour == 11 and current_minute <= 30)
                afternoon = (13 <= current_hour < 15)
                is_trading_time = morning or afternoon

                now_str = now.strftime('%Y-%m-%d %H:%M:%S')
                weekday_str = ['[EMOJI]', '[EMOJI]', '[EMOJI]', '[EMOJI]', '[EMOJI]', '[EMOJI]', '[EMOJI]'][current_weekday]
                print(f"  [[EMOJI]] {now_str} [EMOJI]{weekday_str}")

                if is_weekend:
                    print(f"  [[EMOJI]] [EMOJI]")
                elif is_trading_time:
                    print(f"  [[EMOJI]] [EMOJI]")
                else:
                    print(f"  [[EMOJI]] [EMOJI]")
                    print(f"  [[EMOJI]] [EMOJI]: [EMOJI] 9:30-11:30, 13:00-15:00")
            except Exception as e:
                print(f"  [[EMOJI]] [EMOJI]: {e}")

        except Exception as e:
            print(f"  [[EMOJI]] [EMOJI]: {e}")
            import traceback
            traceback.print_exc()

    def buy(self, stock_code, price, quantity):
        """[EMOJI]02_[EMOJI].py[EMOJI]"""
        if not self.connected or not self.api:
            print("  [[EMOJI]] [EMOJI]")
            return False

        if not self.account_id:
            print("  [[EMOJI]] [EMOJI]ID")
            return False

        try:
            print(f"  [[EMOJI]] [EMOJI] {stock_code} {quantity}[EMOJI] @ {price:.2f}[EMOJI]")

            # [EMOJI]easy_xt[EMOJI]buy[EMOJI]02_[EMOJI].py[EMOJI]
            order_id = self.api.buy(
                account_id=self.account_id,
                code=stock_code,
                volume=quantity,
                price=price,
                price_type='limit'  # [EMOJI]
            )

            if order_id:
                print(f"  [[EMOJI]] [EMOJI]: {order_id}")
                return True
            else:
                print(f"  [[EMOJI]] [EMOJI]")
                return False

        except Exception as e:
            print(f"  [[EMOJI]] [EMOJI]: {e}")
            return False

    def sell(self, stock_code, price, quantity):
        """[EMOJI]02_[EMOJI].py[EMOJI]"""
        if not self.connected or not self.api:
            print("  [[EMOJI]] [EMOJI]")
            return False

        if not self.account_id:
            print("  [[EMOJI]] [EMOJI]ID")
            return False

        try:
            print(f"  [[EMOJI]] [EMOJI] {stock_code} {quantity}[EMOJI] @ {price:.2f}[EMOJI]")

            # [EMOJI]easy_xt[EMOJI]sell[EMOJI]02_[EMOJI].py[EMOJI]
            order_id = self.api.sell(
                account_id=self.account_id,
                code=stock_code,
                volume=quantity,
                price=price,
                price_type='limit'  # [EMOJI]
            )

            if order_id:
                print(f"  [[EMOJI]] [EMOJI]: {order_id}")
                return True
            else:
                print(f"  [[EMOJI]] [EMOJI]")
                return False

        except Exception as e:
            print(f"  [[EMOJI]] [EMOJI]: {e}")
            return False


class MockTrader:
    """[EMOJI] - [EMOJI]"""

    def __init__(self):
        self.orders = []
        self.cash = 100000  # [EMOJI]
        self.position = {}  # [EMOJI]
        print("[NOTE] [EMOJI]")

    def buy(self, stock_code, price, quantity):
        """[EMOJI]"""
        # [EMOJI]
        required_cash = price * quantity
        if required_cash > self.cash:
            print(f"  [!] [EMOJI] {required_cash:.2f}[EMOJI] {self.cash:.2f}")
            return False

        # [EMOJI]
        order = {
            'stock_code': stock_code,
            'action': 'BUY',
            'price': price,
            'quantity': quantity,
            'amount': required_cash,
            'timestamp': datetime.now(),
            'status': 'filled'
        }
        self.orders.append(order)

        # [EMOJI]
        self.cash -= required_cash
        if stock_code not in self.position:
            self.position[stock_code] = {'quantity': 0, 'total_cost': 0}

        old_quantity = self.position[stock_code]['quantity']
        old_total_cost = self.position[stock_code]['total_cost']

        self.position[stock_code]['quantity'] = old_quantity + quantity
        self.position[stock_code]['total_cost'] = old_total_cost + required_cash

        return True

    def sell(self, stock_code, price, quantity):
        """[EMOJI]"""
        # [EMOJI]
        if stock_code not in self.position or self.position[stock_code]['quantity'] < quantity:
            print(f"  [!] [EMOJI] {quantity}[EMOJI] {self.position.get(stock_code, {}).get('quantity', 0)}")
            return False

        # [EMOJI]
        order = {
            'stock_code': stock_code,
            'action': 'SELL',
            'price': price,
            'quantity': quantity,
            'amount': price * quantity,
            'timestamp': datetime.now(),
            'status': 'filled'
        }
        self.orders.append(order)

        # [EMOJI]
        self.cash += price * quantity
        self.position[stock_code]['quantity'] -= quantity

        return True


def main():
    """[EMOJI] - [EMOJI]"""

    # [EMOJI]
    parser = argparse.ArgumentParser(description='[EMOJI]')
    parser.add_argument('--real-trading', action='store_true',
                       help='[EMOJI]')
    parser.add_argument('--sim-data', action='store_true',
                       help='[EMOJI]')
    parser.add_argument('--stock', type=str, default='000001',
                       help='[EMOJI]000001[EMOJI]')
    args = parser.parse_args()

    # [EMOJI]
    # [EMOJI]
    use_real_data = not args.sim_data if args.sim_data else USE_REAL_DATA
    use_real_trading = args.real_trading if args.real_trading else USE_REAL_TRADING

    print("=" * 60)
    print("[EMOJI] - [EMOJI]")
    print("=" * 60)
    print()
    print("[[EMOJI]]")
    print(f"  - [EMOJI]{'[OK] [EMOJI]' if use_real_data else '[TEST] [EMOJI]'}")
    print(f"  - [EMOJI]{'[WARNING] [EMOJI]' if use_real_trading else '[OK] [EMOJI]'}")
    print()
    if use_real_trading:
        print("  [!!!] [EMOJI] [!!!]")
        print()
    print("[[EMOJI]]")
    print("  - [EMOJI] 37-38 [EMOJI]")
    print("  - [EMOJI]python 10_[EMOJI].py --real-trading")
    print()

    # [EMOJI]
    if use_real_trading:
        print("=" * 60)
        print("[EMOJI] [EMOJI] [EMOJI]")
        print("=" * 60)
        print("[EMOJI]")
        print()
        print("[!] [EMOJI]")
        print("  1. [EMOJI]")
        print("  2. [EMOJI]")
        print("  3. [EMOJI]")
        print("  4. [EMOJI]")
        print()
        print("[EMOJI]")
        print("  - [EMOJI]")
        print("  - [EMOJI]")
        print("  - [EMOJI]")
        print()

        # [EMOJI]
        confirm = input("[EMOJI]([EMOJI] 'YES' [EMOJI]): ")
        if confirm != 'YES':
            print("[X] [EMOJI]")
            use_real_trading = False
        else:
            print("[OK] [EMOJI]")
        print("=" * 60)
        print()

    strategy = TradingStrategy(
        use_real_data=use_real_data,
        use_real_trading=use_real_trading
    )

    # [EMOJI]
    stock_code = args.stock

    print("\n" + "=" * 40)
    print("[CHART] [EMOJI]")
    print("=" * 40)

    # [EMOJI]
    data = strategy.load_sample_data(
        stock_code=stock_code,
        # start_date='20240101',  # [EMOJI]
        # end_date='20241231'     # [EMOJI]
    )
    if data.empty:
        print("[X] [EMOJI]")
        return
    
    print(f"[OK] [EMOJI] {len(data)} [EMOJI]")
    print(f"[EMOJI] [EMOJI]: {data.index[0].strftime('%Y-%m-%d')} [EMOJI] {data.index[-1].strftime('%Y-%m-%d')}")
    
    print("\n" + "=" * 40)
    print("[UP] [EMOJI]")
    print("=" * 40)
    
    # [EMOJI]
    data = strategy.calculate_indicators(data)
    
    print("\n" + "=" * 40)
    print("[TARGET] [EMOJI]")
    print("=" * 40)
    
    # [EMOJI]
    data = strategy.generate_signals(data)
    
    print("\n" + "=" * 40)
    print("[EMOJI] [EMOJI]")
    print("=" * 40)
    
    # [EMOJI]
    strategy.execute_trades(data, stock_code)
    
    print("\n" + "=" * 40)
    print("[CHART] [EMOJI]")
    print("=" * 40)
    
    # [EMOJI]
    strategy.analyze_performance()
    
    print("\n" + "=" * 40)
    print("[UP] [EMOJI]")
    print("=" * 40)
    
    # [EMOJI]
    strategy.visualize_results(data, stock_code)
    
    print("\n" + "=" * 60)
    print("[OK] [EMOJI]")
    print("[EMOJI] [EMOJI]")
    print()
    print("[CHART] [EMOJI]", "[EMOJI]" if strategy.use_real_data else "[EMOJI]")
    print("[EMOJI] [EMOJI]", "[EMOJI]" if strategy.use_real_trading else "[EMOJI]")
    print()
    print("[TIP] [EMOJI]")
    print("  1. [EMOJI] + [EMOJI]")
    print("  2. [EMOJI] + [EMOJI]")
    print("  3. [EMOJI] + [EMOJI]")
    print()
    print("[R] [EMOJI]")
    print("  - [EMOJI]")
    print("  - [EMOJI]")
    print("  - [EMOJI]")
    print("=" * 60)


if __name__ == "__main__":
    main()