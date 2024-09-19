from Models.tournamentplayer import TournamentPlayer
from Models.round import Round


class Tournament:

    def __init__(self, name, location, description, start_date, end_date,
                 number_of_rounds=4, current_round_number=0,
                 tournament_players=None, current_round=None,
                 rounds_results=None):
        self.name = name
        self.location = location
        self.start_date = start_date
        self.end_date = end_date
        self.NUMBER_OF_ROUNDS = number_of_rounds
        self.current_round_number = current_round_number
        self.current_round = current_round

        if description == '':
            self.description = 'Pas de description'
        else:
            self.description = description

        if rounds_results is None:
            self.rounds_results = []
        else:
            self.rounds_results = rounds_results

        if tournament_players is None:
            self.tournament_players = []
        else:
            self.tournament_players = tournament_players

    @classmethod
    def from_json_format(cls, tournament_data):
        players = []
        for player_data in tournament_data['players']:
            new_player = (
                TournamentPlayer
                .from_json_format(player_data))
            players.append(new_player)

        current_round = None
        if tournament_data['current_round'] is not None:
            current_round = (Round.from_json_format(
                tournament_data['current_round'], players))

        rounds_results = []
        for round in tournament_data['rounds_results']:
            new_round = Round.from_json_format(round, players)
            rounds_results.append(new_round)

        return cls(tournament_data['name'],
                   tournament_data['location'],
                   tournament_data['description'],
                   tournament_data['start_date'],
                   tournament_data['end_date'],
                   tournament_data['number_of_rounds'],
                   tournament_data['current_round_number'],
                   players,
                   current_round,
                   rounds_results)

    def __str__(self):
        return (f'{self.name} se déroulant du {self.start_date} au '
                f'{self.end_date} à {self.location}')

    def __repr__(self):
        return (f'name={self.name}, '
                f'location={self.location}, '
                f'description={self.description}, '
                f'start_date={self.start_date}, '
                f'end_date={self.end_date}, '
                f'number_of_rounds={self.NUMBER_OF_ROUNDS}, '
                f'current_round_number={self.current_round_number}, '
                f'players={self.tournament_players}, '
                f'current_round={self.current_round}, '
                f'rounds_results={self.rounds_results}')

    def save(self):
        """ Display the tournament's data in a dictionary for the storage """
        players_data = []
        for player in self.tournament_players:
            players_data.append(player.save())

        rounds_data = []
        for round in self.rounds_results:
            rounds_data.append(round.save())

        data = {'name': self.name,
                'location': self.location,
                'description': self.description,
                'start_date': self.start_date,
                'end_date': self.end_date,
                'number_of_rounds': self.NUMBER_OF_ROUNDS,
                'current_round_number': self.current_round_number,
                'players': players_data,
                'current_round': self.current_round.save() if (
                    self.current_round) else None,
                'rounds_results': rounds_data
                }
        return data
