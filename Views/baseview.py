from Util.formatverification import valid_chess_id_format
from Util.formatverification import valid_date_format


class BaseView:

    def __init__(self):
        pass

    def get_tournament_data(self):
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
        number_of_rounds = input('Par défault, un tournoi compte 4 tours. '
                                 'Si c est le cas, laisser cette ligne vide. '
                                 'Sinon, entrer le nombre de tours '
                                 'souhaités : ')
        if number_of_rounds != '':
            tournament_data['number_of_rounds'] = number_of_rounds
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

    def get_players_chess_id(self):
        """ Ask the user to input the chess ID of a tournament participant """
        return input('Identifiant national du participant : ')

    def welcome_message_tournament_player_input(self):
        """
        Starting message shown to the user when entering tournament participant
        """
        print('Selection des joueurs présents dans le tournoi')
        print('Entrer, un par un, les identifiants nationals des joueurs '
              'participant au tournois')
        print('Une fois terminé, appuyer sur Entrer')

    def welcome_message_match_result(self):
        print('Renseignement des résultats du tour')
        print('Entrer 1 si le joueur 1 à gagné, 2 si le joueur 2 à gagné, '
              '0 s ils ont fait match nul : ')
    def get_match_result(self, match):
        return input(f'Qui a gagné le match {match} ? ')
