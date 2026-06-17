import sqlite3

class DatabaseClient:
    """Manages all direct interaction with the SQLite database,
    including connection handling and table initialization."""

    def __init__(self, db_path="siege-backlog.db"):
        """Initializes the database connection and ensures the
        games table exists.

        Args:
            db_path: The file path to the SQLite database file.
        """
        self.db_path = db_path
        self.connection = sqlite3.connect(self.db_path)
        self.cursor = self.connection.cursor()
        self.create_table()
        
    def create_table(self):
        """Creates the games table if it does not already exist."""
        self.cursor.execute('''
         CREATE TABLE IF NOT EXISTS games (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            genre TEXT,
            platform TEXT,
            completion_status TEXT CHECK(completion_status IN ('Backlog', 'Playing', 'Completed', 'Dropped')) NOT NULL DEFAULT 'Backlog',
            date_added DATETIME DEFAULT CURRENT_TIMESTAMP
        );
        ''')
        self.connection.commit()
