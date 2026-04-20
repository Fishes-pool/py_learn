# Chapter 6：字典

> 面向有其他语言经验的开发者，聚焦 Python 特有语法和易混淆点。

## 目录

1. [定义方式](#1-定义方式)
2. [访问元素](#2-访问元素)
3. [增删改](#3-增删改)
4. [遍历](#4-遍历)
5. [字典推导式](#5-字典推导式)
6. [合并字典](#6-合并字典)
7. [嵌套字典与字典列表](#7-嵌套字典与字典列表)
8. [defaultdict](#8-defaultdict)
9. [常用方法速查](#9-常用方法速查)
10. [常见陷阱与其他语言对比](#10-常见陷阱与其他语言对比)

---

## 1. 定义方式

```python
# 字面量
user = {"name": "Alice", "age": 26, "active": True}

# dict() 构造函数
user = dict(name="Alice", age=26, active=True)

# 空字典
empty = {}
empty = dict()

# 从 key 列表创建（统一默认值）
keys = ["a", "b", "c"]
d = dict.fromkeys(keys, 0)         # {"a": 0, "b": 0, "c": 0}
d = dict.fromkeys(keys)            # {"a": None, "b": None, "c": None}
```

> **[注意]** Python 3.7+ 字典**保证插入顺序**，遍历顺序与插入顺序一致。

---

## 2. 访问元素

```python
user = {"name": "Alice", "age": 26}

# 直接访问（key 不存在抛 KeyError）
print(user["name"])          # "Alice"
print(user["email"])         # KeyError!

# 安全访问（key 不存在返回默认值）
print(user.get("email"))             # None
print(user.get("email", "N/A"))      # "N/A"
```

> **[重点]** 优先用 `.get()` 安全访问，避免因 key 不存在导致程序崩溃。

```python
# 判断 key 是否存在
if "name" in user:
    print(user["name"])

if "email" not in user:
    print("无邮箱")
```

---

## 3. 增删改

```python
user = {"name": "Alice", "age": 26}

# 添加 / 修改（同一语法）
user["email"] = "alice@example.com"    # 添加新 key
user["age"] = 27                        # 修改已有 key

# 删除
del user["age"]                          # 删除，key 不存在抛 KeyError
email = user.pop("email")               # 删除并返回值
phone = user.pop("phone", None)         # 不存在时返回默认值，不抛异常

# setdefault：key 不存在时设置默认值，已存在则不修改
user.setdefault("role", "viewer")       # 若 "role" 不存在，设为 "viewer"
```

---

## 4. 遍历

> **[重点]** 遍历字典的三种方式：

```python
config = {"host": "localhost", "port": 8080, "debug": True}

# 遍历 key（默认行为）
for key in config:
    print(key)

# 遍历 value
for value in config.values():
    print(value)

# 遍历 key-value 对（最常用）
for key, value in config.items():
    print(f"{key}: {value}")
```

> **[注意]** 不要在遍历时修改字典的大小（增删 key），会抛 `RuntimeError`。修改 value 是安全的。

```python
# 安全做法：遍历副本
for key in list(config.keys()):
    if key == "debug":
        del config[key]
```

---

## 5. 字典推导式

> **[重点]** 语法：`{key_expr: value_expr for item in iterable if condition}`

```python
# 基本用法
squares = {x: x**2 for x in range(1, 6)}
# {1: 1, 2: 4, 3: 9, 4: 16, 5: 25}

# 从两个列表创建字典
keys = ["a", "b", "c"]
values = [1, 2, 3]
d = {k: v for k, v in zip(keys, values)}
# {"a": 1, "b": 2, "c": 3}

# 过滤条件
users = {"Alice": 90, "Bob": 55, "Carol": 78}
passed = {name: score for name, score in users.items() if score >= 60}
# {"Alice": 90, "Carol": 78}

# 反转字典（key-value 互换）
original = {"a": 1, "b": 2, "c": 3}
inverted = {v: k for k, v in original.items()}
# {1: "a", 2: "b", 3: "c"}

# 转换 value
upper_keys = {k.upper(): v for k, v in original.items()}
# {"A": 1, "B": 2, "C": 3}
```

---

## 6. 合并字典

```python
defaults = {"theme": "dark", "lang": "zh", "debug": False}
overrides = {"lang": "en", "debug": True}

# Python 3.9+：| 运算符（推荐）
merged = defaults | overrides
# {"theme": "dark", "lang": "en", "debug": True}

# |= 原地合并（类似 +=）
defaults |= overrides

# 兼容旧版本：** 解包合并
merged = {**defaults, **overrides}   # 后面的覆盖前面的

# .update()：原地更新（无返回值）
defaults.update(overrides)
```

---

## 7. 嵌套字典与字典列表

```python
# 字典列表（类似 JSON 数组）
users = [
    {"id": 1, "name": "Alice", "tags": ["admin", "user"]},
    {"id": 2, "name": "Bob",   "tags": ["user"]},
]

for user in users:
    print(f"{user['name']}: {', '.join(user['tags'])}")

# 嵌套字典（类似 JSON 对象嵌套）
config = {
    "database": {
        "host": "localhost",
        "port": 5432,
        "credentials": {"user": "admin", "password": "secret"}
    },
    "cache": {"host": "redis://localhost", "ttl": 300}
}

# 访问嵌套 key
db_host = config["database"]["host"]
db_user = config["database"]["credentials"]["user"]

# 安全访问嵌套（get 链）
cache_ttl = config.get("cache", {}).get("ttl", 60)
```

---

## 8. defaultdict

`collections.defaultdict` 在访问不存在的 key 时自动创建默认值，避免 `KeyError`。

```python
from collections import defaultdict

# 统计词频（普通 dict 需要先判断 key 是否存在）
words = ["apple", "banana", "apple", "cherry", "banana", "apple"]

# 普通 dict 写法（繁琐）
freq = {}
for word in words:
    if word in freq:
        freq[word] += 1
    else:
        freq[word] = 1

# defaultdict 写法（简洁）
freq = defaultdict(int)     # 默认值为 int() == 0
for word in words:
    freq[word] += 1

# 默认值为列表
groups = defaultdict(list)
data = [("a", 1), ("b", 2), ("a", 3), ("b", 4)]
for key, val in data:
    groups[key].append(val)
# {"a": [1, 3], "b": [2, 4]}
```

---

## 9. 常用方法速查

```python
d = {"a": 1, "b": 2, "c": 3}

d.keys()           # dict_keys(["a", "b", "c"])
d.values()         # dict_values([1, 2, 3])
d.items()          # dict_items([("a", 1), ("b", 2), ("c", 3)])

d.get("a")         # 1
d.get("z", 0)      # 0（默认值）

d.pop("a")         # 删除并返回 1
d.pop("z", None)   # key 不存在时返回 None

d.setdefault("x", 10)  # key 不存在时添加，存在时不修改
d.update({"b": 99})    # 合并另一个字典

d.copy()           # 浅拷贝
d.clear()          # 清空
len(d)             # 元素数量
```

---

## 10. 常见陷阱与其他语言对比

| 特性 | Python | Java/JS/Go |
|------|--------|------------|
| 不存在 key | `KeyError` | null / undefined |
| 安全访问 | `.get(key, default)` | `getOrDefault()` / `?.` |
| key 存在检测 | `in` | `.containsKey()` / `in` |
| 遍历 key-value | `.items()` | `entrySet()` / `Object.entries()` |
| 合并字典 | `d1 \| d2`（3.9+）| `putAll()` / `{...a, ...b}` |
| 推导式 | `{k: v for ...}` | Stream/Array methods |
| 保证顺序 | 3.7+ 是 | LinkedHashMap / Map |
| 默认值 | `defaultdict` | `getOrDefault` / `Map.withDefault` |
