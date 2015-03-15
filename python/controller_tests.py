from controller import Controller
from gamestate import Gamestate
import json
from glob import glob
from collections import Counter
from game import Game
from common import *
from player import Player


class FakeView:
    pass


def read_controller(document):
    gamestate = Gamestate.from_document(document["gamestate"])
    gamestate.set_available_actions()
    players = [Player("Green", Intelligence.AI), Player("Red", Intelligence.Human)]
    game = Game(players, gamestate)
    view = FakeView()
    controller = Controller(view)
    controller.game = game
    controller.positions = {
        "start_at": Position.from_string(document["start_at"]) if "start_at" in document else None,
        "end_at": Position.from_string(document["end_at"]) if "end_at" in document else None,
    }

    return controller


def check_position_result(document, function):
    controller = read_controller(document)
    position = Position.from_string(document["position"])
    result = document["return"]

    actual_result = getattr(controller, function)(position)

    return actual_result == result


def selecting_ranged_target(document):
    return check_position_result(document, "selecting_ranged_target")


def selecting_melee_target(document):
    return check_position_result(document, "selecting_melee_target")


def selecting_active_unit(document):
    return check_position_result(document, "selecting_active_unit")


def run():
    testcase_files = glob("controller_tests/*/*.json")
    #testcase_files = glob("controller_tests/*/selecting_melee_target_4.json") #running just 1 test.

    results = {}
    for file in testcase_files:
        test_document = json.loads(open(file).read())
        results[str(test_document["type"])] = Counter()

    for file in testcase_files:
        test_document = json.loads(open(file).read())

        if except_exceptions:
            try:
                test = utest(test_document)
            except Exception as e:
                test = "ERROR"
        else:
            test = utest(test_document)
        if test is not True:
            print(file)

        results[test_document["type"]][test] += 1

    print()
    total = Counter()
    for key, value in results.items():
        print(key + ": " + str(value[True]) + " passed, " + str(value[False]) + " failed")
        total += value
    print("total: ", total)


def utest(test_document):
    return globals()[test_document["type"].lower().replace(" ", "_").replace(",", "")](test_document)

except_exceptions = False

if __name__ == "__main__":
    run()