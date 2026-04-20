# Module 5 Brief: The Outside World
**Covers:** Ch10 (with open, pathlib, JSON, try/except/else/finally, custom exceptions)
**Metaphor:** Context managers are a library borrowing system — the book is checked out, used, and automatically returned when done. Even if you forget.
**Opening hook:** Almost every practical script Claude writes for you touches a file or an API. Here is what is happening in those `with open(...)` lines.
**Key insight:** The outside world fails unexpectedly. Good code expects failure and handles it gracefully.
**Previous module:** Module 4 (classes)
**Next module:** Module 6 (testing)

---

## Screens

### Screen 1: Files with Context Managers
**Concept:** `with open(...)` is a context manager — it opens a file, gives you access, and closes it automatically when done, even if an error occurs.
**Teaching arc:** Flow animation showing file lifecycle.

**Flow animation:**
Actors: Your Code → Context Manager → File → Cleanup
Steps:
1. `{"highlight":"flow-actor-1","label":"Your code: `with open('data.txt') as f:`"}`
2. `{"highlight":"flow-actor-2","label":"Context manager calls __enter__: opens the file, returns file object","packet":true,"from":"actor-1","to":"actor-2"}`
3. `{"highlight":"flow-actor-3","label":"File is now open — you can read or write","packet":true,"from":"actor-2","to":"actor-3"}`
4. `{"highlight":"flow-actor-2","label":"Indented block finishes — __exit__ fires automatically","packet":true,"from":"actor-3","to":"actor-2"}`
5. `{"highlight":"flow-actor-4","label":"File closes — even if an exception occurred inside the block"}`
6. `{"highlight":"flow-actor-1","label":"Code continues normally after the with block"}`

**Translation block:**
```python
from pathlib import Path

data_file = Path("tasks.txt")

# Write
with open(data_file, "w") as f:
    f.write("Buy milk\n")
    f.write("Call Alice\n")

# Read
with open(data_file, "r") as f:
    for line in f:
        print(line.strip())
```
Plain English:
- `Path("tasks.txt")` → A cross-platform path object — works on Mac, Windows, Linux
- `open(data_file, "w")` → Open for writing — creates the file if it does not exist, overwrites if it does
- `with ... as f:` → Context manager: f is the open file. When the `with` block ends, f closes automatically
- `f.write("text\n")` → Write text to the file. `\n` is a newline character
- `open(data_file, "r")` → Open for reading. Default mode — "r" is optional

**Glossary terms:**
- `context manager` → An object that manages a resource (like a file). The `with` statement calls `__enter__` to set up and `__exit__` to clean up, even if an error occurs
- `with statement` → Python syntax for using a context manager. Guarantees the cleanup runs
- `pathlib.Path` → A modern Python object for representing file paths. Cross-platform, composable with `/`
- `file mode` → How to open a file: "r" = read, "w" = write (overwrite), "a" = append, "rb"/"wb" = binary

---

### Screen 2: JSON — Python Meets the Web
**Concept:** JSON is how data travels on the internet. Python dicts convert to/from JSON instantly.
**Teaching arc:** Translation block + live conversion demo.

**Translation block:**
```python
import json

user = {
    "name": "Alice",
    "score": 95,
    "tags": ["admin", "active"]
}

# Python dict → JSON string
json_str = json.dumps(user, indent=2)

# JSON string → Python dict
loaded = json.loads(json_str)

# Write to file
with open("user.json", "w") as f:
    json.dump(user, f, indent=2)

# Read from file
with open("user.json", "r") as f:
    data = json.load(f)
```
Plain English:
- `json.dumps(user)` → "dump to string" — converts Python dict to a JSON-formatted string
- `json.loads(json_str)` → "load from string" — converts JSON string back to Python dict
- `indent=2` → Pretty-print with 2-space indentation. Without this, it is one long unreadable line
- `json.dump(user, f)` → Write JSON directly to an open file (no string in between)
- `json.load(f)` → Read JSON directly from an open file — returns a Python dict

**Callout (callout-accent):**
> Every API response Claude parses is JSON. The moment you do `response.json()` in a requests call, Python converts the JSON to a plain dict — and you can access it with all the dict skills from Module 2. `data["user"]["profile"]["city"]` is literally how you read an API response.

**Glossary terms:**
- `JSON` → JavaScript Object Notation. A text format for storing structured data. Python dicts look almost identical — keys must be strings, though
- `json.dumps()` → "dump string" — converts a Python object to a JSON string
- `json.loads()` → "load string" — converts a JSON string back to a Python object
- `serialization` → Converting in-memory data to a storable/transmittable format. JSON is a serialization format

---

### Screen 3: Try/Except — Expecting the Unexpected
**Concept:** `try/except` catches errors before they crash your program. `else` runs if no error. `finally` always runs.
**Teaching arc:** Flow animation with "danger zone" showing all four branches.

**Flow animation:**
Actors: try block → except block → else block → finally block
Steps:
1. `{"highlight":"flow-actor-1","label":"Python enters the try block: run the risky code"}`
2. `{"highlight":"flow-actor-1","label":"Attempt: open the config file and read it"}`
3. `{"highlight":"flow-actor-2","label":"ERROR! File not found — Python jumps to except","packet":true,"from":"actor-1","to":"actor-2"}`
4. `{"highlight":"flow-actor-2","label":"except FileNotFoundError: handle it gracefully — use defaults"}`
5. `{"highlight":"flow-actor-4","label":"finally always runs — log that we attempted, clean up resources","packet":true,"from":"actor-2","to":"actor-4"}`
6. `{"highlight":"flow-actor-3","label":"(On success path: else runs when try succeeds with no exception)"}`

**Translation block:**
```python
try:
    with open("config.json", "r") as f:
        config = json.load(f)
except FileNotFoundError:
    config = {"debug": False, "timeout": 30}
    print("Config not found — using defaults")
except json.JSONDecodeError as e:
    print(f"Invalid JSON in config: {e}")
    config = {}
else:
    print("Config loaded successfully")
finally:
    print("Setup complete")  # always runs
```
Plain English:
- `try:` → Attempt this risky code
- `except FileNotFoundError:` → If the file does not exist, handle it here (no crash)
- `except json.JSONDecodeError as e:` → If the JSON is malformed, handle it here — `e` holds the error details
- `else:` → Runs only if the try block completed with NO exception
- `finally:` → Runs no matter what — success, failure, or exception. Use for cleanup

**Glossary terms:**
- `exception` → An error that Python raises when something goes wrong. If uncaught, it crashes the program
- `try/except` → A block that catches exceptions. Code in `try` runs; if an error occurs, the matching `except` handles it
- `FileNotFoundError` → Raised when you try to open a file that does not exist
- `finally` → A block that always executes — after try, after except, always. Used for cleanup (close connections, log results)

---

### Screen 4: The Exception Hierarchy
**Concept:** Python exceptions form a hierarchy — catching a parent type also catches its children.
**Teaching arc:** Architecture diagram showing exception tree.

**Architecture diagram:**
Zones and components:
Zone "Python Exceptions":
- `BaseException` (data-desc: The root of all Python exceptions. Rarely caught directly — reserved for system events like KeyboardInterrupt)
  - `Exception` (data-desc: The base for all regular exceptions. Catching `Exception` catches almost everything except system events)
    - `ValueError` (data-desc: Raised when a value has the wrong type or value: `int("hello")`, `[][-1]` — wait, that is IndexError)
    - `TypeError` (data-desc: Raised when an operation is applied to the wrong type: `"hello" + 5`)
    - `KeyError` (data-desc: Raised when a dictionary key does not exist: `d["missing"]`)
    - `FileNotFoundError` (data-desc: Raised when a file does not exist. It is a subclass of OSError)
    - `IndexError` (data-desc: Raised when a list index is out of range: `my_list[100]` on a 3-item list)
    - `AttributeError` (data-desc: Raised when you access an attribute that does not exist: `obj.nonexistent`)

**Callout (callout-info):**
> Custom exceptions let you create specific error types for your domain. A payment app might define `PaymentDeclined(ValueError)` or `InsufficientFundsError(Exception)`. Claude often generates these — and now you know they are just subclasses of `Exception`.

---

## Quiz (id="quiz-module5")

**Q1** (scenario, correct: option-b)
> Scenario: Claude wrote code that calls `user["premium_tier"]` in a dict from an API. Some API users do not have this field. What is the safest fix?

- option-a: Wrap it in `try: ... except KeyError:`
- option-b: Change to `user.get("premium_tier", "free")` ✓
- option-c: Add an `if "premium_tier" in user:` check before every access
- option-d: Ask the API to always include this field

right: "Correct! `.get()` with a default is the cleanest solution — one line, no try/except needed. This is the everyday solution for optional dict keys."
wrong: "That works but is more code than needed. `.get(key, default)` handles this case in a single expression."

**Q2** (correct: option-c)
> Trace this code. Which statement(s) run when the file does not exist?

```python
try:
    f = open("missing.txt")
    data = f.read()
except FileNotFoundError:
    data = "default"
else:
    print("File loaded")
finally:
    print("Done")
```

- option-a: Just the `except` block
- option-b: `except` block and `else` block
- option-c: `except` block and `finally` block ✓
- option-d: Just `finally` block

right: "Correct! When an exception occurs, `except` catches it and `else` is skipped. `finally` ALWAYS runs regardless of success or failure."
wrong: "`else` only runs when the `try` block completes WITHOUT an exception. `finally` always runs."

**Q3** (correct: option-a)
> You want to write new log entries without overwriting old ones. Which file mode should you use?

- option-a: `open("log.txt", "a")` — append mode ✓
- option-b: `open("log.txt", "w")` — write mode (overwrites!)
- option-c: `open("log.txt", "r")` — read mode (cannot write)
- option-d: `open("log.txt", "rw")` — not a valid mode

right: "Right! Mode 'a' opens for appending — new content is added to the end. Mode 'w' creates a fresh file each time, deleting existing content."
wrong: "Mode 'w' is destructive — it truncates the file to zero length before writing. Use 'a' for append (adding to existing content)."
