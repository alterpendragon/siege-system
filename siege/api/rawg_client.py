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