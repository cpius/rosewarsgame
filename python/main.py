from view import View
from controller import Controller


if __name__ == '__main__':
    view = View()

    controller = Controller(view)
    controller.run_game()
