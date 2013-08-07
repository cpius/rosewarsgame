from collections import defaultdict
import settings
from common import *


class Unit(object):
    def __init__(self):
        self.variables = defaultdict(int)

    name = ""
    zoc = []
    abilities = []
    xp_to_upgrade = 4
    upgrades = []
    attack_bonuses = {}
    defence_bonuses = {}
    constants = []
    range = 0
    custom_ability = {Ability.poison: "poison",
                      Ability.poison_II: "poison_II",
                      Ability.improve_weapons_II_A: "improve_weapons_II_A",
                      Ability.improve_weapons_II_B: "improve_weapons_II_B"}
    apply_ability = {Ability.sabotage: Trait.sabotaged,
                     Ability.sabotage_II: Trait.sabotaged_II,
                     Ability.improve_weapons: Trait.improved_weapons}

    def __repr__(self):
        return self.name

    def set(self, attribute, n=1):
        self.variables[attribute] = n

    def has(self, attribute):
        return attribute in self.constants or self.variables[attribute]

    def get(self, attribute):
        return self.variables[attribute]

    def increment(self, attribute):
        self.variables[attribute] += 1

    def remove(self, attribute):
        self.variables[attribute] = 0

    def decrement(self, attribute):
        self.variables[attribute] = max(0, self.variables["attribute"] - 1)

    def do(self, ability):
        if ability in self.apply_ability:
            self.set(self.apply_ability[ability])
        if ability in self.custom_ability:
            getattr(self, self.custom_ability[ability])()

    # custom functions
    def poison(self):
        self.freeze(2)

    def poison_II(self):
        self.freeze(3)

    def freeze(self, n):
        self.set(Trait.frozen, max(self.get(Trait.frozen), n))

    def gain_xp(self):
        if not self.has(Trait.used) and not settings.beginner_mode:
            self.increment(Trait.xp)

    def improve_weapons_II_A(self):
        self.set(Trait.improved_weapons_II_A, 2)

    def improve_weapons_II_B(self):
        self.variables[Trait.improved_weapons_II_B] = 1
        self.zoc = {Type.Cavalry}

    def has_extra_life(self):
        return self.has(Trait.extra_life) and not self.has(Trait.lost_extra_life)

    def is_melee(self):
        return self.range == 1

    def is_ranged(self):
        return self.range > 1

    def is_bribed(self):
        return self.has(Trait.bribed) or self.has(Trait.bribed_II)


class Archer(Unit):

    name = "Archer"
    image = "Archer"
    attack = 2
    defence = 2
    movement = 1
    range = 4
    attack_bonuses = {Type.Infantry: 1}
    defence_bonuses = {}
    type = Type.Infantry
    upgrades = ["Longbowman", "Crossbow Archer"]


class Longbowman(Unit):
    name = "Longbowman"
    image = "Archer"
    attack = 2
    defence = 2
    movement = 1
    range = 4
    type = Type.Infantry
    upgrades = ["Longbowman II_A", "Longbowman II_B"]

    constants = [Trait.sharpshooting]


class Longbowman_II_A(Unit):
    name = "Longbowman II_A"
    image = "Archer"
    attack = 3
    defence = 2
    movement = 1
    range = 4
    attack_bonuses = {Type.Infantry: 1}
    defence_bonuses = {}
    type = Type.Infantry

    constants = [Trait.sharpshooting]


class Longbowman_II_B(Unit):
    name = "Longbowman II_B"
    image = "Archer"
    attack = 2
    defence = 3
    movement = 1
    range = 4
    attack_bonuses = {Type.Infantry: 1}
    defence_bonuses = {}
    type = Type.Infantry

    constants = [Trait.sharpshooting]


class Crossbow_Archer(Unit):
    name = "Crossbow Archer"
    image = "Archer"
    attack = 2
    defence = 3
    movement = 1
    range = 4
    attack_bonuses = {Type.Infantry: 1}
    defence_bonuses = {}
    type = Type.Infantry
    upgrades = ["Crossbow Archer II_A", "Crossbow Archer II_B"]


class Crossbow_Archer_II_A(Unit):
    name = "Crossbow Archer II_A"
    image = "Archer"
    attack = 3
    defence = 3
    movement = 1
    range = 4
    attack_bonuses = {Type.Infantry: 1}
    defence_bonuses = {}
    type = Type.Infantry


class Crossbow_Archer_II_B(Unit):
    name = "Crossbow Archer II_B"
    image = "Archer"
    attack = 2
    defence = 4
    movement = 1
    range = 4
    attack_bonuses = {Type.Infantry: 1}
    defence_bonuses = {}
    type = Type.Infantry


class Pikeman(Unit):

    name = "Pikeman"
    image = "Pikeman"
    attack = 2
    defence = 2
    movement = 1
    range = 1
    attack_bonuses = {Type.Cavalry: 1}
    defence_bonuses = {Type.Cavalry: 1}
    type = Type.Infantry
    zoc = [Type.Cavalry]
    upgrades = ["Halberdier", "Royal Guard"]
    xp_to_upgrade = 3


class Halberdier(Unit):
    name = "Halberdier"
    image = "Pikeman"
    attack = 4
    defence = 3
    movement = 1
    range = 1
    type = Type.Infantry

    constants = [Trait.push]


class Halberdier_II_A(Unit):
    name = "Halberdier"
    image = "Pikeman"
    attack = 5
    defence = 3
    movement = 1
    range = 1
    type = Type.Infantry

    constants = [Trait.push]


class Halberdier_II_B(Unit):
    name = "Halberdier"
    image = "Pikeman"
    attack = 4
    defence = 4
    movement = 1
    range = 1
    type = Type.Infantry

    constants = [Trait.push]


class Light_Cavalry(Unit):

    name = "Light Cavalry"
    image = "Light Cavalry"
    attack = 2
    defence = 2
    movement = 4
    range = 1
    attack_bonuses = {}
    defence_bonuses = {}
    type = Type.Cavalry
    upgrades = ["Dragoon", "Cavalry Lieutenant"]
    xp_to_upgrade = 3


class Dragoon(Unit):

    name = "Dragoon"
    image = "Light Cavalry"
    attack = 2
    defence = 2
    movement = 4
    range = 1
    attack_bonuses = {}
    defence_bonuses = {}
    type = Type.Cavalry
    upgrades = ["Dragoon II_A", "Dragoon II_B"]

    constants = [Trait.swiftness]


class Dragoon_II_A(Unit):

    name = "Dragoon"
    image = "Light Cavalry"
    attack = 3
    defence = 2
    movement = 4
    range = 1
    attack_bonuses = {}
    defence_bonuses = {}
    type = Type.Cavalry
    upgrades = ["Dragoon II_A", "Dragoon II_B"]

    constants = [Trait.swiftness]


class Dragoon_II_B(Unit):

    name = "Dragoon"
    image = "Light Cavalry"
    attack = 2
    defence = 3
    movement = 4
    range = 1
    attack_bonuses = {}
    defence_bonuses = {}
    type = Type.Cavalry
    upgrades = ["Dragoon II_A", "Dragoon II_B"]

    constants = [Trait.swiftness]


class Cavalry_Lieutenant(Unit):

    name = "Cavalry Lieutenant"
    image = "Light Cavalry"
    attack = 3
    defence = 2
    movement = 3
    range = 1
    attack_bonuses = {}
    defence_bonuses = {}
    type = Type.Cavalry
    upgrades = ["Cavalry_Luitenant_II_A", "Cavalry_Luitenant_II_B"]

    constants = [Trait.cavalry_charging]


class Cavalry_Lieutenant_II_A(Unit):

    name = "Cavalry Lieutenant II_A"
    image = "Light Cavalry"
    attack = 3
    defence = 3
    movement = 4
    range = 1
    attack_bonuses = {}
    defence_bonuses = {}
    type = Type.Cavalry

    constants = [Trait.cavalry_charging]


class Cavalry_Lieutenant_II_B(Unit):

    name = "Cavalry Lieutenant II_B"
    image = "Light Cavalry"
    attack = 4
    defence = 3
    movement = 3
    range = 1
    attack_bonuses = {}
    defence_bonuses = {}
    type = Type.Cavalry

    constants = [Trait.cavalry_charging]


class Knight(Unit):

    name = "Knight"
    image = "Knight"
    attack = 3
    defence = 3
    movement = 2
    range = 1
    attack_bonuses = {}
    defence_bonuses = {}
    type = Type.Cavalry
    upgrades = ["Lancer", "Hobelar"]


class Ballista(Unit):
 
    name = "Ballista"
    image = "Ballista"
    attack = 4
    defence = 1
    movement = 1
    range = 3
    attack_bonuses = {}
    defence_bonuses = {}
    type = Type.Siege_Weapon
    upgrades = ["Cannon"]


class Catapult(Unit):

    name = "Catapult"
    image = "Catapult"
    attack = 6
    defence = 2
    movement = 1
    range = 3
    attack_bonuses = {}
    defence_bonuses = {}
    type = Type.Siege_Weapon
    xp_to_upgrade = 2

    constants = [Trait.double_attack_cost]


class Catapult_II_A(Unit):

    name = "Catapult II_A"
    image = "Catapult"
    attack = 7
    defence = 2
    movement = 1
    range = 3
    attack_bonuses = {}
    defence_bonuses = {}
    type = Type.Siege_Weapon
    xp_to_upgrade = 3
    upgrades = ["Catapult III_A", "Catapult III_B"]

    constants = [Trait.double_attack_cost]


class Catapult_II_B(Unit):

    name = "Catapult II_B"
    image = "Catapult"
    attack = 6
    defence = 2
    movement = 1
    range = 4
    attack_bonuses = {}
    defence_bonuses = {}
    type = Type.Siege_Weapon
    xp_to_upgrade = 3

    constants = [Trait.double_attack_cost]

    upgrades = ["Catapult III_B", "Catapult IIIC"]


class Catapult_III_A(Unit):

    name = "Catapult III_A"
    image = "Catapult"
    attack = 8
    defence = 2
    movement = 1
    range = 3
    attack_bonuses = {}
    defence_bonuses = {}
    type = Type.Siege_Weapon

    constants = [Trait.double_attack_cost]


class Catapult_III_B(Unit):

    name = "Catapult III_B"
    image = "Catapult"
    attack = 7
    defence = 2
    movement = 1
    range = 4
    attack_bonuses = {}
    defence_bonuses = {}
    type = Type.Siege_Weapon

    constants = [Trait.double_attack_cost]


class Catapult_III_C(Unit):

    name = "Catapult III_C"
    image = "Catapult"
    attack = 6
    defence = 2
    movement = 1
    range = 5
    attack_bonuses = {}
    defence_bonuses = {}
    type = Type.Siege_Weapon

    constants = [Trait.double_attack_cost]


class Royal_Guard(Unit):
  
    name = "Royal Guard"
    image = "Royal Guard"
    attack = 3
    defence = 3
    movement = 1
    range = 1
    attack_bonuses = {}
    defence_bonuses = {}
    type = Type.Infantry
    zoc = [Type.Cavalry, Type.Infantry, Type.Siege_Weapon, Type.Specialist]
    xp_to_upgrade = 3
    upgrades = ["Royal Guard II_A", "Royal Guard II_B"]

    constants = [Trait.defence_maneuverability]


class Royal_Guard_II_A(Unit):

    name = "Royal Guard II_A"
    image = "Royal Guard"
    attack = 3
    defence = 3
    movement = 1
    range = 1
    attack_bonuses = {}
    defence_bonuses = {}
    type = Type.Infantry
    zoc = [Type.Cavalry, Type.Infantry, Type.Siege_Weapon, Type.Siege_Weapon]

    constants = [Trait.defence_maneuverability, Trait.melee_expert]


class Royal_Guard_II_B(Unit):

    name = "Royal Guard II_B"
    image = "Royal Guard"
    attack = 3
    defence = 3
    movement = 1
    range = 1
    attack_bonuses = {}
    defence_bonuses = {}
    type = Type.Infantry
    zoc = [Type.Cavalry, Type.Infantry, Type.Siege_Weapon, Type.Specialist]

    constants = [Trait.defence_maneuverability, Trait.tall_shield, Trait.melee_freeze]


class Scout(Unit):
    
    name = "Scout"
    image = "Scout"
    attack = False
    defence = 2
    movement = 4
    range = 1
    attack_bonuses = {}
    defence_bonuses = {}
    zoc = []
    type = Type.Cavalry
    xp_to_upgrade = 2
    upgrades = ["Scout II_A", "Scout II_B"]

    constants = [Trait.scouting]


class Scout_II_A(Unit):

    name = "Scout II_A"
    image = "Scout"
    attack = 2
    defence = 3
    movement = 4
    range = 1
    attack_bonuses = {}
    defence_bonuses = {}
    zoc = []
    type = Type.Cavalry

    constants = [Trait.scouting]


class Scout_II_B(Unit):

    name = "Scout II_B"
    image = "Scout"
    attack = False
    defence = 2
    movement = 5
    range = 1
    attack_bonuses = {}
    defence_bonuses = {}
    zoc = []
    type = Type.Cavalry

    constants = [Trait.scouting, Trait.tall_shield]


class Viking(Unit):

    name = "Viking"
    image = "Viking"
    attack = 3
    defence = 2
    movement = 1
    range = 1
    attack_bonuses = {}
    defence_bonuses = {Type.Siege_Weapon: 1}
    zoc = []
    type = Type.Infantry
    upgrades = ["Viking II_A", "Viking II_B"]

    constants = [Trait.rage, Trait.extra_life]


class Viking_II_A(Unit):

    name = "Viking"
    image = "Viking"
    attack = 3
    defence = 2
    movement = 1
    range = 1
    attack_bonuses = {}
    defence_bonuses = {Type.Siege_Weapon: 1}
    zoc = []
    type = Type.Infantry

    constants = [Trait.rage_II, Trait.extra_life]


class Viking_II_B(Unit):

    name = "Viking"
    image = "Viking"
    attack = 3
    defence = 2
    movement = 1
    range = 1
    attack_bonuses = {Type.Siege_Weapon: 1}
    defence_bonuses = {Type.Siege_Weapon: 2}
    zoc = []
    type = Type.Infantry

    constants = [Trait.rage, Trait.extra_life]


class Cannon(Unit):
    
    name = "Cannon"
    image = "Cannon"
    attack = 5
    defence = 1
    movement = 1
    range = 4
    attack_bonuses = {}
    defence_bonuses = {}
    zoc = []
    type = Type.Siege_Weapon
    xp_to_upgrade = 3
    upgrades = ["Cannon II_A", "Cannon II_B"]

    constants = [Trait.attack_cooldown]


class Cannon_II_A(Unit):

    name = "Cannon II_A"
    image = "Cannon"
    attack = 5
    defence = 1
    movement = 1
    range = 4
    attack_bonuses = {Type.Siege_Weapon: 2}
    defence_bonuses = {}
    zoc = []
    type = Type.Siege_Weapon

    constants = [Trait.attack_cooldown]


class Cannon_II_B(Unit):

    name = "Cannon II_B"
    image = "Cannon"
    attack = 5
    defence = 1
    movement = 1
    range = 4
    attack_bonuses = {}
    defence_bonuses = {}
    zoc = []
    type = Type.Siege_Weapon

    constants = [Trait.attack_cooldown_II, Trait.far_sighted]


class Lancer(Unit):
    
    name = "Lancer"
    image = "Lancer"
    attack = 2
    defence = 3
    movement = 3
    range = 1
    attack_bonuses = {Type.Cavalry: 1}
    defence_bonuses = {}
    zoc = []
    type = Type.Cavalry
    upgrades = ["Lancer II_A", "Lancer II_B"]

    constants = [Trait.lancing]


class Lancer_II_A(Unit):

    name = "Lancer II_A"
    image = "Lancer"
    attack = 2
    defence = 3
    movement = 3
    range = 1
    attack_bonuses = {Type.Cavalry: 2}
    defence_bonuses = {Type.Cavalry: 1}
    zoc = []
    type = Type.Cavalry

    constants = [Trait.lancing]


class Lancer_II_B(Unit):

    name = "Lancer II_B"
    image = "Lancer"
    attack = 2
    defence = 3
    movement = 4
    range = 1
    attack_bonuses = {Type.Cavalry: 1}
    defence_bonuses = {}
    zoc = []
    type = Type.Cavalry

    constants = [Trait.lancing_II]


class Flag_Bearer(Unit):
   
    name = "Flag Bearer"
    image = "Flag Bearer"
    attack = 2
    defence = 3
    movement = 3
    range = 1
    attack_bonuses = {}
    defence_bonuses = {}
    zoc = []
    type = Type.Cavalry
    upgrades = ["Flag Bearer II_A", "Flag Bearer II_B"]

    constants = [Trait.flag_bearing]


class Flag_Bearer_II_A(Unit):

    name = "Flag Bearer II_A"
    image = "Flag Bearer"
    attack = 2
    defence = 3
    movement = 3
    range = 1
    attack_bonuses = {}
    defence_bonuses = {}
    zoc = []
    type = Type.Cavalry

    constants = [Trait.flag_bearing_II_A]


class Flag_Bearer_II_B(Unit):

    name = "Flag Bearer II_B"
    image = "Flag Bearer"
    attack = 2
    defence = 3
    movement = 3
    range = 1
    attack_bonuses = {}
    defence_bonuses = {}
    zoc = []
    type = Type.Cavalry

    constants = [Trait.flag_bearing_II_B]


class Longswordsman(Unit):

    name = "Longswordsman"
    image = "Longswordsman"
    attack = 3
    defence = 3
    movement = 1
    range = 1
    attack_bonuses = {}
    defence_bonuses = {}
    zoc = []
    type = Type.Infantry
    upgrades = ["Longswordsman II_A", "Longswordsman II_B"]

    constants = [Trait.longsword]


class Longswordsman_II_A(Unit):

    name = "Longswordsman II_A"
    image = "Longswordsman"
    attack = 3
    defence = 3
    movement = 1
    range = 1
    attack_bonuses = {}
    defence_bonuses = {}
    zoc = []
    type = Type.Infantry

    constants = [Trait.longsword]


class Longswordsman_II_B(Unit):

    name = "Longswordsman II_B"
    image = "Longswordsman"
    attack = 3
    defence = 3
    movement = 1
    range = 1
    attack_bonuses = {}
    defence_bonuses = {}
    zoc = []
    type = Type.Infantry

    constants = [Trait.longsword]


class Crusader(Unit):

    name = "Crusader"
    image = "Crusader"
    attack = 3
    defence = 3
    movement = 3
    range = 1
    attack_bonuses = {}
    defence_bonuses = {}
    zoc = []
    type = Type.Cavalry
    upgrades = ["Crusader II_A", "Crusader II_B"]

    constants = [Trait.crusading]


class Crusader_II_A(Unit):

    name = "Crusader II_A"
    image = "Crusader"
    attack = 4
    defence = 3
    movement = 3
    range = 1
    attack_bonuses = {}
    defence_bonuses = {}
    zoc = []
    type = Type.Cavalry

    constants = [Trait.crusading]


class Crusader_II_B(Unit):

    name = "Crusader II_A"
    image = "Crusader"
    attack = 4
    defence = 3
    movement = 3
    range = 1
    attack_bonuses = {}
    defence_bonuses = {}
    zoc = []
    type = Type.Cavalry

    constants = [Trait.crusading_II]


class Berserker(Unit):

    name = "Berserker"
    image = "Berserker"
    attack = 5
    defence = 1
    movement = 1
    range = 1
    attack_bonuses = {}
    defence_bonuses = {}
    zoc = []
    type = Type.Infantry
    upgrades = ["Berserker II_A", "Berserker II_B"]

    constants = [Trait.berserking]


class Berserker_II_A(Unit):

    name = "Berserker II_A"
    image = "Berserker"
    attack = 5
    defence = 1
    movement = 1
    range = 1
    attack_bonuses = {}
    defence_bonuses = {}
    zoc = []
    type = Type.Infantry

    constants = [Trait.berserking, Trait.big_shield]


class Berserker_II_B(Unit):

    name = "Berserker II_B"
    image = "Berserker"
    attack = 7
    defence = 1
    movement = 1
    range = 1
    attack_bonuses = {}
    defence_bonuses = {}
    zoc = []
    type = Type.Infantry

    constants = [Trait.berserking]


class Hobelar(Unit):

    name = "Hobelar"
    image = "Hobelar"
    attack = 3
    defence = 3
    movement = 3
    range = 1
    attack_bonuses = {}
    defence_bonuses = {}
    zoc = []
    type = Type.Cavalry
    upgrades = ["Hobelar II_A", "Hobelar II_B"]

    constants = [Trait.swiftness]


class Hobelar_II_A(Unit):

    name = "Hobelar II_A"
    image = "Hobelar"
    attack = 3
    defence = 3
    movement = 4
    range = 1
    attack_bonuses = {}
    defence_bonuses = {}
    zoc = []
    type = Type.Cavalry

    constants = [Trait.swiftness]


class Hobelar_II_B(Unit):

    name = "Hobelar II_B"
    image = "Hobelar"
    attack = 3
    defence = 3
    movement = 3
    range = 1
    attack_bonuses = {Type.Infantry: 2}
    defence_bonuses = {}
    zoc = []
    type = Type.Cavalry

    constants = [Trait.swiftness]


class War_Elephant(Unit):

    name = "War Elephant"
    image = "War Elephant"
    attack = 3
    defence = 3
    movement = 2
    range = 1
    attack_bonuses = {}
    defence_bonuses = {}
    zoc = []
    type = Type.Cavalry
    upgrades = ["War Elephant II_A", "War Elephant II_B"]
    xp_to_upgrade = 3

    constants = [Trait.double_attack_cost, Trait.triple_attack, Trait.push]


class War_Elephant_II_A(Unit):

    name = "War Elephant II_A"
    image = "War Elephant"
    attack = 4
    defence = 3
    movement = 2
    range = 1
    attack_bonuses = {}
    defence_bonuses = {}
    zoc = []
    type = Type.Cavalry

    constants = [Trait.double_attack_cost, Trait.triple_attack, Trait.push]


class War_Elephant_II_B(Unit):

    name = "War Elephant II_B"
    image = "War Elephant"
    attack = 3
    defence = 4
    movement = 2
    range = 1
    attack_bonuses = {}
    defence_bonuses = {}
    zoc = []
    type = Type.Cavalry

    constants = [Trait.double_attack_cost, Trait.triple_attack, Trait.push]


class Samurai(Unit):
    
    name = "Samurai"
    image = "Samurai"
    attack = 3
    defence = 3
    movement = 1
    range = 1
    attack_bonuses = {Type.Infantry: 1}
    defence_bonuses = {}
    zoc = []
    type = Type.Infantry
    upgrades = ["Samurai II_A", "Samurai II_B"]

    constants = [Trait.combat_agility]


class Samurai_II_A(Unit):

    name = "Samurai II_A"
    image = "Samurai"
    attack = 4
    defence = 3
    movement = 1
    range = 1
    attack_bonuses = {Type.Infantry: 1}
    defence_bonuses = {}
    zoc = []
    type = Type.Infantry

    constants = [Trait.combat_agility]


class Samurai_II_B(Unit):

    name = "Samurai II_B"
    image = "Samurai"
    attack = 3
    defence = 3
    movement = 1
    range = 1
    attack_bonuses = {Type.Infantry: 1}
    defence_bonuses = {}
    zoc = []
    type = Type.Infantry

    constants = [Trait.combat_agility, Trait.bloodlust]


class Saboteur(Unit):
    
    name = "Saboteur"
    image = "Saboteur"
    attack = False
    defence = 2
    movement = 1
    range = 3
    attack_bonuses = {}
    defence_bonuses = {}
    type = Type.Specialist
    upgrades = ["Saboteur II_A", "Saboteur II_B"]

    abilities = [Ability.sabotage, Ability.poison]


class Saboteur_II_A(Unit):

    name = "Saboteur II_A"
    image = "Saboteur"
    attack = False
    defence = 2
    movement = 1
    range = 3
    attack_bonuses = {}
    defence_bonuses = {}
    type = Type.Specialist

    abilities = [Ability.sabotage, Ability.poison_II]


class Saboteur_II_B(Unit):

    name = "Saboteur II_B"
    image = "Saboteur"
    attack = False
    defence = 2
    movement = 1
    range = 3
    attack_bonuses = {}
    defence_bonuses = {}
    type = Type.Specialist

    abilities = [Ability.sabotage_II, Ability.poison]


class Diplomat(Unit):
    
    name = "Diplomat"
    image = "Diplomat"
    attack = False
    defence = 2
    movement = 1
    range = 3
    attack_bonuses = {}
    defence_bonuses = {}
    type = Type.Specialist
    upgrades = ["Diplomat II_A", "Diplomat II_B"]

    abilities = [Ability.bribe]


class Diplomat_II_A(Unit):

    name = "Diplomat II_A"
    image = "Diplomat"
    attack = False
    defence = 2
    movement = 1
    range = 4
    attack_bonuses = {}
    defence_bonuses = {}
    type = Type.Specialist

    abilities = [Ability.bribe]


class Diplomat_II_B(Unit):

    name = "Diplomat II_B"
    image = "Diplomat"
    attack = False
    defence = 2
    movement = 1
    range = 3
    attack_bonuses = {}
    defence_bonuses = {}
    type = Type.Specialist

    abilities = [Ability.bribe_II]


class Weaponsmith(Unit):
    
    name = "Weaponsmith"
    image = "Weaponsmith"
    attack = False   
    defence = 2
    movement = 1
    range = 4
    attack_bonuses = {}
    defence_bonuses = {}
    type = Type.Specialist
    upgrades = ["Weaponsmith II_A", "Weaponsmith II_B"]

    abilities = [Ability.improve_weapons]


class Weaponsmith_II_A(Unit):

    name = "Weaponsmith II_A"
    image = "Weaponsmith"
    attack = False
    defence = 2
    movement = 1
    range = 4
    attack_bonuses = {}
    defence_bonuses = {}
    type = Type.Specialist

    abilities = [Ability.improve_weapons_II_A]


class Weaponsmith_II_B(Unit):

    name = "Weaponsmith II_B"
    image = "Weaponsmith"
    attack = False
    defence = 2
    movement = 1
    range = 4
    attack_bonuses = {}
    defence_bonuses = {}
    type = Type.Specialist

    abilities = [Ability.improve_weapons_II_B]


class Hussar(Unit):

    name = "Hussar"
    image = "Hussar"
    attack = 2
    defence = 2
    movement = 3
    range = 1
    attack_bonuses = {}
    defence_bonuses = {}
    zoc = []
    type = Type.Cavalry
    upgrades = ["Hussar II_A", "Hussar II_B"]

    constants = [Trait.triple_attack, Trait.pikeman_specialist]


class Hussar_II_A(Unit):

    name = "Hussar II_A"
    image = "Hussar"
    attack = 3
    defence = 2
    movement = 3
    range = 1
    attack_bonuses = {}
    defence_bonuses = {}
    zoc = []
    type = Type.Cavalry

    constants = [Trait.triple_attack, Trait.pikeman_specialist]


class Hussar_II_B(Unit):

    name = "Hussar II_B"
    image = "Hussar"
    attack = 2
    defence = 3
    movement = 3
    range = 1
    attack_bonuses = {}
    defence_bonuses = {}
    zoc = []
    type = Type.Cavalry

    constants = [Trait.triple_attack, Trait.pikeman_specialist]
