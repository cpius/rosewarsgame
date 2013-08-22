from json import JSONEncoder, dumps
from datetime import datetime
from bson.objectid import ObjectId
import collections
import functools


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
    reverse_print = dict((value, key.replace("_", " ").capitalize()) for key, value in enums.iteritems())
    enums["name"] = reverse
    enums["write"] = reverse_print
    return type('Enum', (), enums)


trait_descriptions = {
    "attack_cooldown": {
        1: "Can only attack every third turn.",
        2: "Can only attack every second turn"},
    "berserking": {
        1: "Can move 4 tiles if movement ends with an attack."},
    "big_shield": {
        1: "+2D v melee"},
    "cavalry_charging": {
        1: "All cavalry units starting their turn in the 8 surrounding tiles have +1 Movement"},
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
        1: "+3A vs Siege Weapons"},
    "cavalry_specialist": {
        1: "+1A +1D vs Cavalry"},
    "siege_weapon_specialist": {
        1: "+1A +1D vs Siege Weapons"},
    "flanking": {
        1: "+2A vs Infantry"}
}

state_descriptions = {
    "attack_frozen": "Unit cannot attack",
    "extra_action": "Whether the unit is doing its extra action.",
    "lost_extra_life": "Whether the unit has lost its extra life",
    "movement_remaining": "Movement points left for doing an extra action",
    "recently_bribed": "Whether a unit was bribed last turn.",
    "used": "Whether a unit has been used this turn.",
    "experience": "Experience.",
    "recently_upgraded": "Whether a unit was upgraded this turn"
}


effect_descriptions = {
    "bribed": {
        1: "Whether a unit is currently bribed by a Diplomat."},
    "poisoned": {
        1: "Unit cannot perform any actions."},
    "improved_weapons": {
        1: "Whether a unit currently has been the target of an improve_weapons function by a Weaponsmith."},
    "improved_weapons_II": {
        1: "Whether a unit currently has been the target of an improve_weapons_II function"},
    "sabotaged": {
        1: "Whether a unit is currently sabotaged by a Saboteur."},
}

ability_descriptions = {
    "bribe": {
        1: "You can use an opponent's unit this turn. Your opponent can't use it on his next turn. You can't bribe "
        "the same unit on your next turn. The unit gets +1A until end of turn.",
        2: "You can use an opponent's unit this turn. Your opponent can't use it on his next turn. You can't bribe "
        "the same unit on your next turn. The unit gets +2A until end of turn."},
    "improve_weapons": {
        1: "Give melee unit +3 attack, +1 defence until your next turn.",
        2: "Give melee unit +2 attack, +1 defence for two turns."},
    "pikeman_specialist": {
        1: "Pikemen do not get +1D against Hussar."},
    "poison": {
        1: "Freezes a unit for 2 turns.",
        2: "Freezes a unit for 3 turns."},
    "sabotage": {
        1: "Reduces a units defence to 0 for 1 turn.",
        2: "Reduces a units defence to 0 for 2 turns."},
    "triple_attack": {
        1: "Also hits the two diagonally nearby tiles in the attack direction."},
}

types = ["Cavalry", "Infantry", "Siege_Weapon", "Specialist"]

Trait = enum(1, *(trait for trait in dict(trait_descriptions)))

State = enum(1000, *(trait for trait in dict(state_descriptions)))

Effect = enum(2000, *(trait for trait in dict(effect_descriptions)))

Ability = enum(3000, *(ability for ability in ability_descriptions))

Type = enum(4000, *types)


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
        extra_action = None
        poisoned = None
        improved_weapons = None
        movement_remaining = None
        lost_extra_life = None
        experience = None
        used = None
        recently_bribed = None
        sabotaged = None
        recently_upgraded = None

        name = None
        write = None

    class Trait:
        berserking = None
        big_shield = None
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
        scouting = None
        sharpshooting = None
        swiftness = None
        tall_shield = None
        triple_attack = None
        lancing = None
        attack_cooldown = None
        far_sighted = None
        flag_bearing = None
        crusading = None
        crusading = None
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
        write = None

    class Ability:
        bribe = None
        improve_weapons = None
        poison = None
        sabotage = None
        triple_attack = None

        name = {}
        write = {}

    class Effect:
        bribed = None
        improved_weapons = None
        poisoned = None
        sabotaged = None

        name = {}
        write = {}


board_height = 8
board_width = 5
board = set(Position(column, row) for column in range(1, board_width + 1) for row in range(1, board_height + 1))

eight_directions_namedtuple = collections.namedtuple("eight_directions", [name for name in Direction.to_coordinates])
eight_directions = eight_directions_namedtuple(*(Direction(name) for name in Direction.to_coordinates))
four_directions_namedtuple = collections.namedtuple("directions", [name for name in ["Up", "Down", "Left", "Right"]])
directions = four_directions_namedtuple(*(Direction(name) for name in ["Up", "Down", "Left", "Right"]))


def get_description(attribute, level=1):
    if attribute in Effect.name:
        return effect_descriptions[Effect.name[attribute]][level]
    elif attribute in State.name:
        return state_descriptions[State.name[attribute]][level]
    elif attribute in Ability.name:
        return ability_descriptions[Ability.name[attribute]][level]
    elif attribute in Trait.name:
        if attribute == Trait.attack_skill:
            return str(level) + " added to base attack"
        if attribute == Trait.defence_skill:
            return str(level) + " added to base defence"
        if attribute == Trait.movement_skill:
            return str(level) + " added to base movement"
        if attribute == Trait.range_skill:
            return str(level) + " added to base range"

        return trait_descriptions[Trait.name[attribute]][level]


def distance(position1, position2):
    return position1.distance(position2)


def units_excluding_position(player_units, position):
    return dict((pos, player_units[pos]) for pos in player_units if pos != position)


def adjacent_units(position, units):
    return [units[pos] for pos in position.adjacent_tiles() if pos in units]


def surrounding_units(position, units):
    return [units[pos] for pos in position.surrounding_tiles() if pos in units]


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


def readable(attributes):
    if isinstance(attributes, int):
        if attributes in Trait.name:
            return Trait.name[attributes].title()
        if attributes in Ability.name:
            return Ability.name[attributes].title()
        if attributes in Effect.name:
            return Effect.name[attributes].title()
        if attributes in State.name:
            return State.name[attributes].title()

    dictionary = {}
    for key, info in attributes.items():
        if key in Trait.name:
            if info[1]:
                dictionary[Trait.name[key]] = info[1]
        elif key in Ability.name:
            if info[1]:
                dictionary[Ability.name[key]] = info[1]
        elif key in State.name:
            if info[0]:
                dictionary[State.name[key]] = info[0]
        elif key in Effect.name:
            if info[1] == 1:
                dictionary[Effect.name[key]] = info[0]
            elif info[1]:
                dictionary[Effect.name[key]] = {"value": info[0], "level": info[1]}

    return dictionary


def merge(first_dictionary, second_dictionary, third_dictionary=None, fourth_dictionary=None):
    merged_dictionary = first_dictionary.copy()
    merged_dictionary.update(second_dictionary)

    if third_dictionary:
        merged_dictionary.update(third_dictionary)

    if fourth_dictionary:
        merged_dictionary.update(fourth_dictionary)

    return merged_dictionary


def enum_attributes(attributes):
    dictionary = {}

    for attribute, value in attributes.items():
        if attribute in Trait.name.values():
            dictionary[getattr(Trait, attribute)] = value
        elif attribute in Ability.name.values():
            dictionary[getattr(Ability, attribute)] = value
        else:
            dictionary[getattr(State, attribute)] = value

    return dictionary


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
