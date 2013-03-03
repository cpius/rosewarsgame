from __future__ import division
from numpy import random as rnd
import itertools as it
import units_module
import settings



class Player(object):
    def __init__(self, color):
        self.color = color
        if color == "Red":
            self.backline = 8
            self.frontline = 5
        else:
            self.backline = 1
            self.frontline = 4


        


board = set((i,j) for i in range(1,6) for j in range(1, 9))

basic_unit_names = ["Archer", "Ballista", "Catapult", "Light Cavalry", "Heavy Cavalry", "Pikeman"]
special_unit_names = ["Chariot", "Diplomat", "Samurai", "War Elephant", "Weaponsmith", "Scout", "Lancer", "Cannon", "Saboteur", "Viking", "Berserker", "Crusader", "Longswordsman", "Flag Bearer", "Royal Guard"]
non_frontline_unit_names = ["Light Cavalry", "Ballista", "Catapult", "Archer", "Scout", "Saboteur", "Diplomat", "Berserker", "Cannon", "Weaponsmith", "Royal Guard"]
non_backline_unit_names = ["Pikeman", "Berserker", "Longswordsman", "Royal Guard", "Samurai", "Viking", "War Elephant"]

unit_bag_size = settings.unit_bag_size
special_unit_count = settings.special_unit_count
total_unit_count = settings.total_unit_count



def any(iterable):
    for element in iterable:
        if element:
            return True
    return False

def all(iterable):
    for element in iterable:
        if not element:
            return False
    return True

def test_coloumn_blocks(player):
    """ Tests whether there on each coloumn are at least two 'blocks'. A block is either a unit, or a Pikeman zoc tile other than the back line. """
    
    cols = [pos[0] + x for x in [-1, +1] for pos, unit in player.units.items() if unit.name == "Pikeman"] + [pos[0] for pos in player.units]

    return not any(cols.count(col) < 2 for col in [1,2,3,4,5] )


def test_backline_count(player):
    """ Tests whether there is more than one unit on the backline."""
    
    return sum(1 for pos in player.units if pos[1] == player.backline) < 2
   
    
def test_same_kind_limit(player):
    """ Tests whether there is more than three copies of any one kind of unit."""
    
    names = [unit.name for unit in player.units.values()]
    
    return not any(names.count(name) > 3 for name in set(names))
    

def test_one_pikeman(player):
    """ Tests whether the player has at least one Pikeman."""
    
    return any(unit.name == "Pikeman" for unit in player.units.values() )
        

def test_pikeman_coloumn(player):
    """ Tests whether there is more than one Pikeman on any coloumn."""
    
    cols = [pos[0] for pos, unit in player.units.items() if unit.name == "Pikeman"]
    
    return not any(cols.count(col) > 1 for col in [1,2,3,4,5] )


def test_frontline_units(player):
    """ Tests whether any unit in the group 'nonfrontunit_names' is on the frontline."""
    
    return not any((pos[1] == player.frontline and unit.name in non_frontline_unit_names) for pos, unit in player.units.items() )


def test_backline_units(player):
    """ Tests whether any unit in the group 'nonbackunit_names' is on the backline."""

    return not any((pos[1] == player.backline and unit.name in non_backline_unit_names) for pos, unit in player.units.items() )


def get_units_player(player):
    
    def select_basic_units(basic_units_bag, tiles_bag, units):
        
        while len(units) <= total_unit_count - special_unit_count: 
            name = basic_units_bag.pop()
            pos = tiles_bag.pop()

            units[pos] = getattr(units_module, name.replace(" ", "_"))(player.color)

            if len(units) == 0: units[pos].acounters = 1
            if len(units) == 1: units[pos].dcounters = 1
        
        return units
    
    
    def select_special_units(special_units_first_bag, special_units_second_bag, tiles_bag, units):
        
        while len(units) <= total_unit_count and len(special_units_first_bag) > 0:
            name = special_units_first_bag.pop()    
            pos = tiles_bag.pop()

            units[pos] = getattr(units_module, name.replace(" ", "_"))(player.color)

        while len(units) <= total_unit_count:
            name = special_units_second_bag.pop()    
            pos = tiles_bag.pop()

            units[pos] = getattr(units_module, name.replace(" ", "_"))(player.color)
        
        return units
    
    
    def fill_unit_bags():
        
        basic_units_bag = [name for name in basic_unit_names for i in range(unit_bag_size)]
        rnd.shuffle(basic_units_bag)
        
        special_units_first_bag = [name for name in settings.use_special_units]
        rnd.shuffle(special_units_first_bag)
        
        special_units_second_bag = [name for name in special_unit_names if name not in settings.dont_use_special_units]
        rnd.shuffle(special_units_second_bag)
        
        tiles_bag = [pos for pos in board if player.frontline <= pos[1] <= player.backline or player.frontline >= pos[1] >= player.backline]
        rnd.shuffle(tiles_bag)
        
        return basic_units_bag, special_units_first_bag, special_units_second_bag, tiles_bag
        
    
    counter = it.count(1)
    for co in counter:

        units = {}

        basic_units_bag, special_units_first_bag, special_units_second_bag, tiles_bag = fill_unit_bags()
    
        units = select_basic_units(basic_units_bag, tiles_bag, units)
        
        units = select_special_units(special_units_first_bag, special_units_second_bag, tiles_bag, units)
        
        requirements = [test_coloumn_blocks, test_same_kind_limit, test_one_pikeman, test_pikeman_coloumn, test_frontline_units, test_backline_units, test_backline_count]
        
        player.units = units
        if all(requirement(player) for requirement in requirements):
            break
    
    return player


def get_startunits():
    
    p1 = Player("Green")
    p2 = Player("Red")
    
    return [get_units_player(p1), get_units_player(p2)]
