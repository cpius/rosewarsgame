from __future__ import division
import action_doer
import initializer
import action_getter
import ai_module
import ai_methods
import units as units_module
import json
from common import *
from pprint import PrettyPrinter


class Gamestate:
    
    def __init__(self,
                 player1_units,
                 player2_units,
                 actions_remaining,
                 extra_action=False,
                 created_at=None):
        self.units = [player1_units, player2_units]
        self.actions_remaining = actions_remaining
        self.extra_action = extra_action
        self.action_number = 0
        self.created_at = created_at

    def all_units(self):
        all_units = self.units[0].copy()
        all_units.update(self.units[1])
        return all_units

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

    def get_actions(self):
        if getattr(self, "extra_action"):
            actions = action_getter.get_extra_actions(self)
        elif self.actions_remaining == 1 and hasattr(self, "available_actions"):
            actions = self.available_actions
        else:
            actions = action_getter.get_actions(self)

        for action in actions:
            if action.is_attack():
                action.chance_of_win = ai_methods.chance_of_win(self, action.unit, action.target_unit, action)

        return actions

    def copy(self):
        gamestate_document = self.to_document()
        return self.from_document(gamestate_document)

    def __eq__(self, other):
        pass

    def set_network_player(self, local_player):
        for player in range(2):
            if self.players[player].player_id != local_player:
                self.players[player].ai_name = "Network"
                self.players[player].ai = "Network"

    def set_available_actions(self):
        self.available_actions = self.get_actions()

    @property
    def player_units(self):
        return self.units[0]

    @property
    def enemy_units(self):
        return self.units[1]

    def get_actions_remaining(self):
        return self.actions_remaining

    def set_actions_remaining(self, actions_remaining):
        self.actions_remaining = actions_remaining

    def decrement_actions_remaining(self):
        self.actions_remaining -= 1

    @classmethod
    def from_document(cls, document):
        player1_units = cls.units_from_document(document["player1_units"])
        player2_units = cls.units_from_document(document["player2_units"])
        actions_remaining = document["actions_remaining"]
        if "extra_action" in document:
            extra_action = document["extra_action"]
        else:
            extra_action = False
        if "created_at" in document:
            created_at = document["created_at"]
        else:
            created_at = None
        return cls(player1_units, player2_units, actions_remaining, extra_action, created_at)

    @classmethod
    def from_file(cls, path):
        document = json.loads(open(path).read())
        return Gamestate.from_document(document)

    @classmethod
    def units_from_document(cls, document):
        units = {}
        for position_string, unit_document in document.items():
            position = Position.from_string(position_string)

            if isinstance(unit_document, basestring):
                units[position] = getattr(units_module, unit_document.replace(" ", "_"))()
            else:
                unit = getattr(units_module, unit_document["name"].replace(" ", "_"))()
                for attribute, value in unit_document.items():
                    if attribute == "zoc":
                        unit.zoc = {getattr(Type, type) for type in unit_document["zoc"]}
                    elif attribute != "name":
                        attr = getattr(Trait, attribute)
                        unit.variables[attr] = value

                units[position] = unit

        return units

    @classmethod
    def get_ai_from_name(cls, name):
        if name == "Human":
            return name
        else:
            return ai_module.AI(name)

    def to_document(self):
        document = {attribute: getattr(self, attribute) for attribute in ["extra_action", "created_at",
                                                                          "actions_remaining"]
                    if hasattr(self, attribute) and (getattr(self, attribute) or attribute == "actions_remaining")}
        document["player1_units"] = self.get_units_dict(self.units[0])
        document["player2_units"] = self.get_units_dict(self.units[1])
        return document

    def get_units_dict(self, units):
        units_dict = dict()
        for unit_position, unit in units.items():
            position = str(unit_position)

            document_variables = [attribute for attribute, value in unit.variables.items() if value]
            if document_variables:
                unit_dict = {Trait.reverse_mapping[attribute]: unit.variables[attribute] for attribute in document_variables}
                unit_dict["name"] = unit.name
                units_dict[position] = unit_dict
            else:
                units_dict[position] = unit.name

        return units_dict

    def is_turn_done(self):
        return self.actions_remaining < 1 and not getattr(self, "extra_action")

    def shift_turn(self):
        self.flip_units()
        self.units = self.units[::-1]
        self.initialize_turn()
        #self.set_available_actions()

    def update_final_position(self, action):
        action_doer.update_final_position(action)
        action_doer.update_unit_to_final_position(self, action)

    def __str__(self):
        pp = PrettyPrinter()
        return str(pp.pprint(self.to_document()))

    def flip_units(self):
        self.units = [dict((position.flip(), unit) for position, unit in self.units[0].items()),
                      dict((position.flip(), unit) for position, unit in self.units[1].items())]

    def __eq__(self, other):
        return self.to_document() == other.to_document()
