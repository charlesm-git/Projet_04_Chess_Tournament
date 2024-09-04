from .tournamentplayer import TournamentPlayer


class Match:

    def __init__(self, player1: TournamentPlayer, player2: TournamentPlayer):
        self.player1 = player1
        self.match_score_player1 = 0
        self.player2 = player2
        self.match_score_player2 = 0

    def result(self):
        """ Display the match result in a tuple """
        return ([self.player1, self.match_score_player1],
                [self.player2, self.match_score_player2])

    def __str__(self):
        return (f'{self.player1.player_name} {self.player1.player_surname} vs '
                f'{self.player2.player_name} {self.player2.player_surname}')

    def __repr__(self):
        return (f'[{self.player1.player_chess_id}={self.match_score_player1}, '
                f'{self.player2.player_chess_id}={self.match_score_player2}]')
