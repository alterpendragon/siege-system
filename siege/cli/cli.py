"""Command-line interface for the Siege System game backlog tracker."""

from siege.database.db_manager import DatabaseClient
from siege.api.rawg_client import RawgClient
from siege.api.data_mapper import game_to_dictionary

def main():
    """Main function to run the CLI menu loop."""
    db = DatabaseClient()
    client = RawgClient()
    while True:
        print("\n--- [SIEGE SYSTEM] ---")
        print("1. View backlog")
        print("2. Filter backlog")
        print("3. Add new game")
        print("4. Delete game")
        print("5. Update status")
        print("6. Exit system")
        choice = input("Select option: ")
        print()
        if choice == '1':
            games = db.get_all_games()
            for game in games:
                print(f"{game[0]} | {game[1]} | {game[2]} |"
                      f" {game[3]} | {game[4]}")
        elif choice == '2':
            genre = input("Genre (leave blank to skip): ")
            status = input("Status (leave blank to skip): ")
            status = status.capitalize()
            filtered_games = db.filter_games(genre=genre, status=status)
            for game in filtered_games:
                print(f"{game[0]} | {game[1]} | {game[2]} |"
                      f" {game[3]} | {game[4]}")
        elif choice == '3':
            title = input("Game title: ")
            game_data = client.search_games(title)
            if game_data is None:
                print("Error fetching game data.")
            elif game_data == []:
                print("No results found.")
            else:
                for index, game in enumerate(game_data):
                    print(f"{index + 1}. {game['name']}")
                try:
                    selection = int(input("Select a game by number: ")) - 1
                    chosen_game = game_data[selection]
                    game_dict = game_to_dictionary(chosen_game)
                    success = db.add_game(
                        game_dict['title'], game_dict['genre'],
                        game_dict['platform']
                    )
                    if success:
                        print("Game added successfully.")
                    else:
                        print("Error adding game, try again.")
                except (ValueError, IndexError):
                    print("Invalid input.")
        elif choice == '4':
            try:
                game_id = int(input("Enter game ID to delete: "))
                success = db.delete_game(game_id)
                if success:
                    print("Game deleted successfully.")
                else:
                    print("Error deleting game, try again.")
            except ValueError:
                print("Invalid input.")
        elif choice == '5':
            try:
                game_id = int(input("Enter game ID to update: "))
                new_status = input("New status: ")
                new_status = new_status.capitalize()
                success = db.update_status(game_id, new_status)
                if success:
                    print("Status updated successfully.")
                else:
                    print("Error updating status, try again.")
            except ValueError:
                print("Invalid input.")
        elif choice == '6':
            print("Connection terminated.")
            break
        else:
            print("Invalid option, try again.")
