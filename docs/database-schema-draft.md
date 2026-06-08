# Database Schema Draft - Siege System v1.0.0

## 1. Architectural Design Decisions

Before defining the schema, several deliberate architectural trade-offs were made to balance normalization with the lightweight requirements of the v1.0.0 release:

* **Single Table Core:** To maintain simplicity in this initial backend foundation, all game data will reside in a single `games` table.
* **Array Serialization (Many-to-Many Trade-off):** The RAWG API returns `genres` and `platforms` as arrays. While a fully normalized database would utilize separate tables and junction tables for these relationships, v1.0.0 will serialize these arrays into comma-separated strings (e.g., `"Action, RPG"`) at the Python application level before insertion.
* **Data Integrity Enforcement:** The `completion_status` requires strict control to prevent inconsistent data (e.g., "Finished" instead of "Completed"). Since SQLite lacks a native Boolean or Enum type, this is handled using a `TEXT` column combined with a `CHECK` constraint explicitly limiting allowed values.
* **Timestamping:** A `date_added` column leverages SQLite's `CURRENT_TIMESTAMP` to automatically track when items enter the backlog without requiring additional application logic.

## 2. SQL Schema Definition

The following SQL statement defines the exact structure of the `games` table:

```sql
CREATE TABLE games (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    title TEXT NOT NULL,
    genre TEXT,
    platform TEXT,
    completion_status TEXT CHECK(completion_status IN ('Backlog', 'Playing', 'Completed', 'Dropped')) NOT NULL DEFAULT 'Backlog',
    date_added DATETIME DEFAULT CURRENT_TIMESTAMP
);
