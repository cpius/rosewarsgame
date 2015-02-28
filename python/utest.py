import json
from gamestate import Gamestate
from action import Action
from outcome import Outcome
import battle
import action_getter
import glob
from collections import Counter
from common import enum_attributes


def does_action_exist(test_document):
    gamestate = Gamestate.from_document(test_document["gamestate"])
    action = Action.from_document(gamestate.all_units(), test_document["action"])
    available_actions = action_getter.get_actions(gamestate)
    actual = (action in available_actions)
    expected = test_document["result"]

    return actual == expected


def does_turn_shift_work(test_document):
    pre_gamestate = Gamestate.from_document(test_document["pre_gamestate"])
    post_gamestate = Gamestate.from_document(test_document["post_gamestate"])
    pre_gamestate.shift_turn()
    pre_gamestate.flip_all_units()

    gamestate_document = pre_gamestate.to_document()
    expected_gamestate_document = post_gamestate.to_document()

    return gamestate_document == expected_gamestate_document


def does_upgrade_exist(test_document):
    gamestate1 = Gamestate.from_document(test_document["pre_gamestate"])
    gamestate2 = Gamestate.from_document(test_document["pre_gamestate"])
    expected_gamestate = Gamestate.from_document(test_document["post_gamestate"])

    for position, unit in gamestate1.player_units.items():
        if unit.should_be_upgraded():
            gamestate1.player_units[position] = unit.get_upgraded_unit_from_choice(0)
            gamestate2.player_units[position] = unit.get_upgraded_unit_from_choice(1)

    return (expected_gamestate in [gamestate1, gamestate2]) == test_document["result"]



def is_attack_and_defence_correct(test_document):
    gamestate = Gamestate.from_document(test_document["gamestate"])
    action = Action.from_document(gamestate.all_units(), test_document["action"])
    attack = test_document["attack"]
    defence = test_document["defence"]

    action.unit = gamestate.player_units[action.start_at]

    actual_attack = battle.get_attack(action, gamestate)
    actual_defence = battle.get_defence(action, actual_attack, gamestate)

    return (attack == actual_attack and defence == actual_defence)


def is_outcome_correct(test_document):
    gamestate = Gamestate.from_document(test_document["pre_gamestate"])
    expected_gamestate = Gamestate.from_document(test_document["post_gamestate"])
    action = Action.from_document(gamestate.all_units(), test_document["action"])
    outcome = Outcome.from_document(test_document["outcome"]) if "outcome" in test_document else None

    gamestate.do_action(action, outcome)

    gamestate_document = gamestate.to_document()
    expected_gamestate_document = expected_gamestate.to_document()

    return gamestate_document == expected_gamestate_document


def is_outcome_correct_extra_action(test_document):
    gamestate = Gamestate.from_document(test_document["pre_gamestate"])
    expected_gamestate = Gamestate.from_document(test_document["post_gamestate"])

    action = Action.from_document(gamestate.all_units(), test_document["action"])
    outcome = Outcome.from_document(test_document["outcome1"]) if "outcome1" in test_document else None
    gamestate.do_action(action, outcome)

    action = Action.from_document(gamestate.all_units(), test_document["extra_action"])
    outcome = Outcome.from_document(test_document["outcome2"]) if "outcome2" in test_document else None
    gamestate.do_action(action, outcome)

    gamestate_document = gamestate.to_document()
    expected_gamestate_document = expected_gamestate.to_document()

    return gamestate_document == expected_gamestate_document


def upgrade(test_document):
    gamestate = Gamestate.from_document(test_document["pre_gamestate"])
    expected_gamestate = Gamestate.from_document(test_document["post_gamestate"])

    if isinstance(test_document["upgrade"], basestring):
        upgrade_choice = test_document["upgrade"]
    else:
        upgrade_choice = enum_attributes(test_document["upgrade"])

    for position, unit in gamestate.player_units.items():
        gamestate.player_units[position] = unit.get_upgraded_unit_from_upgrade(upgrade_choice)

    return expected_gamestate.to_document() == gamestate.to_document()


def utest(test_document):
    return globals()[test_document["type"].lower().replace(" ", "_").replace(",", "")](test_document)


def run():
    testcase_files = glob.glob("./../sharedtests_1.1/*/*.json")

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

        results[test_document["type"]][test] += 1

    for key, value in results.items():
        print key + ": ", value



except_exceptions = False

if __name__ == "__main__":
    run()

