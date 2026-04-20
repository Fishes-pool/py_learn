"""
Demo: 日志分析工具
场景：读取 JSON Lines 格式的日志文件，统计错误级别分布，将结果写入报告文件。
演示：with open、pathlib.Path、json、try/except/else/finally、自定义异常。
"""

import json
from pathlib import Path
from collections import defaultdict
from datetime import datetime


# ---- 自定义异常 ----
class LogParseError(Exception):
    def __init__(self, line_num: int, content: str, reason: str):
        self.line_num = line_num
        self.content = content
        self.reason = reason
        super().__init__(f"第 {line_num} 行解析失败：{reason}")


# ---- 示例日志数据（写入临时文件演示）----
SAMPLE_LOGS = [
    {"timestamp": "2024-01-01T10:00:00", "level": "INFO",    "service": "auth",    "message": "用户 alice 登录成功"},
    {"timestamp": "2024-01-01T10:01:00", "level": "WARNING", "service": "auth",    "message": "登录失败：密码错误"},
    {"timestamp": "2024-01-01T10:02:00", "level": "ERROR",   "service": "db",      "message": "数据库连接超时"},
    {"timestamp": "2024-01-01T10:03:00", "level": "INFO",    "service": "api",     "message": "GET /users 200"},
    {"timestamp": "2024-01-01T10:04:00", "level": "ERROR",   "service": "payment", "message": "支付接口异常：timeout"},
    {"timestamp": "2024-01-01T10:05:00", "level": "DEBUG",   "service": "api",     "message": "处理请求耗时 45ms"},
    {"timestamp": "2024-01-01T10:06:00", "level": "CRITICAL","service": "db",      "message": "主库宕机，切换从库"},
    {"timestamp": "2024-01-01T10:07:00", "level": "ERROR",   "service": "auth",    "message": "JWT 验证失败"},
    {"timestamp": "2024-01-01T10:08:00", "level": "INFO",    "service": "payment", "message": "订单 #1001 支付成功"},
    {"timestamp": "2024-01-01T10:09:00", "level": "WARNING", "service": "api",     "message": "请求频率超过限制"},
    "这是一条损坏的日志行",           # 故意插入的非 JSON 数据
    {"timestamp": "2024-01-01T10:11:00", "level": "INFO",    "message": "缺少 service 字段"},  # 不完整的记录
]

# ---- 路径设置（基于脚本目录）----
SCRIPT_DIR = Path(__file__).parent
LOG_FILE = SCRIPT_DIR / "sample.log"
REPORT_FILE = SCRIPT_DIR / "report.txt"


def write_sample_logs(filepath: Path, logs: list) -> None:
    """将示例日志写入 JSON Lines 文件（每行一个 JSON 对象）。"""
    with open(filepath, "w", encoding="utf-8") as f:
        for entry in logs:
            if isinstance(entry, dict):
                f.write(json.dumps(entry, ensure_ascii=False) + "\n")
            else:
                f.write(str(entry) + "\n")   # 故意写入非 JSON 数据


def parse_log_line(line: str, line_num: int) -> dict:
    """解析单行日志，失败时抛出 LogParseError。"""
    line = line.strip()
    if not line:
        raise LogParseError(line_num, line, "空行")

    try:
        record = json.loads(line)
    except json.JSONDecodeError as e:
        raise LogParseError(line_num, line, f"JSON 格式错误：{e}") from e

    if not isinstance(record, dict):
        raise LogParseError(line_num, line, "记录不是 JSON 对象")

    required_fields = {"timestamp", "level", "message"}
    missing = required_fields - record.keys()
    if missing:
        raise LogParseError(line_num, line, f"缺少字段：{missing}")

    return record


def analyze_logs(filepath: Path) -> dict:
    """
    读取并分析日志文件。
    返回：{
        "level_stats": {...},
        "service_stats": {...},
        "error_records": [...],
        "parse_errors": [...],
        "total": int,
    }
    """
    level_stats = defaultdict(int)
    service_stats = defaultdict(int)
    error_records = []
    parse_errors = []
    total = 0

    try:
        f = open(filepath, "r", encoding="utf-8")
    except FileNotFoundError:
        print(f"[ERROR] 日志文件不存在：{filepath}")
        return {}
    except PermissionError:
        print(f"[ERROR] 没有权限读取：{filepath}")
        return {}

    try:
        for line_num, line in enumerate(f, start=1):
            total += 1
            try:
                record = parse_log_line(line, line_num)
                level = record["level"]
                service = record.get("service", "unknown")   # 安全访问

                level_stats[level] += 1
                service_stats[service] += 1

                if level in ("ERROR", "CRITICAL"):
                    error_records.append(record)

            except LogParseError as e:
                parse_errors.append(str(e))     # 记录解析错误，继续处理下一行
    finally:
        f.close()                               # 无论是否异常，始终关闭文件

    return {
        "level_stats": dict(level_stats),
        "service_stats": dict(service_stats),
        "error_records": error_records,
        "parse_errors": parse_errors,
        "total": total,
    }


def write_report(filepath: Path, result: dict) -> None:
    """将分析结果写入报告文件。"""
    if not result:
        return

    with open(filepath, "w", encoding="utf-8") as f:
        now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        f.write(f"日志分析报告 - 生成时间：{now}\n")
        f.write("=" * 55 + "\n\n")

        # 级别统计
        f.write("【日志级别统计】\n")
        level_order = ["CRITICAL", "ERROR", "WARNING", "INFO", "DEBUG"]
        for level in level_order:
            count = result["level_stats"].get(level, 0)
            bar = "█" * count
            f.write(f"  {level:10s}: {count:3d}  {bar}\n")

        # 服务统计
        f.write("\n【服务调用统计】\n")
        sorted_services = sorted(
            result["service_stats"].items(),
            key=lambda x: x[1],
            reverse=True,
        )
        for service, count in sorted_services:
            f.write(f"  {service:15s}: {count} 次\n")

        # 错误记录
        f.write(f"\n【错误与严重告警（{len(result['error_records'])} 条）】\n")
        for rec in result["error_records"]:
            f.write(f"  [{rec['level']}] {rec.get('service','?')} - {rec['message']}\n")

        # 解析失败
        f.write(f"\n【解析失败（{len(result['parse_errors'])} 条）】\n")
        for err in result["parse_errors"]:
            f.write(f"  ⚠ {err}\n")

        # 摘要
        f.write(f"\n共处理 {result['total']} 行，其中 "
                f"{len(result['parse_errors'])} 行解析失败。\n")


# ---- 主程序 ----
if __name__ == "__main__":
    print("=" * 50)
    print("日志分析工具")
    print("=" * 50)

    # 1. 写入示例日志
    write_sample_logs(LOG_FILE, SAMPLE_LOGS)
    print(f"示例日志已写入：{LOG_FILE}")

    # 2. 分析日志
    result = analyze_logs(LOG_FILE)

    if result:
        # 3. 写入报告
        write_report(REPORT_FILE, result)
        print(f"分析报告已写入：{REPORT_FILE}")

        # 4. 控制台输出摘要
        print(f"\n处理总行数：{result['total']}")
        print(f"解析失败：{len(result['parse_errors'])} 行")
        print("\n日志级别分布：")
        for level, count in sorted(result["level_stats"].items()):
            print(f"  {level}: {count}")

        print("\n错误日志：")
        for rec in result["error_records"]:
            print(f"  [{rec['level']}] {rec['message']}")

        # 5. 读回报告内容演示（try/except/else）
        print("\n--- 报告文件内容 ---")
        try:
            content = REPORT_FILE.read_text(encoding="utf-8")  # pathlib 直接读取
        except FileNotFoundError:
            print("报告文件不存在")
        except PermissionError:
            print("无读取权限")
        else:
            # else：没有异常时执行
            print(content)
