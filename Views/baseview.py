from Util.formatverification import valid_chess_id_format
from Util.formatverification import valid_date_format


class BaseView:

    def __init__(self):
        pass

    def get_tournament_data(self):
        print()
        print('Création d un nouveau tournoi')
        name = input('Entrer le nom du tournoi : ')
        location = input('Entrer la localisation du tournoi : ')
        description = input('Entrer, si besoin, une description '
                                       'pour le tournoi : ')
        while True:
            start_date = input('Entrer la date de début du tournoi '
                               '(format : YYYY-MM-DD) : ')
            if valid_date_format(start_date):
                break
        while True:
            end_date = input('Entrer la date de fin du tournoi '
                             '(format : YYYY-MM-DD) : ')
            if valid_date_format(end_date):
                break
        tournament_data = {'name': name,
                           'location': location,
                           'description': description,
                           'start_date': start_date,
                           'end_date': end_date}
        while True:
            number_of_rounds = input('Par défault, un tournoi compte 4 tours. '
                                     'Si c est le cas, laisser cette ligne '
                                     'vide. Sinon, entrer le nombre de tours '
                                     'souhaités : ')
            if number_of_rounds.isdigit():
                tournament_data['number_of_rounds'] = int(number_of_rounds)
                break
            elif number_of_rounds == '':
                break
            else:
                print('Entrer soit un nombre entier, soit laisser le champ '
                      'vide')
        return tournament_data

    def get_player_data(self):
        """ Get the data of a new player """
        while True:
            player_chess_id = input('Entrer l identifiant national du joueur '
                                    '(format : AB12345) : ')
            if valid_chess_id_format(player_chess_id) is True:
                break
        player_name = input('Entrer le prenom du joueur : ')
        player_surname = input('Entrer le nom de famille du joueur : ')
        while True:
            player_date_of_birth = input('Entrer la date de naissance du '
                                         'joueur (format : YYYY-MM-DD) : ')
            if valid_date_format(player_date_of_birth):
                break
        return {'player_chess_id': player_chess_id,
                'player_name': player_name,
                'player_surname': player_surname,
                'player_date_of_birth': player_date_of_birth}

    def get_continue_adding_players(self):
        while True:
            user_input = input('Ajouter un nouveau joueur ? Y/N : ')
            if user_input not in ['Y', 'N']:
                print('Erreur de saisie, entrer Y ou N')
            else:
                break
        if user_input == 'Y':
            return True
        return False

    def player_added_successfully(self):
        print('Le joueur a bien été ajouté à la base de données des joueurs')
        print()

    def get_players_chess_id(self):
        """ Ask the user to input the chess ID of a tournament participant """
        return input('Identifiant national du participant : ')

    def welcome_message_tournament_player_input(self):
        """
        Starting message shown to the user when entering tournament participant
        """
        print()
        print('Selection des joueurs présents dans le tournoi')
        print('Entrer, un par un, les identifiants nationals des joueurs '
              'participant au tournois')
        print('Une fois terminé, appuyer sur Entrer')
        print()

    def welcome_message_match_result(self):
        print()
        print('Renseignement des résultats du tour')
        print('Entrer 1 si le joueur 1 à gagné, 2 si le joueur 2 à gagné, '
              '0 s ils ont fait match nul : ')

    def error_match_result(self):
        print('Vous devez entrer 0, 1 ou 2 en fonction du résultat du match')

    def get_match_result(self, match):
        return input(f'Qui a gagné le match {match} ? ')

    def get_next_round_matches(self, tournament):
        print()
        print(f'Les matches pour le {tournament.current_round.name} sont : ')
        for match in tournament.current_round.matches:
            print(match)

    def get_tournament_to_load(self):
        print('Vous avez décidé de charger un tournoi depuis la base de '
              'données')
        name = input('Entrer le nom du tournoi : ')
        while True:
            start_date = input('Entrer la date de début du tournoi : ')
            if valid_date_format(start_date):
                break
        while True:
            end_date = input('Entrer la date de fin du tournoi : ')
            if valid_date_format(end_date):
                break
        return {'name': name,
                'start_date': start_date,
                'end_date': end_date}

    def get_main_menu(self):
        print()
        print('Que souhaitez-vous faire ?')
        print()
        print('1 - Ajouter des joueurs à la base de données')
        print('2 - Créer un nouveau tournoi')
        print('3 - Charger un tournoi déjà enregistré')
        print('4 - Ajouter des joueurs au tournoi selectionné')
        print('5 - Continuer le tournoi selectionné')
        print('9 - Quitter le programme')
        print()
        return input('Entrer le nombre correspondant : ')

    def get_continue_tournament(self, tournament):
        print()
        print(f'Vous êtes actuellement sur le tournoi : {tournament}')
        while True:
            user_input = input('Continuer ? Y/N : ')
            if user_input not in ['Y', 'N']:
                print('Erreur de saisie, entrer Y ou N')
            else:
                break
        if user_input == 'Y':
            return True
        return False

    def error_continue_tournament(self):
        print()
        print('Vous n avez selectionné aucun tournoi pour le moment. '
              'Veuillez créer ou charger un tournoi avant de réaliser cette '
              'action')

    def tournament_loaded_successfully(self, tournament):
        print()
        print(f'Le tournoi {tournament} a bien été chargé')

    def tournament_created_successfully(self, tournament):
        print()
        print(f'Le tournoi {tournament} a bien été créé')

    def tournament_finished(self, tournament):
        print('Le tournoi est terminé. Bravo à tous les participant !')
        print()
        print('Voici les résultats :')

    def player_ranking(self, player, ranking):
        print(f'{ranking} : {player}')

    def error_loading_tournament(self):
        print()
        print('Aucun tournoi avec ces données n est enregistré dans la base '
              'de données')
        print('Vérifier les données entrées ou créer un nouveau tournoi')

    def error_no_players_in_tournament(self):
        print()
        print('Le tournoi ne contient aucun joueur pour le moment. Veuillez '
              'en ajouter avant de continuer')