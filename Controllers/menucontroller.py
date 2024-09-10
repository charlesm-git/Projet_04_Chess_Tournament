class MenuController:

    def __init__(self, view):
        self.view = view

    def main_menu(self):
        while True:
            user_input = int(self.view.get_main_menu())
            if user_input in [1, 2, 3, 4, 5, 9]:
                break
            else:
                print()
                print('Veuillez entrer un chiffre indiqué')
        return int(user_input)

