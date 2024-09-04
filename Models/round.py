from Util.formatverification import round_date


class Round:

    def __init__(self, tournament):
        self.name = f'Round {tournament.current_round_number}'
        self.start_date = round_date()
        self.end_date = 0
        self.players = tournament.tournament_players
        self.matches = []

    def __repr__(self):
        return (f'{self.name} : '
                f'start_date={self.start_date}, '
                f'end_date={self.end_date}, '
                f'matches={self.matches}')
