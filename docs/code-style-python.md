# Python Code Style Rules - Siege System

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
All public modules, classes, and functions must include a docstring. We follow the Google Style format:
* Use triple double quotes (`"""`).
* Explain the purpose of the code, arguments (`Args:`), and return values (`Returns:`).

**Example:**
```python
def fetch_game_data(title: str) -> dict:
    """Fetches game metadata from the RAWG API.

    Args:
        title: The name of the game to search for.

    Returns:
        A dictionary containing the game's title, genre, and platform.
    """
```
## 4. Maximum Line Length
* Limit all lines to a maximum of **79 characters**. This ensures readability and consistency across different editors and screen sizes.
