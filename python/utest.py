import json
from gamestate import Gamestate
from action import Action
from outcome import Outcome
import battle
import action_getter
import glob
from collections import Counter
from common import *
from server_library import *


def does_action_exist(test_document):
    gamestate = Gamestate.from_document(test_document["gamestate"])
    action = Action.from_document(gamestate.all_units(), test_document["action"])
    available_actions = action_getter.get_actions(gamestate)
    actual = (action in available_actions)
    expected = test_document["result"]
    return give_output(actual, expected)


def is_the_game_over(test_document):
    gamestate = Gamestate.from_document(test_document["gamestate"])
    actual = gamestate.is_ended()
    expected = test_document["result"]
    return give_output(actual, expected)


def give_output(actual, expected):
    if actual == expected:
        return True
    print("act", actual)
    print("exp", expected)
    print()
    return False


def does_turn_shift_work(test_document):
    pre_gamestate = Gamestate.from_document(test_document["pre_gamestate"])
    post_gamestate = Gamestate.from_document(test_document["post_gamestate"])
    pre_gamestate.shift_turn()
    pre_gamestate.flip_all_units()

    actual = pre_gamestate.to_document()
    expected = post_gamestate.to_document()
    return give_output(actual, expected)


def does_upgrade_exist(test_document):
    gamestate1 = Gamestate.from_document(test_document["pre_gamestate"])
    gamestate2 = Gamestate.from_document(test_document["pre_gamestate"])
    expected_gamestate = Gamestate.from_document(test_document["post_gamestate"])

    for position, unit in gamestate1.player_units.items():
        if unit.should_be_upgraded():
            gamestate1.player_units[position] = unit.get_upgraded_unit_from_choice(0)
            gamestate2.player_units[position] = unit.get_upgraded_unit_from_choice(1)

    if (expected_gamestate in [gamestate1, gamestate2]) == test_document["result"]:
        return True
    else:
        print("g1", gamestate1.to_document())
        print("g2", gamestate2.to_document())
        print("ex", expected_gamestate.to_document())
        return False


def is_attack_and_defence_correct(test_document):
    gamestate = Gamestate.from_document(test_document["gamestate"])
    action = Action.from_document(gamestate.all_units(), test_document["action"])
    attack = test_document["attack"]
    defence = test_document["defence"]

    action.unit = gamestate.player_units[action.start_at]
    gamestate.move_unit(action.start_at, action.end_at)

    actual_attack = battle.get_attack(action, gamestate)
    actual_defence = battle.get_defence(action, actual_attack, gamestate)

    if attack == actual_attack and defence == actual_defence:
        return True
    else:
        print("actual and expected attack:", actual_attack, attack)
        print("actual and expected defence:", actual_defence, defence)
        return False


def is_outcome_correct(test_document):
    gamestate = Gamestate.from_document(test_document["pre_gamestate"])
    expected_gamestate = Gamestate.from_document(test_document["post_gamestate"])
    action = Action.from_document(gamestate.all_units(), test_document["action"])
    outcome = Outcome.from_document(test_document["outcome"]) if "outcome" in test_document else None

    gamestate.do_action(action, outcome)

    actual = gamestate.to_document()
    expected = expected_gamestate.to_document()
    return give_output(actual, expected)


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
    return give_output(actual, expected)


def upgrade(test_document):
    gamestate = Gamestate.from_document(test_document["pre_gamestate"])

    expected_gamestate = Gamestate.from_document(test_document["post_gamestate"])

    if type(test_document["upgrade"]) is str:
        upgrade_choice = enum_from_string["upgrade"]
    else:
        upgrade_choice = {}
        for key, value in test_document["upgrade"].items():
            attribute_name = key
            number = value

            attribute, attributes = get_attribute_from_document(attribute_name, number)
            upgrade_choice[attribute] = attributes

    for position, unit in gamestate.player_units.items():
        gamestate.player_units[position] = unit.get_upgraded_unit_from_upgrade(upgrade_choice)

    expected = expected_gamestate.to_document()
    actual = gamestate.to_document()
    return give_output(actual, expected)


def server(test_document):
    gamestate = Gamestate.from_document(test_document["gamestate"])
    if "upgrade" in test_document["action"]:
        is_valid, validation_message, new_unit_string = validate_upgrade(test_document["action"], gamestate)

        new_unit = json.loads(new_unit_string)
        expected = test_document["response"]

        if is_valid == expected["Status"] and validation_message == expected["Message"] and new_unit == expected["Unit"]:
            return True

        print("act", is_valid, validation_message, new_unit)
        print("exp", expected["Status"], expected["Message"], expected["Unit"])

        return False
    elif test_document["action"]["type"] == "action":
        result = validate_action(gamestate, test_document["action"])
        if isinstance(result, Action):
            outcome = determine_outcome_if_any(result, gamestate)

            if outcome and not test_document["response"]["Action outcome"]:
                print("Did not expect an outcome")

                return False
            if not outcome and test_document["response"]["Action outcome"]:
                print("Expected an outcome")

                return False

            return True
        else:
            print("Not implemented")

            return False
    else:
        print("Not implemented")

        return False


def utest(test_document):
    return globals()[test_document["type"].lower().replace(" ", "_").replace(",", "")](test_document)


def run():
    testcase_files = glob.glob("./../sharedtests_1.1/*/*.json")
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

