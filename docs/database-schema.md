# Database Schema - Siege System

## 1. Architectural Design Decisions

The schema reflects deliberate architectural trade-offs that balance normalization with the project's lightweight, local-only design:

* **Single Table Core:** To maintain simplicity, all game data resides in a single `games` table.
* **Array Serialization (Many-to-Many Trade-off):** The RAWG API returns `genres` and `platforms` as arrays. While a fully normalized database would utilize separate tables and junction tables for these relationships, these arrays are serialized into comma-separated strings (e.g., `"Action, RPG"`) at the Python application level before insertion.
* **Data Integrity Enforcement:** The `completion_status` requires strict control to prevent inconsistent data (e.g., "Finished" instead of "Completed"). Since SQLite lacks a native Boolean or Enum type, this is handled using a `TEXT` column combined with a `CHECK` constraint explicitly limiting allowed values. `GAME_STATUSES` in `siege/constants.py` is the application source of truth and is used to construct the CHECK constraint shown below.
* **Timestamping:** A `date_added` column leverages SQLite's `CURRENT_TIMESTAMP` to automatically track when items enter the backlog without requiring additional application logic.

## 2. SQL Schema Definition

The following SQL statement defines the exact structure of the `games` table:

```sql
CREATE TABLE IF NOT EXISTS games (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    title TEXT NOT NULL,
    genre TEXT,
    platform TEXT,
    completion_status TEXT CHECK(completion_status IN ('Backlog', 'Playing', 'Completed', 'Dropped')) NOT NULL DEFAULT 'Backlog',
    date_added DATETIME DEFAULT CURRENT_TIMESTAMP
);
```
