from datetime import datetime
import re


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


def round_date():
    timestamp = datetime.now().strftime("%Y-%m-%d-T%H:%M:%S")
    return timestamp
