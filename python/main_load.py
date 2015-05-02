from controller import Controller
from view.view_module import View
from game.enums import Intelligence


if __name__ == '__main__':

    view = View()

    controller = Controller.from_replay('./replay/a.json', player_intelligence=Intelligence.Human, opponent_intelligence=Intelligence.AI)

    controller.run_game()
