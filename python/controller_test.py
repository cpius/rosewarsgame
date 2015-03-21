import json
from gamestate import Gamestate
import glob
from collections import Counter
from server_library import *
from game import Game
from controller import Controller
from outcome import Outcome


rolls = namedtuple("rolls", ["attack", "defence"])

class View:
    def draw_game(self, *args, **kwargs):
        pass

    def draw_action(self, *args, **kwargs):
        pass

    def save_screenshot(self, *args, **kwargs):
        pass


def determine_outcome(*args):
    return Outcome({Position.from_string("E5"): rolls(6, 1)})


def add_log(*args):
    pass


def give_output(actual_gamestate, expected_gamestate, actual_positions, expected_positions):

    print(actual_positions, expected_positions)
    if actual_gamestate == expected_gamestate:
        if actual_positions == expected_positions:
            return True

    if actual_gamestate != expected_gamestate:
        print("act gamestate", actual_gamestate)
        print("exp gamestate", expected_gamestate)
        print()

    if actual_positions != expected_positions:
        print("act position", actual_positions)
        print("exp position", expected_positions)
        print()

    return False


def read_positions(positions):
    for key, value in positions.items():
        if value == "None":
            value = None
        else:
            value = Position.from_string(value)
        positions[key] = value
    return positions


def is_outcome_correct(test_document):
    game = Game.from_log_document(test_document)
    controller = Controller(View())
    controller.positions = read_positions(test_document["pre_positions"])

    controller.game = game
    click_position = Position.from_string(test_document["click_position"])
    controller.game.gamestate.set_available_actions()
    controller.determine_outcome = determine_outcome
    controller.add_log = add_log

    controller.left_click(click_position)

    actual_gamestate = controller.game.gamestate.to_document()
    expected_gamestate = Gamestate.from_document(test_document["post_gamestate"]).to_document()

    actual_positions = controller.positions
    expected_positions = read_positions(test_document["post_positions"])


    return give_output(actual_gamestate, expected_gamestate, actual_positions, expected_positions)


def is_outcome_correct_extra_action(test_document):
    gamestate = Gamestate.from_document(test_document["pre_gamestate"])
    expected_gamestate = Gamestate.from_document(test_document["post_gamestate"])

    action = Action.from_document(gamestate.all_units(), test_document["action"])
    outcome = Outcome.from_document(test_document["outcome1"]) if "outcome1" in test_document else None
    gamestate.do_action(action, outcome)

    extra_action = Action.from_document(gamestate.all_units(), test_document["extra_action"])
    outcome = Outcome.from_document(test_document["outcome2"]) if "outcome2" in test_document else None
    gamestate.do_action(extra_action, outcome)

    actual = gamestate.to_document()
    expected = expected_gamestate.to_document()
    return actual == expected


def utest(test_document):
    return globals()[test_document["type"].lower().replace(" ", "_").replace(",", "")](test_document)


def run():
    testcase_files = glob.glob("./controller_tests/*.json")
    #testcase_files = ["./../sharedtests_1.1/Poison_II/Turn_PoisonII_1.json"] #running just 1 test.

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
    print()
    print("Total:", str(total[True]) + " passed, " + str(total[False]) + " failed")


except_exceptions = False

if __name__ == "__main__":
    run()

