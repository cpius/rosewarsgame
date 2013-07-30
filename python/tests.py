import unittest
from datetime import datetime
from gamestate_module import Gamestate
from pymongo import MongoClient
from bson.objectid import ObjectId
import action_getter
from action import Action
import common


class TestAI(unittest.TestCase):

    def test_GamestateDocument_WhenSavingAndLoadingDocument_ThenItShouldBeTheSame(self):
        document = self.get_test_gamestate_document()
        gamestate = Gamestate.from_document(document)
        same_document = gamestate.to_document()

        self.assert_equal_documents(document, same_document)

    def test_ActionDocument_WhenSavingAndLoading_ThenItShouldBeTheSame(self):
        gamestate = Gamestate.from_document(self.get_test_gamestate_document())
        action = action_getter.get_actions(gamestate)[3]
        action_document = action.to_document()
        same_action = Action.from_document(action_document)
        same_action_document = same_action.to_document()

        self.assertEquals(action, same_action)
        self.assertEquals(action_document, same_action_document)

    def test_IfBoardIsFlippedTwoTimes_ThenItShouldBeTheSame(self):
        gamestate = Gamestate.from_document(self.get_test_gamestate_document())
        gamestate_copy = Gamestate.from_document(self.get_test_gamestate_document())
        gamestate_copy.flip_units()
        gamestate_copy.flip_units()

        self.assertEquals(gamestate, gamestate_copy)

    def test_pymongo_WhenAGameIsInTheDatabase_ThenWeShouldBeAbleToFindIt(self):
        client = MongoClient(host="server.rosewarsgame.com")
        database = client.unnamed
        games = database.games

        game = games.find_one({"_id": ObjectId("51e86e5fea5a8f135cbc0326")})
        self.assertEqual(1, game["Turn"])

    def assert_equal_documents(self, expected, actual):
        documents = "Expected:\n" + common.document_to_string(expected)
        documents += "\nActual:\n" + common.document_to_string(actual)
        self.assertEqual(expected, actual, "The document was wrong.\n\n" + documents)

    def get_test_gamestate_document(self):
        now = datetime.utcnow()

        return {
            "actions_remaining": 1,
            "player1_units":
            {
                "D6":
                {
                    "name": "Knight",
                    "xp": 1
                }
            },
            "player2_units":
            {
                "C7":
                {
                    "name": "Royal Guard",
                    "xp": 3
                },
                "E7": "Archer"
            },
            "created_at": now
        }

if __name__ == "__main__":
    unittest.main()
