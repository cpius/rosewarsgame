from __future__ import division
from numpy import random as rnd
import itertools as it
   

class Player:
    def __init__(self, color):
        self.color = color
        if color == "Red":
            self.backline = 1
            self.frontline = 4
        else:
            self.backline = 8
            self.frontline = 5


class Unit:
    def __init__(self, name, color, acounters, dcounters):
        self.name = name
        self.pic = "./units/" + name + ", " + color.lower() + ".jpg"
        self.color = color
        self.acounters = acounters
        self.dcounters = dcounters
        self.xp = 0
        self.has_attack = True
        self.has_ability = False
        self.is_crusading = False
        self.high_morale = False
        getattr(self, self.name.replace(" ", "_").lower())()
        
    def __repr__(self):
        return "|" + self.name + ", " + self.color + "|\n"
    
    def archer(self):
        self.attack = 5
        self.defence = 2
        self.movement = 1
        self.range= 4
        self.abonus = {"Infantry": 1}
        self.dbonus = {}
        self.type = "Infantry"      

    
    def pikeman(self):
        self.attack = 5
        self.defence = 2
        self.movement = 1
        self.range= 1
        self.abonus = {"Cavalry": 1}
        self.dbonus = {"Cavalry": 1}
        self.type = "Infantry"
        
        self.zoc = ["Cavalry"]


    def light_cavalry(self):
        self.attack = 5
        self.defence = 2
        self.movement = 4
        self.range= 1
        self.abonus = {}
        self.dbonus = {}
        self.type = "Cavalry"


    def heavy_cavalry(self):
        self.attack = 4
        self.defence = 3
        self.movement = 2
        self.range= 1
        self.abonus = {}
        self.dbonus = {}
        self.type = "Cavalry"


    def ballista(self):
        self.attack = 3
        self.defence = 1
        self.movement = 1
        self.range= 3
        self.abonus = {}
        self.dbonus = {}
        self.type = "Siege Weapon"



    def catapult(self):
        self.attack = 1
        self.defence = 2
        self.movement = 1
        self.range= 3
        self.abonus = {}
        self.dbonus = {}
        self.type = "Siege Weapon"
        
        self.double_attack_cost = True #Attack takes two actions.


    def royal_guard(self):
        self.attack = 4
        self.defence = 3
        self.movement = 1
        self.range= 1
        self.abonus = {}
        self.dbonus = {}
        self.type = "Infantry"

        self.zoc = ["Cavalry", "Infantry", "Siege Weapon"]
        self.defence_maneuverability = True #Can move two tiles if one of them is sideways.
        self.shield = True #+1D v melee units.


    def scout(self):
        self.defence = 2
        self.movement = 4
        self.range = 1
        self.abonus = {}
        self.dbonus = {}
        self.zoc = []
        self.type = "Cavalry"
        
        self.has_attack = False
        self.scouting = True #Can move past all units.


    def viking(self):
        self.attack = 4
        self.defence = 2
        self.movement = 1
        self.range = 1
        self.abonus = {}
        self.dbonus = {"Siege Weapon": 1}
        self.zoc = []
        self.type = "Infantry"
        
        self.extra_life = True #It takes two hits to kill viking
        self.rage = True # Can make an attack after it's move. (But not a second move)
        
        
    def cannon(self):
        self.attack = 2
        self.defence = 1
        self.movement = 1
        self.range = 4
        self.abonus = {}
        self.dbonus = {}
        self.zoc = []
        self.type = "Siege Weapon"
        
        self.cooldown = 3 #Can only attack every third turn.


    def lancer(self):
        self.attack = 5
        self.defence = 3
        self.movement = 3
        self.range = 1
        self.abonus = {"Cavalry": 1}
        self.dbonus = {}
        self.zoc = []
        self.type = "Cavalry"
        
        self.lancing = True # If it starts movement with 2 empty tiles between lancer and the unit it attacks, +2A
        
        
    def flag_bearer(self):
        self.attack = 5
        self.defence = 3
        self.movement = 3
        self.range = 1
        self.abonus = {}
        self.dbonus = {}
        self.zoc = []
        self.type = "Cavalry"
        
        self.flag_bearing = True # Friendly melee units receive +2A while adjacent to Flag Bearer
        

    def longswordsman(self):
        self.attack = 4
        self.defence = 3
        self.movement = 1
        self.range = 1
        self.abonus = {}
        self.dbonus = {}
        self.zoc = []
        self.type = "Infantry"
        
        self.longsword = True #Also hits the 4 nearby tiles in the attack direction
        
        
    def crusader(self):
        self.attack = 4
        self.defence = 3
        self.movement = 3
        self.range = 1
        self.abonus = {}
        self.dbonus = {}
        self.zoc = []
        self.type = "Cavalry"
        
        self.crusading = True # Friendly melee units starting their movement in one of the 8 tiles surrounding Crusader gets +1A.
        

    def berserker(self):
        self.attack = 2
        self.defence = 1
        self.movement = 1
        self.range = 1
        self.abonus = {}
        self.dbonus = {}
        self.zoc = []
        self.type = "Infantry"
        
        self.berserking = True # Can move 4 tiles if movement ends with an attack.
        
        
    def chariot(self):
        self.attack = 4
        self.defence = 3
        self.movement = 3
        self.range = 1
        self.abonus = {}
        self.dbonus = {}
        self.zoc = []
        self.type = "Cavalry"
        
        self.charioting = True # Can use remaining moves after attacking


    def war_elephant(self):
        self.attack = 3
        self.defence = 3
        self.movement = 2
        self.range = 1
        self.abonus = {}
        self.dbonus = {}
        self.zoc = []
        self.type = "Cavalry"
        
        self.double_attack_cost = True # Attack takes two actions
        self.triple_attack = True #Also hits the two diagonally nearby tiles in the attack direction.
        self.push = True #If attack and defence rolls both succees, it can still move forward. If not on back line, opponents selfs must retreat directly backwards or die.
        

    def samurai(self):
        self.attack = 3
        self.defence = 3
        self.movement = 1
        self.range = 1
        self.abonus = {"Infantry": 1}
        self.dbonus = {}
        self.zoc = []
        self.type = "Infantry"
        
        self.samuraiing = True # Can make an attack after it's first action. (But not a second move)
        

    def saboteur(self):
        self.defence = 2
        self.movement = 1
        self.range= 3
        self.abonus = {}
        self.dbonus = {}
        self.type = "Infantry"
        
        self.has_attack = False
        self.has_ability = True
        self.abilities = ["sabotage", "poison"] #Sabotage: Reduces a units defence to 0 for 1 turn. Poison: Freezes a unit for 2 turns.


    def diplomat(self):
        self.defence = 2
        self.movement = 1
        self.range= 3
        self.abonus = {}
        self.dbonus = {}
        self.type = "Infantry"
        
        self.has_attack = False
        self.has_ability = True
        self.abilities = ["bribe"] #Bribe: You can use an opponent's unit this turn. Your opponent can't use it on his next turn. You can't bribe the same unit on your next turn. The unit gets +1A until end of turn.


    def weaponsmith(self): 
        self.defence = 2
        self.movement = 1
        self.range= 3
        self.abonus = {}
        self.dbonus = {}
        self.type = "Infantry"
        
        self.has_attack = False
        self.has_ability = True
        self.abilities = ["improve weapons"] #Improve weapons: Give melee unit +3A. +1D until your next turn       
        


board = set((i,j) for i in range(1,6) for j in range(1, 9))
unit_names = ["Archer", "Ballista", "Catapult", "Light Cavalry", "Heavy Cavalry", "Pikeman"]
specialunit_names = ["Chariot", "Diplomat", "Samurai", "War Elephant", "Weaponsmith", "Scout", "Lancer", "Cannon", "Saboteur", "Viking", "Berserker", "Crusader", "Longswordsman", "Flag Bearer", "Royal Guard"]   #Special units that are implemented so far.
nonfrontunit_names = ["Light Cavalry", "Ballista", "Catapult", "Archer", "Scout", "Saboteur", "Diplomat", "Berserker", "Cannon", "Weaponsmith", "Royal Guard"]
nonbackunit_names = ["Pikeman", "Berserker", "Longswordsman", "Royal Guard", "Samurai", "Viking", "War Elephant"]

unit_bag_size = 4
special_unit_count = 3
total_unit_count = 9



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
   
    
def test_samekind_limit(player):
    """ Tests whether there is more than three copies of any one kind of unit."""
    
    names = [unit.name for unit in player.units.values()]
    
    return not any(names.count(name) > 3 for name in set(names))
    

def test_onepikeman(player):
    """ Tests whether the player has at least one Pikeman."""
    
    return any(unit.name == "Pikeman" for unit in player.units.values() )
        

def test_pikeman_coloumn(player):
    """ Tests whether there is more than one Pikeman on any coloumn."""
    
    cols = [pos[0] for pos, unit in player.units.items() if unit.name == "Pikeman"]
    
    return not any(cols.count(col) > 1 for col in [1,2,3,4,5] )


def test_frontline_units(player):
    """ Tests whether any unit in the group 'nonfrontunit_names' is on the frontline."""
    
    return not any((pos[1] == player.frontline and unit.name in nonfrontunit_names) for pos, unit in player.units.items() )


def test_backline_units(player):
    """ Tests whether any unit in the group 'nonbackunit_names' is on the backline."""

    return not any((pos[1] == player.backline and unit.name in nonbackunit_names) for pos, unit in player.units.items() )


def get_units_player(player):
    
    counter = it.count(1)
    for co in counter:

        player.units = {}
        unit_bag = [name for name in unit_names for i in range(unit_bag_size)]
        rnd.shuffle(unit_bag)
        specialunit_bag = [name for name in specialunit_names]
        rnd.shuffle(specialunit_bag)
        player_board = [pos for pos in board if player.frontline <= pos[1] <= player.backline or player.frontline >= pos[1] >= player.backline]
        rnd.shuffle(player_board)
        
        while len(player.units) <= total_unit_count - special_unit_count: 
            name = unit_bag.pop()
            pos = player_board.pop()
            if len(player.units) == 0: acounters = 1
            else: acounters = 0
            if len(player.units) == 1: dcounters = 1
            else: dcounters = 0
            
            player.units[pos] = (Unit(name, player.color, acounters, dcounters))

        while len(player.units) <= total_unit_count:   
            name = specialunit_bag.pop()    
            pos = player_board.pop()
            player.units[pos] = (Unit(name, player.color, 0, 0))
             
        requirements = [test_coloumn_blocks, test_samekind_limit, test_onepikeman, test_pikeman_coloumn, test_frontline_units, test_backline_units, test_backline_count]
        
        if all(requirement(player) for requirement in requirements):
            break
    
    return player


def get_startunits():
    
    p1 = Player("Green")
    p2 = Player("Red")
    
    return [get_units_player(p1), get_units_player(p2)]
