from .player import Player


class Match:

    def __init__(self, player1: Player, player2: Player):
        self.player1 = player1
        self.score_player1 = 0
        self.player2 = player2
        self.score_player2 = 0

    def result(self):
        """ Display the match result in a tuple """
        return ([self.player1, self.score_player1],
                [self.player2, self.score_player2])

    def __repr__(self):
        return (f'{self.player1.player_chess_id}={self.score_player1}, '
                f'{self.player2.player_chess_id}={self.score_player2}')
