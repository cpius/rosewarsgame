from datetime import datetime
from copy import copy
from common import *


class Action(object):
    def __init__(self,
                 units,
                 start_at,
                 end_at=None,
                 target_at=None,
                 move_with_attack=False,
                 ability=None,
                 action_number=None,
                 outcome=SubOutcome.UNKNOWN,
                 created_at=None):

        # The tile the unit starts it's action on
        self.start_at = start_at

        # If the action is a movement, the tile the unit ends its movement on.
        # If the action is an attack, tile the unit stops at while attacking an adjacent tile.
        self.end_at = end_at if end_at else start_at

        # The tile a unit attacks or affects with an ability
        self.target_at = target_at

        self.move_with_attack = move_with_attack
        self.ability = ability
        self.action_number = action_number

        # The tile a unit ends up at after attacks are resolved
        self.final_position = self.end_at

        self.created_at = created_at if created_at else datetime.utcnow()

        self.unit = units[self.start_at]
        if self.target_at and self.target_at in units:
            self.target_unit = units[self.target_at]

        self.outcome = outcome

    @classmethod
    def from_document(cls, units, document):
        document_copy = copy(document)

        meta_attributes = ["created_at", "game", "_id"]
        for attribute in meta_attributes:
            if attribute in document_copy:
                del document_copy[attribute]

        for attribute in ["start_at", "end_at", "target_at"]:
            if attribute in document_copy:
                document_copy[attribute] = Position.from_string(document_copy[attribute])

        start_at = document_copy["start_at"]
        end_at = document_copy["end_at"]

        target_at = None
        if "target_at" in document_copy:
            target_at = document_copy["target_at"]

        move_with_attack = False
        if "move_with_attack" in document_copy:
            move_with_attack = bool(document["move_with_attack"])

        ability = None
        if "ability" in document_copy:
            ability = getattr(Ability, document_copy["ability"])

        created_at = None
        if "created_at" in document_copy:
            created_at = document_copy["created_at"]

        action_number = None
        if "action_number" in document_copy:
            action_number = int(document_copy["action_number"])

        return cls(units, start_at, end_at, target_at, move_with_attack, ability, action_number=action_number, created_at=created_at)

    def __repr__(self):
        return document_to_string(self.to_document_no_created_at())

    def __eq__(self, other):
        basic_attributes = ["start_at", "end_at", "target_at", "move_with_attack", "ability"]
        original = dict((attr, self.__dict__[attr]) for attr in basic_attributes if self.__dict__[attr])
        other = dict((attr, other.__dict__[attr]) for attr in basic_attributes if other.__dict__[attr])

        return original == other

    def __ne__(self, other):
        return not self.__eq__(other)

    def to_document_no_created_at(self):
        attrs = ["action_number", "start_at", "end_at", "target_at", "ability"]
        return dict((attr, str(getattr(self, attr))) for attr in attrs if getattr(self, attr))

    def to_document(self):
        attrs = ["action_number", "start_at", "end_at", "target_at", "ability", "created_at"]
        return dict((attr, str(getattr(self, attr))) for attr in attrs if getattr(self, attr))

    def is_move_with_attack(self):
        return self.move_with_attack

    def ensure_outcome(self, outcome):
        self.final_position = self.end_at

        if outcome:
            self.rolls = (1, 6)
        else:
            self.rolls = (6, 1)

        return self

    def is_attack(self):
        return bool(self.target_at) and not self.ability

    def is_ability(self):
        return bool(self.ability)

    def is_lancing(self):
        return self.unit.has(Trait.lancing) and self.is_attack() and self.distance_to_target() >= 3

    def is_lancing_II(self):
        return self.unit.has(Trait.lancing_II) and self.is_attack() and self.distance_to_target() >= 4

    def is_push(self):
        return self.unit.has(Trait.push) and self.is_attack()

    def is_crusading(self, units):
        return any(unit for unit in surrounding_friendly_units(self.start_at, units) if unit.has(Trait.crusading))

    def is_crusading_II_attack(self, units):
        return any(unit for unit in surrounding_friendly_units(self.start_at, units) if unit.has(Trait.crusading_II))

    def is_crusading_II_defence(self, units):
        return any(unit for unit in surrounding_friendly_units(self.target_at, units) if unit.has(Trait.crusading_II))

    def has_high_morale(self, units):
        return any(pos for pos in adjacent_friendly_positions(self.end_at, units) if
                   pos != self.start_at and units[pos].has(Trait.flag_bearing))

    def has_high_morale_II_A(self, units):
        return any(unit for unit in surrounding_friendly_units(self.end_at, units)
                   if unit.has(Trait.flag_bearing_II_A))

    def has_high_morale_II_B(self, units):
        return any(unit for unit in adjacent_friendly_units(self.end_at, units) if unit.has(Trait.flag_bearing_II_B))

    def distance_to_target(self):
        return distance(self.start_at, self.target_at)

    def is_triple_attack(self):
        return self.unit.has(Trait.triple_attack) and self.is_attack()

    def double_cost(self):
        return self.unit.has(Trait.double_attack_cost) and self.is_attack()
