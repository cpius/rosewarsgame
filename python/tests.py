import unittest
import re
import units as units_module
import ai_module
from player import Player
from gamestate_module import Gamestate


class TestAI(unittest.TestCase):
    def test_AI_Evaluator_WhenMoveAttackIsPossible_ThenItShouldBeChosen(self):

        test_file = open("tests/AI_Evaluator_WhenAttackIsAvailable_ThenChooseIt.txt", "r")
        gamestate = self.parse_test_case(test_file)

        action = gamestate.current_player().ai.select_action(gamestate)

        self.assertTrue(re.search(".*attack.*", str(action)), "The ai did not choose to attack")

    def test_AI_Evaluator_WhenNoActionsAreAvailable_ThenPassTurnToOtherPlayer(self):

        test_file = open("tests/AI_Evaluator_WhenNoActionsAreAvailable_ThenPassTurnToOtherPlayer.txt", "r")
        gamestate = self.parse_test_case(test_file)
        active_player_before = gamestate.current_player()
        action = gamestate.current_player().ai.select_action(gamestate)

        print "Actions before: " + str(gamestate.get_actions_remaining())
        gamestate.do_action(action)
        print "Actions after: " + str(gamestate.get_actions_remaining())

        active_player_after = gamestate.current_player()

        self.assertNotEquals(active_player_before, active_player_after, "The turn did not switch")

    def parse_test_case(self, test_file):

        self.assertTrue(re.search('^== [A-Za-z0-9-_]+ ==\r?\n$', test_file.readline()),
                        "Please begin test specification with '== Test_Name =='")

        match = re.search("^Turn: ([1-9][0-9]*)\r?\n$", test_file.readline())
        self.assertTrue(match, "Incorrent turn specification. Please write Turn: [1..]")
        turn = int(match.group(1))

        match = re.search('^Actions: ([0-2])\r?\n$', test_file.readline())
        self.assertTrue(match, "Incorrect action specification. Please write 'Actions: [0..2]'")
        actions_remaining = int(match.group(1))

        player1, player1_units = self.parse_player(test_file)
        player2, player2_units = self.parse_player(test_file)

        gamestate = Gamestate(player1, player1_units, player2, player2_units, turn, actions_remaining)

        self.assertNotEqual("Human", gamestate.current_player().ai, "Active player is a human. It should be a computer")

        return gamestate

    def parse_player(self, test_file):
        self.assertTrue(re.search('^Player(1|2):\r?\n$', test_file.readline()),
                        "Incorrect player specification. Please write: Player1/Player2")

        match = re.search("^(Red|Green)\r?\n$", test_file.readline())
        self.assertTrue(match, "Incorrect player color specification. Please write: Red/Green")
        player = Player(match.group(1))

        match = re.search('^([A-Za-z]+)\r?\n', test_file.readline())
        self.assertTrue(match, "Incorrect player specification. Please write either Human or a named AI")
        player.ai_name = match.group(1)
        if match.group(1) == "Human":
            player.ai = match.group(1)
        else:
            player.ai = ai_module.AI(match.group(1))

        match = re.search('^Extra action: (True|False)\r?\n$', test_file.readline())
        self.assertTrue(match, "Incorrect extra action specification. Please write 'Extra action: True/False'")
        if match.group(1) == "True":
            player.extra_action = True

        self.assertTrue(re.search("\r?\n", test_file.readline()), "Please wrap unit specifications in empty lines")

        units = {}
        line = test_file.readline()
        while line != "" and line != "\r\n" and line != "\n":
            match = re.search("^([A-E][0-8])\r?\n$", line)
            self.assertTrue(match, "Incorrect unit specification. Please write something like 'A1<newline>Archer'")

            position = (ord(match.group(1)[0]) - 64, int(match.group(1)[1]))

            line = test_file.readline()
            match = re.search("^([A-Za-z -_]+)\r?\n$", line)

            units[position] = getattr(units_module, match.group(1))()

            match = re.search("^\r?\n$", test_file.readline())
            self.assertTrue(match, "Please wrap unit specifications in empty lines")
            line = test_file.readline()

        return player, units


if __name__ == "__main__":
    unittest.main()
