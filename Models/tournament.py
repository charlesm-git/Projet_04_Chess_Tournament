import datetime


def starting_date():
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d")
    return timestamp


class Tournament:

    def __init__(self, name, location, description,
                 tournament_players, number_of_rounds=4):
        self.name = name
        self.location = location
        self.NUMBER_OF_ROUNDS = number_of_rounds
        self.current_round = 1
        self.description = description
        self.start_date = None
        self.finish_date = None
        self.rounds = []
        self.tournament_players = {}

        for player in tournament_players:
            self.tournament_players[player["chess_id"]] = 0

    def __repr__(self):
        return (f'name={self.name}, '
                f'location={self.location}, '
                f'number_of_rounds={self.NUMBER_OF_ROUNDS}, '
                f'current_round={self.current_round}, '
                f'description={self.description}, '
                f'start_date={self.start_date}, '
                f'finish_date={self.finish_date}, '
                f'players={self.tournament_players}')

