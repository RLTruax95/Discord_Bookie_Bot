import csv
import os

from match import Match
from player import Player

class Bet:
    def __init__(self, match: Match, parlay: Player, wager: int):
        self.match_name = match.match_name
        self.parlay = parlay.name
        self.wager = wager

    def save_to_csv(self, bet_list):
        """
        Saves the current bet instance to a CSV file.
        :param bet_list: The list to which the Match instance will be appended.
        """
        filename = 'bets.txt'
        file_exists = os.path.isfile(filename)

        #open the file and create a csv writer instance
        with open(filename, 'a', newline='') as file:
            writer = csv.writer(file)

            #Create the csv file if it doesn't exist
            if not file_exists:
                writer.writerow(['match_name', 'parlay', 'wager'])

            #write the player information to the csv file
            writer.writerow([self.match_name, self.parlay, self.wager])
            bet_list.append(self)

    @staticmethod
    def update_csv(bet_list):
        """
        Updates the CSV file with the current bets list.
        """
        filename = 'bets.txt'

        # open the csv file, clear the data, and rewrite the whole list to the file again
        with open(filename, 'w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(['match_name', 'parlay', 'wager'])
            for bet in bet_list:
                writer.writerow([bet.match_name, bet.parlay, bet.wager])

    @staticmethod
    def load_bets_from_csv(bet_list, match_list: list[Match], player_list: list[Player]):
        """
        Reads bet data from a CSV file and populates the bet_list.
        :param match_list: The list to store Match objects.
        :param player_list: The list of Player objects to reference.
        """
        filename = 'bets.txt'
        bet_list.clear()

        # clear the currently saved list and reload all the csv data
        try:
            # open the csv file and create a csv reader
            with open(filename, 'r') as file:
                reader = csv.DictReader(file)

                # assign the csv headers to the match instance variables
                for row in reader:
                    match_name = row['match_name']
                    parlay_name = row['parlay']
                    wager = row['wager']

                    for match in match_list:
                        if match.match_name == match_name:
                            temp_match: Match = match

                    # Find the Player objects from player_list
                    if parlay_name == temp_match.home_player or parlay_name == temp_match.away_player:
                        for player in player_list:
                            if player.name == parlay_name:
                                temp_parlay = player

                    # if both values exist, create a match instance with these values and add it to the list
                    if temp_match and temp_parlay:
                        bet = Bet(temp_match, temp_parlay, wager)
                        bet_list.append(bet)
                    else:
                        print(f"Warning: Could not find data for the bet")

        except FileNotFoundError:
            print(f"Error: The file '{filename}' was not found.")
        except KeyError as e:
            print(f"Error: Missing expected column in the CSV file: {e}")
        except Exception as e:
            print(f"An unexpected error occurred: {e}")