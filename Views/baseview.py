from Util.formatverification import valid_chess_id_format
from Util.formatverification import valid_date_format


class BaseView:

    def __init__(self):
        pass

    def get_player_data(self):
        """ Get the data of a new player """
        while True:
            player_chess_id = input('Entrer l identifiant national du joueur : ')
            if valid_chess_id_format(player_chess_id) is None:
                print('Erreur de format dans l identifiant national (AB12345)')
            else:
                break
        player_name = input('Entrer le prenom du joueur : ')
        player_surname = input('Entrer le nom de famille du joueur : ')
        while True:
            player_date_of_birth = input('Entrer la date de naissance du '
                                         'joueur (au format YYYY-MM-DD) : ')
            if not valid_date_format(player_date_of_birth):
                print('Erreur de saisie, entrer la date au bon format')
            else:
                break
        return {'player_chess_id': player_chess_id,
                'player_name': player_name,
                'player_surname': player_surname,
                'player_date_of_birth': player_date_of_birth}

    def get_tournament_players(self):
        """ Ask the user to input the chess ID of a tournament participant """
        return input('Identifiant national du participant : ')

    def tournament_player_message(self):
        """
        Starting massage shown to the user when entering tournament participant
        """
        print('Entrer, un par un, les identifiants nationals des joueurs '
              'participant au tournois')
        print('Une fois terminé, appuyer sur Entrer')
