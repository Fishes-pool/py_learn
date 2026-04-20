# Chapter 8：函数

> 面向有其他语言经验的开发者，聚焦 Python 特有语法和易混淆点。

## 目录

1. [定义与调用](#1-定义与调用)
2. [参数类型](#2-参数类型)
3. [可变参数：*args 和 **kwargs](#3-可变参数args-和-kwargs)
4. [返回值](#4-返回值)
5. [作用域](#5-作用域)
6. [函数作为一等公民](#6-函数作为一等公民)
7. [类型注解（Type Hints）](#7-类型注解type-hints)
8. [模块与导入](#8-模块与导入)
9. [常见陷阱与其他语言对比](#9-常见陷阱与其他语言对比)

---

## 1. 定义与调用

```python
# 基本语法：def 函数名(参数):
def greet(name):
    return f"Hello, {name}!"

result = greet("Alice")
print(result)                # "Hello, Alice!"

# 无返回值的函数隐式返回 None
def say_hi(name):
    print(f"Hi, {name}!")

val = say_hi("Bob")          # 打印 "Hi, Bob!"
print(val)                   # None
```

---

## 2. 参数类型

### 位置参数 vs 关键字参数

> **[重点]** 调用时可以用关键字参数，允许乱序传入。

```python
def create_user(name, age, role):
    return {"name": name, "age": age, "role": role}

# 位置参数（顺序必须对）
create_user("Alice", 26, "admin")

# 关键字参数（顺序可以乱）
create_user(role="admin", name="Alice", age=26)

# 混合（位置参数必须在前）
create_user("Alice", role="admin", age=26)
```

### 默认参数值

```python
def connect(host, port=5432, timeout=30):
    print(f"连接 {host}:{port}，超时 {timeout}s")

connect("localhost")                     # port=5432, timeout=30
connect("remote.db", port=5433)         # timeout=30
connect("remote.db", 5433, 60)          # 全部位置参数
```

> **[陷阱]** 默认参数值在**函数定义时**求值一次，不要用可变对象（列表、字典）作默认值：

```python
# 错误！所有调用共享同一个列表
def add_item(item, items=[]):
    items.append(item)
    return items

add_item("a")   # ["a"]
add_item("b")   # ["a", "b"]  ← 意外！不是 ["b"]

# 正确做法：用 None 作占位，函数内创建新对象
def add_item(item, items=None):
    if items is None:
        items = []
    items.append(item)
    return items
```

### 强制关键字参数（* 之后的参数）

```python
# * 之后的参数必须用关键字传入
def create_file(path, *, mode="w", encoding="utf-8"):
    pass

create_file("/tmp/a.txt", mode="a")          # 正确
create_file("/tmp/a.txt", "a")               # TypeError！mode 必须用关键字
```

---

## 3. 可变参数：*args 和 **kwargs

> **[重点]** `*args` 接收任意数量位置参数，得到**元组**；`**kwargs` 接收任意数量关键字参数，得到**字典**。

```python
# *args：任意数量位置参数
def total(*args):
    print(type(args))        # <class 'tuple'>
    return sum(args)

total(1, 2, 3)               # 6
total(1, 2, 3, 4, 5)         # 15

# **kwargs：任意数量关键字参数
def log(**kwargs):
    print(type(kwargs))      # <class 'dict'>
    for key, value in kwargs.items():
        print(f"{key}: {value}")

log(level="INFO", message="启动成功", code=200)

# 同时使用（顺序：普通参数 → *args → 普通关键字参数 → **kwargs）
def func(a, b, *args, key="default", **kwargs):
    print(f"a={a}, b={b}, args={args}, key={key}, kwargs={kwargs}")

func(1, 2, 3, 4, key="x", extra=99)
# a=1, b=2, args=(3, 4), key="x", kwargs={"extra": 99}
```

### 解包传参

```python
# * 解包列表/元组为位置参数
nums = [1, 2, 3]
total(*nums)                 # 等同于 total(1, 2, 3)

# ** 解包字典为关键字参数
options = {"mode": "a", "encoding": "utf-8"}
open("file.txt", **options)  # 等同于 open("file.txt", mode="a", encoding="utf-8")
```

---

## 4. 返回值

```python
# 返回单个值
def square(x):
    return x ** 2

# 返回多个值（实际上是返回元组）
def min_max(items):
    return min(items), max(items)     # 返回元组 (min, max)

lo, hi = min_max([3, 1, 4, 1, 5])   # 元组解包
print(lo, hi)                         # 1 5

# 无 return 时隐式返回 None
def procedure():
    print("做了点事")

result = procedure()                  # None
```

> **[重点]** 返回多值是 Python 的惯用法，本质是返回元组并解包。

---

## 5. 作用域

Python 的作用域规则：**LEGB**（Local → Enclosing → Global → Built-in）

```python
x = "global"

def outer():
    x = "enclosing"

    def inner():
        x = "local"
        print(x)           # "local"

    inner()
    print(x)               # "enclosing"

outer()
print(x)                   # "global"

# global 关键字（不推荐，了解即可）
count = 0
def increment():
    global count
    count += 1

# nonlocal：修改外层函数变量
def make_counter():
    n = 0
    def counter():
        nonlocal n
        n += 1
        return n
    return counter

c = make_counter()
c()  # 1
c()  # 2
```

---

## 6. 函数作为一等公民

```python
# 函数赋值给变量
def double(x):
    return x * 2

fn = double
fn(5)              # 10

# 函数作为参数传入
def apply(func, value):
    return func(value)

apply(double, 5)   # 10

# lambda 匿名函数
triple = lambda x: x * 3
triple(5)          # 15

# 常见用法：sorted 的 key 参数
words = ["banana", "apple", "cherry", "fig"]
words.sort(key=lambda w: len(w))          # 按长度排序
words.sort(key=lambda w: w[-1])           # 按最后一个字母排序

users = [{"name": "Bob", "age": 30}, {"name": "Alice", "age": 25}]
users.sort(key=lambda u: u["age"])        # 按 age 排序

# map / filter（推导式通常更 Pythonic）
nums = [1, 2, 3, 4, 5]
doubled = list(map(lambda x: x * 2, nums))
evens = list(filter(lambda x: x % 2 == 0, nums))
```

---

## 7. 类型注解（Type Hints）

> **[重点]** Python 3.5+ 支持类型注解，是文档和 IDE 提示用途，**运行时不强制**。

```python
# 基本注解
def greet(name: str, times: int = 1) -> str:
    return (f"Hello, {name}!\n") * times

# 复杂类型（Python 3.9+ 直接用内置类型）
def process(items: list[int]) -> dict[str, int]:
    return {"count": len(items), "sum": sum(items)}

# 可选类型（值可以是指定类型或 None）
from typing import Optional
def find_user(user_id: int) -> Optional[dict]:
    ...

# Python 3.10+ 可以用 | 表示联合类型
def process(value: int | str) -> str:
    return str(value)
```

---

## 8. 模块与导入

```python
# 导入整个模块
import math
math.sqrt(16)            # 4.0
math.pi                  # 3.141592...

# 导入特定函数
from math import sqrt, pi
sqrt(16)                 # 直接用，无需前缀

# 导入并重命名（避免命名冲突）
from datetime import datetime as dt
now = dt.now()

import numpy as np       # 社区约定的别名

# 导入全部（不推荐：污染命名空间，难以追踪来源）
from math import *

# 自定义模块
# utils.py 中定义函数，其他文件导入：
from utils import helper_func
```

> **[重点]** `if __name__ == "__main__":` 让文件既可以作为模块导入，也可以直接运行：

```python
# utils.py
def add(a, b):
    return a + b

if __name__ == "__main__":
    # 直接运行 utils.py 时执行
    # 被其他文件 import 时不执行
    print(add(1, 2))
```

---

## 9. 常见陷阱与其他语言对比

| 特性 | Python | Java/JS/Go |
|------|--------|------------|
| 默认参数求值时机 | 定义时（不是调用时）| 调用时 |
| 可变默认参数 | 陷阱！用 None 代替 | 不存在此问题 |
| 关键字参数 | 内置支持 | 不支持（Java）/ 对象模拟（JS）|
| 返回多值 | 元组解包 | 需要包装类 / 数组 |
| 函数是一等公民 | 是 | JS 是，Java 用 Lambda |
| 类型注解 | 可选，运行时不强制 | 强类型，编译时检查 |
| `*args` / `**kwargs` | 内置语法 | 可变参数，无关键字版本 |
