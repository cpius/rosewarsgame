from __future__ import division
import random
import units
import settings
from player import Player


class Tiles_bag(object):
    def __init__(self):
        self.tiles = [(column, row) for column in board_coloumns for row in board_rows]
        
    def pick(self, rows):
        pick = random.choice([item for item in self.tiles if item[1] in rows])
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


basic_units_list = settings.basic_units
special_units_list = settings.special_units
unit_bag_size = settings.unit_bag_size
special_unit_count = settings.special_unit_count
basic_unit_count = settings.basic_unit_count
board_rows = [1, 2, 3, 4]
board_coloumns = [1, 2, 3, 4, 5]


def any(iterable):  # For compatibility with older python versions.
    for element in iterable:
        if element:
            return True
    return False


def test_coloumn_blocks(units):
    """ Tests whether there on each coloumn are at least two 'blocks'.
    A block is either a unit, or a Pikeman zoc tile. """
    
    cols = [pos[0] + x for x in [-1, +1] for pos, unit in units.items() if unit.name == "Pikeman"]\
        + [pos[0] for pos in units]

    return not any(cols.count(col) < 2 for col in board_coloumns)
     

def test_pikeman_coloumn(units):
    """ Tests whether there is more than one Pikeman on any coloumn."""
    
    cols = [pos[0] for pos, unit in units.items() if unit.name == "Pikeman"]
    
    return not any(cols.count(col) > 1 for col in board_coloumns)


def get_units():
    
    def select_basic_units(basic_units_bag, tiles_bag):

        units = {}
        
        while len(units) < basic_unit_count: 
            name = basic_units_bag.pick()
            pos = tiles_bag.pick(basic_units_list[name])      
            units[pos] = getattr(units, name.replace(" ", "_"))()

            if len(units) == 0:
                units[pos].acounters = 1
            if len(units) == 1:
                units[pos].dcounters = 1
        
        return units
    
    def select_special_units(special_units_first_bag, special_units_second_bag, tiles_bag):
         
        units = {}

        while len(units) < special_unit_count and special_units_first_bag.has_units():
            name = special_units_first_bag.pick()    
            pos = tiles_bag.pick(special_units_list[name])        
            units[pos] = getattr(units, name.replace(" ", "_"))()

        while len(units) < special_unit_count:
            name = special_units_second_bag.pick()
            pos = tiles_bag.pick(special_units_list[name])
            units[pos] = getattr(units, name.replace(" ", "_"))()

        return units

    def fill_bags():
        
        basic_units_bag = Unit_bag([name for name in basic_units_list for _ in range(unit_bag_size)])
        
        special_units_first_bag = Unit_bag([name for name in settings.use_special_units])
        
        special_units_second_bag = Unit_bag([name for name in special_units_list
                                             if name not in settings.dont_use_special_units])
        
        tiles_bag = Tiles_bag()
        
        return basic_units_bag, special_units_first_bag, special_units_second_bag, tiles_bag
        
    while True:
        
        basic_units_bag, special_units_first_bag, special_units_second_bag, tiles_bag = fill_bags()
        
        try:
            basic_units = select_basic_units(basic_units_bag, tiles_bag)
            special_units = select_special_units(special_units_first_bag, special_units_second_bag, tiles_bag)
        except IndexError:
            continue
        
        units = dict(basic_units.items() + special_units.items())

        if any(not requirement(units) for requirement in [test_coloumn_blocks, test_pikeman_coloumn]):
            continue
             
        return units


def flip_units(units):
    
    def flip(pos):
        return pos[0], 9 - pos[1]
    
    return dict((flip(pos), unit) for pos, unit in units.items())


def get_start_units():
    
    player1 = Player("Green")
    player2 = Player("Red")
    
    player1.units = get_units()
    player2.units = flip_units(get_units())
    
    return [player1, player2]
