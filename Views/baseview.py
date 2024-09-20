from Util.utils import valid_date_format


class BaseView:

    def __init__(self):
        pass

# Tournament Data Management
    def get_tournament_data(self):
        """
        Ask the User all the data necessary to create a tournament
        :return: The tournament data as a dictionary
        """
        print("\nCréation d'un nouveau tournoi")
        name = input('Entrer le nom du tournoi : ')
        location = input('Entrer la localisation du tournoi : ')
        description = input('Entrer, si besoin, une description '
                            'pour le tournoi : ')
        while True:
            start_date = input('Entrer la date de début du tournoi '
                               '(format : YYYY-MM-DD) : ')
            if valid_date_format(start_date):
                break
        while True:
            end_date = input('Entrer la date de fin du tournoi '
                             '(format : YYYY-MM-DD) : ')
            if valid_date_format(end_date):
                break
        tournament_data = {'name': name,
                           'location': location,
                           'description': description,
                           'start_date': start_date,
                           'end_date': end_date}
        while True:
            number_of_rounds = input('Par défault, un tournoi compte 4 tours. '
                                     'Si c est le cas, laisser cette ligne '
                                     'vide. Sinon, entrer le nombre de tours '
                                     'souhaités : ')
            if number_of_rounds.isdigit():
                tournament_data['number_of_rounds'] = int(number_of_rounds)
                break
            elif number_of_rounds == '':
                break
            else:
                print('Entrer soit un nombre entier, soit laisser le champ '
                      'vide')
        return tournament_data

    def get_tournament_to_load(self):
        """
        Ask the User all the data necessary to load a tournament from the
        database
        :return: The tournament data as a dictionary
        """
        tournament_index = input('Entrer le numéro du tournoi à charger : ')
        return tournament_index

    def tournament_loaded_successfully(self, tournament):
        """ Print a message to notify the tournament has been loaded """
        print(f'\nLe tournoi {tournament} a bien été chargé')

    def tournament_created_successfully(self, tournament):
        """ Print a message to notify the tournament has been created """
        print(f'\nLe tournoi {tournament} a bien été créé')

    def tournament_finished(self):
        """ Print a message to notify the tournament is now finished """
        print('\nLe tournoi est terminé. Bravo à tous les participant !')
        print('\nVoici les résultats :')

    def selected_tournament(self, tournament):
        """ Print a message to notify which tournament is currently in use """
        print(f'Le tournoi actuellement sélectionné est : {tournament}')

# Player Data Management
    def get_player_data(self):
        """
        Get the data of a new player
        :return: The player's data as a dictionary
        """
        player_name = input('Entrer le prenom du joueur : ')
        player_surname = input('Entrer le nom de famille du joueur : ')
        while True:
            player_date_of_birth = input('Entrer la date de naissance du '
                                         'joueur (format : YYYY-MM-DD) : ')
            if valid_date_format(player_date_of_birth):
                break
        return {'player_name': player_name,
                'player_surname': player_surname,
                'player_date_of_birth': player_date_of_birth}

    def get_player_chess_id(self):
        """ Ask the user to input the chess ID of a tournament participant """
        return input('Entrer l identifiant national du joueur (format : '
                     'AB12345) : ')

    def get_continue_adding_players(self):
        """ Ask the user if they want to continue adding players """
        while True:
            user_input = input('Ajouter un nouveau joueur ? Y/N : ')
            if user_input not in ['Y', 'N']:
                print('Erreur de saisie, entrer Y ou N')
            else:
                break
        if user_input == 'Y':
            return True
        return False

    def player_added_successfully(self):
        """
        Print a message to notify the player has been added to the database
        """
        print('Le joueur a bien été ajouté à la base de données des joueurs\n')

    def player_ranking(self, player, ranking):
        """ Print the players ranking at the end of the tournament """
        print(f'{ranking} : {player}')

# Tournament Flow Control
    def get_main_menu(self, tournament_controller):
        """ Print the main menu and get the user input """
        print('\n\nQue souhaitez-vous faire ?\n')
        if tournament_controller is not None:
            self.selected_tournament(tournament_controller.tournament)
        else:
            print('Aucun tournoi sélectionné pour le moment')
        print('\n1 - Ajouter des joueurs à la base de données')
        print('2 - Créer un nouveau tournoi')
        print('3 - Charger un tournoi de la base de données')
        print('4 - Ajouter des joueurs au tournoi')
        print('5 - Continuer le tournoi')
        print('6 - Rapports')
        print('9 - Quitter le programme')
        return input('\nEntrer le nombre correspondant : ')

    def get_report_menu(self):
        """ Print the report menu and get the user input """
        print('\nQuel rapport voulez-vous créer ?')
        print('1 - Liste des joueurs dans la base de données')
        print('2 - Liste des tournois créés')
        print('3 - Liste des joueurs dans le tournoi actuellement selectionné')
        print('4 - Liste de tous les tours et de tous les matchs du tournoi '
              'sélectionné')
        print('5 - Score du tournoi')
        print('9 - Retourner au menu principal')
        return input('\nEntrer le nombre correspondant : ')

    def get_continue_tournament(self, tournament):
        """ Ask the user if they want to continue the tournament """
        print()
        self.selected_tournament(tournament)
        while True:
            user_input = input('Continuer ? Y/N : ')
            if user_input not in ['Y', 'N']:
                print('Erreur de saisie, entrer Y ou N')
            else:
                break
        if user_input == 'Y':
            return True
        return False

    def welcome_message_tournament_player_input(self):
        """
        Starting message shown to the user when entering tournament participant
        """
        print('\nSelection des joueurs présents dans le tournoi')
        print('Entrer, un par un, les identifiants nationals des joueurs '
              'participant au tournois')
        print('Une fois terminé, appuyer sur Entrer\n')

    def get_next_round_matches(self, tournament, players):
        """ Print the matches for the current round """
        print(f'\nLes matches pour le {tournament.current_round.name} sont : ')
        for match in tournament.current_round.matches:
            print(match.print_match(players))

# Match Data Management
    def welcome_message_match_result(self):
        """ Tell the user how to enter the results of a match """
        print()
        print('Renseignement des résultats du tour')
        print('Entrer 1 si le joueur 1 à gagné, 2 si le joueur 2 à gagné, '
              '0 s ils ont fait match nul : ')

    def get_match_result(self, match, players):
        """ Ask the user for the result of a specific match """
        return input(f'Qui a gagné le match {match.print_match(players)} ? ')

# Error Handling
    def error_tournament_not_loaded(self):
        """
        Error in case an action on a tournament is made without a
        tournament being loaded yet
        """
        print('\nVous n avez selectionné aucun tournoi pour le moment. '
              'Veuillez créer ou charger un tournoi avant de réaliser cette '
              'action')

    def error_loading_tournament(self):
        """
        Error in case the tournament that is given by user doesn't exist in the
        database
        """
        print('\nAucun tournoi avec ces données n est enregistré dans la base '
              'de données')
        print('Vérifier les données entrées ou créer un nouveau tournoi')

    def error_no_players_in_tournament(self):
        """
        Error in case the tournament is started without any player in it yet
        """
        print('\nLe tournoi ne contient aucun joueur pour le moment. Veuillez '
              'en ajouter avant de continuer')

    def error_odd_number_of_players_in_tournament(self):
        """
        Error in case the tournament is started with an odd number of players
        """
        print("\nLe tournoi compte un nombre de joueur impair. Assurer vous "
              "d'avoir un nombre de joueur pair avant de le lancer.")

    def error_player_already_in_database(self):
        """
        Error in case the player that the user wants to add is already
        registered in the database
        """
        print('\nLe joueur avec cet identifiant exite déjà dans la base de '
              'données\n')

    def error_input(self):
        """ Error in case the input given by the user is not correct """
        print('\nErreur dans la saisie\n')
