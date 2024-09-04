from .player import Player


class TournamentPlayer(Player):

    def __init__(self, player_chess_id, player_name, player_surname,
                 player_date_of_birth):
        super().__init__(player_chess_id, player_name, player_surname,
                         player_date_of_birth)
        self.score = 0

    def __repr__(self):
        representation = (f'chess_ID={self.player_chess_id}, '
                          f'score={self.score}')
        return representation

    def save(self):
        """ Display the player's data in a dictionary for the storage """
        data = super().save()
        data['player_score'] = self.score
        return data
