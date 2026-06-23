"""Maps raw RAWG API game data into the dictionary shape used by the CLI."""


def game_to_dictionary(game_data):
    """Converts a game object to a dictionary.

    Args:
        game_data: The game object to convert.

    Returns:
        A dictionary representation of the game object.
    """
    genre_list = [genre_item['name'] for genre_item in game_data.get('genres', [])]
    genre = ", ".join(genre_list)
    platform_list = [
        platform_item['platform']['name']
        for platform_item in game_data.get('platforms', [])
        ]
    platform = ", ".join(platform_list)
    return {
        'title': game_data['name'],
        'genre': genre,
        'platform': platform,
    }
