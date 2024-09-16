class Player:

    def __init__(self, player_chess_id, player_name, player_surname,
                 player_date_of_birth):
        self.player_chess_id = player_chess_id
        self.player_name = player_name
        self.player_surname = player_surname
        self.player_date_of_birth = player_date_of_birth

    @classmethod
    def from_json_format(cls, player_data):
        """ Instance a Player from a dictionary built from a JSON format """
        return cls(*player_data.values())

    def __repr__(self):
        return (f'Player : chess_ID={self.player_chess_id}, '
                f'name={self.player_name}, '
                f'surname={self.player_surname}, '
                f'date_of_birth={self.player_date_of_birth}')

    def save(self):
        """ Display the player's data in a dictionary for the storage """
        return {'player_chess_id': self.player_chess_id,
                'player_name': self.player_name,
                'player_surname': self.player_surname,
                'player_date_of_birth': self.player_date_of_birth
                }
