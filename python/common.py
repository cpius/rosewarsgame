from json import JSONEncoder, dumps
from datetime import datetime
from bson import ObjectId


class Direction:
    """ An object direction is one move up, down, left or right.
    The class contains methods for returning the tile going one step in the direction will lead you to,
    and for returning the tiles you should check for zone of control.
    """

    to_coordinates = {"Left": (-1, 0), "Right": (1, 0), "Down": (0, -1), "Up": (0, 1),
                      "Up-Left": (-1, 1), "Up-Right": (1, 1), "Down-Left": (-1, -1), "Down-Right": (-1, 1)}

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


class Position:
    def __init__(self, column, row):
        self.column = column
        self.row = row

    def __repr__(self):
        return " ABCDE"[self.column] + str(self.row)

    def __eq__(self, other):
        return self.column == other.column and self.row == other.row

    def __hash__(self):
        return self.column * 10 + self.row

    @classmethod
    def from_string(cls, string):
        return cls(ord(string[0]) - 64, int(string[1]))

    def distance(self, other):
        return abs(self.column - other.column) + abs(self.row - other.row)

    def get_direction(self, other):
        return list(direction for direction in directions if direction.move(self) == other)[0]

    def flip(self):
        return Position(self.column, board_height - self.row + 1)

    def four_forward_tiles(self, direction):
        return direction.perpendicular(self) + direction.forward_and_sideways(self)

    def surrounding_tiles(self):
        return set(direction.move(self) for direction in eight_directions)

    def adjacent_tiles(self):
        return set(direction.move(self) for direction in directions)

    def two_forward_tiles(self, direction):
        return direction.forward_and_sideways(self)

    def out_of_board_vertical(self):
        return self.row < 1 or self.row > board_height

    def out_of_board_horizontal(self):
        return self.column < 1 or self.column > board_width


board_height = 8
board_width = 5
board = set(Position(column, row) for column in range(1, board_width + 1) for row in range(1, board_height + 1))
directions = {Direction(name) for name in ["Up", "Down", "Left", "Right"]}
eight_directions = {Direction(name) for name in Direction.to_coordinates}


def distance(position1, position2):
    return position1.distance(position2)


def enum(*sequential, **named):
    enums = dict(zip(sequential, range(len(sequential))), **named)
    reverse = dict((value, key) for key, value in enums.iteritems())
    enums['reverse_mapping'] = reverse
    return type('Enum', (), enums)

SubOutcome = enum("UNKNOWN", "WIN", "PUSH", "MISS", "DEFEND", "DETERMINISTIC")
MoveOrStay = enum("UNKNOWN", "MOVE", "STAY")


def merge_units(units1, units2):
    all_units = units1.copy()
    all_units.update(units2)
    return all_units


def find_all_friendly_units_except_current(current_unit_position, player_units):
    return dict((position, player_units[position]) for position in player_units if position != current_unit_position)


def adjacent_friendly_units(position, units):
    return (units[pos] for pos in position.adjacent_tiles() if pos in units)


def adjacent_friendly_positions(position, units):
    return (pos for pos in position.adjacent_tiles() if pos in units)


def surrounding_friendly_units(position, units):
    return (units[pos] for pos in position.surrounding_tiles() if pos in units)

class CustomJsonEncoder(JSONEncoder):
    def default(self, obj):
        if isinstance(obj, datetime):
            return str(obj.strftime("%Y-%m-%dT%H:%M:%SZ"))
        if isinstance(obj, ObjectId):
            return str(obj)
        return JSONEncoder.default(self, obj)


def document_to_string(document):
    return dumps(document, indent=4, cls=CustomJsonEncoder)
