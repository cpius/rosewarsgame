from view import View
from controller import Controller


if __name__ == '__main__':
    view = View()
    view.initialize()

    controller = Controller(view)
    controller.run_game()
