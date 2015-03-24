import battle
import action_doer
import initializer
import action_getter
from units import Unit_class
import json
from common import *
from board import Board


class Gamestate:
    def __init__(self,
                 player1_units,
                 player2_units,
                 actions_remaining,
                 created_at=None,
                 game_id=None,
                 ai_factors=None):
        self.board = Board([player1_units, player2_units])
        self.actions_remaining = actions_remaining
        self.action_count = 0
        self.created_at = created_at
        self.game_id = game_id
        self.available_actions = []
        if ai_factors:
            self.ai_factors = ai_factors
        else:
            self.ai_factors = {}

    def all_units(self):
        return self.board.all_units()

    def do_action(self, action, outcome):
        action_doer.do_action(self, action, outcome)
        self.action_count += 1

        has_available_actions = self.actions_remaining > 0 or action.unit.has(State.extra_action)
        is_move_with_attack_possible = self.is_post_move_with_attack_possible(action, outcome)
        is_move_attack_decided = action.move_with_attack in [True, False] or not is_move_with_attack_possible

        if is_move_attack_decided and has_available_actions:
            self.set_available_actions()
            self.decrement_actions_if_none_available(action)

    def decrement_actions_if_none_available(self, action):
        if not self.available_actions:
            if action.unit.has(State.extra_action):
                action.unit.remove(State.extra_action)
                action.unit.remove(State.movement_remaining)
                self.set_available_actions()
            else:
                self.actions_remaining = 0

    def initialize_turn(self):
        initializer.initialize_turn(self)

    def get_actions(self, positions=None):
        if not positions:
            return self.available_actions

        return [action for action in self.available_actions if all(getattr(action, key) == value for
                                                                   key, value in positions.items())]

    def get_actions_with_move_with_attack_as_none(self, positions=None):

        actions = action_getter.get_actions(self)
        if positions:
            actions = [action for action in actions if all(getattr(action, key) == value for key, value in positions.items())]
        actions_with_none = []
        for action in actions:
            if action.is_attack:
                if not action.move_with_attack:
                    action.move_with_attack = None
                    actions_with_none.append(action)
            else:
                actions_with_none.append(action)
        return actions_with_none

    def get_actions_including_move_with_attack_none(self, positions=None):
        return self.get_actions(positions) + self.get_actions_with_move_with_attack_as_none(positions)

    def copy(self):
        return self.from_document(self.to_document())

    def set_available_actions(self):
        self.available_actions = action_getter.get_actions(self)

    @property
    def player_units(self):
        return self.board.player_units

    @property
    def enemy_units(self):
        return self.board.enemy_units

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
        ai_factors = document["ai_factors"] if "ai_factors" in document else None
        created_at = document["created_at"] if "created_at" in document else None

        return cls(player1_units, player2_units, actions_remaining, created_at, ai_factors=ai_factors)

    @classmethod
    def from_file(cls, path):
        document = json.loads(open(path).read())
        return Gamestate.from_document(document)

    @classmethod
    def units_from_document(cls, document):
        units = {}
        for position_string, unit_document in document.items():
            position = Position.from_string(position_string)

            if type(unit_document) is str:
                unit = Unit_class.make(Unit[unit_document.replace(" ", "_")])
            else:
                unit = Unit_class.make(Unit[unit_document["name"].replace(" ", "_")])

                for attribute_name, number in unit_document.items():
                    if type(number) is bool:
                        number = int(number)
                    if attribute_name != "name":
                        attribute, attributes = get_attribute_from_document(attribute_name, number)
                        unit.attributes[attribute] = attributes
            units[position] = unit

        return units

    @classmethod
    def get_ai_from_name(cls, name):
        if name == "Human":
            return name
        else:
            return ai_module.AI(name)

    def to_document(self):
        document = {
            "actions_remaining": self.actions_remaining,
            "player1_units": {str(position): unit.to_document() for (position, unit) in self.board.units[0].items()},
            "player2_units": {str(position): unit.to_document() for (position, unit) in self.board.units[1].items()}
        }
        if self.created_at:
            document["created_at"] = self.created_at
        if self.game_id:
            document["game"] = self.game_id
        if self.ai_factors:
            document["ai_factors"] = self.ai_factors

        return document

    def is_turn_done(self):
        return self.actions_remaining < 1 and not self.is_extra_action()

    def shift_turn(self):
        self.flip_all_units()
        self.board.units = self.board.units[::-1]
        self.initialize_turn()

    def move_melee_unit_to_target_tile(self, action):
        self.move_unit(action.end_at, action.target_at)
        self.set_available_actions()

        self.decrement_actions_if_none_available(action)

    def __str__(self):
        return document_to_string(self.to_document())

    def flip_all_units(self):
        self.board.flip_all_units()

    def __eq__(self, other):
        return self.to_document() == other.to_document()

    def is_ended(self):
        return self.board.is_ended()

    def get_unit_from_action_document(self, action_document):
        unit_position = Position.from_string(action_document["end_at"])

        if unit_position not in self.all_units():
            unit_position = Position.from_string(action_document["target_at"])

        if unit_position in self.player_units:
            return self.player_units[unit_position], unit_position
        elif unit_position in self.enemy_units:
            return self.enemy_units[unit_position], unit_position
        else:
            return None, None

    def is_extra_action(self):
        return self.board.is_extra_action()

    def get_upgradeable_unit(self):
        return self.board.get_upgradeable_unit()

    def is_post_move_with_attack_possible(self, action, outcome):
        if not action.is_attack or not action.unit.is_melee:
            return False

        rolls = outcome.for_position(action.target_at)
        push_possible = action.is_push and battle.attack_successful(action, rolls, self)

        if not action.unit.get_state(State.movement_remaining):
            return False

        return push_possible or battle.is_win(action, rolls, self)

    def delete_unit_at(self, position):
        self.board.delete_unit_at(position)

    def move_unit(self, start_position, end_position):
        self.board.move_unit(start_position, end_position)

    def change_unit_owner(self, position):
        self.board.change_unit_owner(position)
