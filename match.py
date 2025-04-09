from player import Player

class Match:
    def __init__(self, home_player: Player, away_player: Player):
        self.home_player = home_player
        self.away_player = away_player