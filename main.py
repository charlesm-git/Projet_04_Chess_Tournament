from Views.baseview import BaseView
from Controllers.basecontroller import BaseController

if __name__ == "__main__":

    view = BaseView()
    controller = BaseController(view)
    while controller.menu_controller.main_menu_action():
        pass
