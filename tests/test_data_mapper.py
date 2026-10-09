"""Pytest suite for game_to_dictionary data mapper."""

import pytest

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


def test_game_to_dictionary_null_genres():
    """A null genres value maps to an empty string."""
    sample_game = {
        "name": "Some Game",
        "genres": None,
        "platforms": [{"platform": {"name": "PC"}}],
    }
    result = game_to_dictionary(sample_game)
    assert result['title'] == "Some Game"
    assert result['genre'] == ""
    assert result['platform'] == "PC"


def test_game_to_dictionary_skips_incomplete_platform():
    """Malformed platform entries are omitted."""
    sample_game = {
        "name": "Some Game",
        "genres": [{"name": "Action"}],
        "platforms": [{}],
    }
    result = game_to_dictionary(sample_game)
    assert result['title'] == "Some Game"
    assert result['genre'] == "Action"
    assert result['platform'] == ""


def test_game_to_dictionary_skips_malformed_metadata_entries():
    """Valid metadata is retained in order while malformed entries are skipped."""
    sample_game = {
        "name": "Some Game",
        "genres": [
            {"name": "  Action  "},
            None,
            {},
            {"name": ""},
            {"name": 123},
            {"name": "Adventure"},
        ],
        "platforms": [
            {"platform": {"name": "  PC  "}},
            None,
            {},
            {"platform": None},
            {"platform": {}},
            {"platform": {"name": ""}},
            {"platform": {"name": 123}},
            {"platform": {"name": "PlayStation 5"}},
        ],
    }
    result = game_to_dictionary(sample_game)
    assert result['genre'] == "Action, Adventure"
    assert result['platform'] == "PC, PlayStation 5"


@pytest.mark.parametrize("genres", ["Action", {}, 123])
def test_game_to_dictionary_non_list_genres(genres):
    """Non-list genre values map to an empty string."""
    result = game_to_dictionary({
        "name": "Some Game",
        "genres": genres,
        "platforms": [],
    })
    assert result['genre'] == ""


@pytest.mark.parametrize("platforms", ["PC", {}, 123, None])
def test_game_to_dictionary_non_list_platforms(platforms):
    """Non-list platform values map to an empty string."""
    result = game_to_dictionary({
        "name": "Some Game",
        "genres": [],
        "platforms": platforms,
    })
    assert result['platform'] == ""


def test_game_to_dictionary_missing_title_raises():
    """Title remains required and is accessed directly."""
    with pytest.raises(KeyError):
        game_to_dictionary({"genres": [], "platforms": []})
