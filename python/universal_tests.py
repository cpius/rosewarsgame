import json
from gamestate_module import Gamestate
from action import Action
import action_getter
import battle
from outcome import Outcome
import glob
import unittest


class UniversalTests(unittest.TestCase):

    def test_all_universal_tests(self):
        testcase_files = glob.glob("./utests/*.utest")
        for testcase_file in testcase_files:
            print "Testing: ", testcase_file

            test_document = json.loads(open(testcase_file).read())

            if test_document["type"] == "Does action exist":
                gamestate = Gamestate.from_document(test_document["gamestate"])
                action = Action.from_document_simple(test_document["action"])
                expected = test_document["result"]
                self.does_action_exist(gamestate, action, expected)

            if test_document["type"] == "Is attack and defence correct":
                gamestate = Gamestate.from_document(test_document["gamestate"])
                action = Action.from_document_simple(test_document["action"])
                attack = test_document["attack"]
                defence = test_document["defence"]

                self.is_attack_and_defence_correct(gamestate, action, attack, defence)

            if test_document["type"] == "Is outcome correct":
                gamestate = Gamestate.from_document(test_document["gamestate before action"])
                expected_gamestate = Gamestate.from_document(test_document["gamestate after action"])
                action = Action.from_document_simple(test_document["action"])
                outcome = Outcome.from_document(test_document["outcome"])

                self.is_outcome_correct(gamestate, action, outcome, expected_gamestate)

    def does_action_exist(self, gamestate, action, expected):
        available_actions = action_getter.get_actions(gamestate)
        actual = (action in available_actions)

        self.assertEqual(actual, expected, [str(action) for action in available_actions])

    def is_attack_and_defence_correct(self, gamestate, action, expected_attack, expected_defence):
        all_units = methods.merge_units(gamestate.units[0], gamestate.units[1])

        attacking_unit = all_units[action.start_position]
        defending_unit = all_units[action.attack_position]

        actual_attack = battle.get_attack_rating(attacking_unit, defending_unit, action)
        actual_defence = battle.get_defence_rating(attacking_unit, defending_unit, actual_attack)

        self.assertEqual(actual_attack, expected_attack, "Attack was wrong")
        self.assertEqual(actual_defence, expected_defence, "Defence was wrong")

    def is_outcome_correct(self, gamestate, action, outcome, expected_gamestate):
        gamestate.do_action(action, outcome)

        actual_gamestate_document = gamestate.to_document()
        expected_gamestate_document = expected_gamestate.to_document()

        self.assert_equal_documents(expected_gamestate_document, actual_gamestate_document)

    def assert_equal_documents(self, expected, actual):
        documents = "Expected:\n" + methods.document_to_string(expected)
        documents += "\nActual:\n" + methods.document_to_string(actual)
        self.assertEqual(expected, actual, "The document was mangled.\n\n" + documents)



if __name__ == "__main__":
    unittest.main()
