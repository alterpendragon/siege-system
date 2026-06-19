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
        self.api_key = os.getenv('RAWG_API_KEY')
        self.base_url = 'https://api.rawg.io/api'
    
    def search_games(self, title):
        """Searches for games by title.

        Args:
            title: The title of the game to search for.

        Returns:
            A list of game results from the RAWG API, an empty list
            when no results are found, or None if the request fails.
        """
        url = self.base_url + "/games"
        params = {"key": self.api_key, "search": title, "page_size": 5}
        response = requests.get(url, params=params)
        if response.status_code == 200:
            data = response.json()
            return data['results']
        else:
            return None
    