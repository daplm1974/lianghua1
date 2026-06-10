#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
EasyXT[EMOJI]05: [EMOJI]
[EMOJI]QMT[EMOJI]
[EMOJI]xtdata[EMOJI]v2023-01-31
"""

import sys
import os
import pandas as pd
from datetime import datetime, timedelta

# [EMOJI]
current_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.dirname(current_dir)
sys.path.insert(0, project_root)

from easy_xt import EasyXT
from easy_xt.data_api import get_supported_periods, validate_period

def show_supported_periods():
    """[EMOJI]"""
    print("=" * 60)
    print("QMT[EMOJI]")
    print("=" * 60)
    
    periods = get_supported_periods()
    
    # Level1[EMOJI]
    level1_periods = ['tick', '1m', '5m', '15m', '30m', '1h', '1d']
    print("\n[CHART] Level1[EMOJI] ([EMOJI]):")
    print("-" * 40)
    for period in level1_periods:
        if period in periods:
            print(f"  {period:6} - {periods[period]}")
    
    # Level2[EMOJI]
    level2_periods = ['l2quote', 'l2order', 'l2transaction', 'l2quoteaux', 'l2orderqueue', 'l2thousand']
    print(f"\n[UP] Level2[EMOJI] ([EMOJI]Level2[EMOJI]):")
    print("-" * 40)
    for period in level2_periods:
        if period in periods:
            print(f"  {period:14} - {periods[period]}")

def demo_daily_data():
    """[EMOJI]"""
    print("\n" + "=" * 50)
    print("[UP] [EMOJI]")
    print("=" * 50)
    
    try:
        xt = EasyXT()
        if not xt.init_data():
            print("[X] [EMOJI]QMT")
            return
        
        # [EMOJI]
        codes = ['000001.SZ', '600000.SH']
        print(f"[EMOJI]: {', '.join(codes)}")
        
        data = xt.get_price(
            codes=codes,
            period='1d',
            count=5  # [EMOJI]5[EMOJI]
        )
        
        if data is not None and not data.empty:
            print(f"\n[OK] [EMOJI] ({len(data)} [EMOJI])")
            print("\n[EMOJI]:")
            print(data.head())
            
            # [EMOJI]
            print(f"\n[EMOJI]:")
            print(f"  [EMOJI]: {data['time'].min()} [EMOJI] {data['time'].max()}")
            print(f"  [EMOJI]: {data['code'].nunique()}")
            print(f"  [EMOJI]: {list(data.columns)}")
        else:
            print("[X] [EMOJI]")
            
    except Exception as e:
        print(f"[X] [EMOJI]: {e}")

def demo_minute_data():
    """[EMOJI]"""
    print("\n" + "=" * 50)
    print("⏰ [EMOJI]")
    print("=" * 50)
    
    try:
        xt = EasyXT()
        if not xt.init_data():
            print("[X] [EMOJI]QMT")
            return
        
        # [EMOJI]
        minute_periods = ['1m', '5m', '15m', '30m']
        code = '000001.SZ'
        
        for period in minute_periods:
            try:
                print(f"\n[EMOJI] {period} [EMOJI]...")
                
                data = xt.get_price(
                    codes=code,
                    period=period,
                    count=10  # [EMOJI]10[EMOJI]
                )
                
                if data is not None and not data.empty:
                    print(f"[OK] {period} [EMOJI] ({len(data)} [EMOJI])")
                    print(f"   [EMOJI]: {data['time'].min()} [EMOJI] {data['time'].max()}")
                    
                    # [EMOJI]
                    print("   [EMOJI]:")
                    latest_data = data.tail(3)[['time', 'open', 'high', 'low', 'close', 'volume']]
                    for _, row in latest_data.iterrows():
                        print(f"     {row['time']}: O={row['open']:.2f} H={row['high']:.2f} L={row['low']:.2f} C={row['close']:.2f} V={row['volume']}")
                else:
                    print(f"[X] {period} [EMOJI]")
                    
            except Exception as e:
                print(f"[X] {period} [EMOJI]: {e}")
                
    except Exception as e:
        print(f"[X] [EMOJI]: {e}")

def demo_tick_data():
    """[EMOJI]"""
    print("\n" + "=" * 50)
    print("[CHART] [EMOJI]")
    print("=" * 50)
    
    try:
        xt = EasyXT()
        if not xt.init_data():
            print("[X] [EMOJI]QMT")
            return
        
        code = '000001.SZ'
        print(f"[EMOJI] {code} [EMOJI]...")
        
        data = xt.get_price(
            codes=code,
            period='tick',
            count=5  # [EMOJI]5[EMOJI]
        )
        
        if data is not None and not data.empty:
            print(f"[OK] [EMOJI] ({len(data)} [EMOJI])")
            print("\n[EMOJI]:")
            print(data.head())
            
            # [EMOJI]
            print(f"\n[EMOJI]:")
            print(f"  time: [EMOJI]")
            print(f"  lastPrice: [EMOJI]")
            print(f"  volume: [EMOJI]")
            print(f"  amount: [EMOJI]")
        else:
            print("[X] [EMOJI]")
            
    except Exception as e:
        print(f"[X] [EMOJI]: {e}")

def demo_period_validation():
    """[EMOJI]"""
    print("\n" + "=" * 50)
    print("[OK] [EMOJI]")
    print("=" * 50)
    
    # [EMOJI]
    valid_periods = ['1d', '1m', '5m', '15m', '30m', '1h', 'tick']
    print("[EMOJI]:")
    for period in valid_periods:
        is_valid = validate_period(period)
        print(f"  {period:6} - {'[OK] [EMOJI]' if is_valid else '[X] [EMOJI]'}")
    
    # [EMOJI]
    invalid_periods = ['2m', '10m', '45m', '2h', '1w', '1M']
    print(f"\n[EMOJI]:")
    for period in invalid_periods:
        is_valid = validate_period(period)
        print(f"  {period:6} - {'[OK] [EMOJI]' if is_valid else '[X] [EMOJI]'}")
    
    # [EMOJI]
    print(f"\n[EMOJI]:")
    try:
        xt = EasyXT()
        if xt.init_data():
            # [EMOJI]
            data = xt.get_price('000001.SZ', period='2m')
    except ValueError as e:
        print(f"[OK] [EMOJI]: {e}")
    except Exception as e:
        print(f"[X] [EMOJI]: {e}")

def demo_level2_data():
    """[EMOJI]Level2[EMOJI]"""
    print("\n" + "=" * 50)
    print("[UP] Level2[EMOJI] ([EMOJI])")
    print("=" * 50)
    
    try:
        xt = EasyXT()
        if not xt.init_data():
            print("[X] [EMOJI]QMT")
            return
        
        code = '000001.SZ'
        level2_periods = ['l2quote', 'l2order', 'l2transaction']
        
        for period in level2_periods:
            try:
                print(f"\n[EMOJI] {period} [EMOJI]...")
                
                data = xt.get_price(
                    codes=code,
                    period=period,
                    count=1
                )
                
                if data is not None and not data.empty:
                    print(f"[OK] {period} [EMOJI]")
                    print(f"   [EMOJI]: {list(data.columns)}")
                else:
                    print(f"[X] {period} [EMOJI] ([EMOJI]Level2[EMOJI])")
                    
            except Exception as e:
                error_msg = str(e)
                if "[EMOJI]" in error_msg or "permission" in error_msg.lower():
                    print(f"[X] {period} [EMOJI]Level2[EMOJI]")
                else:
                    print(f"[X] {period} [EMOJI]: {error_msg[:50]}...")
                    
    except Exception as e:
        print(f"[X] [EMOJI]: {e}")

def demo_data_usage_tips():
    """[EMOJI]"""
    print("\n" + "=" * 50)
    print("[TIP] [EMOJI]")
    print("=" * 50)
    
    tips = [
        "1. [EMOJI] (1d): [EMOJI]",
        "2. [EMOJI] (1h): [EMOJI]",
        "3. [EMOJI] (1m/5m/15m/30m): [EMOJI]",
        "4. [EMOJI] (tick): [EMOJI]",
        "5. Level2[EMOJI]: [EMOJI]",
        "",
        "[EMOJI] [EMOJI]:",
        "• [EMOJI]count[EMOJI]",
        "• [EMOJI]",
        "• [EMOJI]tick[EMOJI]Level2[EMOJI]",
        "• [EMOJI]QMT[EMOJI]",
        "",
        "[!]  [EMOJI]:",
        "• [EMOJI]",
        "• Level2[EMOJI]",
        "• [EMOJI]QMT[EMOJI]",
        "• [EMOJI]"
    ]
    
    for tip in tips:
        print(f"  {tip}")

def main():
    """[EMOJI]"""
    print("EasyXT[EMOJI]")
    print("[EMOJI]xtdata[EMOJI]v2023-01-31")
    
    # [EMOJI]
    show_supported_periods()
    
    # [EMOJI]
    demo_period_validation()
    
    # [EMOJI]
    try:
        choice = input("\n[EMOJI]? (y/n): ").lower().strip()
        if choice in ['y', 'yes', '[EMOJI]']:
            # [EMOJI]
            demo_daily_data()
            
            # [EMOJI]
            demo_minute_data()
            
            # [EMOJI]
            demo_tick_data()
            
            # Level2[EMOJI]
            demo_level2_data()
        
        # [EMOJI]
        demo_data_usage_tips()
        
        print(f"\n" + "=" * 60)
        print("[EMOJI]")
        print("=" * 60)
        
    except KeyboardInterrupt:
        print("\n\n[EMOJI]")

if __name__ == "__main__":
    main()