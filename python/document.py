from player import Player
from gamestate_module import Gamestate
import units as units_module
import ai_module


class DocumentConverter:
    def document_to_gamestate(self, document):
        player1 = Player("Green")
        player1.ai_name = document["player1_intelligence"]
        player1.ai = self.get_ai_from_name(player1.ai_name)

        player2 = Player("Red")
        player2.ai_name = document["player2_intelligence"]
        player2.ai = self.get_ai_from_name(player2.ai_name)

        return Gamestate(player1,
                         self.get_units(document["player1_units"]),
                         player2,
                         self.get_units(document["player2_units"]),
                         document["turn"],
                         document["actions_remaining"],
                         document["extra_action"],
                         document["created_at"])

    def gamestate_to_document(self, gamestate):
        player1_units = self.get_units_dict(gamestate.player_units())
        player2_units = self.get_units_dict(gamestate.opponent_units())

        return {
            "player1_intelligence": gamestate.current_player().ai_name,
            "player1_units": player1_units,
            "player2_intelligence": gamestate.opponent_player().ai_name,
            "player2_units": player2_units,
            "turn": gamestate.turn,
            "extra_action": gamestate.has_extra_action,
            "actions_remaining": gamestate.actions_remaining,
            "created_at": gamestate.start_time
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

            unit = getattr(units_module, name.replace(" ", "_"))()

            if type(unit_document) is dict:
                for attribute in unit_document.keys():
                    if attribute == "experience":
                        unit.xp = int(unit_document[attribute])
                    if attribute == "attack_counters":
                        unit.attack_counters = int(unit_document[attribute])
                    if attribute == "defence_counters":
                        unit.defence_counters = int(unit_document[attribute])

            units[position] = unit

        return units

    def get_units_dict(self, units):
        units_dict = dict()
        for unit_position in units.keys():
            unit = units[unit_position]

            unit_dict = dict()
            if unit.xp:
                unit_dict["experience"] = unit.xp
            if unit.attack_counters:
                unit_dict["attack_counters"] = unit.attack_counters
            if unit.defence_counters:
                unit_dict["defence_counters"] = unit.defence_counters
            if hasattr(unit, "blue_counters"):
                unit_dict["blue_counters"] = unit.blue_counters
            if hasattr(unit, "yellow_counters"):
                unit_dict["yellow_counters"] = unit.yellow_counters

            easy_position = self.get_position_string(unit_position)
            if len(unit_dict) > 0:
                unit_dict["name"] = unit.name
                units_dict[easy_position] = unit_dict
            else:
                units_dict[easy_position] = unit.name

        return units_dict

    def get_position(self, position_string):
        column = ord(position_string[0]) - 64  # In ASCII A, B, C, D, E is 65, 66, 67, 68, 69
        row = int(position_string[1])
        return column, row

    def get_position_string(self, position):
        columns = list(" ABCDE")
        return columns[position[0]] + str(position[1])
