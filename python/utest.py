import json
from gamestate_module import Gamestate
from action import Action
from outcome import Outcome
import common
import battle
import action_getter
import glob


def utest(test_document):

    if test_document["type"] == "Is outcome correct":
        gamestate = Gamestate.from_document(test_document["pre_gamestate"])
        expected_gamestate = Gamestate.from_document(test_document["post_gamestate"])
        action = Action.from_document(test_document["action"])
        outcome = Outcome.from_document(test_document["outcome"])

        action.add_references(gamestate)
        gamestate.do_action(action, outcome)

        gamestate_document = gamestate.to_document()
        expected_gamestate_document = expected_gamestate.to_document()

        if gamestate_document != expected_gamestate_document:
            return False

        return True

    if test_document["type"] == "Is attack and defence correct":
        gamestate = Gamestate.from_document(test_document["gamestate"])
        action = Action.from_document(test_document["action"])
        attack = test_document["attack"]
        defence = test_document["defence"]

        action.unit = gamestate.player_units()[action.start_position]

        action.add_references(gamestate)

        action_getter.add_unit_references(gamestate, action)
        all_units = common.merge_units(gamestate.units[0], gamestate.units[1])

        attacking_unit = all_units[action.start_position]

        defending_unit = all_units[action.attack_position]

        actual_attack = battle.get_attack_rating(attacking_unit, defending_unit, action, gamestate)
        actual_defence = battle.get_defence_rating(attacking_unit, defending_unit, actual_attack, action, gamestate)

        if attack != actual_attack or defence != actual_defence:
            print "exp", attack, defence
            print "act", actual_attack, actual_defence
            return False

        return True


    if test_document["type"] == "Does action exist":
        gamestate = Gamestate.from_document(test_document["gamestate"])
        action = Action.from_document(test_document["action"])
        available_actions = action_getter.get_actions(gamestate)
        actual = (action in available_actions)
        expected = test_document["result"]

        if actual != expected:
            print "action", action
            print
            print "available_actions"
            for action in available_actions:
                print action

            return False

        return True

    if test_document["type"] == "Does turn shift work":
        pre_gamestate = Gamestate.from_document(test_document["pre_gamestate"])
        post_gamestate = Gamestate.from_document(test_document["post_gamestate"])
        pre_gamestate.shift_turn()
        pre_gamestate.flip_units()

        gamestate_document = pre_gamestate.to_document()
        expected_gamestate_document = post_gamestate.to_document()

        return gamestate_document == expected_gamestate_document


def run():
    testcase_files = glob.glob("./utests/*.utest")
    for file in testcase_files:
        test_document = json.loads(open(file).read())

        if test_document["type"] != "Does action exist" and test_document["type"] != "Does the AI find the right move":
            print file
            print test_document["type"]
            if "description" in test_document:
                print test_document["description"]

            if except_exceptions:
                try:
                    test = utest(test_document)
                except Exception as e:
                    test = "ERROR"
                    print e
            else:
                test = utest(test_document)

            print "test", test
            print


except_exceptions = False

if __name__ == "__main__":
    run()

