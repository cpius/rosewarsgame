import random
from gamestate.gamestate_library import Unit, Position, board_tiles, Type, flip_units
from gamestate.units import base_units
from collections import namedtuple
from game.settings import version, required_special_unit_set, beginner_mode

Info = namedtuple("Info", ["allowed_rows", "copies", "protection_required"])

units_info = {Unit.Archer: Info({2, 3}, 3, False),
              Unit.Assassin: Info({1}, 1, True),
              Unit.Trebuchet: Info({3}, 1, True),
              Unit.Ballista: Info({2, 3}, 1, True),
              Unit.Catapult: Info({2, 3}, 1, False),
              Unit.Knight: Info({3, 4}, 3, False),
              Unit.Light_Cavalry: Info({2, 3}, 3, False),
              Unit.Pikeman: Info({2, 3}, 2, False),
              Unit.Berserker: Info({2}, 1, False),
              Unit.Cannon: Info({2}, 1, True),
              Unit.Halberdier: Info({4}, 1, False),
              Unit.Hobelar: Info({3, 4}, 1, False),
              Unit.Hussar: Info({3, 4}, 1, False),
              Unit.Flanking_Cavalry: Info({3, 4}, 1, False),
              Unit.Crusader: Info({3, 4}, 1, False),
              Unit.Diplomat: Info({2, 3}, 1, False),
              Unit.Flag_Bearer: Info({3, 4}, 1, False),
              Unit.Lancer: Info({3, 4}, 1, False),
              Unit.Javeliner: Info({3, 4}, 1, False),
              Unit.Longswordsman: Info({4}, 1, False),
              Unit.Royal_Guard: Info({2, 3}, 1, False),
              Unit.Saboteur: Info({2, 3}, 1, True),
              Unit.Fencer: Info({4}, 1, False),
              Unit.Scout: Info({2, 3}, 1, False),
              Unit.Viking: Info({4}, 1, False),
              Unit.War_Elephant: Info({4}, 1, False),
              Unit.Weaponsmith: Info({2, 3}, 1, True)}

basic_unit_set = {
    Unit.Archer, Unit.Ballista, Unit.Catapult, Unit.Knight, Unit.Light_Cavalry, Unit.Pikeman}

if version == 1.1:
    special_unit_set = {
        Unit.Berserker, Unit.Cannon, Unit.Crusader, Unit.Flag_Bearer, Unit.Longswordsman, Unit.Scout, Unit.Viking,
        Unit.Hobelar, Unit.Halberdier, Unit.Flanking_Cavalry, Unit.Hussar, Unit.Lancer, Unit.Royal_Guard,
        Unit.Javeliner, Unit.Trebuchet, Unit.War_Elephant, Unit.Fencer, Unit.Saboteur, Unit.Diplomat, Unit.Assassin,
        Unit.Weaponsmith}

if version == 1.0:
    special_unit_set = {
        Unit.Berserker, Unit.Cannon, Unit.Crusader, Unit.Flag_Bearer, Unit.Longswordsman, Unit.Scout, Unit.Viking,
        Unit.Hobelar}

if beginner_mode:
    basic_unit_count, special_unit_count = 9, 0
else:
    basic_unit_count, special_unit_count = 6, 3

board_columns = [1, 2, 3, 4, 5]

melee_units = [unit for unit in special_unit_set & basic_unit_set if base_units[unit].range == 1]


class TilesBag(object):
    def __init__(self):
        self.tiles = board_tiles.copy()
        
    def pick_from_row(self, rows):
        pick = random.choice([tile for tile in self.tiles if tile.row in rows])
        self.tiles.remove(pick)
        return pick

    def pick_protected_tile(self, rows):
        possible_tiles = [Position(column, row) for column in board_columns for row in [1, 2, 3]
                          if Position(column, row) in self.tiles and (Position(column, row + 1) not in self.tiles
                          or Position(column, row + 2) not in self.tiles)]

        pick = random.choice([tile for tile in possible_tiles if tile.row in rows])
        self.tiles.remove(pick)
        return pick


class UnitBag(object):
    def __init__(self, units):
        self.units = list(units)
    
    def pick(self, n=1):
        units = []
        for _ in range(n):
            pick = random.choice(self.units)
            self.units.remove(pick)
            units.append(pick)
        return units
    
    def has_units(self):
        return self.units


def place_units_on_board(units_list):
    """
    :param units_list: A list of players units
    :return: A dictionary with board positions as keys and the units placed there as values.
    Units with protection_required has to stand behind a friendly unit.
    """
    tiles_bag = TilesBag()
    units = {}
    unprotected_units = [unit for unit in units_list if not units_info[unit].protection_required]
    protected_units = [unit for unit in units_list if units_info[unit].protection_required]

    for unit in unprotected_units:
        position = tiles_bag.pick_from_row(units_info[unit].allowed_rows)
        units[position] = unit

    for unit in protected_units:
        position = tiles_bag.pick_protected_tile(units_info[unit].allowed_rows)
        units[position] = unit

    return units


def fill_bag(unit_set):
    """
    :param unit_set: A set of units
    :return: A UnitBag with the desired number of copies of each unit.
    """
    return UnitBag([unit for unit in unit_set for _ in range(units_info[unit].copies)])


def select_units():
    """
    :return: A list of units to be placed on the board.
    Basic units are drawn from a bag with 2-3 copies of each unit, thus decreasing the chance of getting many of the
    same unit. Special units are drawn in the same manner, but the number of copies is currently set to 1 for all special
    units.
    required_special_units can be specified in settings. If so these are drawn first, and remaining special unit slots
    are filled normally.
    """
    basic_units_bag = fill_bag(basic_unit_set)
    special_units_bag = fill_bag(special_unit_set - required_special_unit_set)
    required_special_units_bag = fill_bag(required_special_unit_set)

    basic_units = basic_units_bag.pick(basic_unit_count)

    special_units = []
    while len(special_units) < special_unit_count and required_special_units_bag.has_units():
        special_units += required_special_units_bag.pick()
    while len(special_units) < special_unit_count:
        special_units += special_units_bag.pick()

    return basic_units + special_units


def at_least_n_column_blocks(units, n):
    blocks = ([pos.column + n for n in [-1, +1] for pos, unit in units.items() if unit.unit == Unit.Pikeman] +
              [pos.column for pos in units])

    return all(blocks.count(column) >= n for column in board_columns)


def at_least_two_column_blocks(units):
    """
    :param units: The units of one player
    :return: False if there is a column that has less than two "blocks". A block is either a unit, or a tile that is
    under ZOC by a Pikeman.
    """
    return at_least_n_column_blocks(units, 2)


def at_least_one_column_block(units):
    """
    :param units: The units of one player
    :return: False if there is a column that has less than one "blocks". A block is either a unit, or a tile that is
    under ZOC by a Pikeman.
    """
    return at_least_n_column_blocks(units, 1)


def at_most_one_pikeman_per_column(units):
    """
    :param units: The units of one player
    :return: False if there is a column with more than one Pikeman.
    """
    return not any(column for column in board_columns if
                   sum(1 for pos, unit in units.items() if pos.column == column and unit.unit == Unit.Pikeman) > 1)


def no_pikemen_on_the_edges(units):
    """
    :param units: The units of one player
    :return: False if there is a Pikeman on the first or fifth column.
    """
    return not any(pos.column in [1, 5] and unit.unit == Unit.Pikeman for pos, unit in units.items())


def at_least_one_war_machine(unit_list):
    """
    :param unit_list: A list of unit enums
    :return: False if there are no basic War Machines
    """
    return Unit.Ballista in unit_list or Unit.Catapult in unit_list


def at_least_one_pikeman(unit_list):
    """
    :param unit_list: A list of unit enums
    :return: False if there are no Pikemen
    """
    return Unit.Pikeman in unit_list


def at_least_five_melee_with_weaponsmith(unit_list):
    """
    :param unit_list: A list of unit enums
    :return: False if Weaponsmith is in the units and there is less than 5 melee units it can be used on.
    """
    return not (Unit.Weaponsmith in unit_list and sum(1 for unit in unit_list if unit in melee_units) < 5)


draw_requirements = {at_least_one_war_machine, at_least_five_melee_with_weaponsmith, at_least_one_pikeman}

placement_requirements = {at_least_two_column_blocks, at_most_one_pikeman_per_column, no_pikemen_on_the_edges}


def draw_units():
    """
    :return: A list of unit enums fulfilling draw_requirements
    """
    while True:
        unit_list = select_units()
        if all(requirement(unit_list) for requirement in draw_requirements):
            return unit_list


def place_units(unit_list):
    """
    :param unit_list: A list of unit enums
    :return: A list of units placed on the board, fulfilling placement_requirements. If unsuccesful after 1000 attemps,
    return an empty list.
    """
    attempts_at_placement = 0
    while True:
        attempts_at_placement += 1
        if attempts_at_placement > 1000:
            return None

        try:
            units = place_units_on_board(unit_list)

        # If there isn't an appropriate tile to place the unit on, start over.
        except IndexError:
            continue

        # After successful placement, Unit objects are created.
        for position, unit in units.items():
            units[position] = base_units[unit]()

        # Test if all requirements for the setup are fulfilled, otherwise start over.
        if any(not requirement(units) for requirement in placement_requirements):
            continue

        return units


def get_units():
    """
    :return: The units of one player, drawn semi-randomly and placed on the board semi-randomly.
    """
    while True:
        unit_list = draw_units()

        units = place_units(unit_list)
        if not units:
            continue

        return units


def get_start_units():

    player1_units = get_units()
    player2_units = flip_units(get_units())

    return player1_units, player2_units
