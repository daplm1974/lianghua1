"""
[EMOJI] - EasyXT[EMOJI]
[EMOJI] + EasyXT[EMOJI]

[EMOJI]
1. [EMOJI]K[EMOJI]
2. [EMOJI]
3. EasyXT[EMOJI]
4. EasyXT[EMOJI]
5. [EMOJI]
6. [EMOJI]
7. [EMOJI] + [EMOJI]

[EMOJI]quant
[EMOJI]2025-01-30
[EMOJI]2025-02-03[EMOJI]5[EMOJI]
"""

import sys
from pathlib import Path

# [EMOJI]
project_root = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(project_root))

import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import warnings
warnings.filterwarnings('ignore')

# ==================== [EMOJI] ====================
try:
    from easy_xt.config import config

    # [EMOJI]QMT userdata[EMOJI]
    QMT_PATH = config.get_userdata_path()

    # [EMOJI]ID[EMOJI]
    ACCOUNT_ID = config.get('settings.account.account_id', default='39020958')

    # [EMOJI]
    MAX_POSITION_RATIO = config.get('settings.risk.max_total_exposure', default=0.8)
    STOP_LOSS_RATIO = config.get('settings.risk.stop_loss_ratio', default=0.05)

    # [EMOJI]QMT[EMOJI]
    if not QMT_PATH:
        qmt_path_from_config = config.get('settings.account.qmt_path')
        if qmt_path_from_config:
            config.set_qmt_path(qmt_path_from_config)
            QMT_PATH = config.get_userdata_path()

    print(f"[OK] [EMOJI]")
    print(f"  QMT userdata[EMOJI]: {QMT_PATH}")
    print(f"  [EMOJI]ID: {ACCOUNT_ID}")
    print(f"  [EMOJI]: {MAX_POSITION_RATIO}")
    print(f"  [EMOJI]: {STOP_LOSS_RATIO}")
    print()

except Exception as e:
    # [EMOJI]
    print(f"[WARN] [EMOJI]: {e}")

    QMT_PATH = r'D:\[EMOJI]QMT[EMOJI]\userdata_mini'
    ACCOUNT_ID = '39020958'
    MAX_POSITION_RATIO = 0.8
    STOP_LOSS_RATIO = 0.05

STOCK_POOL = {
    '[EMOJI]': ['605168.SH', '000333.SZ', '600519.SH'],
    '[EMOJI]': ['300059.SZ', '300015.SZ', '002475.SZ'],
    '[EMOJI]': ['000063.SZ', '002230.SZ', '600036.SH'],
}


# ==================== [EMOJI] ====================

class TdxEasyXTSystem:
    """[EMOJI] + EasyXT[EMOJI]"""

    def __init__(self):
        """[EMOJI]"""
        print("[OK] [EMOJI]+EasyXT[EMOJI]...")

        # [EMOJI]
        self.init_tdx_data()

        # [EMOJI]
        self.init_easyxt_trading()

        # [EMOJI]
        self.data_cache = {}
        self.signal_history = []

        print("[OK] [EMOJI]\n")

    def init_tdx_data(self):
        """[EMOJI]"""
        print("[DATA] [EMOJI]...")

        try:
            from easy_xt.tdx_client import TdxClient

            # [EMOJI]
            with TdxClient() as client:
                test_df = client.get_market_data(
                    stock_list=['605168.SH'],
                    start_time='20250101',
                    period='1d',
                    count=5
                )

                if not test_df.empty:
                    print(f"[OK] [EMOJI]")
                    print(f"  [EMOJI]: {len(test_df)} [EMOJI]")
                else:
                    print("[WARN]  [EMOJI]")

            self.tdx_available = True

        except Exception as e:
            print(f"[ERROR] [EMOJI]: {e}")
            print("[TIP] [EMOJI]:")
            print("  1. [EMOJI]")
            print("  2. PYPlugins/user[EMOJI]")
            self.tdx_available = False

    def init_easyxt_trading(self):
        """[EMOJI]EasyXT[EMOJI]"""
        print("[TRADE] [EMOJI]EasyXT[EMOJI]...")

        try:
            from easy_xt.api import EasyXT

            # 1. [EMOJI]EasyXT[EMOJI]
            self.trader = EasyXT()

            # 2. [EMOJI]QMT[EMOJI]
            success = self.trader.init_trade(
                userdata_path=QMT_PATH,
                session_id=ACCOUNT_ID
            )

            if not success:
                raise Exception("[EMOJI]")

            # 3. [EMOJI]
            self.trader.add_account(ACCOUNT_ID)

            print("[OK] EasyXT[EMOJI]")
            self.trading_available = True

        except Exception as e:
            print(f"[ERROR] EasyXT[EMOJI]: {e}")
            print("[TIP] [EMOJI]:")
            print("  1. QMT[EMOJI]")
            print("  2. [EMOJI]qmt_path[EMOJI]")
            self.trading_available = False

    # ==================== [EMOJI] ====================

    def get_market_data(self, stock_list, start_time, end_time="", period='1d'):
        """
        [EMOJI]

        Args:
            stock_list: [EMOJI] ['605168.SH', '000333.SZ']
            start_time: [EMOJI] '20250101'
            end_time: [EMOJI] '20250131'
            period: [EMOJI] '1d'=[EMOJI] '1wk'=[EMOJI] '1min'=[EMOJI]

        Returns:
            pd.DataFrame: [EMOJI]
        """
        if not self.tdx_available:
            print("[ERROR] [EMOJI]")
            return pd.DataFrame()

        try:
            from easy_xt.tdx_client import TdxClient

            with TdxClient() as client:
                df = client.get_market_data(
                    stock_list=stock_list,
                    start_time=start_time,
                    end_time=end_time,
                    period=period,
                    dividend_type='front'  # [EMOJI]
                )

                return df

        except Exception as e:
            print(f"[ERROR] [EMOJI]: {e}")
            return pd.DataFrame()

    def get_financial_data(self, stock_list, field_list, start_time=None, end_time=None):
        """
        [EMOJI]
        [WARN] [EMOJI]

        Args:
            stock_list: [EMOJI]
            field_list: [EMOJI] ['[EMOJI]', '[EMOJI]', '[EMOJI]']
            start_time: [EMOJI]
            end_time: [EMOJI]

        Returns:
            pd.DataFrame: [EMOJI]
        """
        if not self.tdx_available:
            print("[ERROR] [EMOJI]")
            return pd.DataFrame()

        print("[WARN]  [EMOJI]")
        print("[TIP] [EMOJI]")

        try:
            from easy_xt.tdx_client import TdxClient

            with TdxClient() as client:
                df = client.get_financial_data(
                    stock_list=stock_list,
                    field_list=field_list,
                    start_time=start_time,
                    end_time=end_time,
                    report_type='report_time'
                )

                return df

        except Exception as e:
            error_msg = str(e)
            if '[EMOJI]' in error_msg or '[EMOJI]' in error_msg:
                print("[ERROR] [EMOJI]")
                print("[TIP] [EMOJI]:")
                print("   1. [EMOJI]")
                print("   2. [EMOJI]akshare[EMOJI]")
            else:
                print(f"[ERROR] [EMOJI]: {e}")

            return pd.DataFrame()

    # ==================== [EMOJI] ====================

    def calculate_indicators(self, df):
        """
        [EMOJI]

        Args:
            df: [EMOJI]DataFrame

        Returns:
            pd.DataFrame: [EMOJI]
        """
        data = df.copy()

        # [EMOJI]
        data['MA5'] = data['close'].rolling(window=5).mean()
        data['MA10'] = data['close'].rolling(window=10).mean()
        data['MA20'] = data['close'].rolling(window=20).mean()
        data['MA60'] = data['close'].rolling(window=60).mean()

        # MACD
        exp12 = data['close'].ewm(span=12, adjust=False).mean()
        exp26 = data['close'].ewm(span=26, adjust=False).mean()
        data['MACD'] = exp12 - exp26
        data['MACD_SIGNAL'] = data['MACD'].ewm(span=9, adjust=False).mean()
        data['MACD_HIST'] = data['MACD'] - data['MACD_SIGNAL']

        # RSI
        delta = data['close'].diff()
        gain = (delta.where(delta > 0, 0)).rolling(window=14).mean()
        loss = (-delta.where(delta < 0, 0)).rolling(window=14).mean()
        data['RSI'] = 100 - (100 / (1 + gain / loss))

        # [EMOJI]
        data['BB_MIDDLE'] = data['close'].rolling(window=20).mean()
        bb_std = data['close'].rolling(window=20).std()
        data['BB_UPPER'] = data['BB_MIDDLE'] + (bb_std * 2)
        data['BB_LOWER'] = data['BB_MIDDLE'] - (bb_std * 2)

        # [EMOJI]
        data['VOL_MA5'] = data['volume'].rolling(window=5).mean()
        data['VOL_MA10'] = data['volume'].rolling(window=10).mean()

        return data

    # ==================== [EMOJI] ====================

    def generate_signal(self, symbol, data):
        """
        [EMOJI]

        Args:
            symbol: [EMOJI]
            data: [EMOJI]

        Returns:
            dict: [EMOJI]
        """
        if len(data) < 20:
            return None

        latest = data.iloc[-1]
        prev = data.iloc[-2]

        signals = []

        # [EMOJI]1: MA[EMOJI]/[EMOJI]
        if latest['MA5'] > latest['MA20'] and prev['MA5'] <= prev['MA20']:
            signals.append(('MA[EMOJI]', 0.3))
        elif latest['MA5'] < latest['MA20'] and prev['MA5'] >= prev['MA20']:
            signals.append(('MA[EMOJI]', -0.3))

        # [EMOJI]2: MACD[EMOJI]/[EMOJI]
        if latest['MACD'] > latest['MACD_SIGNAL'] and prev['MACD'] <= prev['MACD_SIGNAL']:
            signals.append(('MACD[EMOJI]', 0.25))
        elif latest['MACD'] < latest['MACD_SIGNAL'] and prev['MACD'] >= prev['MACD_SIGNAL']:
            signals.append(('MACD[EMOJI]', -0.25))

        # [EMOJI]3: RSI[EMOJI]
        if latest['RSI'] < 30:
            signals.append(('RSI[EMOJI]', 0.2))
        elif latest['RSI'] > 70:
            signals.append(('RSI[EMOJI]', -0.2))

        # [EMOJI]4: [EMOJI]
        if latest['close'] < latest['BB_LOWER']:
            signals.append(('[EMOJI]', 0.15))
        elif latest['close'] > latest['BB_UPPER']:
            signals.append(('[EMOJI]', -0.15))

        # [EMOJI]
        strength = sum(s[1] for s in signals) if signals else 0

        # [EMOJI]
        signal_type = 'HOLD'
        if strength > 0.3:
            signal_type = 'BUY'
        elif strength < -0.3:
            signal_type = 'SELL'

        # [EMOJI]
        confidence = min(95, max(5, 50 + abs(strength) * 40))

        return {
            'symbol': symbol,
            'signal_type': signal_type,
            'strength': strength,
            'confidence': confidence,
            'reasons': [s[0] for s in signals],
            'price': latest['close'],
            'time': datetime.now()
        }

    # ==================== [EMOJI] ====================

    def execute_trade(self, signal):
        """
        [EMOJI]

        Args:
            signal: [EMOJI]

        Returns:
            dict: [EMOJI]
        """
        if not self.trading_available:
            print("[ERROR] [EMOJI]")
            return {'status': 'failed', 'message': '[EMOJI]'}

        if signal['signal_type'] == 'HOLD':
            return {'status': 'skipped', 'message': '[EMOJI]'}

        # [EMOJI]
        try:
            account = self.trader.get_account_asset(ACCOUNT_ID)

            print(f"\n[TRADE] [EMOJI]:")
            print(f"  [EMOJI]: {account.get('total_asset', 0):,.2f}")
            print(f"  [EMOJI]: {account.get('cash', 0):,.2f}")
            print(f"  [EMOJI]: {account.get('market_value', 0):,.2f}")

        except Exception as e:
            print(f"[ERROR] [EMOJI]: {e}")
            return {'status': 'failed', 'message': '[EMOJI]'}

        # [EMOJI]
        if signal['signal_type'] == 'BUY':
            return self._execute_buy(signal)

        # [EMOJI]
        elif signal['signal_type'] == 'SELL':
            return self._execute_sell(signal)

    def _execute_buy(self, signal):
        """[EMOJI]"""
        cash = self.trader.get_account_asset(ACCOUNT_ID).get('cash', 0)

        # [EMOJI]30%[EMOJI]
        trade_amount = cash * 0.3
        price = signal['price']
        quantity = int(trade_amount / price) // 100 * 100

        if quantity < 100:
            return {'status': 'skipped', 'message': '[EMOJI]'}

        print(f"\n[UP] [EMOJI]: {signal['symbol']}")
        print(f"  [EMOJI]: {signal['strength']:.2f}")
        print(f"  [EMOJI]: {signal['confidence']:.1f}%")
        print(f"  [EMOJI]: {', '.join(signal['reasons'])}")
        print(f"  [EMOJI]: {quantity} [EMOJI]")
        print(f"  [EMOJI]: {price:.2f}")

        # [EMOJI]
        # result = self.trader.order_stock(
        #     account_id=ACCOUNT_ID,
        #     stock_code=signal['symbol'],
        #     order_type='buy',
        #     order_volume=quantity,
        #     price_type='limit',
        #     price=price
        # )

        # print(f"[OK] [EMOJI]")

        return {'status': 'success', 'message': f'[EMOJI] {quantity} [EMOJI]'}

    def _execute_sell(self, signal):
        """[EMOJI]"""
        try:
            positions = self.trader.get_positions(
                ACCOUNT_ID,
                signal['symbol']
            )

            if positions.empty:
                return {'status': 'skipped', 'message': '[EMOJI]'}

            position = positions.iloc[0]
            can_sell = position.get('can_use_volume', 0)

            if can_sell < 100:
                return {'status': 'skipped', 'message': '[EMOJI]'}

            # [EMOJI]
            sell_ratio = min(0.5, abs(signal['strength']))
            quantity = int(can_sell * sell_ratio) // 100 * 100

            print(f"\n[DOWN] [EMOJI]: {signal['symbol']}")
            print(f"  [EMOJI]: {can_sell} [EMOJI]")
            print(f"  [EMOJI]: {quantity} [EMOJI]")
            print(f"  [EMOJI]: {signal['strength']:.2f}")
            print(f"  [EMOJI]: {', '.join(signal['reasons'])}")

            # [EMOJI]
            # result = self.trader.order_stock(
            #     account_id=ACCOUNT_ID,
            #     stock_code=signal['symbol'],
            #     order_type='sell',
            #     order_volume=quantity,
            #     price_type='limit',
            #     price=signal['price']
            # )

            return {'status': 'success', 'message': f'[EMOJI] {quantity} [EMOJI]'}

        except Exception as e:
            return {'status': 'failed', 'message': f'[EMOJI]: {e}'}


# ==================== [EMOJI] ====================

def main():
    """[EMOJI]"""
    print("="*70)
    print("  [EMOJI] + EasyXT[EMOJI] [EMOJI]")
    print("="*70)
    print(f"  [EMOJI]: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")

    # [EMOJI]
    system = TdxEasyXTSystem()

    # [EMOJI]1: [EMOJI]
    print("="*70)
    print("  [EMOJI]1[EMOJI]")
    print("="*70)

    stocks = ['605168.SH', '000333.SZ']
    print(f"[UP] [EMOJI]: {stocks}\n")

    market_data = system.get_market_data(
        stock_list=stocks,
        start_time='20250101',
        period='1d'
    )

    if not market_data.empty:
        print(f"[OK] [EMOJI]")
        print(f"  [EMOJI]: {market_data.shape}")
        print(f"  [EMOJI]: {market_data.columns.tolist()}")
        print(f"\n  [EMOJI]:")
        print(market_data.tail(5).to_string())
    else:
        print("[ERROR] [EMOJI]")

    # [EMOJI]2: [EMOJI]
    print("\n" + "="*70)
    print("  [EMOJI]2[EMOJI]")
    print("="*70)

    if not market_data.empty:
        # [EMOJI]1: [EMOJI]
        print("\n[[EMOJI]1] [EMOJI]")
        print("-"*70)

        print(f"  [EMOJI]: {len(stocks)}")
        print(f"  [EMOJI]: {market_data.shape}")
        print(f"  [EMOJI]: {market_data.columns.tolist()}")
        print(f"\n  [EMOJI]:")

        for _, row in market_data.iterrows():
            symbol = row['Symbol']
            close = row['Close']  # [EMOJI]
            high = row['High']
            low = row['Low']
            volume = row['Volume']
            amount = row['Amount']
            print(f"    {symbol}: [EMOJI] {close:.2f}, [EMOJI] {high:.2f}, [EMOJI] {low:.2f}, [EMOJI] {volume:,.0f}, [EMOJI] {amount:,.0f}")

        # [EMOJI]2: [EMOJI]
        print("\n\n[[EMOJI]2] [EMOJI]")
        print("-"*70)

        test_stock = '605168.SH'

        # [EMOJI]
        from easy_xt.tdx_client import TdxClient

        with TdxClient() as client:
            try:
                # [EMOJI]
                historical_data = client.get_market_data(
                    stock_list=[test_stock],
                    start_time='20250101',
                    period='1d'
                )

                if not historical_data.empty:
                    print(f"\n  {test_stock} [EMOJI]:")
                    print(f"  [EMOJI]: {len(historical_data)}")

                    # [EMOJI]
                    print(f"\n  [EMOJI]:")
                    print(f"    [EMOJI]: {historical_data['High'].max():.2f}")
                    print(f"    [EMOJI]: {historical_data['Low'].min():.2f}")
                    print(f"    [EMOJI]: {historical_data['Close'].mean():.2f}")
                    print(f"    [EMOJI]: {historical_data['Close'].iloc[-1]:.2f}")
                    print(f"    [EMOJI]: {historical_data['Volume'].sum():,.0f}")

                    # [EMOJI]
                    if len(historical_data) >= 3:
                        historical_data['MA3'] = historical_data['Close'].rolling(window=3).mean()
                        latest_ma3 = historical_data['MA3'].iloc[-1]
                        print(f"\n  [EMOJI]:")
                        print(f"    3[EMOJI]: {latest_ma3:.2f}")
                        print(f"    [EMOJI]: {'[EMOJI]' if historical_data['Close'].iloc[-1] > historical_data['Close'].iloc[0] else '[EMOJI]'}")
                else:
                    print(f"  [[EMOJI]] [EMOJI]")

            except Exception as e:
                print(f"  [ERROR] [EMOJI]: {e}")

        # [EMOJI]3: [EMOJI]
        print("\n\n[[EMOJI]3] [EMOJI]")
        print("-"*70)

        print(f"\n  [EMOJI]:")
        print(f"  {'[EMOJI]':12} {'[EMOJI]':>10} {'[EMOJI]':>10} {'[EMOJI]':>15}")
        print(f"  {'-'*12} {'-'*10} {'-'*10} {'-'*15}")

        for symbol in stocks:
            symbol_data = market_data[market_data['Symbol'] == symbol]
            if not symbol_data.empty:
                row = symbol_data.iloc[0]
                close = row['Close']
                open_price = row['Open']
                amount = row['Amount']
                change = close - open_price
                change_pct = (change / open_price) * 100

                print(f"  {symbol:12} {close:>10.2f} {change_pct:>9.2f}% {amount:>15,.2f}")

        # [EMOJI]4: [EMOJI]API[EMOJI]
        print("\n\n[[EMOJI]4] [EMOJI]API[EMOJI]")
        print("-"*70)

        with TdxClient() as client:
            print(f"\n  [INFO] [EMOJI]API[EMOJI]:")
            print(f"    - [EMOJI]: [EMOJI]PYPlugins/user")
            print(f"    - [EMOJI]: [EMOJI](1d)[EMOJI](1wk)[EMOJI](1m)")
            print(f"    - [EMOJI]: [EMOJI](none)[EMOJI](front)[EMOJI](back)")
            print(f"    - [EMOJI]: Open, High, Low, Close, Volume, Amount")
            print(f"    - [EMOJI]: [EMOJI]DataFrame[EMOJI]")
            print(f"\n  [TIP] [EMOJI]:")
            print(f"    data = client.get_market_data(")
            print(f"        stock_list=['000001.SZ'],")
            print(f"        start_time='20240101',  # [EMOJI]")
            print(f"        period='1d',")
            print(f"        dividend_type='front'  # [EMOJI]")
            print(f"    )")

        print("\n[INFO] [EMOJI]!")
        print("  [EMOJI]")
        print("  [EMOJI]K[EMOJI]")
        print("  [EMOJI]")
        print("  [EMOJI]DataFrame[EMOJI]")

    # [EMOJI]3: [EMOJI]
    print("\n" + "="*70)
    print("  [EMOJI]3[EMOJI]")
    print("="*70)

    print("[WARN]  [EMOJI]")
    print("[TIP] [EMOJI]:")
    print("""
    financial_data = system.get_financial_data(
        stock_list=['000001.SZ'],
        field_list=['[EMOJI]', '[EMOJI]', '[EMOJI]',
                    '[EMOJI]', '[EMOJI]', '[EMOJI]'],
        start_time='20230101',
        end_time='20241231'
    )
    """)

    # [EMOJI]
    fin_data = system.get_financial_data(
        stock_list=['000001.SZ'],
        field_list=['[EMOJI]', '[EMOJI]'],
    )

    if not fin_data.empty:
        print(f"\n[OK] [EMOJI]!")
        print(f"  [EMOJI]: {fin_data.shape}")
        print(f"\n  [EMOJI]:")
        print(fin_data.head())
    else:
        print(f"\n[ERROR] [EMOJI]")

    # [EMOJI]4: [EMOJI] + EasyXT [EMOJI]
    print("\n" + "="*70)
    print("  [EMOJI]4[EMOJI] + EasyXT[EMOJI]")
    print("="*70)

    print("\n[[EMOJI]]")
    print("  [EMOJI]")
    print("\n[[EMOJI]]")
    print("  1. [EMOJI]F6[EMOJI]")
    print("  2. [EMOJI]: python tools/parse_tdx_zixg.py")
    print("  3. [EMOJI]: my_favorites.txt")
    print("  4. [EMOJI]")
    print("\n[[EMOJI]]")
    print("  1. [EMOJI]")
    print("  2. [EMOJI]")
    print("  3. [EMOJI]")
    print("  4. [EMOJI]")
    print("\n[[EMOJI]]")
    print("  [EMOJI]: python tools/parse_tdx_zixg.py")
    print("  [EMOJI]: my_favorites.txt")

    from easy_xt.tdx_client import TdxClient

    with TdxClient() as client:
        # ============================================================
        # [EMOJI]1: [EMOJI]
        # ============================================================
        print("\n" + "="*70)
        print("  [EMOJI]1[EMOJI]")
        print("="*70)

        print("\n[[EMOJI]1] [EMOJI]")
        print("-"*70)

        print("""
  [EMOJI]:
  [EMOJI]
  [EMOJI] 1. [EMOJI] -> [EMOJI] -> [EMOJI]Ctrl+T[EMOJI]  [EMOJI]
  [EMOJI] 2. [EMOJI]:                               [EMOJI]
  [EMOJI]    - [EMOJI]: MACD[EMOJI]KDJ[EMOJI]RSI[EMOJI]         [EMOJI]
  [EMOJI]    - K[EMOJI]: [EMOJI]              [EMOJI]
  [EMOJI]    - [EMOJI]: ROE[EMOJI]PE[EMOJI]PB[EMOJI]                    [EMOJI]
  [EMOJI] 3. [EMOJI]"[EMOJI]"                              [EMOJI]
  [EMOJI] 4. [EMOJI] -> "[EMOJI]" -> "[EMOJI]"  [EMOJI]
  [EMOJI] 5. [EMOJI]'[EMOJI]'[EMOJI]'CSBK'[EMOJI]         [EMOJI]
  [EMOJI] 6. [EMOJI]                                    [EMOJI]
  [EMOJI]

  [EMOJI]:
  - MACD[EMOJI]: CROSS(MACD.DIF, MACD.DEA)
  - KDJ[EMOJI]: CROSS(KDJ.K, KDJ.D)
  - RSI[EMOJI]: RSI.RSI1(6, 12, 24) < 20
  - [EMOJI]: MA5 > MA10 > MA20 > MA60
  - [EMOJI]: CLOSE/REF(CLOSE,1) > 1.03 AND VOL/REF(VOL,1) > 1.5
        """)

        print("\n[[EMOJI]2] [EMOJI]")
        print("-"*70)

        # [EMOJI]A: [EMOJI]
        print("\n  [[EMOJI]A] [EMOJI]")
        print("  " + "-"*66)

        stock_list = []
        favorites_file = Path(__file__).parent.parent / "my_favorites.txt"

        if favorites_file.exists():
            try:
                with open(favorites_file, 'r', encoding='utf-8') as f:
                    stock_list = [line.strip() for line in f if line.strip()]

                if stock_list:
                    print(f"\n  [OK] [EMOJI]")
                    print(f"  [EMOJI]: {favorites_file}")
                    print(f"  [EMOJI]: {len(stock_list)}")
                    print(f"  [EMOJI]: {stock_list[:5]}")

                    if len(stock_list) > 5:
                        print(f"             ... [EMOJI] {len(stock_list) - 5} [EMOJI]")
                else:
                    print(f"\n  [WARN] [EMOJI]")
                    stock_list = []

            except Exception as e:
                print(f"\n  [ERROR] [EMOJI]: {e}")
                stock_list = []
        else:
            print(f"\n  [INFO] [EMOJI]: {favorites_file}")
            print(f"  [TIP] [EMOJI]:")
            print(f"        python tools/parse_tdx_zixg.py")

        # [EMOJI]B: [EMOJI]
        if not stock_list:
            print("\n  [[EMOJI]B] [EMOJI]")
            print("  " + "-"*66)

            # [EMOJI]
            sector_examples = {
                '[EMOJI]': '[EMOJI]',
                'CSBK': '[EMOJI]',
                '[EMOJI]300': '[EMOJI]300[EMOJI]',
                '[EMOJI]500': '[EMOJI]500[EMOJI]',
            }

            print("\n  [EMOJI]:")
            for name, desc in sector_examples.items():
                print(f"    - {name:12} : {desc}")

            # [EMOJI]
            sector_name = '[EMOJI]'
            print(f"\n  [EMOJI]: {sector_name}")

            try:
                # [EMOJI]
                sector_stocks = client.get_sector_stocks(sector_name, block_type=1)

                if sector_stocks and len(sector_stocks) > 0:
                    print(f"\n  [OK] [EMOJI] '{sector_name}' [EMOJI]")
                    print(f"  [EMOJI]: {len(sector_stocks)}")
                    print(f"  [EMOJI]: {sector_stocks}")
                    stock_list = sector_stocks
                else:
                    print(f"\n  [WARN] [EMOJI] '{sector_name}' [EMOJI]")

            except Exception as e:
                print(f"\n  [ERROR] [EMOJI]: {e}")

        # [EMOJI]C: [EMOJI]
        if not stock_list:
            print("\n  [[EMOJI]C] [EMOJI]")
            print("  " + "-"*66)
            stock_list = ['605168.SH', '000333.SZ', '600519.SH']
            print(f"\n  [INFO] [EMOJI]: {stock_list}")

        print(f"\n  [[EMOJI]] [EMOJI]: {len(stock_list)} [EMOJI]")

        # ============================================================
        # [EMOJI]2: [EMOJI]
        # ============================================================
        print("\n" + "="*70)
        print("  [EMOJI]2[EMOJI]")
        print("="*70)

        print("\n[[EMOJI]1] [EMOJI]")
        print("-"*70)

        # [EMOJI]
        print(f"  [EMOJI]: {len(stock_list)} [EMOJI]")

        try:
            # [EMOJI]
            all_stock_data = client.get_market_data(
                stock_list=stock_list,
                start_time='20250101',
                period='1d'
            )

            print(f"  [OK] [EMOJI]: {len(all_stock_data)} [EMOJI]")

        except Exception as e:
            print(f"  [ERROR] [EMOJI]: {e}")
            all_stock_data = None

        # [EMOJI]2: [EMOJI]
        print("\n[[EMOJI]2] [EMOJI]")
        print("-"*70)

        selected_stocks = []

        if all_stock_data is not None and not all_stock_data.empty:
            print("\n  [EMOJI]:")
            print("    1. [EMOJI] > [EMOJI]")
            print("    2. [EMOJI] > 100[EMOJI]")
            print("    3. [EMOJI] > MA20[EMOJI]")

            for symbol in stock_list:
                try:
                    # [EMOJI]
                    hist_data = client.get_market_data(
                        stock_list=[symbol],
                        start_time='20240101',  # [EMOJI]
                        period='1d'
                    )

                    if hist_data is None or hist_data.empty:
                        continue

                    # [EMOJI]
                    hist_data['MA20'] = hist_data['Close'].rolling(window=20).mean()
                    latest = hist_data.iloc[-1]

                    # [EMOJI]
                    conditions = []
                    condition_desc = []

                    # [EMOJI]1: [EMOJI]
                    is_red = latest['Close'] > latest['Open']
                    conditions.append(is_red)
                    if is_red:
                        condition_desc.append("[EMOJI]")

                    # [EMOJI]2: [EMOJI]
                    volume_ok = latest['Volume'] > 1000000
                    conditions.append(volume_ok)
                    if volume_ok:
                        condition_desc.append("[EMOJI]")

                    # [EMOJI]3: [EMOJI]
                    if len(hist_data) >= 20 and not pd.isna(latest['MA20']):
                        trend_up = latest['Close'] > latest['MA20']
                        conditions.append(trend_up)
                        if trend_up:
                            condition_desc.append("[EMOJI]")

                    # [EMOJI]
                    if all(conditions) and len(condition_desc) >= 2:
                        selected_stocks.append({
                            'symbol': symbol,
                            'close': latest['Close'],
                            'volume': latest['Volume'],
                            'change': ((latest['Close'] - latest['Open']) / latest['Open']) * 100,
                            'reasons': ', '.join(condition_desc)
                        })

                except Exception as e:
                    print(f"    {symbol}: [EMOJI] - {e}")

            # [EMOJI]
            print(f"\n  [[EMOJI]]")
            if selected_stocks:
                print(f"    [EMOJI]: {len(selected_stocks)} [EMOJI]")

                for stock in selected_stocks:
                    print(f"    - {stock['symbol']}: "
                          f"{stock['close']:.2f} ({stock['change']:+.2f}%) - "
                          f"{stock['reasons']}")
            else:
                print(f"    [INFO] [EMOJI]")

        # ============================================================
        # [EMOJI]
        # ============================================================
        print("\n" + "="*70)
        print("  [EMOJI]")
        print("="*70)

        print("\n[[EMOJI]] [EMOJI]")
        print("="*70)
        print(f"  [[EMOJI]] [EMOJI]")
        print(f"  [[EMOJI]]")
        print(f"    1. QMT[EMOJI]")
        print(f"    2. [EMOJI]ID: {ACCOUNT_ID}")
        print(f"    3. [EMOJI]: {len(stock_list)} [EMOJI]")
        print(f"    4. [EMOJI]: {len(selected_stocks) if selected_stocks else 0} [EMOJI]")
        print(f"\n  [EMOJI] Ctrl+C")

        # [EMOJI]
        if not system.trading_available:
            print("\n[ERROR] [EMOJI]")
            print("  [EMOJI]:")
            print("    1. QMT[EMOJI]")
            print("    2. EasyXT[EMOJI]")
            return

        # [EMOJI]
        import time
        try:
            print(f"\n  [EMOJI]...")
            for i in range(5, 0, -1):
                print(f"    {i} [EMOJI]...")
                time.sleep(1)
            print(f"  [[EMOJI]] [EMOJI]...\n")
        except KeyboardInterrupt:
            print("\n[INFO] [EMOJI]")
            return

        # [EMOJI]
        target_stocks = selected_stocks if selected_stocks else []

        # [EMOJI]
        if not target_stocks:
            print(f"[INFO] [EMOJI]")
            print(f"[[EMOJI]] [EMOJI]:")
            print(f"  1. [EMOJI]")
            print(f"  2. [EMOJI]")

            user_confirm = input(f"\n  [EMOJI]3[EMOJI](yes/no): ").strip().lower()

            if user_confirm != 'yes':
                print("[INFO] [EMOJI]")
                return

            # [EMOJI]3[EMOJI]
            print(f"\n[[EMOJI]] [EMOJI]...")
            import random
            random_stocks = random.sample(stock_list, min(3, len(stock_list)))

            for symbol in random_stocks:
                try:
                    hist_data = client.get_market_data(
                        stock_list=[symbol],
                        start_time='20250101',
                        period='1d'
                    )

                    if hist_data is not None and not hist_data.empty:
                        latest = hist_data.iloc[-1]
                        target_stocks.append({
                            'symbol': symbol,
                            'close': latest['Close'],
                            'reasons': '[EMOJI]'
                        })
                except Exception as e:
                    print(f"  [WARN] [EMOJI] {symbol} [EMOJI]: {e}")

            if not target_stocks:
                print(f"[ERROR] [EMOJI]")
                return

        # [EMOJI]
        print("\n[[EMOJI]]")
        print("-"*70)

        try:
            account = system.trader.get_account_asset(ACCOUNT_ID)
            print(f"  [EMOJI]: {account.get('total_asset', 0):,.2f}")
            print(f"  [EMOJI]: {account.get('cash', 0):,.2f}")
            print(f"  [EMOJI]: {account.get('market_value', 0):,.2f}")

            available_cash = account.get('cash', 0)

            if available_cash < 10000:
                print(f"\n[WARN] [EMOJI]: {available_cash:,.2f}")
                print("  [EMOJI]")
                return

        except Exception as e:
            print(f"[ERROR] [EMOJI]: {e}")
            return

        # [EMOJI]
        print(f"\n[[EMOJI]]")
        print("-"*70)

        # [EMOJI]
        single_stock_amount = 5000  # [EMOJI]
        orders_submitted = []

        for i, stock in enumerate(target_stocks, 1):
            symbol = stock['symbol']
            price = stock['close']

            # [EMOJI]
            quantity = int(single_stock_amount / price) // 100 * 100

            if quantity < 100:
                print(f"\n  [{i}/{len(target_stocks)}] {symbol}")
                print(f"    [SKIP] [EMOJI]")
                continue

            print(f"\n  [{i}/{len(target_stocks)}] {symbol}")
            print(f"    [EMOJI]: [EMOJI]")
            print(f"    [EMOJI]: {quantity} [EMOJI]")
            print(f"    [EMOJI]: {price:.2f}")
            print(f"    [EMOJI]: {quantity * price:,.2f}")

            # [EMOJI]
            try:
                # [EMOJI]EasyXT[EMOJI]buy[EMOJI]
                result = system.trader.trade.buy(
                    account_id=ACCOUNT_ID,
                    code=symbol,
                    volume=quantity,
                    price=price,
                    price_type='limit'  # [EMOJI]
                )

                if result:
                    print(f"    [OK] [EMOJI]")
                    print(f"    [EMOJI]: {result}")
                    orders_submitted.append({
                        'symbol': symbol,
                        'quantity': quantity,
                        'price': price,
                        'amount': quantity * price,
                        'order_id': result
                    })
                else:
                    print(f"    [FAIL] [EMOJI]")

            except Exception as e:
                print(f"    [ERROR] [EMOJI]: {e}")
                import traceback
                traceback.print_exc()

        # [EMOJI]
        print("\n" + "="*70)
        print("  [[EMOJI]]")
        print("="*70)

        if orders_submitted:
            total_quantity = sum(o['quantity'] for o in orders_submitted)
            total_amount = sum(o['amount'] for o in orders_submitted)

            print(f"\n  [EMOJI]: {len(orders_submitted)} [EMOJI]")
            print(f"  [EMOJI]: {total_quantity} [EMOJI]")
            print(f"  [EMOJI]: {total_amount:,.2f}")

            print(f"\n  [EMOJI]:")
            for order in orders_submitted:
                print(f"    - {order['symbol']}: "
                      f"{order['quantity']}[EMOJI] × {order['price']:.2f} = "
                      f"{order['amount']:,.2f}")

            print(f"\n  [[EMOJI]]")
            print(f"    1. [EMOJI]QMT[EMOJI]")
            print(f"    2. [EMOJI]QMT[EMOJI]")
            print(f"    3. [EMOJI]")
            print(f"    4. [EMOJI]")
        else:
            print(f"\n  [INFO] [EMOJI]")

        # ============================================================
        # [EMOJI]
        # ============================================================
        print("\n" + "="*70)
        print("  [EMOJI]")
        print("="*70)

        print("""
[EMOJI]: [EMOJI]
[EMOJI]

1. [EMOJI]:
   - [EMOJI]F6[EMOJI]
   - [EMOJI]
   - [EMOJI]

2. [EMOJI]:
   python tools/parse_tdx_zixg.py

   [EMOJI]:
     [[EMOJI]] [EMOJI] 35 [EMOJI]:
        1. 002475.SZ
        2. 002528.SZ
        ...
     [[EMOJI]] [EMOJI]: my_favorites.txt

3. [EMOJI]:
   python [EMOJI]/11_[EMOJI].py

   [EMOJI]:
   - [EMOJI] my_favorites.txt
   - [EMOJI]
   - [EMOJI]+[EMOJI]+[EMOJI]
   - [EMOJI]


[EMOJI]: [EMOJI]
[EMOJI]

1. [EMOJI]:
   - [EMOJI]: [EMOJI] -> [EMOJI] (Ctrl+T)
   - [EMOJI]:
     * MACD[EMOJI]: CROSS(MACD.DIF, MACD.DEA)
     * KDJ[EMOJI]: CROSS(KDJ.K(9,3,3), 20)
     * RSI[EMOJI]: RSI.RSI1(6,12,24) < 20
     * [EMOJI]: C > REF(C,1) * 1.03 AND V > REF(V,1) * 1.5

2. [EMOJI]:
   - [EMOJI]"[EMOJI]"
   - [EMOJI]
   - [EMOJI] -> "[EMOJI]"
   - [EMOJI]"[EMOJI]"
   - [EMOJI]
   - [EMOJI]

3. [EMOJI]:
   python [EMOJI]/11_[EMOJI].py


[EMOJI]: [EMOJI]
[EMOJI]

1. [EMOJI] my_favorites.txt [EMOJI]:
   002475.SZ
   002528.SZ
   600519.SH
   ...

2. [EMOJI]:
   python [EMOJI]/11_[EMOJI].py


[EMOJI]:
[EMOJI]

[EMOJI]:
   ACCOUNT_ID = '39020958'           # [EMOJI]ID
   single_stock_amount = 5000       # [EMOJI]
   max_stocks = 3                   # [EMOJI]

[EMOJI]:
   1. [EMOJI]: Close > Open
   2. [EMOJI]: Volume > 1000000
   3. [EMOJI]: Close > MA20

[EMOJI]

3. [EMOJI]


[EMOJI]
[EMOJI]

1. [EMOJI]
2. [EMOJI]
3. [EMOJI]
4. [EMOJI]
5. [EMOJI]
6. [EMOJI]
        """)

        print("\n[TIP] [EMOJI]:")
        print("  1. [EMOJI]F6[EMOJI]")
        print("  2. [EMOJI]: python tools/parse_tdx_zixg.py")
        print("  3. [EMOJI]: my_favorites.txt [EMOJI]")
        print("  4. [EMOJI]: python [EMOJI]/11_[EMOJI].py")
        print("  5. [EMOJI]")

        print("\n[TIP] [EMOJI] + EasyXT = [EMOJI]!")
        print("  - [EMOJI]: [EMOJI]")
        print("  - EasyXT: [EMOJI]")
        print("  - [EMOJI]: [EMOJI] + [EMOJI]")
        print("  - [EMOJI]: [EMOJI]")

    # [EMOJI]5: [EMOJI] + [EMOJI]
    print("\n" + "="*70)
    print("  [EMOJI]5[EMOJI] + [EMOJI]")
    print("="*70)

    print("""
[EMOJI]
[EMOJI]  [EMOJI] + [EMOJI] = [EMOJI]              [EMOJI]
[EMOJI]                                                              [EMOJI]
[EMOJI]  [EMOJI]                                                      [EMOJI]
[EMOJI]  1. [EMOJI]                                    [EMOJI]
[EMOJI]  2. [EMOJI]                                [EMOJI]
[EMOJI]  3. [EMOJI]                                  [EMOJI]
[EMOJI]  4. [EMOJI]                                              [EMOJI]
[EMOJI]
    """)

    print("\n[[EMOJI]]")
    print("  [EMOJI]'[EMOJI]'[EMOJI]'[EMOJI]'[EMOJI]")
    print("  - [EMOJI] → [EMOJI] → [EMOJI]")
    print("  - [EMOJI] → [EMOJI] → [EMOJI]")

    print("\n[[EMOJI]]")
    print("="*70)

    print("""
[EMOJI]1: [EMOJI]
[EMOJI]

1. [EMOJI]:
   - [EMOJI] → [EMOJI] ([EMOJI] Ctrl+W)
   - [EMOJI]: [EMOJI] → [EMOJI] → [EMOJI]

2. [EMOJI]:
   [EMOJI]
   [EMOJI] [EMOJI]:                                         [EMOJI]
   [EMOJI]                                                  [EMOJI]
   [EMOJI] [EMOJI]                                      [EMOJI]
   [EMOJI]  - [EMOJI]20[EMOJI]:                              [EMOJI]
   [EMOJI]    C > HHV(C, 20)                                [EMOJI]
   [EMOJI]                                                  [EMOJI]
   [EMOJI] [EMOJI]                                  [EMOJI]
   [EMOJI]  - MACD[EMOJI]:                                      [EMOJI]
   [EMOJI]    CROSS(MACD.DIF, MACD.DEA)                     [EMOJI]
   [EMOJI]  - KDJ[EMOJI]:                                       [EMOJI]
   [EMOJI]    CROSS(KDJ.K, KDJ.D)                           [EMOJI]
   [EMOJI]  - RSI[EMOJI]:                                       [EMOJI]
   [EMOJI]    RSI.RSI1(6,12,24) < 20                        [EMOJI]
   [EMOJI]                                                  [EMOJI]
   [EMOJI] [EMOJI]                                    [EMOJI]
   [EMOJI]  - [EMOJI]:                                      [EMOJI]
   [EMOJI]    C/REF(C,1) > 1.03 AND V/REF(V,1) > 2         [EMOJI]
   [EMOJI]  - [EMOJI]:                                      [EMOJI]
   [EMOJI]    V > MA(V, 5) * 3                              [EMOJI]
   [EMOJI]                                                  [EMOJI]
   [EMOJI] [EMOJI]                                      [EMOJI]
   [EMOJI]  - [EMOJI]:                                        [EMOJI]
   [EMOJI]    O < REF(C, 1) AND C > REF(O, 1)              [EMOJI]
   [EMOJI]  - [EMOJI]:                                      [EMOJI]
   [EMOJI]    C > O AND L < REF(L, 1) AND H > REF(H, 1)    [EMOJI]
   [EMOJI]

3. [EMOJI]:
   - [EMOJI]"[EMOJI]"
   - [EMOJI]: "[EMOJI]"
   - [EMOJI]"[EMOJI]" ([EMOJI])
   - [EMOJI]: 5[EMOJI]/[EMOJI]

4. [EMOJI]:
   - [EMOJI]"[EMOJI]"
   - [EMOJI]
   - [EMOJI]"[EMOJI]"[EMOJI]


[EMOJI]2: Python[EMOJI]
[EMOJI]
    """)

    # [EMOJI]
    print("\n[[EMOJI]]")
    print("-"*70)

    print("""
# ===== [EMOJI] =====

import time
from datetime import datetime
from easy_xt.tdx_client import TdxClient

class AlertTradingBot:
    '''[EMOJI] - [EMOJI]'''

    def __init__(self, trader, account_id):
        self.trader = trader
        self.account_id = account_id
        self.alert_block = '[EMOJI]'  # [EMOJI]
        self.processed_alerts = set()  # [EMOJI]

    def check_alerts(self):
        '''[EMOJI]'''
        with TdxClient() as client:
            # [EMOJI]
            alert_stocks = client.get_sector_stocks(
                self.alert_block,
                block_type=1  # 1=[EMOJI]
            )

            if not alert_stocks:
                print(f"[{datetime.now()}] [EMOJI]")
                return []

            # [EMOJI]
            new_alerts = [s for s in alert_stocks if s not in self.processed_alerts]

            if new_alerts:
                print(f"\\n[{datetime.now()}] [EMOJI] {len(new_alerts)} [EMOJI]:")
                for stock in new_alerts:
                    print(f"  - {stock}")

            return new_alerts

    def evaluate_and_trade(self, stock_list):
        '''[EMOJI]'''
        if not stock_list:
            return

        with TdxClient() as client:
            for stock_code in stock_list:
                try:
                    # [EMOJI]
                    data = client.get_market_data(
                        stock_list=[stock_code],
                        start_time='20250101',
                        period='1d'
                    )

                    if data.empty:
                        continue

                    latest = data.iloc[-1]
                    current_price = latest['Close']

                    # [EMOJI]
                    # [EMOJI]
                    print(f"\\n  {stock_code}")
                    print(f"    [EMOJI]: {current_price:.2f}")
                    print(f"    [EMOJI]: [EMOJI]")

                    # [EMOJI]
                    self.auto_buy(stock_code, current_price)

                    # [EMOJI]
                    self.processed_alerts.add(stock_code)

                except Exception as e:
                    print(f"    [EMOJI]: {e}")

    def auto_buy(self, stock_code, price):
        '''[EMOJI]'''
        try:
            # [EMOJI]
            account = self.trader.get_account_asset(self.account_id)
            cash = account.get('cash', 0)

            # [EMOJI]10%[EMOJI]
            trade_amount = cash * 0.1
            quantity = int(trade_amount / price) // 100 * 100

            if quantity < 100:
                print(f"    [[EMOJI]] [EMOJI]")
                return

            # [EMOJI]
            print(f"    [[EMOJI]] {quantity}[EMOJI] @ {price:.2f}[EMOJI]")

            # [EMOJI]
            # result = self.trader.trade.buy(
            #     account_id=self.account_id,
            #     code=stock_code,
            #     volume=quantity,
            #     price=price,
            #     price_type='limit'
            # )
            # print(f"    [[EMOJI]] [EMOJI]: {result}")

        except Exception as e:
            print(f"    [[EMOJI]] {e}")

    def run(self, duration_hours=4):
        '''[EMOJI]'''
        print(f"\\n[[EMOJI]] [EMOJI]")
        print(f"  [EMOJI]: {duration_hours}[EMOJI]")
        print(f"  [EMOJI]: {self.alert_block}")
        print(f"  [EMOJI]: [EMOJI]30[EMOJI]")

        start_time = time.time()
        check_interval = 30  # 30[EMOJI]

        while True:
            try:
                # [EMOJI]
                if time.time() - start_time > duration_hours * 3600:
                    print(f"\\n[[EMOJI]] [EMOJI]")
                    break

                # [EMOJI]
                new_alerts = self.check_alerts()

                # [EMOJI]
                if new_alerts:
                    self.evaluate_and_trade(new_alerts)

                # [EMOJI]
                time.sleep(check_interval)

            except KeyboardInterrupt:
                print(f"\\n[[EMOJI]] [EMOJI]")
                break
            except Exception as e:
                print(f"\\n[[EMOJI]] {e}")
                time.sleep(check_interval)


# [EMOJI]
print("\\n" + "="*70)
print("  [EMOJI]")
print("="*70)

if system.trading_available:
    # [EMOJI]
    bot = AlertTradingBot(system.trader, ACCOUNT_ID)

    # [EMOJI]4[EMOJI]
    print("\\n[[EMOJI]] [EMOJI] Ctrl+C [EMOJI]")
    print("[[EMOJI]] [EMOJI]30[EMOJI]...\\n")

    try:
        # [EMOJI]4[EMOJI]
        bot.run(duration_hours=0.01)  # [EMOJI]30[EMOJI]

    except KeyboardInterrupt:
        print("\\n[[EMOJI]] [EMOJI]")
else:
    print("\\n[[EMOJI]] [EMOJI]")
    """)

    print("\n[[EMOJI]][EMOJI]")
    print("-"*70)

    print("""
# [EMOJI]1: [EMOJI]Windows[EMOJI]
# [EMOJI]
# 1. [EMOJI]"[EMOJI]"[EMOJI]taskschd.msc[EMOJI]
# 2. [EMOJI]
# 3. [EMOJI]: [EMOJI] 9:25
# 4. [EMOJI]: [EMOJI] python alert_trading_bot.py
# 5. [EMOJI]

# [EMOJI]2: [EMOJI]Python[EMOJI]
# [EMOJI]
import schedule
import time

def run_trading_bot():
    bot = AlertTradingBot(trader, ACCOUNT_ID)
    bot.run(duration_hours=4)  # [EMOJI]4[EMOJI]

# [EMOJI]9:25[EMOJI]
schedule.every().day.at("09:25").do(run_trading_bot)

while True:
    schedule.run_pending()
    time.sleep(60)

# [EMOJI]3: Docker[EMOJI]
# [EMOJI]
# docker-compose.yml
version: '3'
services:
  trading-bot:
    image: python:3.9
    volumes:
      - ./app:/app
    command: python alert_trading_bot.py
    restart: always
    """)

    print("\n[[EMOJI]]")
    print("-"*70)

    print("""
1. [EMOJI]
   - [EMOJI]10%
   - [EMOJI]5[EMOJI]
   - [EMOJI]20%

2. [EMOJI]
   - [EMOJI] + 1%
   - [EMOJI]

3. [EMOJI]
   - [EMOJI]9:30-15:00
   - [EMOJI]30[EMOJI]
   - [EMOJI]30[EMOJI]

4. [EMOJI]
   - [EMOJI]3[EMOJI]
   - [EMOJI]

5. [EMOJI]
   - [EMOJI]80%
   - [EMOJI]
   - [EMOJI]
    """)

    print("\n[[EMOJI]]")
    print("="*70)

    print("""
[EMOJI]: [EMOJI]
[EMOJI]
1. [EMOJI] → [EMOJI] → [EMOJI]
2. [EMOJI]MACD[EMOJI]
3. [EMOJI]"[EMOJI]"[EMOJI]
4. [EMOJI]

[EMOJI]: [EMOJI]
[EMOJI]
python [EMOJI]/11_[EMOJI].py

[EMOJI]: [EMOJI]
[EMOJI]
- [EMOJI]
- [EMOJI]
- [EMOJI]
- Python[EMOJI]
- [EMOJI]


[EMOJI]
[EMOJI]
[EMOJI]
[EMOJI]   [EMOJI]       [EMOJI]   [EMOJI]    [EMOJI]   [EMOJI]      [EMOJI]
[EMOJI]
[EMOJI] [EMOJI]     [EMOJI] [EMOJI]        [EMOJI] [EMOJI]        [EMOJI]
[EMOJI] [EMOJI]     [EMOJI] [EMOJI]        [EMOJI] [EMOJI]    [EMOJI]
[EMOJI] [EMOJI]     [EMOJI] [EMOJI]  [EMOJI] [EMOJI]  [EMOJI]
[EMOJI] [EMOJI]     [EMOJI] [EMOJI]    [EMOJI] [EMOJI]    [EMOJI]
[EMOJI] [EMOJI]     [EMOJI] [EMOJI]      [EMOJI] [EMOJI]/[EMOJI]   [EMOJI]
[EMOJI] [EMOJI]   [EMOJI] [EMOJI]          [EMOJI] [EMOJI]          [EMOJI]
[EMOJI]

[EMOJI]:
  - [EMOJI]: [EMOJI]4[EMOJI]
  - [EMOJI]: [EMOJI]5[EMOJI]
  - [EMOJI]: [EMOJI]
    """)

    print("\n[[EMOJI]]")
    print("-"*70)

    print("""
[!] [EMOJI]:
1. [EMOJI]
2. [EMOJI]QMT[EMOJI]
3. [EMOJI]
4. [EMOJI]
5. [EMOJI]

[OK] [EMOJI]:
1. [EMOJI]
2. [EMOJI]
3. [EMOJI]
4. [EMOJI]

[X] [EMOJI]:
1. [EMOJI]
2. [EMOJI]
3. [EMOJI]
4. [EMOJI]

[TIP] [EMOJI]:
1. [EMOJI]
2. [EMOJI]
3. [EMOJI]
4. [EMOJI]
5. [EMOJI]
    """)

    # [EMOJI]
    print("\n" + "="*70)
    print("  [EMOJI]")
    print("="*70)

    print("""
[OK] [EMOJI] + EasyXT [EMOJI]:

1. [EMOJI]
   - K[EMOJI]
   - [EMOJI]
   - [EMOJI]

2. [EMOJI]
   - [EMOJI]
   - [EMOJI]
   - [EMOJI]
   - [EMOJI]ROE[EMOJI]PE[EMOJI]PB[EMOJI]

3. [EMOJI]
   - [EMOJI]MA[EMOJI]
   - MACD
   - RSI
   - [EMOJI]
   - [EMOJI]

4. [EMOJI]
   - [EMOJI]
   - [EMOJI]
   - [EMOJI]

5. EasyXT[EMOJI]
   - [EMOJI]
   - [EMOJI]
   - [EMOJI]

6. [EMOJI]4[EMOJI]
   - [EMOJI]
   - [EMOJI]
   - [EMOJI]
   - [EMOJI]
   - [EMOJI]

7. [EMOJI]5[EMOJI]
   - [EMOJI]
   - [EMOJI]
   - [EMOJI]
   - [EMOJI]
   - [EMOJI]
   - [EMOJI]


[TIP] [EMOJI]:

[EMOJI]: [EMOJI]
[EMOJI] [EMOJI]
[EMOJI] [EMOJI]
[EMOJI] [EMOJI]

[EMOJI]: [EMOJI]
[EMOJI] [EMOJI]
[EMOJI] [EMOJI]
[EMOJI] [EMOJI]
[EMOJI] [EMOJI]

[EMOJI]: [EMOJI]
[EMOJI] [EMOJI]
[EMOJI] [EMOJI]
[EMOJI] [EMOJI]


[EMOJI]:
1. [EMOJI] -> [EMOJI]
2. [EMOJI] -> [EMOJI]/[EMOJI]
3. [EMOJI] -> [EMOJI]EasyXT[EMOJI]
4. [EMOJI] -> [EMOJI]


[EMOJI]:
   GitHub: https://github.com/quant-king299/EasyXT

[EMOJI] [EMOJI]:
   - [EMOJI] + [EMOJI]
   - [EMOJI]
   - [EMOJI]
    """)


if __name__ == "__main__":
    main()
