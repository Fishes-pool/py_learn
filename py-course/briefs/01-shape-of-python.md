# Module 1 Brief: The Shape of Python
**Covers:** Ch2 (variables, strings, numbers, None) + Ch3 (lists, tuples, comprehensions)
**Metaphor:** Variables are luggage tags — labels that point to bags. The label is not the bag.
**Opening hook:** When you ask Claude to "store the username," this is *exactly* what it writes under the hood.
**Key insight:** Python data has *type*. A number is not a string. Claude knows this — but now you will too.
**Previous module:** None (this is Module 1)
**Next module:** Making Decisions (Module 2) — conditionals and dictionaries

---

## Screens

### Screen 1: Names & Values
**Concept:** Variables are names that point to values. snake_case is Python convention. None means "intentionally empty."
**Teaching arc:** Start with the assignment operator. Make it concrete. Then cover None.

**Translation block:**
```python
user_name = "Alice"
score = 42
is_active = True
last_login = None
```
Plain English (line by line):
- `user_name = "Alice"` → Create a label called "user_name" and attach it to the text "Alice"
- `score = 42` → Create a label called "score" pointing to the number 42
- `is_active = True` → A yes/no flag — "is this user active?" Answer: yes
- `last_login = None` → Intentionally empty — this user has never logged in. None is not zero, not empty string — it means "no value yet"

**Callout (callout-info):**
> Python uses `snake_case` (underscores between words) for variable names. Java and JavaScript use `camelCase`. Neither is wrong — they are just different conventions. When you tell Claude "create a variable for user name," it will automatically write `user_name` in Python.

**Glossary terms on this screen:**
- `variable` → A named label that points to a value in memory — like a Post-it note with a name, stuck to a piece of data
- `snake_case` → Naming convention where words are separated by underscores: `user_name`, `is_active`. Python's standard style
- `None` → Python's way of saying "intentionally no value." Not zero. Not empty. Just... absent. Like an empty slot in a form

---

### Screen 2: Strings Are More Than Text
**Concept:** Strings have built-in methods. f-strings embed values.
**Teaching arc:** Show methods as "verbs attached to text." Then show f-strings as a template engine.

**Flow animation actors:** `raw_string` → `.upper()` → `.strip()` → `f"Hello, {name}!"`
Steps:
1. `{highlight: "flow-actor-1", label: "Start with a raw string: email from a signup form"}` 
2. `{highlight: "flow-actor-1", label: "Apply .strip() to remove accidental spaces", packet: true, from: "actor-1", to: "actor-2"}`
3. `{highlight: "flow-actor-2", label: "Apply .lower() to standardize for database storage", packet: true, from: "actor-2", to: "actor-3"}`
4. `{highlight: "flow-actor-3", label: "Build a greeting with an f-string: f\"Welcome, {name}!\"", packet: true, from: "actor-3", to: "actor-4"}`
5. `{highlight: "flow-actor-4", label: "Result: a clean, personalized greeting ready to display"}`

**Callout (callout-accent):**
> The `f` in `f"Hello, {name}"` stands for "formatted." The `{}` curly braces act as windows into your code — whatever is inside gets substituted with its value. Claude uses f-strings constantly. Now you know what the curly braces mean.

**Glossary terms:**
- `string` → Any sequence of text in Python. Defined with quotes. "Alice", "hello@example.com", "42" (note: "42" is text, 42 is a number)
- `method` → A function built into a type. `.strip()` is a method of strings — a verb that belongs to text. Call it with dot notation: `text.strip()`
- `f-string` → A string with a lowercase f in front. Anything in {} gets replaced with the value of that expression. `f"Score: {42}"` becomes `"Score: 42"`

---

### Screen 3: Lists vs Tuples
**Concept:** Both hold sequences. Lists are mutable (changeable). Tuples are immutable (fixed forever).
**Teaching arc:** Group chat animation with two characters.

**Group chat:** id="chat-lists-tuples"
Actors: List (actor-1, coral), Tuple (actor-2, teal)

Messages:
1. List → "Hey! I hold your tasks. You can add new ones anytime — `.append('buy milk')` and I grow."
2. Tuple → "I hold your (latitude, longitude) coordinates. Once set at birth, never changed."
3. List → "You can also remove tasks from me with `.pop()` or `.remove()`."
4. Tuple → "Mutability? No thanks. Being fixed is a *feature* — my coordinates will never accidentally change."
5. List → "I can also be sorted! `.sort()` or `sorted(me)` — your choice."
6. Tuple → "I'm faster and use less memory. When your data should be fixed, use me. When it changes — use List."

**Callout (callout-warning):**
> Common mistake: trying to do `my_tuple[0] = "new value"` on a tuple. Python will throw a `TypeError`. This is intentional — tuples protect data that should never change.

**Glossary terms:**
- `list` → An ordered, changeable collection of items in Python. Written with square brackets: `[1, 2, 3]`. You can add, remove, and reorder items
- `tuple` → An ordered, fixed collection. Written with parentheses: `(42.3, -73.9)`. Once created, cannot be changed. Great for coordinates, RGB colors, or anything that represents a single unchangeable unit
- `mutable` → Can be changed after creation. Lists are mutable
- `immutable` → Cannot be changed after creation. Tuples and strings are immutable

---

### Screen 4: Reading Lists
**Concept:** Indexing, negative indexing, slicing.
**Teaching arc:** Translation block showing visual indexing.

**Translation block:**
```python
tasks = ["buy milk", "write report", "call Alice", "review PR"]

first = tasks[0]        # "buy milk"
last  = tasks[-1]       # "review PR"
two   = tasks[1:3]      # ["write report", "call Alice"]
rev   = tasks[::-1]     # reversed: last item first
```
Plain English:
- `tasks[0]` → Index 0 is the first item. Python always counts from 0, not 1
- `tasks[-1]` → Negative index = count from the back. -1 is the last item. -2 is second-to-last
- `tasks[1:3]` → Slice from index 1 up to (but not including) index 3 — gives items at index 1 and 2
- `tasks[::-1]` → Slice with step -1: start from the end, move backward — reverses the list

**Callout (callout-info):**
> Python counts from 0. This surprises everyone at first. Think of it like a ruler: the first item is at position 0, not position 1. After a few weeks, 0-indexing feels completely natural — and you start finding 1-indexing strange.

**Glossary terms:**
- `index` → The position of an item in a list. Python starts counting at 0. `tasks[0]` is the first item
- `slice` → A way to grab a chunk of a list. `tasks[1:3]` means "from index 1, up to (not including) index 3"
- `negative index` → Count from the end of the list. `-1` is always the last item, no matter how long the list is

---

### Screen 5: List Comprehensions
**Concept:** Compact syntax to build new lists from existing ones — with optional filtering.
**Teaching arc:** Flow animation showing transformation pipeline.

**Flow animation:**
Actors: Source List → Filter → Transform → Result
Steps (use double-quotes for data-steps to avoid apostrophe issues):
1. `{"highlight":"flow-actor-1","label":"Start: a list of numbers [1, 2, 3, 4, 5, 6, 7, 8]"}`
2. `{"highlight":"flow-actor-2","label":"Filter: keep only even numbers (if n % 2 == 0)"}`
3. `{"highlight":"flow-actor-2","label":"[2, 4, 6, 8] pass the filter","packet":true,"from":"actor-2","to":"actor-3"}`
4. `{"highlight":"flow-actor-3","label":"Transform: square each one (n * n)"}`
5. `{"highlight":"flow-actor-3","label":"[4, 16, 36, 64] ready","packet":true,"from":"actor-3","to":"actor-4"}`
6. `{"highlight":"flow-actor-4","label":"Result: evens_squared = [4, 16, 36, 64]"}`

**Translation block:**
```python
numbers = [1, 2, 3, 4, 5, 6, 7, 8]

# Long way (for loop)
result = []
for n in numbers:
    if n % 2 == 0:
        result.append(n * n)

# Short way (comprehension)
result = [n * n for n in numbers if n % 2 == 0]
```
Plain English:
- Long way: make an empty list, loop through numbers, check if even, square it, add it
- Short way: `[expression for item in source if condition]`
- They produce identical results — the comprehension is just more compact
- Claude almost always writes the short form — now you can read it

**Callout (callout-accent):**
> When you ask Claude to "filter a list and transform each item," it will almost always write a comprehension. This is idiomatic Python — the "native way" to express this idea. Seeing `[x for x in things if condition]` means: go through things, keep some, transform each one.

---

## Quiz (id="quiz-module1")

**Q1** (correct: option-b)
> You have a list of filenames. Which expression gives you only the `.py` files?

- option-a: `files.filter(".py")`
- option-b: `[f for f in files if f.endswith(".py")]` ✓
- option-c: `files.find(".py")`
- option-d: `for f in files: if ".py" in f`

right explanation: "Exactly! List comprehensions with a condition (`if ...`) are how Python filters lists. `.endswith()` checks if a string ends with a given suffix — perfect for file extensions."
wrong explanation: "Python lists don't have a `.filter()` method. The Pythonic way to filter is a comprehension with an `if` clause."

**Q2** (correct: option-c)
> Your code does: `if my_list:` to check if a list has items. A colleague says "that's wrong, you should use `len(my_list) > 0`". Who is right?

- option-a: The colleague — `len()` is more explicit
- option-b: Neither — you need `my_list != []`
- option-c: You — empty lists are "falsy" in Python, so `if my_list:` correctly checks if it has items ✓
- option-d: Both work identically, but `len()` is faster

right explanation: "Correct! In Python, empty collections (`[]`, `{}`, `''`) are 'falsy' — they evaluate to False in a condition. `if my_list:` is the idiomatic, Pythonic way to check if a list has items."
wrong explanation: "`len(my_list) > 0` works, but `if my_list:` is the Python idiom. The colleague is being more verbose than necessary. In Python, empty means false."

**Q3** (drag-and-drop: match type to property)
Chips: `list`, `tuple`, `str`
Zones:
- Mutable (can be changed after creation) → correct: `list`
- Immutable, ordered, often used for fixed records → correct: `tuple`
- Immutable sequence of characters → correct: `str`
