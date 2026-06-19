from unittest.mock import MagicMock, patch

import pytest

from siege.cli.cli import main


@pytest.fixture
def mock_dependencies():
    """Fixture to patch DatabaseClient and RawgClient for each test.

    Yields:
        A tuple containing the mocked database instance and the mocked
        API client instance.
    """
    with patch("siege.cli.cli.DatabaseClient") as mock_db, \
         patch("siege.cli.cli.RawgClient") as mock_rawg:
        yield mock_db.return_value, mock_rawg.return_value


def test_cli_option_1_view_backlog(mock_dependencies, capsys):
    """Test option 1: View backlog with mock games data.

    The test simulates the user inputting '1' to view the backlog list
    and then '6' to terminate the main menu loop.

    Args:
        mock_dependencies: The mocked database and API clients.
        capsys: Pytest fixture to capture stdout and stderr.
    """
    db, _ = mock_dependencies
    db.get_all_games.return_value = [
        (1, "Rainbow Six Siege", "FPS", "PC", "Backlog")
    ]

    with patch("builtins.input", side_effect=["1", "6"]):
        main()

    captured = capsys.readouterr()
    assert "1 | Rainbow Six Siege | FPS | PC | Backlog" in captured.out
    assert "Connection terminated." in captured.out


def test_cli_option_2_filter_backlog(mock_dependencies, capsys):
    """Test option 2: Filter backlog by genre and status.

    The test simulates selecting option '2', filtering by 'RPG' and
    'playing', and verifies that the database method receives the
    capitalized status 'Playing' before exiting with '6'.

    Args:
        mock_dependencies: The mocked database and API clients.
        capsys: Pytest fixture to capture stdout and stderr.
    """
    db, _ = mock_dependencies
    db.filter_games.return_value = [
        (2, "The Witcher 3", "RPG", "PC", "Playing")
    ]

    with patch("builtins.input", side_effect=["2", "RPG", "playing", "6"]):
        main()

    captured = capsys.readouterr()
    db.filter_games.assert_called_with(genre="RPG", status="Playing")
    assert "2 | The Witcher 3 | RPG | PC | Playing" in captured.out


@patch("siege.cli.cli.game_to_dictionary")
def test_cli_option_3_add_game_success(
    mock_mapper, mock_dependencies, capsys
):
    """Test option 3: Successfully search and add a new game.

    The test simulates searching for a game, displaying the API
    results, selecting the first result, mapping it to a dictionary,
    and confirming the successful database insertion.

    Args:
        mock_mapper: The mocked data mapper function.
        mock_dependencies: The mocked database and API clients.
        capsys: Pytest fixture to capture stdout and stderr.
    """
    db, client = mock_dependencies

    client.search_games.return_value = [{"name": "Elden Ring"}]
    mock_mapper.return_value = {
        "title": "Elden Ring",
        "genre": "RPG",
        "platform": "PC",
    }
    db.add_game.return_value = True

    with patch("builtins.input", side_effect=["3", "Elden", "1", "6"]):
        main()

    captured = capsys.readouterr()
    assert "1. Elden Ring" in captured.out
    assert "Game added successfully." in captured.out


def test_cli_option_3_add_game_no_results(mock_dependencies, capsys):
    """Test option 3: API returns empty list when no game is found.

    The test ensures that the application prints a specific message
    when the RAWG API client returns an empty list for a query.

    Args:
        mock_dependencies: The mocked database and API clients.
        capsys: Pytest fixture to capture stdout and stderr.
    """
    _, client = mock_dependencies
    client.search_games.return_value = []

    with patch("builtins.input", side_effect=["3", "UnknownGame", "6"]):
        main()

    captured = capsys.readouterr()
    assert "No results found." in captured.out


def test_cli_option_3_add_game_api_error(mock_dependencies, capsys):
    """Test option 3: API returns None due to an error.

    The test ensures that the application gracefully handles a None
    return value from the API client by displaying an error message.

    Args:
        mock_dependencies: The mocked database and API clients.
        capsys: Pytest fixture to capture stdout and stderr.
    """
    _, client = mock_dependencies
    client.search_games.return_value = None

    with patch("builtins.input", side_effect=["3", "Elden", "6"]):
        main()

    captured = capsys.readouterr()
    assert "Error fetching game data." in captured.out


def test_cli_option_3_add_game_db_failure(
    mock_dependencies, capsys
):
    """Test option 3: Database fails to save the game.

    The test ensures that when the database client returns False during
    an addition, the proper error message is shown to the user.

    Args:
        mock_dependencies: The mocked database and API clients.
        capsys: Pytest fixture to capture stdout and stderr.
    """
    db, client = mock_dependencies
    client.search_games.return_value = [{"name": "Elden Ring"}]
    db.add_game.return_value = False

    with patch("builtins.input", side_effect=["3", "Elden", "1", "6"]):
        with patch("siege.cli.cli.game_to_dictionary") as mock_mapper:
            mock_mapper.return_value = {
                "title": "Elden Ring",
                "genre": "RPG",
                "platform": "PC",
            }
            main()

    captured = capsys.readouterr()
    assert "Error adding game, try again." in captured.out


def test_cli_option_3_add_game_index_error(mock_dependencies, capsys):
    """Test option 3: User selects an invalid game number.

    The test simulates an IndexError when the user inputs a numeric
    selection that is out of bounds for the returned games list.

    Args:
        mock_dependencies: The mocked database and API clients.
        capsys: Pytest fixture to capture stdout and stderr.
    """
    _, client = mock_dependencies
    client.search_games.return_value = [{"name": "Elden Ring"}]

    with patch("builtins.input", side_effect=["3", "Elden", "99", "6"]):
        main()

    captured = capsys.readouterr()
    assert "Invalid input." in captured.out


def test_cli_option_4_delete_game_success(mock_dependencies, capsys):
    """Test option 4: Successfully delete a game by its ID.

    The test verifies that the database delete method is triggered
    with the correct integer conversion of the user input.

    Args:
        mock_dependencies: The mocked database and API clients.
        capsys: Pytest fixture to capture stdout and stderr.
    """
    db, _ = mock_dependencies
    db.delete_game.return_value = True

    with patch("builtins.input", side_effect=["4", "15", "6"]):
        main()

    captured = capsys.readouterr()
    db.delete_game.assert_called_with(15)
    assert "Game deleted successfully." in captured.out


def test_cli_option_4_delete_game_failure(mock_dependencies, capsys):
    """Test option 4: Database fails to delete the game.

    The test ensures that the user is notified with an error message
    if the database client fails to delete the record.

    Args:
        mock_dependencies: The mocked database and API clients.
        capsys: Pytest fixture to capture stdout and stderr.
    """
    db, _ = mock_dependencies
    db.delete_game.return_value = False

    with patch("builtins.input", side_effect=["4", "15", "6"]):
        main()

    captured = capsys.readouterr()
    assert "Error deleting game, try again." in captured.out


def test_cli_option_4_delete_game_invalid_input(mock_dependencies, capsys):
    """Test option 4: Enter a non-numeric string to trigger ValueError.

    The test verifies that entering an invalid string instead of a game ID
    is caught by the exception block and does not call the database.

    Args:
        mock_dependencies: The mocked database and API clients.
        capsys: Pytest fixture to capture stdout and stderr.
    """
    db, _ = mock_dependencies

    with patch("builtins.input", side_effect=["4", "abc", "6"]):
        main()

    captured = capsys.readouterr()
    assert "Invalid input." in captured.out
    db.delete_game.assert_not_called()


def test_cli_option_5_update_status_success(mock_dependencies, capsys):
    """Test option 5: Successfully update a game status.

    The test verifies that the update method receives the correct ID
    and the capitalized string representation of the new status.

    Args:
        mock_dependencies: The mocked database and API clients.
        capsys: Pytest fixture to capture stdout and stderr.
    """
    db, _ = mock_dependencies
    db.update_status.return_value = True

    with patch(
        "builtins.input", side_effect=["5", "10", "completed", "6"]
    ):
        main()

    captured = capsys.readouterr()
    db.update_status.assert_called_with(10, "Completed")
    assert "Status updated successfully." in captured.out


def test_cli_option_5_update_status_failure(mock_dependencies, capsys):
    """Test option 5: Database fails to update the game status.

    The test ensures that an error message is printed if the database
    update operation returns False.

    Args:
        mock_dependencies: The mocked database and API clients.
        capsys: Pytest fixture to capture stdout and stderr.
    """
    db, _ = mock_dependencies
    db.update_status.return_value = False

    with patch(
        "builtins.input", side_effect=["5", "10", "playing", "6"]
    ):
        main()

    captured = capsys.readouterr()
    assert "Error updating status, try again." in captured.out
