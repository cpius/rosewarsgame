import json
from gamestate_module import Gamestate
from action import Action
import action_getter
import battle
from outcome import Outcome
import glob
import unittest
import common
import sys


class UniversalTestCase(unittest.TestCase):
    def __init__(self, testcase_file):
        super(UniversalTestCase, self).__init__()
        self.testcase_file = testcase_file

    def runTest(self):
        test_document = json.loads(open(self.testcase_file).read())

        # print "\n\nTesting", self.testcase_file

        if test_document["type"] == "Does action exist":
            gamestate = Gamestate.from_document(test_document["gamestate"])
            action = Action.from_document(gamestate.all_units(), test_document["action"])
            expected = test_document["result"]
            self.does_action_exist(gamestate, action, expected)

        if test_document["type"] == "Is attack and defence correct":
            gamestate = Gamestate.from_document(test_document["gamestate"])
            action = Action.from_document(gamestate.all_units(), test_document["action"])
            attack = test_document["attack"]
            defence = test_document["defence"]

            self.is_attack_and_defence_correct(gamestate, action, attack, defence)

        if test_document["type"] == "Is outcome correct":
            gamestate = Gamestate.from_document(test_document["pre_gamestate"])
            expected_gamestate = Gamestate.from_document(test_document["post_gamestate"])
            action = Action.from_document(gamestate.all_units(), test_document["action"])
            outcome = Outcome.from_document(test_document["outcome"])

            self.is_outcome_correct(gamestate, action, outcome, expected_gamestate)

    def does_action_exist(self, gamestate, action, expected):
        available_actions = action_getter.get_actions(gamestate)
        actual = (action in available_actions)

        message = "Wrong action existance for " + self.testcase_file + "\n\n"
        if expected:
            message += "Requested action: " + str(action) + "\n"
        else:
            message += "Not-allowed action:" + str(action) + "\n"

        message += "Available actions:"
        for available_action in available_actions:
            message += str(available_action) + "\n"

        self.assertEqual(actual, expected, message)

    def is_attack_and_defence_correct(self, gamestate, action, expected_attack, expected_defence):
        all_units = gamestate.all_units()

        attacking_unit = all_units[action.start_at]
        defending_unit = all_units[action.target_at]

        actual_attack = battle.get_attack_rating(attacking_unit, defending_unit, action, gamestate.player_units)
        actual_defence = battle.get_defence_rating(attacking_unit, defending_unit, actual_attack, action,
                                                   gamestate.enemy_units)

        error_string = "Filename" + self.testcase_file + "\n" + \
                       "Expected attack / defence " + str(expected_attack) + "," + str(expected_defence) + "\n" + \
                       "Actual attack / defence " + str(actual_attack) + "," + str(actual_defence) + "\n" \


        self.assertEqual(actual_attack, expected_attack, error_string)
        self.assertEqual(actual_defence, expected_defence, error_string)

    def is_outcome_correct(self, gamestate, action, outcome, expected_gamestate):
        gamestate.do_action(action, outcome)

        actual_gamestate_document = gamestate.to_document()
        expected_gamestate_document = expected_gamestate.to_document()

        self.assert_equal_documents(expected_gamestate_document, actual_gamestate_document)

    def assert_equal_documents(self, expected, actual):
        message = "Wrong document for " + self.testcase_file + "\n\n"
        message += "Expected:\n" + common.document_to_string(expected)
        message += "\nActual:\n" + common.document_to_string(actual)

        self.assertEqual(expected, actual, message)


if __name__ == "__main__":
    runner = unittest.TextTestRunner()

    suite = unittest.TestSuite()

    if len(sys.argv) == 2:
        testcase_files = [sys.argv[1]]

    else:
        testcase_files = glob.glob("./utests/*.utest")

    for testcase_file in testcase_files:
        suite.addTest(UniversalTestCase(testcase_file))

    runner.run(suite)
