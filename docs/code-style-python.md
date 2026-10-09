# Python Code Style Conventions - Siege System

These conventions are followed through code review. The project does not use
an automated linter or formatter.

## 1. Naming Conventions
Following PEP 8 standards:
* **Variables & Functions:** `snake_case` (e.g., `user_input`, `fetch_game_data`).
* **Classes:** `PascalCase` (e.g., `GameManager`, `DatabaseClient`).
* **Constants:** `UPPER_CASE_WITH_UNDERSCORES` (e.g., `API_BASE_URL`).

## 2. Import Ordering
Imports must be grouped in the following order, with a blank line between each group:
1. Standard library imports (e.g., `os`, `sys`, `sqlite3`).
2. Related third-party imports (e.g., `requests`, `pytest`).
3. Local application/library specific imports.

## 3. Docstring Format
Public modules, classes, and functions should include a concise docstring.
Use Google-style `Args:` and `Returns:` sections when they add useful
information; simple functions do not need empty sections.

* Use triple double quotes (`"""`).
* Explain the purpose of the code and any non-obvious arguments or return values.

**Example:**
```python
def fetch_game_data(title):
    """Fetches game metadata from the RAWG API.

    Args:
        title: The name of the game to search for.

    Returns:
        A dictionary containing the game's title, genre, and platform.
    """
```
## 4. Maximum Line Length
* Aim for **79 characters** where practical. Longer lines are acceptable when
  splitting them would reduce readability, such as URLs or clear expressions.
