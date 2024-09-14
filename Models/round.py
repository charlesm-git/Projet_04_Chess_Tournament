from Util.utils import get_round_date
from Models.match import Match


class Round:

    def __init__(self, tournament=None, name=None, start_date=None,
                 end_date=None, matches=None):
        if tournament:
            self.name = f'Round {tournament.current_round_number}'
            self.start_date = get_round_date()
            self.end_date = 0
            self.matches = []
        else:
            self.name = name
            self.start_date = start_date
            self.end_date = end_date
            self.matches = matches

    @classmethod
    def from_json_format(cls, round_data, tournament_players):
        round_matches = []
        for match in round_data['round_matches']:
            new_match = Match.from_json_format(match, tournament_players)
            round_matches.append(new_match)

        return cls(name=round_data['round_name'],
                   start_date=round_data['round_start_date'],
                   end_date=round_data['round_end_date'],
                   matches=round_matches)

    @classmethod
    def new_round_tournament(cls, tournament):
        return cls(tournament=tournament)

    def __str__(self):
        end_status = 'En cours'
        if self.end_date != 0:
            end_status = self.end_date

        matches_str = '\n'.join([f'{match.player1} / '
                                 f'{match.player2} /// '
                                 f'résultat du match : '
                                 f'{match.match_score_player1}'
                                 f'-{match.match_score_player2}'
                                 for match in self.matches])

        return (f'{self.name}\n'
                f'Date de début : {self.start_date}\n'
                f'Date de fin : {end_status}\n'
                f'matchs du round : \n{matches_str}')

    def __repr__(self):
        return (f'{self.name} : '
                f'start_date={self.start_date}, '
                f'end_date={self.end_date}, '
                f'matches={self.matches}')

    def save(self):
        """ Display the round's data in a dictionary for the storage """
        matches_data = []
        for match in self.matches:
            matches_data.append(match.save())
        return {'round_name': self.name,
                'round_start_date': self.start_date,
                'round_end_date': self.end_date,
                'round_matches': matches_data
                }
