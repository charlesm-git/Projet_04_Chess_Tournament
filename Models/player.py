class Player:

    def __init__(self, player_chess_id, player_name, player_surname,
                 player_date_of_birth):
        self.player_chess_id = player_chess_id
        self.player_name = player_name
        self.player_surname = player_surname
        self.player_date_of_birth = player_date_of_birth

    @classmethod
    def from_scratch(cls, chess_id, player_name, player_surname,
                     player_date_of_birth):
        return cls(chess_id, player_name, player_surname, player_date_of_birth)

    @classmethod
    def from_json_format(cls, player_data):
        # player_data = json.loads(json_data)
        return cls(player_data['player_chess_id'],
                   player_data['player_name'],
                   player_data['player_surname'],
                   player_data['player_date_of_birth'])

    def __repr__(self):
        return (f'chess_ID={self.player_chess_id}, '
                f'name={self.player_name}, '
                f'surname={self.player_surname}, '
                f'date_of_birth={self.player_date_of_birth}')

    def player_json_data(self):
        """ Display the player's data in a dictionary """
        data = {'player_chess_id': self.player_chess_id,
                'player_name': self.player_name,
                'player_surname': self.player_surname,
                'player_date_of_birth': self.player_date_of_birth
                }
        return data
