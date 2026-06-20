# Siege System

A local, CLI-based video game backlog management tool and recommendation engine.

> **Note:** This project is currently under active development. v1.0.0 covers a CLI/SQLite backend; a web interface and AI-driven recommendations are planned for later versions (see [docs/roadmap.md](docs/roadmap.md)).

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
git clone <repo-url>
cd siege-system
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

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
└── docs/                       # Planning docs (requirements, roadmap, schema, conventions)
```

## Architecture

The codebase is split into three decoupled layers:

- **`database/`** — owns all SQLite interaction (schema creation, CRUD). Knows nothing about the CLI or the API.
- **`api/`** — `rawg_client.py` handles HTTP communication with RAWG; `data_mapper.py` separately converts RAWG's nested JSON response into the flat shape the app uses internally. Splitting these means the API client doesn't need to know the app's internal data shape, and the mapping logic can be unit-tested without making real HTTP requests.
- **`cli/`** — the only layer that talks to the user; it orchestrates calls into the database and API layers.

This separation keeps each layer independently testable and means a future web interface could reuse the `database` and `api` packages unchanged.

### Database schema

A single `games` table is used for v1.0.0. RAWG returns `genre` and `platform` as arrays, which are serialized into comma-separated strings (e.g. `"Action, RPG"`) before insertion, trading normalization for simplicity at this stage. `completion_status` is constrained at the database level via `CHECK(completion_status IN ('Backlog', 'Playing', 'Completed', 'Dropped'))`, since SQLite has no native enum type — this guarantees invalid statuses can never be written regardless of which caller writes to the table.

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

## Roadmap

- **v1.0.0** — CLI + SQLite backend foundation (current)
- **v2.0.0** — Flask web interface, Docker, CI/CD
- **v3.0.0** — Anthropic API recommendation engine, MCP server
- **v4.0.0** — TypeScript port and production hardening

Full details in [docs/roadmap.md](docs/roadmap.md).
