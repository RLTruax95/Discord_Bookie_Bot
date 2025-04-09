import csv
import os

class Player:
    def __init__(self, name, faction, TV, coins):
        self.name = name
        self.faction = faction
        self.TV = TV
        self.coins = coins

    def save_to_csv(self, player_list):
        """
        Saves the current Player instance to a CSV file and appends it to the provided list.
        :param player_list: The list to which the Player instance will be appended.
        """
        filename = 'players.txt'
        file_exists = os.path.isfile(filename)

        with open(filename, 'a', newline='') as file:
            writer = csv.writer(file)

            # If the file doesn't exist, write the header
            if not file_exists:
                writer.writerow(['Name', 'Faction', 'TV', 'Coins'])

            # Write the player data
            writer.writerow([self.name, self.faction, self.TV, self.coins])
            player_list.append(self)  # Append the current Player instance to the list

    @staticmethod
    def load_players_from_csv(player_list):
        """
        Reads player data from a CSV file and stores it in the provided list as Player objects.
        :param player_list: The list to store Player objects in.
        """
        filename = 'players.txt'
        player_list.clear()  # Clear the list before loading new data

        try:
            with open(filename, 'r') as file:
                reader = csv.DictReader(file)  # Use DictReader to handle headers
                for row in reader:
                    # Create a Player object using data from the CSV row
                    player = Player(
                        name=row['Name'],
                        faction=row['Faction'],
                        TV=int(row['TV']),
                        coins=int(row['Coins'])
                    )
                    player_list.append(player)  # Add the player object to the list
        except FileNotFoundError:
            print(f"Error: The file '{filename}' was not found.")
        except KeyError as e:
            print(f"Error: Missing expected column in the CSV file: {e}")
        except Exception as e:
            print(f"An unexpected error occurred: {e}")
