from json import JSONEncoder, dumps
from datetime import datetime
from bson import ObjectId
import collections
import functools


class Direction:
    """ A direction is one move up, down, left or right.
    The class contains methods for returning the tile going one step in the direction will lead you to,
    and for returning the tiles you should check for zone of control.
    """

    to_coordinates = {"Left": (-1, 0), "Right": (1, 0), "Down": (0, -1), "Up": (0, 1),
                      "Up_Left": (-1, 1), "Up_Right": (1, 1), "Down_Left": (-1, -1), "Down_Right": (-1, 1)}

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

    def __ne__(self, other):
        return not self.__eq__(other)

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


def enum(*sequential, **named):
    enums = dict(zip(sequential, range(1, len(sequential) + 1)), **named)
    reverse = dict((value, key) for key, value in enums.iteritems())
    enums['reverse_mapping'] = reverse
    return type('Enum', (), enums)


trait_descriptions = {
    "attack_cooldown": "Can only attack every third turn.",
    "attack_cooldown_II": "Can only attack every second turn.",
    "attack_frozen": "Unit cannot attack",
    "berserking": "Can move 4 tiles if movement ends with an attack.",
    "big_shield": "+2D v melee",
    "bloodlust": "Every kill gives it an extra attack",
    "bribed": "Whether a unit is currently bribed by a Diplomat.",
    "bribed_II": "Whether a unit is currently bribed by a Diplomat_II_B.",
    "cavalry_charging": "All cavalry units starting their turn in the 8 surrounding tiles have +1 Movement",
    "combat_agility": "Can make an attack after its first action. (But not a second move.)",
    "crusading": "Friendly melee units starting their movement in one of the 8 tiles surrounding Crusader get +1A.",
    "crusading_II": "Friendly melee units starting their movement in one of the 8 tiles surrounding Crusader get +1A, "
                    "+1D.",
    "defence_maneuverability": "Can move two tiles if one of them is sideways.",
    "double_attack_cost": "Attack takes two actions.",
    "extra_action": "Whether the unit is doing its extra action",
    "extra_life": "It takes two successful hits to kill a unit with an extra life",
    "far_sighted": "-1A if target is less than 4 tiles away.",
    "flag_bearing": "Friendly melee units receive +2A while adjacent to Flag Bearer.",
    "flag_bearing_II_A": "Friendly melee units receive +2A while surrounding Flag Bearer.",
    "flag_bearing_II_B": "Friendly melee units receive +3A while adjacent to Flag Bearer.",
    "frozen": "Frozen units cannot perform any actions.",
    "improved_weapons": "Whether a unit currently has been the target of an improve_weapons function by a Weaponsmith.",
    "improved_weapons_II_A": "Whether a unit currently has been the target of an improve_weapons function by a "
                             "Weaponsmith_II_A",
    "improved_weapons_II_B": "Whether a unit currently has been the target of an improve_weapons function by a "
                             "Weaponsmith_II_B",
    "melee_expert": "+1A, +1D vs melee units.",
    "melee_freeze": "Units adjacent to it can only attack it, not move.",
    "movement_remaining": "Movement points left for doing an extra action",
    "pikeman_specialist": "Pikemen do not get +1A/+1D against it.",
    "lancing": "If it starts movement with 2 empty tiles between lancer and the unit it attacks, +2A.",
    "lancing_II": "If it starts movement with 3 empty tiles between lancer and the unit it attacks, +3A.",
    "longsword": "Also hits the 4 nearby tiles in the attack direction.",
    "lost_extra_life": "Whether the unit has lost its extra life",
    "push": "If attack and defence rolls both succeed, it can still move forward. If not on back line, opponents units "
            "must retreat directly backwards or die.",
    "rage": "Can make an attack after it's move. (But not a second move.)",
    "rage_II": "Can move up to two tiles to make an attack. (But cannot take over the attacked tile if it's 3 tiles "
               "away.)",
    "recently_bribed": "Whether a unit was bribed last turn.",
    "sabotaged": "Whether a unit is currently sabotaged by a Saboteur.",
    "sabotaged_II": "Whether a unit is currently sabotaged by a Saboteur_II_B.",
    "scouting": "Can move past all units.",
    "sharpshooting": "Targets have their defence reduced to 1 during the attack.",
    "swiftness": "Can use remaining moves after attacking.",
    "tall_shield": "+1D against ranged attacks.",
    "triple_attack": "Also hits the two diagonally nearby tiles in the attack direction.",
    "used": "Whether a unit has been used this round.",
    "xp": "Experience."
}


ability_descriptions = {
    "bribe": "You can use an opponent's unit this turn. Your opponent can't use it on his next turn. You can't bribe "
             "the same unit on your next turn. The unit gets +1A until end of turn.",
    "bribe_II": "You can use an opponent's unit this turn. Your opponent can't use it on his next turn. You can't bribe "
                "the same unit on your next turn. The unit gets +2A until end of turn.",
    "improve_weapons": "Give melee unit +3 attack, +1 defence until your next turn.",
    "improve_weapons_II_A": "Give melee unit +2 attack, +1 defence for two turns.",
    "improve_weapons_II_B": "Give melee unit +3 attack, +2 defence, and zoc against cavalry until your next turn",
    "pikeman_specialist": "Pikemen do not get +1D against Hussar.",
    "poison": "Freezes a unit for 2 turns.",
    "poison_II": "Freezes a unit for 3 turns.",
    "sabotage": "Reduces a units defence to 0 for 1 turn.",
    "sabotage_II": "Reduces a units defence to -1 for 1 turn.",
    "triple_attack": "Also hits the two diagonally nearby tiles in the attack direction."
}


types = ["Cavalry", "Infantry", "Siege_Weapon", "Specialist"]

Trait = enum(*(trait for trait in trait_descriptions))

Ability = enum(*(ability for ability in ability_descriptions))

Type = enum(*types)


if 1 == 2:
    class Type:
        Cavalry = 1
        Infantry = 2
        Siege_Weapon = 3
        Specialist = 4

    class Trait:
        attack_cooldown = 1
        attack_frozen = 2
        berserking = 3
        big_shield = 4
        bloodlust = 5
        bribed = 6
        bribed_II = 7
        cavalry_charging = 8
        combat_agility = 9
        defence_maneuverability = 10
        double_attack_cost = 11
        extra_action = 12
        extra_life = 13
        frozen = 14
        improved_weapons = 15
        improved_weapons_II_A = 16
        improved_weapons_II_B = 17
        melee_expert = 18
        melee_freeze = 19
        movement_remaining = 20
        longsword = 21
        push = 22
        rage = 23
        rage_II = 24
        recently_bribed = 25
        sabotaged = 26
        sabotaged_II = 27
        scouting = 28
        sharpshooting = 29
        swiftness = 30
        tall_shield = 31
        triple_attack = 32
        used = 33
        lancing = 34
        attack_cooldown = 35
        far_sighted = 36
        lancing_II = 37
        flag_bearing = 38
        flag_bearing_II_A = 39
        flag_bearing_II_B = 40
        crusading = 41
        crusading = 42
        attack_cooldown_II = 43
        crusading_II = 44
        xp = 45
        pikeman_specialist = 46
        lost_extra_life = 47

        reverse_mapping = {}

    class Ability:
        bribe = 1
        bribe_II = 2
        improve_weapons = 3
        improve_weapons_II_A = 4
        improve_weapons_II_B = 5
        pikeman_specialist = 6
        poison = 7
        sabotage = 8
        sabotage_II = 9
        triple_attack = 10
        poison_II = 11

board_height = 8
board_width = 5
board = set(Position(column, row) for column in range(1, board_width + 1) for row in range(1, board_height + 1))

eight_directions_namedtuple = collections.namedtuple("eight_directions", [name for name in Direction.to_coordinates])
eight_directions = eight_directions_namedtuple(*(Direction(name) for name in Direction.to_coordinates))
four_directions_namedtuple = collections.namedtuple("directions", [name for name in ["Up", "Down", "Left", "Right"]])
directions = four_directions_namedtuple(*(Direction(name) for name in ["Up", "Down", "Left", "Right"]))


def distance(position1, position2):
    return position1.distance(position2)


SubOutcome = enum("UNKNOWN", "WIN", "PUSH", "MISS", "DEFEND", "DETERMINISTIC")


def find_all_friendly_units_except_current(current_unit_position, player_units):
    return dict((pos, player_units[pos]) for pos in player_units if pos != current_unit_position)


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


class memoized(object):
    """Decorator. Caches a function's return value each time it is called.
    If called later with the same arguments, the cached value is returned
    (not reevaluated).
    """
    def __init__(self, func):
        self.func = func
        self.cache = {}

    def __call__(self, *args):
        if not isinstance(args, collections.Hashable):
            return self.func(*args)
        if args in self.cache:
            return self.cache[args]
        else:
            value = self.func(*args)
            self.cache[args] = value
            return value

    def __repr__(self):
        return self.func.__doc__

    def __get__(self, obj):
        return functools.partial(self.__call__, obj)
