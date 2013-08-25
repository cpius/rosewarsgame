import os
import json
from gamestate import Gamestate
from action import Action
import action_getter
import battle
from outcome import Outcome
from common import *
import traceback


def run_test(test_file):

    def write_message_action():
        print "Wrong action existence for", test_file
        if "description" in test_document:
            print "Description:", test_document["description"]
        print "Gamestate:", gamestate
        if expected:
            print "Requested action: " + str(action) + "\n"
        else:
            print "Not-allowed action:" + str(action) + "\n"

        print "Available actions:"
        for available_action in available_actions:
            print str(available_action)
        print

    def write_message_extra_action():
        print "Wrong action existence for", test_file
        if "description" in test_document:
            print "Description:", test_document["description"]
        print "Gamestate:", gamestate
        print "Requested action: " + str(extra_action) + "\n"

        print "Available actions:"
        for available_action in extra_actions:
            print str(available_action)
        print

    def write_message_AD():
        print "Wrong attack / defence for", test_file
        if "description" in test_document:
            print "Description:", test_document["description"]
        print "Gamestate: ", gamestate
        print "Expected attack / defence " + str(expected_attack) + "," + str(expected_defence)
        print "Actual attack / defence " + str(actual_attack) + "," + str(actual_defence)
        print

    def write_message_outcome():
        print "Wrong outcome for", test_file
        if "description" in test_document:
            print "Description:", test_document["description"]
        print "Action:"
        print action
        print "Actual gamestate:"
        print document_to_string(actual_gamestate_document)
        print "Expected gamestate:"
        print document_to_string(expected_gamestate_document)
        print

    def write_message_extra_outcome():
        print "Wrong outcome for", test_file
        if "description" in test_document:
            print "Description:", test_document["description"]
        print "Initial gamestate:"
        print document_to_string(initial_gamestate)
        print "Intermediate gamestate:"
        print document_to_string(intermediate_gamestate)
        print "Actual gamestate:"
        print document_to_string(actual_gamestate_document)
        print "Expected gamestate:"
        print document_to_string(expected_gamestate_document)
        print

    def write_message_turn_shift():
        print "Wrong turn shift for", test_file
        if "description" in test_document:
            print "Description:", test_document["description"]
        print "Actual gamestate:"
        print document_to_string(actual_gamestate_document)
        print "Expected gamestate:"
        print document_to_string(expected_gamestate_document)
        print

    def write_message_upgrade():
        print "wrong result upgrade for", test_file
        if "description" in test_document:
            print "Description:", test_document["description"]
        print "Actual gamestate:"
        print document_to_string(actual_gamestate_document)
        print "Expected gamestate:"
        print document_to_string(expected_gamestate_document)
        print

    try:
        test_document = json.loads(open(test_file).read())
    except ValueError:
        print "Failed to load test document: " + test_file
        print
        return "read error"

    try:
        if test_document["type"] == "Does action exist":
            gamestate = Gamestate.from_document(test_document["gamestate"])
            action = Action.from_document(gamestate.all_units(), test_document["action"])
            expected = test_document["result"]

            available_actions = action_getter.get_actions(gamestate)
            actual = (action in available_actions)

            if actual == expected:
                return "pass"
            else:
                write_message_action()
                return "wrong result"

        if test_document["type"] == "Is attack and defence correct":
            gamestate = Gamestate.from_document(test_document["gamestate"])
            action = Action.from_document(gamestate.all_units(), test_document["action"])
            expected_attack = test_document["attack"]
            expected_defence = test_document["defence"]

            all_units = gamestate.all_units()

            attacking_unit = all_units[action.start_at]
            defending_unit = all_units[action.target_at]

            actual_attack = battle.get_attack_rating(attacking_unit, defending_unit, action, gamestate.player_units)
            actual_defence = battle.get_defence_rating(attacking_unit, defending_unit, actual_attack, action,
                                                       gamestate.enemy_units)

            if actual_attack == expected_attack and actual_defence == expected_defence:
                return "pass"
            else:
                write_message_AD()
                return "wrong result"

        if test_document["type"] == "Is outcome correct":
            gamestate = Gamestate.from_document(test_document["pre_gamestate"])
            expected_gamestate = Gamestate.from_document(test_document["post_gamestate"])
            action = Action.from_document(gamestate.all_units(), test_document["action"])
            outcome = None
            if "outcome" in test_document:
                outcome = Outcome.from_document(test_document["outcome"])

            gamestate.do_action(action, outcome)

            actual_gamestate_document = gamestate.to_document()
            expected_gamestate_document = expected_gamestate.to_document()

            if actual_gamestate_document == expected_gamestate_document:
                if not action.is_attack():
                    return "pass"
            else:
                write_message_outcome()
                return "wrong result"

        if test_document["type"] == "Is outcome correct, extra action":
            gamestate = Gamestate.from_document(test_document["pre_gamestate"])
            expected_gamestate = Gamestate.from_document(test_document["post_gamestate"])
            action = Action.from_document(gamestate.all_units(), test_document["action"])
            extra_action = Action.from_document(gamestate.all_units(), test_document["extra_action"])
            outcome1 = None
            outcome2 = None
            if "outcome1" in test_document:
                outcome1 = Outcome.from_document(test_document["outcome1"])
            if "outcome2" in test_document:
                outcome2 = Outcome.from_document(test_document["outcome2"])

            initial_gamestate = gamestate.to_document()
            gamestate.do_action(action, outcome1)
            intermediate_gamestate = gamestate.to_document()
            extra_action.unit = gamestate.all_units()[extra_action.start_at]
            extra_actions = gamestate.get_actions()

            if not extra_action in extra_actions:
                write_message_extra_action()
                return "wrong result"

            gamestate.do_action(extra_action, outcome2)
            actual_gamestate_document = gamestate.to_document()
            expected_gamestate_document = expected_gamestate.to_document()

            if actual_gamestate_document == expected_gamestate_document:
                return "pass"
            else:
                write_message_extra_outcome()
                return "wrong result"

        if test_document["type"] == "Is outcome correct":
            gamestate = Gamestate.from_document(test_document["pre_gamestate"])
            expected_gamestate = Gamestate.from_document(test_document["post_gamestate"])
            action = Action.from_document(gamestate.all_units(), test_document["action"])
            if action.is_attack() and action.move_with_attack:
                outcome = None
                if "outcome" in test_document:
                    outcome = Outcome.from_document(test_document["outcome"])

                action.move_with_attack = None
                gamestate.do_action(action, outcome)
                action.move_with_attack = True
                rolls = outcome.for_position(action.target_at)
                gamestate.move_melee_unit_to_target_tile(rolls, action)

                actual_gamestate_document = gamestate.to_document()
                expected_gamestate_document = expected_gamestate.to_document()

                if actual_gamestate_document == expected_gamestate_document:
                    return "pass"
                else:
                    print
                    print "Wrong outcome for post movement"
                    write_message_outcome()
                    return "wrong result"
            else:
                return "pass"

        if test_document["type"] == "Does turn shift work":
            gamestate = Gamestate.from_document(test_document["pre_gamestate"])
            expected_gamestate = Gamestate.from_document(test_document["post_gamestate"])

            gamestate.shift_turn()
            gamestate.flip_all_units()

            actual_gamestate_document = gamestate.to_document()
            expected_gamestate_document = expected_gamestate.to_document()

            if actual_gamestate_document == expected_gamestate_document:
                return "pass"
            else:
                write_message_turn_shift()
                return "wrong result"

        if test_document["type"] == "Upgrade":
            gamestate = Gamestate.from_document(test_document["pre_gamestate"])
            expected_gamestate = Gamestate.from_document(test_document["post_gamestate"])

            if isinstance(test_document["upgrade"], basestring):
                upgrade_choice = test_document["upgrade"]
            else:
                upgrade_choice = enum_attributes(test_document["upgrade"])

            for position, unit in gamestate.player_units.items():
                if unit.is_allowed_upgrade_choice(upgrade_choice):
                    gamestate.player_units[position] = unit.get_upgraded_unit(upgrade_choice)

            actual_gamestate_document = gamestate.to_document()
            expected_gamestate_document = expected_gamestate.to_document()

            if actual_gamestate_document == expected_gamestate_document:
                return "pass"
            else:
                write_message_upgrade()
                return "wrong result"

    except Exception as e:
        print test_file
        print e
        print traceback.format_exc()
        return "run error"


break_at_error = False
test_file = "./../sharedtests_development\OutcomeExtra_Samurai_2.json"
test_file = ""

if test_file:

    result = run_test(test_file)
    print result

else:
    path1 = "./../sharedtests/"
    path2 = "./../sharedtests_development/"
    testcase_files = [os.path.join(dirpath, f) for dirpath, dirnames, files in os.walk(path1)
                      for f in files if f.endswith(".json")] + \
                     [os.path.join(dirpath, f) for dirpath, dirnames, files in os.walk(path2)
                      for f in files if f.endswith(".json")]

    results = {"pass": 0, "read error": 0, "wrong result": 0, "run error": 0, "total": 0}
    for test_file in testcase_files:

        result = run_test(test_file)
        results[result] += 1
        results["total"] += 1
        if break_at_error and result != "pass":
            break

    print
    print "RESULTS", results
