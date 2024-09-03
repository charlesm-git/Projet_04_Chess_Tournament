from .player import Player


class TournamentPlayer(Player):

    def __init__(self, player_chess_id, player_name, player_surname,
                 player_date_of_birth):
        super().__init__(player_chess_id, player_name, player_surname,
                         player_date_of_birth)
        self.score = 0
