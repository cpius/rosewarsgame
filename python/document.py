from player import Player
from gamestate_module import Gamestate
import units as units_module
import ai_module


class DocumentConverter:
    def document_to_gamestate(self, document):
        player1 = Player("Green")
        player1.ai_name = document["player1_intelligence"]
        player1.ai = self.get_ai_from_name(player1.ai_name)

        player1_units = self.get_units(document["player1_units"])

        player2 = Player("Red")
        player2.ai_name = document["player2_intelligence"]
        player2.ai = self.get_ai_from_name(player2.ai_name)

        player2_units = self.get_units(document["player2_units"])

        turn = document["turn"]
        has_extra_action = document["extra_action"]
        actions_remaining = document["actions_remaining"]

        return Gamestate(player1, player1_units, player2, player2_units, turn, actions_remaining, has_extra_action)

    def gamestate_to_document(self, gamestate):
        return {
            "Player1": "Mads",
            "Player2": "Jonatan"
        }

    def get_ai_from_name(self, name):
        if name == "Human":
            return name
        else:
            return ai_module.AI(name)

    def get_units(self, document):
        units = {}
        for position_string in document.keys():
            position = self.get_position(position_string)
            unit_document = document[position_string]
            if type(unit_document) is str:
                name = unit_document
            else:
                name = document[position_string]["name"]

            unit = getattr(units_module, name)()

            if type(unit_document) is dict:
                for attribute in unit_document:
                    setattr(unit, attribute, unit_document[attribute])

            units[position] = unit

        return units

    def get_position(self, position_string):
        column = ord(position_string[0]) - 64  # In ASCII A, B, C, D, E is 65, 66, 67, 68, 69
        row = int(position_string[1])
        return column, row
