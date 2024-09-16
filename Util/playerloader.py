import json

from Models.player import Player


def load_players_from_database():
    """
    Load the players from the JSON database
    :return: a list containing all Player
    """
    with open('./data/players.json', 'r') as players_file:
        players_data = json.load(players_file)
        players = []
        for player_data in players_data:
            players.append(Player
                           .from_json_format(player_data))
        return players


def get_player_from_chess_id(chess_id, players):
    """
    Get the player in the database that has a certain chess_id
    :param chess_id: ID of the player researched
    :param players: list of players in the database
    :return: The player that has this chess_id in the database. None if no
    player is found.
    """
    for player in players:
        if player.player_chess_id == chess_id:
            return player
    return None
