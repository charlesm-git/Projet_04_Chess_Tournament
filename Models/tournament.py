import datetime


def starting_date():
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d")
    return timestamp


class Tournament:

    def __init__(self, name, location, description, start_date, end_date,
                 number_of_rounds=4):
        self.name = name
        self.location = location
        self.NUMBER_OF_ROUNDS = number_of_rounds
        self.current_round_number = 0
        if description == '':
            self.description = 'Pas de description'
        else:
            self.description = description
        self.start_date = start_date
        self.end_date = end_date
        self.current_round = None
        self.rounds_results = []
        self.tournament_players = []

    def __repr__(self):
        return (f'name={self.name}, '
                f'location={self.location}, '
                f'number_of_rounds={self.NUMBER_OF_ROUNDS}, '
                f'current_round={self.current_round_number}, '
                f'description={self.description}, '
                f'start_date={self.start_date}, '
                f'end_date={self.end_date}, '
                f'players={self.tournament_players}')

    def save(self):
        """ Display the tournament's data in a dictionary for the storage """
        return {'name': self.name,
                'location': self.location,
                'description': self.description,
                'start_date': self.start_date,
                'end_date': self.end_date,
                'number_of_rounds': self.NUMBER_OF_ROUNDS,
                'current_round': self.current_round_number,
                'rounds_results': self.rounds_results,
                'players': self.tournament_players
                }
