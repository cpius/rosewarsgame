from action import Action, MoveOrStay


class DocumentConverter:
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
            move_with_attack = document["move_with_attack"]
        else:
            move_with_attack = MoveOrStay.UNKNOWN

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

    def get_position(self, position_string):
        column = ord(position_string[0]) - 64  # In ASCII A, B, C, D, E is 65, 66, 67, 68, 69
        row = int(position_string[1])
        return column, row

    def get_position_string(self, position):
        columns = list(" ABCDE")
        return columns[position.column] + str(position.row)
