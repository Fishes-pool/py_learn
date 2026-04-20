# Chapter 9：类

> 面向有其他语言经验的开发者，聚焦 Python 特有语法和易混淆点。

## 目录

1. [类定义基础](#1-类定义基础)
2. [特殊方法（Dunder Methods）](#2-特殊方法dunder-methods)
3. [继承](#3-继承)
4. [访问控制](#4-访问控制)
5. [类方法与静态方法](#5-类方法与静态方法)
6. [@property 装饰器](#6-property-装饰器)
7. [dataclass](#7-dataclass)
8. [常见陷阱与其他语言对比](#8-常见陷阱与其他语言对比)

---

## 1. 类定义基础

```python
class Dog:
    # 类属性（所有实例共享）
    species = "Canis familiaris"

    # 构造函数
    def __init__(self, name: str, age: int):
        # 实例属性（每个实例独立）
        self.name = name
        self.age = age

    # 实例方法（第一个参数必须是 self）
    def bark(self) -> str:
        return f"{self.name} says: Woof!"

    def describe(self) -> str:
        return f"{self.name} is {self.age} years old"


# 创建实例
dog = Dog("Rex", 3)
print(dog.bark())            # "Rex says: Woof!"
print(Dog.species)           # 通过类名访问类属性
print(dog.species)           # 也可以通过实例访问
```

> **[重点]** Python 的 `self` 相当于其他语言的 `this`，但必须**显式声明**为第一个参数，且方法调用时 Python 自动传入，不需要手动传。

> **[注意]** 类属性和实例属性的区别：类属性是所有实例共享的，实例属性是每个实例独立的。

---

## 2. 特殊方法（Dunder Methods）

Python 通过特殊方法（双下划线开头和结尾）实现运算符重载和内置函数支持。

### `__str__` 和 `__repr__`

> **[重点]** `__str__` 控制 `print(obj)` 的输出（用户友好）；`__repr__` 是开发者视角的表示（应能重建对象）。

```python
class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __str__(self):
        return f"Point({self.x}, {self.y})"   # print() 调用

    def __repr__(self):
        return f"Point(x={self.x}, y={self.y})"   # 调试/交互式环境调用

p = Point(3, 5)
print(p)              # "Point(3, 5)"   → __str__
repr(p)               # "Point(x=3, y=5)"  → __repr__
```

### 运算符重载

```python
class Vector:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __add__(self, other):        # v1 + v2
        return Vector(self.x + other.x, self.y + other.y)

    def __eq__(self, other):         # v1 == v2
        return self.x == other.x and self.y == other.y

    def __len__(self):               # len(v)
        return int((self.x**2 + self.y**2) ** 0.5)

    def __str__(self):
        return f"Vector({self.x}, {self.y})"
```

---

## 3. 继承

> **[重点]** 语法：`class Child(Parent):`，`super()` 调用父类方法。

```python
class Animal:
    def __init__(self, name: str):
        self.name = name

    def speak(self) -> str:
        raise NotImplementedError("子类必须实现 speak()")

    def __str__(self):
        return f"{type(self).__name__}({self.name})"


class Dog(Animal):
    def speak(self) -> str:
        return f"{self.name}: Woof!"


class Cat(Animal):
    def __init__(self, name: str, indoor: bool = True):
        super().__init__(name)         # 调用父类 __init__
        self.indoor = indoor           # 子类新增属性

    def speak(self) -> str:
        return f"{self.name}: Meow!"


# 多态
animals = [Dog("Rex"), Cat("Whiskers"), Cat("Tom", indoor=False)]
for animal in animals:
    print(animal.speak())

# 类型检查
isinstance(animals[0], Dog)       # True
isinstance(animals[0], Animal)    # True（继承）
type(animals[0]) == Dog           # True
type(animals[0]) == Animal        # False
```

### 多继承（了解，谨慎使用）

```python
class A:
    def method(self):
        return "A"

class B(A):
    def method(self):
        return "B"

class C(A):
    def method(self):
        return "C"

class D(B, C):   # 多继承
    pass

D().method()     # "B"（MRO：Method Resolution Order，从左到右）
D.__mro__        # (D, B, C, A, object)
```

---

## 4. 访问控制

> **[注意]** Python **没有** `private` / `protected` 关键字，靠命名约定表达意图。

```python
class BankAccount:
    def __init__(self, balance: float):
        self.owner = "Alice"          # 公开属性
        self._balance = balance       # _：约定"内部使用"（类似 protected）
        self.__pin = "1234"           # __：触发名称改写（name mangling）

    def get_balance(self):
        return self._balance

    def _validate(self):              # _：内部方法
        return True

account = BankAccount(1000)
account.owner            # 合法
account._balance         # 合法，但约定不应直接访问
account.__pin            # AttributeError！
account._BankAccount__pin  # 合法，name mangling 后的真实名称（仅用于调试）
```

---

## 5. 类方法与静态方法

> **[重点]** 区分三种方法：

```python
class User:
    _count = 0

    def __init__(self, name: str):
        self.name = name
        User._count += 1

    def greet(self):                  # 实例方法：第一参数是 self
        return f"Hi, I'm {self.name}"

    @classmethod
    def get_count(cls) -> int:        # 类方法：第一参数是 cls（类本身）
        return cls._count

    @classmethod
    def from_dict(cls, data: dict):   # 工厂方法（常见用法）
        return cls(data["name"])

    @staticmethod
    def validate_name(name: str) -> bool:  # 静态方法：无 self/cls
        return len(name) >= 2 and name.isalpha()


u1 = User("Alice")
u2 = User.from_dict({"name": "Bob"})   # 工厂方法创建实例

User.get_count()           # 2（通过类调用）
u1.get_count()             # 2（也可通过实例调用）
User.validate_name("Al")   # True（静态方法）
```

---

## 6. @property 装饰器

> **[重点]** `@property` 让方法像属性一样访问，无需加括号。常用于 getter/setter/deleter。

```python
class Temperature:
    def __init__(self, celsius: float):
        self._celsius = celsius

    @property
    def celsius(self) -> float:        # getter：像属性一样读取
        return self._celsius

    @celsius.setter
    def celsius(self, value: float):   # setter：像属性一样赋值
        if value < -273.15:
            raise ValueError("温度不能低于绝对零度")
        self._celsius = value

    @property
    def fahrenheit(self) -> float:     # 计算属性（只读）
        return self._celsius * 9/5 + 32


t = Temperature(100)
print(t.celsius)           # 100（调用 getter，无括号）
t.celsius = 200            # 调用 setter
print(t.fahrenheit)        # 392.0（计算属性）
t.celsius = -300           # ValueError
```

---

## 7. dataclass

> **[重点]** Python 3.7+ 的 `@dataclass` 装饰器自动生成 `__init__`、`__repr__`、`__eq__` 等方法，大幅减少样板代码。

```python
from dataclasses import dataclass, field

@dataclass
class Product:
    name: str
    price: float
    quantity: int = 0
    tags: list = field(default_factory=list)   # 可变默认值必须用 field

p1 = Product("iPhone", 999.0, 10, ["electronics", "apple"])
p2 = Product("iPhone", 999.0, 10, ["electronics", "apple"])

print(p1)          # Product(name='iPhone', price=999.0, quantity=10, tags=[...])
p1 == p2           # True（自动生成 __eq__）

# frozen=True：不可变（类似元组）
@dataclass(frozen=True)
class Point:
    x: float
    y: float

pt = Point(3.0, 5.0)
pt.x = 10          # FrozenInstanceError！

# order=True：支持比较运算符（<, >, <=, >=）
@dataclass(order=True)
class Version:
    major: int
    minor: int
    patch: int

Version(1, 2, 3) < Version(1, 3, 0)   # True
```

---

## 8. 常见陷阱与其他语言对比

| 特性 | Python | Java/JS/Go |
|------|--------|------------|
| self/this | 显式声明为参数 | 隐式可用 |
| 构造函数 | `__init__` | `constructor` / 类名方法 |
| 访问控制 | 命名约定（无关键字）| private/protected/public |
| 继承语法 | `class Child(Parent):` | `extends` / `:` |
| 调用父类 | `super().__init__()` | `super()` |
| 多继承 | 支持（MRO 解决冲突）| Java 不支持，JS/Go 不同方式 |
| 运算符重载 | 特殊方法（dunder）| Java 不支持，C++ 支持 |
| getter/setter | `@property` | Java Bean / get/set 方法 |
| 数据类 | `@dataclass` | Record（Java 16+）/ 手写 |
