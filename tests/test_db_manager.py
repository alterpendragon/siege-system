import pytest
import sqlite3
from siege.database.db_manager import DatabaseClient

@pytest.fixture
def db_client():
    return DatabaseClient(db_path=":memory:")

def test_add_game_success(db_client):
    assert db_client.add_game("Test Game", "Action", "PC")

# Title is a NOT NULL column, so add_game should
# reject and return falsy.
def test_add_game_fails_with_null_title(db_client):
    assert not db_client.add_game(None, "Action", "PC")

def test_get_all_games(db_client):
    db_client.add_game("Test Game 1", "Action", "PC")
    db_client.add_game("Test Game 2", "Adventure", "Console")
    games = db_client.get_all_games()
    assert len(games) == 2

def test_update_status_success(db_client):
    db_client.add_game("Test Game", "Action", "PC")
    game_id = db_client.get_all_games()[0][0]
    assert db_client.update_status(game_id, "Completed")

# "Finished" isn't an allowed status, so the update
# should be rejected.
def test_update_game_status_invalid_value(db_client):
    db_client.add_game("Test Game", "Action", "PC")
    game_id = db_client.get_all_games()[0][0]
    assert not db_client.update_status(game_id, "Finished")
    
def test_delete_game_success(db_client):
    db_client.add_game("Test Game", "Action", "PC")
    game_id =db_client.get_all_games()[0][0]
    assert db_client.delete_game(game_id)

# 999 is assumed to never collide with an autoincremented
# id from a fresh db.
def test_delete_game_nonexistent_id(db_client):
    db_client.add_game("Test Game", "Action", "PC")
    assert not db_client.delete_game(999)

def test_filter_games_by_genre(db_client):
    db_client.add_game("Test Game 1", "Action", "PC")
    db_client.add_game("Test Game 2", "Horror", "Console")
    filtered_games = db_client.filter_games(genre="Horror")
    assert len(filtered_games) == 1
    assert filtered_games[0][1] == "Test Game 2"

def test_filter_games_by_status(db_client):
    db_client.add_game("Test Game 1", "Action", "PC")
    db_client.add_game("Test Game 2", "Horror", "Console")
    game_id = db_client.get_all_games()[0][0]
    db_client.update_status(game_id, "Completed")
    filtered_games = db_client.filter_games(status="Completed")
    assert len(filtered_games) == 1

# sqlite3 raises ProgrammingError when using a cursor after
# its connection closed.
def test_close_connection(db_client):
    db_client.close_connection()
    with pytest.raises(sqlite3.ProgrammingError):
        db_client.cursor.execute("SELECT * FROM games;")
