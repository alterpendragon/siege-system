"""Pytest suite for RawgClient, with requests.get mocked out so
tests don't hit the real RAWG API."""

from unittest.mock import patch, Mock

import requests

from siege.api.rawg_client import RawgClient


def test_search_game_success():
    """A successful search returns the API's results list."""
    client = RawgClient()
    with patch("siege.api.rawg_client.requests.get") as fake_get:
        fake_response = Mock()
        fake_response.status_code = 200
        fake_response.json.return_value = {"results": ["fake_game_data"]}
        fake_get.return_value = fake_response
        fake_ds = client.search_games("Dark Souls")
        assert fake_ds == ["fake_game_data"]


def test_search_game_empty_results():
    """No matches found, but request still succeeds."""
    client = RawgClient()
    with patch("siege.api.rawg_client.requests.get") as fake_get:
        fake_response = Mock()
        fake_response.status_code = 200
        fake_response.json.return_value = {"results": []}
        fake_get.return_value = fake_response
        fake_ds = client.search_games("Dark Souls")
        assert fake_ds == []


def test_search_game_api_failure():
    """Non-200 status (e.g. bad/missing API key) should yield None."""
    client = RawgClient()
    with patch("siege.api.rawg_client.requests.get") as fake_get:
        fake_response = Mock()
        fake_response.status_code = 403
        fake_get.return_value = fake_response
        fake_ds = client.search_games("Dark Souls")
        assert fake_ds is None


def test_search_game_connection_error():
    """A connection failure should yield None instead of crashing."""
    client = RawgClient()
    with patch("siege.api.rawg_client.requests.get") as fake_get:
        fake_get.side_effect = requests.exceptions.ConnectionError("Connection error")
        fake_ds = client.search_games("Dark Souls")
        assert fake_ds is None


def test_search_game_timeout():
    """A request timeout is a RequestException and yields None."""
    client = RawgClient()
    with patch("siege.api.rawg_client.requests.get") as fake_get:
        fake_get.side_effect = requests.exceptions.Timeout("timed out")
        assert client.search_games("Dark Souls") is None


def test_search_game_invalid_json_returns_none():
    """requests.json() raises JSONDecodeError, a RequestException subclass.

    The client therefore returns None rather than propagating the error.
    """
    client = RawgClient()
    with patch("siege.api.rawg_client.requests.get") as fake_get:
        fake_response = Mock()
        fake_response.status_code = 200
        fake_response.json.side_effect = requests.exceptions.JSONDecodeError(
            "Expecting value", "doc", 0
        )
        fake_get.return_value = fake_response
        assert client.search_games("Dark Souls") is None

