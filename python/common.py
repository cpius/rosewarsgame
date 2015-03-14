from json import JSONEncoder, dumps
from datetime import datetime
import collections
import functools
from dictdiffer import DictDiffer
from enum import Enum


class Direction:
    """ A direction is one move up, down, left or right.
    The class contains methods for returning the tile going one step in the direction will lead you to,
    and for returning the tiles you should check for zone of control.
    """

    to_coordinates = {"Left": (-1, 0), "Right": (1, 0), "Down": (0, -1), "Up": (0, 1),
                      "Up_Left": (1, -1), "Up_Right": (1, 1), "Down_Left": (-1, -1), "Down_Right": (-1, 1)}

    def __init__(self, name):
        self.x, self.y = self.to_coordinates[name]
        self.name = name

    def move(self, position):
        return Position(position.column + self.x, position.row + self.y)

    def perpendicular(self, position):
        return [Position(position.column + i * self.y, position.row + i * self.x) for i in [-1, 1]]

    def forward_and_sideways(self, position):
        return [Position(position.column + i, position.row + self.y) for i in (-1, 1)] if self.x == 0 else \
            [Position(position.column + self.x, position.row + i) for i in (-1, 1)]

    def __repr__(self):
        return self.name

    def __eq__(self, other):
        return self.x == other.x and self.y == other.y

    def __ne__(self, other):
        return not self.__eq__(other)


class Position:
    def __init__(self, column, row):
        self.column = column
        self.row = row

    def __repr__(self):
        return " ABCDE"[self.column] + str(self.row)

    def __eq__(self, other):
        return not other is None and self.column == other.column and self.row == other.row

    def __ne__(self, other):
        return not self.__eq__(other)

    def __hash__(self):
        return self.column * 10 + self.row

    @classmethod
    def from_string(cls, string):
        return cls(ord(string[0]) - 64, int(string[1]))

    def distance(self, other):
        return abs(self.column - other.column) + abs(self.row - other.row)

    def get_direction_to(self, other):
        return list(direction for direction in directions if direction.move(self) == other)[0]

    def flip(self):
        return Position(self.column, board_height - self.row + 1)

    def four_forward_tiles(self, direction):
        return set(pos for pos in direction.perpendicular(self) + direction.forward_and_sideways(self) if pos in board)

    def surrounding_tiles(self):
        return set(pos for pos in [direction.move(self) for direction in eight_directions] if pos in board)

    def adjacent_tiles(self):
        return set(pos for pos in [direction.move(self) for direction in directions] if pos in board)

    def two_forward_tiles(self, direction):
        return set(pos for pos in direction.forward_and_sideways(self) if pos in board)


class AttributeValues():
    def __init__(self, value=None, level=None, duration=None):
        self.value = value
        self.level = level
        self.duration = duration

    def __repr__(self):
        string = ""
        if self.value:
            string += "Value: " + str(self.value) + " "
        if self.level:
            string += "Level: " + str(self.level) + " "
        if self.duration:
            string += "Duration: " + str(self.duration) + " "
        return string


class ActionType(Enum):
    Attack = 1
    Ability = 2
    Move = 3


class Log():
    def __init__(self, action_type, unit, target_unit, action_number, colors, outcome_string=None):
        self.action_type = action_type
        self.unit = unit
        self.target_unit = target_unit
        self.outcome_string = outcome_string
        self.action_number = action_number
        self.colors = colors


trait_descriptions = {
    "attack_cooldown": {
        1: "Can only attack every third turn.",
        2: "Can only attack every second turn"},
    "berserking": {
        1: "Can move 4 tiles if movement ends with an attack."},
    "big_shield": {
        1: "+2D v melee"},
    "combat_agility": {
        1: "Can make an attack after its first action. (But not a second move.)"},
    "crusading": {
        1: "Friendly melee units starting their movement in one of the 8 tiles surrounding Crusader get +1A.",
        2: "Friendly melee units starting their movement in one of the 8 tiles surrounding Crusader get +1A, +1D"},
    "defence_maneuverability": {
        1: "Can move two tiles if one of them is sideways."},
    "double_attack_cost": {
        1: "Attack takes two actions."},
    "extra_life": {
        1: "It takes two successful hits to kill this unit."},
    "far_sighted": {
        1: "-1A if target is less than 4 tiles away."},
    "flag_bearing": {
        1: "Friendly melee units receive +2A if attacking from a tile adjacent to Flag Bearer.",
        2: "Friendly melee units receive +2A if attacking from a tile surrounding Flag Bearer."},
    "melee_expert": {
        1: "+1A, +1D vs melee units."},
    "melee_freeze": {
        1: "Units adjacent to it can only attack it, not move."},
    "pikeman_specialist": {
        1: "Pikemen do not get +1A/+1D against it."},
    "lancing": {
        1: "If it starts movement with 2 empty tiles between lancer and the unit it attacks, +2A.",
        2: "If it starts movement with 3 empty tiles between lancer and the unit it attacks, +3A."},
    "longsword": {
        1: "Also hits the 4 nearby tiles in the attack direction."},
    "push": {
        1: "If attack and defence rolls both succeed, it can still move forward. If not on back line, opponents units "
        "must retreat directly backwards or die."},
    "rage": {
        1: "Can make an attack after it's move. (But not a second move.)"},
    "scouting": {
        1: "Can move past all units."},
    "sharpshooting": {
        1: "Targets have their defence reduced to 1 during the attack."},
    "swiftness": {
        1: "Can use remaining moves after attacking."},
    "tall_shield": {
        1: "+1D against ranged attacks."},
    "triple_attack": {
        1: "Also hits the two diagonally nearby tiles in the attack direction."},
    "attack_skill": {
        1: "Is added to the units base attack"},
    "defence_skill": {
        1: "Is added to the units base defence"},
    "range_skill": {
        1: "Is added to the units base range"},
    "movement_skill": {
        1: "Is added to the units base movement"},
    "fire_arrows": {
        1: "+3A vs War Machines"},
    "cavalry_specialist": {
        1: "+1A +1D vs Cavalry"},
    "war_machine_specialist": {
        1: "+1A +1D vs War Machines"},
    "flanking": {
        1: "If it attacks a unit from a direction that is not the front, and it did not attack the defending unit last "
           "turn, 2 is added to it's attack.",
        2: "If it attacks a unit from a direction that is not the front, and it did not attack the defending unit last "
           "turn, 4 is added to it's attack."},
    "ride_through": {
        1: "If there is an enemy unit next to it, and the tile behind that unit is empty, it can make an attack where "
           "it ends up on this empty tile. Zone of control has no effect on this ability."},
    "spread_attack": {
        1: "Also attacks the adjacent tiles with -1A."},
    "javelin": {
        1: "Can one time make a ranged attack with range 3. The defending unit has it's defence reduced by 1."}
}

state_descriptions = {
    "extra_action": "Whether the unit is doing its extra action.",
    "lost_extra_life": "Whether the unit has lost its extra life",
    "javelin_thrown": "Whether a unit has used it's javelin",
    "movement_remaining": "Movement points left for doing an extra action",
    "used": "Whether a unit has been used this turn.",
    "experience": "Experience.",
    "recently_upgraded": "Whether a unit was upgraded this turn",
    "recently_bribed": "Whether a unit was bribed last turn.",
    "flanked": "This unit was attacked by a unit with flanking last turn.",
}


effect_descriptions = {
    "attack_frozen": "Unit cannot attack",
    "bribed": "Whether a unit is bribed by a Diplomat.",
    "poisoned": "Unit cannot perform any actions.",
    "improved_weapons": "Whether a unit currently has been the target of an improve_weapons function by a Weaponsmith.",
    "sabotaged": "Whether a unit is sabotaged by a Saboteur."
}

ability_descriptions = {
    "bribe": {
        1: "You can use an opponent's unit this turn. Your opponent can't use it on his next turn. The unit gets +1A "
           "until end of turn.",
        2: "You can use an opponent's unit this turn. Your opponent can't use it on his next turn. The unit gets +2A "
           "until end of turn."},
    "improve_weapons": {
        1: "Give melee unit +3 attack, +1 defence until your next turn.",
        2: "Give melee unit +2 attack, +1 defence for two turns."},
    "pikeman_specialist": {
        1: "Pikemen do not get +1D against Hussar."},
    "poison": {
        1: "Makes a unit unable to perform actions until your next turn.",
        2: "Makes a unit unable to perform actions for two turns."},
    "sabotage": {
        1: "Reduces a units defence to 0 this turn.",
        2: "Reduces a units defence to 0 for two turns."},
    "assassinate": {
        1: "Assassin attacks an enemy unit, and it's defence is reduced to 2. Assassin is attacked. This ability can "
           "only be performed on your second action."}
}

opponent_descriptions = {
    "HotSeat": "Start a new hot seat game on this machine",
    "AI": "Start a new game against an AI",
    "Load": "Load the most recent game",
    "Internet": "Start a new game against an opponent from the internet"
}

ai_descriptions = {
    "1": "Easy",
    "2": "Medium",
    "3": "Hard"
}


class Type(Enum):
    Cavalry = 1
    Infantry = 2
    War_Machine = 3
    Specialist = 4


class State(Enum):
    extra_action = 1
    movement_remaining = 2
    lost_extra_life = 3
    experience = 4
    used = 5
    recently_bribed = 6
    recently_upgraded = 7
    javelin_thrown = 8
    flanked = 9


class Trait(Enum):
    berserking = 1
    big_shield = 2
    combat_agility = 3
    defence_maneuverability = 4
    double_attack_cost = 5
    extra_life = 6
    melee_expert = 7
    melee_freeze = 8
    longsword = 9
    push = 10
    rage = 11
    scouting = 12
    sharpshooting = 13
    swiftness = 14
    tall_shield = 15
    triple_attack = 16
    lancing = 17
    attack_cooldown = 18
    far_sighted = 19
    flag_bearing = 20
    crusading = 21
    pikeman_specialist = 22
    attack_skill = 23
    defence_skill = 24
    range_skill = 25
    movement_skill = 26
    fire_arrows = 27
    cavalry_specialist = 28
    war_machine_specialist = 29
    flanking = 30
    ride_through = 31
    spread_attack = 32
    javelin = 33


class Ability(Enum):
    bribe = 1
    improve_weapons = 2
    poison = 3
    sabotage = 4
    assassinate = 5


class Effect(Enum):
    attack_frozen = 1
    bribed = 2
    improved_weapons = 3
    poisoned = 4
    sabotaged = 5


class Unit(Enum):
    Archer = 1
    Ballista = 2
    Catapult = 3
    Knight = 4
    Light_Cavalry = 5
    Pikeman = 6
    Berserker = 7
    Cannon = 8
    Crusader = 9
    Flag_Bearer = 10
    Longswordsman = 11
    Saboteur = 12
    Royal_Guard = 13
    Scout = 14
    War_Elephant = 15
    Weaponsmith = 16
    Viking = 17
    Diplomat = 18
    Halberdier = 19
    Hussar = 20
    Flanking_Cavalry = 21
    Hobelar = 22
    Lancer = 23
    Fencer = 24
    Assassin = 25
    Trebuchet = 26
    Javeliner = 27


class Opponent(Enum):
    HotSeat = 1
    AI = 2
    Internet = 3
    Load = 4


enum_from_string = {enum.name: enum for enum_type in [Trait, State, Effect, Ability, Unit] for enum in enum_type}


def get_attribute_from_document(attribute_name, number):

    attribute = enum_from_string[attribute_name]
    if attribute in State:
        return attribute, AttributeValues(value=number)
    elif attribute in Trait or attribute in Ability:
        return attribute, AttributeValues(level=number)
    elif attribute in Effect:
        if type(number) is int or type(number) is bool:
            return attribute, AttributeValues(level=1, duration=number)
        else:
            return attribute, AttributeValues(**number)

board_height = 8
board_width = 5
board = set(Position(column, row) for column in range(1, board_width + 1) for row in range(1, board_height + 1))

eight_directions_namedtuple = collections.namedtuple("eight_directions", [name for name in Direction.to_coordinates])
eight_directions = eight_directions_namedtuple(*(Direction(name) for name in Direction.to_coordinates))
four_directions_namedtuple = collections.namedtuple("directions", [name for name in ["Up", "Down", "Left", "Right"]])
directions = four_directions_namedtuple(*(Direction(name) for name in ["Up", "Down", "Left", "Right"]))


def get_ability_description(ability, level=1):
    return ability_descriptions[ability.name][level]


def distance(position1, position2):
    return position1.distance(position2)


def assert_equal_documents(testcase, expected, actual, testcase_file):
    message = "Wrong document for " + testcase_file + "\n\n"

    message += "Expected:\n" + document_to_string(expected)
    message += "\nActual:\n" + document_to_string(actual) + "\n"

    difference = DictDiffer(actual, expected)
    if difference.added():
        message += "Added " + str(difference.added())
    if difference.removed():
        message += "Removed " + str(difference.removed())
    if difference.changed_recursive():
        message += "Changed " + str(difference.changed_recursive())

    testcase.assertEqual(expected, actual, message)


class CustomJsonEncoder(JSONEncoder):
    def default(self, obj):
        if isinstance(obj, datetime):
            return str(obj.strftime("%Y-%m-%dT%H:%M:%SZ"))
        if isinstance(obj, Enum):
            return obj.name
        return JSONEncoder.default(self, obj)


def document_to_string(document):
    return dumps(document, indent=4, cls=CustomJsonEncoder, sort_keys=False)


def readable(attributes):
    dictionary = {}
    if attributes in Unit:
        return attributes.name
    for attribute, attribute_values in attributes:
        if attribute in Trait or attribute in Ability:
            dictionary[attribute.name] = attribute_values.level
        elif attribute in State:
            dictionary[attribute.name] = attribute_values.value
        if attribute in Effect:
            dictionary[attribute.name] = {"duration": attribute_values.duration, "level": attribute_values.level}

    return dictionary


def merge(first_dictionary, second_dictionary, third_dictionary=None, fourth_dictionary=None):
    merged_dictionary = first_dictionary.copy()
    merged_dictionary.update(second_dictionary)

    if third_dictionary:
        merged_dictionary.update(third_dictionary)

    if fourth_dictionary:
        merged_dictionary.update(fourth_dictionary)

    return merged_dictionary


def attribute_key(attribute, value):
    if value == 1:
        return attribute
    elif value > 1:
        attribute_key = attribute + "_"
        for i in range(0, value):
            attribute_key += "I"

        return attribute_key


def flip_units(units):
    return dict((position.flip(), unit) for position, unit in units.items())


def merge_units(units1, units2):
    units = units1.copy()
    units.update(units2)
    return units


def get_setting(name):
    with open("settings.txt") as input:
        for line in input:
            line = line.split()
            if len(line) > 1 and line[0] == name:
                setting = line[2].strip()
                if setting in ["yes", "no"]:
                    return setting == "yes"
                elif setting in [str(i) for i in range(10)]:
                    return int(setting)
                else:
                    return setting


def unit_with_attribute_at(pos, attribute, units, level=1):
    return pos in units and units[pos].has(attribute, level)






