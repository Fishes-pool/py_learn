# Chapter 11：测试代码

> 面向有其他语言经验的开发者，聚焦 Python 特有语法和易混淆点。

## 目录

1. [测试框架选择](#1-测试框架选择)
2. [pytest 基础](#2-pytest-基础)
3. [测试异常](#3-测试异常)
4. [Fixture（测试夹具）](#4-fixture测试夹具)
5. [参数化测试](#5-参数化测试)
6. [Mock（模拟）](#6-mock模拟)
7. [测试覆盖率](#7-测试覆盖率)
8. [unittest 对比](#8-unittest-对比)
9. [常见陷阱与最佳实践](#9-常见陷阱与最佳实践)

---

## 1. 测试框架选择

| | pytest | unittest |
|---|---|---|
| 安装 | `pip install pytest` | 内置 |
| 测试函数 | 普通函数 `test_*` | 继承 `TestCase` 的类 |
| 断言 | 直接用 `assert` | `assertEqual` 等方法 |
| 输出 | 更友好，差异显示 | 较简洁 |
| 插件生态 | 丰富 | 有限 |
| 业界主流 | ✅ | 仍在使用 |

> **[重点]** 现代 Python 项目主流使用 pytest，但 pytest 可以直接运行 unittest 风格的测试。

安装：
```bash
pip install pytest pytest-cov
```

---

## 2. pytest 基础

### 测试文件和函数命名规则

- 文件：`test_*.py` 或 `*_test.py`
- 函数：`test_*`
- 类（可选）：`Test*`（类内方法也用 `test_*`）

```python
# test_math.py
def add(a, b):
    return a + b

def test_add_basic():
    assert add(1, 2) == 3       # 直接用 assert，pytest 自动增强错误信息

def test_add_negative():
    assert add(-1, -2) == -3

def test_add_floats():
    result = add(0.1, 0.2)
    assert abs(result - 0.3) < 1e-9   # 浮点数比较

# 运行：pytest test_math.py -v
```

> **[重点]** pytest 会在 `assert` 失败时自动展示详细的差异信息，不需要特殊断言方法。

### 运行命令

```bash
pytest                          # 运行当前目录所有测试
pytest test_math.py             # 运行指定文件
pytest test_math.py -v          # 详细输出
pytest test_math.py -k "add"    # 只运行名称含 "add" 的测试
pytest -x                       # 遇到第一个失败立即停止
pytest --tb=short               # 简短错误追踪
```

---

## 3. 测试异常

> **[重点]** 用 `pytest.raises()` 验证函数是否抛出了预期的异常。

```python
import pytest

def divide(a, b):
    if b == 0:
        raise ValueError("除数不能为零")
    return a / b

def test_divide_by_zero():
    with pytest.raises(ValueError):
        divide(10, 0)

def test_divide_by_zero_message():
    with pytest.raises(ValueError, match="除数不能为零"):  # 验证错误消息
        divide(10, 0)

def test_divide_normal():
    result = divide(10, 2)
    assert result == 5.0
```

---

## 4. Fixture（测试夹具）

> **[重点]** `@pytest.fixture` 用于测试前置数据初始化，避免在每个测试中重复创建。

```python
import pytest

@pytest.fixture
def sample_user():
    """返回测试用的用户字典，每个测试函数调用前重新创建。"""
    return {"name": "Alice", "age": 25, "role": "admin", "active": True}

@pytest.fixture
def empty_cart():
    return {"items": [], "total": 0}

# 在测试函数中声明参数名即可注入 fixture
def test_user_name(sample_user):
    assert sample_user["name"] == "Alice"

def test_user_is_admin(sample_user):
    assert sample_user["role"] == "admin"

def test_cart_initially_empty(empty_cart):
    assert len(empty_cart["items"]) == 0

# 多个 fixture 同时使用
def test_add_to_cart(sample_user, empty_cart):
    empty_cart["items"].append({"product": "iPhone", "price": 999})
    assert len(empty_cart["items"]) == 1
```

### Fixture 作用域

```python
@pytest.fixture(scope="function")  # 默认：每个测试函数重新创建
@pytest.fixture(scope="class")     # 每个测试类共享一个实例
@pytest.fixture(scope="module")    # 整个测试文件共享
@pytest.fixture(scope="session")   # 整个测试会话共享（适合数据库连接）
```

### Fixture 清理（yield）

```python
@pytest.fixture
def db_connection():
    conn = create_connection()    # 前置：建立连接
    yield conn                    # 测试代码在这里运行
    conn.close()                  # 后置：清理连接（等同 finally）
```

---

## 5. 参数化测试

> **[重点]** `@pytest.mark.parametrize` 让一个测试函数跑多组数据，相当于 JUnit 的 `@ParameterizedTest`。

```python
import pytest

def is_palindrome(s: str) -> bool:
    s = s.lower().replace(" ", "")
    return s == s[::-1]

# 单参数
@pytest.mark.parametrize("text,expected", [
    ("racecar", True),
    ("hello", False),
    ("A man a plan a canal Panama", True),
    ("", True),
])
def test_is_palindrome(text, expected):
    assert is_palindrome(text) == expected

# 多参数组合
@pytest.mark.parametrize("a,b,expected", [
    (1, 2, 3),
    (0, 0, 0),
    (-1, 1, 0),
    (100, -50, 50),
])
def test_add(a, b, expected):
    assert a + b == expected
```

---

## 6. Mock（模拟）

> **[重点]** 用 `unittest.mock.patch` 模拟外部依赖（网络请求、文件 IO、数据库），让测试可预测、不依赖外部环境。

```python
from unittest.mock import patch, MagicMock
import pytest

# 被测代码
def get_user_from_api(user_id: int) -> dict:
    import requests
    response = requests.get(f"https://api.example.com/users/{user_id}")
    return response.json()

# 测试：mock 掉网络请求
def test_get_user_from_api():
    mock_response = MagicMock()
    mock_response.json.return_value = {"id": 1, "name": "Alice"}

    with patch("requests.get", return_value=mock_response) as mock_get:
        result = get_user_from_api(1)

    assert result["name"] == "Alice"
    mock_get.assert_called_once_with("https://api.example.com/users/1")

# 作为装饰器使用
@patch("requests.get")
def test_get_user_api_error(mock_get):
    mock_get.side_effect = ConnectionError("网络错误")
    with pytest.raises(ConnectionError):
        get_user_from_api(1)
```

---

## 7. 测试覆盖率

```bash
# 安装
pip install pytest-cov

# 运行测试并查看覆盖率
pytest --cov=your_module test_your_module.py

# 生成 HTML 报告
pytest --cov=your_module --cov-report=html

# 查看覆盖率不足 80% 时失败
pytest --cov=your_module --cov-fail-under=80
```

---

## 8. unittest 对比

```python
# unittest 风格（对比参考）
import unittest

class TestMath(unittest.TestCase):
    def setUp(self):                     # 等同于 pytest fixture（每个测试前运行）
        self.nums = [1, 2, 3, 4, 5]

    def test_sum(self):
        self.assertEqual(sum(self.nums), 15)   # 需要用 assertEqual 等方法

    def test_min(self):
        self.assertEqual(min(self.nums), 1)

    def tearDown(self):                  # 每个测试后运行（清理）
        pass

if __name__ == "__main__":
    unittest.main()
```

pytest 可以直接运行上面的 unittest 测试，无需任何修改。

---

## 9. 常见陷阱与最佳实践

```python
# ✅ 每个测试只验证一件事
def test_user_name():
    user = create_user("Alice")
    assert user.name == "Alice"

# ❌ 一个测试验证多件事（失败时难以定位）
def test_user():
    user = create_user("Alice")
    assert user.name == "Alice"
    assert user.age == 0
    assert user.active == True

# ✅ 测试名称描述行为
def test_divide_raises_value_error_when_divisor_is_zero():
    ...

# ❌ 模糊的测试名称
def test_divide2():
    ...

# ✅ 不要在测试中写逻辑（条件/循环）
# ❌ 这样的测试难以阅读和调试
def test_bad():
    for x in range(10):
        if x % 2 == 0:
            assert process(x) == x * 2
```
