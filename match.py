import csv
import os

from player import Player

class Match:
    def __init__(self, home_player: Player, away_player: Player):
        self.match_name = f'{home_player.name} vs {away_player.name}'
        self.home_player : Player = home_player
        self.away_player : Player = away_player

    def save_to_csv(self, match_list):
        """
        Saves the current Match instance to a CSV file.
        :param match_list: The list to which the Match instance will be appended.
        """
        filename = 'matches.txt'
        file_exists = os.path.isfile(filename)

        #open the file and create a csv writer instance
        with open(filename, 'a', newline='') as file:
            writer = csv.writer(file)

            #Create the csv file if it doesn't exist
            if not file_exists:
                writer.writerow(['home_player', 'away_player'])

            #write the player information to the csv file
            writer.writerow([self.home_player.name, self.away_player.name])
            match_list.append(self)

    @staticmethod
    def update_csv(match_list):
        """
        Updates the CSV file with the current match list.
        """
        filename = 'matches.txt'

        #open the csv file, clear the data, and rewrite the whole list to the file again
        with open(filename, 'w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(['home_player', 'away_player'])
            for match in match_list:
                writer.writerow([match.home_player.name, match.away_player.name])

    @staticmethod
    def load_matches_from_csv(match_list, player_list : list[Player]):
        """
        Reads match data from a CSV file and populates the match_list.
        :param match_list: The list to store Match objects.
        :param player_list: The list of Player objects to reference.
        """
        filename = 'matches.txt'
        match_list.clear()

        #clear the currently saved list and reload all the csv data
        try:
            #open the csv file and create a csv reader
            with open(filename, 'r') as file:
                reader = csv.DictReader(file)

                #assign the csv headers to the match instance variables
                for row in reader:
                    home_player_name = row['home_player']
                    away_player_name = row['away_player']

                    # Find the Player objects from player_list
                    for p in player_list:
                        if p.name == home_player_name:
                            temp_home_player = p
                        if p.name == away_player_name:
                            temp_away_player = p

                    #if both values exist, create a match instance with these values and add it to the list
                    if temp_home_player and temp_away_player:
                        match = Match(temp_home_player, temp_away_player)
                        match_list.append(match)
                    else:
                        print(f"Warning: Could not find players for match {home_player_name} vs {away_player_name}")

        except FileNotFoundError:
            print(f"Error: The file '{filename}' was not found.")
        except KeyError as e:
            print(f"Error: Missing expected column in the CSV file: {e}")
        except Exception as e:
            print(f"An unexpected error occurred: {e}")