import json

from Models.player import Player
from Models.tournament import Tournament
from Controllers.menucontroller import MenuController
from Controllers.tournamentcontroller import TournamentController
from Controllers.reportcontroller import ReportController
from Util.utils import folder_creation
from Util.utils import tournament_name_formatting
from Util.utils import valid_chess_id_format
from Util.playerloader import load_players_from_database
from Util.playerloader import get_player_from_chess_id


class BaseController:
    def __init__(self, view):
        folder_creation()
        self.players = load_players_from_database()
        self.view = view
        self.tournament_controller = None
        self.report_controller = ReportController(self.view, self.players)
        self.menu_controller = MenuController(self.view, self,
                                              self.report_controller)

    def add_player_to_database(self):
        """ Add a player to the database """
        while True:
            if self.view.get_continue_adding_players():
                while True:
                    player_chess_id = self.view.get_player_chess_id()
                    if valid_chess_id_format(player_chess_id):
                        if (get_player_from_chess_id(player_chess_id,
                                                     self.players) is None):
                            data = {'player_chess_id': player_chess_id}
                            data.update(self.view.get_player_data())
                            player_to_add = Player.from_json_format(data)
                            self.players.append(player_to_add)
                            break
                        else:
                            self.view.error_player_already_in_database()
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
        tournament_list = self.report_controller.tournaments_list_report()
        while True:
            user_input = self.view.get_tournament_to_load()
            if user_input.isdigit():
                user_input = int(user_input)
                if user_input in range(1, len(tournament_list) + 1):
                    break
        self.update_controllers(tournament_list[user_input - 1])
        self.view.tournament_loaded_successfully(
            self.tournament_controller.tournament)

    def update_controllers(self, tournament):
        self.tournament_controller = TournamentController(tournament,
                                                          self.view,
                                                          self.players)
        self.report_controller = ReportController(self.view,
                                                  self.players,
                                                  self.tournament_controller)
        self.menu_controller = MenuController(self.view,
                                              self,
                                              self.report_controller,
                                              self.tournament_controller)
