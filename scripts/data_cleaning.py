#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
DuckDB 数据清洗脚本
清洗规则：
1. 基础有效性：open/high/low/close > 0，volume >= 0
2. 无缺失值：OHLCV 任意一项为 NULL 则删除该条
3. 去重：同一 stock_code + date 只保留一条
4. 最少交易日：在 2020-2023 期间至少 500 个交易日
5. 连续性：最大连续停牌不超过 60 天
6. 价格异常：单日涨跌幅不超过 ±20%（排除除权除息异常）
7. 成交量异常：剔除长期 volume=0 的停牌股

输出：
- 清洗后可用股票列表（按数据完整度排序取 Top 500）
- 清洗统计报告
"""

import sys
import os
from datetime import datetime, timedelta
from pathlib import Path

import duckdb
import pandas as pd
import numpy as np

# 配置
DB_PATH = Path(__file__).parent.parent / 'data' / 'stock_data.ddb'
MIN_TRADING_DAYS = 500
MAX_GAP_DAYS = 60
MAX_DAILY_CHANGE = 0.20
OUTPUT_TOP_N = 500


def connect_db():
    return duckdb.connect(str(DB_PATH), read_only=True)


def get_raw_stats(con):
    """原始数据统计"""
    print("\n" + "=" * 70)
    print("原始数据统计")
    print("=" * 70)

    total_rows = con.execute("SELECT COUNT(*) FROM stock_data").fetchone()[0]
    total_stocks = con.execute("SELECT COUNT(DISTINCT symbol) FROM stock_data").fetchone()[0]
    date_range = con.execute("SELECT MIN(date), MAX(date) FROM stock_data").fetchone()

    print(f"总记录数: {total_rows:,}")
    print(f"总股票数: {total_stocks}")
    print(f"日期范围: {date_range[0]} ~ {date_range[1]}")

    # 缺失值统计
    null_stats = con.execute("""
        SELECT
            COUNT(*) as total,
            SUM(CASE WHEN open IS NULL THEN 1 ELSE 0 END) as null_open,
            SUM(CASE WHEN high IS NULL THEN 1 ELSE 0 END) as null_high,
            SUM(CASE WHEN low IS NULL THEN 1 ELSE 0 END) as null_low,
            SUM(CASE WHEN close IS NULL THEN 1 ELSE 0 END) as null_close,
            SUM(CASE WHEN volume IS NULL THEN 1 ELSE 0 END) as null_volume
        FROM stock_data
    """).fetchdf()

    print("\n缺失值统计:")
    for col in ['open', 'high', 'low', 'close', 'volume']:
        n = null_stats[f'null_{col}'].iloc[0]
        pct = n / total_rows * 100 if total_rows > 0 else 0
        print(f"  {col}: {n:,} ({pct:.2f}%)")

    # 价格为零或负数
    zero_price = con.execute("""
        SELECT COUNT(*) FROM stock_data
        WHERE open <= 0 OR high <= 0 OR low <= 0 OR close <= 0
    """).fetchone()[0]
    print(f"\n价格 <= 0 的记录: {zero_price:,}")

    # 成交量为负
    neg_volume = con.execute("""
        SELECT COUNT(*) FROM stock_data WHERE volume < 0
    """).fetchone()[0]
    print(f"成交量 < 0 的记录: {neg_volume:,}")

    return total_rows, total_stocks


def load_and_clean(con):
    """加载并清洗数据"""
    print("\n" + "=" * 70)
    print("加载数据到内存")
    print("=" * 70)

    df = con.execute("""
        SELECT
            symbol as stock_code,
            date,
            open, high, low, close, volume
        FROM stock_data
        WHERE period = '1d'
        ORDER BY symbol, date
    """).df()

    print(f"加载记录数: {len(df):,}")

    # 1. 删除缺失值
    df_clean = df.dropna(subset=['open', 'high', 'low', 'close', 'volume']).copy()
    print(f"删除缺失值后: {len(df_clean):,} (-{len(df) - len(df_clean):,})")

    # 2. 删除价格为零或负数
    price_valid = (
        (df_clean['open'] > 0) &
        (df_clean['high'] > 0) &
        (df_clean['low'] > 0) &
        (df_clean['close'] > 0) &
        (df_clean['volume'] >= 0)
    )
    df_clean = df_clean[price_valid].copy()
    print(f"删除无效价格后: {len(df_clean):,}")

    # 3. 去重
    before_dedup = len(df_clean)
    df_clean = df_clean.drop_duplicates(subset=['stock_code', 'date'])
    print(f"去重后: {len(df_clean):,} (-{before_dedup - len(df_clean):,})")

    # 4. 转换日期
    df_clean['date'] = pd.to_datetime(df_clean['date'])

    # 5. 按股票分组检查
    print("\n" + "=" * 70)
    print("按股票分组检查")
    print("=" * 70)

    stock_stats = []
    removed_reasons = {
        'too_few_days': 0,
        'long_gap': 0,
        'extreme_change': 0,
        'long_suspension': 0,
    }

    for stock_code, group in df_clean.groupby('stock_code'):
        group = group.sort_values('date').reset_index(drop=True)

        # 5.1 最少交易日
        if len(group) < MIN_TRADING_DAYS:
            removed_reasons['too_few_days'] += 1
            continue

        # 5.2 最大连续停牌天数
        group['date_diff'] = group['date'].diff().dt.days
        max_gap = group['date_diff'].max()
        if max_gap > MAX_GAP_DAYS:
            removed_reasons['long_gap'] += 1
            continue

        # 5.3 单日涨跌幅异常
        group['daily_change'] = group['close'].pct_change().abs()
        extreme_changes = (group['daily_change'] > MAX_DAILY_CHANGE).sum()
        if extreme_changes > 5:  # 允许少量除权除息
            removed_reasons['extreme_change'] += 1
            continue

        # 5.4 长期停牌检查（连续20天volume=0超过2次）
        group['vol_zero_streak'] = (group['volume'] == 0).astype(int)
        group['vol_zero_streak'] = (
            group['vol_zero_streak']
            .groupby((group['vol_zero_streak'] != group['vol_zero_streak'].shift()).cumsum())
            .cumsum()
        )
        max_zero_streak = group['vol_zero_streak'].max()
        if max_zero_streak > 20:
            removed_reasons['long_suspension'] += 1
            continue

        # 计算质量指标
        trading_days = len(group)
        date_span = (group['date'].max() - group['date'].min()).days
        completeness = trading_days / max(date_span, 1)
        avg_volume = group['volume'].mean()

        stock_stats.append({
            'stock_code': stock_code,
            'trading_days': trading_days,
            'date_span': date_span,
            'completeness': completeness,
            'max_gap': max_gap,
            'extreme_changes': extreme_changes,
            'max_zero_streak': max_zero_streak,
            'avg_volume': avg_volume,
            'start_date': group['date'].min(),
            'end_date': group['date'].max(),
        })

    stats_df = pd.DataFrame(stock_stats)
    print(f"通过清洗的股票数: {len(stats_df)}")
    print(f"\n剔除原因统计:")
    for reason, count in removed_reasons.items():
        print(f"  {reason}: {count}")

    return stats_df, df_clean


def select_top500(stats_df, df_clean):
    """选择数据质量最好的 500 只股票"""
    print("\n" + "=" * 70)
    print("选择 Top 500 股票")
    print("=" * 70)

    # 排序：交易日多、完整度高、成交量大
    stats_df['score'] = (
        stats_df['trading_days'] * 0.5 +
        stats_df['completeness'] * 500 * 0.3 +
        np.log1p(stats_df['avg_volume']) * 0.2
    )
    stats_df = stats_df.sort_values('score', ascending=False).reset_index(drop=True)

    top500 = stats_df.head(OUTPUT_TOP_N)

    print(f"Top 500 股票:")
    print(f"  平均交易日: {top500['trading_days'].mean():.0f}")
    print(f"  最小交易日: {top500['trading_days'].min()}")
    print(f"  平均完整度: {top500['completeness'].mean():.3f}")
    print(f"  平均最大停牌: {top500['max_gap'].mean():.1f} 天")

    print(f"\n前 10 只股票:")
    print(top500[['stock_code', 'trading_days', 'completeness', 'start_date', 'end_date']].head(10).to_string(index=False))

    # 保存股票列表
    output_dir = Path(__file__).parent.parent / 'data'
    output_dir.mkdir(exist_ok=True)

    top500_list_path = output_dir / 'top500_stocks.txt'
    with open(top500_list_path, 'w') as f:
        for code in top500['stock_code']:
            f.write(code + '\n')
    print(f"\nTop 500 股票列表已保存: {top500_list_path}")

    # 保存清洗统计
    stats_path = output_dir / 'cleaning_stats.csv'
    stats_df.to_csv(stats_path, index=False)
    print(f"完整统计已保存: {stats_path}")

    # 计算清洗后样本数
    df_top500 = df_clean[df_clean['stock_code'].isin(top500['stock_code'])].copy()
    print(f"\nTop 500 样本数: {len(df_top500):,}")
    print(f"日期范围: {df_top500['date'].min()} ~ {df_top500['date'].max()}")

    return top500, df_top500


def main():
    print("=" * 70)
    print("DuckDB 数据清洗")
    print("=" * 70)
    print(f"数据库路径: {DB_PATH}")
    print(f"最少交易日: {MIN_TRADING_DAYS}")
    print(f"最大允许停牌: {MAX_GAP_DAYS} 天")
    print(f"最大单日涨跌: {MAX_DAILY_CHANGE * 100:.0f}%")

    if not DB_PATH.exists():
        print(f"[ERROR] 数据库不存在: {DB_PATH}")
        return

    con = connect_db()
    try:
        get_raw_stats(con)
        stats_df, df_clean = load_and_clean(con)
        if len(stats_df) > 0:
            select_top500(stats_df, df_clean)
        else:
            print("[ERROR] 没有股票通过清洗")
    finally:
        con.close()

    print("\n" + "=" * 70)
    print("清洗完成")
    print("=" * 70)


if __name__ == "__main__":
    main()
