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
        if choice == '1':
            games = db.get_all_games()
            for game in games:
                print(f"{game[0]} | {game[1]} | {game[2]} | {game[3]} | {game[4]}")
        elif choice == '2':
            genre = input("Genre (leave blank to skip): ")
            status = input("Status (leave blank to skip): ")
            status = status.capitalize()
            filtered_games = db.filter_games(genre=genre, status=status)
            for game in filtered_games:
                print(f"{game[0]} | {game[1]} | {game[2]} | {game[3]} | {game[4]}")
        elif choice == '6':
            print("Connection terminated.")
            break
        