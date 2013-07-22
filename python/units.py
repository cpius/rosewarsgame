class Unit(object):

    attack_counters = 0
    defence_counters = 0
    xp = 0
    zoc = []
    abilities = []
    used = False
    xp_gained_this_round = False

    def __repr__(self):
        return self.name


class Archer(Unit):

    name = "Archer"        
    attack = 2
    defence = 2
    movement = 1
    range= 4
    abonus = {"Infantry": 1}
    dbonus = {}
    type = "Infantry"
        

class Pikeman(Unit):

    name = "Pikeman"
    attack = 2
    defence = 2
    movement = 1
    range = 1
    abonus = {"Cavalry": 1}
    dbonus = {"Cavalry": 1}
    type = "Infantry"   
    zoc = ["Cavalry"]
        

class Light_Cavalry(Unit):

    name = "Light Cavalry"       
    attack = 2
    defence = 2
    movement = 4
    range = 1
    abonus = {}
    dbonus = {}
    type = "Cavalry"


class Heavy_Cavalry(Unit):

    name = "Heavy Cavalry"
    attack = 3
    defence = 3
    movement = 2
    range = 1
    abonus = {}
    dbonus = {}
    type = "Cavalry"


class Ballista(Unit):
 
    name = "Ballista"
    attack = 4
    defence = 1
    movement = 1
    range = 3
    abonus = {}
    dbonus = {}
    type = "Siege Weapon"


class Catapult(Unit):

    name = "Catapult"
    attack = 6
    defence = 2
    movement = 1
    range = 3
    abonus = {}
    dbonus = {}
    type = "Siege Weapon"
        
    double_attack_cost = True

    descriptions = {"double_attack_cost": "Attack takes two actions."}


class Royal_Guard(Unit):
  
    name = "Royal Guard"
    attack = 3
    defence = 3
    movement = 1
    range = 1
    abonus = {}
    dbonus = {}
    type = "Infantry"
    
    zoc = ["Cavalry", "Infantry", "Siege Weapon"]
    defence_maneuverability = True
    shield = True

    descriptions = {"defence_maneuverability": "Can move two tiles if one of them is sideways.",
                    "shield": "+1D v melee units."}


class Scout(Unit):
    
    name = "Scout"
    attack = False
    defence = 2
    movement = 4
    range = 1
    abonus = {}
    dbonus = {}
    zoc = []
    type = "Cavalry"
        
    scouting = True

    descriptions = {"scouting": "Can move past all units."}


class Viking(Unit):

    def __init__(self):
        self.extra_life = True  # It takes two hits to kill viking

    name = "Viking"
    attack = 3
    defence = 2
    movement = 1
    range = 1
    abonus = {}
    dbonus = {"Siege Weapon": 1}
    zoc = []
    type = "Infantry"

    rage = True  #

    descriptions = {"rage": "Can make an attack after it's move. (But not a second move.)"}


class Cannon(Unit):
    
    name = "Cannon"
    attack = 5
    defence = 1
    movement = 1
    range = 4
    abonus = {}
    dbonus = {}
    zoc = []
    type = "Siege Weapon"
        
    attack_cooldown = 3

    descriptions = {"attack_cooldown": "Can only attack every third turn."}


class Lancer(Unit):
    
    name = "Lancer"

    attack = 2
    defence = 3
    movement = 3
    range = 1
    abonus = {"Cavalry": 1}
    dbonus = {}
    zoc = []
    type = "Cavalry"
        
    lancing = True

    descriptions = {"lancing": "If it starts movement with 2 empty tiles between lancer and the unit it attacks, +2A."}


class Flag_Bearer(Unit):
   
    name = "Flag Bearer"
    attack = 2
    defence = 3
    movement = 3
    range = 1
    abonus = {}
    dbonus = {}
    zoc = []
    type = "Cavalry"
        
    flag_bearing = True  #

    descriptions = {"flag_bearing": "Friendly melee units receive +2A while adjacent to Flag Bearer."}


class Longswordsman(Unit):

    name = "Longswordsman"
    attack = 3
    defence = 3
    movement = 1
    range = 1
    abonus = {}
    dbonus = {}
    zoc = []
    type = "Infantry"
        
    longsword = True

    descriptions = {"longsword": "Also hits the 4 nearby tiles in the attack direction."}


class Crusader(Unit):

    name = "Crusader"
    attack = 3
    defence = 3
    movement = 3
    range = 1
    abonus = {}
    dbonus = {}
    zoc = []
    type = "Cavalry"
        
    crusading = True

    descriptions = {"crusading": "Friendly melee units starting their movement in one of the 8 tiles surrounding "
                                 "Crusader get +1A."}


class Berserker(Unit):

    name = "Berserker"
    attack = 5
    defence = 1
    movement = 1
    range = 1
    abonus = {}
    dbonus = {}
    zoc = []
    type = "Infantry"
        
    berserking = True

    descriptions = {"berserking": "Can move 4 tiles if movement ends with an attack."}


class Chariot(Unit):
  
    name = "Chariot"
    attack = 4
    defence = 3
    movement = 3
    range = 1
    abonus = {}
    dbonus = {}
    zoc = []
    type = "Cavalry"
        
    charioting = True

    descriptions = {"charioting": "Can use remaining moves after attacking."}


class War_Elephant(Unit):

    name = "War Elephant"
    attack = 3
    defence = 3
    movement = 2
    range = 1
    abonus = {}
    dbonus = {}
    zoc = []
    type = "Cavalry"
        
    double_attack_cost = True
    triple_attack = True
    push = True

    descriptions = {"double_attack_cost": "Attack takes two actions.",
                    "triple_attack": "Also hits the two diagonally nearby tiles in the attack direction.",
                    "push": "If attack and defence rolls both succeed, it can still move forward. If not on back line, "
                            "opponents units must retreat directly backwards or die."}


class Samurai(Unit):
    
    name = "Samurai"
    attack = 6
    defence = 3
    movement = 1
    range = 1
    abonus = {"Infantry": 1}
    dbonus = {}
    zoc = []
    type = "Infantry"
        
    samuraiing = True

    descriptions = {"samuraiing": "Can make an attack after its first action. (But not a second move.)"}


class Saboteur(Unit):
    
    name = "Saboteur"
    attack = False
    defence = 2
    movement = 1
    range= 3
    abonus = {}
    dbonus = {}
    type = "Infantry"
    
    abilities = ["sabotage", "poison"]

    descriptions = {"sabotage": "Reduces a units defence to 0 for 1 turn.", "poison": "Freezes a unit for 2 turns."}


class Diplomat(Unit):
    
    name = "Diplomat"
    attack = False
    defence = 2
    movement = 1
    range= 3
    abonus = {}
    dbonus = {}
    type = "Infantry"
        
    abilities = ["bribe"]

    descriptions = {"bribe": "You can use an opponent's unit this turn. Your opponent can't use it on his next turn. "
                             "You can't bribe the same unit on your next turn. The unit gets +1A until end of turn."}


class Weaponsmith(Unit):
    
    name = "Weaponsmith"
    attack = False   
    defence = 2
    movement = 1
    range = 3
    abonus = {}
    dbonus = {}
    type = "Infantry"
    
    abilities = ["improve_weapons"]

    descriptions = {"improve_weapons": "Give melee unit +3 attack, +1 defence until your next turn"}


def get_position(position_string):
    if len(position_string) != 2:
        return None

    column = ord(position_string[0]) - 64  # In ASCII A, B, C, D, E is 65, 66, 67, 68, 69
    row = int(position_string[1])
    return column, row


def get_position_string(position):
    columns = list(" ABCDE")
    return columns[position[0]] + str(position[1])
