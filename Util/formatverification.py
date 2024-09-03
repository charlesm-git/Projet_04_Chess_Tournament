from datetime import datetime
import re


def valid_date_format(date):
    """ Verify that the date input has the right format """
    try:
        datetime.strptime(date, '%Y-%m-%d')
    except ValueError:
        return False
    return True


def valid_chess_id_format(chess_id):
    """ Verify that the chess ID input has the right format """
    pattern = r'^[A-Z]{2}\d{5}$'
    return re.match(pattern, chess_id)
