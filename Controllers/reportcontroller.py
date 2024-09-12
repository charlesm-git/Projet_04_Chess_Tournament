import json
from pathlib import Path
from prettytable import prettytable

from Views import baseview
from Models.tournament import Tournament
from Models.round import Round
from Util.loadplayers import load_players_from_database


class ReportController:

    def __init__(self, view: baseview, tournament_controller=None):
        self.tournament_controller = tournament_controller
        self.players = None
        self.view = view

    def update_players(self):
        self.players = load_players_from_database()

    def players_list_report(self):
        self.update_players()
        report = prettytable.PrettyTable()
        report.title = 'Liste des joueurs présents 7dans la base de données'
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
        report = prettytable.PrettyTable()
        report.title = 'Liste des tournois créés'
        report.field_names = ['Nom', 'Date de début', 'Date de fin',
                              'nombre de round', 'Description',]
        report.padding_width = 2
        folder_path = Path('../data/tournament/')
        for file in folder_path.iterdir():
            if file.is_file():
                with (open(file, 'r') as file_content):
                    tournament_data = json.load(file_content)
                    tournament = Tournament.from_json_format(tournament_data)
                    report.add_row([tournament.name,
                                    tournament.start_date,
                                    tournament.end_date,
                                    tournament.NUMBER_OF_ROUNDS,
                                    tournament.description])
        print()
        print(report)

    def tournaments_players_list_report(self):
        if self.tournament_controller is not None:
            report = prettytable.PrettyTable()
            report.title = ('Liste des joueurs dans le tournoi actuellement '
                            'sélectionné')
            report.field_names = ['Nom', 'Prénom', 'Identifiant',
                                 'Score actuel']
            report.padding_width = 2
            for player in self.tournament_controller.tournament.tournament_players:
                report.add_row([player.player_surname,
                               player.player_name,
                               player.player_chess_id,
                               player.score])
            report.sortby = 'Nom'
            print()
            print(report)
        else:
            self.view.error_tournament_not_loaded()

    def tournament_rounds_and_matches_report(self):
        if self.tournament_controller.tournament.current_round is None:
            print("\nLe tournoi n'a pas encore commencé, vous pouvez "
                  "encore ajouter des joueurs si vous le souhaitez")
        elif self.tournament_controller.tournament.current_round.end_date == 0:
            self.round_results_report(self.tournament_controller.tournament
                                      .current_round)
        else:
            number_of_round_left = (self.tournament_controller.tournament
                                    .NUMBER_OF_ROUNDS
                                    - self.tournament_controller.tournament
                                    .current_round_number)
            print(f'\nLe {self.tournament_controller.tournament.current_round
                  .name} est marqué commé terminé. Il reste '
                  f'{number_of_round_left} round(s) à jouer')
        if self.tournament_controller.tournament.rounds_results:
            print(f'\nLes résultats des rounds terminés sont :')
            for round in self.tournament_controller.tournament.rounds_results:
                self.round_results_report(round)
                print('\n')

    def tournament_results(self):
        if self.tournament_controller is not None:
            report = prettytable.PrettyTable()
            report.title = ('Résultats du tournoi sélectionné')
            report.field_names = ['Rang', 'Nom', 'Prénom', 'Identifiant',
                                 'Score actuel']
            report.padding_width = 2
            rank = 1
            for player in (self.tournament_controller.tournament
                           .tournament_players):
                report.add_row([rank,
                               player.player_surname,
                               player.player_name,
                               player.player_chess_id,
                               player.score])
                rank += 1
            report.sortby = 'Score actuel'
            report.reversesort = True
            print()
            print(report)
            if self.tournament_controller.tournament.current_round is None:
                print("Le tournoi n'a pas encore commencé, vous pouvez encore "
                      "ajouter des joueurs")
            elif (self.tournament_controller.tournament.current_round_number <=
                  self.tournament_controller.tournament.NUMBER_OF_ROUNDS or
                  self.tournament_controller.tournament.current_round
                  .end_date == 0):
                print("Attention, le tournoi n'est pas encore terminé !")
        else:
            self.view.error_tournament_not_loaded()

    def round_results_report(self, round: Round):
        round_report = prettytable.PrettyTable()
        round_report.padding_width = 2
        round_report.title = f'{round.name}'
        round_report.field_names = ['Date de début', 'Date de fin']
        round_report.add_row([round.start_date, round.end_date])

        match_report = prettytable.PrettyTable()
        match_report.padding_width = 2
        match_report.title = f'Liste des matchs du {round.name}'
        match_report.field_names = ['Match #', 'Joueur 1', 'Joueur 2', 'score']
        match_number = 1
        for match in round.matches:
            match_report.add_row([match_number,
                                  f'{match.player1.player_name} '
                                  f'{match.player1.player_surname}',
                                  f'{match.player2.player_name} '
                                  f'{match.player2.player_surname}',
                                  f'{match.match_score_player1}-'
                                  f'{match.match_score_player2}'])
            match_number += 1
        print(round_report)
        print(match_report)
