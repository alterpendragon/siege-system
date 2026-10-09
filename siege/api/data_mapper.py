"""Maps raw RAWG API game data into the dictionary shape used by the CLI."""


def game_to_dictionary(game_data):
    """Converts a game object to a dictionary.

    Args:
        game_data: The game object to convert.

    Returns:
        A dictionary representation of the game object.
    """
    genres = game_data.get('genres', [])
    if not isinstance(genres, list):
        genres = []
    genre_list = []
    for genre_item in genres:
        if not isinstance(genre_item, dict):
            continue
        name = genre_item.get('name')
        if isinstance(name, str) and name.strip():
            genre_list.append(name.strip())

    platforms = game_data.get('platforms', [])
    if not isinstance(platforms, list):
        platforms = []
    platform_list = []
    for platform_item in platforms:
        if not isinstance(platform_item, dict):
            continue
        platform_data = platform_item.get('platform')
        if not isinstance(platform_data, dict):
            continue
        name = platform_data.get('name')
        if isinstance(name, str) and name.strip():
            platform_list.append(name.strip())

    return {
        'title': game_data['name'],
        'genre': ", ".join(genre_list),
        'platform': ", ".join(platform_list),
    }
