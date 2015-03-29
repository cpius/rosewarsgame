from json import loads
from collections import namedtuple
from game.game_library import get_setting, convert_quoted_integers_to_integers, merge
from gamestate.enums import *

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


class Log():
    def __init__(self, action_type, unit, target_unit, action_number, colors, outcome_string=None):
        self.action_type = action_type
        self.unit = unit
        self.target_unit = target_unit
        self.outcome_string = outcome_string
        self.action_number = action_number
        self.colors = colors


enum_from_string = {enum.name: enum for type in [Trait, State, Effect, Ability, Unit] for enum in type}


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


descriptions_document = convert_quoted_integers_to_integers(loads(open("./../Version_1.1/Descriptions.json").read()))
descriptions = merge(*[descriptions_document[key] for key in ["abilities", "traits", "states", "effects"]])


def get_description(attribute, level):
    return descriptions[attribute.name][level]


def distance(position1, position2):
    return position1.distance(position2)


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
