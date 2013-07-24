import battle
import methods
from datetime import datetime
from copy import copy


class Action(object):
    def __init__(self,
                 start_position,
                 end_position=None,
                 attack_position=None,
                 ability_position=None,
                 move_with_attack=False,
                 ability="",
                 action_number=None,
                 sub_actions=None,
                 outcome=True):
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

        self.is_attack = bool(attack_position)
        self.is_ability = bool(ability)

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
            document_copy[attribute] = methods.position_to_tuple(document_copy[attribute])

        if "sub_actions" in document_copy:
            document_copy["sub_actions"] =\
                [cls.from_document(sub_action_document) for sub_action_document in document_copy["sub_actions"]]
        action = cls(**document_copy)
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
            document_copy[attribute] = methods.position_to_tuple(document_copy[attribute])

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

        if self.start_position != self.end_position:
            representation += " move from " + coordinates(self.start_position)
            representation += " to " + coordinates(self.end_position)
            if self.is_attack:
                representation += " and"
        else:
            representation += " at " + coordinates(self.start_position)

        if self.is_attack and not self.move_with_attack:
            representation += " attack " + self.target_reference.name + " " + coordinates(self.attack_position)

        if self.is_attack and self.move_with_attack:
            representation += " attack-move " + self.target_reference.name + " " + coordinates(self.attack_position)

        if self.is_ability:
            representation += " use "\
                              + self.ability\
                              + " on "\
                              + self.target_reference.name\
                              + " "\
                              + coordinates(self.ability_position)

        return representation

    def get_basic_string(self):
        representation = self.unit_reference.name

        if self.start_position != self.end_position:
            representation += " move from " + coordinates(self.start_position)
            representation += " to " + coordinates(self.end_position)
            if self.is_attack:
                representation += " and"
        else:
            representation += " at " + coordinates(self.start_position)

        if self.is_attack and not self.move_with_attack:
            representation += " attack " + self.target_reference.name + " " + coordinates(self.attack_position)

        if self.is_attack and self.move_with_attack:
            representation += " attack-move " + self.target_reference.name + " " + coordinates(self.attack_position)

        if self.is_ability:
            representation += " use "\
                              + self.ability\
                              + " on "\
                              + self.target_reference.name\
                              + " "\
                              + coordinates(self.ability_position)

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
            representation += "and attack " + coordinates(sub_action.attack_position)
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
                            "is_attack",
                            "move_with_attack",
                            "is_ability",
                            "ability"]
        original = dict((attribute, self.__dict__[attribute]) for attribute in basic_attributes)
        other = dict((attribute, other.__dict__[attribute]) for attribute in basic_attributes)

        return original == other

    def to_document(self):
        action_number = self.action_number if self.action_number else 0
        sub_action_docs = [sub_action.to_document() for sub_action in self.sub_actions]

        return {"action_number": action_number,
                "start_position": methods.position_to_string(self.start_position),
                "end_position": methods.position_to_string(self.end_position),
                "attack_position": methods.position_to_string(self.attack_position),
                "ability_position": methods.position_to_string(self.ability_position),
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
            document[attribute] = methods.position_to_string(getattr(self, attribute))
        for attribute in write_attributes - convert_attributes:
            document[attribute] = getattr(self, attribute)
        if sub_action_docs:
            document["sub_actions"] = sub_action_docs
        return document

    def ensure_outcome(self, outcome):
        self.final_position = self.end_position

        if outcome:
            self.rolls = (1, 6)
        else:
            self.rolls = (6, 1)

        for sub_action in self.sub_actions:
            sub_action.rolls = self.rolls

        return self


def coordinates(position):
    columns = list(" ABCDE")
    return columns[position[0]] + str(position[1])
