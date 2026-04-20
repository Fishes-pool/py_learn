# Module 2 Brief: Making Decisions
**Covers:** Ch5 (conditionals, truthiness, match/case, ternary) + Ch6 (dicts, comprehensions, nested, defaultdict)
**Metaphor:** Conditionals are a traffic roundabout — every car follows the same rules but takes a different exit.
**Opening hook:** Every time Claude writes "check if the user is logged in," it uses these exact structures.
**Key insight:** Python evaluates many things as True or False — not just booleans. And dictionaries are how Python stores almost everything structured.
**Previous module:** Module 1 (variables, lists, tuples)
**Next module:** Module 3 (loops and functions)

---

## Screens

### Screen 1: Truthiness — More Than True/False
**Concept:** In Python, many values evaluate as True or False in conditions — not just `True` and `False` literals.
**Teaching arc:** Interactive truth meter cards + `==` vs `is` side-by-side.

**Pattern cards grid (4 cards):**
- 🟢 Truthy values: Non-zero numbers, non-empty strings, non-empty lists — "something there"
- 🔴 Falsy values: `0`, `""`, `[]`, `{}`, `None`, `False` — "nothing there"
- ⚠️ `==` checks value equality: `"admin" == "admin"` → True
- 🔑 `is` checks identity: `x is None` → True only if x IS None (same object in memory)

**Translation block:**
```python
users = []
role = ""
count = 0
name = None

if users:          # empty list → False
    send_emails()

if not role:       # empty string → False, not flips it
    ask_for_role()

if count == 0:     # explicit comparison
    show_empty_state()

if name is None:   # identity check for None
    set_default_name()
```
Plain English:
- `if users:` → "if users has anything in it" — no `.length > 0` needed
- `if not role:` → "if role is empty" — `not` flips False to True
- `if count == 0:` → explicit equality check — both styles work, this one is clearer for numbers
- `if name is None:` → ALWAYS use `is` (not `==`) to check for None — it is the Python convention

**Glossary terms:**
- `boolean` → A True or False value. In Python, written as `True` and `False` (capital T and F)
- `truthy` → A value that Python treats as True in a condition, even if it is not `True` itself. Non-empty lists, non-zero numbers, non-empty strings are truthy
- `falsy` → A value Python treats as False in a condition: `0`, `""`, `[]`, `{}`, `None`, `False`

---

### Screen 2: If/Elif/Else — The Roundabout
**Concept:** Python evaluates conditions top to bottom. First match wins. Else is the default exit.
**Teaching arc:** Flow animation showing branching.

**Flow animation:**
Actors: Request → if-check → elif-check → elif-check → else
Steps:
1. `{"highlight":"flow-actor-1","label":"A request arrives with role = 'viewer'"}`
2. `{"highlight":"flow-actor-2","label":"if role == 'admin': False — skip this branch","packet":true,"from":"actor-1","to":"actor-2"}`
3. `{"highlight":"flow-actor-3","label":"elif role == 'editor': False — skip this too","packet":true,"from":"actor-2","to":"actor-3"}`
4. `{"highlight":"flow-actor-4","label":"elif role == 'viewer': True! Enter this branch","packet":true,"from":"actor-3","to":"actor-4"}`
5. `{"highlight":"flow-actor-4","label":"show_read_only_view() executes — done, rest is skipped"}`

**Callout (callout-info):**
> Python stops at the FIRST True branch. If `role == 'viewer'` matches, the `else` block is skipped entirely. This is called "short-circuit" evaluation — efficient and predictable.

**Glossary terms:**
- `if` → Start of a conditional block. Python evaluates the condition. If True, runs the indented code
- `elif` → "else if" — checked only if all previous conditions were False
- `else` → Catch-all block — runs only if no previous condition was True

---

### Screen 3: Match/Case — Routing Made Clean
**Concept:** Python 3.10+ `match/case` is cleaner than long if/elif chains when routing on a single value.
**Teaching arc:** Group chat showing router behavior.

**Group chat:** id="chat-match-case"
Actors: Router (actor-1, teal), if/elif Block (actor-2, amber), match/case Block (actor-3, forest)

Messages:
1. Router → "Got command: 'quit'"
2. if/elif Block → "I check: `if cmd == 'help': ... elif cmd == 'quit': ... elif cmd == 'list': ...` — works, but verbose."
3. match/case Block → "I do it cleaner: `match cmd: case 'help': ... case 'quit': ... case _:`"
4. Router → "Both give identical results. But match/case reads more like a table of options."
5. match/case Block → "The `case _:` is the default — like else. It catches anything that did not match."
6. Router → "Use if/elif for complex logic. Use match/case when you are routing a single value to one of many fixed options."

**Translation block:**
```python
command = input("Enter command: ")

match command:
    case "help":
        show_help()
    case "quit":
        exit_app()
    case "list":
        show_tasks()
    case _:
        print(f"Unknown command: {command}")
```
Plain English:
- `match command:` → "Look at the value of `command` and find a matching case"
- `case "help":` → "If command is exactly 'help', run this block"
- `case _:` → "Default: if nothing above matched, run this. The `_` means 'anything else'"

**Glossary terms:**
- `match/case` → Python 3.10+ pattern matching. Like a cleaner if/elif for routing a value to different code paths
- `case _` → The wildcard/default case. Runs when no other case matched. Equivalent to `else`

---

### Screen 4: Dictionaries as Named Storage
**Concept:** Dicts map keys to values. Access with brackets or `.get()`. Add/update with assignment.
**Teaching arc:** Translation block showing dict operations.

**Callout (callout-accent):**
> When Claude writes code to handle an API response, parse a form submission, or configure settings — it almost always uses a dictionary. JSON data (from web APIs) becomes a Python dict the moment you load it. Understanding dicts means understanding how Claude reads the outside world.

**Translation block:**
```python
user = {
    "name": "Alice",
    "role": "admin",
    "score": 0
}

name = user["name"]           # "Alice"
role = user.get("role", "viewer")  # safe: default if missing
user["score"] = 10            # update existing key
user["email"] = "a@b.com"    # add new key
del user["score"]             # remove a key
```
Plain English:
- `user["name"]` → Look up the value stored at key "name" — returns "Alice"
- `user.get("role", "viewer")` → Safe lookup: if "role" exists, return it; otherwise return "viewer" as default
- `user["score"] = 10` → Set or update the value at key "score"
- `user["email"] = "a@b.com"` → Add a new key-value pair — dicts grow dynamically
- `del user["score"]` → Remove the key (and its value) entirely

**Glossary terms:**
- `dictionary` → A Python data structure that maps keys to values. Like a real dictionary: you look up a word (key) to find its definition (value). Written with `{}`
- `key` → The label in a dictionary. Used to look up values. Usually a string, but can be any immutable type
- `value` → What you get when you look up a key. Can be any type — string, number, list, even another dict
- `.get()` → A safe way to look up a dictionary key. Returns a default value instead of crashing if the key does not exist

---

### Screen 5: Nested Dicts & Comprehensions
**Concept:** Dicts can contain other dicts. Dict comprehensions transform key-value pairs.
**Teaching arc:** Nested dict explorer + comprehension comparison.

**Step cards (nested dict access):**
1. Start with a response dict: `data = {"user": {"name": "Alice", "address": {"city": "NYC"}}}`
2. Access first level: `data["user"]` → gives you the inner user dict
3. Access second level: `data["user"]["name"]` → "Alice"
4. Access third level: `data["user"]["address"]["city"]` → "NYC"
5. Safer: `data.get("user", {}).get("address", {}).get("city", "unknown")`

**Translation block:**
```python
scores = {"Alice": 92, "Bob": 45, "Carol": 88, "Dave": 30}

# Dict comprehension: keep only scores >= 60
passing = {name: score
           for name, score in scores.items()
           if score >= 60}
# Result: {"Alice": 92, "Carol": 88}
```
Plain English:
- `scores.items()` → Loop through both keys AND values at once — returns pairs like `("Alice", 92)`
- `for name, score in ...` → Unpack each pair into two variables
- `if score >= 60` → Only include this pair in the result if the condition is true
- The pattern: `{key_expr: value_expr for k, v in d.items() if condition}`

**Callout (callout-info):**
> Dict comprehensions mirror list comprehensions exactly — just use `{}` and include a `key: value` expression. When Claude writes code to "filter a dict" or "transform all values," this is the pattern it reaches for.

---

## Quiz (id="quiz-module2")

**Q1** (correct: option-c)
> Your code has: `user_list = get_users()`. You want to check if any users were returned. What is the most Pythonic way?

- option-a: `if user_list != []:`
- option-b: `if len(user_list) > 0:`
- option-c: `if user_list:` ✓
- option-d: `if user_list == True:`

right: "Correct! In Python, an empty list is falsy. `if user_list:` is the idiomatic way. Knowing this lets you write cleaner code and read Claude-generated code without confusion."
wrong: "That works, but it is not idiomatic Python. Since empty lists are falsy, `if user_list:` expresses the same intent more cleanly."

**Q2** (correct: option-b)
> A config dict might not have a "timeout" key. Which access is safest?

- option-a: `config["timeout"]` — crashes with KeyError if missing
- option-b: `config.get("timeout", 30)` ✓
- option-c: `try: config["timeout"] except: 30`
- option-d: `"timeout" in config and config["timeout"]`

right: "Exactly! `.get(key, default)` is the safe, idiomatic way to access a dict when a key might be absent. The default is returned instead of raising a KeyError."
wrong: "That approach works but is more verbose than needed. `.get()` was designed for exactly this case."

**Q3** (scenario, correct: option-a)
> Scenario: You are writing code to process commands: 'start', 'stop', 'status', 'restart'. Each needs different code. Which Python structure fits best?

- option-a: `match command: case "start": ...` ✓
- option-b: A long chain of `if command == "start": ... elif command == "stop": ...`
- option-c: A list comprehension
- option-d: A while loop

right: "Right! When routing a single value to one of several fixed cases, match/case is cleaner and more readable than a long if/elif chain."
wrong: "if/elif works, but match/case was designed for exactly this routing pattern and is much cleaner."
