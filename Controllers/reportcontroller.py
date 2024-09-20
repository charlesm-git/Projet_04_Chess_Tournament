from prettytable import PrettyTable

from Views import baseview
from Models.round import Round
from Util.playerloader import get_player_from_chess_id
from Util.tournamentloader import load_tournament_from_database


class ReportController:

    def __init__(self, view: baseview, players, tournament_controller=None):
        self.tournament_controller = tournament_controller
        self.players = players
        self.view = view

    def players_list_report(self):
        """
        Prints, in a PrettyTable, the report containing all the players in the
        database
        """
        report = PrettyTable()
        report.title = 'Liste des joueurs présents dans la base de données'
        report.field_names = ['Nom', 'Prénom', 'Identifiant',
                              'Date de naissance']
        report.padding_width = 2
        for player in self.players:
            report.add_row([player.player_surname,
                           player.player_name,
                           player.player_chess_id,
                           player.player_date_of_birth])
        report.sortby = 'Nom'
        print()
        print(report)

    def tournaments_list_report(self):
        """
        Prints, in a PrettyTable, the report containing all the tournaments in
        the database
        """
        report = PrettyTable()
        report.title = 'Liste des tournois créés'
        report.field_names = ['Index', 'Nom', 'Date de début', 'Date de fin',
                              'nombre de round', 'Description',]
        report.padding_width = 2
        index = 1
        tournament_list = load_tournament_from_database()
        for tournament in tournament_list:
            report.add_row([index,
                            tournament.name,
                            tournament.start_date,
                            tournament.end_date,
                            tournament.NUMBER_OF_ROUNDS,
                            tournament.description])
            index += 1
        print()
        print(report)
        return tournament_list

    def tournaments_players_list_report(self):
        """
        Prints, in a PrettyTable, the report containing all the players in a
        tournament
        """
        if self.tournament_controller is not None:
            report = PrettyTable()
            report.title = ('Liste des joueurs dans le tournoi actuellement '
                            'sélectionné')
            report.field_names = ['Nom', 'Prénom', 'Identifiant',
                                  'Score actuel']
            report.padding_width = 2
            for tournament_player in (self.tournament_controller.tournament
                                      .tournament_players):
                player = get_player_from_chess_id(tournament_player
                                                  .player_chess_id,
                                                  self.players)
                report.add_row([player.player_surname,
                                player.player_name,
                                tournament_player.player_chess_id,
                                tournament_player.player_tournament_score])
            report.sortby = 'Nom'
            print()
            print(report)
        else:
            self.view.error_tournament_not_loaded()

    def tournament_rounds_and_matches_report(self):
        """
        Prints the report containing the rounds and matches (passed and/or
        current) in a tournament
        """
        if self.tournament_controller.tournament.current_round is None:
            print("\nLe tournoi n'a pas encore commencé, vous pouvez "
                  "encore ajouter des joueurs si vous le souhaitez")
        elif self.tournament_controller.tournament.current_round.end_date == 0:
            print(f'\nLe {self.tournament_controller.tournament.current_round
                  .name} est en cours :')
            self.round_results_report(self.tournament_controller.tournament
                                      .current_round)
        else:
            number_of_round_left = (self.tournament_controller.tournament
                                    .NUMBER_OF_ROUNDS
                                    - self.tournament_controller.tournament
                                    .current_round_number)
            print(f"\nLe "
                  f"{self.tournament_controller.tournament.current_round.name}"
                  f" est marqué comme terminé. Il reste "
                  f"{number_of_round_left} round(s) à jouer")
        if self.tournament_controller.tournament.rounds_results:
            print('\nLes résultats des rounds terminés sont :')
            for round in self.tournament_controller.tournament.rounds_results:
                self.round_results_report(round)
                print('\n')

    def tournament_results(self):
        """
        Prints, in a PrettyTable, the report containing the provisional results
        of the tournament
        """
        if self.tournament_controller is not None:
            report = PrettyTable()
            report.title = 'Résultats du tournoi sélectionné'
            report.field_names = ['Nom', 'Prénom', 'Identifiant',
                                  'Score actuel']
            report.padding_width = 2
            self.tournament_controller.order_tournament_players_by_score()
            for tournament_player in (self.tournament_controller.tournament
                                      .tournament_players):
                player = get_player_from_chess_id(tournament_player
                                                  .player_chess_id,
                                                  self.players)
                report.add_row([player.player_surname,
                                player.player_name,
                                tournament_player.player_chess_id,
                                tournament_player.player_tournament_score])
            report.sortby = 'Score actuel'
            report.reversesort = True
            print()
            print(report)
            if self.tournament_controller.tournament.current_round is None:
                print("Le tournoi n'a pas encore commencé, vous pouvez encore "
                      "ajouter des joueurs")
            elif (self.tournament_controller.tournament.current_round_number <
                  self.tournament_controller.tournament.NUMBER_OF_ROUNDS or
                  self.tournament_controller.tournament.current_round
                  .end_date == 0):
                print("\nAttention, le tournoi n'est pas encore terminé !")
        else:
            self.view.error_tournament_not_loaded()

    def round_results_report(self, round: Round):
        """
        Creates the report for on round.
        Called in tournament_rounds_and_matches_report()
        """
        round_report = PrettyTable()
        round_report.padding_width = 2
        round_report.title = f'{round.name}'
        round_report.field_names = ['Date de début', 'Date de fin']
        round_report.add_row([round.start_date, round.end_date])

        match_report = PrettyTable()
        match_report.padding_width = 2
        match_report.title = f'Liste des matchs du {round.name}'
        match_report.field_names = ['Match #', 'Joueur 1', 'Joueur 2', 'score']
        match_number = 1
        for match in round.matches:
            # Get the players from their chess_id
            player1 = get_player_from_chess_id(match.player1.player_chess_id,
                                               self.players)
            player2 = get_player_from_chess_id(match.player2.player_chess_id,
                                               self.players)
            match_report.add_row([match_number,
                                  f'{player1.player_name} '
                                  f'{player1.player_surname}',
                                  f'{player2.player_name} '
                                  f'{player2.player_surname}',
                                  f'{match.match_score_player1}-'
                                  f'{match.match_score_player2}'])
            match_number += 1
        print(round_report)
        print(match_report)
