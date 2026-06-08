# Siege System - v1.0.0 Requirements

## 1. Functional Requirements
* The system shall allow the user to add a new game to the backlog via the CLI.
* The system shall fetch game metadata from the RAWG API using a provided game title.
* The system shall store game metadata including title, genre, and platform in the SQLite database.
* The system shall allow the user to update the completion status of a game.
* The system shall allow the user to delete a game record from the database.
* The system shall display the list of all games stored in the database.
* The system shall allow the user to filter the backlog by genre or completion status.

## 2. Non-Functional Requirements

### Performance
* The system shall respond to CLI commands within 500ms, excluding network latency for API calls.

### Reliability
* The system shall handle API connection timeouts without crashing.
* The system shall validate all user inputs to prevent SQL injection vulnerabilities.

### Maintainability
* The system shall use modular code to decouple the database interface from the business logic.
* The system shall document all public functions using standard docstrings.
* The system shall maintain a minimum of 80% automated test coverage for all core business logic modules.

### Constraints
* The system shall use Python 3.10+ as the primary programming language.
* The system shall use SQLite as the exclusive database engine.
* The system shall persist the database file locally in the project directory.
* The system shall require a `.env` file for all external API credentials.
