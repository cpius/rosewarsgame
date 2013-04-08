from __future__ import division
import random
import units as units_module
import settings
from collections import namedtuple


class Tiles_bag(object):
    def __init__(self):
        self.tiles = [(column, row) for column in board_columns for row in board_rows]
        
    def pick_from_row(self, rows):
        pick = random.choice([tile for tile in self.tiles if tile[1] in rows])
        self.tiles.remove(pick)
        return pick

    def pick_protected_tile(self, rows):
        possible_tiles = [(coloumn, row) for coloumn in board_columns for
                          row in [2, 3] if (coloumn, row) in self.tiles and (coloumn, row + 1) not in self.tiles]

        pick = random.choice([tile for tile in possible_tiles if tile[1] in rows])
        self.tiles.remove(pick)
        return pick


class Unit_bag(object):
    def __init__(self, units):
        self.units = units
    
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

Info = namedtuple("Info", ["allowed_rows", "copies_in_bag", "protection_required"])

units_info = {"Archer": Info({2, 3}, 3, False),
              "Ballista": Info({2, 3}, 2, True),
              "Catapult": Info({2, 3}, 2, False),
              "Heavy Cavalry": Info({4}, 3, False),
              "Light Cavalry": Info({2, 3}, 3, False),
              "Pikeman": Info({2, 3, 4}, 3, False),
              "Berserker": Info({2, 3}, 1, False),
              "Cannon": Info({2}, 1, True),
              "Chariot": Info({3, 4}, 1, False),
              "Crusader": Info({3, 4}, 1, False),
              "Diplomat": Info({2, 3}, 1, False),
              "Flag Bearer": Info({3, 4}, 1, False),
              "Lancer": Info({3, 4}, 1, False),
              "Longswordsman": Info({4}, 1, False),
              "Royal Guard": Info({2, 3}, 1, False),
              "Saboteur": Info({2, 3}, 1, True),
              "Samurai": Info({4}, 1, False),
              "Scout": Info({2, 3}, 1, False),
              "Viking": Info({4}, 1, False),
              "War Elephant": Info({4}, 1, False),
              "Weaponsmith": Info({2, 3}, 1, True)}


def test_coloumn_blocks(units):
    """ Tests whether there on each coloumn are at least two 'blocks'.
    A block is either a unit, or a Pikeman zoc tile. """
    
    columns = [position[0] + x for x in [-1, +1] for position, unit in units.items() if unit.name == "Pikeman"]\
        + [position[0] for position in units]

    return not any(columns.count(column) < 2 for column in board_columns)
     

def test_pikeman_coloumn(units):
    """ Tests whether there is more than one Pikeman on any coloumn."""
    
    columns = [position[0] for position, unit in units.items() if unit.name == "Pikeman"]
    
    return not any(columns.count(column) > 1 for column in board_columns)


def enforce_max_siege_weapons(units, unit_bag):

    siege_count = sum(1 for unit in units if unit.name in siege_weapons)

    if siege_count >= 2:
        unit_bag.remove_units(siege_weapons)


def get_units():
    
    def select_basic_units(basic_units_bag):

        units = []

        if settings.at_least_one_siege_weapon:
            unit_name = random.choice(["Ballista", "Catapult"])
            units.append(getattr(units_module, unit_name.replace(" ", "_"))())
            basic_units_bag.remove_one_unit("Ballista")
            basic_units_bag.remove_one_unit("Catapult")


        while len(units) < settings.basic_unit_count:

            if settings.max_two_siege_weapons:
                enforce_max_siege_weapons(units, basic_units_bag)

            unit_name = basic_units_bag.pick()
            units.append(getattr(units_module, unit_name.replace(" ", "_"))())

        random.shuffle(units)
        units[0].attack_counters = 1
        units[1].defence_counters = 1

        return units

    def select_special_units(special_units_first_bag, special_units_second_bag, units):

        total_unit_count = settings.basic_unit_count + settings.special_unit_count

        while len(units) < total_unit_count and special_units_first_bag.has_units():

            if settings.max_two_siege_weapons:
                enforce_max_siege_weapons(units, special_units_first_bag)

            unit_name = special_units_first_bag.pick()
            units.append(getattr(units_module, unit_name.replace(" ", "_"))())

        while len(units) < total_unit_count:

            if settings.max_two_siege_weapons:
                enforce_max_siege_weapons(units, special_units_second_bag)

            unit_name = special_units_second_bag.pick()
            units.append(getattr(units_module, unit_name.replace(" ", "_"))())

        return units

    def fill_bags():
        
        basic_units_bag = Unit_bag([name for name in settings.basic_units for _ in
                                    range(units_info[name].copies_in_bag)])
        
        special_units_first_bag = Unit_bag(list(settings.required_special_units))
        
        special_units_second_bag = Unit_bag(list(set(settings.allowed_special_units) -
                                                 set(settings.required_special_units)))

        tiles_bag = Tiles_bag()
        
        return basic_units_bag, special_units_first_bag, special_units_second_bag, tiles_bag
        
    while True:
        
        basic_units_bag, special_units_first_bag, special_units_second_bag, tiles_bag = fill_bags()
        
        try:
            unitslist = select_basic_units(basic_units_bag)
            unitslist = select_special_units(special_units_first_bag, special_units_second_bag, unitslist)

            units = place_units_on_board(unitslist, tiles_bag)

        except IndexError:
            continue

        if any(not requirement(units) for requirement in [test_coloumn_blocks, test_pikeman_coloumn]):
            continue
             
        return units


def flip_units(units):
    
    def flip(position):
        return position[0], 9 - position[1]
    
    return dict((flip(position), unit) for position, unit in units.items())


def get_start_units():

    player1_units = get_units()
    player2_units = flip_units(get_units())
    
    return player1_units, player2_units
