"""Client for fetching game data from the RAWG Video Games Database API."""

import os

import requests
from dotenv import load_dotenv

class RawgClient:
    """Client for interacting with the RAWG Video Games Database API."""

    def __init__(self):
        """Initializes the RAWG client by loading the API
        key from environment variables."""
        load_dotenv()
        api_key = os.getenv('RAWG_API_KEY')
        self.api_key = api_key.strip() if isinstance(api_key, str) else None
        self.base_url = 'https://api.rawg.io/api'
    
    def search_games(self, title):
        """Searches for games by title.

        Args:
            title: The title of the game to search for.

        Returns:
            A list of game results from the RAWG API, an empty list
            when no results are found, or None if the request fails.
        """
        if not self.api_key:
            return None

        url = self.base_url + "/games"
        params = {"key": self.api_key, "search": title, "page_size": 5}
        try:
            response = requests.get(url, params=params, timeout=5)
        except requests.exceptions.RequestException:
            return None

        if response.status_code != 200:
            return None

        try:
            data = response.json()
        except ValueError:
            return None

        if not isinstance(data, dict):
            return None

        results = data.get('results')
        if not isinstance(results, list):
            return None

        return [
            game for game in results
            if (
                isinstance(game, dict)
                and isinstance(game.get('name'), str)
                and game['name'].strip()
            )
        ]
    