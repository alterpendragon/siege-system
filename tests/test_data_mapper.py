"""Pytest suite for game_to_dictionary data mapper."""

from siege.api.data_mapper import game_to_dictionary


def test_game_to_dictionary():
    """Raw shape matches the RAWG API response game_to_dictionary expects.

    Genres and platforms are flattened into comma-joined strings.
    """
    sample_game = {
        "name": "Some Game",
        "genres": [{"name": "Action"}, {"name": "Adventure"}],
        "platforms": [
            {"platform": {"name": "PC"}},
            {"platform": {"name": "PlayStation 5"}}
        ]
    }
    result = game_to_dictionary(sample_game)
    """ Genres and platforms are flattened into comma-joined strings. """
    assert result['title'] == "Some Game"
    assert result['genre'] == "Action, Adventure"
    assert result['platform'] == "PC, PlayStation 5"


def test_game_to_dictionary_missing_genres():
    """RAWG doesn't guarantee the genres key is populated.

    Missing genres should fall back to an empty string instead
    of raising a KeyError.
    """
    sample_game = {
        "name": "Some Game",
        "platforms": [{"platform": {"name": "PC"}}]
    }
    result = game_to_dictionary(sample_game)
    assert result['title'] == "Some Game"
    assert result['genre'] == ""
    assert result['platform'] == "PC"


def test_game_to_dictionary_missing_platforms():
    """RAWG doesn't guarantee the platforms key is populated.

    Missing platforms should fall back to an empty string instead
    of raising a KeyError.
    """
    sample_game = {
        "name": "Some Game",
        "genres": [{"name": "Action"}]
    }
    result = game_to_dictionary(sample_game)
    assert result['title'] == "Some Game"
    assert result['genre'] == "Action"
    assert result['platform'] == ""
