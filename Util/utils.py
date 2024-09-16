import re
from datetime import datetime
from pathlib import Path


def valid_date_format(date):
    """ Verify that the date input has the right format """
    try:
        datetime.strptime(date, '%Y-%m-%d')
    except ValueError:
        print('Erreur dans le format de la date, réessayez')
        return False
    return True


def valid_chess_id_format(chess_id):
    """ Verify that the chess ID input has the right format """
    pattern = r'^[A-Z]{2}\d{5}$'
    if re.match(pattern, chess_id) is None:
        print('Erreur dans le format de l identifiant, réessayez')
        return False
    return True


def get_round_date():
    """ Get the timestamps for the round start and end dates """
    timestamp = datetime.now().strftime("%Y-%m-%d-T%H:%M:%S")
    return timestamp


def folder_creation():
    """ Creates the data's storing folders if they don't already exist """
    tournament_directory = Path('../data/tournament/')
    player_database = Path('../data/players.json')
    if not tournament_directory.exists():
        tournament_directory.mkdir(parents=True)
        player_database.touch()


def tournament_name_formatting(name):
    """ Format the name of the tournament. Used for the storing """
    name = name.title()
    name = name.replace(' ', '_')
    return name
