#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
从 QMT 导入 A 股日线数据到 DuckDB
用于验证 EasyXT 的 LightGBM 方案
"""

import sys
import os
import re
import time
from datetime import datetime

# 项目路径
project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, project_root)

from easy_xt import get_api
from easy_xt.config import config
# 直接导入 unified_duckdb_manager，绕过 data_manager/__init__.py 的依赖检查
import importlib.util
manager_path = os.path.join(project_root, 'data_manager', 'unified_duckdb_manager.py')
spec = importlib.util.spec_from_file_location("unified_duckdb_manager", manager_path)
manager_module = importlib.util.module_from_spec(spec)
sys.modules["unified_duckdb_manager"] = manager_module
spec.loader.exec_module(manager_module)
UnifiedDuckDBManager = manager_module.UnifiedDuckDBManager

# 配置
QMT_PATH = r'D:\国金证券QMT交易端'
START_DATE = '2020-01-01'
END_DATE = '2023-12-31'
PERIOD = '1d'
DATA_SOURCE = 'qmt'


def is_a_stock(code: str) -> bool:
    """过滤 A 股股票"""
    if not code:
        return False
    code = code.upper().strip()
    if not re.match(r'^\d{6}\.(SH|SZ|BJ)$', code):
        return False
    num = code[:6]
    # 沪市主板
    if code.endswith('.SH') and num[:3] in ('600', '601', '603', '605'):
        return True
    # 科创板
    if code.endswith('.SH') and num[:3] in ('688', '689'):
        return True
    # 深市主板/中小板
    if code.endswith('.SZ') and num[:3] in ('000', '001', '002', '003'):
        return True
    # 创业板
    if code.endswith('.SZ') and num[:3] in ('300', '301'):
        return True
    # 北交所
    if code.endswith('.BJ') and num[:2] in ('43', '83', '87'):
        return True
    return False


def main():
    print("=" * 70)
    print("QMT -> DuckDB 数据导入")
    print("=" * 70)
    print(f"QMT 路径: {QMT_PATH}")
    print(f"日期范围: {START_DATE} ~ {END_DATE}")
    print(f"数据周期: {PERIOD}")
    print()

    # 1. 设置 QMT 路径
    config.set_qmt_path(QMT_PATH)

    # 2. 初始化 QMT 数据服务
    api = get_api()
    ok = api.init_data()
    if not ok:
        print("[ERROR] QMT 数据服务初始化失败")
        return

    # 3. 获取 A 股列表
    print("\n[1/4] 获取 A 股列表...")
    all_stocks = api.get_stock_list('A股')
    print(f"  原始列表: {len(all_stocks)} 只")

    stock_pool = [s for s in all_stocks if is_a_stock(s)]
    print(f"  A 股股票: {len(stock_pool)} 只")
    print(f"  示例: {stock_pool[:5]}")

    # 4. 初始化 DuckDB
    print("\n[2/4] 初始化 DuckDB...")
    manager = UnifiedDuckDBManager(threads=4, memory_limit='4GB')
    print(f"  数据库路径: {manager.db_path}")

    # 5. 批量下载数据
    print("\n[3/4] 开始下载数据...")
    t0 = time.time()

    # 分批处理，避免内存问题
    batch_size = 500
    total_success = 0
    total_failed = 0
    failed_stocks = []

    for batch_idx in range(0, len(stock_pool), batch_size):
        batch = stock_pool[batch_idx:batch_idx + batch_size]
        print(f"\n  批次 {batch_idx // batch_size + 1}/{(len(stock_pool) - 1) // batch_size + 1}: "
              f"{batch_idx + 1}-{min(batch_idx + batch_size, len(stock_pool))} ({len(batch)} 只)")

        results = manager.download_data(
            symbols=batch,
            start_date=START_DATE,
            end_date=END_DATE,
            period=PERIOD,
            data_source=DATA_SOURCE,
        )

        success = len(results)
        failed = len(batch) - success
        total_success += success
        total_failed += failed

        for s in batch:
            if s not in results:
                failed_stocks.append(s)

        print(f"    成功: {success}, 失败: {failed}, 累计成功: {total_success}")

    elapsed = time.time() - t0

    # 6. 统计
    print("\n[4/4] 数据统计...")
    try:
        count = manager.conn.execute("SELECT COUNT(*) FROM stock_data").fetchone()[0]
        stocks_in_db = manager.conn.execute(
            "SELECT COUNT(DISTINCT symbol) FROM stock_data"
        ).fetchone()[0]
        date_range = manager.conn.execute(
            "SELECT MIN(date), MAX(date) FROM stock_data"
        ).fetchone()
        print(f"  总记录数: {count:,}")
        print(f"  股票数量: {stocks_in_db}")
        print(f"  日期范围: {date_range[0]} ~ {date_range[1]}")
    except Exception as e:
        print(f"  统计失败: {e}")

    print("\n" + "=" * 70)
    print("导入完成")
    print("=" * 70)
    print(f"总股票: {len(stock_pool)}")
    print(f"成功: {total_success}")
    print(f"失败: {total_failed}")
    print(f"耗时: {elapsed:.1f} 秒 ({elapsed / 60:.1f} 分钟)")
    if failed_stocks:
        print(f"失败示例: {failed_stocks[:10]}")


if __name__ == "__main__":
    main()
