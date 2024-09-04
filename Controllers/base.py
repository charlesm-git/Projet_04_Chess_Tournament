import json
from pathlib import Path

from Views.baseview import BaseView
from Models.player import Player
from Models.tournament import Tournament
from Models.tournamentplayer import TournamentPlayer
from Models.match import Match
from Models.round import Round
from Util.formatverification import valid_chess_id_format
from Util.formatverification import round_date


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
        """ Add a player to the database """
        data = self.view.get_player_data()
        player_to_add = Player.from_json_format(data)
        self.players.append(player_to_add)
        database_content = []
        # Recreate the list of dictionaries necessary for the JSON storage
        for player in self.players:
            database_content.append(player.save())
        with open('../data/players.json', 'w') as players_file:
            json.dump(database_content, players_file, indent=4)

    def add_player_to_tournament(self, tournament: Tournament):
        """ Create the list of players for one tournament """
        view.welcome_message_tournament_player_input()
        while True:
            tournament_player_chess_id = view.get_players_chess_id()
            # Execution if the user has given a chess ID
            if tournament_player_chess_id != '':
                # Verify if the chess ID given has the right format
                # if it's not, valid_chess_id_format notify the user
                if valid_chess_id_format(tournament_player_chess_id):
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
                            (tournament.tournament_players
                             .append(tournament_player))
                            player_found = True
                            break
                    # If the player is not found in the database, a
                    # notification is sent to the user
                    if not player_found:
                        print('Le joueur n est pas enregistré dans la base de '
                              'donnees. Veuillez l enregistrer avant de '
                              'l ajouter à un tournoi')
            else:
                break

    def create_tournament(self):
        """ Create a tournament according to the data provided by the user """
        tournament_data = self.view.get_tournament_data()
        if 'number_of_rounds' in tournament_data:
            new_tournament = Tournament(tournament_data['name'],
                                        tournament_data['location'],
                                        tournament_data['description'],
                                        tournament_data['start_date'],
                                        tournament_data['end_date'],
                                        tournament_data['number_of_rounds'])
        else:
            new_tournament = Tournament(tournament_data['name'],
                                        tournament_data['location'],
                                        tournament_data['description'],
                                        tournament_data['start_date'],
                                        tournament_data['end_date'],)
        return new_tournament

    def create_round(self, tournament: Tournament):
        """ Create a round of a tournament """
        tournament.current_round_number += 1
        if tournament.current_round_number <= tournament.NUMBER_OF_ROUNDS:
            new_round = Round(tournament)
            new_round.matches = self.round_association(tournament)
            tournament.current_round = new_round

    def round_association(self, tournament: Tournament):
        """
        Realize the match association of a specific round
        :return a list of matches for this round
        """
        match_list = []
        # Sort the list of players in the tournament according to their
        # current score
        self.order_tournament_players(tournament)
        players = tournament.tournament_players
        i = 0
        # Create the matches associations
        while i < len(players):
            new_match = Match(players[i], players[i+1])
            match_list.append(new_match)
            i += 2
        return match_list

    def order_tournament_players(self, tournament: Tournament):
        """
        Order the players of a tournament according to their ranking
        """
        (tournament.tournament_players
         .sort(key=lambda tournament_player: tournament_player.score))

    def round_result(self, tournament: Tournament):
        """
        Update the tournament rounds_results with the results of the last round
        """
        self.view.welcome_message_match_result()
        # Set the time of the end of the round
        tournament.current_round.end_date = round_date()
        round_result = []
        # For every match, the user is asked for the winner
        for match in tournament.current_round.matches:
            match = self.match_winner_update(match)
            round_result.append(match)
        tournament.current_round.matches = round_result
        tournament.rounds_results.append(tournament.current_round)

    def match_winner_update(self, match: Match):
        """
        Update a match according to the result given by the user
        Used in round_result
        :return the match result in a tuple format
        """
        result = self.view.get_match_result(match)
        match int(result):
            case 1:
                match.match_score_player1 = 1
                match.player1.score += 1
            case 2:
                match.match_score_player2 = 1
                match.player2.score += 1
            case 0:
                match.match_score_player1 = 0.5
                match.player1.score += 0.5
                match.match_score_player2 = 0.5
                match.player2.score += 0.5
        return match.result()


if __name__ == "__main__":

    view = BaseView()
    controller = Controller(view)
    # controller.add_player_to_database()
    tournament = Tournament('WC', 'Paris', '',
                            '2024-12-12', '2024-12-12')
    controller.add_player_to_tournament(tournament)
    controller.create_round(tournament)
    print(tournament.current_round)
    controller.round_result(tournament)
    print(tournament.rounds_results)
    # controller.create_round(tournament)
    # print(tournament.current_round)
    # controller.round_result(tournament)
    # print(tournament.rounds_results)
