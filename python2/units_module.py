 
class Unit(object):
    def __init__(self, color):
        self.color = color
        self.acounters = 0
        self.dcounters = 0
        self.xp = 0
        self.zoc = []
        self.has_attack = True
        self.has_ability = False

        self.pic = self.name + ", " + color.lower() + ".jpg"
        
    def __repr__(self):
        return "|" + self.name + ", " + self.color + "|"


class Archer(Unit):
    def __init__(self, color):
        self.name = "Archer"
        super(Archer, self).__init__(color)
        
        self.attack = 2
        self.defence = 2
        self.movement = 1
        self.range= 4
        self.abonus = {"Infantry": 1}
        self.dbonus = {}
        self.type = "Infantry"
        

class Pikeman(Unit):
    def __init__(self, color):
        self.name = "Pikeman"
        super(Pikeman, self).__init__(color)

        self.attack = 2
        self.defence = 2
        self.movement = 1
        self.range= 1
        self.abonus = {"Cavalry": 1}
        self.dbonus = {"Cavalry": 1}
        self.type = "Infantry"   
        self.zoc = ["Cavalry"]
        

class Light_Cavalry(Unit):
    def __init__(self, color):
        self.name = "Light Cavalry"
        super(Light_Cavalry, self).__init__(color)
       
        self.attack = 2
        self.defence = 2
        self.movement = 4
        self.range= 1
        self.abonus = {}
        self.dbonus = {}
        self.type = "Cavalry"


class Heavy_Cavalry(Unit):
    def __init__(self, color):
        self.name = "Heavy Cavalry"
        super(Heavy_Cavalry, self).__init__(color)

        self.attack = 3
        self.defence = 3
        self.movement = 2
        self.range= 1
        self.abonus = {}
        self.dbonus = {}
        self.type = "Cavalry"


class Ballista(Unit):
    def __init__(self, color):
        self.name = "Ballista"
        super(Ballista, self).__init__(color)
 
        self.attack = 4
        self.defence = 1
        self.movement = 1
        self.range= 3
        self.abonus = {}
        self.dbonus = {}
        self.type = "Siege Weapon"


class Catapult(Unit):
    def __init__(self, color):
        self.name = "Catapult"
        super(Catapult, self).__init__(color)

        self.attack = 6
        self.defence = 2
        self.movement = 1
        self.range= 3
        self.abonus = {}
        self.dbonus = {}
        self.type = "Siege Weapon"
        
        self.double_attack_cost = True #Attack takes two actions.



class Royal_Guard(Unit):
    def __init__(self, color):
        self.name = "Royal Guard"
        super(Royal_Guard, self).__init__(color)
  
        self.attack = 3
        self.defence = 3
        self.movement = 1
        self.range= 1
        self.abonus = {}
        self.dbonus = {}
        self.type = "Infantry"
    
        self.zoc = ["Cavalry", "Infantry", "Siege Weapon"]
        self.defence_maneuverability = True #Can move two tiles if one of them is sideways.
        self.shield = True #+1D v melee units.


class Scout(Unit):
    def __init__(self, color):
        self.name = "Scout"
        super(Scout, self).__init__(color)
       
        self.defence = 2
        self.movement = 4
        self.range = 1
        self.abonus = {}
        self.dbonus = {}
        self.zoc = []
        self.type = "Cavalry"
        
        self.has_attack = False
        self.scouting = True #Can move past all units.


class Viking(Unit):
    def __init__(self, color):
        self.name = "Viking"
        super(Viking, self).__init__(color)
 
        self.attack = 3
        self.defence = 2
        self.movement = 1
        self.range = 1
        self.abonus = {}
        self.dbonus = {"Siege Weapon": 1}
        self.zoc = []
        self.type = "Infantry"
        
        self.extra_life = True #It takes two hits to kill viking
        self.rage = True # Can make an attack after it's move. (But not a second move)


class Cannon(Unit):
    def __init__(self, color):
        self.name = "Cannon"
        super(Cannon, self).__init__(color)
    
        self.attack = 5
        self.defence = 1
        self.movement = 1
        self.range = 4
        self.abonus = {}
        self.dbonus = {}
        self.zoc = []
        self.type = "Siege Weapon"
        
        self.cooldown = 3 #Can only attack every third turn.
    

class Lancer(Unit):
    def __init__(self, color):
        self.name = "Lancer"
        super(Lancer, self).__init__(color)

        self.attack = 2
        self.defence = 3
        self.movement = 3
        self.range = 1
        self.abonus = {"Cavalry": 1}
        self.dbonus = {}
        self.zoc = []
        self.type = "Cavalry"
        
        self.lancing = True # If it starts movement with 2 empty tiles between lancer and the unit it attacks, +2A


class Flag_Bearer(Unit):
    def __init__(self, color):
        self.name = "Flag Bearer"
        super(Flag_Bearer, self).__init__(color)
   
        self.attack = 2
        self.defence = 3
        self.movement = 3
        self.range = 1
        self.abonus = {}
        self.dbonus = {}
        self.zoc = []
        self.type = "Cavalry"
        
        self.flag_bearing = True # Friendly melee units receive +2A while adjacent to Flag Bearer


class Longswordsman(Unit):
    def __init__(self, color):
        self.name = "Longswordsman"
        super(Longswordsman, self).__init__(color)

        self.attack = 3
        self.defence = 3
        self.movement = 1
        self.range = 1
        self.abonus = {}
        self.dbonus = {}
        self.zoc = []
        self.type = "Infantry"
        
        self.longsword = True #Also hits the 4 nearby tiles in the attack direction


class Crusader(Unit):
    def __init__(self, color):
        self.name = "Crusader"
        super(Crusader, self).__init__(color)
  
        self.attack = 3
        self.defence = 3
        self.movement = 3
        self.range = 1
        self.abonus = {}
        self.dbonus = {}
        self.zoc = []
        self.type = "Cavalry"
        
        self.crusading = True # Friendly melee units starting their movement in one of the 8 tiles surrounding Crusader gets +1A.



class Berserker(Unit):
    def __init__(self, color):
        self.name = "Berserker"
        super(Berserker, self).__init__(color)
   
        self.attack = 5
        self.defence = 1
        self.movement = 1
        self.range = 1
        self.abonus = {}
        self.dbonus = {}
        self.zoc = []
        self.type = "Infantry"
        
        self.berserking = True # Can move 4 tiles if movement ends with an attack.


class Chariot(Unit):
    def __init__(self, color):
        self.name = "Chariot"
        super(Chariot, self).__init__(color)
  
        self.attack = 3
        self.defence = 3
        self.movement = 3
        self.range = 1
        self.abonus = {}
        self.dbonus = {}
        self.zoc = []
        self.type = "Cavalry"
        
        self.charioting = True # Can use remaining moves after attacking


class War_Elephant(Unit):
    def __init__(self, color):
        self.name = "War Elephant"
        super(War_Elephant, self).__init__(color)

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


class Samurai(Unit):
    def __init__(self, color):
        self.name = "Samurai"
        super(Samurai, self).__init__(color)
    
        self.attack = 3
        self.defence = 3
        self.movement = 1
        self.range = 1
        self.abonus = {"Infantry": 1}
        self.dbonus = {}
        self.zoc = []
        self.type = "Infantry"
        
        self.samuraiing = True # Can make an attack after it's first action. (But not a second move)
    

class Saboteur(Unit):
    def __init__(self, color):
        self.name = "Saboteur"
        super(Saboteur, self).__init__(color)

        self.defence = 2
        self.movement = 1
        self.range= 3
        self.abonus = {}
        self.dbonus = {}
        self.type = "Infantry"
        
        self.has_attack = False
        self.has_ability = True
        self.abilities = ["sabotage", "poison"] #Sabotage: Reduces a units defence to 0 for 1 turn. Poison: Freezes a unit for 2 turns.


class Diplomat(Unit):
    def __init__(self, color):
        self.name = "Diplomat"
        super(Diplomat, self).__init__(color)

        self.defence = 2
        self.movement = 1
        self.range= 3
        self.abonus = {}
        self.dbonus = {}
        self.type = "Infantry"
        
        self.has_attack = False
        self.has_ability = True
        self.abilities = ["bribe"] #Bribe: You can use an opponent's unit this turn. Your opponent can't use it on his next turn. You can't bribe the same unit on your next turn. The unit gets +1A until end of turn.



class Weaponsmith(Unit):
    def __init__(self, color):
        self.name = "Weaponsmith"
        super(Weaponsmith, self).__init__(color)
   
        self.defence = 2
        self.movement = 1
        self.range= 3
        self.abonus = {}
        self.dbonus = {}
        self.type = "Infantry"
        
        self.has_attack = False
        self.has_ability = True
        self.abilities = ["improve_weapons"] #Improve weapons: Give melee unit +3A. +1D until your next turn
