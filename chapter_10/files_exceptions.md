# Chapter 10：文件和异常

> 面向有其他语言经验的开发者，聚焦 Python 特有语法和易混淆点。

## 目录

1. [读文件](#1-读文件)
2. [写文件](#2-写文件)
3. [文件路径（pathlib）](#3-文件路径pathlib)
4. [JSON 处理](#4-json-处理)
5. [异常处理](#5-异常处理)
6. [抛出异常](#6-抛出异常)
7. [常见内置异常](#7-常见内置异常)
8. [常见陷阱与其他语言对比](#8-常见陷阱与其他语言对比)

---

## 1. 读文件

> **[重点]** 使用 `with` 语句（上下文管理器），**自动关闭文件**，是 Python 标准写法。

```python
# 基本读取
with open("data.txt", "r", encoding="utf-8") as f:
    content = f.read()          # 全部读取为字符串

# 按行读取为列表
with open("data.txt", "r", encoding="utf-8") as f:
    lines = f.readlines()       # ["line1\n", "line2\n", ...]

# 逐行迭代（内存友好，推荐大文件）
with open("data.txt", "r", encoding="utf-8") as f:
    for line in f:
        print(line.strip())     # strip() 去除行尾换行符
```

> **[注意]** 始终指定 `encoding="utf-8"`，避免在不同操作系统上出现编码问题（Windows 默认 GBK）。

```python
# 读取二进制文件
with open("image.png", "rb") as f:     # "rb" = read binary
    data = f.read()
```

---

## 2. 写文件

```python
# 覆盖写（"w" 模式会清空原文件）
with open("output.txt", "w", encoding="utf-8") as f:
    f.write("第一行\n")
    f.write("第二行\n")

# 追加写（不清空原文件）
with open("output.txt", "a", encoding="utf-8") as f:
    f.write("追加的内容\n")

# 写多行
lines = ["行1", "行2", "行3"]
with open("output.txt", "w", encoding="utf-8") as f:
    f.writelines(f"{line}\n" for line in lines)
```

> **[陷阱]** `"w"` 模式会**立即清空**原文件，即使后续写入失败也已经清空。操作前确认路径和意图。

---

## 3. 文件路径（pathlib）

> **[重点]** Python 3.4+ 推荐用 `pathlib.Path` 处理路径，比字符串拼接更安全、跨平台。

```python
from pathlib import Path

# 基本用法
p = Path("data") / "input" / "file.txt"   # / 运算符拼接路径
p.exists()              # 是否存在
p.is_file()             # 是否是文件
p.is_dir()              # 是否是目录
p.suffix                # ".txt"（扩展名）
p.stem                  # "file"（不含扩展名的文件名）
p.name                  # "file.txt"（文件名）
p.parent                # data/input（父目录）

# 获取当前脚本所在目录（避免相对路径问题）
script_dir = Path(__file__).parent
data_file = script_dir / "data.json"

# 列出目录内容
for f in Path(".").iterdir():
    print(f)

# 查找文件
for f in Path(".").glob("**/*.py"):     # 递归查找所有 .py 文件
    print(f)

# 创建目录
Path("output/reports").mkdir(parents=True, exist_ok=True)

# 读写文件（Path 对象直接支持）
text = data_file.read_text(encoding="utf-8")
data_file.write_text("内容", encoding="utf-8")
```

---

## 4. JSON 处理

```python
import json

# Python 对象 → JSON 字符串
data = {"name": "Alice", "scores": [95, 87, 92], "active": True}
json_str = json.dumps(data)                          # 紧凑格式
json_str = json.dumps(data, indent=2, ensure_ascii=False)  # 格式化，支持中文

# JSON 字符串 → Python 对象
obj = json.loads(json_str)

# 写入文件
with open("data.json", "w", encoding="utf-8") as f:
    json.dump(data, f, indent=2, ensure_ascii=False)

# 从文件读取
with open("data.json", "r", encoding="utf-8") as f:
    obj = json.load(f)
```

> **[重点]** 区分：`json.dumps()` / `json.loads()` 处理字符串；`json.dump()` / `json.load()` 处理文件。

JSON 和 Python 类型对应关系：

| JSON | Python |
|------|--------|
| `object` | `dict` |
| `array` | `list` |
| `string` | `str` |
| `number` | `int` / `float` |
| `true/false` | `True/False` |
| `null` | `None` |

---

## 5. 异常处理

> **[重点]** Python 的 `try/except/else/finally` 中，`else` 块是 Python 特有的（Java/JS 没有）。

```python
try:
    result = int("abc")         # 可能抛出异常的代码
except ValueError as e:
    print(f"转换失败：{e}")     # 捕获到异常时执行
else:
    print(f"转换成功：{result}")    # 没有异常时执行（Python 特有！）
finally:
    print("始终执行（清理工作）")   # 无论如何都执行
```

### 捕获多个异常

```python
try:
    with open("data.txt") as f:
        data = json.load(f)
except FileNotFoundError:
    print("文件不存在")
except json.JSONDecodeError as e:
    print(f"JSON 格式错误：{e}")
except PermissionError:
    print("没有读取权限")
except (TypeError, ValueError) as e:    # 多个异常类型合并捕获
    print(f"数据类型错误：{e}")
```

> **[陷阱]** 不要使用裸 `except:`，它会捕获所有异常（包括 `KeyboardInterrupt`、`SystemExit`），导致程序难以退出：

```python
# 错误做法
try:
    risky_operation()
except:                   # 捕获一切，包括 Ctrl+C！
    pass

# 正确做法
try:
    risky_operation()
except Exception as e:    # 捕获所有非系统异常
    log_error(e)

# 或捕获具体类型
try:
    risky_operation()
except (ValueError, IOError) as e:
    handle_error(e)
```

---

## 6. 抛出异常

```python
# 抛出内置异常
def divide(a, b):
    if b == 0:
        raise ValueError("除数不能为零")
    return a / b

# 自定义异常（继承 Exception 或其子类）
class InsufficientFundsError(Exception):
    def __init__(self, amount: float, balance: float):
        self.amount = amount
        self.balance = balance
        super().__init__(f"余额不足：需要 {amount}，当前 {balance}")

# 使用自定义异常
def withdraw(balance, amount):
    if amount > balance:
        raise InsufficientFundsError(amount, balance)
    return balance - amount

# 重新抛出（在 except 块内）
try:
    withdraw(100, 200)
except InsufficientFundsError as e:
    log_error(e)
    raise              # 重新抛出，不改变原始堆栈
```

---

## 7. 常见内置异常

```python
FileNotFoundError       # 文件不存在
PermissionError         # 权限不足
IsADirectoryError       # 期望文件，得到目录

ValueError              # 值不合法（int("abc")）
TypeError               # 类型不对（"a" + 1）
KeyError                # 字典 key 不存在
IndexError              # 列表索引越界
AttributeError          # 访问不存在的属性
NameError               # 变量名未定义

ZeroDivisionError       # 除以零
OverflowError           # 数值溢出（Python int 不会，float 可能）
RecursionError          # 递归深度超限

StopIteration           # 迭代器耗尽
RuntimeError            # 运行时错误（通用）
NotImplementedError     # 子类未实现抽象方法
```

---

## 8. 常见陷阱与其他语言对比

| 特性 | Python | Java/JS/Go |
|------|--------|------------|
| 文件自动关闭 | `with open(...) as f:` | try-finally / using |
| 路径处理 | `pathlib.Path` / `/` 运算符 | `File` / `path.join()` |
| JSON 读写 | `json` 标准库 | `gson` / `JSON.parse()` |
| try-else | Python 特有 | 无对应 |
| 裸 except | 危险，别用 | catch(Exception) 类似 |
| 自定义异常 | 继承 `Exception` | extends Exception |
| 强制编码声明 | `encoding="utf-8"` | 需要注意 |
