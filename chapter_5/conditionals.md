# Chapter 5：if 逻辑判断

> 面向有其他语言经验的开发者，聚焦 Python 特有语法和易混淆点。

## 目录

1. [比较运算符](#1-比较运算符)
2. [布尔运算符](#2-布尔运算符)
3. [成员检测：in / not in](#3-成员检测in--not-in)
4. [if-elif-else 结构](#4-if-elif-else-结构)
5. [真值测试（Truthiness）](#5-真值测试truthiness)
6. [三元表达式](#6-三元表达式)
7. [is vs ==](#7-is-vs-)
8. [短路求值](#8-短路求值)
9. [常见陷阱与其他语言对比](#9-常见陷阱与其他语言对比)

---

## 1. 比较运算符

```python
x, y = 5, 10

x == y     # False（相等）
x != y     # True（不等）
x < y      # True
x > y      # False
x <= y     # True
x >= y     # False
```

> **[重点]** Python 支持链式比较（其他语言通常不支持）：

```python
# 判断 x 是否在 1 到 10 之间
1 <= x <= 10           # True（Python 特有）

# 等价于其他语言的：x >= 1 && x <= 10
```

---

## 2. 布尔运算符

> **[重点]** Python 使用英文单词 `and` / `or` / `not`，不是 `&&` / `||` / `!`。

```python
age = 25
has_id = True
is_banned = False

# and：所有条件为真
if age >= 18 and has_id:
    print("允许入场")

# or：至少一个条件为真
if age < 18 or is_banned:
    print("拒绝入场")

# not：取反
if not is_banned:
    print("未封禁")
```

---

## 3. 成员检测：in / not in

> **[重点]** `in` 是 Python 特有的成员检测运算符，适用于列表、元组、字符串、字典、集合。

```python
fruits = ["apple", "banana", "cherry"]
role = "admin"
allowed_roles = ["admin", "editor"]

# 列表成员检测
if "apple" in fruits:
    print("找到了")

if "grape" not in fruits:
    print("没有葡萄")

# 字符串包含检测
if "admin" in role:
    print("是管理员")

# 字典 key 检测
config = {"debug": True, "port": 8080}
if "debug" in config:
    print(config["debug"])

# 替代 switch/case 的惯用法
if role in ["admin", "superuser"]:
    print("高权限用户")
```

---

## 4. if-elif-else 结构

> **[重点]** Python 用 `elif`，不是 `else if`（区别于 Java/JS/Go）。条件无需括号，无需花括号，靠缩进。

```python
score = 85

if score >= 90:
    grade = "A"
elif score >= 80:
    grade = "B"
elif score >= 70:
    grade = "C"
elif score >= 60:
    grade = "D"
else:
    grade = "F"

print(f"成绩：{grade}")
```

> **[注意]** Python 3.10+ 引入了 `match/case`（结构模式匹配），类似其他语言的 switch，但更强大：

```python
# Python 3.10+
command = "quit"

match command:
    case "start":
        print("启动")
    case "stop" | "quit":    # 多个 case 用 |
        print("停止")
    case _:                  # 默认分支
        print("未知命令")
```

---

## 5. 真值测试（Truthiness）

> **[陷阱]** 以下值在布尔上下文中都被视为 `False`（falsy）：

```python
# Falsy 值
bool(False)    # False
bool(0)        # False
bool(0.0)      # False
bool("")       # False（空字符串）
bool([])       # False（空列表）
bool(())       # False（空元组）
bool({})       # False（空字典）
bool(set())    # False（空集合）
bool(None)     # False

# 其他所有值都是 Truthy
bool(1)        # True
bool("hello")  # True
bool([0])      # True（非空列表，即使元素是 0）
```

Python 惯用法：直接用容器本身做条件判断：

```python
items = []

# Pythonic 写法
if items:
    process(items)

if not items:
    print("列表为空")

# 不推荐（冗余）
if len(items) > 0:
    process(items)
```

---

## 6. 三元表达式

> **[重点]** Python 的三元表达式语序与其他语言不同：`值 if 条件 else 另一个值`

```python
age = 20

# Python 三元
label = "成年" if age >= 18 else "未成年"

# 对比 JS 三元：age >= 18 ? "成年" : "未成年"
# 对比 Go：if age >= 18 { "成年" } else { "未成年" }

# 可嵌套（不推荐过度嵌套）
level = "高级" if age >= 60 else "中级" if age >= 30 else "初级"
```

---

## 7. is vs ==

> **[陷阱]** `is` 比较**对象身份**（内存地址），`==` 比较**值**。

```python
a = [1, 2, 3]
b = [1, 2, 3]
c = a

a == b     # True（值相同）
a is b     # False（不同对象）
a is c     # True（同一对象）

# None 判断必须用 is
result = None
result is None      # True（推荐）
result == None      # True（可以工作，但不推荐）
```

> **[陷阱]** 小整数和短字符串可能被 Python 缓存，导致 `is` 偶尔返回 `True`，不要依赖这个行为：

```python
# 这是实现细节，不要依赖
x = 256
y = 256
x is y    # True（Python 缓存了 -5 到 256 的整数）

x = 257
y = 257
x is y    # False（超出缓存范围）
```

---

## 8. 短路求值

与其他语言一致，`and` / `or` 具有短路求值行为：

```python
# and：第一个为 False 时立即返回，不计算后面
def check():
    print("checked!")
    return True

False and check()    # 不会调用 check()，不打印

# or：第一个为 True 时立即返回
True or check()      # 不会调用 check()

# 常见用法：提供默认值
name = user_input or "匿名用户"    # user_input 为空/None 时用默认值

# 条件链（guard clause）
user = get_user()
if user and user.is_active and user.has_permission("read"):
    do_something()
```

---

## 9. 常见陷阱与其他语言对比

| 特性 | Python | Java/JS/Go |
|------|--------|------------|
| 布尔运算符 | `and` `or` `not` | `&&` `\|\|` `!` |
| 多分支 | `elif` | `else if` |
| 条件括号 | 不需要 | 需要 |
| 成员检测 | `in` / `not in` | `.contains()` / `indexOf` |
| 三元表达式 | `a if cond else b` | `cond ? a : b` |
| 空值判断 | `is None` | `=== null` / `== null` |
| 空容器判断 | `if not list:` | `list.isEmpty()` / `list.length === 0` |
| 链式比较 | `1 < x < 10` | 需要拆成两个条件 |
