from json import JSONEncoder, dumps
from datetime import datetime
from bson.objectid import ObjectId
import collections
import functools
from dictdiffer import DictDiffer
import random
from collections import namedtuple


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
        return set(pos for pos in direction.perpendicular(self) + direction.forward_and_sideways(self) if pos in board)

    def surrounding_tiles(self):
        return set(pos for pos in [direction.move(self) for direction in eight_directions] if pos in board)

    def adjacent_tiles(self):
        return set(pos for pos in [direction.move(self) for direction in directions] if pos in board)

    def two_forward_tiles(self, direction):
        return set(pos for pos in direction.forward_and_sideways(self) if pos in board)


def enum(n, *sequential, **named):
    enums = dict(zip(sequential, range(n, len(sequential) + n)), **named)
    reverse = dict((value, key) for key, value in enums.iteritems())
    reverse_print = dict((value, key.replace("_", " ").capitalize()) for key, value in enums.iteritems())
    enums["get_enum"] = enums
    enums["name"] = reverse
    enums["write"] = reverse_print
    return type('Enum', (), enums)

rolls = namedtuple("rolls", ["attack", "defence"])

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
    "flanked": {
        1: "This unit was attacked by a unit with flanking last turn."},
    "ride_through": {
        1: "If there is an enemy unit next to it, and the tile behind that unit is empty, it can make an attack where it"
           "ends up on this empty tile. Zone of control has no effect on this ability."},
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
    "recently_bribed": "Whether a unit was bribed last turn."
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

unit_descriptions = {
    "Archer": "Archer",
    "Ballista": "Ballista",
    "Catapult": "Catapult",
    "Knight": "Knight",
    "Light_Cavalry": "Light Cavalry",
    "Pikeman": "Pikeman",
    "Berserker": "Berserker",
    "Cannon": "Cannon",
    "Crusader": "Crusader",
    "Flag_Bearer": "Flag Bearer",
    "Longswordsman": "Longswordsman",
    "Saboteur": "Saboteur",
    "Royal_Guard": "Royal Guard",
    "Scout": "Scout",
    "War_Elephant": "War Elephant",
    "Weaponsmith": "Weaponsmith",
    "Viking": "Viking",
    "Diplomat": "Diplomat",
    "Halberdier": "Halberdier",
    "Hussar": "Hussar",
    "Flanking_Cavalry": "Flanking Cavalry",
    "Hobelar": "Hobelar",
    "Lancer": "Lancer",
    "Fencer": "Fencer",
    "Assassin": "Assassin",
    "Trebuchet": "Trebuchet",
    "Javeliner": "Javeliner"
}


types = ["Cavalry", "Infantry", "War_Machine", "Specialist"]

Trait = enum(1000, *(trait for trait in dict(trait_descriptions)))

State = enum(2000, *(state for state in dict(state_descriptions)))

Effect = enum(3000, *(effect for effect in dict(effect_descriptions)))

Ability = enum(4000, *(ability for ability in ability_descriptions))

Type = enum(1, *types)

Unit = enum(1, *(unit for unit in unit_descriptions))

Opponent = enum(1, *(opponent for opponent in dict(opponent_descriptions)))

AI = enum(1, *(ai for ai in dict(ai_descriptions)))

if 1 == 2:
    class Type:
        Cavalry = None
        Infantry = None
        War_Machine = None
        Specialist = None

        name = {}
        write = {}
        get_enum = {}

    class State:
        attack_cooldown = None
        bribed = None
        extra_action = None
        improved_weapons = None
        movement_remaining = None
        lost_extra_life = None
        experience = None
        used = None
        recently_bribed = None
        sabotaged = None
        recently_upgraded = None
        javelin_thrown = None

        name = None
        write = None

    class Trait:
        berserking = None
        big_shield = None
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
        war_machine_specialist = None
        flanking = None
        flanked = None
        ride_through = None
        spread_attack = None
        javelin = None

        name = None
        write = None

    class Ability:
        bribe = None
        improve_weapons = None
        poison = None
        sabotage = None
        assassinate = None

        name = {}
        write = {}

    class Effect:
        attack_frozen = None
        bribed = None
        improved_weapons = None
        poisoned = None
        sabotaged = None

        name = {}
        write = {}

    class Unit:
        Archer = None
        Ballista = None
        Catapult = None
        Knight = None
        Light_Cavalry = None
        Pikeman = None
        Berserker = None
        Cannon = None
        Crusader = None
        Flag_Bearer = None
        Longswordsman = None
        Saboteur = None
        Royal_Guard = None
        Scout = None
        War_Elephant = None
        Weaponsmith = None
        Viking = None
        Diplomat = None
        Halberdier = None
        Hussar = None
        Flanking_Cavalry = None
        Hobelar = None
        Lancer = None
        Fencer = None
        Assassin = None
        Trebuchet = None
        Javeliner = None

        name = {}
        write = {}
        get_enum = {}

    class Opponent:
        HotSeat = None
        AI = None
        Internet = None
        Load = None

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
    for attribute, value in attributes.items():
        if attribute in Trait.name:
            dictionary[Trait.name[attribute]] = value
        elif attribute in Ability.name:
            dictionary[Ability.name[attribute]] = value
        elif attribute in State.name:
            dictionary[State.name[attribute]] = value
        elif attribute in Effect.name:
            dictionary[Effect.name[attribute]] = list(value)

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
        elif attribute in Effect.name.values():
            dictionary[getattr(Effect, attribute)] = value
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


def unit_with_trait_at(pos, trait, units, level=None):
    return pos in units and units[pos].has(trait, level)


def get_rolls():
    return rolls(random.randint(1, 6), random.randint(1, 6))


