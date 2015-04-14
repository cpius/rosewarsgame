from game.game_module import Game
import json
from game import server_library


def test_get_expected_action():
    game_document = json.loads(open("./tests/keep_replays/3.json").read())
    game = Game.from_log_document(game_document)
    expected_action = server_library.get_expected_action(game_document, game.gamestate)

    assert expected_action == (11, "move_with_attack")


def run():
    test_get_expected_action()
