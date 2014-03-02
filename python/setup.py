from __future__ import division
import random
from common import *
from units import Unit
from collections import namedtuple

required_special_units = []

requirements = ["at_least_two_column_blocks", "at_most_one_pikeman_per_column", "at_least_one_war_machine",
                "at_most_two_war_machines", "at_least_five_melee_with_weaponsmith"]

Info = namedtuple("Info", ["allowed_rows", "copies", "protection_required"])

units_info = {"Archer": Info({2, 3}, 3, False),
              "Assassin": Info({1}, 1, True),
              "Trebuchet": Info({2, 3}, 1, True),
              "Ballista": Info({2, 3}, 2, True),
              "Catapult": Info({2, 3}, 2, False),
              "Knight": Info({4}, 3, False),
              "Light Cavalry": Info({2, 3}, 3, False),
              "Pikeman": Info({2, 3, 4}, 3, False),
              "Berserker": Info({2, 3}, 1, False),
              "Cannon": Info({2}, 1, True),
              "Halberdier": Info({4}, 1, False),
              "Hobelar": Info({3, 4}, 1, False),
              "Hussar": Info({3, 4}, 1, False),
              "Flanking Cavalry": Info({3, 4}, 1, False),
              "Crusader": Info({3, 4}, 1, False),
              "Diplomat": Info({2, 3}, 1, False),
              "Flag Bearer": Info({3, 4}, 1, False),
              "Lancer": Info({3, 4}, 1, False),
              "Javeliner": Info({3, 4}, 1, False),
              "Longswordsman": Info({4}, 1, False),
              "Royal Guard": Info({2, 3}, 1, False),
              "Saboteur": Info({2, 3}, 1, True),
              "Samurai": Info({4}, 1, False),
              "Scout": Info({2, 3}, 1, False),
              "Viking": Info({4}, 1, False),
              "War Elephant": Info({4}, 1, False),
              "Weaponsmith": Info({2, 3}, 1, True),
              "Crossbow Archer": Info({2, 3}, 3, False),
              "Fire Archer": Info({2, 3}, 3, False)}

board_rows = [1, 2, 3, 4]
board_columns = [1, 2, 3, 4, 5]


class Tiles_bag(object):
    def __init__(self):
        self.tiles = board.copy()
        
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


class Unit_bag(object):
    def __init__(self, units):
        self.units = list(units)
    
    def pick(self):
        pick = random.choice(self.units)
        self.units.remove(pick)
        return pick
    
    def has_units(self):
        return self.units


def at_least_two_column_blocks(units):
    """ Tests whether there on each column are at least two 'blocks'.
    A block is either a unit, or a Pikeman zoc tile. """
    
    blocks = [pos.column + n for n in [-1, +1] for pos, unit in units.items() if unit.zoc] + \
             [pos.column for pos in units]

    return all(blocks.count(column) >= 2 for column in board_columns)
     

def at_most_one_pikeman_per_column(units):
    return not any(column for column in board_columns if sum(1 for pos, unit in units.items() if
                                                             pos.column == column and unit.zoc) > 1)


def at_least_one_war_machine(units):
    return any(unit.type == Type.War_Machine for unit in units.values())


def at_most_two_war_machines(units):
    return sum(1 for unit in units.values() if unit.type == Type.War_Machine) <= 2


def at_least_five_melee_with_weaponsmith(units):
    return not any(unit.name == "Weaponsmith" for unit in units.values()) or \
        sum(1 for unit in units.values() if unit.range == 1) >=5


def get_units():

    if get_setting("Beginner_mode"):
        basic_unit_count, special_unit_count = 9, 0
    else:
        basic_unit_count, special_unit_count = 6, 3
    
    def select_basic_units(basic_units_bag):
        return [basic_units_bag.pick() for _ in range(basic_unit_count)]

    def select_special_units(special_units_first_bag, special_units_second_bag):
        special_units = []
        while len(special_units) < special_unit_count and special_units_first_bag.has_units():
            special_units.append(special_units_first_bag.pick())

        while len(special_units) < special_unit_count:
            special_units.append(special_units_second_bag.pick())

        return special_units

    def fill_bags():
        
        basic_units_bag = Unit_bag([name for name in allowed_basic_units for _ in range(units_info[name].copies)])
        special_units_first_bag = Unit_bag(required_special_units)
        special_units_second_bag = Unit_bag(set(allowed_special_units) - set(required_special_units))
        tiles_bag = Tiles_bag()
        
        return basic_units_bag, special_units_first_bag, special_units_second_bag, tiles_bag

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

    while True:

        basic_units_bag, special_units_first_bag, special_units_second_bag, tiles_bag = fill_bags()
        
        try:
            basic_units = select_basic_units(basic_units_bag)
            special_units = select_special_units(special_units_first_bag, special_units_second_bag)

            units = place_units_on_board(basic_units + special_units, tiles_bag)

        # This happens if a unit is picked from the unit bag, but there isn't any tile it can be placed on
        except IndexError:
            continue

        for position, unit in units.items():
            units[position] = Unit.make(unit)

        if any(not globals()[requirement](units) for requirement in requirements):
            continue

        return units


def get_start_units():

    player1_units = get_units()
    player2_units = flip_units(get_units())

    return player1_units, player2_units
