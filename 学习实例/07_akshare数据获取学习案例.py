"""
[EMOJI] - [EMOJI] ([EMOJI]akshare)
[EMOJI]akshare[EMOJI]

[EMOJI]
1. [EMOJI]
2. [EMOJI]
3. [EMOJI]K[EMOJI]
4. [EMOJI]
5. [EMOJI]

[EMOJI]quant
[EMOJI]2025-01-09
"""

import akshare as ak
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from datetime import datetime, timedelta
import os
import warnings
warnings.filterwarnings('ignore')

# [EMOJI]
plt.rcParams['font.sans-serif'] = ['SimHei']
plt.rcParams['axes.unicode_minus'] = False

class StockDataFetcher:
    """[EMOJI] - [EMOJI]akshare"""
    
    def __init__(self):
        """[EMOJI]"""
        self.data_dir = "data"
        if not os.path.exists(self.data_dir):
            os.makedirs(self.data_dir)
        print("[CHART] [EMOJI] ([EMOJI]akshare)")
    
    def get_stock_info(self, stock_code):
        """
        [EMOJI]
        
        Args:
            stock_code (str): [EMOJI] '000001' [EMOJI] '600000'
            
        Returns:
            dict: [EMOJI]
        """
        try:
            print(f"[SEARCH] [EMOJI] {stock_code} [EMOJI]...")
            
            # [EMOJI]
            stock_info = ak.stock_zh_a_spot_em()
            stock_data = stock_info[stock_info['[EMOJI]'] == stock_code]
            
            if not stock_data.empty:
                data = stock_data.iloc[0]
                
                info = {
                    'stock_code': stock_code,
                    'name': data['[EMOJI]'],
                    'latest_price': data['[EMOJI]'],
                    'change_pct': data['[EMOJI]'],
                    'change_amount': data['[EMOJI]'],
                    'volume': data['[EMOJI]'],
                    'amount': data['[EMOJI]'],
                    'amplitude': data['[EMOJI]'],
                    'high': data['[EMOJI]'],
                    'low': data['[EMOJI]'],
                    'open': data['[EMOJI]'],
                    'prev_close': data['[EMOJI]']
                }
                
                print(f"[OK] [EMOJI] {stock_code} ({data['[EMOJI]']}) [EMOJI]")
                return info
            else:
                print(f"[X] [EMOJI] {stock_code} [EMOJI]")
                return None
                
        except Exception as e:
            print(f"[X] [EMOJI]: {str(e)}")
            return None
    
    def get_realtime_data(self, stock_codes):
        """
        [EMOJI]
        
        Args:
            stock_codes (list): [EMOJI]
            
        Returns:
            pd.DataFrame: [EMOJI]
        """
        try:
            print(f"[UP] [EMOJI] {len(stock_codes)} [EMOJI]...")
            
            # [EMOJI]A[EMOJI]
            all_stocks = ak.stock_zh_a_spot_em()
            
            # [EMOJI]
            selected_stocks = all_stocks[all_stocks['[EMOJI]'].isin(stock_codes)]
            
            if not selected_stocks.empty:
                realtime_data = []
                
                for _, row in selected_stocks.iterrows():
                    realtime_data.append({
                        'stock_code': row['[EMOJI]'],
                        'name': row['[EMOJI]'],
                        'latest_price': row['[EMOJI]'],
                        'change_pct': row['[EMOJI]'],
                        'change_amount': row['[EMOJI]'],
                        'volume': row['[EMOJI]'],
                        'amount': row['[EMOJI]'],
                        'high': row['[EMOJI]'],
                        'low': row['[EMOJI]'],
                        'open': row['[EMOJI]'],
                        'prev_close': row['[EMOJI]']
                    })
                    print(f"  [OK] {row['[EMOJI]']} {row['[EMOJI]']}: {row['[EMOJI]']:.2f} ({row['[EMOJI]']:+.2f}%)")
                
                df = pd.DataFrame(realtime_data)
                print(f"[OK] [EMOJI] {len(realtime_data)} [EMOJI]")
                return df
            else:
                print("[X] [EMOJI]")
                return pd.DataFrame()
                
        except Exception as e:
            print(f"[X] [EMOJI]: {str(e)}")
            return pd.DataFrame()
    
    def get_historical_data(self, stock_code, period="daily", adjust="qfq", start_date=None, end_date=None):
        """
        [EMOJI]K[EMOJI]
        
        Args:
            stock_code (str): [EMOJI]
            period (str): [EMOJI]"daily"
            adjust (str): [EMOJI]"qfq"[EMOJI]
            start_date (str): [EMOJI]"20240101"
            end_date (str): [EMOJI]"20241231"
            
        Returns:
            pd.DataFrame: [EMOJI]K[EMOJI]
        """
        try:
            # [EMOJI]30[EMOJI]
            if not start_date:
                start_date = (datetime.now() - timedelta(days=60)).strftime("%Y%m%d")
            if not end_date:
                end_date = datetime.now().strftime("%Y%m%d")
            
            print(f"[CHART] [EMOJI] {stock_code} [EMOJI] {start_date} [EMOJI] {end_date} [EMOJI]...")
            
            # [EMOJI]
            hist_data = ak.stock_zh_a_hist(symbol=stock_code, period=period, 
                                         start_date=start_date, end_date=end_date, adjust=adjust)
            
            if hist_data is not None and not hist_data.empty:
                # [EMOJI]
                hist_data.columns = ['date', 'open', 'close', 'high', 'low', 'volume', 'amount', 'amplitude', 'change_pct', 'change_amount', 'turnover']
                
                # [EMOJI]
                hist_data['date'] = pd.to_datetime(hist_data['date'])
                hist_data.set_index('date', inplace=True)
                
                # [EMOJI]
                hist_data = self._add_technical_indicators(hist_data)
                
                # [EMOJI]
                filename = f"{self.data_dir}/{stock_code}_historical.csv"
                hist_data.to_csv(filename)
                
                print(f"[OK] [EMOJI] {len(hist_data)} [EMOJI] {filename}")
                return hist_data
            else:
                print(f"[X] [EMOJI] {stock_code} [EMOJI]")
                return pd.DataFrame()
                
        except Exception as e:
            print(f"[X] [EMOJI]: {str(e)}")
            return pd.DataFrame()
    
    def _add_technical_indicators(self, data):
        """
        [EMOJI]
        
        Args:
            data (pd.DataFrame): [EMOJI]K[EMOJI]
            
        Returns:
            pd.DataFrame: [EMOJI]
        """
        try:
            # [EMOJI]
            data['MA5'] = data['close'].rolling(window=5).mean()
            data['MA10'] = data['close'].rolling(window=10).mean()
            data['MA20'] = data['close'].rolling(window=20).mean()
            
            # [EMOJI]
            data['VOL_MA5'] = data['volume'].rolling(window=5).mean()
            
            # [EMOJI]RSI
            delta = data['close'].diff()
            gain = (delta.where(delta > 0, 0)).rolling(window=14).mean()
            loss = (-delta.where(delta < 0, 0)).rolling(window=14).mean()
            rs = gain / loss
            data['RSI'] = 100 - (100 / (1 + rs))
            
            # [EMOJI]MACD
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
            
            return data
            
        except Exception as e:
            print(f"[X] [EMOJI]: {str(e)}")
            return data
    
    def visualize_data(self, data, stock_code, title="[EMOJI]K[EMOJI]"):
        """
        [EMOJI]
        
        Args:
            data (pd.DataFrame): [EMOJI]
            stock_code (str): [EMOJI]
            title (str): [EMOJI]
        """
        try:
            if data.empty:
                print("[X] [EMOJI]")
                return
            
            print(f"[UP] [EMOJI] {stock_code} [EMOJI]K[EMOJI]...")
            
            # [EMOJI]
            fig, ((ax1, ax2), (ax3, ax4)) = plt.subplots(2, 2, figsize=(15, 12))
            
            # 1. [EMOJI]K[EMOJI]
            ax1.plot(data.index, data['close'], label='[EMOJI]', linewidth=2, color='blue')
            
            if 'MA5' in data.columns:
                ax1.plot(data.index, data['MA5'], label='MA5', alpha=0.7, color='orange')
            if 'MA10' in data.columns:
                ax1.plot(data.index, data['MA10'], label='MA10', alpha=0.7, color='green')
            if 'MA20' in data.columns:
                ax1.plot(data.index, data['MA20'], label='MA20', alpha=0.7, color='red')
            
            # [EMOJI]
            if 'BB_upper' in data.columns:
                ax1.fill_between(data.index, data['BB_upper'], data['BB_lower'], 
                               alpha=0.2, color='gray', label='[EMOJI]')
            
            ax1.set_title(f'{title} - {stock_code}', fontsize=14, fontweight='bold')
            ax1.set_ylabel('[EMOJI] ([EMOJI])', fontsize=12)
            ax1.legend()
            ax1.grid(True, alpha=0.3)
            
            # 2. [EMOJI]
            ax2.bar(data.index, data['volume'], alpha=0.6, color='gray', label='[EMOJI]')
            if 'VOL_MA5' in data.columns:
                ax2.plot(data.index, data['VOL_MA5'], color='red', label='[EMOJI]MA5')
            
            ax2.set_title('[EMOJI]', fontsize=12)
            ax2.set_ylabel('[EMOJI]', fontsize=12)
            ax2.legend()
            ax2.grid(True, alpha=0.3)
            
            # 3. [EMOJI]RSI
            if 'RSI' in data.columns:
                ax3.plot(data.index, data['RSI'], color='purple', label='RSI')
                ax3.axhline(y=70, color='r', linestyle='--', alpha=0.7, label='[EMOJI](70)')
                ax3.axhline(y=30, color='g', linestyle='--', alpha=0.7, label='[EMOJI](30)')
                ax3.set_title('RSI[EMOJI]', fontsize=12)
                ax3.set_ylabel('RSI', fontsize=12)
                ax3.set_ylim(0, 100)
                ax3.legend()
                ax3.grid(True, alpha=0.3)
            
            # 4. [EMOJI]MACD
            if 'MACD' in data.columns:
                ax4.plot(data.index, data['MACD'], color='blue', label='MACD')
                ax4.plot(data.index, data['MACD_signal'], color='red', label='Signal')
                ax4.bar(data.index, data['MACD_hist'], alpha=0.6, color='green', label='Histogram')
                ax4.axhline(y=0, color='black', linestyle='-', alpha=0.3)
                ax4.set_title('MACD[EMOJI]', fontsize=12)
                ax4.set_ylabel('MACD', fontsize=12)
                ax4.legend()
                ax4.grid(True, alpha=0.3)
            
            # [EMOJI]x[EMOJI]
            for ax in [ax1, ax2, ax3, ax4]:
                ax.xaxis.set_major_formatter(mdates.DateFormatter('%m-%d'))
                plt.setp(ax.xaxis.get_majorticklabels(), rotation=45)
            
            plt.tight_layout()
            
            # [EMOJI]
            chart_filename = f"{self.data_dir}/{stock_code}_chart.png"
            plt.savefig(chart_filename, dpi=300, bbox_inches='tight')
            
            plt.show()
            print(f"[OK] [EMOJI] {chart_filename}")
            
        except Exception as e:
            print(f"[X] [EMOJI]: {str(e)}")
    
    def get_market_summary(self, stock_codes):
        """
        [EMOJI]
        
        Args:
            stock_codes (list): [EMOJI]
            
        Returns:
            pd.DataFrame: [EMOJI]
        """
        try:
            print(f"[CHART] [EMOJI] {len(stock_codes)} [EMOJI]...")
            
            # [EMOJI]A[EMOJI]
            all_stocks = ak.stock_zh_a_spot_em()
            
            # [EMOJI]
            selected_stocks = all_stocks[all_stocks['[EMOJI]'].isin(stock_codes)]
            
            if not selected_stocks.empty:
                summary_data = []
                
                for _, row in selected_stocks.iterrows():
                    summary_data.append({
                        'stock_code': row['[EMOJI]'],
                        'name': row['[EMOJI]'],
                        'latest_price': row['[EMOJI]'],
                        'change_pct': row['[EMOJI]'],
                        'change_amount': row['[EMOJI]'],
                        'volume': row['[EMOJI]'],
                        'amount': row['[EMOJI]'],
                        'amplitude': row['[EMOJI]'],
                        'high': row['[EMOJI]'],
                        'low': row['[EMOJI]'],
                        'turnover': row['[EMOJI]']
                    })
                
                df = pd.DataFrame(summary_data)
                print(f"[OK] [EMOJI] {len(summary_data)} [EMOJI]")
                return df
            else:
                print("[X] [EMOJI]")
                return pd.DataFrame()
                
        except Exception as e:
            print(f"[X] [EMOJI]: {str(e)}")
            return pd.DataFrame()


def main():
    """[EMOJI] - [EMOJI]"""
    print("=" * 60)
    print("[LAUNCH] [EMOJI] - [EMOJI] (akshare[EMOJI])")
    print("=" * 60)
    
    # [EMOJI]
    fetcher = StockDataFetcher()
    
    # [EMOJI]
    test_stocks = ['000001', '600000', '000002', '600036']  # [EMOJI]A[EMOJI]
    single_stock = '000001'  # [EMOJI]
    
    print("\n" + "=" * 40)
    print("[EMOJI] [EMOJI]")
    print("=" * 40)
    
    # [EMOJI]
    stock_info = fetcher.get_stock_info(single_stock)
    if stock_info:
        print(f"\n[CHART] [EMOJI] {single_stock} [EMOJI]")
        for key, value in stock_info.items():
            print(f"  {key}: {value}")
    
    print("\n" + "=" * 40)
    print("[UP] [EMOJI]")
    print("=" * 40)
    
    # [EMOJI]
    realtime_df = fetcher.get_realtime_data(test_stocks)
    if not realtime_df.empty:
        print(f"\n[CHART] [EMOJI]")
        display_cols = ['stock_code', 'name', 'latest_price', 'change_pct', 'volume']
        print(realtime_df[display_cols].to_string(index=False))
    
    print("\n" + "=" * 40)
    print("[CHART] [EMOJI]K[EMOJI]")
    print("=" * 40)
    
    # [EMOJI]
    historical_df = fetcher.get_historical_data(single_stock)
    if not historical_df.empty:
        print(f"\n[CHART] [EMOJI]")
        print(f"  [EMOJI]: {len(historical_df)}")
        print(f"  [EMOJI]: {historical_df.index[0].strftime('%Y-%m-%d')} [EMOJI] {historical_df.index[-1].strftime('%Y-%m-%d')}")
        print(f"  [EMOJI]: {historical_df['high'].max():.2f}")
        print(f"  [EMOJI]: {historical_df['low'].min():.2f}")
        print(f"  [EMOJI]: {historical_df['volume'].mean():.0f}")
        
        # [EMOJI]5[EMOJI]
        print(f"\n[CHART] [EMOJI]5[EMOJI]")
        recent_data = historical_df.tail(5)[['open', 'high', 'low', 'close', 'volume', 'MA5', 'RSI']]
        print(recent_data.round(2).to_string())
    
    print("\n" + "=" * 40)
    print("[UP] [EMOJI]")
    print("=" * 40)
    
    # [EMOJI]K[EMOJI]
    if not historical_df.empty:
        fetcher.visualize_data(historical_df, single_stock, "[EMOJI]K[EMOJI]")
    
    print("\n" + "=" * 40)
    print("[CHART] [EMOJI]")
    print("=" * 40)
    
    # [EMOJI]
    market_summary = fetcher.get_market_summary(test_stocks)
    if not market_summary.empty:
        print(f"\n[CHART] [EMOJI]")
        display_cols = ['stock_code', 'name', 'latest_price', 'change_pct', 'amplitude', 'turnover']
        print(market_summary[display_cols].to_string(index=False))
    
    print("\n" + "=" * 60)
    print("[OK] [EMOJI]")
    print("[EMOJI] [EMOJI] data/ [EMOJI]")
    print("[UP] [EMOJI] data/ [EMOJI]")
    print("=" * 60)


if __name__ == "__main__":
    main()