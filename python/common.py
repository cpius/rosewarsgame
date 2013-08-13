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

    def get_direction_to(self, other):
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


def enum(n, *sequential, **named):
    enums = dict(zip(sequential, range(n, len(sequential) + n)), **named)
    reverse = dict((value, key) for key, value in enums.iteritems())
    reverse_print = dict((value, key.replace("_", " ")) for key, value in enums.iteritems())
    enums['name'] = reverse
    enums['write'] = reverse_print
    return type('Enum', (), enums)


trait_descriptions = {
    "attack_cooldown": "Can only attack every third turn.",
    "attack_cooldown_II": "Can only attack every second turn.",
    "berserking": "Can move 4 tiles if movement ends with an attack.",
    "big_shield": "+2D v melee",
    "bloodlust": "Every kill gives it an extra attack",
    "cavalry_charging": "All cavalry units starting their turn in the 8 surrounding tiles have +1 Movement",
    "combat_agility": "Can make an attack after its first action. (But not a second move.)",
    "crusading": "Friendly melee units starting their movement in one of the 8 tiles surrounding Crusader get +1A.",
    "crusading_II": "Friendly melee units starting their movement in one of the 8 tiles surrounding Crusader get +1A, "
                    "+1D.",
    "defence_maneuverability": "Can move two tiles if one of them is sideways.",
    "double_attack_cost": "Attack takes two actions.",
    "extra_life": "It takes two successful hits to kill this unit.",
    "far_sighted": "-1A if target is less than 4 tiles away.",
    "flag_bearing": "Friendly melee units receive +2A while adjacent to Flag Bearer.",
    "flag_bearing_II_A": "Friendly melee units receive +2A while surrounding Flag Bearer.",
    "flag_bearing_II_B": "Friendly melee units receive +3A while adjacent to Flag Bearer.",
    "melee_expert": "+1A, +1D vs melee units.",
    "melee_freeze": "Units adjacent to it can only attack it, not move.",
    "pikeman_specialist": "Pikemen do not get +1A/+1D against it.",
    "lancing": "If it starts movement with 2 empty tiles between lancer and the unit it attacks, +2A.",
    "lancing_II": "If it starts movement with 3 empty tiles between lancer and the unit it attacks, +3A.",
    "longsword": "Also hits the 4 nearby tiles in the attack direction.",
    "push": "If attack and defence rolls both succeed, it can still move forward. If not on back line, opponents units "
            "must retreat directly backwards or die.",
    "rage": "Can make an attack after it's move. (But not a second move.)",
    "rage_II": "Can move up to two tiles to make an attack. (But cannot take over the attacked tile if it's 3 tiles "
               "away.)",
    "scouting": "Can move past all units.",
    "sharpshooting": "Targets have their defence reduced to 1 during the attack.",
    "swiftness": "Can use remaining moves after attacking.",
    "tall_shield": "+1D against ranged attacks.",
    "triple_attack": "Also hits the two diagonally nearby tiles in the attack direction.",
    "attack_skill": "Is added to the units base attack",
    "defence_skill": "Is added to the units base defence",
    "range_skill": "Is added to the units base range",
    "movement_skill": "Is added to the units base movement",
    "fire_arrows": "+3A vs Siege Weapons",
    "cavalry_specialist": "+1A +1D vs Cavalry",
    "siege_weapon_specialist": "+1A +1D vs Siege Weapons",
    "flanking": "+2A vs Infantry",
    "level": "The number of upgrades."
}

state_descriptions = {
    "attack_frozen": "Unit cannot attack",
    "bribed": "Whether a unit is currently bribed by a Diplomat.",
    "bribed_II": "Whether a unit is currently bribed by a Diplomat_II_B.",
    "extra_action": "Whether the unit is doing its extra action.",
    "frozen": "Unit cannot perform any actions.",
    "improved_weapons": "Whether a unit currently has been the target of an improve_weapons function by a Weaponsmith.",
    "improved_weapons_II_A": "Whether a unit currently has been the target of an improve_weapons function by a "
                             "Weaponsmith_II_A",
    "lost_extra_life": "Whether the unit has lost its extra life",
    "movement_remaining": "Movement points left for doing an extra action",
    "recently_bribed": "Whether a unit was bribed last turn.",
    "sabotaged": "Whether a unit is currently sabotaged by a Saboteur.",
    "sabotaged_II": "Whether a unit is currently sabotaged by a Saboteur_II_B.",
    "used": "Whether a unit has been used this round.",
    "xp": "Experience.",
}

ability_descriptions = {
    "bribe": "You can use an opponent's unit this turn. Your opponent can't use it on his next turn. You can't bribe "
             "the same unit on your next turn. The unit gets +1A until end of turn.",
    "bribe_II": "You can use an opponent's unit this turn. Your opponent can't use it on his next turn. You can't "
                "bribe the same unit on your next turn. The unit gets +2A until end of turn.",
    "improve_weapons": "Give melee unit +3 attack, +1 defence until your next turn.",
    "improve_weapons_II_A": "Give melee unit +2 attack, +1 defence for two turns.",
    "pikeman_specialist": "Pikemen do not get +1D against Hussar.",
    "poison": "Freezes a unit for 2 turns.",
    "poison_II": "Freezes a unit for 3 turns.",
    "sabotage": "Reduces a units defence to 0 for 1 turn.",
    "sabotage_II": "Reduces a units defence to -1 for 1 turn.",
    "triple_attack": "Also hits the two diagonally nearby tiles in the attack direction."
}


types = ["Cavalry", "Infantry", "Siege_Weapon", "Specialist"]

Trait = enum(1, *(trait for trait in dict(trait_descriptions)))

State = enum(1000, *(trait for trait in dict(state_descriptions)))

Ability = enum(2000, *(ability for ability in ability_descriptions))

Type = enum(3000, *types)


def is_trait(n):
    return n < 999


if 1 == 2:
    class Type:
        Cavalry = None
        Infantry = None
        Siege_Weapon = None
        Specialist = None

        name = {}
        write = {}

    class State:
        attack_cooldown = None
        attack_frozen = None
        bribed = None
        bribed_II = None
        extra_action = None
        frozen = None
        improved_weapons = None
        improved_weapons_II_A = None
        movement_remaining = None
        lost_extra_life = None
        xp = None
        used = None
        recently_bribed = None
        sabotaged = None
        sabotaged_II = None

        name = None

    class Trait:
        berserking = None
        big_shield = None
        bloodlust = None
        cavalry_charging = None
        combat_agility = None
        defence_maneuverability = None
        double_attack_cost = None
        extra_life = None
        melee_expert = None
        melee_freeze = None
        longsword = None
        push = None
        rage = None
        rage_II = None
        scouting = None
        sharpshooting = None
        swiftness = None
        tall_shield = None
        triple_attack = None
        lancing = None
        attack_cooldown = None
        far_sighted = None
        lancing_II = None
        flag_bearing = None
        flag_bearing_II_A = None
        flag_bearing_II_B = None
        crusading = None
        crusading = None
        attack_cooldown_II = None
        crusading_II = None
        pikeman_specialist = None
        attack_skill = None
        defence_skill = None
        range_skill = None
        movement_skill = None
        fire_arrows = None
        cavalry_specialist = None
        siege_weapon_specialist = None
        flanking = None

        name = None

    class Ability:
        bribe = None
        bribe_II = None
        improve_weapons = None
        improve_weapons_II_A = None
        pikeman_specialist = None
        poison = None
        sabotage = None
        sabotage_II = None
        triple_attack = None
        poison_II = None

        name = {}
        write = {}

board_height = 8
board_width = 5
board = set(Position(column, row) for column in range(1, board_width + 1) for row in range(1, board_height + 1))

eight_directions_namedtuple = collections.namedtuple("eight_directions", [name for name in Direction.to_coordinates])
eight_directions = eight_directions_namedtuple(*(Direction(name) for name in Direction.to_coordinates))
four_directions_namedtuple = collections.namedtuple("directions", [name for name in ["Up", "Down", "Left", "Right"]])
directions = four_directions_namedtuple(*(Direction(name) for name in ["Up", "Down", "Left", "Right"]))


def distance(position1, position2):
    return position1.distance(position2)


def find_all_friendly_units_except_current(current_unit_position, player_units):
    return dict((pos, player_units[pos]) for pos in player_units if pos != current_unit_position)


def adjacent_friendly_units(position, units):
    return (units[pos] for pos in position.adjacent_tiles() if pos in units)


def adjacent_friendly_positions(position, units):
    return (pos for pos in position.adjacent_tiles() if pos in units)


def surrounding_friendly_units(position, units):
    return (units[pos] for pos in position.surrounding_tiles() if pos in units)


def assert_equal_documents(testcase, expected, actual, testcase_file):
    message = "Wrong document for " + testcase_file + "\n\n"
    message += "Expected:\n" + document_to_string(expected)
    message += "\nActual:\n" + document_to_string(actual)

    testcase.assertEqual(expected, actual, message)


class CustomJsonEncoder(JSONEncoder):
    def default(self, obj):
        if isinstance(obj, datetime):
            return str(obj.strftime("%Y-%m-%dT%H:%M:%SZ"))
        if isinstance(obj, ObjectId):
            return str(obj)
        return JSONEncoder.default(self, obj)


def document_to_string(document):
    return dumps(document, indent=4, cls=CustomJsonEncoder, sort_keys=True)


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


def readable_attributes(attributes):
    d = {}
    for key, value in attributes.items():
        if value:
            if is_trait(key):
                d[Trait.name[key]] = value
            else:
                d[State.name[key]] = value
    return d


def merge(d1, d2):
    d = d1.copy()
    d.update(d2)
    return d


def get_trait_enum_dict(dictionary):
    return dict((getattr(Trait, key), value) for key, value in dictionary.items())
