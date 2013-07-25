class Unit(object):
    def __init__(self):
        self.variables = {"xp_gained_this_round": False, "used": False, "xp": 0}

    name = ""
    zoc = []
    abilities = []
    xp_to_upgrade = 4
    upgrades = []
    abonus = {}
    dbonus = {}

    def __repr__(self):
        return self.name


class Archer(Unit):

    name = "Archer"
    image = "Archer"
    attack = 2
    defence = 2
    movement = 1
    range = 4
    abonus = {"Infantry": 1}
    dbonus = {}
    type = "Infantry"
    upgrades = ["Longbowman", "Crossbow Archer"]


class Longbowman(Unit):
    name = "Longbowman"
    image = "Archer"
    attack = 2
    defence = 2
    movement = 1
    range = 4
    type = "Infantry"
    upgrades = ["Longbowman II_A", "Longbowman II_B"]

    sharpshooting = True

    descriptions = {"sharpshooting": "Targets have their defence reduced to 1 during the attack"}


class Longbowman_II_A(Unit):
    name = "Longbowman II_A"
    image = "Archer"
    attack = 4
    defence = 2
    movement = 1
    range = 4
    abonus = {"Infantry": 1}
    dbonus = {}
    type = "Infantry"


class Longbowman_II_B(Unit):
    name = "Longbowman II_B"
    image = "Archer"
    attack = 3
    defence = 3
    movement = 1
    range = 4
    abonus = {"Infantry": 1}
    dbonus = {}
    type = "Infantry"


class Crossbow_Archer(Unit):
    name = "Crossbow Archer"
    image = "Archer"
    attack = 2
    defence = 3
    movement = 1
    range = 4
    abonus = {"Infantry": 1}
    dbonus = {}
    type = "Infantry"
    upgrades = ["Crossbow Archer II_A", "Crossbow Archer II_B"]


class Crossbow_Archer_II_A(Unit):
    name = "Crossbow Archer II_A"
    image = "Archer"
    attack = 3
    defence = 3
    movement = 1
    range = 4
    abonus = {"Infantry": 1}
    dbonus = {}
    type = "Infantry"


class Crossbow_Archer_II_B(Unit):
    name = "Crossbow Archer II_B"
    image = "Archer"
    attack = 2
    defence = 4
    movement = 1
    range = 4
    abonus = {"Infantry": 1}
    dbonus = {}
    type = "Infantry"


class Pikeman(Unit):

    name = "Pikeman"
    image = "Pikeman"
    attack = 2
    defence = 2
    movement = 1
    range = 1
    abonus = {"Cavalry": 1}
    dbonus = {"Cavalry": 1}
    type = "Infantry"   
    zoc = ["Cavalry"]
    upgrades = ["Halberdier", "Royal Guard"]
    xp_to_upgrade = 3


class Halberdier(Unit):
    name = "Halberdier"
    image = "Pikeman"
    attack = 4
    defence = 3
    movement = 1
    range = 1
    type = "Infantry"

    push = True

    descriptions = {"push": "If attack and defence rolls both succeed, it can still move forward. If not on back line, "
                            "opponents units must retreat directly backwards or die."}


class Halberdier_II_A(Unit):
    name = "Halberdier"
    image = "Pikeman"
    attack = 5
    defence = 3
    movement = 1
    range = 1
    type = "Infantry"

    push = True

    descriptions = {"push": "If attack and defence rolls both succeed, it can still move forward. If not on back line, "
                            "opponents units must retreat directly backwards or die."}


class Halberdier_II_B(Unit):
    name = "Halberdier"
    image = "Pikeman"
    attack = 4
    defence = 4
    movement = 1
    range = 1
    type = "Infantry"

    push = True

    descriptions = {"push": "If attack and defence rolls both succeed, it can still move forward. If not on back line, "
                            "opponents units must retreat directly backwards or die."}


class Light_Cavalry(Unit):

    name = "Light Cavalry"
    image = "Light Cavalry"
    attack = 2
    defence = 2
    movement = 4
    range = 1
    abonus = {}
    dbonus = {}
    type = "Cavalry"

    upgrades = ["Dragoon", "Cavalry Lieutenant"]
    xp_to_upgrade = 3


class Dragoon(Unit):

    name = "Dragoon"
    image = "Light Cavalry"
    attack = 3
    defence = 2
    movement = 4
    range = 1
    abonus = {}
    dbonus = {}
    type = "Cavalry"
    upgrades = ["Dragoon II_A", "Dragoon II_B"]


class Dragoon_II_A(Unit):

    name = "Dragoon II_A"
    image = "Light Cavalry"
    attack = 4
    defence = 2
    movement = 4
    range = 1
    abonus = {}
    dbonus = {}
    type = "Cavalry"


class Dragoon_II_B(Unit):

    name = "Dragoon II_B"
    image = "Light Cavalry"
    attack = 3
    defence = 3
    movement = 4
    range = 1
    abonus = {}
    dbonus = {}
    type = "Cavalry"


class Cavalry_Lieutenant(Unit):

    name = "Cavalry Lieutenant"
    image = "Light Cavalry"
    attack = 2
    defence = 3
    movement = 4
    range = 1
    abonus = {}
    dbonus = {}
    type = "Cavalry"
    upgrades = ["Cavalry_Luitenant_II_A", "Cavalry_Luitenant_II_B"]


class Cavalry_Luitenant_II_A(Unit):

    name = "Cavalry Liuetenant II_A"
    image = "Light Cavalry"
    attack = 3
    defence = 3
    movement = 4
    range = 1
    abonus = {}
    dbonus = {}
    type = "Cavalry"


class Cavalry_Luitenant_II_B(Unit):

    name = "Cavalry Liuetenant II_B"
    image = "Light Cavalry"
    attack = 2
    defence = 4
    movement = 4
    range = 1
    abonus = {}
    dbonus = {}
    type = "Cavalry"


class Heavy_Cavalry(Unit):

    name = "Heavy Cavalry"
    image = "Heavy Cavalry"
    attack = 3
    defence = 3
    movement = 2
    range = 1
    abonus = {}
    dbonus = {}
    type = "Cavalry"
    upgrades = ["Lancer", "Chariot"]


class Ballista(Unit):
 
    name = "Ballista"
    image = "Ballista"
    attack = 4
    defence = 1
    movement = 1
    range = 3
    abonus = {}
    dbonus = {}
    type = "Siege Weapon"
    upgrades = ["Cannon", "Trebuchet"]


class Trebuchet(Unit):

    name = "Trebuchet"
    image = "Ballista"
    attack = 5
    defence = 1
    movement = 1
    range = 3
    abonus = {}
    dbonus = {}
    type = "Siege Weapon"
    upgrades = ["Trebuchet II_A", "Trebuchet II_A"]


class Trebuchet_II_A(Unit):

    name = "Trebuchet II_A"
    image = "Ballista"
    attack = 6
    defence = 1
    movement = 1
    range = 3
    abonus = {}
    dbonus = {}
    type = "Siege Weapon"


class Trebuchet_II_B(Unit):

    name = "Trebuchet II_B"
    image = "Ballista"
    attack = 5
    defence = 2
    movement = 1
    range = 3
    abonus = {}
    dbonus = {}
    type = "Siege Weapon"


class Catapult(Unit):

    name = "Catapult"
    image = "Catapult"
    attack = 6
    defence = 2
    movement = 1
    range = 3
    abonus = {}
    dbonus = {}
    type = "Siege Weapon"
        
    double_attack_cost = True
    xp_to_upgrade = 2

    descriptions = {"double_attack_cost": "Attack takes two actions."}


class Catapult_II_A(Unit):

    name = "Catapult II_A"
    image = "Catapult"
    attack = 6
    defence = 2
    movement = 1
    range = 3
    abonus = {}
    dbonus = {}
    type = "Siege Weapon"

    double_attack_cost = True
    xp_to_upgrade = 3

    descriptions = {"double_attack_cost": "Attack takes two actions."}

    upgrades = ["Catapult III_A", "Catapult III_B"]


class Catapult_II_B(Unit):

    name = "Catapult II_B"
    image = "Catapult"
    attack = 6
    defence = 2
    movement = 1
    range = 3
    abonus = {}
    dbonus = {}
    type = "Siege Weapon"

    double_attack_cost = True
    xp_to_upgrade = 3

    descriptions = {"double_attack_cost": "Attack takes two actions."}

    upgrades = ["Catapult III_B", "Catapult IIIC"]


class Catapult_III_A(Unit):

    name = "Catapult III_A"
    image = "Catapult"
    attack = 8
    defence = 2
    movement = 1
    range = 3
    abonus = {}
    dbonus = {}
    type = "Siege Weapon"

    double_attack_cost = True

    descriptions = {"double_attack_cost": "Attack takes two actions."}


class Catapult_III_B(Unit):

    name = "Catapult III_B"
    image = "Catapult"
    attack = 7
    defence = 2
    movement = 1
    range = 4
    abonus = {}
    dbonus = {}
    type = "Siege Weapon"

    double_attack_cost = True

    descriptions = {"double_attack_cost": "Attack takes two actions."}


class Catapult_III_C(Unit):

    name = "Catapult III_C"
    image = "Catapult"
    attack = 7
    defence = 2
    movement = 1
    range = 5
    abonus = {}
    dbonus = {}
    type = "Siege Weapon"

    double_attack_cost = True

    descriptions = {"double_attack_cost": "Attack takes two actions."}


class Royal_Guard(Unit):
  
    name = "Royal Guard"
    image = "Royal Guard"
    attack = 3
    defence = 3
    movement = 1
    range = 1
    abonus = {}
    dbonus = {}
    type = "Infantry"
    
    zoc = ["Cavalry", "Infantry", "Siege Weapon", "Specialist"]
    defence_maneuverability = True
    shield = True
    xp_to_upgrade = 3

    descriptions = {"defence_maneuverability": "Can move two tiles if one of them is sideways.",
                    "shield": "+1D v melee units."}

    upgrades = ["Royal Guard II_A", "Royal Guard II_B"]


class Royal_Guard_II_A(Unit):

    name = "Royal Guard II_A"
    image = "Royal Guard"
    attack = 4
    defence = 3
    movement = 1
    range = 1
    abonus = {}
    dbonus = {}
    type = "Infantry"

    zoc = ["Cavalry", "Infantry", "Siege Weapon", "Specialist"]
    defence_maneuverability = True
    shield = True

    descriptions = {"defence_maneuverability": "Can move two tiles if one of them is sideways.",
                    "shield": "+1D v melee units."}


class Royal_Guard_II_B(Unit):

    name = "Royal Guard II_B"
    image = "Royal Guard"
    attack = 3
    defence = 4
    movement = 1
    range = 1
    abonus = {}
    dbonus = {}
    type = "Infantry"

    zoc = ["Cavalry", "Infantry", "Siege Weapon", "Specialist"]
    defence_maneuverability = True
    shield = True

    descriptions = {"defence_maneuverability": "Can move two tiles if one of them is sideways.",
                    "shield": "+1D v melee units."}


class Scout(Unit):
    
    name = "Scout"
    image = "Scout"
    attack = False
    defence = 2
    movement = 4
    range = 1
    abonus = {}
    dbonus = {}
    zoc = []
    type = "Cavalry"
        
    scouting = True
    xp_to_upgrade = 2

    descriptions = {"scouting": "Can move past all units."}

    upgrades = ["Scout II_A", "Scout II_B"]


class Scout_II_A(Unit):

    name = "Scout II_A"
    image = "Scout"
    attack = False
    defence = 3
    movement = 4
    range = 1
    abonus = {}
    dbonus = {}
    zoc = []
    type = "Cavalry"

    scouting = True

    descriptions = {"scouting": "Can move past all units."}


class Scout_II_B(Unit):

    name = "Scout II_B"
    image = "Scout"
    attack = False
    defence = 2
    movement = 5
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
    image = "Viking"
    attack = 3
    defence = 2
    movement = 1
    range = 1
    abonus = {}
    dbonus = {"Siege Weapon": 1}
    zoc = []
    type = "Infantry"

    rage = True

    descriptions = {"rage": "Can make an attack after it's move. (But not a second move.)"}

    upgrades = ["Viking II_A", "Viking II_B"]


class Viking_II_A(Unit):

    def __init__(self):
        self.extra_life = True  # It takes two hits to kill viking

    name = "Viking II_A"
    image = "Viking"
    attack = 4
    defence = 2
    movement = 1
    range = 1
    abonus = {}
    dbonus = {"Siege Weapon": 1}
    zoc = []
    type = "Infantry"

    rage = True

    descriptions = {"rage": "Can make an attack after it's move. (But not a second move.)"}


class Viking_II_B(Unit):

    def __init__(self):
        self.extra_life = True  # It takes two hits to kill viking

    name = "Viking II_B"
    image = "Viking"
    attack = 3
    defence = 3
    movement = 1
    range = 1
    abonus = {}
    dbonus = {"Siege Weapon": 1}
    zoc = []
    type = "Infantry"

    rage = True

    descriptions = {"rage": "Can make an attack after it's move. (But not a second move.)"}


class Cannon(Unit):
    
    name = "Cannon"
    image = "Cannon"
    attack = 5
    defence = 1
    movement = 1
    range = 4
    abonus = {}
    dbonus = {}
    zoc = []
    type = "Siege Weapon"
        
    attack_cooldown = 3
    xp_to_upgrade = 3

    descriptions = {"attack_cooldown": "Can only attack every third turn."}

    upgrades = ["Cannon II_A", "Cannon II_B"]


class Cannon_II_A(Unit):

    name = "Cannon II_A"
    image = "Cannon"
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


class Cannon_II_B(Unit):

    name = "Cannon II_B"
    image = "Cannon"
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
    image = "Lancer"
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

    upgrades = ["Lancer II_A", "Lancer II_B"]


class Lancer_II_A(Unit):

    name = "Lancer II_A"
    image = "Lancer"
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


class Lancer_II_B(Unit):

    name = "Lancer II_B"
    image = "Lancer"
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
    image = "Flag Bearer"
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

    upgrades = ["Flag Bearer II_A", "Flag Bearer II_B"]


class Flag_Bearer_II_A(Unit):

    name = "Flag Bearer II_A"
    image = "Flag Bearer"
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


class Flag_Bearer_II_B(Unit):

    name = "Flag Bearer II_B"
    image = "Flag Bearer"
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
    image = "Longswordsman"
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

    upgrades = ["Longswordsman II_A", "Longswordsman II_B"]


class Longswordsman_II_A(Unit):

    name = "Longswordsman II_A"
    image = "Longswordsman"
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


class Longswordsman_II_B(Unit):

    name = "Longswordsman II_B"
    image = "Longswordsman"
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
    image = "Crusader"
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

    upgrades = ["Crusader II_A", "Crusader II_B"]


class Crusader_II_A(Unit):

    name = "Crusader II_A"
    image = "Crusader"
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


class Crusader_II_B(Unit):

    name = "Crusader II_B"
    image = "Crusader"
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
    image = "Berserker"
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

    upgrades = ["Berserker II_A", "Berserker II_B"]


class Berserker_II_A(Unit):

    name = "Berserker II_A"
    image = "Berserker"
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


class Berserker_II_B(Unit):

    name = "Berserker II_B"
    image = "Berserker"
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
    image = "Chariot"
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

    upgrades = ["Chariot II_A", "Chariot II_B"]


class Chariot_II_A(Unit):

    name = "Chariot II_A"
    image = "Chariot"
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


class Chariot_II_B(Unit):

    name = "Chariot II_B"
    image = "Chariot"
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
    image = "War Elephant"
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
    xp_to_upgrade = 3

    descriptions = {"double_attack_cost": "Attack takes two actions.",
                    "triple_attack": "Also hits the two diagonally nearby tiles in the attack direction.",
                    "push": "If attack and defence rolls both succeed, it can still move forward. If not on back line, "
                            "opponents units must retreat directly backwards or die."}

    upgrades = ["War Elephant II_A", "War Elephant II_B"]


class War_Elephant_II_A(Unit):

    name = "War Elephant II_A"
    image = "War Elephant"
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


class War_Elephant_II_B(Unit):

    name = "War Elephant II_B"
    image = "War Elephant"
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
    image = "Samurai"
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

    upgrades = ["Samurai II_A", "Samurai II_B"]


class Samurai_II_A(Unit):

    name = "Samurai II_A"
    image = "Samurai"
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


class Samurai_II_B(Unit):

    name = "Samurai II_B"
    image = "Samurai"
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
    image = "Saboteur"
    attack = False
    defence = 2
    movement = 1
    range = 3
    abonus = {}
    dbonus = {}
    type = "Specialist"
    
    abilities = ["sabotage", "poison"]

    descriptions = {"sabotage": "Reduces a units defence to 0 for 1 turn.", "poison": "Freezes a unit for 2 turns."}

    upgrades = ["Saboteur II_A", "Saboteur II_B"]


class Saboteur_II_A(Unit):

    name = "Saboteur II_A"
    image = "Saboteur"
    attack = False
    defence = 2
    movement = 1
    range = 3
    abonus = {}
    dbonus = {}
    type = "Specialist"

    abilities = ["sabotage", "poison"]

    descriptions = {"sabotage": "Reduces a units defence to 0 for 1 turn.", "poison": "Freezes a unit for 2 turns."}


class Saboteur_II_B(Unit):

    name = "Saboteur II_B"
    image = "Saboteur"
    attack = False
    defence = 2
    movement = 1
    range = 3
    abonus = {}
    dbonus = {}
    type = "Specialist"

    abilities = ["sabotage", "poison"]

    descriptions = {"sabotage": "Reduces a units defence to 0 for 1 turn.", "poison": "Freezes a unit for 2 turns."}


class Diplomat(Unit):
    
    name = "Diplomat"
    image = "Diplomat"
    attack = False
    defence = 2
    movement = 1
    range = 3
    abonus = {}
    dbonus = {}
    type = "Specialist"
        
    abilities = ["bribe"]

    descriptions = {"bribe": "You can use an opponent's unit this turn. Your opponent can't use it on his next turn. "
                             "You can't bribe the same unit on your next turn. The unit gets +1A until end of turn."}

    upgrades = ["Diplomat II_A", "Diplomat II_B"]


class Diplomat_II_A(Unit):

    name = "Diplomat II_A"
    image = "Diplomat"
    attack = False
    defence = 2
    movement = 1
    range = 3
    abonus = {}
    dbonus = {}
    type = "Specialist"

    abilities = ["bribe"]

    descriptions = {"bribe": "You can use an opponent's unit this turn. Your opponent can't use it on his next turn. "
                             "You can't bribe the same unit on your next turn. The unit gets +1A until end of turn."}


class Diplomat_II_B(Unit):

    name = "Diplomat II_B"
    image = "Diplomat"
    attack = False
    defence = 2
    movement = 1
    range = 3
    abonus = {}
    dbonus = {}
    type = "Specialist"

    abilities = ["bribe"]

    descriptions = {"bribe": "You can use an opponent's unit this turn. Your opponent can't use it on his next turn. "
                             "You can't bribe the same unit on your next turn. The unit gets +1A until end of turn."}


class Weaponsmith(Unit):
    
    name = "Weaponsmith"
    image = "Weaponsmith"
    attack = False   
    defence = 2
    movement = 1
    range = 3
    abonus = {}
    dbonus = {}
    type = "Specialist"
    
    abilities = ["improve_weapons"]

    descriptions = {"improve_weapons": "Give melee unit +3 attack, +1 defence until your next turn"}

    upgrades = ["Weaponsmith II_A", "Weaponsmith II_B"]


class Weaponsmith_II_A(Unit):

    name = "Weaponsmith II_A"
    image = "Weaponsmith"
    attack = False
    defence = 2
    movement = 1
    range = 3
    abonus = {}
    dbonus = {}
    type = "Specialist"

    abilities = ["improve_weapons"]

    descriptions = {"improve_weapons": "Give melee unit +3 attack, +1 defence until your next turn"}


class Weaponsmith_II_B(Unit):

    name = "Weaponsmith II_B"
    image = "Weaponsmith"
    attack = False
    defence = 2
    movement = 1
    range = 3
    abonus = {}
    dbonus = {}
    type = "Specialist"

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
