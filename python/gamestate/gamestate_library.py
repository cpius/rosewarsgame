from json import JSONEncoder, dumps, loads
from datetime import datetime
from collections import namedtuple
from enum import Enum
from game.game_library import get_setting

coordinates = namedtuple("coordinates", ["x", "y"])


class Direction():
    left = coordinates(-1, 0)
    right = coordinates(1, 0)
    down = coordinates(0, -1)
    up = coordinates(0, 1)
    up_left = coordinates(-1, 1)
    up_right = coordinates(1, 1)
    down_left = coordinates(-1, -1)
    down_right = coordinates(1, -1)


directions = {Direction.up, Direction.down, Direction.left, Direction.right}
eight_directions = directions | {Direction.up_left, Direction.up_right, Direction.down_left, Direction.down_right}


class Position:
    def __init__(self, column, row):
        self.column = column
        self.row = row

    def __repr__(self):
        return " ABCDE"[self.column] + str(self.row)

    def __eq__(self, other):
        return other is not None and self.column == other.column and self.row == other.row

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
        return next(direction for direction in directions if self.move(direction) == other)

    def flip(self):
        return Position(self.column, board_height - self.row + 1)

    def four_forward_tiles(self, direction):
        return self.perpendicular(direction) | self.forward_and_sideways(direction)

    def surrounding_tiles(self):
        return {pos for pos in [self.move(direction) for direction in eight_directions] if pos}

    def adjacent_tiles(self):
        return {pos for pos in [self.move(direction) for direction in directions] if pos}

    def adjacent_moves(self):
        return {direction: self.move(direction) for direction in directions if self.move(direction)}

    def two_forward_tiles(self, direction):
        return self.forward_and_sideways(direction)

    def move(self, direction):
        pos = Position(self.column + direction.x, self.row + direction.y)
        if pos in board_tiles:
            return pos

    def perpendicular(self, direction):
        return {Position(self.column + i * direction.y, self.row + i * direction.x) for i in [-1, 1]} & board_tiles

    def forward_and_sideways(self, direction):
        return {Position(self.column + i, self.row + direction.y) for i in (-1, 1)} if direction.x == 0 else \
            {Position(self.column + direction.x, self.row + i) for i in (-1, 1)} & board_tiles


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

    def __eq__(self, other):
        if other is None:
            return False

        return self.value == other.value and self.level == other.level and self.duration == other.duration

    def __ne__(self, other):
        return not self.__eq__(other)


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


def convert_quoted_integers_to_integers(document):
    if type(document) is str:
        return document
    else:
        new_document = {}
        for key, value in document.items():
            try:
                key = int(key)
            except Exception:
                pass
            new_document[key] = convert_quoted_integers_to_integers(value)
        return new_document


description_document = convert_quoted_integers_to_integers(loads(open("./../Version_1.1/Descriptions.json").read()))

ability_descriptions = description_document["abilities"]
trait_descriptions = description_document["traits"]
state_descriptions = description_document["states"]
effect_descriptions = description_document["effects"]



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


class Intelligence(Enum):
    Human = 1
    AI = 2
    Network = 3


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
    attack_frozen = 10


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


enum_from_string = {enum.name: enum for type in [Trait, State, Effect, Ability, Unit, Intelligence] for enum in type}


def get_attribute_from_document(attribute_name, info):
    """
    :param attribute_name: string
    :param info: A number or dictionary that contains info about the attribute.
                 If the attribute is a state, info is the value of the state.
                 If the attribute is a trait or ability, info is the level of the trait or ability.
                 If the attribute is an effect, info is a dictionary containing the level and duration of the effect.
    :return: An attribute enum, and its AttributeValues
    """

    attribute = enum_from_string[attribute_name]
    if attribute in State:
        return attribute, AttributeValues(value=info)
    elif attribute in Trait or attribute in Ability:
        return attribute, AttributeValues(level=info)
    elif attribute in Effect:
        if get_setting("version") == "1.1":
            return attribute, AttributeValues(**info)
        elif get_setting("version") == "1.0":
            return attribute, AttributeValues(duration=info, level=info)

board_height = 8
board_width = 5
board_tiles = set(Position(column, row) for column in range(1, board_width + 1) for row in range(1, board_height + 1))


def get_description(attribute, level):
    if attribute in Ability:
        return ability_descriptions[attribute.name][level]
    elif attribute in Trait:
        return trait_descriptions[attribute.name][level]
    elif attribute in Effect:
        return effect_descriptions[attribute.name][level]
    elif attribute in State:
        return state_descriptions[attribute.name]


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

    if actual == expected:
        return True, "Everything is swell"
    else:
        return False, message


class CustomJsonEncoder(JSONEncoder):
    def default(self, obj):
        if isinstance(obj, datetime):
            return str(obj.strftime("%Y-%m-%dT%H:%M:%SZ"))
        if isinstance(obj, Enum):
            return obj.name
        return JSONEncoder.default(self, obj)


def document_to_string(document):
    return dumps(document, indent=4, cls=CustomJsonEncoder, sort_keys=False)


def get_string_attributes(attributes):
    """
    :param attributes: A Unit enum or a dictionary with enums as keys and attributevalues as values.
    :return: If input is a Unit enum, the unit name
             Otherwise: If the enum is of type Trait, Ability or State, a dictionary with strings as keys and numbers as
             values
                        If the enum is of type Effect, a dictionary with strings as keys and a dictionaries as values
    """
    if attributes in Unit:
        return attributes.name

    dictionary = {}
    for attribute_enum, attribute_values in attributes.items():
        if attribute_enum in Trait or attribute_enum in Ability:
            dictionary[attribute_enum.name] = attribute_values.level
        elif attribute_enum in State:
            dictionary[attribute_enum.name] = attribute_values.value
        if attribute_enum in Effect:
            dictionary[attribute_enum.name] = {"duration": attribute_values.duration, "level": attribute_values.level}

    return dictionary


def merge(first_dictionary, second_dictionary, third_dictionary=None, fourth_dictionary=None):
    merged_dictionary = first_dictionary.copy()
    merged_dictionary.update(second_dictionary)

    if third_dictionary:
        merged_dictionary.update(third_dictionary)

    if fourth_dictionary:
        merged_dictionary.update(fourth_dictionary)

    return merged_dictionary


def flip_units(units):
    return dict((position.flip(), unit) for position, unit in units.items())


def unit_with_attribute_at(pos, attribute, units, level=1):
    return pos in units and units[pos].has(attribute, level)


def get_enum_attributes(attributes):
    """
    :param attributes: A string or a dictionary
    :return: If input is a string, returns an enum.
             If input is a dictionary, returns a dictionary with enums as keys and Attributevalues as values.
    """
    if type(attributes) is str:
        return enum_from_string[attributes]
    else:
        enum_dict = {}
        for key, value in attributes.items():
            if type(key) is str:
                key = enum_from_string[key]
            if type(value) is str or type(value) is int:
                value = AttributeValues(level=value)
            enum_dict[key] = value
        return enum_dict


def filter_actions(actions, positions):
    if not positions:
        return actions
    return [action for action in actions if all(getattr(action, key) == value for key, value in positions.items())]
