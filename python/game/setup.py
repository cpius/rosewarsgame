import random
from gamestate.gamestate_library import Unit, Position, board_tiles, Type, flip_units
from gamestate.units import Unit_class
from collections import namedtuple
from game.game_library import *


Info = namedtuple("Info", ["allowed_rows", "copies", "protection_required"])

units_info = {Unit.Archer: Info({2, 3}, 3, False),
              Unit.Assassin: Info({1}, 1, True),
              Unit.Trebuchet: Info({3}, 1, True),
              Unit.Ballista: Info({2, 3}, 2, True),
              Unit.Catapult: Info({2, 3}, 2, False),
              Unit.Knight: Info({4}, 3, False),
              Unit.Light_Cavalry: Info({2, 3}, 3, False),
              Unit.Pikeman: Info({2, 3, 4}, 3, False),
              Unit.Berserker: Info({2, 3}, 1, False),
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

if get_setting("version") == "1.1":
    allowed_special_units = {
        Unit.Berserker, Unit.Cannon, Unit.Crusader, Unit.Flag_Bearer, Unit.Longswordsman, Unit.Scout, Unit.Viking,
        Unit.Hobelar, Unit.Halberdier, Unit.Flanking_Cavalry, Unit.Hussar, Unit.Lancer, Unit.Royal_Guard,
        Unit.Javeliner, Unit.Trebuchet, Unit.War_Elephant, Unit.Fencer, Unit.Saboteur, Unit.Diplomat, Unit.Assassin,
        Unit.Weaponsmith
    }
    allowed_basic_units = {
        Unit.Archer, Unit.Ballista, Unit.Catapult, Unit.Knight, Unit.Light_Cavalry, Unit.Pikeman
    }
    required_special_units = {}

if get_setting("version") == "1.0":
    allowed_special_units = {
        Unit.Berserker, Unit.Cannon, Unit.Crusader, Unit.Flag_Bearer, Unit.Longswordsman, Unit.Scout, Unit.Viking,
        Unit.Hobelar}
    allowed_basic_units = {
        Unit.Archer, Unit.Ballista, Unit.Catapult, Unit.Knight, Unit.Light_Cavalry, Unit.Pikeman}
    required_special_units = {}

if get_setting("Beginner_mode"):
    basic_unit_count, special_unit_count = 9, 0
else:
    basic_unit_count, special_unit_count = 6, 3

board_rows = [1, 2, 3, 4]
board_columns = [1, 2, 3, 4, 5]


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
    
    def pick(self):
        pick = random.choice(self.units)
        self.units.remove(pick)
        return pick
    
    def has_units(self):
        return self.units


def place_units_on_board(units_list, tiles_bag):

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


def select_basic_units(basic_units_bag):
    return [basic_units_bag.pick() for _ in range(basic_unit_count)]


def select_special_units(special_units_first_bag, special_units_second_bag):
    special_units = []
    while len(special_units) < special_unit_count and special_units_first_bag.has_units():
        special_units.append(special_units_first_bag.pick())

    while len(special_units) < special_unit_count:
        special_units.append(special_units_second_bag.pick())

    return special_units


def fill_unit_bags():

    basic_unit_bag = UnitBag([name for name in allowed_basic_units for _ in range(units_info[name].copies)])
    special_unit_required_bag = UnitBag(required_special_units)
    special_unit_bag = UnitBag(set(allowed_special_units) - set(required_special_units))

    return basic_unit_bag, special_unit_required_bag, special_unit_bag


def at_least_two_column_blocks(units):
    """
    :param units: The units of one player
    :return: Boolean of whether each column has at least two blocks. A block is either a unit, or a tile that is under
    ZOC by a Pikeman.
    """
    blocks = [pos.column + n for n in [-1, +1] for pos, unit in units.items() if unit.name == "Pikeman"] + \
             [pos.column for pos in units]

    return all(blocks.count(column) >= 2 for column in board_columns)
     

def at_most_one_pikeman_per_column(units):
    return not any(column for column in board_columns if
                   sum(1 for pos, unit in units.items() if pos.column == column and unit.zoc) > 1)


def at_least_one_war_machine(units):
    return any(unit.type == Type.War_Machine for unit in units.values())


def at_most_two_war_machines(units):
    return sum(1 for unit in units.values() if unit.type == Type.War_Machine) <= 2


def at_least_five_melee_with_weaponsmith(units):
    """
    :param units: The units of one player
    :return: False if Weaponsmith is in the units, and there is not at least 5 melee units it can be used on.
    """
    return not any(unit.unit == Unit.Weaponsmith for unit in units.values()) or \
        sum(1 for unit in units.values() if unit.range == 1) >= 5

requirements = [at_least_two_column_blocks, at_most_one_pikeman_per_column, at_least_one_war_machine,
                at_most_two_war_machines, at_least_five_melee_with_weaponsmith]


def get_units():
    """
    :return: The units of one player, drawn semi-randomly and placed on the board semi-randomly.
    """

    while True:

        # Special units that can be picked and placed on the board.
        basic_unit_bag, special_unit_required_bag, special_unit_bag = fill_unit_bags()

        # The tiles on the board
        tiles_bag = TilesBag()

        # Selects units from the bags and place them on board.
        try:
            special_units = select_special_units(special_unit_required_bag, special_unit_bag)
            basic_units = select_basic_units(basic_unit_bag)

            units = place_units_on_board(basic_units + special_units, tiles_bag)

        # This happens if a unit is picked from the unit bag, but there isn't any tile it can be placed on
        except IndexError:
            continue

        # After successful placement, Unit objects are created.
        for position, unit in units.items():
            units[position] = Unit_class.make(unit)

        # Test if all requirements for the setup are fulfilled, otherwise try again.
        if any(not requirement(units) for requirement in requirements):
            continue

        return units


def get_start_units():

    player1_units = get_units()
    player2_units = flip_units(get_units())

    return player1_units, player2_units
