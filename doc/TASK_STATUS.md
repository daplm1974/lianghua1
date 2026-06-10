# EasyXT LightGBM 项目 - 任务状态跟踪

## 当前会话完成的工作

### 1. 环境搭建 ✅
- [x] EasyXT 项目克隆到 `C:\Users\dap_c\Desktop\test_opensquilla\`
- [x] xtquant 特殊版解压到 `xtquant/` 目录
- [x] easy_xt 核心库安装到 qmt conda 环境
- [x] 依赖安装：duckdb, lightgbm, scipy, scikit-learn
- [x] QMT 路径配置：`D:\国金证券QMT交易端`
- [x] 编码修复：emoji 替换为 ASCII，避免 Windows GBK 报错

### 2. 数据导入 ✅
- [x] 从 QMT 获取 A 股列表（5206 只）
- [x] 批量下载日线数据到 DuckDB
- [x] 结果：5006 只成功，200 只失败
- [x] 总记录数：4,215,845 条
- [x] 日期范围：2020-01-02 ~ 2023-12-29
- [x] 数据库大小：~400MB

### 3. 数据清洗 ✅
- [x] 编写 `scripts/data_cleaning.py`
- [x] 清洗规则：去缺失、去无效价格、去重、最少500交易日、最大停牌60天、涨跌幅<20%
- [x] 通过清洗：4206 只
- [x] 选出 Top 500（按完整度排序）
- [x] Top 500 平均交易日：970 天
- [x] 保存 `data/top500_stocks.txt`

### 4. LightGBM 训练 ✅
- [x] 绕过 `easyxt_backtest` 的 backtrader 依赖，直接加载 trainer.py
- [x] 训练参数：n_estimators=100, lr=0.1, label_horizon=5
- [x] 训练集：2022-01-01 ~ 2022-12-31（121,000 条）
- [x] 验证集：2023-01-01 ~ 2023-06-30（59,000 条）
- [x] 实际跑了 62 个因子（fast_mode 未生效）
- [x] 训练样本：87,418，验证样本：26,397
- [x] 保存模型：`models/lightgbm_v1.pkl`

### 5. 结果分析 ✅
- [x] IC = 0.0598（PPT: 0.062）✅ 基本吻合
- [x] Rank_IC = 0.0592
- [x] Top20%-Bottom20% = 0.785%（PPT: 0.53%）✅ 更好
- [x] 训练耗时：3.6 秒（PPT: 4 秒）✅ 更快
- [x] 因子重要性分析：62 个因子完整排序
- [x] 发现：PPT 17 个因子只占 19.7% 重要性，80% 来自扩展因子

### 6. 文档生成 ✅
- [x] `doc/PROJECT_STATUS.md` - 项目状态报告
- [x] `doc/ARCHITECTURE_DESIGN.md` - 中间交互层架构设计

---

## 待办任务（按优先级）

### 高优先级

- [ ] **修复 backtrader 依赖**
  - 问题：`easyxt_backtest/__init__.py` 强制导入 backtrader，导致正常 import 失败
  - 方案 A：`pip install backtrader`
  - 方案 B：修改 `__init__.py`，延迟导入或设为可选
  - 影响：不修复无法通过正常方式使用 easyxt_backtest 模块

- [ ] **严格按 PPT 17 因子重新训练**
  - 问题：实际跑了 62 个因子，不是 PPT 的 17 个
  - 原因：`compute_features()` 没传 `fast_mode=True`
  - 方案：修改 trainer.py 或调用时传 `fast_mode=True`
  - 目标：验证 PPT 的 baseline 效果

### 中优先级

- [ ] **扩展数据到最新日期**
  - 当前数据：2020-01-02 ~ 2023-12-29
  - QMT 实际有到：2026-06-10
  - 方案：修改导入脚本，重新导入 2020-2026 数据
  - 影响：训练集可扩展到 2024-2025，验证用 2026

- [ ] **实现中间交互层（Orchestrator）**
  - 设计文档：`doc/ARCHITECTURE_DESIGN.md`
  - 模块：StateManager, TaskScheduler, HealthChecker, ErrorHandler, EventBus, VersionControl
  - 目标：解耦 UI 与业务逻辑，支持状态恢复

- [ ] **对接原项目 UI**
  - PyQt5 GUI：`gui_app/main_window.py`
  - Streamlit Web：`easyxt_backtest/web_app/streamlit_app.py`
  - 方案：用 Orchestrator 替换直接调用

### 低优先级

- [ ] **修复 `close_position` 名字不匹配**
  - PPT 叫 `close_position`，代码叫 `close_pos_10/20/60`
  - 影响：PPT 17 因子名不对应

- [ ] **终端编码问题**
  - Windows GBK 不支持 emoji，日志显示乱码
  - 不影响功能，仅美观问题

---

## 关键文件路径

```
C:\Users\dap_c\Desktop\test_opensquilla\
├── data\
│   ├── stock_data.ddb              # DuckDB 数据库
│   ├── top500_stocks.txt           # 500 只股票列表
│   └── cleaning_stats.csv          # 清洗统计
├── models\
│   └── lightgbm_v1.pkl             # 训练好的模型
├── scripts\
│   ├── import_qmt_to_duckdb.py     # 数据导入脚本
│   └── data_cleaning.py            # 数据清洗脚本
├── logs\
│   ├── import_qmt_to_duckdb.log    # 导入日志
│   ├── data_cleaning.log           # 清洗日志
│   ├── train_v1.log                # 训练日志
│   ├── feature_importance.log      # 因子重要性
│   └── all_factors_rank.log        # 完整因子排序
├── doc\
│   ├── PROJECT_STATUS.md           # 项目状态
│   ├── ARCHITECTURE_DESIGN.md      # 架构设计
│   └── TASK_STATUS.md              # 本文件
└── easyxt_backtest\
    └── ml\
        ├── trainer.py              # 训练器
        └── predictor.py            # 预测器
```

---

## 环境信息

| 项目 | 值 |
|:---|:---|
| Python | `C:\Users\dap_c\miniconda3\envs\qmt\python.exe` |
| QMT 路径 | `D:\国金证券QMT交易端` |
| 数据库 | `data/stock_data.ddb` (~400MB) |
| 关键包 | duckdb 1.5.3, lightgbm 4.6.0, scipy 1.17.1 |

---

## 重启后恢复步骤

1. 激活 qmt 环境：`conda activate qmt`
2. 进入项目目录：`cd C:\Users\dap_c\Desktop\test_opensquilla`
3. 检查 QMT 连接：运行测试脚本
4. 加载已有模型：`models/lightgbm_v1.pkl`
5. 继续未完成任务（见上方待办列表）
