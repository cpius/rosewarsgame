from gamestate.gamestate_module import Gamestate
from tests.test_library import *
from gamestate.action import Action
import ai.ai as ai
from operator import attrgetter
from glob import glob


def test(test_document, filename):

    gamestate = Gamestate.from_document(test_document["gamestate"])
    expected_action = Action.from_document(gamestate.all_units(), test_document["action"])

    gamestate.set_available_actions()
    actions = list(ai.score_actions(gamestate, set()))
    actions.sort(key=attrgetter("total_score"), reverse=True)

    ai.document_actions(actions, "./replay/" + filename + ".txt")

    action = ai.select_action(gamestate)

    if test_document["type"] == "Is action correct":
        expected_result = True
    else:
        expected_result = False

    if (action == expected_action) == expected_result:
        return True

    else:
        print()
        print("wrong result")
        for action in actions:
            print(action, action.total_score)
            if hasattr(action, "chance_of_win"):
                print("Chance of win:", action.chance_of_win)
            print("Factors:", action.factors)
            if hasattr(action, "next_action"):
                print("Next action:", action.next_action)
            print()

        print(gamestate)
        print(expected_action)
        return False


def run():
    testcase_files = glob("./tests/ai_tests/*.json")

    #testcase_files = ["./tests/ai_tests/test12.json"]

    run_method(testcase_files, test)




