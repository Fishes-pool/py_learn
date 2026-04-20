# Chapter 7：用户输入和 while 循环

> 面向有其他语言经验的开发者，聚焦 Python 特有语法和易混淆点。

## 目录

1. [input() 函数](#1-input-函数)
2. [while 循环基础](#2-while-循环基础)
3. [break / continue / pass](#3-break--continue--pass)
4. [while True + break 模式](#4-while-true--break-模式)
5. [循环中处理列表](#5-循环中处理列表)
6. [常见陷阱与其他语言对比](#6-常见陷阱与其他语言对比)

---

## 1. input() 函数

> **[重点]** `input()` 返回值**永远是字符串**，无论用户输入什么。

```python
# 基本用法
name = input("请输入你的名字：")
print(f"你好，{name}！")

# 必须手动转型
age_str = input("请输入年龄：")
age = int(age_str)           # 转换为整数

# 通常合并写
age = int(input("请输入年龄："))
price = float(input("请输入价格："))
```

> **[陷阱]** 用户输入非数字时 `int()` 会抛 `ValueError`，需要异常处理：

```python
try:
    age = int(input("请输入年龄："))
except ValueError:
    print("请输入有效的数字")
```

---

## 2. while 循环基础

```python
count = 0

while count < 5:
    print(f"count = {count}")
    count += 1              # Python 没有 count++，用 count += 1
```

> **[注意]** Python **没有** `++` 和 `--` 运算符，使用 `+= 1` 和 `-= 1`。

### 用标志变量控制循环（Python 惯用法）

```python
active = True
result = []

while active:
    data = get_next_item()
    if data is None:
        active = False          # 通过标志退出，逻辑更清晰
    else:
        result.append(data)
```

---

## 3. break / continue / pass

```python
# break：立即退出整个循环
for i in range(10):
    if i == 5:
        break
    print(i)               # 打印 0 1 2 3 4

# continue：跳过当前迭代，进入下一次
for i in range(10):
    if i % 2 == 0:
        continue
    print(i)               # 打印 1 3 5 7 9

# pass：占位符，什么都不做（保持语法完整）
for i in range(5):
    if i == 3:
        pass               # 占位，后续再实现
    print(i)
```

### while-else（Python 特有）

```python
# while 的 else 块在循环正常结束（未被 break 中断）时执行
items = [1, 2, 3, 4, 5]
target = 3

i = 0
while i < len(items):
    if items[i] == target:
        print(f"找到 {target}，位置 {i}")
        break
    i += 1
else:
    print(f"未找到 {target}")   # break 时不执行，正常结束才执行
```

---

## 4. while True + break 模式

> **[重点]** Python 没有 `do-while` 循环，用 `while True: ... break` 代替，确保至少执行一次。

```python
# do-while 等价写法
while True:
    user_input = input("请输入命令（quit 退出）：").strip().lower()
    if not user_input:
        print("输入不能为空，请重试")
        continue
    if user_input == "quit":
        print("退出")
        break
    print(f"执行命令：{user_input}")
```

对比其他语言：
```
// Java/C 的 do-while
do {
    input = scanner.nextLine();
} while (!input.equals("quit"));
```

### 带重试次数的 while True

```python
MAX_RETRIES = 3

for attempt in range(1, MAX_RETRIES + 1):
    result = try_connect()
    if result.success:
        print("连接成功")
        break
    print(f"第 {attempt} 次尝试失败")
else:
    # for-else：for 循环未被 break 中断时执行
    print("达到最大重试次数，放弃")
```

---

## 5. 循环中处理列表

> **[陷阱]** 不能在 `for` 循环中直接修改正在遍历的列表（增删元素），会导致跳元素或 RuntimeError。

```python
# 错误做法（跳过元素）
items = [1, 2, 3, 4, 5]
for item in items:
    if item % 2 == 0:
        items.remove(item)   # 修改正在遍历的列表！

# 正确做法 1：遍历副本，修改原列表
for item in items[:]:        # items[:] 是副本
    if item % 2 == 0:
        items.remove(item)

# 正确做法 2：列表推导式生成新列表
items = [item for item in items if item % 2 != 0]

# 正确做法 3：while 循环消耗列表
queue = [1, 2, 3, 4, 5]
while queue:                 # 队列非空时继续
    item = queue.pop(0)      # 取出第一个
    print(f"处理：{item}")
```

> **[重点]** `while list:` 是 Python 逐步消耗列表的惯用法，`list` 为空时自动结束。

---

## 6. 常见陷阱与其他语言对比

| 特性 | Python | Java/JS/Go |
|------|--------|------------|
| `input()` 返回类型 | 始终是 `str` | 类型取决于 API |
| 自增 | `+= 1`（无 `++`）| `++` / `+=` |
| do-while | 无，用 `while True: break` | `do {...} while (cond)` |
| 循环中修改列表 | 需要遍历副本 | 通常同样危险 |
| 空容器结束循环 | `while list:` 自动结束 | 需要 `while (!list.isEmpty())` |
| for-else / while-else | Python 特有 | 无对应语法 |
| pass | 占位符关键字 | 空语句块 `{}` |
