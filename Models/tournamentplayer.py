from Models.player import Player


class TournamentPlayer(Player):
    def __init__(self, player_chess_id, player_name, player_surname,
                 player_date_of_birth, player_current_score=0):
        super().__init__(player_chess_id, player_name, player_surname,
                         player_date_of_birth)
        self.score = player_current_score

    @classmethod
    def from_tournament_player_database_json_format(cls, player_data):
        return cls(*player_data.values())
        # return cls(player_data['player_chess_id'],
        #            player_data['player_name'],
        #            player_data['player_surname'],
        #            player_data['player_date_of_birth'],
        #            player_data['player_current_score'])

    def __str__(self):
        return (f'{self.player_name} {self.player_surname} - '
                f'{self.player_chess_id} (score total sur le tournoi de {self.score})')

    def __repr__(self):
        representation = (f'[chess_ID={self.player_chess_id}, '
                          f'score={self.score}]')
        return representation

    def save(self):
        """
        Display the tournament player's data in a dictionary for the storage
        """
        data = super().save()
        data['player_current_score'] = self.score
        return data


