import json
import random

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

    def tournament_management(self):
        """ Manage the tournament flow """
        if (self.tournament.tournament_players and
                len(self.tournament.tournament_players) % 2 == 0):
            # Loops until the last round is finished
            while (self.tournament.current_round_number
                   < self.tournament.NUMBER_OF_ROUNDS or
                   self.tournament.current_round.end_date == 0):
                if self.view.get_continue_tournament(self.tournament):
                    # If the current round if finished or non existent, create
                    # a new round
                    if (self.tournament.current_round is None
                            or self.tournament.current_round.end_date != 0):
                        self.create_round()
                    # Shows the matches for the next round
                    self.view.get_next_round_matches(self.tournament,
                                                     self.players)
                    # Get the results of all the matches
                    if self.view.get_continue_tournament(self.tournament):
                        self.round_result()
                    else:
                        break
                else:
                    break
        elif (self.tournament.tournament_players and
                len(self.tournament.tournament_players) % 2 != 0):
            self.view.error_odd_number_of_players_in_tournament()
        else:
            self.view.error_no_players_in_tournament()
        # When the tournament is finished, shows the results
        if (self.tournament.current_round_number ==
                self.tournament.NUMBER_OF_ROUNDS and
                self.tournament.current_round.end_date != 0):
            self.view.tournament_finished()
            self.tournament_result()

    def tournament_result(self):
        """ Shows the results once the tournament is finished """
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
                tournament_player_chess_id = self.view.get_player_chess_id()
                if tournament_player_chess_id != '':
                    # Verify if the chess ID given has the right format
                    # If it doesn't, valid_chess_id_format notify the user
                    if valid_chess_id_format(tournament_player_chess_id):
                        player_found = False
                        # Check if this chess_id is in the players database and
                        # not already added to the tournament
                        player_in_database = get_player_from_chess_id(
                            tournament_player_chess_id, self.players)
                        player_in_tournament = get_player_from_chess_id(
                            tournament_player_chess_id,
                            self.tournament.tournament_players)
                        if (player_in_database is not None and
                                player_in_tournament is None):
                            # Creates the tournament player, appends the list
                            # and saves the tournament
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
                                  'base de donnees ou a déjà été ajouté au '
                                  'tournoi. Verifiez votre saisie')
                else:
                    break
        else:
            print()
            print('Le tournoi a déjà commencé, vous ne pouvez plus ajouter de '
                  'joueurs')

    def create_round(self):
        """ Create a round of a tournament """
        self.tournament.current_round_number += 1
        self.tournament.current_round = Round.new_round_tournament(self
                                                                   .tournament)
        self.round_association()
        self.save_tournament()

    def round_association(self):
        """
        Realize the match association of a specific round
        :return a list of matches for this round
        """
        if self.tournament.current_round_number == 1:
            self.random_pair()
        else:
            self.pair_by_score()

    def random_pair(self):
        """ Randomly associate the players on the first round """
        random_players = self.tournament.tournament_players
        random.shuffle(random_players)
        for i in range(0, len(random_players), 2):
            new_match = Match(random_players[i], random_players[i + 1])
            self.tournament.current_round.matches.append(new_match)

    def pair_by_score(self):
        """
        Associate the players according to their score.
        The program tries to avoid associating players that have already played
        together as much as possible.
        """
        self.order_tournament_players_by_score()
        # Creation of a dictionary that group the players according to their
        # score. The key is the score, the value is a list of all the player
        # that have this score
        grouped_players = {}
        for player in self.tournament.tournament_players:
            score = player.player_tournament_score
            if score not in grouped_players:
                grouped_players[score] = []
            grouped_players[score].append(player)

        # List of players that couldn't be matched on the previous loop
        unmatched_players = []
        # Goes through all the score groups
        for score_group_players in grouped_players.values():
            random.shuffle(score_group_players)
            # Add the unmatched players to the current score group and reset
            # the unmatched_players list
            if unmatched_players:
                score_group_players = unmatched_players + score_group_players
                unmatched_players = []
            while len(score_group_players) > 1:
                # Tries to associate the first player of the list with the
                # players of its group. If it's not possible, the player is
                # added to the unmatched_players
                player1 = score_group_players.pop(0)
                match_found = False
                for i, player2 in enumerate(score_group_players):
                    if not self.have_played_together(player1, player2):
                        self.tournament.current_round.matches.append(
                            Match(player1, player2))
                        score_group_players.pop(i)
                        match_found = True
                        break
                if not match_found:
                    unmatched_players.append(player1)
            # In case of an odd number of players in the score group, the last
            # one is added to the unmatched_players to be associated in the
            # next score group
            unmatched_players += score_group_players

        # All the remaining players are sorted according to their score
        unmatched_players.sort(key=lambda tournament_player: tournament_player
                               .player_tournament_score)
        # The remaining players have already played together. Thus, they are
        # associated according to their score
        while unmatched_players:
            player1 = unmatched_players.pop(0)
            player2 = unmatched_players.pop(0)
            self.tournament.current_round.matches.append(
                Match(player1, player2))

    def have_played_together(self, player1, player2):
        """
        Checks if two players have already played together by going through the
        matches list of the previous rounds
        """
        for round in self.tournament.rounds_results:
            for match in round.matches:
                if ((player1.player_chess_id
                     == match.player1.player_chess_id and
                     player2.player_chess_id
                     == match.player2.player_chess_id) or
                        (player1.player_chess_id
                         == match.player2.player_chess_id and
                         player2.player_chess_id
                         == match.player1.player_chess_id)):
                    return True
        return False

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
        # For every match, the user is asked for the winner, the score of the
        # match is updated accordingly
        for match in self.tournament.current_round.matches:
            match_result = self.match_winner_update(match)
            round_result.append(match_result)
        # Updates the matches list
        self.tournament.current_round.matches = round_result
        # Set the time of the end of the round
        self.tournament.current_round.end_date = get_round_date()
        self.tournament.rounds_results.append(self.tournament.current_round)
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
        winning_point = 1
        draw_point = 0.5
        match result:
            case '1':
                match.match_score_player1 = winning_point
                match.player1.player_tournament_score += winning_point
            case '2':
                match.match_score_player2 = winning_point
                match.player2.player_tournament_score += winning_point
            case '0':
                match.match_score_player1 = draw_point
                match.player1.player_tournament_score += draw_point
                match.match_score_player2 = draw_point
                match.player2.player_tournament_score += draw_point
        return match

    def save_tournament(self):
        """ Save the tournament data in the database """
        with open(f'./data/tournament/'
                  f'{self.tournament.start_date}_{self.tournament.end_date}_'
                  f'{self.tournament.name}.json', 'w') as tournament_file:
            json.dump(self.tournament.save(), tournament_file, indent=4)
