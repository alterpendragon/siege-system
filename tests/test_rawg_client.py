"""Pytest suite for RawgClient, with requests.get mocked out so
tests don't hit the real RAWG API."""

from unittest.mock import patch, Mock

import pytest
import requests

from siege.api.rawg_client import RawgClient


@pytest.fixture
def client():
    """Provide a client with a deterministic test API key."""
    with patch("siege.api.rawg_client.load_dotenv"), \
         patch("siege.api.rawg_client.os.getenv", return_value="test-key"):
        return RawgClient()


def test_search_game_success(client):
    """A successful search returns the API's results list."""
    result = {"name": "Dark Souls", "id": 1}
    with patch("siege.api.rawg_client.requests.get") as fake_get:
        fake_response = Mock()
        fake_response.status_code = 200
        fake_response.json.return_value = {"results": [result]}
        fake_get.return_value = fake_response
        fake_ds = client.search_games("Dark Souls")
        assert fake_ds == [result]
        assert fake_ds[0] is result


def test_search_game_empty_results(client):
    """No matches found, but request still succeeds."""
    with patch("siege.api.rawg_client.requests.get") as fake_get:
        fake_response = Mock()
        fake_response.status_code = 200
        fake_response.json.return_value = {"results": []}
        fake_get.return_value = fake_response
        fake_ds = client.search_games("Dark Souls")
        assert fake_ds == []


def test_search_game_api_failure(client):
    """Non-200 status (e.g. bad/missing API key) should yield None."""
    with patch("siege.api.rawg_client.requests.get") as fake_get:
        fake_response = Mock()
        fake_response.status_code = 403
        fake_get.return_value = fake_response
        fake_ds = client.search_games("Dark Souls")
        assert fake_ds is None


def test_search_game_connection_error(client):
    """A connection failure should yield None instead of crashing."""
    with patch("siege.api.rawg_client.requests.get") as fake_get:
        fake_get.side_effect = requests.exceptions.ConnectionError("Connection error")
        fake_ds = client.search_games("Dark Souls")
        assert fake_ds is None


def test_search_game_timeout(client):
    """A request timeout is a RequestException and yields None."""
    with patch("siege.api.rawg_client.requests.get") as fake_get:
        fake_get.side_effect = requests.exceptions.Timeout("timed out")
        assert client.search_games("Dark Souls") is None


def test_search_game_invalid_json_returns_none(client):
    """requests.json() raises JSONDecodeError, a RequestException subclass.

    The client therefore returns None rather than propagating the error.
    """
    with patch("siege.api.rawg_client.requests.get") as fake_get:
        fake_response = Mock()
        fake_response.status_code = 200
        fake_response.json.side_effect = requests.exceptions.JSONDecodeError(
            "Expecting value", "doc", 0
        )
        fake_get.return_value = fake_response
        assert client.search_games("Dark Souls") is None


@pytest.mark.parametrize("api_key", [None, "", "   "])
def test_search_game_missing_api_key_does_not_request(api_key):
    """Missing or blank credentials fail without making an HTTP request."""
    with patch("siege.api.rawg_client.load_dotenv"), \
         patch("siege.api.rawg_client.os.getenv", return_value=api_key), \
         patch("siege.api.rawg_client.requests.get") as fake_get:
        client = RawgClient()
        assert client.search_games("Dark Souls") is None
        fake_get.assert_not_called()


def test_api_key_is_stripped():
    """Surrounding whitespace is removed from a configured API key."""
    with patch("siege.api.rawg_client.load_dotenv"), \
         patch(
             "siege.api.rawg_client.os.getenv",
             return_value="  test-key  ",
         ):
        client = RawgClient()
    assert client.api_key == "test-key"


@pytest.mark.parametrize(
    "payload",
    [
        None,
        [],
        {},
        {"results": None},
        {"results": {}},
        {"results": "not-a-list"},
    ],
)
def test_search_game_malformed_response_returns_none(client, payload):
    """A 200 response must contain a results list."""
    with patch("siege.api.rawg_client.requests.get") as fake_get:
        fake_response = Mock()
        fake_response.status_code = 200
        fake_response.json.return_value = payload
        fake_get.return_value = fake_response
        assert client.search_games("Dark Souls") is None


def test_search_game_filters_malformed_results(client):
    """Only named game dictionaries are returned, in their original order."""
    first = {"name": "First Game", "id": 1}
    second = {"name": "Second Game", "id": 2}
    results = [
        first,
        None,
        "not-a-game",
        {},
        {"name": ""},
        {"name": "   "},
        {"name": 123},
        second,
    ]
    with patch("siege.api.rawg_client.requests.get") as fake_get:
        fake_response = Mock()
        fake_response.status_code = 200
        fake_response.json.return_value = {"results": results}
        fake_get.return_value = fake_response
        returned = client.search_games("Game")

    assert returned == [first, second]
    assert returned[0] is first
    assert returned[1] is second


def test_search_game_all_malformed_results_returns_empty_list(client):
    """A valid results list with no usable games is a no-results response."""
    with patch("siege.api.rawg_client.requests.get") as fake_get:
        fake_response = Mock()
        fake_response.status_code = 200
        fake_response.json.return_value = {
            "results": [None, {}, {"name": ""}]
        }
        fake_get.return_value = fake_response
        assert client.search_games("Dark Souls") == []

