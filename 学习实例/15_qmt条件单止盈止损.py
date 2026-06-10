#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
QMT[EMOJI]
[EMOJI]

[EMOJI]
1. [EMOJI]
2. [EMOJI]
3. [EMOJI]
4. [EMOJI]

[EMOJI]
1. [EMOJI]1([EMOJI])[EMOJI]A[EMOJI]B[EMOJI]C[EMOJI]
2. [EMOJI]2([EMOJI])[EMOJI]A + [EMOJI]B[EMOJI]
3. [EMOJI]3([EMOJI])[EMOJI]A, [EMOJI]B, [EMOJI]C[EMOJI]
4. [EMOJI]4([EMOJI])[EMOJI]A[EMOJI]

[EMOJI]quant
[EMOJI]2025-02-24
"""

import sys
import os
import io

# Windows[EMOJI]
if sys.platform == 'win32':
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8', errors='replace')

# [EMOJI]
project_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, project_path)

import json
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Tuple
import pandas as pd
import numpy as np

try:
    import easy_xt
    from xtquant import xtdata
    from easy_xt.utils import StockCodeUtils
    EASYXT_AVAILABLE = True
except ImportError:
    EASYXT_AVAILABLE = False
    print("[EMOJI]: easy_xt[EMOJI]easy_xt[EMOJI]")


class StopLossConditionOrderManager:
    """
    [EMOJI]
    [EMOJI]
    """

    def __init__(self):
        """[EMOJI]"""
        self.orders = []  # [EMOJI]
        self.order_counter = 0  # [EMOJI]
        self.trade_api = None  # [EMOJI]API
        self._trade_initialized = False  # [EMOJI]API[EMOJI]
        self.monitoring_active = False  # [EMOJI]

        # [EMOJI]
        self.init_trade_connection()

    def init_trade_connection(self):
        """[EMOJI]"""
        if not EASYXT_AVAILABLE:
            print("[EMOJI]: EasyXT[EMOJI]")
            return

        try:
            # [EMOJI]
            config_file = os.path.join(project_path, 'config', 'unified_config.json')
            if not os.path.exists(config_file):
                print("[EMOJI]: [EMOJI] config/unified_config.json")
                print("[EMOJI]")
                return

            with open(config_file, 'r', encoding='utf-8') as f:
                config = json.load(f)

            # [EMOJI]
            settings = config.get('settings', {})
            account_config = settings.get('account', {})

            userdata_path = account_config.get('qmt_path', '')
            account_id = account_config.get('account_id', '')

            if not userdata_path or not account_id:
                print("[EMOJI]: [EMOJI]")
                return

            print(f"[EMOJI]...")
            print(f"  QMT[EMOJI]: {userdata_path}")
            print(f"  [EMOJI]ID: {account_id}")

            # [EMOJI]API[EMOJI]
            self.trade_api = easy_xt.get_extended_api()

            # [EMOJI]
            if hasattr(self.trade_api, 'init_trade'):
                result = self.trade_api.init_trade(userdata_path)
                if result:
                    self._trade_initialized = True
                    print("[OK] [EMOJI]")
                else:
                    print("[X] [EMOJI]")
                    return

            # [EMOJI]
            account_type = 'STOCK'
            if self.trade_api.add_account(account_id, account_type):
                print(f"[OK] [EMOJI]: {account_id} ({account_type})")
            else:
                print(f"[X] [EMOJI]: {account_id}")

        except Exception as e:
            print(f"[EMOJI]: {str(e)}")

    def create_advanced_stop_loss_order(self, params: Dict) -> Optional[Dict]:
        """
        [EMOJI]

        [EMOJI]:
        - stock_code: [EMOJI]
        - cost_price: [EMOJI]
        - position_qty: [EMOJI]
        - strategy_preset: [EMOJI]/[EMOJI]/[EMOJI]
        - enabled_strategies: [EMOJI] [1,2,3,4]
        - validity_hours: [EMOJI]24[EMOJI]

        [EMOJI]:
            [EMOJI]None
        """
        try:
            # [EMOJI]
            stock_code = params.get('stock_code', '000001.SZ')
            cost_price = params.get('cost_price', 10.0)
            position_qty = params.get('position_qty', 1000)
            strategy_preset = params.get('strategy_preset', '[EMOJI]')
            enabled_strategies = params.get('enabled_strategies', [1, 2, 3, 4])
            validity_hours = params.get('validity_hours', 24)

            # [EMOJI]
            strategy_params = self._get_strategy_preset(strategy_preset)

            # [EMOJI]
            self.order_counter += 1
            order_id = f"ASL{self.order_counter:04d}"  # ASL = Advanced Stop Loss

            # [EMOJI]
            expiry_time = datetime.now() + timedelta(hours=validity_hours)

            # [EMOJI]
            order = {
                'id': order_id,
                'stock_code': stock_code,
                'cost_price': cost_price,
                'position_qty': position_qty,
                'strategy_preset': strategy_preset,
                'enabled_strategies': enabled_strategies,
                'strategy_params': strategy_params,
                'status': '[EMOJI]',
                'created_time': datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                'expiry': expiry_time.strftime("%Y-%m-%d %H:%M:%S"),

                # [EMOJI]
                'highest_price': cost_price,
                'lowest_price': cost_price,
                'highest_price_after_profit': 0.0,
                'today_open_price': None,
                'yesterday_close_price': None,
                'current_price': 0.0,

                # [EMOJI]
                'triggered_strategies': [],
                'triggered_price': None,
                'triggered_time': None,
            }

            self.orders.append(order)

            print("="*60)
            print(f"[OK] [EMOJI]: {order_id}")
            print("="*60)
            print(f"[EMOJI]: {stock_code}")
            print(f"[EMOJI]: {cost_price:.2f}[EMOJI]")
            print(f"[EMOJI]: {position_qty}[EMOJI]")
            print(f"[EMOJI]: {strategy_preset}")
            print(f"[EMOJI]: {enabled_strategies}")
            print(f"[EMOJI]: {order['expiry']}")
            print("="*60)

            return order

        except Exception as e:
            print(f"[X] [EMOJI]: {str(e)}")
            import traceback
            traceback.print_exc()
            return None

    def _get_strategy_preset(self, preset_name: str) -> Dict:
        """[EMOJI]"""
        presets = {
            '[EMOJI]': {
                's1_profit_min': 0.20, 's1_profit_max': 0.50, 's1_pullback': 0.10,
                's2_rise_threshold': 0.10, 's2_pullback': 0.05,
                's3_gap_open': 0.03, 's3_high_above_open': 0.02, 's3_pullback': 0.02,
                's4_loss_threshold': -0.05,
            },
            '[EMOJI]': {
                's1_profit_min': 0.10, 's1_profit_max': 0.20, 's1_pullback': 0.05,
                's2_rise_threshold': 0.10, 's2_pullback': 0.05,
                's3_gap_open': 0.05, 's3_high_above_open': 0.03, 's3_pullback': 0.03,
                's4_loss_threshold': -0.08,
            },
            '[EMOJI]': {
                's1_profit_min': 0.15, 's1_profit_max': 0.30, 's1_pullback': 0.08,
                's2_rise_threshold': 0.05, 's2_pullback': 0.02,
                's3_gap_open': 0.02, 's3_high_above_open': 0.015, 's3_pullback': 0.015,
                's4_loss_threshold': -0.05,
            }
        }
        return presets.get(preset_name, presets['[EMOJI]'])

    def get_current_price(self, stock_code: str) -> Optional[float]:
        """[EMOJI]"""
        if not EASYXT_AVAILABLE:
            print("[EMOJI]: EasyXT[EMOJI]")
            return None

        try:
            normalized_code = StockCodeUtils.normalize_code(stock_code)

            # [EMOJI]get_full_tick[EMOJI]
            tick_data = xtdata.get_full_tick([normalized_code])
            if tick_data and normalized_code in tick_data:
                tick_info = tick_data[normalized_code]
                if tick_info and 'lastPrice' in tick_info:
                    return float(tick_info['lastPrice'])
                elif tick_info and 'price' in tick_info:
                    return float(tick_info['price'])

            # [EMOJI]get_market_data
            current_data = xtdata.get_market_data(
                stock_list=[normalized_code],
                period='tick',
                count=1
            )

            if current_data and isinstance(current_data, dict) and normalized_code in current_data:
                data_array = current_data[normalized_code]
                if hasattr(data_array, '__len__') and len(data_array) > 0:
                    first_item = data_array[0]
                    if hasattr(first_item, 'lastPrice'):
                        return float(first_item['lastPrice'])

            return None
        except Exception as e:
            print(f"[EMOJI]{stock_code}[EMOJI]: {str(e)}")
            return None

    def check_strategies(self, order: Dict) -> List[Dict]:
        """[EMOJI]"""
        triggered_strategies = []
        current_price = order['current_price']
        cost_price = order['cost_price']
        params = order['strategy_params']
        enabled = order['enabled_strategies']

        # [EMOJI]
        order['highest_price'] = max(order['highest_price'], current_price)
        order['lowest_price'] = min(order['lowest_price'], current_price)

        # [EMOJI]1: [EMOJI]
        if 1 in enabled:
            triggered, reason = self._check_strategy1(order, current_price, cost_price, params)
            if triggered:
                triggered_strategies.append({'strategy_id': 1, 'name': '[EMOJI]', 'reason': reason})

        # [EMOJI]2: [EMOJI]
        if 2 in enabled:
            triggered, reason = self._check_strategy2(order, current_price, cost_price, params)
            if triggered:
                triggered_strategies.append({'strategy_id': 2, 'name': '[EMOJI]', 'reason': reason})

        # [EMOJI]3: [EMOJI]
        if 3 in enabled:
            triggered, reason = self._check_strategy3(order, current_price, cost_price, params)
            if triggered:
                triggered_strategies.append({'strategy_id': 3, 'name': '[EMOJI]', 'reason': reason})

        # [EMOJI]4: [EMOJI]
        if 4 in enabled:
            triggered, reason = self._check_strategy4(order, current_price, cost_price, params)
            if triggered:
                triggered_strategies.append({'strategy_id': 4, 'name': '[EMOJI]', 'reason': reason})

        return triggered_strategies

    def _check_strategy1(self, order: Dict, current_price: float, cost_price: float, params: Dict) -> Tuple[bool, str]:
        """[EMOJI]1[EMOJI]"""
        current_profit = (current_price - cost_price) / cost_price

        if current_profit < params['s1_profit_min']:
            return False, f"[EMOJI]([EMOJI]{current_profit*100:.1f}%[EMOJI]{params['s1_profit_min']*100:.0f}%)"

        if current_profit >= params['s1_profit_max']:
            return True, f"[EMOJI]{current_profit*100:.1f}%[EMOJI]{params['s1_profit_max']*100:.0f}%"

        # [EMOJI]
        if order['highest_price_after_profit'] == 0:
            order['highest_price_after_profit'] = current_price
        else:
            order['highest_price_after_profit'] = max(order['highest_price_after_profit'], current_price)

        pullback_ratio = (order['highest_price_after_profit'] - current_price) / order['highest_price_after_profit']

        if pullback_ratio >= params['s1_pullback']:
            return True, f"[EMOJI]{pullback_ratio*100:.1f}%[EMOJI]{params['s1_pullback']*100:.0f}%"

        return False, f"[EMOJI]([EMOJI]{pullback_ratio*100:.1f}%[EMOJI]{params['s1_pullback']*100:.0f}%)"

    def _check_strategy2(self, order: Dict, current_price: float, cost_price: float, params: Dict) -> Tuple[bool, str]:
        """[EMOJI]2[EMOJI]"""
        highest_price = order['highest_price']
        highest_rise = (highest_price - cost_price) / cost_price

        if highest_rise < params['s2_rise_threshold']:
            return False, f"[EMOJI]([EMOJI]{highest_rise*100:.1f}%[EMOJI]{params['s2_rise_threshold']*100:.0f}%)"

        pullback_ratio = (highest_price - current_price) / highest_price

        if pullback_ratio >= params['s2_pullback']:
            return True, f"[EMOJI]{highest_rise*100:.1f}%[EMOJI]{pullback_ratio*100:.1f}%[EMOJI]"

        return False, f"[EMOJI]([EMOJI]{pullback_ratio*100:.1f}%[EMOJI]{params['s2_pullback']*100:.0f}%)"

    def _check_strategy3(self, order: Dict, current_price: float, cost_price: float, params: Dict) -> Tuple[bool, str]:
        """[EMOJI]3[EMOJI]"""
        if order['today_open_price'] is None or order['yesterday_close_price'] is None:
            return False, "[EMOJI]"

        gap_open_ratio = (order['today_open_price'] - order['yesterday_close_price']) / order['yesterday_close_price']

        if gap_open_ratio < params['s3_gap_open']:
            return False, f"[EMOJI]([EMOJI]{gap_open_ratio*100:.1f}%[EMOJI]{params['s3_gap_open']*100:.0f}%)"

        high_above_ratio = (order['highest_price'] - order['today_open_price']) / order['today_open_price']

        if high_above_ratio < params['s3_high_above_open']:
            return False, f"[EMOJI]([EMOJI]{high_above_ratio*100:.1f}%[EMOJI]{params['s3_high_above_open']*100:.1f}%)"

        pullback_ratio = (order['highest_price'] - current_price) / order['highest_price']

        if pullback_ratio >= params['s3_pullback']:
            return True, f"[EMOJI]{gap_open_ratio*100:.1f}%[EMOJI]{pullback_ratio*100:.1f}%[EMOJI]"

        return False, f"[EMOJI]([EMOJI]{pullback_ratio*100:.1f}%[EMOJI]{params['s3_pullback']*100:.1f}%)"

    def _check_strategy4(self, order: Dict, current_price: float, cost_price: float, params: Dict) -> Tuple[bool, str]:
        """[EMOJI]4[EMOJI]"""
        profit_loss = (current_price - cost_price) / cost_price

        if profit_loss <= params['s4_loss_threshold']:
            return True, f"[EMOJI]{abs(profit_loss)*100:.1f}%[EMOJI]{abs(params['s4_loss_threshold'])*100:.0f}%"

        if profit_loss < 0:
            loss_ratio = abs(profit_loss)
            distance_to_stop = (abs(params['s4_loss_threshold']) - loss_ratio) * 100
            return False, f"[EMOJI]([EMOJI]{loss_ratio*100:.1f}%[EMOJI]{distance_to_stop:.1f}%)"

        return False, f"[EMOJI]{profit_loss*100:.1f}%"

    def execute_sell_order(self, order: Dict) -> bool:
        """[EMOJI]"""
        if not EASYXT_AVAILABLE:
            print("[EMOJI]: EasyXT[EMOJI]")
            return False

        if not self._trade_initialized or self.trade_api is None:
            print("[EMOJI]: [EMOJI]API[EMOJI]")
            return False

        try:
            stock_code = order['stock_code']
            quantity = order['position_qty']
            current_price = order['current_price']

            # [EMOJI]ID
            if not hasattr(self.trade_api, 'trade_api') or self.trade_api.trade_api is None:
                print("[EMOJI]: trade_api[EMOJI]")
                return False

            if not hasattr(self.trade_api.trade_api, 'accounts') or not self.trade_api.trade_api.accounts:
                print("[EMOJI]: [EMOJI]")
                return False

            account_id = list(self.trade_api.trade_api.accounts.keys())[0]

            # [EMOJI]
            order_id = self.trade_api.trade_api.sell(
                account_id=account_id,
                code=stock_code,
                volume=quantity,
                price=current_price,  # [EMOJI]
                price_type='limit'
            )

            if order_id:
                print(f"[OK] [EMOJI]: {stock_code} {quantity}[EMOJI] @{current_price:.2f}")
                print(f"  [EMOJI]: {order_id}")
                return True
            else:
                print(f"[X] [EMOJI]")
                return False

        except Exception as e:
            print(f"[X] [EMOJI]: {str(e)}")
            import traceback
            traceback.print_exc()
            return False

    def monitor_and_execute(self):
        """[EMOJI]"""
        if not EASYXT_AVAILABLE:
            print("[EMOJI]: EasyXT[EMOJI]")
            return

        print("\n" + "="*60)
        print("[SEARCH] [EMOJI]...")
        print("="*60)

        for order in self.orders:
            if order['status'] != '[EMOJI]':
                continue

            # [EMOJI]
            try:
                expiry_time = datetime.strptime(order['expiry'], "%Y-%m-%d %H:%M:%S")
                if datetime.now() > expiry_time:
                    order['status'] = '[EMOJI]'
                    print(f"⏰ [EMOJI]: {order['id']}")
                    continue
            except:
                pass

            # [EMOJI]
            current_price = self.get_current_price(order['stock_code'])
            if current_price is None or current_price <= 0:
                print(f"[EMOJI] [EMOJI] {order['stock_code']} [EMOJI]")
                continue

            order['current_price'] = current_price

            # [EMOJI]
            try:
                normalized_code = StockCodeUtils.normalize_code(order['stock_code'])
                tick_data = xtdata.get_full_tick([normalized_code])
                if tick_data and normalized_code in tick_data:
                    tick_info = tick_data[normalized_code]
                    if 'open' in tick_info:
                        order['today_open_price'] = float(tick_info['open'])
                    if 'lastClose' in tick_info:
                        order['yesterday_close_price'] = float(tick_info['lastClose'])
            except:
                pass

            # [EMOJI]
            triggered_strategies = self.check_strategies(order)

            # [EMOJI]
            if triggered_strategies:
                print(f"\n[EMOJI] [EMOJI]: {order['id']}")
                print(f"[EMOJI]: {order['stock_code']}")
                print(f"[EMOJI]: {current_price:.2f}[EMOJI]")
                print(f"[EMOJI]:")
                for s in triggered_strategies:
                    print(f"  - [EMOJI]{s['strategy_id']}: {s['name']}")
                    print(f"    [EMOJI]: {s['reason']}")

                # [EMOJI]
                success = self.execute_sell_order(order)

                if success:
                    order['status'] = '[EMOJI]'
                    order['triggered_price'] = current_price
                    order['triggered_time'] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                    order['triggered_strategies'] = triggered_strategies

                    profit_loss = (current_price - order['cost_price']) / order['cost_price']
                    profit_amount = (current_price - order['cost_price']) * order['position_qty']

                    print(f"[OK] [EMOJI]")
                    print(f"  [EMOJI]: {profit_loss*100:+.2f}% ({profit_amount:+.2f}[EMOJI])")
                else:
                    print(f"[X] [EMOJI]")

            else:
                # [EMOJI]
                profit_loss = (current_price - order['cost_price']) / order['cost_price']
                print(f"{order['id']} | {order['stock_code']} | [EMOJI]: {current_price:.2f} | [EMOJI]: {profit_loss*100:+.2f}%")

    def start_monitoring(self, interval_seconds: int = 5):
        """[EMOJI]"""
        import time

        self.monitoring_active = True
        print(f"\n[LAUNCH] [EMOJI]: {interval_seconds}[EMOJI]")
        print("[EMOJI] Ctrl+C [EMOJI]\n")

        try:
            while self.monitoring_active:
                self.monitor_and_execute()
                time.sleep(interval_seconds)
        except KeyboardInterrupt:
            print("\n\n⏹ [EMOJI]")
        finally:
            self.monitoring_active = False

    def list_orders(self):
        """[EMOJI]"""
        print("\n" + "="*80)
        print(f"{'ID':<8} {'[EMOJI]':<12} {'[EMOJI]':<8} {'[EMOJI]':<8} {'[EMOJI]':<12} {'[EMOJI]':<8} {'[EMOJI]'}")
        print("="*80)

        for order in self.orders:
            print(f"{order['id']:<8} {order['stock_code']:<12} {order['cost_price']:<8.2f} "
                  f"{order['position_qty']:<8} {order['strategy_preset']:<12} "
                  f"{order['status']:<8} {order['created_time']}")

            # [EMOJI]
            if order['status'] == '[EMOJI]':
                print(f"  [EMOJI] [EMOJI]: {order['triggered_time']}, [EMOJI]: {order['triggered_price']:.2f}")
                print(f"  [EMOJI] [EMOJI]: {[s['strategy_id'] for s in order['triggered_strategies']]}")

        print("="*80 + "\n")


def demo_create_orders():
    """[EMOJI]"""
    print("\n" + "="*60)
    print("[NOTE] QMT[EMOJI]")
    print("="*60)

    # [EMOJI]
    manager = StopLossConditionOrderManager()

    # [EMOJI]
    orders_config = [
        {
            'stock_code': '511090.SH',  # [EMOJI]
            'cost_price': 102.50,
            'position_qty': 1000,
            'strategy_preset': '[EMOJI]',
            'enabled_strategies': [1, 2, 3, 4],
            'validity_hours': 24,
        },
        {
            'stock_code': '000001.SZ',
            'cost_price': 10.00,
            'position_qty': 1000,
            'strategy_preset': '[EMOJI]',
            'enabled_strategies': [2, 4],  # [EMOJI]2[EMOJI]4
            'validity_hours': 48,
        },
    ]

    for config in orders_config:
        manager.create_advanced_stop_loss_order(config)

    # [EMOJI]
    manager.list_orders()

    # [EMOJI]
    print("\n" + "="*60)
    print("[TIP] [EMOJI]:")
    print("1. [EMOJI]")
    print("2. [EMOJI]")
    print("3. [EMOJI] Ctrl+C [EMOJI]")
    print("="*60)

    response = input("\n[EMOJI]? (y/n): ").lower()
    if response == 'y':
        manager.start_monitoring(interval_seconds=5)
    else:
        print("\n[EMOJI]: [EMOJI]:")
        print("  manager.start_monitoring(interval_seconds=5)")


def demo_simple_usage():
    """[EMOJI]"""
    print("\n" + "="*60)
    print("[EMOJI] [EMOJI]")
    print("="*60)

    # [EMOJI]
    manager = StopLossConditionOrderManager()

    # [EMOJI]
    order = manager.create_advanced_stop_loss_order({
        'stock_code': '511090.SH',
        'cost_price': 102.50,
        'position_qty': 1000,
        'strategy_preset': '[EMOJI]',
        'enabled_strategies': [1, 2, 3, 4],
    })

    if order:
        print("\n[OK] [EMOJI]!")
        print(f"  ID: {order['id']}")
        print(f"  [EMOJI]: {order['status']}")

        # [EMOJI]
        # manager.start_monitoring(interval_seconds=5)

    print("\n" + "="*60)
    print("[TIP] [EMOJI]:")
    print("  - [EMOJI]: manager.list_orders()")
    print("  - [EMOJI]: manager.monitor_and_execute()")
    print("  - [EMOJI]: manager.start_monitoring(interval_seconds=5)")
    print("="*60)


def main():
    """[EMOJI]"""
    import sys

    if len(sys.argv) > 1 and sys.argv[1] == 'simple':
        demo_simple_usage()
    else:
        demo_create_orders()


if __name__ == "__main__":
    main()
