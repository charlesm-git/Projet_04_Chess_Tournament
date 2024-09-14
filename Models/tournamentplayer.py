class TournamentPlayer:
    def __init__(self, player_chess_id, player_current_score=0):
        self.player_chess_id = player_chess_id
        self.player_tournament_score = player_current_score

    @classmethod
    def from_json_format(cls, player_data):
        return cls(*player_data.values())

    def __str__(self):
        return (f'{self.player_chess_id} - Score total sur le tournoi de '
                f'{self.player_tournament_score}')

    def __repr__(self):
        representation = (f'[chess_ID={self.player_chess_id}, '
                          f'score={self.player_tournament_score}]')
        return representation

    def save(self):
        """
        Display the tournament player's data in a dictionary for the storage
        """
        return {'player_chess_id': self.player_chess_id,
                'player_tournament_score': self.player_tournament_score}
