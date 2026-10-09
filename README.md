# Siege System

A local, CLI-based video game backlog management tool.

This is a complete, self-contained project — scope was intentionally limited to a local CLI/SQLite backend.

## Overview

Gamers often suffer from "backlog paralysis": hundreds of unplayed games scattered across Steam, Epic, PlayStation, and other storefronts, with no unified, store-agnostic way to track ownership, completion status, and decide what to play next.

Siege System solves this locally. Search for a game by title, pull accurate metadata (genre, platform) from the [RAWG Video Games Database](https://rawg.io/apidocs) API, and store it in a local SQLite database. From there you can list your backlog, filter by genre or status, update a game's status as you play through it, or remove it entirely — all from a simple terminal menu, no account or server required.

## Features

- Search and add games via the RAWG API
- View the full backlog
- Filter games by genre and/or completion status
- Update a game's completion status (`Backlog`, `Playing`, `Completed`, `Dropped`)
- Delete games from the backlog
- Local-only persistence via SQLite — no network dependency beyond the initial RAWG lookup

## Requirements

- Python 3.10+
- A free [RAWG API key](https://rawg.io/apidocs)

## Installation

```bash
git clone https://github.com/alterpendragon/siege-system.git
cd siege-system
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```
> **Note:** these commands are written for macOS/Linux. On Windows, use `python` instead of `python3`, and activate the virtual environment with `.venv\Scripts\activate` (Command Prompt) or `.venv\Scripts\Activate.ps1` (PowerShell) instead of `source .venv/bin/activate`.

Create a `.env` file in the project root with your RAWG API key:

```
RAWG_API_KEY=your_api_key_here
```

## Usage

Run the CLI from the project root:

```bash
python main.py
```

You'll be presented with a menu:

```
--- [SIEGE SYSTEM] ---
1. View backlog
2. Filter backlog
3. Add new game
4. Delete game
5. Update status
6. Exit system
```

Select an option by number and follow the prompts. Adding a game searches RAWG by title, lists matching results, and lets you pick the correct one to import.

## Running Tests

```bash
pytest
```

`pytest` also prints a terminal coverage report for the `siege` package (`--cov=siege --cov-report=term-missing` is set in `pytest.ini`). To write an HTML report as well:

```bash
pytest --cov-report=html
```

The test suite (`tests/`) covers the CLI flow, the RAWG client (with HTTP calls mocked), the API-to-dictionary data mapper, and the database layer.

## Project Structure

```
.
├── main.py                     # Entry point — launches the CLI
├── siege/
│   ├── api/
│   │   ├── rawg_client.py      # RawgClient: wraps RAWG API requests
│   │   └── data_mapper.py      # Maps raw RAWG JSON into the app's game dict shape
│   ├── cli/
│   │   └── cli.py              # Interactive menu loop and user-facing logic
│   └── database/
│       └── db_manager.py       # DatabaseClient: SQLite connection and CRUD
├── tests/                      # PyTest suite
├── requirements.txt
└── docs/                       # Planning docs (requirements, schema, conventions)
```

## Architecture

The codebase is split into three decoupled layers:

- **`database/`** — owns all SQLite interaction (schema creation, CRUD). Knows nothing about the CLI or the API.
- **`api/`** — `rawg_client.py` handles HTTP communication with RAWG; `data_mapper.py` separately converts RAWG's nested JSON response into the flat shape the app uses internally. Splitting these means the API client doesn't need to know the app's internal data shape, and the mapping logic can be unit-tested without making real HTTP requests.
- **`cli/`** — the only layer that talks to the user; it orchestrates calls into the database and API layers.

The layers were kept decoupled by design — a discipline that would have made a future web interface straightforward, had the project continued past v1.0.0.

### Database schema

A single `games` table is used. RAWG returns `genre` and `platform` as arrays, which are serialized into comma-separated strings (e.g. `"Action, RPG"`) before insertion, trading normalization for simplicity. `completion_status` is constrained at the database level via `CHECK(completion_status IN ('Backlog', 'Playing', 'Completed', 'Dropped'))`, since SQLite has no native enum type — this guarantees invalid statuses can never be written regardless of which caller writes to the table.

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

See [docs/database-schema-draft.md](docs/database-schema-draft.md) for the full rationale.