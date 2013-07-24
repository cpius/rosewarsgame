from __future__ import division
import action_doer
import initializer
import action_getter
import ai_module
import ai_methods
import units as units_module
import json


class Gamestate:
    
    def __init__(self,
                 player1_units,
                 player2_units,
                 actions_remaining,
                 extra_action=False):
        self.units = [player1_units, player2_units]
        self.actions_remaining = actions_remaining
        self.extra_action = extra_action
        self.action_number = 0

    def do_action(self, action, outcome=None):
        outcome = action_doer.do_action(self, action, outcome)
        self.action_number += 1

        if self.actions_remaining > 0:
            self.available_actions = action_getter.get_actions(self)
            if not self.available_actions:
                self.actions_remaining = 0

        return outcome

    def initialize_turn(self):
        initializer.initialize_turn(self)

    def initialize_action(self):
        initializer.initialize_action(self)

    def get_actions(self):
        if getattr(self, "extra_action"):
            actions = action_getter.get_extra_actions(self)
        elif self.actions_remaining == 1 and hasattr(self, "available_actions"):
            actions = self.available_actions
        else:
            actions = action_getter.get_actions(self)

        for action in actions:
            if action.is_attack():
                action.chance_of_win = ai_methods.chance_of_win(action.unit_reference, action.target_reference, action)
                for sub_action in action.sub_actions:
                    sub_action.chance_of_win = ai_methods.chance_of_win(sub_action.unit_reference,
                                                                        sub_action.target_reference, sub_action)

        return actions

    def copy(self):
        saved_gamestate = save_gamestate(self)
        return load_gamestate(saved_gamestate)

    def __eq__(self, other):
        pass

    def set_network_player(self, local_player):
        for player in range(2):
            if self.players[player].player_id != local_player:
                self.players[player].ai_name = "Network"
                self.players[player].ai = "Network"

    def set_available_actions(self):
        self.available_actions = self.get_actions()


    def player_units(self):
        return self.units[0]

    def opponent_units(self):
        return self.units[1]

    def get_actions_remaining(self):
        return self.actions_remaining

    def set_actions_remaining(self, actions_remaining):
        self.actions_remaining = actions_remaining

    def decrement_actions_remaining(self):
        self.actions_remaining -= 1

    def recalculate_special_counters(self):
        for unit in self.units[0].itervalues():
            self.add_yellow_counters(unit)
            self.add_blue_counters(unit)

        for unit in self.units[1].itervalues():
            self.add_yellow_counters(unit)
            self.add_blue_counters(unit)

    def add_yellow_counters(self, unit):
        if hasattr(unit, "extra_life"):
            unit.yellow_counters = 1
        else:
            unit.yellow_counters = 0

    def add_blue_counters(self, unit):
        unit.blue_counters = 0
        if hasattr(unit, "frozen"):
            unit.blue_counters = unit.frozen
        if hasattr(unit, "attack_frozen"):
            unit.blue_counters = unit.attack_frozen
        if hasattr(unit, "just_bribed"):
            unit.blue_counters = 1

    @classmethod
    def from_document(cls, document):
        player1_units = cls.units_from_document(document["player1_units"])
        player2_units = cls.units_from_document(document["player2_units"])
        actions_remaining = document["actions_remaining"]
        if "extra_action" in document:
            extra_action = document["extra_action"]
        else:
            extra_action = False
        return cls(player1_units, player2_units, actions_remaining, extra_action)

    @classmethod
    def from_file(cls, path):
        document = json.loads(open(path).read())
        return Gamestate.from_document(document)

    @classmethod
    def units_from_document(cls, document):
        units = {}
        for position_string in document.keys():
            position = units_module.get_position(position_string)
            unit_document = document[position_string]

            if not type(unit_document) is dict:
                units[position] = getattr(units_module, unit_document.replace(" ", "_"))()
                continue

            name = document[position_string]["name"]
            unit = getattr(units_module, name.replace(" ", "_"))()
            for attribute in unit_document.keys():
                setattr(unit, attribute, unit_document[attribute])

            units[position] = unit

        return units

    @classmethod
    def get_ai_from_name(cls, name):
        if name == "Human":
            return name
        else:
            return ai_module.AI(name)

    def to_document(self):
        return {
            "player1_units": self.get_units_dict(self.units[0]),
            "player2_units": self.get_units_dict(self.units[1]),
            "extra_action": self.extra_action,
            "actions_remaining": self.actions_remaining
        }

    def get_units_dict(self, units):
        units_dict = dict()
        for unit_position in units.keys():
            unit = units[unit_position]

            unit_dict = {attribute: getattr(unit, attribute) for attribute in units_module.variable_attributes
                         if hasattr(unit, attribute) and getattr(unit, attribute)}

            easy_position = units_module.get_position_string(unit_position)
            if len(unit_dict) > 0:
                unit_dict["name"] = unit.name
                units_dict[easy_position] = unit_dict
            else:
                units_dict[easy_position] = unit.name

        return units_dict

    def is_turn_done(self):
        return self.actions_remaining < 1 and not getattr(self, "extra_action")

    def shift_turn(self):
        self.units = transform_units(self.units)
        self.units = self.units[::-1]
        self.initialize_turn()
        self.initialize_action()
        self.set_available_actions()

    def update_final_position(self, action, outcome):
        action_doer.update_final_position(action, outcome)


def save_gamestate(gamestate):
    return gamestate.to_document()


def load_gamestate(saved_gamestate):
    return Gamestate.from_document(saved_gamestate)


def transform_position(position):
    if position:
        return position[0], 9 - position[1]


def transform_units(units):
    new_units_players = []
    for units_player in units:
        new_units = {}
        for position, unit in units_player.items():
            new_units[transform_position(position)] = unit

        new_units_players.append(new_units)

    return new_units_players
