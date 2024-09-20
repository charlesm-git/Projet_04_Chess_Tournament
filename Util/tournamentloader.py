import json

from pathlib import Path
from Models.tournament import Tournament


def load_tournament_from_database():
    folder_path = Path('./data/tournament/')
    tournament_list = []
    for file in folder_path.iterdir():
        if file.is_file():
            with (open(file, 'r') as file_content):
                tournament_data = json.load(file_content)
                tournament = Tournament.from_json_format(tournament_data)
                tournament_list.append(tournament)
    return tournament_list
