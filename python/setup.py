from __future__ import division
import random
from setup_settings import *
from common import *
from units import Unit


class Tiles_bag(object):
    def __init__(self):
        self.tiles = [Position(column, row) for column in board_columns for row in board_rows]
        
    def pick_from_row(self, rows):
        pick = random.choice([tile for tile in self.tiles if tile.row in rows])
        self.tiles.remove(pick)
        return pick

    def pick_protected_tile(self, rows):
        possible_tiles = [Position(column, row) for column in board_columns for
                          row in [2, 3] if Position(column, row) in self.tiles and
                          Position(column, row + 1) not in self.tiles]

        pick = random.choice([tile for tile in possible_tiles if tile.row in rows])
        self.tiles.remove(pick)
        return pick


class Unit_bag(object):
    def __init__(self, units):
        self.units = list(units)
    
    def pick(self):
        pick = random.choice(self.units)
        self.units.remove(pick)
        return pick
    
    def has_units(self):
        return self.units

    def remove_units(self, name_list):
        self.units = [unit for unit in self.units if unit not in name_list]

    def remove_one_unit(self, name):
        self.units.remove(name)


board_rows = [1, 2, 3, 4]
board_columns = [1, 2, 3, 4, 5]

siege_weapons = ["Ballista", "Catapult", "Cannon"]


def at_least_two_column_blocks(units):
    """ Tests whether there on each column are at least two 'blocks'.
    A block is either a unit, or a Pikeman zoc tile. """
    
    columns = [position.column + x for x in [-1, +1] for position, unit in units.items() if unit.name == "Pikeman"] + \
              [position.column for position in units]

    return not any(columns.count(column) < 2 for column in board_columns)
     

def at_most_one_pikeman_per_column(units):
    columns = [position.column for position, unit in units.items() if unit.name == "Pikeman"]
    
    return not any(columns.count(column) > 1 for column in board_columns)


def at_least_one_siege_weapon(units):
    return any(unit.name in siege_weapons for unit in units.values())


def at_most_two_siege_weapons(units):
    return sum(1 for unit in units.values() if unit.name in siege_weapons) <= 2


def get_units():
    
    def select_basic_units(basic_units_bag):
        return [Unit.make(basic_units_bag.pick()) for _ in range(basic_unit_count)]

    def select_special_units(special_units_first_bag, special_units_second_bag):

        special_units = []
        while len(special_units) < special_unit_count and special_units_first_bag.has_units():
            unit = Unit.make(special_units_first_bag.pick())
            special_units.append(unit)

        while len(special_units) < special_unit_count:
            special_units.append(Unit.make(special_units_second_bag.pick()))

        return special_units

    def fill_bags():
        
        basic_units_bag = Unit_bag([name for name in allowed_basic_units for _ in range(units_info[name].copies)])
        special_units_first_bag = Unit_bag(required_special_units)
        special_units_second_bag = Unit_bag(set(allowed_special_units) - set(required_special_units))
        tiles_bag = Tiles_bag()
        
        return basic_units_bag, special_units_first_bag, special_units_second_bag, tiles_bag

    def place_units_on_board(units_list, tiles_bag):

        units = {}
        unprotected_units = [unit for unit in units_list if not units_info[unit.name].protection_required]
        protected_units = [unit for unit in units_list if units_info[unit.name].protection_required]

        for unit in unprotected_units:
            allowed_rows = units_info[unit.name].allowed_rows.copy()
            position = tiles_bag.pick_from_row(allowed_rows)
            units[position] = unit

        for unit in protected_units:
            position = tiles_bag.pick_protected_tile(units_info[unit.name].allowed_rows)
            units[position] = unit

        return units

    while True:

        basic_units_bag, special_units_first_bag, special_units_second_bag, tiles_bag = fill_bags()
        
        try:
            basic_units = select_basic_units(basic_units_bag)
            special_units = select_special_units(special_units_first_bag, special_units_second_bag)

            units = place_units_on_board(basic_units + special_units, tiles_bag)

        # This happens if a unit is picked from the unit bag, but there isn't any tile it can be placed on
        except IndexError:
            continue

        if any(not globals()[requirement](units) for requirement in requirements):
            continue
             
        return units


def get_start_units():

    player1_units = get_units()
    player2_units = flip_units(get_units())

    return player1_units, player2_units
