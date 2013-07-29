from datetime import datetime
from copy import copy
from common import *


class Action(object):
    def __init__(self,
                 start_position,
                 end_position=None,
                 attack_position=None,
                 ability_position=None,
                 move_with_attack=MoveOrStay.UNKNOWN,
                 ability=None,
                 action_number=None,
                 outcome=True,
                 created_at=None):
        self.start_position = start_position  # The tile the unit starts it's action on
        self.end_position = end_position if end_position else start_position  # If the action is a movement, the tile
        # the unit ends its movement on. If the action is an attack, tile the unit stops at while attacking an adjacent
        # tile.
        self.attack_position = attack_position  # The tile a unit attacks
        self.ability_position = ability_position
        self.move_with_attack = move_with_attack
        self.ability = ability
        self.action_number = action_number
        self.final_position = self.end_position  # The tile a unit ends up at after attacks are resolved
        self.created_at = created_at if created_at else datetime.utcnow()
        self.rolls = None
        self.outcome = outcome
        self.double_cost = False

    @classmethod
    def from_document(cls, document):
        document_copy = copy(document)

        meta_attributes = ["created_at", "game", "_id"]
        for attribute in meta_attributes:
            if attribute in document_copy:
                del document_copy[attribute]

        for attribute in ["start_position", "end_position", "attack_position", "ability_position"]:
            if attribute in document_copy:
                document_copy[attribute] = Position.from_string(document_copy[attribute])

        action = cls(**document_copy)

        if "created_at" in document:
            action.created_at = document["created_at"]

        if "move_with_attack" in document and isinstance(document["move_with_attack"], basestring):
            action.move_with_attack = getattr(MoveOrStay, document["move_with_attack"].upper())
        elif not action.is_attack():
            action.move_with_attack = MoveOrStay.STAY
        else:
            action.move_with_attack = MoveOrStay.UNKNOWN

        return action

    def __repr__(self):
        return document_to_string(self.to_document())

    def __eq__(self, other):
        basic_attributes = ["start_position", "end_position", "attack_position", "ability_position", "move_with_attack",
                            "ability"]
        original = dict((attr, self.__dict__[attr]) for attr in basic_attributes if self.__dict__[attr])
        other = dict((attr, other.__dict__[attr]) for attr in basic_attributes if other.__dict__[attr])

        return original == other

    def __ne__(self, other):
        return not self.__eq__(other)

    def to_document(self):
        d = {"action_number": self.action_number,
             "start_position": str(self.start_position),
             "end_position": str(self.end_position),
             "attack_position": str(self.attack_position),
             "ability_position": str(self.ability_position),
             "move_with_attack": self.move_with_attack,
             "ability": self.ability,
             "created_at": self.created_at}

        return dict((key, value) for key, value in d.items() if value and value != "None")

    def is_move_with_attack(self):
        return self.move_with_attack == MoveOrStay.MOVE

    def ensure_outcome(self, outcome):
        self.final_position = self.end_position

        if outcome:
            self.rolls = (1, 6)
        else:
            self.rolls = (6, 1)

        return self

    def is_attack(self):
        return bool(self.attack_position)

    def is_ability(self):
        return bool(self.ability)

    def is_lancing(self):
        return self.unit.has("lancing") and self.is_attack() and self.distance_to_target() >= 3

    def is_lancing_II(self):
        return self.unit.has("lancing_II") and self.is_attack() and self.distance_to_target() >= 4

    def is_push(self):
        return self.unit.has("push") and self.is_attack()

    def is_crusading(self, units):
        return any(unit for unit in surrounding_friendly_units(self.start_position, units) if unit.has("crusading"))

    def is_crusading_II_attack(self, units):
        return any(unit for unit in surrounding_friendly_units(self.start_position, units) if unit.has("crusading_II"))

    def is_crusading_II_defence(self, units):
        return any(unit for unit in surrounding_friendly_units(self.attack_position, units) if unit.has("crusading_II"))

    def has_high_morale(self, units):
        return any(pos for pos in adjacent_friendly_positions(self.end_position, units) if
                   pos != self.start_position and units[pos].has("flag_bearing"))

    def has_high_morale_II_A(self, units):
        return any(unit for unit in surrounding_friendly_units(self.end_position, units)
                   if unit.has("flag_bearing_II_A"))

    def has_high_morale_II_B(self, units):
        return any(unit for unit in adjacent_friendly_units(self.end_position, units) if unit.has("flag_bearing_II_B"))

    def distance_to_target(self):
        return distance(self.start_position, self.attack_position)

    def is_triple_attack(self):
        return self.unit.has("triple_attack") and self.is_attack()

    def add_references(self, gamestate):
        player_units = gamestate.player_units()
        enemy_units = gamestate.opponent_units()
        self.unit = player_units[self.start_position]
        if self.is_attack():
            self.target_unit = enemy_units[self.attack_position]
        elif self.is_ability():
            if self.ability_position in enemy_units:
                self.target_unit = enemy_units[self.ability_position]
            elif self.ability_position in player_units:
                self.target_unit = player_units[self.ability_position]
