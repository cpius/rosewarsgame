import sys
from view import View
from controller import Controller


if __name__ == '__main__':
    view = View()

    if len(sys.argv) >= 4 and sys.argv[1] == "network":
        game_id = sys.argv[2]
        player = sys.argv[3]
        controller = Controller.from_network(view, game_id, player)
    else:
        controller = Controller.new_game(view)

    controller.run_game()
