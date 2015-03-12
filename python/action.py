from datetime import datetime
from copy import copy, deepcopy
from common import *


class Action(object):
    def __init__(self,
                 units,
                 start_at,
                 end_at=None,
                 target_at=None,
                 move_with_attack=False,
                 ability=None,
                 number=None,
                 outcome=None,
                 created_at=None):

        # The tile the unit starts it's action on
        self.start_at = start_at

        # If the action is a movement, the tile the unit ends its movement on.
        # If the action is an attack, tile the unit stops at while attacking an adjacent tile.
        self.end_at = end_at if end_at else start_at

        # The tile a unit attacks or affects with an ability
        self.target_at = target_at

        self.move_with_attack = move_with_attack
        self.number = number
        self.ability = ability
        self.outcome = outcome

        self.created_at = created_at if created_at else datetime.utcnow()

        if self.target_at and self.target_at in units:
            self.target_unit = units[self.target_at]

        self.unit = units[self.start_at]

        is_move_with_attack_feasible = self.is_attack() and self.unit.is_melee()
        if self.move_with_attack is None and not is_move_with_attack_feasible:
            self.move_with_attack = False

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

        move_with_attack = None
        if "move_with_attack" in document_copy:
            move_with_attack = bool(document["move_with_attack"])

        ability = None
        if "ability" in document_copy:
            ability = getattr(Ability, document_copy["ability"])

        created_at = None
        if "created_at" in document_copy:
            created_at = document_copy["created_at"]

        number = None
        if "number" in document_copy:
            number = int(document_copy["number"])

        return cls(units, start_at, end_at, target_at, move_with_attack, ability, number=number, created_at=created_at)

    def __repr__(self):
        representation = str(self.unit) + " on " + str(self.start_at)
        if self.end_at != self.start_at:
            representation += " move to " + str(self.end_at)
        if self.ability:
            representation += " " + self.ability.name
            representation += " " + str(self.target_unit) + " on " + str(self.target_at)
        elif self.is_attack() and self.move_with_attack:
            representation += " attack-move " + str(self.target_unit) + " on " + str(self.target_at)
        elif self.is_attack():
            if hasattr(self, "target_unit"):
                target = str(self.target_unit)
            else:
                target = "unit"
            representation += " attack " + target + " on " + str(self.target_at)
            if self.move_with_attack is None:
                representation += ", unknown if move with attack"

        return representation

    def __eq__(self, other1):

        basic_attributes = ["start_at", "end_at", "target_at", "move_with_attack", "ability"]
        original = dict((attr, self.__dict__[attr]) for attr in basic_attributes if self.__dict__[attr] is not None)
        other = dict((attr, other1.__dict__[attr]) for attr in basic_attributes if other1.__dict__[attr] is not None)

        return original == other

    def __ne__(self, other):
        return not self.__eq__(other)

    def to_document_no_created_at(self):
        document = self.to_document()
        if "created_at" in document:
            del document["created_at"]
        return document

    def to_document(self):
        attributes = ["start_at", "end_at", "target_at"]
        document = dict((attribute, str(getattr(self, attribute)))
                        for attribute in attributes if getattr(self, attribute))
        if self.created_at:
            document["created_at"] = self.created_at
        if self.number:
            document["number"] = self.number
        if self.ability:
            document["ability"] = self.ability.name
        if not self.move_with_attack is None:
            document["move_with_attack"] = self.move_with_attack

        return document

    def to_network(self, action_count):
        if not self.number:
            self.number = action_count + 1
        document = self.to_document()
        document["type"] = "action"

        return document

    def is_attack(self):
        return bool(self.target_at) and not self.ability

    def is_ability(self):
        return bool(self.ability)

    def is_push(self):
        return self.unit.has(Trait.push) and self.is_attack()

    def is_javelin_throw(self):
        return self.unit.has_javelin() and distance(self.end_at, self.target_at) > 1

    def double_cost(self):
        return self.unit.has(Trait.double_attack_cost) and self.is_attack()

    def copy(self):
        return deepcopy(self)

    def update_references(self, gamestate):
        units = merge_units(gamestate.player_units, gamestate.enemy_units)
        self.unit = units[self.start_at]
        if self.target_at and self.target_at in units:
            self.target_unit = units[self.target_at]

    def has_outcome(self):
        return self.is_attack() or self.ability == Ability.assassinate
