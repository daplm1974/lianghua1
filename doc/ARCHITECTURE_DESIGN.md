# 中间交互层架构设计文档

## 一、设计目标

1. **解耦**：UI 层与业务逻辑层分离
2. **可观测**：每步执行状态可追溯
3. **可恢复**：中断后可从断点继续
4. **可扩展**：新模块可插拔注册

## 二、整体架构

```
┌─────────────────────────────────────────────────────────┐
│                    用户交互层                             │
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────────┐ │
│  │  PyQt5 GUI  │  │ Streamlit   │  │  CLI / Jupyter  │ │
│  │  (桌面)      │  │  (Web)      │  │  (脚本)         │ │
│  └──────┬──────┘  └──────┬──────┘  └────────┬────────┘ │
│         │                │                   │          │
│         └────────────────┼───────────────────┘          │
│                          ▼                              │
│         ┌────────────────────────────────────┐          │
│         │      统一 API 网关层 (API Gateway)   │          │
│         │  - 参数校验、权限控制、日志记录        │          │
│         │  - 统一返回格式 {status, data, error} │          │
│         └────────────────┬───────────────────┘          │
│                          ▼                              │
│         ┌────────────────────────────────────┐          │
│         │    中间交互层 (Orchestrator)        │          │
│         │                                    │          │
│         │  ┌──────────┐  ┌──────────────┐   │          │
│         │  │ 状态机   │  │ 任务调度器    │   │          │
│         │  │ StateMgr │  │ TaskScheduler│   │          │
│         │  └──────────┘  └──────────────┘   │          │
│         │                                    │          │
│         │  ┌──────────┐  ┌──────────────┐   │          │
│         │  │ 健康检查 │  │ 错误恢复      │   │          │
│         │  │ HealthChk│  │ ErrorHandler │   │          │
│         │  └──────────┘  └──────────────┘   │          │
│         │                                    │          │
│         │  ┌──────────┐  ┌──────────────┐   │          │
│         │  │ 版本控制 │  │ 事件总线      │   │          │
│         │  │ Version  │  │ EventBus     │   │          │
│         │  └──────────┘  └──────────────┘   │          │
│         └────────────────┬───────────────────┘          │
│                          │                              │
│         ┌────────────────┼────────────────┐             │
│         ▼                ▼                ▼             │
│    ┌────────┐      ┌────────┐      ┌────────┐         │
│    │ 数据层  │      │ 模型层  │      │ 回测层  │         │
│    │DuckDB  │      │LGBM    │      │引擎    │         │
│    └────────┘      └────────┘      └────────┘         │
└─────────────────────────────────────────────────────────┘
```

## 三、核心模块接口

### 3.1 StateManager（状态管理器）

```python
class StateManager:
    """统一管理所有状态，支持持久化和恢复"""
    
    def get(self, key: str, default=None) -> Any
    def set(self, key: str, value: Any, persist: bool = True)
    def get_config(self) -> Dict
    def set_config(self, config: Dict)
    def get_data_version(self) -> str
    def get_model_version(self) -> str
    def snapshot(self) -> str  # 生成状态快照ID
    def restore(self, snapshot_id: str) -> bool
```

### 3.2 TaskScheduler（任务调度器）

```python
class TaskScheduler:
    """任务队列、异步执行、进度回调"""
    
    def register_task(self, name: str, handler: Callable)
    def submit(self, task_name: str, params: Dict, callback: Callable = None) -> TaskID
    def get_status(self, task_id: TaskID) -> TaskStatus
    def get_progress(self, task_id: TaskID) -> float  # 0.0 ~ 1.0
    def cancel(self, task_id: TaskID) -> bool
    def list_running(self) -> List[TaskID]
```

### 3.3 HealthChecker（健康检查）

```python
class HealthChecker:
    """前置检查，生成健康报告"""
    
    def check_all(self) -> HealthReport
    def check_qmt(self) -> CheckResult
    def check_duckdb(self) -> CheckResult
    def check_dependencies(self) -> CheckResult
    def check_data_integrity(self) -> CheckResult
```

### 3.4 ErrorHandler（错误处理）

```python
class ErrorHandler:
    """统一错误处理、降级策略"""
    
    def handle(self, error: Exception, context: Dict) -> ErrorResponse
    def fallback(self, task_name: str, params: Dict) -> Any
    def notify(self, message: str, level: str = "warning")
    def retry(self, task_id: TaskID, max_retries: int = 3) -> bool
```

### 3.5 EventBus（事件总线）

```python
class EventBus:
    """模块间解耦通信"""
    
    def subscribe(self, event_type: str, handler: Callable)
    def publish(self, event_type: str, payload: Dict)
    def unsubscribe(self, event_type: str, handler: Callable)
```

## 四、与原项目 UI 的对接

### 4.1 PyQt5 GUI 对接

```python
# 原：直接调用 easy_xt
api = easy_xt.get_api()
api.init_data()

# 新：通过 Orchestrator
from orchestrator import Orchestrator
orch = Orchestrator()

# 健康检查
report = orch.health.check_all()
if not report.all_passed:
    show_error_dialog(report.failures)

# 执行任务
job = orch.submit('data.import', {
    'stock_pool': stock_list,
    'start_date': '2020-01-01',
    'end_date': '2023-12-31'
})

# 进度回调（PyQt5 信号槽）
job.on_progress.connect(update_progress_bar)
job.on_complete.connect(show_result)
```

### 4.2 Streamlit Web 对接

```python
# 原：直接调用 backtest engine
result = run_enhanced_backtest(config)

# 新：通过 Orchestrator
orch = Orchestrator()

# 提交任务
job = orch.submit('backtest.run', config=config)

# 轮询进度（Streamlit）
progress_bar = st.progress(0)
while job.status == 'running':
    progress_bar.progress(job.get_progress())
    time.sleep(0.5)

# 显示结果
if job.status == 'completed':
    st.success(f"IC: {job.result['IC']}")
```

## 五、任务注册表

| 任务名 | 模块 | 参数 | 输出 |
|:---|:---|:---|:---|
| `data.import` | DataPipeline | stock_pool, start_date, end_date | DuckDB 记录数 |
| `data.clean` | DataPipeline | min_trading_days, max_gap | 清洗后股票列表 |
| `data.validate` | DataPipeline | - | 数据质量报告 |
| `model.train` | ModelPipeline | stock_pool, train_start, train_end | 模型文件 + 指标 |
| `model.predict` | ModelPipeline | date, stock_pool | 预测分数 DataFrame |
| `model.evaluate` | ModelPipeline | model_path, valid_start, valid_end | IC, RankIC, 分层收益 |
| `backtest.run` | BacktestEngine | config, start_date, end_date | 回测报告 |
| `report.generate` | ReportGenerator | backtest_result | HTML/PDF 报告 |

## 六、状态持久化格式

```json
{
  "version": "1.0",
  "timestamp": "2026-06-10T15:30:00",
  "state": {
    "config": {
      "qmt_path": "D:\\国金证券QMT交易端",
      "db_path": "data/stock_data.ddb"
    },
    "data": {
      "version": "v1",
      "imported_at": "2026-06-10T14:46:00",
      "total_stocks": 5006,
      "total_records": 4215845
    },
    "model": {
      "version": "v1",
      "trained_at": "2026-06-10T15:00:00",
      "path": "models/lightgbm_v1.pkl",
      "metrics": {
        "IC": 0.0598,
        "Rank_IC": 0.0592
      }
    }
  },
  "tasks": {
    "task_001": {
      "name": "data.import",
      "status": "completed",
      "started_at": "...",
      "completed_at": "...",
      "result": {...}
    }
  }
}
```

## 七、错误降级策略

| 场景 | 降级策略 |
|:---|:---|
| QMT 未连接 | 使用 DuckDB 本地数据，提示用户 |
| DuckDB 数据缺失 | 自动触发数据导入任务 |
| 模型文件损坏 | 回滚到上一版本模型 |
| 内存不足 | 分批处理，减少 batch_size |
| 训练失败 | 自动降低 n_estimators 重试 |

## 八、文件规划

```
test_opensquilla/
├── orchestrator/              # 中间交互层（新增）
│   ├── __init__.py
│   ├── api_gateway.py         # API 网关
│   ├── state_manager.py       # 状态管理
│   ├── task_scheduler.py      # 任务调度
│   ├── health_checker.py      # 健康检查
│   ├── error_handler.py       # 错误处理
│   ├── event_bus.py           # 事件总线
│   └── version_control.py     # 版本控制
├── gui_app/                   # PyQt5 GUI（已有）
├── easyxt_backtest/web_app/   # Streamlit Web（已有）
├── doc/                       # 文档（新增）
│   ├── PROJECT_STATUS.md
│   └── ARCHITECTURE_DESIGN.md
└── ...
```
