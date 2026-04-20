# Module 3 Brief: Keeping Things Moving
**Covers:** Ch7 (input(), while loops, break/continue, while-else) + Ch8 (functions, args/kwargs, defaults, scope, lambdas, type hints)
**Metaphor:** Functions are vending machines — same buttons every time, different items come out depending on your selection.
**Opening hook:** The `while True` + `break` pattern is in almost every Claude-generated interactive script. Here is why.
**Key insight:** Loops are repetition. Functions are reuse. Together they are the core engine of all programs.
**Previous module:** Module 2 (conditionals, dicts)
**Next module:** Module 4 (classes and objects)

---

## Screens

### Screen 1: While Loops — Keep Going Until
**Concept:** `while` repeats as long as a condition is true. `break` exits early. `continue` skips to the next iteration.
**Teaching arc:** Flow animation showing circular execution.

**Flow animation:**
Actors: Condition Check → Loop Body → Break → Continue
Steps:
1. `{"highlight":"flow-actor-1","label":"Check condition: is count < 5? Yes."}`
2. `{"highlight":"flow-actor-2","label":"Run the loop body: print(count), count += 1","packet":true,"from":"actor-1","to":"actor-2"}`
3. `{"highlight":"flow-actor-1","label":"Check again: is count < 5? Yes. Keep going.","packet":true,"from":"actor-2","to":"actor-1"}`
4. `{"highlight":"flow-actor-3","label":"User types quit — break fires! Loop exits immediately","packet":true,"from":"actor-2","to":"actor-3"}`
5. `{"highlight":"flow-actor-4","label":"Or: continue skips rest of body, jumps back to condition","packet":true,"from":"actor-2","to":"actor-4"}`
6. `{"highlight":"flow-actor-1","label":"Eventually condition becomes False — loop exits naturally"}`

**Callout (callout-warning):**
> Infinite loops happen when the condition never becomes False and there is no `break`. Python will run forever until you force-stop it. Always make sure your loop has an exit condition.

**Translation block:**
```python
count = 0
while count < 5:
    if count == 3:
        count += 1
        continue   # skip printing 3
    print(count)
    count += 1
```
Plain English:
- `while count < 5:` → Keep repeating while count is less than 5
- `if count == 3:` → Special case: skip the number 3
- `continue` → Skip the rest of this iteration; jump back to the `while` check
- `print(count)` → Normal case: print the number
- `count += 1` → Increment the counter (Python has no `++`)

**Glossary terms:**
- `while loop` → Repeats a block of code as long as a condition is true. Unlike `for`, it does not need to count through a collection
- `break` → Immediately exits the loop, no matter what the condition says
- `continue` → Skip the rest of the current iteration and jump back to the condition check
- `infinite loop` → A loop whose condition never becomes False. Will run until the program is force-stopped

---

### Screen 2: The Input Loop Pattern
**Concept:** `while True` + `input()` + `break` is the standard pattern for interactive command-line programs.
**Teaching arc:** Group chat simulating a CLI session.

**Group chat:** id="chat-input-loop"
Actors: Your Script (actor-1, teal), User (actor-2, amber), Loop Engine (actor-3, forest)

Messages:
1. Loop Engine → "`while True:` starts — I will keep running until someone breaks me"
2. Your Script → "I call `input('> ')` — waiting for user to type something"
3. User → "I type: `add buy milk`"
4. Your Script → "I receive `'add buy milk'`. I parse it: command='add', task='buy milk'"
5. Your Script → "I add 'buy milk' to the tasks list and print 'Added!'"
6. Loop Engine → "Back to the top of `while True:` — waiting for next input"
7. User → "I type: `quit`"
8. Your Script → "Command is 'quit' — I call `break`"
9. Loop Engine → "Loop exits. Program ends. This pattern is in almost every CLI Claude writes."

**Translation block:**
```python
tasks = []
while True:
    user_input = input("Command: ").strip()
    if not user_input:
        continue
    if user_input == "quit":
        break
    tasks.append(user_input)
    print(f"Added: {user_input}")
```
Plain English:
- `while True:` → Run forever (intentional) — we control exit with `break`
- `input("Command: ").strip()` → Show a prompt, wait for user, remove surrounding spaces
- `if not user_input: continue` → If user pressed Enter without typing, skip and ask again
- `if user_input == "quit": break` → User typed quit — exit the loop
- `tasks.append(user_input)` → Add whatever they typed to our tasks list

**Callout (callout-accent):**
> This `while True` + `break` pattern replaces the "do-while" loop that other languages have. When you see it in Claude-generated code, it means: "keep asking until the user is done." The loop itself does not know when to stop — the `break` inside the body decides that.

---

### Screen 3: Functions — Packaging Work
**Concept:** A function wraps a block of code into a named unit. Call it anytime with different inputs.
**Teaching arc:** Flow animation (function machine).

**Flow animation:**
Actors: Caller → Function Entry → Process → Return
Steps:
1. `{"highlight":"flow-actor-1","label":"Caller: greet('Alice') — sending 'Alice' as argument"}`
2. `{"highlight":"flow-actor-2","label":"Function receives: name = 'Alice'","packet":true,"from":"actor-1","to":"actor-2"}`
3. `{"highlight":"flow-actor-3","label":"Process: builds greeting = f'Hello, Alice!'","packet":true,"from":"actor-2","to":"actor-3"}`
4. `{"highlight":"flow-actor-4","label":"return greeting — sends result back to caller","packet":true,"from":"actor-3","to":"actor-4"}`
5. `{"highlight":"flow-actor-1","label":"Caller receives 'Hello, Alice!' — can call again with 'Bob'","packet":true,"from":"actor-4","to":"actor-1"}`

**Callout (callout-info):**
> A function with no `return` statement returns `None`. This surprises people who expect `print()` to count — it does not. `print()` shows text to the screen; `return` sends a value back to the caller. These are different operations.

**Glossary terms:**
- `function` → A named, reusable block of code. Define once with `def`, call many times with `function_name()`
- `parameter` → The variable name in the function definition: `def greet(name)` — `name` is the parameter
- `argument` → The actual value passed when calling: `greet("Alice")` — `"Alice"` is the argument
- `return` → Sends a value back to the caller and exits the function. Functions with no `return` give back `None`

---

### Screen 4: Args, Kwargs & Defaults
**Concept:** Functions can have positional args, keyword args, defaults, `*args`, and `**kwargs`.
**Teaching arc:** Translation block + badge list for each parameter type.

**Translation block:**
```python
def create_task(
    title: str,
    priority: int = 2,
    *tags: str,
    due_date: str | None = None
) -> dict:
    return {
        "title": title,
        "priority": priority,
        "tags": tags,
        "due_date": due_date
    }

# Calling it
task = create_task("Buy milk", 1, "shopping", "errands", due_date="2024-12-01")
```
Plain English:
- `title: str` → Required argument. Must be provided. `: str` is a type hint — just a label, not enforced
- `priority: int = 2` → Optional — defaults to 2 if not given
- `*tags: str` → Collect any extra positional arguments into a tuple. "Buy milk", "shopping" ... all extras go here
- `due_date: str | None = None` → Keyword-only argument — must be named when calling: `due_date="..."`
- `-> dict` → Type hint saying this function returns a dict

**Badge list:**
- `positional arg` → Matched by position. `create_task("Buy milk")` — first arg is title
- `default arg` → Has a fallback. If you do not provide it, the default is used
- `*args` → Collects unlimited extra positional arguments into a tuple
- `**kwargs` → Collects unlimited keyword arguments into a dict
- `type hint` → Optional label for humans (and AI) — Python does not enforce it at runtime

**Glossary terms:**
- `type hint` → A label on a parameter or return value showing what type is expected: `name: str`. Python ignores it at runtime — it is documentation for humans and tools like Claude
- `*args` → Starred parameter that collects unlimited extra positional arguments into a tuple
- `**kwargs` → Double-starred parameter that collects unlimited keyword arguments into a dictionary
- `default parameter` → A parameter with a fallback value. Used when the caller does not provide that argument

---

### Screen 5: Scope — What Can See What
**Concept:** Variables live in scopes. LEGB: Local → Enclosing → Global → Built-in. Lambda is a compact function.
**Teaching arc:** Flow animation with nested boxes showing LEGB. Then lambda compression demo.

**Step cards (LEGB rule):**
1. **Local** → Inside the current function. Only exists while the function runs
2. **Enclosing** → Outer function scope (for nested functions). The enclosing function can share its variables
3. **Global** → Module level — the whole file. Use `global x` to modify from inside a function
4. **Built-in** → Python built-ins: `len`, `print`, `range` — always available everywhere

**Translation block:**
```python
# Long form function
def is_even(n):
    return n % 2 == 0

# Lambda (anonymous function) — same thing, one line
is_even = lambda n: n % 2 == 0

# Common use: sorting
tasks.sort(key=lambda t: t["priority"])
```
Plain English:
- `def is_even(n):` → Named function taking one parameter
- `lambda n: n % 2 == 0` → Anonymous function: "take n, return `n % 2 == 0`"
- `key=lambda t: t["priority"]` → "For sorting, extract the priority field from each task"
- Lambdas cannot have multiple lines — for anything complex, use a real `def`

**Callout (callout-accent):**
> Lambdas appear constantly in Claude-generated code, especially as `key=` arguments to `sort()` and `sorted()`. `sorted(items, key=lambda x: x["name"])` means "sort these items by their name field." Once you see the pattern, lambdas become easy to read.

**Glossary terms:**
- `scope` → Where a variable can be seen. Variables inside a function are "local" — invisible outside it
- `LEGB` → Python scope lookup order: Local → Enclosing → Global → Built-in. Python searches this chain when it encounters a name
- `lambda` → A compact, anonymous (unnamed) function. `lambda x: x + 1` is a function that adds 1 to its argument

---

## Quiz (id="quiz-module3")

**Q1** (scenario, correct: option-b)
> Scenario: You want to keep asking the user for input until they type "done." Which loop pattern is correct?

- option-a: `for i in range(100): if input() == "done": break`
- option-b: `while True: cmd = input(); if cmd == "done": break` ✓
- option-c: `while input() != "done": pass`
- option-d: `for cmd in input(): if cmd == "done": break`

right: "Correct! `while True` with a `break` is the standard Python pattern for open-ended input loops. It runs until the user explicitly triggers the exit condition."
wrong: "That approach has problems. Using `range(100)` limits to 100 iterations. `while input()` calls input in the condition which makes it hard to use the value."

**Q2** (correct: option-c)
> A function is defined as `def greet(name, greeting="Hello"):`. Which call is valid?

- option-a: `greet()` — missing required arg
- option-b: `greet(greeting="Hi")` — still missing required arg
- option-c: `greet("Alice")` ✓
- option-d: `greet("Alice", "Hi", "extra")` — too many args

right: "Right! `name` is required (no default), `greeting` is optional (defaults to 'Hello'). `greet('Alice')` provides the required argument and uses the default for the optional one."
wrong: "Check which parameters have defaults and which do not. Required parameters must always be provided."

**Q3** (correct: option-a)
> You see `tasks.sort(key=lambda t: t["due_date"])` in Claude-generated code. What does this do?

- option-a: Sorts the tasks list in-place, ordering tasks by their due_date field ✓
- option-b: Filters tasks to only include those with a due_date
- option-c: Returns a new sorted list (the original is unchanged)
- option-d: Groups tasks by due_date

right: "Exactly! `.sort()` modifies the list in-place. The `key=lambda t: t['due_date']` tells Python which value to use for comparing items during sorting."
wrong: "`.sort()` sorts in-place (modifies the original). Use `sorted()` if you want a new list. The lambda extracts the comparison key from each item."
