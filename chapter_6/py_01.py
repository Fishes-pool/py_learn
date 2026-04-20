"""
Demo: 多环境配置管理器
场景：项目需要根据运行环境（dev/staging/prod）加载不同配置，支持默认值、环境覆盖、敏感信息过滤。
演示：字典定义、安全访问、遍历、推导式、合并、嵌套字典、defaultdict。
"""

from collections import defaultdict

# ---- 1. 默认配置（基础层）----
BASE_CONFIG = {
    "app": {
        "name": "MyApp",
        "version": "1.0.0",
        "debug": False,
        "log_level": "INFO",
    },
    "database": {
        "host": "localhost",
        "port": 5432,
        "pool_size": 5,
        "timeout": 30,
    },
    "cache": {
        "backend": "memory",
        "ttl": 300,
    },
    "features": {
        "enable_metrics": False,
        "enable_tracing": False,
    }
}

# ---- 2. 环境特定配置（覆盖层）----
ENV_CONFIGS = {
    "dev": {
        "app": {"debug": True, "log_level": "DEBUG"},
        "database": {"host": "localhost", "pool_size": 2},
        "features": {"enable_metrics": True},
    },
    "staging": {
        "app": {"log_level": "WARNING"},
        "database": {"host": "staging-db.internal", "pool_size": 10},
        "features": {"enable_metrics": True, "enable_tracing": True},
    },
    "prod": {
        "app": {"log_level": "ERROR"},
        "database": {"host": "prod-db.internal", "port": 5433, "pool_size": 20},
        "cache": {"backend": "redis", "ttl": 3600},
        "features": {"enable_metrics": True, "enable_tracing": True},
    },
}

# ---- 3. 敏感字段（不允许打印的 key）----
SENSITIVE_KEYS = {"password", "secret", "token", "api_key"}


def merge_config(base: dict, override: dict) -> dict:
    """递归合并配置字典，override 的值覆盖 base。"""
    result = base.copy()
    for key, value in override.items():
        if key in result and isinstance(result[key], dict) and isinstance(value, dict):
            result[key] = merge_config(result[key], value)
        else:
            result[key] = value
    return result


def get_config(env: str) -> dict:
    """获取指定环境的完整配置。"""
    env_override = ENV_CONFIGS.get(env, {})   # get 安全访问，不存在返回空字典
    return merge_config(BASE_CONFIG, env_override)


def filter_sensitive(config: dict) -> dict:
    """过滤掉敏感字段，返回可打印的配置（字典推导式递归过滤）。"""
    return {
        k: filter_sensitive(v) if isinstance(v, dict) else "***"
        if k in SENSITIVE_KEYS else v
        for k, v in config.items()
    }


def print_config(config: dict, indent: int = 0) -> None:
    """递归打印配置字典。"""
    for key, value in config.items():             # 遍历 key-value
        prefix = "  " * indent
        if isinstance(value, dict):
            print(f"{prefix}{key}:")
            print_config(value, indent + 1)
        else:
            print(f"{prefix}{key}: {value}")


def analyze_configs() -> dict:
    """分析所有环境配置的差异，用 defaultdict 收集统计。"""
    diff_tracker = defaultdict(list)             # 默认值为列表

    for env in ENV_CONFIGS:
        cfg = get_config(env)
        # 字典推导式：提取所有 app 级别的配置项
        app_cfg = {k: v for k, v in cfg["app"].items() if k != "name"}
        for key, value in app_cfg.items():
            diff_tracker[key].append(f"{env}={value}")

    return dict(diff_tracker)


# ---- 主程序 ----
print("=" * 55)
print("多环境配置管理器")
print("=" * 55)

# 展示各环境配置
for env_name in ["dev", "staging", "prod"]:
    print(f"\n【{env_name.upper()} 环境配置】")
    cfg = get_config(env_name)
    safe_cfg = filter_sensitive(cfg)             # 过滤敏感字段
    print_config(safe_cfg)

# 分析各环境差异
print("\n【各环境 App 配置差异分析】")
diff = analyze_configs()
for key, values in diff.items():
    print(f"  {key}: {' | '.join(values)}")

# 字典合并演示（Python 3.9+）
print("\n【字典合并演示】")
a = {"x": 1, "y": 2}
b = {"y": 99, "z": 3}
merged = a | b                    # 后面的 b 覆盖前面的 a
print(f"  a | b = {merged}")

# 字典推导式：提取 prod 环境中所有 feature 开关
prod_cfg = get_config("prod")
enabled_features = [
    feature for feature, enabled in prod_cfg["features"].items()
    if enabled
]
print(f"\n【Prod 已启用功能】: {enabled_features}")

# setdefault 演示
runtime_data = {}
runtime_data.setdefault("request_count", 0)
runtime_data["request_count"] += 1
runtime_data.setdefault("errors", [])
runtime_data["errors"].append("404 Not Found")
print(f"\n【运行时数据】: {runtime_data}")
