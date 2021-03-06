import gamestate.battle as battle
import gamestate.action_doer as action_doer
import gamestate.initializer as initializer
import gamestate.action_getter as action_getter
from gamestate.units import base_units
import json
from gamestate.gamestate_library import *
from gamestate.board import Board
from game.game_library import document_to_string
from gamestate.action import Action


class Gamestate:
    def __init__(self,
                 player1_units,
                 player2_units,
                 actions_remaining,
                 created_at=None,
                 game_id=None):
        self.board = Board([player1_units, player2_units])
        self.actions_remaining = actions_remaining
        self.action_count = 0
        self.created_at = created_at
        self.game_id = game_id
        self.available_actions = []
        self.bonus_tiles = {}

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
        return filter_actions(self.available_actions, positions)

    def get_actions_including_pass_extra(self, positions=None):
        actions = filter_actions(self.available_actions, positions)
        if self.is_extra_action():
            for position, unit in self.player_units.items():
                actions.add(Action(self.player_units, position, position))
        return actions

    def get_actions_with_move_with_attack_as_none(self):

        actions_with_none = set()
        for action in action_getter.get_actions(self):
            if action.is_attack:
                if not action.move_with_attack:
                    action.move_with_attack = None
                    actions_with_none.add(action)
            else:
                actions_with_none.add(action)
        return actions_with_none

    def get_actions_including_move_with_attack_none(self):
        return self.get_actions() | self.get_actions_with_move_with_attack_as_none()

    def copy(self):
        return self.from_document(self.to_document())

    def set_available_actions(self):
        self.available_actions = action_getter.get_actions(self)
        self.bonus_tiles = action_getter.get_bonus_tiles(self)

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
        created_at = document["created_at"] if "created_at" in document else None

        return cls(player1_units, player2_units, actions_remaining, created_at)

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
                unit_class = base_units[Unit[unit_document.replace(" ", "_")]]
                unit = unit_class()

            else:
                unit_class = base_units[Unit[unit_document["name"].replace(" ", "_")]]
                unit = unit_class()

                for attribute_name, number in unit_document.items():
                    if type(number) is bool:
                        number = int(number)
                    if attribute_name != "name":
                        attribute, attributes = get_attribute_from_document(attribute_name, number)
                        unit.attributes[attribute] = attributes
            units[position] = unit

        return units

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

        return document

    def is_turn_done(self):
        return self.actions_remaining < 1 and not self.is_extra_action()

    def shift_turn(self):
        self.flip_all_units()
        self.board.units = self.board.units[::-1]
        self.initialize_turn()

    def move_melee_unit_to_target_tile(self, action):
        self.move_unit(action.end_at, action.target_at)
        if not action.unit.has(Trait.swiftness):
            action.unit.remove(State.movement_remaining)
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

        action_copy = action.copy()
        action_copy.move_with_attack = True
        if action_copy not in self.get_actions():
            return False

        if not action.is_attack or not action.unit.is_melee:
            return False

        rolls = outcome.for_position(action.target_at)
        push_possible = action.is_push and battle.attack_successful(action, rolls, self)

        if self.is_extra_action() and not action.unit.get(State.movement_remaining):
            return False

        return push_possible or battle.is_win(action, rolls, self)

    def delete_unit_at(self, position):
        self.board.delete_unit_at(position)

    def move_unit(self, start_position, end_position):
        self.board.move_unit(start_position, end_position)

    def change_unit_owner(self, position):
        self.board.change_unit_owner(position)

    def pass_extra_action(self):
        self.board.pass_extra_action()

    def copy(self):
        return Gamestate.from_document(self.to_document())
