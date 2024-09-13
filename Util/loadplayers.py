import json

from Models.player import Player


def load_players_from_database():
    """
    Load the players from the JSON database and return a list containing
    all Player
    """
    with open('./data/players.json', 'r') as players_file:
        players_data = json.load(players_file)
        players = []
        for player_data in players_data:
            players.append(Player
                           .from_player_database_json_format(player_data))
        return players
