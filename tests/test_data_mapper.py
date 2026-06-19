from siege.api.data_mapper import game_to_dictionary

def test_game_to_dictionary():
    # Raw shape matches the RAWG API response game_to_dictionary expects.
    sample_game = {
        "name": "Some Game",
        "genres": [{"name": "Action"}, {"name": "Adventure"}],
        "platforms": [
            {"platform": {"name": "PC"}},
            {"platform": {"name": "PlayStation 5"}}
        ]
    }
    result = game_to_dictionary(sample_game)
    # Genres and platforms are flattened into comma-joined strings.
    assert result['title'] == "Some Game"
    assert result['genre'] == "Action, Adventure"
    assert result['platform'] == "PC, PlayStation 5"
