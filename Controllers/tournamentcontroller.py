import json

from Models.tournament import Tournament
from Models.tournamentplayer import TournamentPlayer
from Models.round import Round
from Models.match import Match
from Views.baseview import BaseView
from Util.utils import get_round_date
from Util.utils import valid_chess_id_format
from Util.playerloader import get_player_from_chess_id


class TournamentController:

    def __init__(self, tournament: Tournament, view: BaseView, players):
        self.tournament = tournament
        self.players = players
        self.view = view

    def continue_tournament(self):
        if self.tournament.tournament_players:
            while (self.tournament.current_round_number
                   < self.tournament.NUMBER_OF_ROUNDS or
                   self.tournament.current_round.end_date == 0):
                if self.view.get_continue_tournament(self.tournament):
                    if (self.tournament.current_round is None
                            or self.tournament.current_round.end_date != 0):
                        self.create_round()
                    self.view.get_next_round_matches(self.tournament,
                                                     self.players)
                    if self.view.get_continue_tournament(self.tournament):
                        self.round_result()
                    else:
                        break
                else:
                    break
        else:
            self.view.error_no_players_in_tournament()
        if (self.tournament.current_round_number ==
                self.tournament.NUMBER_OF_ROUNDS and
                self.tournament.current_round.end_date != 0):
            self.view.tournament_finished(self.tournament)
            self.tournament_result()

    def tournament_result(self):
        self.order_tournament_players_by_score()
        player_ranking = self.tournament.tournament_players[::-1]
        rank = 1
        for player in player_ranking:
            self.view.player_ranking(player, rank)
            rank += 1

    def add_player_to_tournament(self):
        """ Create the list of players for one tournament """
        if self.tournament.current_round is None:
            self.view.welcome_message_tournament_player_input()
            while True:
                tournament_player_chess_id = self.view.get_players_chess_id()
                # Execution if the user has given a chess ID
                if tournament_player_chess_id != '':
                    # Verify if the chess ID given has the right format
                    # if it's not, valid_chess_id_format notify the user
                    if valid_chess_id_format(tournament_player_chess_id):
                        player_found = False
                        # Go thought de list of all the players
                        player = get_player_from_chess_id(
                            tournament_player_chess_id, self.players)
                        if player is not None:
                            tournament_player = (
                                TournamentPlayer(tournament_player_chess_id))
                            (self.tournament.tournament_players
                             .append(tournament_player))
                            player_found = True
                            self.save_tournament()
                        # If the player is not found in the database, a
                        # notification is sent to the user
                        if not player_found:
                            print('Le joueur n est pas enregistré dans la '
                                  'base de donnees. Veuillez l enregistrer '
                                  'avant de l ajouter à un tournoi')
                else:
                    break
        else:
            print()
            print('Le tournoi a déjà commencé, vous ne pouvez plus ajouter de '
                  'joueurs')

    def create_round(self):
        """ Create a round of a tournament """
        if self.tournament.tournament_players:
            self.tournament.current_round_number += 1
            new_round = Round.new_round_tournament(self.tournament)
            new_round.matches = self.round_association()
            self.tournament.current_round = new_round
            self.save_tournament()
        else:
            print('Le tournoi ne comporte aucun joueur pour le moment. '
                  'Veuillez ajouter des joueurs avant de lancer le tournoi')

    def round_association(self):
        """
        Realize the match association of a specific round
        :return a list of matches for this round
        """
        match_list = []
        # Sort the list of players in the tournament according to their
        # current score
        self.order_tournament_players_by_score()
        players = self.tournament.tournament_players
        i = 0
        # Create the matches associations
        while i < len(players):
            new_match = Match(players[i], players[i + 1])
            match_list.append(new_match)
            i += 2
        return match_list

    def order_tournament_players_by_score(self):
        """
        Order the players of a tournament according to their ranking
        """
        (self.tournament.tournament_players
         .sort(key=lambda tournament_player: tournament_player
               .player_tournament_score))

    def round_result(self):
        """
        Update the tournament rounds_results with the results of the last round
        """
        self.view.welcome_message_match_result()
        round_result = []
        # For every match, the user is asked for the winner
        for match in self.tournament.current_round.matches:
            match_result = self.match_winner_update(match)
            round_result.append(match_result)
        # Change the list of matches of that round from the list of matches to
        # the list of the matches results
        self.tournament.current_round.matches = round_result
        self.tournament.rounds_results.append(self.tournament.current_round)
        # Set the time of the end of the round
        self.tournament.current_round.end_date = get_round_date()
        self.save_tournament()

    def match_winner_update(self, match):
        """
        Update a match according to the result given by the user
        Used in round_result
        :return the match result in a tuple format
        """
        while True:
            result = self.view.get_match_result(match, self.players)
            if result in ['0', '1', '2']:
                break
            else:
                self.view.error_input()
        match result:
            case '1':
                match.match_score_player1 = 1
                match.player1.player_tournament_score += 1
            case '2':
                match.match_score_player2 = 1
                match.player2.player_tournament_score += 1
            case '0':
                match.match_score_player1 = 0.5
                match.player1.player_tournament_score += 0.5
                match.match_score_player2 = 0.5
                match.player2.player_tournament_score += 0.5
        return match

    def save_tournament(self):
        with open(f'./data/tournament/'
                  f'{self.tournament.start_date}_{self.tournament.end_date}_'
                  f'{self.tournament.name}.json', 'w') as tournament_file:
            json.dump(self.tournament.save(), tournament_file, indent=4)
