from action import Action


class DocumentConverter:
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

    def action_to_document(self, action):
        return {
            "start_position": action.start_position,
            "end_position": action.end_position,
            "attack_position": action.attack_position,
            "ability_position": action.ability_position,
            "move_with_attack": action.move_with_attack,
            "ability": action.ability
        }

    def document_to_action(self, document):
        start_position = self.get_position(document["start_position"])

        if "end_position" in document:
            end_position = self.get_position(document["end_position"])
        else:
            end_position = None

        if "attack_position" in document:
            attack_position = self.get_position(document["attack_position"])
        else:
            attack_position = None

        if "ability_position" in document:
            ability_position = self.get_position(document["ability_position"])
        else:
            ability_position = None

        if "move_with_attack" in document:
            move_with_attack = document["move_with_attack"].lower() == "True"
        else:
            move_with_attack = False

        if "ability" in document:
            ability = document["ability"]
        else:
            ability = ""

        return Action(start_position,
                      end_position,
                      attack_position,
                      ability_position,
                      move_with_attack,
                      ability)

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
