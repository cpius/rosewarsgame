from gamestate.gamestate_module import Gamestate
from tests.test_library import *
from gamestate.action import Action
import ai.ai as ai
from operator import attrgetter
import ai.ai_factors as ai_factors
from glob import glob


def test(test_document, filename):

    gamestate = Gamestate.from_document(test_document["gamestate"])
    expected_action = Action.from_document(gamestate.all_units(), test_document["action"])

    scorer = ai_factors.FactorScorer()

    gamestate.set_available_actions()
    actions = list(ai.score_actions(gamestate, set(), scorer))
    actions.sort(key=attrgetter("total_score"), reverse=True)

    ai.document_actions(actions, "./replay/" + filename + ".txt")

    action = ai.select_action(gamestate)

    if action == expected_action:
        return True

    else:
        print()
        print("wrong result")
        for action in actions:
            print(action, action.total_score)
            print(action.factors)
            if hasattr(action, "next_action_if_win"):
                print(action.next_action_if_win)
            print()

        print(gamestate)
        print(expected_action)
        return False


def run():
    testcase_files = glob("./tests/ai_tests/*.json")

    #testcase_files = ["./tests/ai_tests/test6.json"]

    run_method(testcase_files, test)




