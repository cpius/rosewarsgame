class Unit(object):

    name = ""
    xp = 0
    zoc = []
    abilities = []
    used = False
    xp_gained_this_round = False
    xp_to_upgrade = 2
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
    upgrades = ["Longbowman IIA", "Longbowman IIB"]

    sharpshooting = True

    descriptions = {"sharpshooting": "Targets have their defence reduced to 1 during the attack"}


class Longbowman_IIA(Unit):
    name = "Longbowman IIA"
    image = "Archer"
    attack = 4
    defence = 2
    movement = 1
    range = 4
    abonus = {"Infantry": 1}
    dbonus = {}
    type = "Infantry"


class Longbowman_IIB(Unit):
    name = "Longbowman IIB"
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
    upgrades = ["Crossbow Archer IIA", "Crossbow Archer IIB"]


class Crossbow_Archer_II_A(Unit):
    name = "Crossbow Archer IIA"
    image = "Archer"
    attack = 3
    defence = 3
    movement = 1
    range = 4
    abonus = {"Infantry": 1}
    dbonus = {}
    type = "Infantry"


class Crossbow_Archer_II_B(Unit):
    name = "Crossbow Archer IIB"
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


class Halberdier_IIA(Unit):
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


class Halberdier_IIB(Unit):
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
    upgrades = ["Dragoon IIA", "Dragoon IIB"]


class Dragoon_IIA(Unit):

    name = "Dragoon IIA"
    image = "Light Cavalry"
    attack = 4
    defence = 2
    movement = 4
    range = 1
    abonus = {}
    dbonus = {}
    type = "Cavalry"


class Dragoon_IIB(Unit):

    name = "Dragoon IIB"
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
    upgrades = ["Cavalry_Luitenant_IIA", "Cavalry_Luitenant_IIB"]


class Cavalry_Luitenant_IIA(Unit):

    name = "Cavalry Liuetenant IIA"
    image = "Light Cavalry"
    attack = 3
    defence = 3
    movement = 4
    range = 1
    abonus = {}
    dbonus = {}
    type = "Cavalry"


class Cavalry_Luitenant_IIB(Unit):

    name = "Cavalry Liuetenant IIB"
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
    upgrades = ["Trebuchet IIA", "Trebuchet IIA"]


class Trebuchet_IIA(Unit):

    name = "Trebuchet IIA"
    image = "Ballista"
    attack = 6
    defence = 1
    movement = 1
    range = 3
    abonus = {}
    dbonus = {}
    type = "Siege Weapon"


class Trebuchet_IIB(Unit):

    name = "Trebuchet IIB"
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

    descriptions = {"double_attack_cost": "Attack takes two actions."}


class Catapult_IIA(Unit):

    name = "Catapult IIA"
    image = "Catapult"
    attack = 6
    defence = 2
    movement = 1
    range = 3
    abonus = {}
    dbonus = {}
    type = "Siege Weapon"

    double_attack_cost = True

    descriptions = {"double_attack_cost": "Attack takes two actions."}

    upgrades = ["Catapult IIIA", "Catapult IIIB"]


class Catapult_IIB(Unit):

    name = "Catapult IIB"
    image = "Catapult"
    attack = 6
    defence = 2
    movement = 1
    range = 3
    abonus = {}
    dbonus = {}
    type = "Siege Weapon"

    double_attack_cost = True

    descriptions = {"double_attack_cost": "Attack takes two actions."}

    upgrades = ["Catapult IIIB", "Catapult IIIC"]


class Catapult_IIIA(Unit):

    name = "Catapult IIIA"
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


class Catapult_IIIA(Unit):

    name = "Catapult IIIB"
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


class Catapult_IIIA(Unit):

    name = "Catapult IIIC"
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

    descriptions = {"defence_maneuverability": "Can move two tiles if one of them is sideways.",
                    "shield": "+1D v melee units."}

    upgrades = ["Royal Guard IIA", "Royal Guard IIB"]


class Royal_Guard_IIA(Unit):

    name = "Royal Guard IIA"
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


class Royal_Guard_IIB(Unit):

    name = "Royal Guard IIB"
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

    descriptions = {"scouting": "Can move past all units."}

    upgrades = ["Scout IIA", "Scout IIB"]


class Scout_IIA(Unit):

    name = "Scout IIA"
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


class Scout_IIB(Unit):

    name = "Scout IIB"
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

    upgrades = ["Viking IIA", "Viking IIB"]


class Viking_IIA(Unit):

    def __init__(self):
        self.extra_life = True  # It takes two hits to kill viking

    name = "Viking IIA"
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


class Viking_IIB(Unit):

    def __init__(self):
        self.extra_life = True  # It takes two hits to kill viking

    name = "Viking IIB"
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

    descriptions = {"attack_cooldown": "Can only attack every third turn."}

    upgrades = ["Cannon IIA", "Cannon IIB"]


class Cannon_IIA(Unit):

    name = "Cannon IIA"
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


class Cannon_IIB(Unit):

    name = "Cannon IIB"
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

    upgrades = ["Lancer IIA", "Lancer IIB"]


class Lancer_IIA(Unit):

    name = "Lancer IIA"
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


class Lancer_IIB(Unit):

    name = "Lancer IIB"
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

    upgrades = ["Flag Bearer IIA", "Flag Bearer IIB"]


class Flag_Bearer_IIA(Unit):

    name = "Flag Bearer IIA"
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


class Flag_Bearer_IIB(Unit):

    name = "Flag Bearer IIB"
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

    upgrades = ["Longswordsman IIA", "Longswordsman IIB"]


class Longswordsman_IIA(Unit):

    name = "Longswordsman IIA"
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


class Longswordsman_IIB(Unit):

    name = "Longswordsman IIB"
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

    upgrades = ["Crusader IIA", "Crusader IIB"]


class Crusader_IIA(Unit):

    name = "Crusader IIA"
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


class Crusader_IIB(Unit):

    name = "Crusader IIB"
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

    upgrades = ["Berserker IIA", "Berserker IIB"]


class Berserker_IIA(Unit):

    name = "Berserker IIA"
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


class Berserker_IIB(Unit):

    name = "Berserker IIB"
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

    upgrades = ["Chariot IIA", "Chariot IIB"]


class Chariot_IIA(Unit):

    name = "Chariot IIA"
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


class Chariot_IIB(Unit):

    name = "Chariot IIB"
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

    descriptions = {"double_attack_cost": "Attack takes two actions.",
                    "triple_attack": "Also hits the two diagonally nearby tiles in the attack direction.",
                    "push": "If attack and defence rolls both succeed, it can still move forward. If not on back line, "
                            "opponents units must retreat directly backwards or die."}

    upgrades = ["War Elephant IIA", "War Elephant IIB"]



class War_Elephant_IIA(Unit):

    name = "War Elephant IIA"
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



class War_Elephant_IIB(Unit):

    name = "War Elephant IIB"
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

    upgrades = ["Samurai IIA", "Samurai IIB"]


class Samurai_IIA(Unit):

    name = "Samurai IIA"
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


class Samurai_IIB(Unit):

    name = "Samurai IIB"
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

    upgrades = ["Saboteur IIA", "Saboteur IIB"]


class Saboteur_IIA(Unit):

    name = "Saboteur IIA"
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


class Saboteur_IIB(Unit):

    name = "Saboteur IIB"
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

    upgrades = ["Diplomat IIA", "Diplomat IIB"]


class Diplomat_IIA(Unit):

    name = "Diplomat IIA"
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


class Diplomat_IIB(Unit):

    name = "Diplomat IIB"
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

    upgrades = ["Weaponsmith IIA", "Weaponsmith IIB"]


class Weaponsmith_IIA(Unit):

    name = "Weaponsmith IIA"
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


class Weaponsmith_IIB(Unit):

    name = "Weaponsmith IIB"
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
