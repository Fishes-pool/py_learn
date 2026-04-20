# Chapter 3：列表、操作列表、遍历、元组

> 面向有其他语言经验的开发者，聚焦 Python 特有语法和易混淆点。

## 目录

1. [列表基础](#1-列表基础)
2. [增删改](#2-增删改)
3. [排序](#3-排序)
4. [遍历](#4-遍历)
5. [range()](#5-range)
6. [切片](#6-切片)
7. [列表推导式](#7-列表推导式)
8. [数值函数](#8-数值函数)
9. [元组](#9-元组)
10. [列表 vs 元组选择原则](#10-列表-vs-元组选择原则)
11. [常见陷阱与其他语言对比](#11-常见陷阱与其他语言对比)

---

## 1. 列表基础

```python
# 定义
fruits = ["apple", "banana", "cherry"]
mixed = [1, "hello", 3.14, True]   # Python 列表可以混合类型
empty = []

# 访问：正索引
print(fruits[0])   # "apple"
print(fruits[2])   # "cherry"

# 访问：负数索引（从末尾计）
print(fruits[-1])  # "cherry"（等同于 fruits[len(fruits)-1]）
print(fruits[-2])  # "banana"

# 长度
len(fruits)        # 3
```

> **[重点]** `list[-1]` 是 Python 特有语法，获取最后一个元素，比其他语言的 `list[list.length-1]` 简洁得多。

---

## 2. 增删改

```python
fruits = ["apple", "banana"]

# 追加到末尾
fruits.append("cherry")           # ["apple", "banana", "cherry"]

# 插入到指定位置
fruits.insert(1, "mango")         # ["apple", "mango", "banana", "cherry"]

# 修改元素
fruits[0] = "avocado"

# 删除：del（按索引，无返回值）
del fruits[0]

# 删除：pop（按索引，返回被删元素，默认删末尾）
last = fruits.pop()               # 返回 "cherry"，列表缩短
second = fruits.pop(0)            # 返回第 0 个元素

# 删除：remove（按值，删除第一个匹配项）
fruits.remove("banana")           # 无返回值（返回 None）
```

> **[陷阱]** `.remove(val)` 返回 `None`，不是被删除的元素。如果需要被删元素，用 `.pop(index)`。

```python
item = fruits.remove("banana")    # item 是 None，不是 "banana"
item = fruits.pop(fruits.index("banana"))  # 正确做法：先找索引再 pop
```

> **[注意]** `.remove()` 只删除第一个匹配项；若值不存在会抛 `ValueError`。

---

## 3. 排序

```python
nums = [3, 1, 4, 1, 5, 9, 2, 6]

# 原地排序（修改原列表，返回 None）
nums.sort()                        # [1, 1, 2, 3, 4, 5, 6, 9]
nums.sort(reverse=True)            # [9, 6, 5, 4, 3, 2, 1, 1]

# 返回新列表（不修改原列表）
sorted_nums = sorted(nums)
sorted_desc = sorted(nums, reverse=True)

# 反转（原地）
nums.reverse()

# 按自定义规则排序
words = ["banana", "apple", "cherry", "fig"]
words.sort(key=len)                # 按字符串长度排序
words.sort(key=lambda x: x[-1])   # 按最后一个字母排序
```

> **[重点]** `.sort()` 原地修改，`sorted()` 返回新列表。这与其他语言（如 Java 的 `Collections.sort()`）类似，但 Python 的 `sorted()` 是内置函数，更通用。

---

## 4. 遍历

```python
fruits = ["apple", "banana", "cherry"]

# 基础遍历（直接迭代值，不需要索引）
for fruit in fruits:
    print(fruit)

# 同时获取索引和值
for i, fruit in enumerate(fruits):
    print(f"{i}: {fruit}")

# 从指定索引开始
for i, fruit in enumerate(fruits, start=1):   # 索引从 1 开始
    print(f"{i}: {fruit}")

# 同时遍历两个列表
names = ["Alice", "Bob"]
scores = [95, 87]
for name, score in zip(names, scores):
    print(f"{name}: {score}")
```

> **[重点]** `enumerate()` 是 Python 获取索引的惯用方式，比 `for i in range(len(list))` 更 Pythonic。

---

## 5. range()

```python
# range(stop)：0 到 stop-1
list(range(5))             # [0, 1, 2, 3, 4]

# range(start, stop)
list(range(2, 7))          # [2, 3, 4, 5, 6]

# range(start, stop, step)
list(range(0, 10, 2))      # [0, 2, 4, 6, 8]
list(range(10, 0, -1))     # [10, 9, 8, 7, 6, 5, 4, 3, 2, 1]

# 遍历数字范围
for i in range(1, 6):
    print(i)               # 1 2 3 4 5
```

> **[注意]** `range()` 本身不是列表，是惰性序列。需要列表时用 `list(range(...))`。

---

## 6. 切片

> **[重点]** 语法：`list[start:stop:step]`，三个参数都可省略。

```python
nums = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]

nums[2:5]       # [2, 3, 4]（索引 2 到 4，不含 5）
nums[:3]        # [0, 1, 2]（从头到索引 2）
nums[7:]        # [7, 8, 9]（从索引 7 到末尾）
nums[:]         # [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]（浅拷贝整个列表）

# 带步长
nums[::2]       # [0, 2, 4, 6, 8]（每隔一个）
nums[1::2]      # [1, 3, 5, 7, 9]
nums[::-1]      # [9, 8, 7, 6, 5, 4, 3, 2, 1, 0]（反转）

# 负数索引切片
nums[-3:]       # [7, 8, 9]（最后 3 个）
nums[:-2]       # [0, 1, 2, 3, 4, 5, 6, 7]（除最后 2 个）
```

> **[注意]** `list[:]` 是浅拷贝，嵌套对象仍共享引用。深拷贝用 `copy.deepcopy(list)`。

---

## 7. 列表推导式

> **[重点]** 列表推导式是 Python 最具代表性的语法，相当于其他语言的 `.map().filter()` 链。

```python
# 基本语法：[表达式 for 变量 in 可迭代对象]
squares = [x ** 2 for x in range(1, 6)]      # [1, 4, 9, 16, 25]

# 带条件过滤：[表达式 for 变量 in 可迭代对象 if 条件]
evens = [x for x in range(10) if x % 2 == 0] # [0, 2, 4, 6, 8]

# 对比 JS 的 map + filter
# JS: [1,2,...,9].map(x => x**2).filter(x => x > 10)
large_squares = [x ** 2 for x in range(1, 10) if x ** 2 > 10]

# 嵌套推导式（扁平化二维列表）
matrix = [[1, 2], [3, 4], [5, 6]]
flat = [num for row in matrix for num in row]  # [1, 2, 3, 4, 5, 6]

# 字符串处理
words = ["  hello  ", "  world  "]
cleaned = [w.strip().upper() for w in words]   # ["HELLO", "WORLD"]
```

---

## 8. 数值函数

```python
nums = [3, 1, 4, 1, 5, 9, 2, 6]

min(nums)    # 1
max(nums)    # 9
sum(nums)    # 31
len(nums)    # 8
```

---

## 9. 元组

元组（tuple）是**不可变的列表**，用圆括号定义。

```python
# 定义
point = (3, 5)
rgb = (255, 128, 0)

# 访问（与列表相同）
print(point[0])   # 3
print(point[-1])  # 5

# 切片
rgb[:2]           # (255, 128)
```

> **[陷阱]** 单元素元组必须加逗号，否则会被解析为普通括号表达式：

```python
single = (42,)    # 这是元组，type 是 tuple
not_tuple = (42)  # 这是整数！type 是 int
```

### 元组解包（Tuple Unpacking）

> **[重点]** 元组解包是 Python 最常用的特性之一：

```python
# 基本解包
x, y = (3, 5)
a, b, c = (1, 2, 3)

# 交换变量（Python 惯用法，利用元组解包）
a, b = b, a          # 无需临时变量

# 星号解包：* 接收剩余部分
first, *rest = [1, 2, 3, 4, 5]
# first = 1, rest = [2, 3, 4, 5]

head, *middle, last = [1, 2, 3, 4, 5]
# head = 1, middle = [2, 3, 4], last = 5

# 函数返回多值（本质是返回元组）
def min_max(nums):
    return min(nums), max(nums)    # 返回元组

lo, hi = min_max([3, 1, 4, 1, 5])
```

### 元组不可变性

```python
point = (3, 5)
point[0] = 10    # TypeError: 'tuple' object does not support item assignment

# 但若元组包含可变对象，该对象本身可以修改
data = ([1, 2], [3, 4])
data[0].append(99)   # 合法：修改的是列表，不是元组
```

---

## 10. 列表 vs 元组选择原则

| 场景 | 选择 |
|------|------|
| 需要修改的序列（增删改）| 列表 `[]` |
| 固定数据（坐标、RGB、数据库行）| 元组 `()` |
| 函数返回多个值 | 元组 `()` |
| 字典的 key（需要 hashable）| 元组 `()` |
| 性能敏感的只读序列 | 元组（略快于列表）|

---

## 11. 常见陷阱与其他语言对比

| 特性 | Python | Java/JS/Go |
|------|--------|------------|
| 负数索引 | `list[-1]` 合法 | 不支持 |
| `remove()` 返回值 | `None` | 通常返回被删元素 |
| 除法索引遍历 | `enumerate()` | `for(int i=0; ...)` |
| 浅拷贝 | `list[:]` 或 `list.copy()` | 各语言不同 |
| 推导式 | `[x for x in ...]` | `.stream().map()...` |
| 单元素元组 | `(val,)` 逗号必须 | 无对应概念 |
| 变量交换 | `a, b = b, a` | 需要临时变量 |
