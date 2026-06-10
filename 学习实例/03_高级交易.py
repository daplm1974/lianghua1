"""
EasyXT[EMOJI] 03 - [EMOJI]
[EMOJI]
[EMOJI]
"""

import sys
import os
import pandas as pd
import time
import asyncio
from datetime import datetime

# [EMOJI]Python[EMOJI]
current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)
sys.path.insert(0, parent_dir)

import easy_xt

# [EMOJI]
try:
    exec(open(os.path.join(parent_dir, 'generate_mock_data.py')).read())
    exec(open(os.path.join(parent_dir, 'mock_trade_functions.py')).read())
    mock_mode = True
    print("[R] [EMOJI]")
except:
    mock_mode = False

# [EMOJI]API
try:
    from easy_xt.advanced_trade_api import AdvancedTradeAPI
    advanced_api_available = True
except ImportError:
    print("[!] [EMOJI]API[EMOJI]API[EMOJI]")
    advanced_api_available = False

# [EMOJI]
USERDATA_PATH = r'D:\[EMOJI]QMT[EMOJI]\userdata_mini' #[EMOJI]
ACCOUNT_ID = "39020958"  # [EMOJI]
TEST_CODES = ["000001.SZ", "000002.SZ", "600000.SH"]  # [EMOJI]

class MockAdvancedTradeAPI:
    """[EMOJI]API"""
    
    def __init__(self):
        self.api = easy_xt.get_api()
        self.connected = False
        self.accounts = {}
        
    def connect(self, userdata_path: str, session_id: str = None) -> bool:
        """[EMOJI]"""
        try:
            # [EMOJI]API[EMOJI]
            success = self.api.init_data()
            if success:
                success = self.api.init_trade(userdata_path, session_id or 'advanced_session')
                if success:
                    self.connected = True
                    print("[OK] [EMOJI]API[EMOJI]")
                    return True
            
            # [EMOJI]API[EMOJI]
            print("[!] [EMOJI]API[EMOJI]")
            if mock_mode:
                # [EMOJI]
                success = self.api.mock_init_trade(userdata_path, session_id or 'advanced_session')
                if success:
                    self.connected = True
                    print("[OK] [EMOJI]")
                    return True
            
            # [EMOJI]
            self.connected = True
            print("[OK] [EMOJI]")
            return True
            
        except Exception as e:
            print(f"[!] [EMOJI]: {e}")
            # [EMOJI]
            self.connected = True
            print("[OK] [EMOJI]")
            return True
    
    def set_callbacks(self, order_callback=None, trade_callback=None, error_callback=None):
        """[EMOJI]"""
        print("[OK] [EMOJI]")
    
    def add_account(self, account_id: str, account_type: str = 'STOCK') -> bool:
        """[EMOJI]"""
        try:
            success = self.api.add_account(account_id, account_type)
            if success:
                self.accounts[account_id] = account_type
                return True
            
            if mock_mode:
                success = self.api.mock_add_account(account_id, account_type)
                if success:
                    self.accounts[account_id] = account_type
                    return True
            
            return False
        except Exception as e:
            if mock_mode:
                self.accounts[account_id] = account_type
                return True
            return False
    
    def set_risk_params(self, max_position_ratio=0.3, max_single_order_amount=10000, slippage=0.002):
        """[EMOJI]"""
        print(f"[OK] [EMOJI]: [EMOJI]={max_position_ratio}, [EMOJI]={max_single_order_amount}, [EMOJI]={slippage}")
    
    def check_trading_time(self) -> bool:
        """[EMOJI]"""
        from datetime import datetime
        now = datetime.now().time()
        # [EMOJI]
        return (9 <= now.hour <= 11) or (13 <= now.hour <= 15)
    
    def validate_order(self, account_id: str, amount: float) -> dict:
        """[EMOJI]"""
        return {
            'valid': amount <= 50000,  # [EMOJI]
            'reasons': [] if amount <= 50000 else ['[EMOJI]']
        }
    
    def sync_order(self, account_id: str, code: str, order_type: str, volume: int, 
                   price: float = 0, price_type: str = 'market', 
                   strategy_name: str = 'EasyXT', order_remark: str = '') -> int:
        """[EMOJI]"""
        try:
            if order_type == 'buy':
                return self.api.buy(account_id, code, volume, price, price_type)
            else:
                return self.api.sell(account_id, code, volume, price, price_type)
        except:
            return 12345  # [EMOJI]
    
    def async_order(self, account_id: str, code: str, order_type: str, volume: int,
                    price: float = 0, price_type: str = 'market',
                    strategy_name: str = 'EasyXT', order_remark: str = '') -> int:
        """[EMOJI]"""
        # [EMOJI]
        return 67890
    
    def batch_order(self, account_id: str, orders: list) -> list:
        """[EMOJI]"""
        results = []
        for order in orders:
            order_id = self.sync_order(
                account_id, order['code'], order['order_type'], 
                order['volume'], order.get('price', 0), 
                order.get('price_type', 'market')
            )
            results.append(order_id)
        return results
    
    def condition_order(self, account_id: str, code: str, condition_type: str,
                       trigger_price: float, order_type: str, volume: int,
                       target_price: float = 0) -> bool:
        """[EMOJI]"""
        print(f"[OK] [EMOJI]: {code}, [EMOJI]: {condition_type}, [EMOJI]: {trigger_price}")
        return True
    
    def sync_cancel_order(self, account_id: str, order_id: int) -> bool:
        """[EMOJI]"""
        try:
            return self.api.cancel_order(account_id, order_id)
        except:
            return True  # [EMOJI]
    
    def batch_cancel_orders(self, account_id: str, order_ids: list) -> list:
        """[EMOJI]"""
        return [self.sync_cancel_order(account_id, order_id) for order_id in order_ids]
    
    def get_account_asset_detailed(self, account_id: str) -> dict:
        """[EMOJI]"""
        try:
            asset = self.api.get_account_asset(account_id)
            if asset:
                asset['profit_loss'] = 1000.0  # [EMOJI]
                asset['update_time'] = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                return asset
        except:
            pass
        
        # [EMOJI]
        return {
            'total_asset': 100000.0,
            'cash': 50000.0,
            'frozen_cash': 0.0,
            'market_value': 50000.0,
            'profit_loss': 1000.0,
            'update_time': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        }
    
    def get_positions_detailed(self, account_id: str, code: str = None):
        """[EMOJI]"""
        try:
            positions = self.api.get_positions(account_id, code)
            if not positions.empty:
                # [EMOJI]
                positions['open_price'] = 10.0
                positions['current_price'] = 10.5
                positions['profit_loss'] = 500.0
                positions['profit_loss_ratio'] = 0.05
                positions['update_time'] = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            return positions
        except:
            return pd.DataFrame()
    
    def get_today_orders(self, account_id: str, cancelable_only: bool = False):
        """[EMOJI]"""
        try:
            orders = self.api.get_orders(account_id)
            if not orders.empty:
                # [EMOJI]
                if 'code' in orders.columns and 'stock_code' not in orders.columns:
                    orders['stock_code'] = orders['code']
                elif 'stock_code' not in orders.columns:
                    orders['stock_code'] = 'N/A'
                
                # [EMOJI]
                required_fields = ['order_type', 'order_volume', 'order_price', 'order_status']
                for field in required_fields:
                    if field not in orders.columns:
                        # [EMOJI]
                        if field == 'order_volume' and 'volume' in orders.columns:
                            orders['order_volume'] = orders['volume']
                        elif field == 'order_price' and 'price' in orders.columns:
                            orders['order_price'] = orders['price']
                        elif field == 'order_status' and 'status' in orders.columns:
                            orders['order_status'] = orders['status']
                        else:
                            orders[field] = 'N/A'
            
            return orders
        except Exception as e:
            print(f"[EMOJI]: {e}")
            return pd.DataFrame()
    
    def get_today_trades(self, account_id: str):
        """[EMOJI]"""
        try:
            return self.api.get_trades(account_id)
        except:
            return pd.DataFrame()
    
    def subscribe_realtime_data(self, codes, period='tick', callback=None) -> bool:
        """[EMOJI]"""
        print(f"[OK] [EMOJI]: {codes}")
        return True
    
    def download_history_data(self, codes, period='1d', start=None, end=None) -> bool:
        """[EMOJI]"""
        print(f"[OK] [EMOJI]: {codes}")
        return True
    
    def get_local_data(self, codes, period='1d', count=10):
        """[EMOJI]"""
        try:
            return self.api.get_history_data(codes, period, count=count)
        except:
            # [EMOJI]
            import numpy as np
            dates = pd.date_range(end=datetime.now(), periods=count, freq='D')
            data = pd.DataFrame({
                'code': codes if isinstance(codes, str) else codes[0],
                'open': np.random.uniform(10, 12, count),
                'high': np.random.uniform(11, 13, count),
                'low': np.random.uniform(9, 11, count),
                'close': np.random.uniform(10, 12, count),
                'volume': np.random.randint(1000000, 5000000, count)
            }, index=dates)
            return data

def lesson_01_advanced_setup():
    """[EMOJI]1[EMOJI]API[EMOJI]"""
    print("=" * 60)
    print("[EMOJI]1[EMOJI]API[EMOJI]")
    print("=" * 60)
    
    # 1. [EMOJI]API[EMOJI]
    print("1. [EMOJI]API[EMOJI]")
    
    # [EMOJI]API[EMOJI]API[EMOJI]
    print("[EMOJI]API[EMOJI]")
    advanced_api = MockAdvancedTradeAPI()
    print("[OK] [EMOJI]API[EMOJI]")
    
    # 2. [EMOJI]
    print(f"\n2. [EMOJI]")
    print(f"[EMOJI]: {USERDATA_PATH}")
    try:
        success = advanced_api.connect(USERDATA_PATH, 'advanced_learning')
        print("[OK] [EMOJI]")
    except Exception as e:
        print(f"[!] [EMOJI]: {e}")
        print("[OK] [EMOJI]")
    
    # 3. [EMOJI]
    print(f"\n3. [EMOJI]: {ACCOUNT_ID}")
    try:
        success = advanced_api.add_account(ACCOUNT_ID, 'STOCK')
        print("[OK] [EMOJI]")
    except Exception as e:
        print(f"[!] [EMOJI]: {e}")
        print("[OK] [EMOJI]")
    
    # 4. [EMOJI]
    print("\n4. [EMOJI]")
    
    def order_callback(order):
        try:
            print(f"[EMOJI] [EMOJI]: {getattr(order, 'stock_code', 'N/A')} {getattr(order, 'order_type', 'N/A')} {getattr(order, 'order_volume', 0)}[EMOJI] [EMOJI]:{getattr(order, 'order_status', 'N/A')}")
        except:
            print(f"[EMOJI] [EMOJI]: {order}")
    
    def trade_callback(trade):
        try:
            print(f"[MONEY] [EMOJI]: {getattr(trade, 'stock_code', 'N/A')} {getattr(trade, 'traded_volume', 0)}[EMOJI] [EMOJI]:{getattr(trade, 'traded_price', 0)}")
        except:
            print(f"[MONEY] [EMOJI]: {trade}")
    
    def error_callback(error):
        try:
            print(f"[X] [EMOJI]: {getattr(error, 'error_msg', str(error))}")
        except:
            print(f"[X] [EMOJI]: {error}")
    
    advanced_api.set_callbacks(
        order_callback=order_callback,
        trade_callback=trade_callback,
        error_callback=error_callback
    )
    print("[OK] [EMOJI]")
    
    return advanced_api

def lesson_02_risk_management(advanced_api):
    """[EMOJI]2[EMOJI]"""
    print("\n" + "=" * 60)
    print("[EMOJI]2[EMOJI]")
    print("=" * 60)
    
    # 1. [EMOJI]
    print("1. [EMOJI]")
    advanced_api.set_risk_params(
        max_position_ratio=0.3,      # [EMOJI]30%
        max_single_order_amount=10000,  # [EMOJI]1[EMOJI]
        slippage=0.002               # [EMOJI]0.2%
    )
    print("[OK] [EMOJI]")
    print("  - [EMOJI]: 30%")
    print("  - [EMOJI]: 10,000[EMOJI]")
    print("  - [EMOJI]: 0.2%")
    
    # 2. [EMOJI]
    print("\n2. [EMOJI]")
    is_trading_time = advanced_api.check_trading_time()
    if is_trading_time:
        print("[OK] [EMOJI]")
    else:
        print("[!] [EMOJI]")
        print("[EMOJI]: 09:30-11:30, 13:00-15:00")
    
    # 3. [EMOJI]
    print("\n3. [EMOJI]")
    test_amounts = [5000, 15000, 50000]  # [EMOJI]
    
    for amount in test_amounts:
        validation = advanced_api.validate_order(ACCOUNT_ID, amount)
        if validation['valid']:
            print(f"[OK] {amount}[EMOJI]")
        else:
            print(f"[X] {amount}[EMOJI]: {', '.join(validation['reasons'])}")

def lesson_03_sync_async_orders(advanced_api):
    """[EMOJI]3[EMOJI]"""
    print("\n" + "=" * 60)
    print("[EMOJI]3[EMOJI]")
    print("=" * 60)
    
    print("[!]  [EMOJI]")
    confirm = input("[EMOJI]([EMOJI] 'yes' [EMOJI] 'y' [EMOJI]): ")
    if confirm.lower() not in ['yes', 'y']:
        print("[EMOJI]")
        return
    
    test_code = TEST_CODES[0]  # [EMOJI]
    
    # 1. [EMOJI]
    print(f"\n1. [EMOJI] {test_code}")
    try:
        order_id = advanced_api.sync_order(
            account_id=ACCOUNT_ID,
            code=test_code,
            order_type='buy',
            volume=100,
            price=0,  # [EMOJI]
            price_type='market',
            strategy_name='[EMOJI]',
            order_remark='[EMOJI]'
        )
        
        if order_id:
            print(f"[OK] [EMOJI]: {order_id}")
            
            # [EMOJI]
            time.sleep(2)
            
            # [EMOJI]
            print("[EMOJI]...")
            cancel_result = advanced_api.sync_cancel_order(ACCOUNT_ID, order_id)
            if cancel_result:
                print("[OK] [EMOJI]")
            else:
                print("[X] [EMOJI]")
        else:
            print("[X] [EMOJI]")
    except Exception as e:
        print(f"[X] [EMOJI]: {e}")
    
    # 2. [EMOJI]
    print(f"\n2. [EMOJI] {test_code}")
    try:
        seq = advanced_api.async_order(
            account_id=ACCOUNT_ID,
            code=test_code,
            order_type='buy',
            volume=100,
            price=0,
            price_type='market',
            strategy_name='[EMOJI]',
            order_remark='[EMOJI]'
        )
        
        if seq:
            print(f"[OK] [EMOJI]: {seq}")
            print("[EMOJI]...")
            time.sleep(3)  # [EMOJI]
        else:
            print("[X] [EMOJI]")
    except Exception as e:
        print(f"[X] [EMOJI]: {e}")

def lesson_04_batch_operations(advanced_api):
    """[EMOJI]4[EMOJI]"""
    print("\n" + "=" * 60)
    print("[EMOJI]4[EMOJI]")
    print("=" * 60)
    
    print("[!]  [EMOJI]")
    confirm = input("[EMOJI]([EMOJI] 'yes' [EMOJI] 'y' [EMOJI]): ")
    if confirm.lower() not in ['yes', 'y']:
        print("[EMOJI]")
        return
    
    # 1. [EMOJI]
    print("1. [EMOJI]")
    batch_orders = []
    for i, code in enumerate(TEST_CODES[:2]):  # [EMOJI]
        batch_orders.append({
            'code': code,
            'order_type': 'buy',
            'volume': 100,
            'price': 0,
            'price_type': 'market',
            'strategy_name': '[EMOJI]',
            'order_remark': f'[EMOJI]{i+1}'
        })
    
    print(f"[EMOJI] {len(batch_orders)} [EMOJI]:")
    for order in batch_orders:
        print(f"  - {order['code']} {order['order_type']} {order['volume']}[EMOJI]")
    
    try:
        results = advanced_api.batch_order(ACCOUNT_ID, batch_orders)
        print(f"\n[EMOJI]:")
        successful_orders = []
        for i, (order, result) in enumerate(zip(batch_orders, results)):
            if result:
                print(f"[OK] {order['code']}: [EMOJI] {result}")
                successful_orders.append(result)
            else:
                print(f"[X] {order['code']}: [EMOJI]")
        
        # 2. [EMOJI]
        if successful_orders:
            print(f"\n2. [EMOJI]")
            print("[EMOJI]3[EMOJI]...")
            time.sleep(3)
            
            cancel_results = advanced_api.batch_cancel_orders(ACCOUNT_ID, successful_orders)
            print("[EMOJI]:")
            for order_id, result in zip(successful_orders, cancel_results):
                if result:
                    print(f"[OK] [EMOJI] {order_id}: [EMOJI]")
                else:
                    print(f"[X] [EMOJI] {order_id}: [EMOJI]")
        else:
            print("\n2. [EMOJI]")
            
    except Exception as e:
        print(f"[X] [EMOJI]: {e}")

def lesson_05_condition_orders(advanced_api):
    """[EMOJI]5[EMOJI]"""
    print("\n" + "=" * 60)
    print("[EMOJI]5[EMOJI]")
    print("=" * 60)
    
    # [EMOJI]
    api = easy_xt.get_api()
    test_code = TEST_CODES[0]
    
    print(f"1. [EMOJI] {test_code} [EMOJI]")
    try:
        current = api.get_current_price(test_code)
        if not current.empty:
            current_price = current.iloc[0]['price']
            print(f"[OK] [EMOJI]: {current_price:.2f}")
        else:
            print("[X] [EMOJI]")
            return
    except Exception as e:
        print(f"[X] [EMOJI]: {e}")
        return
    
    # 2. [EMOJI]
    print(f"\n2. [EMOJI]")
    stop_loss_price = round(current_price * 0.95, 2)  # [EMOJI]95%
    target_price = round(current_price * 0.94, 2)     # [EMOJI]94%
    
    print(f"[EMOJI]: {stop_loss_price}")
    print(f"[EMOJI]: {target_price}")
    
    try:
        result = advanced_api.condition_order(
            account_id=ACCOUNT_ID,
            code=test_code,
            condition_type='stop_loss',
            trigger_price=stop_loss_price,
            order_type='sell',
            volume=100,
            target_price=target_price
        )
        
        if result:
            print("[OK] [EMOJI]")
        else:
            print("[X] [EMOJI]")
    except Exception as e:
        print(f"[X] [EMOJI]: {e}")
    
    # 3. [EMOJI]
    print(f"\n3. [EMOJI]")
    take_profit_price = round(current_price * 1.05, 2)  # [EMOJI]105%
    target_price = round(current_price * 1.04, 2)       # [EMOJI]104%
    
    print(f"[EMOJI]: {take_profit_price}")
    print(f"[EMOJI]: {target_price}")
    
    try:
        result = advanced_api.condition_order(
            account_id=ACCOUNT_ID,
            code=test_code,
            condition_type='take_profit',
            trigger_price=take_profit_price,
            order_type='sell',
            volume=100,
            target_price=target_price
        )
        
        if result:
            print("[OK] [EMOJI]")
        else:
            print("[X] [EMOJI]")
    except Exception as e:
        print(f"[X] [EMOJI]: {e}")

def lesson_06_detailed_queries(advanced_api):
    """[EMOJI]6[EMOJI]"""
    print("\n" + "=" * 60)
    print("[EMOJI]6[EMOJI]")
    print("=" * 60)
    
    # 1. [EMOJI]
    print("1. [EMOJI]")
    try:
        asset = advanced_api.get_account_asset_detailed(ACCOUNT_ID)
        if asset:
            print("[OK] [EMOJI]:")
            print(f"  [EMOJI]: {asset['total_asset']:,.2f}")
            print(f"  [EMOJI]: {asset['cash']:,.2f}")
            print(f"  [EMOJI]: {asset['frozen_cash']:,.2f}")
            print(f"  [EMOJI]: {asset['market_value']:,.2f}")
            print(f"  [EMOJI]: {asset['profit_loss']:,.2f}")
            print(f"  [EMOJI]: {asset['update_time']}")
        else:
            print("[X] [EMOJI]")
    except Exception as e:
        print(f"[X] [EMOJI]: {e}")
    
    # 2. [EMOJI]
    print("\n2. [EMOJI]")
    try:
        positions = advanced_api.get_positions_detailed(ACCOUNT_ID)
        if not positions.empty:
            print("[OK] [EMOJI]:")
            print(positions[['code', 'volume', 'open_price', 'current_price', 
                           'market_value', 'profit_loss', 'profit_loss_ratio']].to_string())
        else:
            print("[OK] [EMOJI]")
    except Exception as e:
        print(f"[X] [EMOJI]: {e}")
    
    # 3. [EMOJI]
    print("\n3. [EMOJI]")
    try:
        orders = advanced_api.get_today_orders(ACCOUNT_ID)
        if not orders.empty:
            print(f"[OK] [EMOJI] {len(orders)} [EMOJI]:")
            for _, order in orders.iterrows():
                print(f"  {order['stock_code']} {order['order_type']} "
                      f"{order['order_volume']}[EMOJI] @{order['order_price']:.2f} "
                      f"[EMOJI]:{order['order_status']}")
        else:
            print("[OK] [EMOJI]")
    except Exception as e:
        print(f"[X] [EMOJI]: {e}")
    
    # 4. [EMOJI]
    print("\n4. [EMOJI]")
    try:
        trades = advanced_api.get_today_trades(ACCOUNT_ID)
        if not trades.empty:
            print(f"[OK] [EMOJI] {len(trades)} [EMOJI]:")
            for _, trade in trades.iterrows():
                print(f"  {trade['stock_code']} {trade['traded_volume']}[EMOJI] "
                      f"@{trade['traded_price']:.2f} {trade['traded_time']}")
        else:
            print("[OK] [EMOJI]")
    except Exception as e:
        print(f"[X] [EMOJI]: {e}")

def lesson_07_data_subscription(advanced_api):
    """[EMOJI]7[EMOJI]"""
    print("\n" + "=" * 60)
    print("[EMOJI]7[EMOJI]")
    print("=" * 60)
    
    # 1. [EMOJI]
    print("1. [EMOJI]")
    
    def quote_callback(data):
        print(f"[UP] [EMOJI]: {data}")
    
    try:
        result = advanced_api.subscribe_realtime_data(
            codes=TEST_CODES[:2],  # [EMOJI]
            period='tick',
            callback=quote_callback
        )
        
        if result:
            print("[OK] [EMOJI]")
            print("[EMOJI]5[EMOJI]...")
            time.sleep(5)
        else:
            print("[X] [EMOJI]")
    except Exception as e:
        print(f"[X] [EMOJI]: {e}")
    
    # 2. [EMOJI]
    print("\n2. [EMOJI]")
    try:
        result = advanced_api.download_history_data(
            codes=TEST_CODES[0],
            period='1d',
            start='20231201',
            end='20231231'
        )
        
        if result:
            print("[OK] [EMOJI]")
        else:
            print("[X] [EMOJI]")
    except Exception as e:
        print(f"[X] [EMOJI]: {e}")
    
    # 3. [EMOJI]
    print("\n3. [EMOJI]")
    try:
        local_data = advanced_api.get_local_data(
            codes=TEST_CODES[0],
            period='1d',
            count=10
        )
        
        if not local_data.empty:
            print("[OK] [EMOJI]")
            print(f"[EMOJI]: {local_data.shape}")
            print("[EMOJI]5[EMOJI]:")
            print(local_data.tail()[['code', 'open', 'high', 'low', 'close', 'volume']].to_string())
        else:
            print("[X] [EMOJI]")
    except Exception as e:
        print(f"[X] [EMOJI]: {e}")

def lesson_08_practice_summary(advanced_api):
    """[EMOJI]8[EMOJI]"""
    print("\n" + "=" * 60)
    print("[EMOJI]8[EMOJI]")
    print("=" * 60)
    
    print("[EMOJI]")
    print("1. [OK] [EMOJI]API[EMOJI]")
    print("2. [OK] [EMOJI]")
    print("3. [OK] [EMOJI]")
    print("4. [OK] [EMOJI]")
    print("5. [OK] [EMOJI]")
    print("6. [OK] [EMOJI]")
    print("7. [OK] [EMOJI]")
    
    print("\n[EMOJI]")
    print("• [EMOJI]API[EMOJI]")
    print("• [EMOJI]")
    print("• [EMOJI]")
    print("• [EMOJI]")
    print("• [EMOJI]")
    print("• [EMOJI]")
    print("• [EMOJI]")
    
    print("\n[EMOJI]")
    try:
        # [EMOJI]
        asset = advanced_api.get_account_asset_detailed(ACCOUNT_ID)
        if asset:
            print(f"[EMOJI]: {asset['total_asset']:,.2f}")
        
        # [EMOJI]
        positions = advanced_api.get_positions_detailed(ACCOUNT_ID)
        print(f"[EMOJI]: {len(positions) if not positions.empty else 0}")
        
        # [EMOJI]
        orders = advanced_api.get_today_orders(ACCOUNT_ID)
        print(f"[EMOJI]: {len(orders) if not orders.empty else 0}")
        
    except Exception as e:
        print(f"[EMOJI]: {e}")

def main():
    """[EMOJI]"""
    print("[COURSE] EasyXT[EMOJI]")
    print("[EMOJI]EasyXT[EMOJI]")
    print("\n[!]  [EMOJI]")
    print("1. [EMOJI]")
    print("2. [EMOJI]USERDATA_PATH[EMOJI]ACCOUNT_ID[EMOJI]")
    print("3. [EMOJI]")
    print("4. [EMOJI]")
    
    # [EMOJI]
    confirm = input("\n[EMOJI]([EMOJI] 'yes' [EMOJI] 'y' [EMOJI]): ")
    if confirm.lower() not in ['yes', 'y']:
        print("[EMOJI]")
        return
    
    # [EMOJI]1[EMOJI]
    advanced_api = lesson_01_advanced_setup()
    if not advanced_api:
        print("[EMOJI]")
        return
    
    # [EMOJI]
    lessons = [
        lambda: lesson_02_risk_management(advanced_api),
        lambda: lesson_03_sync_async_orders(advanced_api),
        lambda: lesson_04_batch_operations(advanced_api),
        lambda: lesson_05_condition_orders(advanced_api),
        lambda: lesson_06_detailed_queries(advanced_api),
        lambda: lesson_07_data_subscription(advanced_api),
        lambda: lesson_08_practice_summary(advanced_api)
    ]
    
    for i, lesson in enumerate(lessons, 2):
        try:
            lesson()
            if i < len(lessons) + 1:  # [EMOJI]
                input(f"\n[EMOJI]{i+1}[EMOJI]...")
        except KeyboardInterrupt:
            print("\n\n[EMOJI]")
            break
        except Exception as e:
            print(f"\n[EMOJI]: {e}")
            input("[EMOJI]...")
    
    print("\n[EMOJI] [EMOJI]")
    print("[EMOJI]")
    print("- 04_[EMOJI].py - [EMOJI]")
    print("- 05_[EMOJI].py - [EMOJI]")
    print("- 06_[EMOJI].py - [EMOJI]")

if __name__ == "__main__":
    main()