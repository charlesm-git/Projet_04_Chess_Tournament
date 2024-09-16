from Views.baseview import BaseView
from Controllers.reportcontroller import ReportController


class MenuController:
    def __init__(self,
                 view: BaseView,
                 base_controller,
                 report_controller: ReportController,
                 tournament_controller=None):
        self.view = view
        self.base_controller = base_controller
        self.report_controller = report_controller
        self.tournament_controller = tournament_controller

    def main_menu_action(self):
        user_input = self.view.get_main_menu(self.tournament_controller)
        match user_input:
            case '1':
                self.base_controller.add_player_to_database()
                return True
            case '2':
                self.base_controller.create_tournament()
                return True
            case '3':
                self.base_controller.load_tournament_from_database()
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
            self.tournament_controller.tournament_management()
        else:
            self.view.error_tournament_not_loaded()
