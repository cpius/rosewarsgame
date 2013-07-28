from json import JSONEncoder
from datetime import datetime
from bson import ObjectId
from collections import namedtuple


class Direction:
    """ An object direction is one move up, down, left or right.
    The class contains methods for returning the tile going one step in the direction will lead you to,
    and for returning the tiles you should check for zone of control.
    """
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def move(self, position):
        return position[0] + self.x, position[1] + self.y

    def perpendicular(self, position):
        return (position[0] + self.y, position[1] + self.x), (position[0] - self.y, position[1] - self.x)

    def __repr__(self):

        if self.x == -1:
            return "Left"

        if self.x == 1:
            return "Right"

        if self.y == -1:
            return "Down"

        if self.y == 1:
            return "Up"


Position = namedtuple("Position", ["column", "row"])


def position_to_string(position):
    if position is None:
        return ""

    columns = list(" ABCDE")
    return columns[position[0]] + str(position[1])


def position_to_tuple(position_string):
    if position_string is None or len(position_string) != 2:
        return None

    column = ord(position_string[0]) - 64  # In ASCII A, B, C, D, E is 65, 66, 67, 68, 69
    row = int(position_string[1])
    return column, row


def merge_units(units1, units2):
    all_units = units1.copy()
    all_units.update(units2)
    return all_units


def distance(position1, position2):
    return abs(position1[0] - position2[0]) + abs(position1[1] - position2[1])


def get_direction(position, forward_position):
    """ Returns the direction that would take you from position to forward_position """
    return Direction(-position[0] + forward_position[0], -position[1] + forward_position[1])


def flip(position):
    if position:
        return position[0], 9 - position[1]


eight_directions = [Direction(i, j) for i in[-1, 0, 1] for j in [-1, 0, 1] if not i == j == 0]
four_directions = [Direction(*tuple) for tuple in [0, 1], [0, -1], [1, 0], [-1, 0]]


def four_forward_tiles(position, forward_position):
    """ Returns the 4 other nearby tiles in the direction towards forward_position """
    return surrounding_tiles(position) & surrounding_tiles(forward_position)


def adjacent_tiles(position):
    return set(direction.move(position) for direction in four_directions)


def two_forward_tiles(position, forward_position):
    """ Returns the 2 other nearby tiles in the direction towards forward_position """
    return set(direction.move(position) for direction in eight_directions) & \
        set(direction.move(forward_position) for direction in four_directions)


def surrounding_tiles(position):
    """ Returns the 8 surrounding tiles"""
    return set(direction.move(position) for direction in eight_directions)


class CustomJsonEncoder(JSONEncoder):
    def default(self, obj):
        if isinstance(obj, datetime):
            return str(obj.strftime("%Y-%m-%dT%H:%M:%SZ"))
        if isinstance(obj, ObjectId):
            return str(obj)
        return JSONEncoder.default(self, obj)
