from datetime import datetime
from copy import copy, deepcopy
from common import *
import battle


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
            representation += " " + Ability.name[self.ability]
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
            document["ability"] = Ability.name[self.ability]
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

    def lancing(self):
        if self.unit.has(Trait.lancing, 1) and self.is_attack() and self.distance_to_target() >= 3:
            return 2
        elif self.unit.has(Trait.lancing, 2) and self.is_attack() and self.distance_to_target() >= 4:
            return 3
        else:
            return 0

    def flanking(self):
        if not self.unit.has(Trait.flanking) or self.target_unit.has(Trait.flanked):
            return False
        attack_direction = self.end_at.get_direction_to(self.target_at)
        if attack_direction == Direction("Up"):
            return False

        return True

    def is_push(self):
        return self.unit.has(Trait.push) and self.is_attack()

    def is_crusading_attack(self, units, level=None):
        return self.unit.is_melee() and (self.is_surrounding_unit_with(units, Trait.crusading, self.start_at, level))

    def is_crusading_defense(self, units, level=None):
        return self.unit.is_melee() and (self.is_surrounding_unit_with(units, Trait.crusading, self.target_at, level))

    def has_high_morale(self, units):
        return self.unit.is_melee() and (self.is_adjacent_unit_with(units, Trait.flag_bearing, self.end_at) or
                                         self.is_surrounding_unit_with(units, Trait.flag_bearing, self.end_at, 2))

    def is_surrounding_unit_with(self, units, trait, position, level=None):
        return any(unit_with_trait_at(pos, trait, units, level) for pos in position.surrounding_tiles() if
                   pos != self.start_at)

    def is_adjacent_unit_with(self, units, trait, position, level=None):
        return any(unit_with_trait_at(pos, trait, units, level) for pos in position.adjacent_tiles() if
                   pos != self.start_at)

    def distance_to_target(self):
        return distance(self.start_at, self.target_at)

    def is_javelin_throw(self):
        return self.unit.has_javelin() and distance(self.end_at, self.target_at) > 1

    def double_cost(self):
        return self.unit.has(Trait.double_attack_cost) and self.is_attack()

    def get_attack(self, gamestate):
        if not hasattr(self, "attack"):
            self.attack = battle.get_attack(self, gamestate)
        return self.attack

    def get_defence(self, gamestate):
        if not hasattr(self, "defence"):
            attack = self.get_attack(gamestate)
            self.defence = battle.get_defence(self, attack, gamestate)
        return self.defence

    def attack_successful(self, rolls, gamestate):
        return rolls.attack <= self.get_attack(gamestate)

    def defence_successful(self, rolls, gamestate):
        return rolls.defence <= self.get_defence(gamestate)

    def is_win(self, rolls, gamestate):
        return self.attack_successful(rolls, gamestate) and not self.defence_successful(rolls, gamestate)

    def is_miss(self, rolls, gamestate):
        return not self.attack_successful(rolls, gamestate)

    def outcome_string(self, rolls, gamestate):
        if not self.is_attack() or not rolls:
            return ""
        elif self.is_miss(rolls, gamestate):
            return "Miss"
        elif self.is_win(rolls, gamestate):
            return "Win"
        else:
            return "Defend"

    def copy(self):
        return deepcopy(self)

    def update_references(self, gamestate):
        units = merge_units(gamestate.player_units, gamestate.enemy_units)
        self.unit = units[self.start_at]
        if self.target_at and self.target_at in units:
            self.target_unit = units[self.target_at]
