from Views.baseview import BaseView
from Controllers.basecontroller import Controller

if __name__ == "__main__":

    view = BaseView()
    controller = Controller(view)
    while controller.main_menu_action():
        pass
