import json

from Models.player import Player
from Models.tournament import Tournament
from Controllers.tournamentcontroller import TournamentController
from Controllers.reportcontroller import ReportController
from Util.utils import folder_creation
from Util.utils import tournament_name_formatting
from Util.playerloader import load_players_from_database


class Controller:
    def __init__(self, view):
        folder_creation()
        self.players = load_players_from_database()
        self.view = view
        self.tournament_controller = None
        self.report_controller = ReportController(self.view, self.players)

    def add_player_to_database(self):
        """ Add a player to the database """
        while True:
            if self.view.get_continue_adding_players():
                data = self.view.get_player_data()
                player_to_add = Player.from_player_database_json_format(data)
                self.players.append(player_to_add)
                # Recreate the list of dictionaries necessary for the JSON
                # storage
                database_content = []
                for player in self.players:
                    database_content.append(player.save())
                with open('./data/players.json', 'w') as players_file:
                    json.dump(database_content, players_file, indent=4)
                self.view.player_added_successfully()
            else:
                break

    def create_tournament(self):
        """ Create a tournament according to the data provided by the user """
        tournament_data = self.view.get_tournament_data()
        formatted_name = tournament_name_formatting(tournament_data['name'])
        if 'number_of_rounds' in tournament_data:
            new_tournament = Tournament(formatted_name,
                                        tournament_data['location'],
                                        tournament_data['description'],
                                        tournament_data['start_date'],
                                        tournament_data['end_date'],
                                        tournament_data['number_of_rounds'])
        else:
            new_tournament = Tournament(formatted_name,
                                        tournament_data['location'],
                                        tournament_data['description'],
                                        tournament_data['start_date'],
                                        tournament_data['end_date'])
        self.update_controllers(new_tournament)
        self.tournament_controller.save_tournament()
        self.view.tournament_created_successfully(
            self.tournament_controller.tournament)

    def load_tournament_from_database(self):
        """
        Load a tournament from the JSON database and update the
        tournament_controller to manage the new tournament loaded
        """
        tournament_data = self.view.get_tournament_to_load()
        name = tournament_name_formatting(tournament_data['name'])
        start_date = tournament_data['start_date']
        end_date = tournament_data['end_date']
        try:
            with (open(f'./data/tournament/'
                       f'{start_date}_{end_date}_{name}.json', 'r')
                  as tournament_file):
                tournament_data = json.load(tournament_file)

            new_tournament = Tournament.from_json_format(tournament_data)
            self.update_controllers(new_tournament)
            self.view.tournament_loaded_successfully(
                self.tournament_controller.tournament)
        except FileNotFoundError:
            self.view.error_loading_tournament()

    def update_controllers(self, tournament):
        self.tournament_controller = TournamentController(tournament,
                                                          self.view,
                                                          self.players)
        self.report_controller = ReportController(self.view,
                                                  self.players,
                                                  self.tournament_controller)

    def main_menu_action(self):
        user_input = self.view.get_main_menu(self.tournament_controller)
        match user_input:
            case '1':
                self.add_player_to_database()
                return True
            case '2':
                self.create_tournament()
                return True
            case '3':
                self.load_tournament_from_database()
                return True
            case '4':
                self.handle_add_players_to_tournament()
                return True
            case '5':
                self.handle_continue_tournament()
                return True
            case '6':
                self.report_menu_action()
                return True
            case '9':
                return False
            case _:
                self.view.error_input()
                return True

    def report_menu_action(self):
        user_input = self.view.get_report_menu()
        match user_input:
            case '1':
                self.report_controller.players_list_report()
            case '2':
                self.report_controller.tournaments_list_report()
            case '3':
                self.report_controller.tournaments_players_list_report()
            case '4':
                self.report_controller.tournament_rounds_and_matches_report()
            case '5':
                self.report_controller.tournament_results()
            case '9':
                pass
            case _:
                self.view.error_input()

    def handle_add_players_to_tournament(self):
        if self.tournament_controller is not None:
            (self.tournament_controller
             .add_player_to_tournament())
        else:
            self.view.error_tournament_not_loaded()

    def handle_continue_tournament(self):
        if self.tournament_controller is not None:
            self.tournament_controller.continue_tournament()
        else:
            self.view.error_tournament_not_loaded()
