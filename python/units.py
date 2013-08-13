from collections import defaultdict
import settings
from common import *


class Unit(object):
    def __init__(self):
        self.traits = defaultdict(int)
        self.states = defaultdict(int)

    name = ""
    zoc = []
    abilities = []
    xp_to_upgrade = 4
    upgrades = []
    attack_bonuses = {}
    defence_bonuses = {}
    traits = {}
    base_attack = 0
    base_defence = 0
    base_range = 0
    base_movement = 0

    @property
    def attack(self):
        return self.base_attack + self.get(Trait.attack_skill)

    @property
    def defence(self):
        return self.base_defence + self.get(Trait.defence_skill)

    @property
    def range(self):
        return self.base_range + self.get(Trait.range_skill)

    @property
    def movement(self):
        return self.base_movement + self.get(Trait.movement_skill)

    type = None
    level = 0
    upgrades = []
    special_upgrades = []
    final_upgrades = []
    custom_ability = {Ability.poison: "poison",
                      Ability.poison_II: "poison_II",
                      Ability.improve_weapons_II_A: "improve_weapons_II_A"}
    apply_ability = {Ability.sabotage: State.sabotaged,
                     Ability.sabotage_II: State.sabotaged_II,
                     Ability.improve_weapons: State.improved_weapons}

    def __repr__(self):
        return self.name

    def set(self, attr, n=1):
        if is_trait(attr):
            self.traits[attr] = n
            self.remove_lower_traits(attr)
        else:
            self.states[attr] = n

    def add(self, attr, n):
        if is_trait(attr):
            self.traits[attr] += n
            self.remove_lower_traits(attr)
        else:
            self.states[attr] += n

    def has(self, attribute):
        return self.traits[attribute] or self.states[attribute]

    def get(self, attribute):
        if is_trait(attribute):
            return self.traits[attribute]
        else:
            return self.states[attribute]

    def increment(self, attribute):
        self.states[attribute] += 1

    def remove(self, attr):
        if is_trait(attr):
            self.traits[attr] = 0
        else:
            self.states[attr] = 0

    def decrement(self, attribute):
        self.states[attribute] = max(0, self.states[attribute] - 1)

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
        self.set(State.frozen, max(self.get(State.frozen), n))

    def gain_xp(self):
        if not self.has(State.used) and not settings.beginner_mode:
            self.increment(State.xp)

    def improve_weapons_II_A(self):
        self.set(State.improved_weapons_II_A, 2)

    def has_extra_life(self):
        return self.has(Trait.extra_life) and not self.has(State.lost_extra_life)

    def is_melee(self):
        return self.range == 1

    def is_ranged(self):
        return self.range > 1

    def is_bribed(self):
        return self.has(State.bribed) or self.has(State.bribed_II)

    def remove_lower_traits(self, trait):
        if trait == Trait.attack_cooldown_II:
            self.remove(Trait.attack_cooldown)
        elif trait == Trait.crusading_II:
            self.remove(Trait.crusading)
        elif trait in [Trait.flag_bearing_II_A, Trait.flag_bearing_II_B]:
            self.remove(Trait.flag_bearing)
        elif trait == Trait.lancing_II:
            self.remove(Trait.lancing)
        elif trait == Trait.rage_II:
            self.remove(Trait.rage)

    def get_upgrade_choice(self, choice_number):
        if getattr(self, "upgrades"):
            return self.upgrades[choice_number].replace(" ", "_")

        if getattr(self, "special_upgrades"):
            available_special_upgrades = [upgrade for upgrade in self.special_upgrades if upgrade.keys()[0] not in self.traits]
        else:
            available_special_upgrades = []

        if len(available_special_upgrades) == 1:
            choices = [available_special_upgrades[0], self.final_upgrades[0]]
        elif len(available_special_upgrades) == 2:
            choices = available_special_upgrades
        else:
            choices = self.final_upgrades

        return choices[choice_number]

    def get_upgraded_unit(self, choice):
        if getattr(self, "upgrades"):
            return globals()[choice]()

        upgrade = globals()[self.name.replace(" ", "_")]()
        for state, value in self.states.items():
            upgrade.add(state, value)
        for trait, value in self.traits.items():
            upgrade.add(trait, value)
        for trait, value in choice.items():
            upgrade.add(trait, value)

        return upgrade

    def get_traits_not_in_base(self):
        traits = dict((trait, value) for trait, value in self.traits.items() if value)
        base_unit = globals()[self.name.replace(" ", "_")]()
        for trait in base_unit.traits:
            del traits[trait]

        return traits

    def get_states(self):
        return dict((state, value) for state, value in self.states.items() if value)

    def has_xp_required_to_upgrade(self):
        return self.get(State.xp) % self.xp_to_upgrade == 0


class Archer(Unit):

    name = "Archer"
    image = "Archer"
    base_attack = 2
    base_defence = 2
    base_movement = 1
    base_range = 4
    attack_bonuses = {Type.Infantry: 1}
    defence_bonuses = {}
    type = Type.Infantry
    upgrades = ["Fire Archer", "Crossbow Archer"]


class Fire_Archer(Unit):
    def __init__(self):
        super(Fire_Archer, self).__init__()
        self.set(Trait.fire_arrows, 1)
    name = "Fire Archer"
    image = "Fire Archer"
    base_attack = 2
    base_defence = 2
    base_movement = 1
    base_range = 4
    type = Type.Infantry
    final_upgrades = [{Trait.attack_skill: 1}, {Trait.range_skill: 1}]


class Crossbow_Archer(Unit):
    def __init__(self):
        super(Crossbow_Archer, self).__init__()
        self.set(Trait.sharpshooting, 1)
    name = "Crossbow Archer"
    image = "Crossbow Archer"
    base_attack = 2
    base_defence = 2
    base_movement = 1
    base_range = 4
    attack_bonuses = {Type.Infantry: 1}
    defence_bonuses = {}
    type = Type.Infantry
    special_upgrades = [{Trait.fire_arrows: 1}]
    final_upgrades = [{Trait.range_skill: 1}, {Trait.attack_skill: 1}, ]


class Pikeman(Unit):
    def __init__(self):
        super(Pikeman, self).__init__()
        self.set(Trait.cavalry_specialist, 1)
    name = "Pikeman"
    image = "Pikeman"
    base_attack = 2
    base_defence = 2
    base_movement = 1
    base_range = 1
    #attack_bonuses = {Type.Cavalry: 1}
    #defence_bonuses = {Type.Cavalry: 1}
    type = Type.Infantry
    zoc = [Type.Cavalry]
    upgrades = ["Halberdier", "Royal Guard"]
    xp_to_upgrade = 3


class Halberdier(Unit):
    def __init__(self):
        super(Halberdier, self).__init__()
        self.set(Trait.push, 1)
    name = "Halberdier"
    image = "Halberdier"
    base_attack = 3
    base_defence = 2
    base_movement = 1
    base_range = 1
    attack_bonuses = {Type.Cavalry: 1}
    defence_bonuses = {Type.Cavalry: 1}
    type = Type.Infantry
    final_upgrades = [{Trait.attack_skill: 1}, {Trait.defence_skill: 1}]


class Light_Cavalry(Unit):

    name = "Light Cavalry"
    image = "Light Cavalry"
    base_attack = 2
    base_defence = 2
    base_movement = 4
    base_range = 1
    attack_bonuses = {}
    defence_bonuses = {}
    type = Type.Cavalry
    upgrades = ["Dragoon", "Hussar"]
    xp_to_upgrade = 3


class Dragoon(Unit):
    def __init__(self):
        super(Dragoon, self).__init__()
        self.set(Trait.swiftness, 1)

    name = "Dragoon"
    image = "Dragoon"
    base_attack = 2
    base_defence = 2
    base_movement = 4
    base_range = 1
    attack_bonuses = {}
    defence_bonuses = {}
    type = Type.Cavalry
    special_upgrades = [{Trait.flanking: 1}]
    final_upgrades = [{Trait.attack_skill: 1}, {Trait.defence_skill: 1}]

    traits = {Trait.swiftness: 1}


class Hussar(Unit):
    def __init__(self):
        super(Hussar, self).__init__()
        self.set(Trait.triple_attack, 1)

    name = "Hussar"
    image = "Hussar"
    base_attack = 2
    base_defence = 2
    base_movement = 4
    base_range = 1
    attack_bonuses = {}
    defence_bonuses = {}
    zoc = []
    type = Type.Cavalry
    final_upgrades = [{Trait.attack_skill: 1}, {Trait.movement_skill: 1}]


class Cavalry_Lieutenant(Unit):
    def __init__(self):
        super(Cavalry_Lieutenant, self).__init__()
        self.set(Trait.cavalry_charging, 1)

    name = "Cavalry Lieutenant"
    image = "Light Cavalry"
    base_attack = 3
    base_defence = 2
    base_movement = 3
    base_range = 1
    attack_bonuses = {}
    defence_bonuses = {}
    type = Type.Cavalry
    final_upgrades = [{Trait.attack_skill: 1}, {Trait.defence_skill: 1}]


class Knight(Unit):

    name = "Knight"
    image = "Knight"
    base_attack = 3
    base_defence = 3
    base_movement = 2
    base_range = 1
    attack_bonuses = {}
    defence_bonuses = {}
    type = Type.Cavalry
    upgrades = ["Lancer", "Hobelar"]


class Lancer(Unit):
    def __init__(self):
        super(Lancer, self).__init__()
        self.set(Trait.lancing, 1)

    name = "Lancer"
    image = "Lancer"
    base_attack = 2
    base_defence = 3
    base_movement = 3
    base_range = 1
    attack_bonuses = {Type.Cavalry: 1}
    defence_bonuses = {}
    zoc = []
    type = Type.Cavalry
    special_upgrades = [{Trait.cavalry_specialist: 1}, {Trait.lancing_II: 1, Trait.movement_skill: 1}]
    final_upgrades = [{Trait.attack_skill: 1}, {Trait.defence_skill: 1}]


class Hobelar(Unit):
    def __init__(self):
        super(Hobelar, self).__init__()
        self.set(Trait.swiftness, 1)

    name = "Hobelar"
    image = "Hobelar"
    base_attack = 3
    base_defence = 3
    base_movement = 3
    base_range = 1
    attack_bonuses = {}
    defence_bonuses = {}
    zoc = []
    type = Type.Cavalry
    special_upgrades = [{Trait.flanking: 1}]


class Ballista(Unit):
 
    name = "Ballista"
    image = "Ballista"
    base_attack = 4
    base_defence = 1
    base_movement = 1
    base_range = 3
    attack_bonuses = {}
    defence_bonuses = {}
    type = Type.Siege_Weapon
    special_upgrades = [{Trait.fire_arrows: 1}]
    final_upgrades = [{Trait.attack_skill: 1}, {Trait.range_skill: 1}]


class Catapult(Unit):
    def __init__(self):
        super(Catapult, self).__init__()
        self.set(Trait.double_attack_cost, 1)

    name = "Catapult"
    image = "Catapult"
    base_attack = 6
    base_defence = 2
    base_movement = 1
    base_range = 3
    attack_bonuses = {}
    defence_bonuses = {}
    type = Type.Siege_Weapon
    xp_to_upgrade = 2
    final_upgrades = [[{Trait.attack_skill: 1}, {Trait.range_skill: 1}]]


class Royal_Guard(Unit):
    def __init__(self):
        super(Royal_Guard, self).__init__()
        self.set(Trait.defence_maneuverability, 1)
  
    name = "Royal Guard"
    image = "Royal Guard"
    base_attack = 3
    base_defence = 3
    base_movement = 1
    base_range = 1
    attack_bonuses = {}
    defence_bonuses = {}
    type = Type.Infantry
    zoc = [Type.Cavalry, Type.Infantry, Type.Siege_Weapon, Type.Specialist]
    xp_to_upgrade = 3
    special_upgrades = [{Trait.melee_expert: 1}, {Trait.tall_shield: 1, Trait.melee_freeze: 1}]
    final_upgrades = [{Trait.attack_skill: 1}, {Trait.defence_skill: 1}]


class Scout(Unit):
    def __init__(self):
        super(Scout, self).__init__()
        self.set(Trait.scouting, 1)
    
    name = "Scout"
    image = "Scout"
    base_attack = 0
    base_defence = 2
    base_movement = 4
    base_range = 1
    attack_bonuses = {}
    defence_bonuses = {}
    zoc = []
    type = Type.Cavalry
    xp_to_upgrade = 2
    special_upgrades = [{Trait.tall_shield}, {Trait.attack_skill: 2}]
    final_upgrades = [{Trait.movement_skill: 2}, {Trait.defence_skill}]


class Viking(Unit):
    def __init__(self):
        super(Viking, self).__init__()
        self.set(Trait.rage, 1)
        self.set(Trait.extra_life, 1)

    name = "Viking"
    image = "Viking"
    base_attack = 3
    base_defence = 2
    base_movement = 1
    base_range = 1
    attack_bonuses = {}
    defence_bonuses = {Type.Siege_Weapon: 1}
    zoc = []
    type = Type.Infantry
    special_upgrades = [{Trait.rage_II: 1}, {Trait.siege_weapon_specialist: 1}]
    final_upgrades = [{Trait.attack_skill: 1}, {Trait.defence_skill: 1}]

    traits = {Trait.rage: 1, Trait.extra_life: 1}


class Cannon(Unit):
    def __init__(self):
        super(Cannon, self).__init__()
        self.set(Trait.attack_cooldown, 1)
    
    name = "Cannon"
    image = "Cannon"
    base_attack = 5
    base_defence = 1
    base_movement = 1
    base_range = 4
    attack_bonuses = {}
    defence_bonuses = {}
    zoc = []
    type = Type.Siege_Weapon
    xp_to_upgrade = 3
    special_upgrades = [{Trait.fire_arrows: 1}, {Trait.attack_cooldown: 2, Trait.far_sighted: 1}]


class Flag_Bearer(Unit):
    def __init__(self):
        super(Flag_Bearer, self).__init__()
        self.set(Trait.flag_bearing, 1)
   
    name = "Flag Bearer"
    image = "Flag Bearer"
    base_attack = 2
    base_defence = 3
    base_movement = 3
    base_range = 1
    attack_bonuses = {}
    defence_bonuses = {}
    zoc = []
    type = Type.Cavalry
    special_upgrades = [{Trait.flag_bearing_II_A: 1}, {Trait.flag_bearing_II_B: 1}]
    final_upgrades = [{Trait.attack_skill: 1}, {Trait.defence_skill: 1}]


class Longswordsman(Unit):
    def __init__(self):
        super(Longswordsman, self).__init__()
        self.set(Trait.longsword, 1)

    name = "Longswordsman"
    image = "Longswordsman"
    base_attack = 3
    base_defence = 3
    base_movement = 1
    base_range = 1
    attack_bonuses = {}
    defence_bonuses = {}
    zoc = []
    type = Type.Infantry
    special_upgrades = [{Trait.rage: 1}]
    final_upgrades = [{Trait.attack_skill: 1}, {Trait.defence_skill: 1}]


class Crusader(Unit):
    def __init__(self):
        super(Crusader, self).__init__()
        self.set(Trait.crusading, 1)

    name = "Crusader"
    image = "Crusader"
    base_attack = 3
    base_defence = 3
    base_movement = 3
    base_range = 1
    attack_bonuses = {}
    defence_bonuses = {}
    zoc = []
    type = Type.Cavalry
    special_upgrades = [{Trait.crusading_II}]
    final_upgrades = [{Trait.attack_skill: 1}, {Trait.defence_skill: 1}]


class Berserker(Unit):
    def __init__(self):
        super(Berserker, self).__init__()
        self.set(Trait.berserking, 1)

    name = "Berserker"
    image = "Berserker"
    base_attack = 5
    base_defence = 1
    base_movement = 1
    base_range = 1
    attack_bonuses = {}
    defence_bonuses = {}
    zoc = []
    type = Type.Infantry
    special_upgrades = [{Trait.big_shield: 1}, {Trait.attack_skill: 2}]
    final_upgrades = [{Trait.attack_skill: 1}, {Trait.defence_skill: 1}]


class War_Elephant(Unit):
    def __init__(self):
        super(War_Elephant, self).__init__()
        self.set(Trait.double_attack_cost, 1)
        self.set(Trait.triple_attack, 1)
        self.set(Trait.push, 1)

    name = "War Elephant"
    image = "War Elephant"
    base_attack = 3
    base_defence = 3
    base_movement = 2
    base_range = 1
    attack_bonuses = {}
    defence_bonuses = {}
    zoc = []
    type = Type.Cavalry
    final_upgrades = [{Trait.defence_skill: 1}, {Trait.attack_skill: 1}]
    xp_to_upgrade = 3

    traits = {Trait.double_attack_cost: 1, Trait.triple_attack: 1, Trait.push: 1}


class Samurai(Unit):
    def __init__(self):
        super(Samurai, self).__init__()
        self.set(Trait.combat_agility, 1)

    name = "Samurai"
    image = "Samurai"
    base_attack = 3
    base_defence = 3
    base_movement = 1
    base_range = 1
    attack_bonuses = {Type.Infantry: 1}
    defence_bonuses = {}
    zoc = []
    type = Type.Infantry
    special_upgrades = [{Trait.bloodlust: 1}],
    final_upgrades = [{Trait.attack_skill: 1}, {Trait.defence_skill: 1}]

    traits = {Trait.combat_agility: 1}


class Saboteur(Unit):
    
    name = "Saboteur"
    image = "Saboteur"
    base_attack = 0
    base_defence = 2
    base_movement = 1
    base_range = 3
    attack_bonuses = {}
    defence_bonuses = {}
    type = Type.Specialist
    special_upgrades = [{Ability.sabotage_II: 1}, {Ability.poison_II: 1}]
    final_upgrades = [{Trait.range_skill: 1}, {Trait.defence_skill: 1}]

    abilities = [Ability.sabotage, Ability.poison]


class Diplomat(Unit):
    
    name = "Diplomat"
    image = "Diplomat"
    base_attack = 0
    base_defence = 2
    base_movement = 1
    base_range = 3
    attack_bonuses = {}
    defence_bonuses = {}
    type = Type.Specialist
    special_upgrades = [{Ability.bribe_II}]
    final_upgrades = [{Trait.range_skill: 1}, {Trait.defence_skill: 1}]

    abilities = [Ability.bribe]


class Weaponsmith(Unit):
    
    name = "Weaponsmith"
    image = "Weaponsmith"
    base_attack = 0
    base_defence = 2
    base_movement = 1
    base_range = 4
    attack_bonuses = {}
    defence_bonuses = {}
    type = Type.Specialist
    special_upgrades = [{State.improved_weapons_II_A: 1}]
    final_upgrades = [{Trait.range_skill: 1}, {Trait.defence_skill: 1}]

    abilities = [Ability.improve_weapons]

