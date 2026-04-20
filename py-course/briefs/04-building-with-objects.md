# Module 4 Brief: Building with Objects
**Covers:** Ch9 (classes, inheritance, properties, dataclasses, special methods)
**Metaphor:** A class is a cookie cutter. Instances are the cookies — same shape, different frosting.
**Opening hook:** Every library Claude pulls in — pandas, FastAPI, Pydantic — is built from classes. Reading them stops feeling mysterious once you know the pattern.
**Key insight:** A class bundles data and behavior together. Once you understand `self`, everything else clicks.
**Previous module:** Module 3 (loops and functions)
**Next module:** Module 5 (files and exceptions)

---

## Screens

### Screen 1: Classes as Blueprints
**Concept:** A class defines structure. Instances are individual objects created from that structure. `self` is the instance talking about itself.
**Teaching arc:** Group chat showing Blueprint vs Instances.

**Group chat:** id="chat-classes"
Actors: Blueprint/class (actor-1, teal), Alice instance (actor-2, coral), Bob instance (actor-3, amber)

Messages:
1. Blueprint → "I am the `User` class. I define the structure: every User has a `name`, `email`, and `role`."
2. Blueprint → "My `__init__` method runs when a new User is created: `def __init__(self, name, email):`"
3. Alice → "I was created with `User('Alice', 'alice@co.com')`. My `self.name` is 'Alice'."
4. Bob → "I was created with `User('Bob', 'bob@co.com')`. My `self.name` is 'Bob'."
5. Blueprint → "`self` is how an instance refers to its own data. When Alice calls `self.name`, she gets 'Alice'."
6. Alice → "I also have methods from the blueprint — `greet()` uses my own `self.name` to personalize."
7. Bob → "And I call the same `greet()`, but I get 'Hello, Bob!' because `self` points to me."

**Translation block:**
```python
class User:
    def __init__(self, name: str, email: str):
        self.name = name
        self.email = email
        self.role = "viewer"   # default

    def greet(self) -> str:
        return f"Hello, {self.name}!"

alice = User("Alice", "alice@co.com")
print(alice.greet())   # "Hello, Alice!"
```
Plain English:
- `class User:` → Define a blueprint named User
- `def __init__(self, name, email):` → The constructor: runs automatically when `User(...)` is called
- `self.name = name` → Store the `name` argument on this specific instance as `self.name`
- `def greet(self):` → An instance method — `self` is always the first parameter, means "this object"
- `alice = User("Alice", "alice@co.com")` → Create an instance from the blueprint
- `alice.greet()` → Call the greet method on alice — Python passes `alice` as `self` automatically

**Glossary terms:**
- `class` → A blueprint for creating objects. Defines what data they hold and what they can do
- `instance` → A specific object created from a class. `alice = User(...)` creates one instance
- `__init__` → The constructor method. Runs automatically when you create a new instance with `ClassName(...)`
- `self` → The instance itself, passed automatically as the first argument to every instance method

---

### Screen 2: Inheritance — Is-A Relationships
**Concept:** A child class inherits everything from its parent. Use `super()` to call the parent's version.
**Teaching arc:** Flow animation showing inheritance tree.

**Flow animation:**
Actors: Product (base), PhysicalProduct (child), DigitalProduct (child)
Steps:
1. `{"highlight":"flow-actor-1","label":"Product is the base class: name, price, get_info()"}`
2. `{"highlight":"flow-actor-2","label":"PhysicalProduct inherits Product — adds weight and shipping_cost()","packet":true,"from":"actor-1","to":"actor-2"}`
3. `{"highlight":"flow-actor-3","label":"DigitalProduct inherits Product — adds download_url and no shipping","packet":true,"from":"actor-1","to":"actor-3"}`
4. `{"highlight":"flow-actor-2","label":"PhysicalProduct calls super().__init__() to run Product setup first"}`
5. `{"highlight":"flow-actor-3","label":"DigitalProduct overrides get_info() — same name, different behavior"}`
6. `{"highlight":"flow-actor-1","label":"Both children share Product data — but each adds its own unique behavior"}`

**Translation block:**
```python
class Product:
    def __init__(self, name: str, price: float):
        self.name = name
        self.price = price

    def get_info(self) -> str:
        return f"{self.name}: ${self.price:.2f}"

class PhysicalProduct(Product):
    def __init__(self, name, price, weight_kg: float):
        super().__init__(name, price)   # run parent setup
        self.weight_kg = weight_kg

    def shipping_cost(self) -> float:
        return self.weight_kg * 2.5
```
Plain English:
- `class PhysicalProduct(Product):` → PhysicalProduct IS-A Product. Gets everything Product has
- `super().__init__(name, price)` → Run the parent (Product) constructor first, then our extra setup
- `self.weight_kg = weight_kg` → Add our own attribute after the parent is initialized
- `def shipping_cost(self):` → New method only PhysicalProduct has — Product does not know about it

**Glossary terms:**
- `inheritance` → When a child class takes on all the data and methods of its parent class
- `super()` → A reference to the parent class. `super().__init__()` calls the parent constructor
- `override` → When a child class redefines a method from its parent, replacing its behavior

---

### Screen 3: Dataclasses & Properties — Less Boilerplate
**Concept:** `@dataclass` auto-generates `__init__`, `__repr__`, `__eq__`. `@property` adds validation to attribute access.
**Teaching arc:** Side-by-side collapse animation showing verbose vs compact.

**Pattern cards (before/after):**
Two cards side by side:
- Before (without @dataclass): 15 lines of boilerplate `__init__`, `__repr__`, `__eq__`
- After (with @dataclass): 4 lines — decorator does the rest

**Translation block:**
```python
from dataclasses import dataclass

@dataclass
class OrderItem:
    product_name: str
    quantity: int
    unit_price: float

    @property
    def total(self) -> float:
        return self.quantity * self.unit_price

item = OrderItem("Widget", 3, 9.99)
print(item.total)     # 29.97 (no parentheses!)
print(item)           # OrderItem(product_name='Widget', quantity=3, unit_price=9.99)
```
Plain English:
- `@dataclass` → Decorator that auto-generates `__init__`, `__repr__`, and `__eq__` from the field annotations
- `product_name: str` → Field definition — name and type. Becomes `self.product_name` automatically
- `@property` → Makes `total` act like an attribute, not a method — call it as `item.total`, not `item.total()`
- `print(item)` → Dataclass auto-generates a nice representation. Without `@dataclass`, you would get a memory address

**Callout (callout-accent):**
> Pydantic, the library Claude often uses for data validation, is built entirely on this dataclass-like pattern — but with runtime type checking. Understanding `@dataclass` means Pydantic models will make immediate sense.

**Glossary terms:**
- `decorator` → A function that wraps another function or class to add behavior. Written with `@` above the definition
- `@dataclass` → A decorator that auto-generates common methods (`__init__`, `__repr__`, `__eq__`) from field annotations
- `@property` → A decorator that makes a method look like a plain attribute when accessed. No parentheses needed

---

### Screen 4: Dunder Methods — The Secret Language
**Concept:** Special methods named `__like_this__` hook into Python operations. `__str__`, `__len__`, `__eq__`, `__add__`.
**Teaching arc:** Interactive "dunder decoder" — click an operation to see which method it calls.

**Pattern cards (clickable dunder decoder):**
Each card shows an operation and the dunder behind it:
- `print(obj)` → calls `obj.__str__()`
- `len(obj)` → calls `obj.__len__()`
- `obj1 == obj2` → calls `obj1.__eq__(obj2)`
- `obj + other` → calls `obj.__add__(other)`
- `str(obj)` → calls `obj.__str__()`
- `obj[key]` → calls `obj.__getitem__(key)`

**Translation block:**
```python
class TaskList:
    def __init__(self):
        self._tasks = []

    def __str__(self) -> str:
        return f"TaskList with {len(self._tasks)} tasks"

    def __len__(self) -> int:
        return len(self._tasks)

    def __eq__(self, other) -> bool:
        return self._tasks == other._tasks

tasks = TaskList()
print(tasks)      # "TaskList with 0 tasks"
print(len(tasks)) # 0
```
Plain English:
- `__str__` → Called when you `print(tasks)` or do `str(tasks)`. Return a human-readable string
- `__len__` → Called when you do `len(tasks)`. Return the integer length
- `__eq__` → Called when you do `tasks1 == tasks2`. Return True if equal, False if not
- These methods make your custom objects feel like built-in Python types

**Callout (callout-info):**
> The double underscores are called "dunders" (double underscores). You pronounce `__str__` as "dunder str." When Claude generates a class with `__repr__` or `__post_init__`, these are the same mechanism — hooking into Python operations.

---

## Quiz (id="quiz-module4")

**Q1** (correct: option-b)
> You want two `User` instances to be considered equal if they have the same `user_id`. Which method do you implement?

- option-a: `__str__`
- option-b: `__eq__` ✓
- option-c: `__init__`
- option-d: `__len__`

right: "Correct! `__eq__` is called whenever `==` is used between two objects. Implement it to define what 'equal' means for your class."
wrong: "`__str__` controls how the object prints. `__init__` sets it up. `__eq__` is what controls the `==` operator."

**Q2** (correct: option-c)
> Scenario: `class Dog(Animal):` — Dog calls `super().__init__(name)` in its `__init__`. What does this do?

- option-a: Creates a new Animal instance
- option-b: Imports the Animal class
- option-c: Runs Animal's `__init__` to set up the inherited attributes ✓
- option-d: Copies all of Animal's methods into Dog

right: "Right! `super().__init__()` calls the parent class constructor. This ensures all of Animal's setup (like `self.name`) runs before Dog adds its own attributes."
wrong: "`super()` gives you a reference to the parent class. Calling `__init__()` on it runs the parent setup — essential when your child class adds attributes to an already-initialized parent."

**Q3** (drag-and-drop)
Chips: `@dataclass`, `@property`, `super()`, `__init__`
Zones:
- Auto-generates constructor and repr from field annotations → correct: `@dataclass`
- Makes a method look like a plain attribute (no parentheses) → correct: `@property`
- Reference to the parent class — used to call parent methods → correct: `super()`
- The constructor: runs automatically when a new instance is created → correct: `__init__`
