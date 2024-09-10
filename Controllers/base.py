import json

from Views.baseview import BaseView
from Models.player import Player
from Models.tournament import Tournament
from Util.formatverification import folder_creation
from Util.formatverification import tournament_name_formatting
from Controllers.tournamentcontroller import TournamentController
from Controllers.menucontroller import MenuController


def load_players_from_database():
    """
    Load the players from the JSON database and return a list containing
    all Player
    """
    with open('../data/players.json', 'r') as players_file:
        players_data = json.load(players_file)
        players = []
        for player_data in players_data:
            players.append(Player.from_player_database_json_format(player_data))
        return players


class Controller:

    def __init__(self, view):
        folder_creation()
        self.players = load_players_from_database()
        self.view = view
        self.menu_controller = MenuController(self.view)
        self.tournament_controller = None

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
                with open('../data/players.json', 'w') as players_file:
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
        self.tournament_controller = TournamentController(new_tournament,
                                                          self.view)
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
            with (open(f'../data/tournament/'
                       f'{start_date}_{end_date}_{name}.json', 'r')
                  as tournament_file):
                tournament_data = json.load(tournament_file)

            new_tournament = Tournament.from_json_format(tournament_data)
            self.tournament_controller = TournamentController(new_tournament,
                                                              self.view)
            self.view.tournament_loaded_successfully(
                self.tournament_controller.tournament)
        except FileNotFoundError:
            self.view.error_loading_tournament()

    def main_menu_action(self):
        user_input = self.menu_controller.main_menu()
        match user_input:
            case 1:
                self.add_player_to_database()
                return True
            case 2:
                self.create_tournament()
                return True
            case 3:
                self.load_tournament_from_database()
                return True
            case 4:
                if self.tournament_controller is not None:
                    (self.tournament_controller
                     .add_player_to_tournament(self.players))
                else:
                    self.view.error_continue_tournament()
                return True
            case 5:
                if self.tournament_controller is not None:
                    self.tournament_controller.continue_tournament()
                else:
                    self.view.error_continue_tournament()
                return True
            case 9:
                return False


if __name__ == "__main__":

    view = BaseView()
    controller = Controller(view)
    while controller.main_menu_action():
        pass
