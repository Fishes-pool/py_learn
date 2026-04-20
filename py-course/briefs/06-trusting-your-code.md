# Module 6 Brief: Trusting Your Code
**Covers:** Ch11 (pytest, assertions, fixtures, parametrize, mocking)
**Metaphor:** Tests are a ratchet wrench — each green test is a click that holds your progress and prevents slipping back.
**Opening hook:** When you ask Claude to "add tests," this is what it writes. Understanding tests means you can tell when Claude's tests are real versus decoration.
**Key insight:** Tests are a communication system — they tell future you (and future Claude) what the code was supposed to do.
**Previous module:** Module 5 (files and exceptions)
**Next module:** None (this is the final module)

---

## Screens

### Screen 1: Why Tests Exist
**Concept:** Tests catch regressions — changes that break things that used to work.
**Teaching arc:** Group chat showing before/after scenario.

**Group chat:** id="chat-why-tests"
Actors: You/Developer (actor-1, teal), Test Suite (actor-2, forest), The Code (actor-3, amber)

Messages:
1. You → "I refactored the discount calculation function. Should be faster now."
2. Test Suite → "Running 47 tests..."
3. Test Suite → "ERROR: `test_zero_discount_returns_full_price` FAILED"
4. You → "Wait — my refactor broke the zero-discount case?"
5. The Code → "Yes. The new formula divides by discount_pct. When pct=0, that is a ZeroDivisionError."
6. Test Suite → "Without me, you would have shipped this. Users would have seen a crash. With me, you caught it in 3 seconds."
7. You → "So tests are not just for finding bugs now — they prevent future regressions too."
8. Test Suite → "Exactly. Each green test is a ratchet click. Progress is locked in. You cannot accidentally slip backward."

**Callout (callout-accent):**
> When Claude generates tests alongside code, it is creating a record of intended behavior. The test says "this function should do X." If someone (including Claude on a later chat) changes the function and breaks X, the test fails loudly. Tests are a contract written in executable form.

**Glossary terms:**
- `test` → A piece of code that checks whether another piece of code works correctly
- `regression` → A bug introduced by a change — something that used to work now does not
- `pytest` → The most popular Python testing framework. Runs any function starting with `test_` automatically
- `test suite` → The collection of all tests for a project

---

### Screen 2: Writing Assertions
**Concept:** A pytest test is a function that asserts expected outcomes. If the assertion fails, pytest shows exactly what went wrong.
**Teaching arc:** Translation block showing assertion patterns.

**Translation block:**
```python
# File: test_calculator.py
from calculator import add, divide

def test_add_positive_numbers():
    result = add(3, 4)
    assert result == 7

def test_divide_by_zero_raises():
    import pytest
    with pytest.raises(ZeroDivisionError):
        divide(10, 0)

def test_add_returns_float():
    result = add(1.5, 2.5)
    assert isinstance(result, float)
    assert result == 4.0
```
Plain English:
- `def test_add_positive_numbers():` → Any function starting with `test_` is picked up by pytest automatically
- `assert result == 7` → "I expect result to equal 7. If not, stop and show me what it actually was."
- `with pytest.raises(ZeroDivisionError):` → "I expect this code to raise ZeroDivisionError. If it does not, that is a test failure."
- `assert isinstance(result, float)` → Check the type of the result, not just its value

**Step cards (pytest output on failure):**
1. `FAILED test_calculator.py::test_add_positive_numbers`
2. `AssertionError: assert 6 == 7`
3. `Where: result = 6`
4. pytest tells you exactly what the actual value was — no `print()` debugging needed

**Glossary terms:**
- `assert` → A Python keyword that raises an `AssertionError` if the condition is False. pytest uses assertions to detect test failures
- `pytest.raises()` → A context manager that asserts a specific exception is raised. Used to test error handling
- `assertion` → A claim about the state of your code. "After running X, the result should be Y."

---

### Screen 3: Fixtures — Shared Setup
**Concept:** `@pytest.fixture` provides shared setup data to multiple tests. `@pytest.mark.parametrize` runs one test with many inputs.
**Teaching arc:** Flow animation showing fixture extraction.

**Flow animation:**
Actors: Test A → Test B → Test C → Fixture
Steps:
1. `{"highlight":"flow-actor-1","label":"test_active_user: creates a sample user dict — 5 lines of setup"}`
2. `{"highlight":"flow-actor-2","label":"test_admin_user: creates the SAME sample user dict — 5 lines duplicated"}`
3. `{"highlight":"flow-actor-3","label":"test_can_view: creates the SAME sample user dict — 5 lines duplicated again"}`
4. `{"highlight":"flow-actor-4","label":"Extract to @pytest.fixture: write setup ONCE, all three tests receive it automatically"}`
5. `{"highlight":"flow-actor-4","label":"Now each test just declares the fixture as a parameter: def test_active_user(sample_user):"}`

**Translation block:**
```python
import pytest
from app import User, is_admin

@pytest.fixture
def sample_user():
    return User(name="Alice", role="admin", active=True)

def test_user_is_active(sample_user):
    assert sample_user.active is True

def test_admin_check(sample_user):
    assert is_admin(sample_user) is True

@pytest.mark.parametrize("a,b,expected", [
    (1, 2, 3),
    (0, 0, 0),
    (-1, 1, 0),
])
def test_add(a, b, expected):
    assert add(a, b) == expected
```
Plain English:
- `@pytest.fixture` → Marks a function as a fixture — pytest will call it and pass the return value to any test that lists it as a parameter
- `def test_user_is_active(sample_user):` → pytest sees `sample_user` in the signature and automatically runs the fixture to provide it
- `@pytest.mark.parametrize("a,b,expected", [...])` → Run this test multiple times with different inputs — no copy-pasting the same test
- The parametrize table `(1,2,3), (0,0,0), (-1,1,0)` runs the test 3 times, once per row

**Callout (callout-info):**
> Parametrize is how Claude writes efficient tests. Instead of `test_add_positives`, `test_add_zeros`, `test_add_negatives` — three separate functions — it writes one parametrized test. When you see that decorator, it means "this one function tests many cases."

**Glossary terms:**
- `fixture` → A function decorated with `@pytest.fixture` that provides data or state to tests. Runs before the test that requests it
- `@pytest.mark.parametrize` → Decorator that runs the same test function multiple times with different arguments
- `scope` → How long a fixture lives: "function" (default, once per test), "module" (once per file), "session" (once per test run)

---

### Screen 4: Mocking — Stub the World
**Concept:** Mocking replaces real external dependencies (APIs, databases, files) with fake versions during tests. Lets you test your code in isolation.
**Teaching arc:** Flow animation + group chat showing real vs mocked call.

**Group chat:** id="chat-mocking"
Actors: Your Code (actor-1, teal), Real API (actor-2, coral), Mock (actor-3, forest)

Messages:
1. Your Code → "I call `fetch_weather('Tokyo')` — this normally hits the real weather API."
2. Real API → "That would cost money, be slow, and fail if you are offline. Not good for automated tests."
3. Mock → "I intercept that call with `unittest.mock.patch`. Your code never knows the difference."
4. Your Code → "I called `fetch_weather('Tokyo')` — got a response."
5. Mock → "I returned `{'temp': 22, 'condition': 'sunny'}` — a fake response I control perfectly."
6. Your Code → "My logic processed it: formatted the display, returned a string."
7. Mock → "Your test can now verify how your code handles weather data — without touching the real API once."

**Translation block:**
```python
from unittest.mock import patch, MagicMock
import pytest
from weather_app import get_weather_summary

def test_weather_sunny():
    fake_response = {"temp": 22, "condition": "sunny"}

    with patch("weather_app.fetch_weather") as mock_fetch:
        mock_fetch.return_value = fake_response
        result = get_weather_summary("Tokyo")

    assert "sunny" in result
    mock_fetch.assert_called_once_with("Tokyo")
```
Plain English:
- `patch("weather_app.fetch_weather")` → Replace `fetch_weather` in the `weather_app` module with a fake for the duration of the `with` block
- `mock_fetch.return_value = fake_response` → When your code calls the fake, it returns this value
- `get_weather_summary("Tokyo")` → Your real function runs — but the API call is intercepted
- `mock_fetch.assert_called_once_with("Tokyo")` → Verify the function was called exactly once, with exactly this argument

**Callout (callout-warning):**
> A common trap: tests that pass but test nothing. `def test_something(): result = function(); assert result` — this just checks that `result` is truthy, not that it is correct. When reviewing Claude-generated tests, check that assertions are specific: `assert result == expected_value`, not just `assert result`.

**Glossary terms:**
- `mock` → A fake object that replaces a real one during testing. Returns controlled values so tests run in isolation
- `patch` → A function from `unittest.mock` that temporarily replaces an object with a mock during a test
- `assert_called_once_with()` → A mock method that verifies the mock was called exactly once with specific arguments
- `isolation` → Testing code without triggering its dependencies (database, API, filesystem). Mocks enable isolation

---

## Quiz (id="quiz-module6")

**Q1** (scenario, correct: option-c)
> Scenario: Claude wrote a function that sends a Stripe payment. You want to test that it handles declined cards correctly. How do you test this without charging a real card?

- option-a: Use a real Stripe test card number
- option-b: Skip the test — payment functions cannot be tested
- option-c: Mock the Stripe API call to return a "declined" response ✓
- option-d: Test manually by clicking through the UI

right: "Exactly! Mocking replaces the real Stripe call with a fake that you control. You can make the fake return 'declined' and verify your code handles it correctly — no real money involved."
wrong: "Mocking is exactly the right tool here. `patch('app.stripe.charge')` with a fake 'declined' response lets you test the error handling path deterministically."

**Q2** (correct: option-b)
> In a pytest fixture that uses `yield`, what separates setup from teardown?

- option-a: The `return` statement
- option-b: The `yield` statement ✓
- option-c: The end of the fixture function
- option-d: A `finally` block

right: "Correct! Everything before `yield` is setup (runs before the test). Everything after `yield` is teardown (runs after the test). The `yield` statement hands control to the test."
wrong: "In fixtures, `yield` is the boundary: setup is above it, teardown is below it. A `return` would exit the fixture with no teardown capability."

**Q3** (correct: option-a)
> You want to run `test_discount` with five different price inputs. What is the most efficient approach?

- option-a: `@pytest.mark.parametrize("price", [0, 10, 50, 99, 100])` on one test function ✓
- option-b: Write five separate test functions: `test_discount_zero`, `test_discount_ten`, etc.
- option-c: Loop inside the test: `for price in [0,10,50,99,100]: assert ...`
- option-d: Use a fixture that returns a list

right: "Right! `@pytest.mark.parametrize` runs the test once for each value. Each run is independent — if `price=50` fails, the others still run. You get 5 separate test results."
wrong: "Five separate functions works but is repetitive. A loop inside a test is worse — if one iteration fails, pytest reports it as a single failure with no detail about which value failed."

**Q4** (correct: option-b)
> You spot this test Claude generated: `def test_process(): result = process_data(sample); assert result`. What is wrong with it?

- option-a: Nothing — `assert result` is equivalent to `assert result is not None`
- option-b: The assertion only checks that `result` is truthy — it does not verify what `result` actually contains ✓
- option-c: The test should use `assertEqual` instead of `assert`
- option-d: The test needs a fixture

right: "Correct! `assert result` passes if result is any truthy value — a non-empty string, a non-zero number, a non-empty list. It does not verify that result is actually correct. A real assertion checks the specific expected value."
wrong: "`assert result` only checks truthiness — not correctness. Good tests assert specific values: `assert result['status'] == 'processed'`, not `assert result`."
