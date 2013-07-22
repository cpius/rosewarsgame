from __future__ import division
import action_doer
import initializer
import action_getter
import saver
import ai_module
import ai_methods
from datetime import datetime
import units as units_module
from player import Player


class Gamestate:
    
    def __init__(self,
                 player1,
                 player1_units,
                 player2,
                 player2_units,
                 turn=1,
                 actions_remaining=2,
                 has_extra_action=False,
                 start_time=datetime.utcnow()):
        self.turn = turn
        self.units = [player1_units, player2_units]
        self.players = [player1, player2]
        self.actions_remaining = actions_remaining
        self.has_extra_action = has_extra_action
        self.start_time = start_time

    def do_action(self, action, controller=None):
        action_doer.do_action(self, action, controller)

        if self.actions_remaining > 0:
            self.available_actions = action_getter.get_actions(self)
            if not self.available_actions:
                self.actions_remaining = 0

    def initialize_turn(self):
        initializer.initialize_turn(self)

    def initialize_action(self):
        initializer.initialize_action(self)

    def get_actions(self):
        if hasattr(self.players[0], "extra_action"):
            actions = action_getter.get_extra_actions(self)
        elif self.actions_remaining == 1 and hasattr(self, "available_actions"):
            actions = self.available_actions
        else:
            actions = action_getter.get_actions(self)

        for action in actions:
            if action.is_attack:
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

    def set_ais(self):
        if self.players[0].ai_name != "Human":
            self.players[0].ai = ai_module.AI(self.players[0].ai_name)
        else:
            self.players[0].ai = "Human"

        if self.players[1].ai_name != "Human":
            self.players[1].ai = ai_module.AI(self.players[1].ai_name)
        else:
            self.players[1].ai = "Human"

    def set_available_actions(self):
        self.available_actions = self.get_actions()

    def turn_shift(self):
        if self.players[0].color == "Green":
            self.turn += 1
        self.units = [self.units[1], self.units[0]]
        self.players = [self.players[1], self.players[0]]
        self.initialize_turn()
        self.initialize_action()
        self.set_available_actions()

    def current_player(self):
        return self.players[0]

    def opponent_player(self):
        return self.players[1]

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

    def shift_turn_if_done(self, all_actions=None):
        if all_actions is None:
            all_actions = self.get_actions()
        if (self.actions_remaining < 1 or len(all_actions) == 1) and not hasattr(self.players[0], "extra_action"):
            self.turn_shift()

    @classmethod
    def from_document(cls, document):
        player1 = Player("Green")
        player1.ai_name = document["player1_intelligence"]
        player1.ai = cls.get_ai_from_name(player1.ai_name)

        player2 = Player("Red")
        player2.ai_name = document["player2_intelligence"]
        player2.ai = cls.get_ai_from_name(player2.ai_name)

        return cls(player1,
                   cls.units_from_document(document["player1_units"]),
                   player2,
                   cls.units_from_document(document["player2_units"]),
                   document["turn"],
                   document["actions_remaining"],
                   document["extra_action"],
                   document["created_at"])

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
                if attribute == "experience":
                    unit.xp = int(unit_document[attribute])

            units[position] = unit

        return units

    @classmethod
    def get_ai_from_name(cls, name):
        if name == "Human":
            return name
        else:
            return ai_module.AI(name)

    def to_document(self):
        player1_units = self.get_units_dict(self.units[0])
        player2_units = self.get_units_dict(self.units[1])

        return {
            "player1_intelligence": self.players[0].ai_name,
            "player1_units": player1_units,
            "player2_intelligence": self.players[1].ai_name,
            "player2_units": player2_units,
            "turn": self.turn,
            "extra_action": self.has_extra_action,
            "actions_remaining": self.actions_remaining,
            "created_at": self.start_time
        }

    def get_units_dict(self, units):
        units_dict = dict()
        for unit_position in units.keys():
            unit = units[unit_position]

            unit_dict = dict()
            if unit.xp:
                unit_dict["experience"] = unit.xp
            if hasattr(unit, "blue_counters"):
                unit_dict["blue_counters"] = unit.blue_counters
            if hasattr(unit, "yellow_counters"):
                unit_dict["yellow_counters"] = unit.yellow_counters

            easy_position = units_module.get_position_string(unit_position)
            if len(unit_dict) > 0:
                unit_dict["name"] = unit.name
                units_dict[easy_position] = unit_dict
            else:
                units_dict[easy_position] = unit.name

        return units_dict


def save_gamestate(gamestate):
    return saver.save_gamestate(gamestate)


def load_gamestate(saved_gamestate):
    return saver.load_gamestate(saved_gamestate)
