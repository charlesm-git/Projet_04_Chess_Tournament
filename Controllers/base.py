import json
import re
from pathlib import Path
from datetime import datetime
from collections import UserList

from Views.baseview import BaseView
from Models.player import Player
from Models.tournament import Tournament
from Models.tournamentplayer import TournamentPlayer
from Models.match import Match
from Models.round import Round
from Util.formatverification import valid_chess_id_format


def tournament_date():
    timestamp = datetime.now().strftime("%Y-%m-%d")
    return timestamp


def round_date():
    timestamp = datetime.now().strftime("%Y-%m-%d-T%H:%M:%S")
    return timestamp


def folder_creation():
    """ Creates the data's storing folders if they don't already exist """
    tournament_directory = Path('../data/tournament/')
    player_database = Path('../data/players.json')
    if not tournament_directory.exists():
        tournament_directory.mkdir(parents=True)
        player_database.touch()


def load_players_from_database():
    """
    Load the players from the JSON database and return a list containing
    all Player
    """
    with open('../data/players.json', 'r') as players_file:
        players_data = json.load(players_file)
        players = []
        for player_data in players_data:
            players.append(Player.from_json_format(player_data))
        return players


class Controller:

    def __init__(self, view):
        folder_creation()
        self.players = load_players_from_database()
        self.view = view

    def add_player_to_database(self):
        """ Add a player to the database"""
        data = self.view.get_player_data()
        player_to_add = Player.from_json_format(data)
        self.players.append(player_to_add)
        database_content = []
        for player in self.players:
            database_content.append(player.player_json_data())
        with open('../data/players.json', 'w') as players_file:
            json.dump(database_content, players_file, indent=4)

    def create_tournament_players_list(self):
        """ Create the list of players for one tournament """
        view.tournament_player_message()
        tournament_players = []
        while True:
            tournament_player_chess_id = view.get_tournament_players()
            # Execution if the user has given a chess ID
            if tournament_player_chess_id is not None:
                # Verify if the chess ID given has the right format
                if (valid_chess_id_format(tournament_player_chess_id)
                        is not None):
                    player_found = False
                    # Go thought de list of all the players
                    for player in self.players:
                        # If the player is found in the database, a tournament
                        # player is created and the tournament players list
                        # is appended
                        if (player.player_chess_id ==
                                tournament_player_chess_id):
                            tournament_player = (
                                TournamentPlayer(player.player_chess_id,
                                                 player.player_name,
                                                 player.player_surname,
                                                 player.player_date_of_birth)
                            )
                            tournament_players.append(tournament_player)
                            player_found = True
                            break
                    # If the player is not found in the database, a
                    # notification is sent to the user
                    if not player_found:
                        print('Le joueur n est pas enregistré dans la base de '
                              'donnees. Veuillez l enregistrer avant de '
                              'l ajouter à un tournois')
                # If the chess ID given doesn't have the right format, a
                # notification is sent to the user
                else:
                    print('L identifiant n est pas au bon format (AB12345), '
                          'Veuillez réessayer')
            else:
                break
        return tournament_players

    def order_tournament_players(self):
        """
        Order the players of a tournament according to their ranking
        """
        pass

    def create_tournament(self):
        """ Create a tournament """
        pass

    def create_round(self, tournament: Tournament):
        """ Create a round of a tournament """
        pass

    def round_association(self):
        """ Realize the match association of a specific round """
        pass

    def match_winner(self):
        pass


if __name__ == "__main__":
    # pattern = r'^[A-Z]{2}\d{5}$'
    # result = re.match(pattern, 'DA12456')
    # print(result)

    view = BaseView()
    controller = Controller(view)
    # controller.add_player_to_database()
    tournament_list = controller.create_tournament_players_list()
    for player in tournament_list:
        print(player)
    # player_id = 'FT45675'
    # for player in controller.players:
    #     if player.player_chess_id == player_id:
    #         print(player.player_name, player.player_surname)
    #         break
