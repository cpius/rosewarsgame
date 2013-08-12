from __future__ import division
import action_doer
import initializer
import action_getter
import ai_module
import units as units_module
import json
from common import *
from action import Action
from outcome import Outcome


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
        self.action_count = 0
        self.created_at = created_at

    @classmethod
    def from_log_document(cls, log_document):
        gamestate_document = log_document["initial_gamestate"]
        gamestate = cls.from_document(gamestate_document)
        action_count = int(log_document["action_count"])

        for action_number in range(1, action_count + 1):
            if gamestate.is_turn_done():
                gamestate.shift_turn()

            if not str(action_number) in log_document:
                # This happens when loading replays that are continuations of other replays
                continue

            action_document = log_document[str(action_number)]

            action = Action.from_document(gamestate.all_units(), action_document)

            outcome = None
            if action.is_attack():
                outcome_document = log_document[str(action_number) + "_outcome"]
                outcome = Outcome.from_document(outcome_document)
                if str(action_number) + "_options" in log_document:
                    options = log_document[str(action_number) + "_options"]
                    if "move_with_attack" in options:
                        action.move_with_attack = bool(options["move_with_attack"])

            gamestate.do_action(action, outcome)

        return gamestate

    def all_units(self):
        all_units = self.units[0].copy()
        all_units.update(self.units[1])
        return all_units

    def do_action(self, action, outcome):
        action_doer.do_action(self, action, outcome)
        self.action_count += 1

        if self.actions_remaining > 0 or self.extra_action:
            self.available_actions = action_getter.get_actions(self)
            if not self.available_actions:
                self.actions_remaining = 0

    def initialize_turn(self):
        initializer.initialize_turn(self)

    def get_actions(self):
        return self.available_actions

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
        self.available_actions = action_getter.get_actions(self)

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
                name = unit_document.replace(" ", "_")
                unit_class = getattr(units_module, name)
                unit = unit_class()
                units[position] = unit
                unit.constants = unit.constants.copy()

            else:
                unit_name = unit_document["name"].replace(" ", "_")
                unit = getattr(units_module, unit_name)()
                unit.constants = unit.constants.copy()

                for attribute, value in unit_document.items():
                    if attribute == "zoc":
                        unit.zoc = {getattr(Type, unit_type) for unit_type in unit_document["zoc"]}
                    elif attribute in constant_traits:
                        attr = getattr(Trait, attribute)
                        unit.constants[attr] = value

                    elif attribute in ability_descriptions:
                        attr = getattr(Ability, attribute)
                        if hasattr(unit, "constants"):
                            unit.constants[attr] = value
                        else:
                            unit.constants = {attr: value}

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

            base_unit = getattr(units_module, unit.name.replace(" ", "_"))()
            document_constants = [attribute for attribute in unit.constants if attribute not in base_unit.constants]

            if document_variables or document_constants:
                unit_dict = {}
                for attribute in document_variables:
                    unit_dict[Trait.name[attribute]] = unit.variables[attribute]
                for attribute in document_constants:
                    unit_dict[Trait.name[attribute]] = unit.constants[attribute]
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

    def move_melee_unit_to_target_tile(self, action):
        action_doer.move_melee_unit_to_target_tile(self, action)

    def __str__(self):
        return document_to_string(self.to_document())

    def flip_units(self):
        self.units = [dict((position.flip(), unit) for position, unit in self.units[0].items()),
                      dict((position.flip(), unit) for position, unit in self.units[1].items())]

    def __eq__(self, other):
        return self.to_document() == other.to_document()

    def is_ended(self):
        backline = 8
        for position, unit in self.player_units.items():
            if not unit.is_bribed():
                if position.row == backline:
                    return True

        if not self.enemy_units:
            at_least_one_bribed = False
            for unit in self.player_units:
                if unit.is_bribed():
                    at_least_one_bribed = True
            if not at_least_one_bribed:
                return True

        return False
