class Unit(object):

    def __init__(self):
        self.acounters = 0
        self.dcounters = 0
        self.xp = 0
        self.used = False

    zoc = []
    abilities = []

    def __repr__(self):
        return self.name


class Archer(Unit):

    def __init__(self):
        super(Archer, self).__init__()

    name = "Archer"        
    attack = 2
    defence = 2
    movement = 1
    range= 4
    abonus = {"Infantry": 1}
    dbonus = {}
    type = "Infantry"
        

class Pikeman(Unit):

    def __init__(self):
        super(Pikeman, self).__init__()

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

    def __init__(self):
        super(Light_Cavalry, self).__init__()

    name = "Light Cavalry"       
    attack = 2
    defence = 2
    movement = 4
    range = 1
    abonus = {}
    dbonus = {}
    type = "Cavalry"


class Heavy_Cavalry(Unit):

    def __init__(self):
        super(Heavy_Cavalry, self).__init__()

    name = "Heavy Cavalry"
    attack = 3
    defence = 3
    movement = 2
    range = 1
    abonus = {}
    dbonus = {}
    type = "Cavalry"


class Ballista(Unit):

    def __init__(self):
        super(Ballista, self).__init__()

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
        
    double_attack_cost = True  # Attack takes two actions.


class Royal_Guard(Unit):

    def __init__(self):
        super(Royal_Guard, self).__init__()

    name = "Royal Guard"
    attack = 3
    defence = 3
    movement = 1
    range = 1
    abonus = {}
    dbonus = {}
    type = "Infantry"
    
    zoc = ["Cavalry", "Infantry", "Siege Weapon"]
    defence_maneuverability = True  # Can move two tiles if one of them is sideways.
    shield = True  # +1D v melee units.


class Scout(Unit):

    def __init__(self):
        super(Scout, self).__init__()

    name = "Scout"
    attack = False
    defence = 2
    movement = 4
    range = 1
    abonus = {}
    dbonus = {}
    zoc = []
    type = "Cavalry"
        
    scouting = True  # Can move past all units.


class Viking(Unit):

    def __init__(self):
        super(Viking, self).__init__()
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

    rage = True  # Can make an attack after it's move. (But not a second move)


class Cannon(Unit):

    def __init__(self):
        super(Cannon, self).__init__()

    name = "Cannon"
    attack = 5
    defence = 1
    movement = 1
    range = 4
    abonus = {}
    dbonus = {}
    zoc = []
    type = "Siege Weapon"
        
    attack_cooldown = 3  # Can only attack every third turn.
    

class Lancer(Unit):

    def __init__(self):
        super(Lancer, self).__init__()

    name = "Lancer"

    attack = 2
    defence = 3
    movement = 3
    range = 1
    abonus = {"Cavalry": 1}
    dbonus = {}
    zoc = []
    type = "Cavalry"
        
    lancing = True  # If it starts movement with 2 empty tiles between lancer and the unit it attacks, +2A


class Flag_Bearer(Unit):

    def __init__(self):
        super(Flag_Bearer, self).__init__()

    name = "Flag Bearer"
    attack = 2
    defence = 3
    movement = 3
    range = 1
    abonus = {}
    dbonus = {}
    zoc = []
    type = "Cavalry"
        
    flag_bearing = True  # Friendly melee units receive +2A while adjacent to Flag Bearer


class Longswordsman(Unit):

    def __init__(self):
        super(Longswordsman, self).__init__()

    name = "Longswordsman"
    attack = 3
    defence = 3
    movement = 1
    range = 1
    abonus = {}
    dbonus = {}
    zoc = []
    type = "Infantry"
        
    longsword = True  # Also hits the 4 nearby tiles in the attack direction


class Crusader(Unit):

    def __init__(self):
        super(Crusader, self).__init__()

    name = "Crusader"
    attack = 3
    defence = 3
    movement = 3
    range = 1
    abonus = {}
    dbonus = {}
    zoc = []
    type = "Cavalry"
        
    crusading = True  # Friendly melee units starting their movement in one of the 8 tiles surrounding Crusader gets +1A.


class Berserker(Unit):

    def __init__(self):
        super(Berserker, self).__init__()

    name = "Berserker"
    attack = 5
    defence = 1
    movement = 1
    range = 1
    abonus = {}
    dbonus = {}
    zoc = []
    type = "Infantry"
        
    berserking = True  # Can move 4 tiles if movement ends with an attack.


class Chariot(Unit):

    def __init__(self):
        super(Chariot, self).__init__()

    name = "Chariot"
    attack = 3
    defence = 3
    movement = 3
    range = 1
    abonus = {}
    dbonus = {}
    zoc = []
    type = "Cavalry"
        
    charioting = True  # Can use remaining moves after attacking


class War_Elephant(Unit):

    def __init__(self):
        super(War_Elephant, self).__init__()

    name = "War Elephant"
    attack = 3
    defence = 3
    movement = 2
    range = 1
    abonus = {}
    dbonus = {}
    zoc = []
    type = "Cavalry"
        
    double_attack_cost = True  # Attack takes two actions
    triple_attack = True  # Also hits the two diagonally nearby tiles in the attack direction.
    push = True  # If attack and defence rolls both succees, it can still move forward.
                 # If not on back line, opponents selfs must retreat directly backwards or die.


class Samurai(Unit):

    def __init__(self):
        super(Samurai, self).__init__()

    name = "Samurai"
    attack = 3
    defence = 3
    movement = 1
    range = 1
    abonus = {"Infantry": 1}
    dbonus = {}
    zoc = []
    type = "Infantry"
        
    samuraiing = True  # Can make an attack after it's first action. (But not a second move)
    

class Saboteur(Unit):

    def __init__(self):
        super(Saboteur, self).__init__()

    name = "Saboteur"
    attack = False
    defence = 2
    movement = 1
    range= 3
    abonus = {}
    dbonus = {}
    type = "Infantry"
    
    abilities = ["sabotage",  # Reduces a units defence to 0 for 1 turn.
                 "poison"]  # Freezes a unit for 2 turns.


class Diplomat(Unit):

    def __init__(self):
        super(Diplomat, self).__init__()

    name = "Diplomat"
    attack = False
    defence = 2
    movement = 1
    range= 3
    abonus = {}
    dbonus = {}
    type = "Infantry"
        
    abilities = ["bribe"]  # You can use an opponent's unit this turn. Your opponent can't use it on his next turn.
                           # You can't bribe the same unit on your next turn. The unit gets +1A until end of turn.


class Weaponsmith(Unit):

    def __init__(self):
        super(Weaponsmith, self).__init__()

    name = "Weaponsmith"
    attack = False   
    defence = 2
    movement = 1
    range= 3
    abonus = {}
    dbonus = {}
    type = "Infantry"
    
    abilities = ["improve_weapons"]  # Improve weapons: Give melee unit +3A. +1D until your next turn
