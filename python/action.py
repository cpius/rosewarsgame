from datetime import datetime
from copy import copy
from common import *
import battle


class Action(object):
    def __init__(self,
                 units,
                 start_at,
                 end_at=None,
                 target_at=None,
                 move_with_attack=None,
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
        self.ability = ability
        self.number = number

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
        if "action" in document_copy:
            number = int(document_copy["number"])

        return cls(units, start_at, end_at, target_at, move_with_attack, ability, number=number, created_at=created_at)

    def __repr__(self):
        representation = self.unit.name + " on " + str(self.start_at)
        if self.end_at != self.start_at:
            representation += " move to " + str(self.end_at)
        if self.ability:
            representation += " ability on " + self.target_unit.name + " on " + str(self.target_at)
        elif self.is_attack() and self.move_with_attack:
            representation += " attack-move " + self.target_unit.name + " on " + str(self.target_at)
        elif self.is_attack():
            if hasattr(self, "target_unit"):
                target = self.target_unit.name
            else:
                target = "unit"
            representation += " attack " + target + " on " + str(self.target_at)

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
        attrs = ["number", "start_at", "end_at", "target_at", "ability", "created_at"]
        document = dict((attr, str(getattr(self, attr))) for attr in attrs if getattr(self, attr))
        if not self.move_with_attack is None:
            document["move_with_attack"] = self.move_with_attack

        return document

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

    def double_cost(self):
        return self.unit.has(Trait.double_attack_cost) and self.is_attack()

    def is_successful(self, rolls, gamestate):
        if not self.is_attack():
            return True
        attack_successful = battle.attack_successful(self, rolls, gamestate)
        if not attack_successful:
            return False
        defence_successful = battle.defence_successful(self, rolls, gamestate)
        return not defence_successful

    def is_failure(self, rolls, gamestate):
        if not rolls:
            return False

        return not self.is_successful(rolls, gamestate)

    def is_miss(self, rolls, gamestate):
        return not battle.attack_successful(self, rolls, gamestate)

    def outcome_string(self, rolls, gamestate):
        if not self.is_attack() or not rolls:
            return ""

        if self.is_miss(rolls, gamestate):
            return "Miss"

        if self.is_successful(rolls, gamestate):
            return "Win"

        return "Defend"

    def copy(self):
        return copy(self)
