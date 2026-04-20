# Chapter 2：变量和简单数据类型

> 面向有其他语言经验的开发者，聚焦 Python 特有语法和易混淆点。

## 目录

1. [变量命名规则](#1-变量命名规则)
2. [字符串](#2-字符串)
3. [数字](#3-数字)
4. [类型转换](#4-类型转换)
5. [None](#5-none)
6. [常量惯例](#6-常量惯例)
7. [常见陷阱与其他语言对比](#7-常见陷阱与其他语言对比)

---

## 1. 变量命名规则

Python 使用 **snake_case**（下划线命名），不使用 camelCase。

```python
# 推荐
user_name = "Alice"
max_retry_count = 3

# 不推荐（虽然合法）
userName = "Alice"
MaxRetryCount = 3  # 这是类名惯例
```

- `_var`：约定为内部使用（类似 protected）
- `__var`：在类中触发名称改写（name mangling）
- `__var__`：Python 保留的特殊方法/属性（dunder）

---

## 2. 字符串

### 2.1 定义方式

```python
s1 = 'single quotes'
s2 = "double quotes"         # 单双引号完全等价
s3 = "It's a string"        # 内含单引号时用双引号
s4 = 'Say "hello"'          # 内含双引号时用单引号

# 三引号：多行字符串
s5 = """
Line 1
Line 2
Line 3
"""
```

### 2.2 f-string（Python 3.6+）

> **[重点]** f-string 内可嵌入任意 Python 表达式，不只是变量名。

```python
name = "alice"
age = 26

# 基本用法
print(f"Name: {name}, Age: {age}")

# 表达式
print(f"Name: {name.upper()}")       # 方法调用
print(f"Result: {2 + 2}")            # 运算
print(f"Formatted: {age:03d}")       # 格式化（补零到3位）
print(f"Pi: {3.14159:.2f}")          # 小数位数控制
```

> **[注意]** Python 3.5 及以前使用 `.format()` 或 `%`，现代代码统一用 f-string。

```python
# 旧写法（了解即可）
"Hello, {}".format(name)
"Hello, %s" % name
```

### 2.3 常用字符串方法

```python
s = "  Hello, World!  "

s.upper()           # "  HELLO, WORLD!  "
s.lower()           # "  hello, world!  "
s.title()           # "  Hello, World!  "（每个单词首字母大写）

s.strip()           # "Hello, World!"（去除两端空白）
s.lstrip()          # "Hello, World!  "（去除左侧）
s.rstrip()          # "  Hello, World!"（去除右侧）

s.replace("World", "Python")   # "  Hello, Python!  "
s.split(",")                   # ["  Hello", " World!  "]
",".join(["a", "b", "c"])      # "a,b,c"

"hello".startswith("he")       # True
"hello".endswith("lo")         # True
"hello".find("ll")             # 2（返回索引，-1 表示未找到）
"hello".count("l")             # 2
```

> **[重点]** `removeprefix()` / `removesuffix()`（Python 3.9+）

```python
url = "https://example.com"
url.removeprefix("https://")     # "example.com"

filename = "report.pdf"
filename.removesuffix(".pdf")    # "report"
```

> **[注意]** 字符串是**不可变的**（immutable），所有方法都返回新字符串，不修改原字符串。

---

## 3. 数字

### 3.1 整数

```python
x = 100
big = 1_000_000     # 下划线分隔符，仅增加可读性，值等同 1000000
binary = 0b1010     # 二进制，值为 10
octal = 0o17        # 八进制，值为 15
hex_val = 0xFF      # 十六进制，值为 255
```

> **[重点]** Python 整数是**任意精度**，不会溢出（区别于 Java/C 的 int/long）。

```python
# 这在 Python 里完全合法
huge = 2 ** 100
print(huge)  # 1267650600228229401496703205376
```

### 3.2 运算符

```python
10 / 3       # 3.3333...（始终返回浮点数）
10 // 3      # 3（整除，向下取整）
10 % 3       # 1（取余）
2 ** 10      # 1024（幂运算，区别于其他语言的 Math.pow(2, 10)）
abs(-5)      # 5
round(3.14159, 2)  # 3.14
```

> **[重点]** `/` 在 Python 3 中始终返回浮点数，`//` 才是整除。

### 3.3 浮点数

```python
0.1 + 0.2   # 0.30000000000000004（IEEE 754 精度问题，与其他语言一致）

# 精确计算用 decimal
from decimal import Decimal
Decimal("0.1") + Decimal("0.2")  # Decimal('0.3')
```

---

## 4. 类型转换

```python
int("42")         # 42
int(3.9)          # 3（截断，不是四舍五入）
float("3.14")     # 3.14
str(100)          # "100"
bool(0)           # False
bool("")          # False
bool([])          # False
bool(None)        # False
bool(1)           # True
bool("hello")     # True
```

> **[陷阱]** `int()` 不能直接转换 `"3.14"` 这样的浮点字符串，需要先转 float：

```python
int("3.14")          # ValueError!
int(float("3.14"))   # 3（正确做法）
```

---

## 5. None

```python
result = None
print(type(None))    # <class 'NoneType'>

# None 判断必须用 is，不用 ==
if result is None:
    print("no value")

if result is not None:
    print("has value")
```

> **[陷阱]** `result == None` 虽然通常能工作，但某些对象重写了 `__eq__` 会导致意外结果。始终用 `is None`。

---

## 6. 常量惯例

```python
# Python 没有 const 关键字，靠全大写命名约定表示常量
MAX_CONNECTIONS = 100
DATABASE_URL = "postgresql://localhost/mydb"
PI = 3.14159
```

> **[注意]** 这只是约定，Python 本身不会阻止修改这些值。

---

## 7. 常见陷阱与其他语言对比

| 特性 | Python | Java/JS/Go |
|------|--------|------------|
| 幂运算 | `2 ** 10` | `Math.pow(2, 10)` |
| 整除 | `10 // 3` | `10 / 3`（整型） |
| 除法 | `/` 始终返回 float | 整型相除得整型 |
| 整数溢出 | 不会溢出 | 有上限 |
| 空值判断 | `is None` | `== null` |
| 常量 | 全大写约定 | `const`/`final` 关键字 |
| 字符串不可变 | 是 | 是 |
| 多行字符串 | `"""..."""` | 各语言不同 |
