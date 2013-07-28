import battle
import common
from datetime import datetime
from copy import copy


class MoveOrStay:
    UNKNOWN = 0
    MOVE = 1
    STAY = 2


class Action(object):
    def __init__(self,
                 start_position,
                 end_position=None,
                 attack_position=None,
                 ability_position=None,
                 move_with_attack=MoveOrStay.UNKNOWN,
                 ability="",
                 action_number=None,
                 sub_actions=None,
                 outcome=True,
                 created_at=None):
        self.start_position = start_position  # The tile the unit starts it's action on
        if not end_position:
            self.end_position = start_position
        else:
            self.end_position = end_position  # If the action is a movement, the tile the unit ends its movement on.
                                          # If the action is an attack, tile the unit stops at while attacking
                                          # an adjacent tile.
        self.attack_position = attack_position  # The tile a unit attacks
        self.ability_position = ability_position
        self.move_with_attack = move_with_attack
        self.ability = ability
        self.action_number = action_number
        self.sub_actions = sub_actions if sub_actions else []
        self.final_position = self.end_position  # The tile a unit ends up at after attacks are resolved
        self.created_at = created_at

        self.unit = None
        self.target = None
        self.unit_reference = None
        self.target_reference = None
        self.rolls = None
        self.outcome = outcome

        self.created_at = datetime.utcnow()

    @classmethod
    def from_document(cls, document):
        document_copy = copy(document)

        meta_attributes = ["created_at", "game", "_id"]
        for attribute in meta_attributes:
            if attribute in document_copy:
                del document_copy[attribute]

        for attribute in ["start_position", "end_position", "attack_position", "ability_position"]:
            if attribute in document_copy:
                document_copy[attribute] = common.position_to_tuple(document_copy[attribute])

        if "sub_actions" in document_copy:
            document_copy["sub_actions"] =\
                [cls.from_document(sub_action_document) for sub_action_document in document_copy["sub_actions"]]
        action = cls(**document_copy)
        if "created_at" in document:
            action.created_at = document["created_at"]
        return action

    @classmethod
    def from_document_simple(cls, document):
        document_copy = copy(document)

        simple_attributes = {"start_position", "end_position", "attack_position", "ability_position",
                             "move_with_attack", "ability", "sub_actions"}
        convert_attributes = {"start_position", "end_position", "attack_position", "ability_position"}

        read_attributes = set(attribute for attribute in simple_attributes if attribute in document and document[attribute])

        for attribute in convert_attributes & read_attributes:
            document_copy[attribute] = common.position_to_tuple(document_copy[attribute])

        if "sub_actions" in document_copy and document_copy["sub_actions"]:
            document_copy["sub_actions"] = [cls.from_document_simple(sub_action_document)
                                            for sub_action_document in document_copy["sub_actions"]]

        return cls(**document_copy)

    def attribute_representation(self):
        return str(self.__dict__)

    def get_simple_string(self):
        if self.unit:
            representation = self.unit.name
        elif self.unit_reference:
            representation = self.unit_reference.name
        else:
            representation = "Unit"

        if self.target_reference:
            target = self.target_reference.name
        else:
            target = "Unit"

        if self.start_position != self.end_position:
            representation += " move from " + common.position_to_string(self.start_position)
            representation += " to " + common.position_to_string(self.end_position)
            if self.is_attack():
                representation += " and"
        else:
            representation += " at " + common.position_to_string(self.start_position)

        if self.is_attack() and not self.is_move_with_attack():
            representation += " attack " + target + " " + common.position_to_string(self.attack_position)

        if self.is_attack() and self.is_move_with_attack():
            representation += " attack-move " + target + " " + common.position_to_string(self.attack_position)

        if self.is_ability():
            representation += " use " \
                              + self.ability\
                              + " on " \
                              + target \
                              + " " \
                              + common.position_to_string(self.ability_position)

        return representation

    def get_basic_string(self):
        representation = self.unit_reference.name

        if self.start_position != self.end_position:
            representation += " move from " + common.position_to_string(self.start_position)
            representation += " to " + common.position_to_string(self.end_position)
            if self.is_attack():
                representation += " and"
        else:
            representation += " at " + common.position_to_string(self.start_position)

        if self.is_attack() and self.move_with_attack != MoveOrStay.MOVE:
            representation += " attack " + self.target_reference.name + " " + common.position_to_string(self.attack_position)

        if self.is_attack() and self.move_with_attack == MoveOrStay.MOVE:
            representation += " attack-move " + self.target_reference.name + " " + common.position_to_string(self.attack_position)

        if self.is_ability():
            representation += " use "\
                              + self.ability\
                              + " on "\
                              + self.target_reference.name\
                              + " "\
                              + common.position_to_string(self.ability_position)

        return representation

    def get_battle_outcome_string(self):
        if self.outcome:
            return self.outcome
        else:
            return ""

    def get_full_battle_outcome_string(self):
        representation = ""
        if self.rolls:
            attack = battle.get_attack_rating(self.unit_reference, self.target_reference, self)
            defence = battle.get_defence_rating(self.unit_reference, self.target_reference, attack)

            representation += "Stats A: " + str(attack) + ", D: " + str(defence)
            representation += " Rolls A: " + str(self.rolls[0]) + " D: " + str(self.rolls[1])
            representation += ", " + self.outcome

        for sub_action in self.sub_actions:
            representation += "\n"
            representation += "and attack " + common.position_to_string(sub_action.attack_position)
            if sub_action.rolls:
                attack = battle.get_attack_rating(self.unit_reference, self.target_reference, self)
                defence = battle.get_defence_rating(self.unit_reference, self.target_reference, attack)

                representation += ", Stats A: " + str(attack) + ", D: " + str(defence)
                representation += " Rolls A: " + str(self.rolls[0]) + " D: " + str(self.rolls[1])
                representation += ", " + self.outcome

        return representation

    def __repr__(self):
        return self.get_simple_string()

    def full_string(self):
        return self.get_basic_string() + ", "\
                                       + self.get_battle_outcome_string() + "\n" \
                                       + self.get_full_battle_outcome_string()

    def string_with_outcome(self):
        return self.get_basic_string() + ", " + self.get_battle_outcome_string()

    def __eq__(self, other):
        basic_attributes = ["start_position",
                            "end_position",
                            "attack_position",
                            "ability_position",
                            "move_with_attack",
                            "ability"]
        original = dict((attribute, self.__dict__[attribute]) for attribute in basic_attributes)
        other = dict((attribute, other.__dict__[attribute]) for attribute in basic_attributes)

        return original == other

    def to_document(self):
        action_number = self.action_number if self.action_number else 0
        sub_action_docs = [sub_action.to_document() for sub_action in self.sub_actions]

        return {"action_number": action_number,
                "start_position": common.position_to_string(self.start_position),
                "end_position": common.position_to_string(self.end_position),
                "attack_position": common.position_to_string(self.attack_position),
                "ability_position": common.position_to_string(self.ability_position),
                "move_with_attack": self.move_with_attack,
                "ability": self.ability,
                "sub_actions": sub_action_docs,
                "created_at": self.created_at}

    def to_document_simple(self):
        sub_action_docs = [sub_action.to_document_simple() for sub_action in self.sub_actions]
        simple_attributes = {"start_position", "end_position", "attack_position", "ability_position",
                             "move_with_attack", "ability", "sub_actions"}
        convert_attributes = {"start_position", "end_position", "attack_position", "ability_position"}
        write_attributes = set(attribute for attribute in simple_attributes if getattr(self, attribute))
        document = {}
        for attribute in write_attributes & convert_attributes:
            document[attribute] = common.position_to_string(getattr(self, attribute))
        for attribute in write_attributes - convert_attributes:
            document[attribute] = getattr(self, attribute)
        if sub_action_docs:
            document["sub_actions"] = sub_action_docs
        return document

    def is_move_with_attack(self):
        return self.move_with_attack == MoveOrStay.MOVE

    def ensure_outcome(self, outcome):
        self.final_position = self.end_position

        if outcome:
            self.rolls = (1, 6)
        else:
            self.rolls = (6, 1)

        for sub_action in self.sub_actions:
            sub_action.rolls = self.rolls

        return self

    def is_attack(self):
        return bool(self.attack_position)

    def is_ability(self):
        return bool(self.ability)

    def is_lancing(self):
        return self.unit.lancing() and self.is_attack() and self.distance_to_target() >= 3

    def is_lancing_II(self):
        return self.unit.lancing_II() and self.is_attack() and self.distance_to_target() >= 4

    def is_push(self):
        return self.unit.hasattr("push") and self.is_attack()

    def is_crusading(self, gamestate):
        return any(unit for unit in self.surrounding_friendly_units(gamestate) if unit.crusading())

    def is_crusading_II(self, gamestate):
        return any(unit for unit in self.surrounding_friendly_units(gamestate) if unit.crusading_II())

    def has_high_morale(self, gamestate):
        return any(unit for unit in self.adjacent_friendly_units(gamestate) if unit.flag_bearing())

    def has_high_morale_II_A(self, gamestate):
        return any(unit for unit in self.adjacent_friendly_units(gamestate) if unit.flag_bearing_II_A())

    def has_high_morale_II_B(self, gamestate):
        return any(unit for unit in self.adjacent_friendly_units(gamestate) if unit.flag_bearing_II_B())

    def surrounding_friendly_units(self, gamestate):
        return (gamestate.units[0][position] for position in common.surrounding_tiles(self.start_position) if position
                in gamestate.units[0])

    def adjacent_friendly_units(self, gamestate):
        return (gamestate.units[0][position] for position in common.adjacent_tiles(self.start_position) if position
                in gamestate.units[0])

    def distance_to_target(self):
        return common.distance(self.start_position, self.attack_position)





