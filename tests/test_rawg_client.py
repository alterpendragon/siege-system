from unittest.mock import patch, Mock

import pytest

from siege.api.rawg_client import RawgClient

# Mock requests.get so tests don't hit the real RAWG API.

def test_search_game_success():
    client = RawgClient()
    with patch("siege.api.rawg_client.requests.get") as fake_get:
        fake_response = Mock()
        fake_response.status_code = 200
        fake_response.json.return_value = {"results": ["fake_game_data"]}
        fake_get.return_value = fake_response
        fake_ds = client.search_games("Dark Souls")
        assert fake_ds == ["fake_game_data"]

def test_search_game_empty_results():
    client = RawgClient()
    with patch("siege.api.rawg_client.requests.get") as fake_get:
        fake_response = Mock()
        fake_response.status_code = 200
        # No matches found, but request still succeeds.
        fake_response.json.return_value = {"results": []}
        fake_get.return_value = fake_response
        fake_ds = client.search_games("Dark Souls")
        assert fake_ds == []

def test_search_game_api_failure():
    client = RawgClient()
    with patch("siege.api.rawg_client.requests.get") as fake_get:
        fake_response = Mock()
        # Non-200 status (e.g. bad/missing API key) should yield None.
        fake_response.status_code = 403
        fake_get.return_value = fake_response
        fake_ds = client.search_games("Dark Souls")
        assert fake_ds is None
