from Models.tournamentplayer import TournamentPlayer
from Util.playerloader import get_player_from_chess_id


class Match:

    def __init__(self, player1: TournamentPlayer, player2: TournamentPlayer,
                 match_score_player1=0, match_score_player2=0):
        self.player1 = player1
        self.match_score_player1 = match_score_player1
        self.player2 = player2
        self.match_score_player2 = match_score_player2

    @classmethod
    def from_json_format(cls, match_data, tournament_players):
        player1 = None
        player2 = None
        for player in tournament_players:
            if (player.player_chess_id ==
                    match_data['player1']['player_chess_id']):
                player1 = player
                break
        for player in tournament_players:
            if (player.player_chess_id ==
                    match_data['player2']['player_chess_id']):
                player2 = player
                break
        return cls(player1,
                   player2,
                   match_data['match_score_player1'],
                   match_data['match_score_player2'])

    def get_match_status(self):
        """
        Display the match result in a tuple
        This result is stored in round.matches_result
        """
        return ([self.player1, self.match_score_player1],
                [self.player2, self.match_score_player2])

    def print_match(self, players):
        player1 = get_player_from_chess_id(self.player1.player_chess_id,
                                           players)
        player2 = get_player_from_chess_id(self.player2.player_chess_id,
                                           players)
        return (f'{player1.player_name} {player1.player_surname} vs '
                f'{player2.player_name} {player2.player_surname}')

    def __repr__(self):
        return (f'[{self.player1.player_chess_id}={self.match_score_player1}, '
                f'{self.player2.player_chess_id}={self.match_score_player2}]')

    def save(self):
        """ Display the match's data in a dictionary for the storage """
        return {'player1': self.player1.save(),
                'match_score_player1': self.match_score_player1,
                'player2': self.player2.save(),
                'match_score_player2': self.match_score_player2}
