"""SQLite-backed client for managing the games backlog table."""

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
            completion_status TEXT CHECK(completion_status IN
                ('Backlog', 'Playing', 'Completed', 'Dropped'))
                NOT NULL DEFAULT 'Backlog',
            date_added DATETIME DEFAULT CURRENT_TIMESTAMP
        );
        ''')
        self.connection.commit()

    def add_game(self, title, genre=None, platform=None):
        """Adds a new game to the database.

        Args:
            title: The title of the game.
            genre: The genre of the game.
            platform: The platform of the game.

        Returns:
            True if the game was added successfully, False otherwise.
        """
        try:
            self.cursor.execute('''
            INSERT INTO games (title, genre, platform)
            VALUES (?, ?, ?);
            ''', (title, genre, platform))
            self.connection.commit()
            return True
        except sqlite3.IntegrityError:
            return False

    def get_all_games(self):
        """Retrieves all games from the database.

        Returns:
            A list of tuples, each representing a game record.
        """
        self.cursor.execute('SELECT * FROM games;')
        return self.cursor.fetchall()
    
    def update_status(self, game_id, new_status):
        """Updates the completion status of a game.

        Args:
            game_id: The ID of the game to update.
            new_status: The new completion status (e.g.,
                'Playing', 'Completed').

        Returns:
            True if the update succeeded, False otherwise.
        """
        try:
            self.cursor.execute('''
             UPDATE games
             SET completion_status = ?
             WHERE id = ?;
            ''', (new_status, game_id))
            self.connection.commit()
            return self.cursor.rowcount > 0
        except sqlite3.IntegrityError:
            return False

    def delete_game(self, game_id):
        """Deletes a game from the database.

        Args:
            game_id: The ID of the game to delete.

        Returns:
            True if the game was deleted successfully, False otherwise.
        """

        self.cursor.execute('''
         DELETE FROM games
         WHERE id = ?;
        ''', (game_id,))
        self.connection.commit()
        return self.cursor.rowcount > 0

    def filter_games(self, genre=None, status=None):
        """Filters games based on genre and/or completion status.

        Args:
            genre: The genre to filter by (optional).
            status: The completion status to filter by (optional).

        Returns:
            A list of tuples, each representing a matching game record.
        """
        query = 'SELECT * FROM games WHERE 1=1'
        params = []
        if genre:
            query += ' AND genre LIKE ?'
            params.append(f"%{genre}%")
        if status:
            query += ' AND completion_status = ?'
            params.append(status)
        self.cursor.execute(query, params)
        return self.cursor.fetchall()
    
    def close_connection(self):
        """Closes the database connection."""
        self.connection.close()
        