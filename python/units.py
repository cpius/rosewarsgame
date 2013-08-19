from collections import defaultdict
import setup_settings as settings
from common import *


class Unit(object):
    def __init__(self):
        self.traits = defaultdict(int)
        self.states = defaultdict(int)
        self.abilities = defaultdict(int)

    name = ""
    zoc = []
    abilities = []
    experience_to_upgrade = settings.experience_to_upgrade
    attack_bonuses = {}
    defence_bonuses = {}
    traits = {}
    base_attack = 0
    base_defence = 0
    base_range = 0
    base_movement = 0
    type = None
    level = 0
    upgrades = []
    special_upgrades = []
    final_upgrades = []

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

    def __repr__(self):
        return self.name

    def set(self, attribute, n=1):
        if attribute in Trait.name:
            self.traits[attribute] = n
        elif attribute in Ability.name:
            self.abilities[attribute] = n
        else:
            self.states[attribute] = n

    def add(self, attr, n):
        if attr in Trait.name:
            self.traits[attr] += n
        elif attr in Ability.name:
            self.abilities[attr] += n
        elif attr in State.name:
            self.states[attr] += n

    def has(self, attribute, value=None):
        if not value and attribute in Trait.name:
            return self.traits[attribute]
        elif not value:
            return self.states[attribute]
        elif attribute in Trait.name:
            return self.traits[attribute] == value
        else:
            return self.states[attribute] == value

    def get(self, attribute):
        if attribute in Trait.name:
            return self.traits[attribute]
        else:
            return self.states[attribute]

    def increment(self, attribute):
        self.states[attribute] += 1

    def remove(self, attribute):
        if attribute in Trait.name:
            self.traits[attribute] = 0
        else:
            self.states[attribute] = 0

    def decrement(self, attribute):
        self.states[attribute] = max(0, self.states[attribute] - 1)

    def do(self, ability, value):
        if ability == Ability.poison:
            self.set(State.frozen, value + 1)

        if ability == Ability.sabotage:
            self.set(State.sabotaged, value)

        if ability == Ability.improve_weapons:
            if value == 2:
                self.set(State.improved_weapons_II, value)
            else:
                self.set(State.improved_weapons)

    # custom functions
    def poison(self):
        self.freeze(2)

    def freeze(self, n):
        self.set(State.frozen, max(self.get(State.frozen), n))

    def gain_xp(self):
        if not self.has(State.used) and not settings.beginner_mode:
            self.increment(State.experience)
            self.remove(State.recently_upgraded)

    def has_extra_life(self):
        return self.has(Trait.extra_life) and not self.has(State.lost_extra_life)

    def is_melee(self):
        return self.range == 1

    def is_ranged(self):
        return self.range > 1

    def get_upgrade_choice(self, choice_number):
        if getattr(self, "upgrades"):
            return self.upgrades[choice_number].replace(" ", "_")

        available_upgrades = []
        if getattr(self, "special_upgrades"):
            for upgrade in self.special_upgrades:
                for attribute in upgrade:
                    is_trait_already_upgraded = attribute in self.get_traits_not_in_base()
                    is_ability_already_upgraded = attribute in self.get_abilities_not_in_base()
                    if not is_trait_already_upgraded and not is_ability_already_upgraded:
                        available_upgrades.append(upgrade)

        if len(available_upgrades) == 2:
            return available_upgrades[choice_number]
        if len(available_upgrades) == 1:
            return [available_upgrades[0], self.final_upgrades[0]][choice_number]

        return self.final_upgrades[choice_number]

    def get_upgraded_unit(self, choice):
        simple_upgrade = False
        if getattr(self, "upgrades"):
            upgraded_unit = globals()[choice]()
            simple_upgrade = True
        else:
            upgraded_unit = globals()[self.name.replace(" ", "_")]()

        upgraded_unit.set(State.recently_upgraded)

        for state, value in self.states.items():
            upgraded_unit.add(state, value)

        if simple_upgrade:
            return upgraded_unit

        for trait, value in self.get_traits_not_in_base().items():
            upgraded_unit.add(trait, value)
        for ability, value in self.get_abilities_not_in_base().items():
            upgraded_unit.set(ability, value)

        for attribute, value in choice.items():
            upgraded_unit.add(attribute, value)

            if hasattr(upgraded_unit, "special_upgrades"):
                chosen_index = None
                for i, special_upgrade in enumerate(upgraded_unit.special_upgrades):
                    if special_upgrade == choice:
                        chosen_index = i
                if chosen_index is int:
                    del upgraded_unit.special_upgrades[chosen_index]

        return upgraded_unit

    def is_allowed_upgrade_choice(self, upgrade_choice):
        if not self.is_milf():
            return False

        return upgrade_choice in [self.get_upgrade_choice(0), self.get_upgrade_choice(1)]

    def get_abilities_not_in_base(self):
        abilities = self.abilities.copy()
        base_unit = globals()[self.name.replace(" ", "_")]()
        for ability, value in abilities.items():
            if ability in base_unit.abilities and value == base_unit.abilities[ability]:
                del abilities[ability]

        return abilities

    def get_traits_not_in_base(self):
        traits = dict((trait, value) for trait, value in self.traits.items() if value)

        base_unit = globals()[self.name.replace(" ", "_")]()
        for trait in base_unit.traits:
            if trait in traits:
                del traits[trait]

        return traits

    def get_states(self):
        return dict((state, value) for state, value in self.states.items() if value)

    def is_milf(self):
        experience = self.get(State.experience)
        to_upgrade = self.experience_to_upgrade
        return experience and experience % to_upgrade == 0 and not self.get(State.recently_upgraded)

    def to_document(self):
        attributes = merge(self.get_states(), self.get_traits_not_in_base(), self.get_abilities_not_in_base())

        if attributes:
            unit_dict = readable_attributes(attributes)
            unit_dict["name"] = self.name
            return unit_dict
        else:
            return self.name

    @classmethod
    def make(cls, name):
        name = name.replace(" ", "_")
        return globals()[name]()


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
    upgrades = ["Fire_Archer", "Crossbow_Archer"]


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
    attack_bonuses = {Type.Infantry: 1}
    type = Type.Infantry
    special_upgrades = [{Trait.sharpshooting: 1}]
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
    final_upgrades = [{Trait.range_skill: 1}, {Trait.attack_skill: 1}]


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
    type = Type.Infantry
    zoc = [Type.Cavalry]
    upgrades = ["Halberdier", "Royal_Guard"]
    experience_to_upgrade = 3


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
    experience_to_upgrade = 3


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
    #special_upgrades = [{Trait.flanking: 1}]
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
    #special_upgrades = [{Trait.cavalry_specialist: 1}, {Trait.lancing: 1, Trait.movement_skill: 1}]
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
    #special_upgrades = [{Trait.flanking: 1}]
    final_upgrades = [{Trait.attack_skill: 1}, {Trait.defence_skill: 1}]


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
    experience_to_upgrade = 2
    final_upgrades = [{Trait.attack_skill: 1}, {Trait.range_skill: 1}]


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
    experience_to_upgrade = 3
    #special_upgrades = [{Trait.melee_expert: 1}, {Trait.tall_shield: 1, Trait.melee_freeze: 1}]
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
    experience_to_upgrade = 2
    #special_upgrades = [{Trait.tall_shield}, {Trait.attack_skill: 2}]
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
    #special_upgrades = [{Trait.rage: 1}, {Trait.siege_weapon_specialist: 1}]
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
    experience_to_upgrade = 3
    #special_upgrades = [{Trait.fire_arrows: 1}, {Trait.attack_cooldown: 2, Trait.far_sighted: 1}]
    final_upgrades = [{Trait.attack_skill: 1}, {Trait.range_skill: 1}]


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
    #special_upgrades = [{Trait.flag_bearing_B: 1}]
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
    #special_upgrades = [{Trait.rage: 1}]
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
    #special_upgrades = [{Trait.crusading: 1}]
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
    #special_upgrades = [{Trait.big_shield: 1}, {Trait.attack_skill: 2}]
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
    experience_to_upgrade = 3

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
    #special_upgrades = [{Trait.bloodlust: 1}],
    final_upgrades = [{Trait.attack_skill: 1}, {Trait.defence_skill: 1}]

    traits = {Trait.combat_agility: 1}


class Saboteur(Unit):
    def __init__(self):
        super(Saboteur, self).__init__()
        self.set(Ability.sabotage, 1)
        self.set(Ability.poison, 1)
    name = "Saboteur"
    image = "Saboteur"
    base_attack = 0
    base_defence = 2
    base_movement = 1
    base_range = 3
    attack_bonuses = {}
    defence_bonuses = {}
    type = Type.Specialist
    #special_upgrades = [{Ability.sabotage: 1}, {Ability.poison: 1}]
    final_upgrades = [{Trait.range_skill: 1}, {Trait.defence_skill: 1}]


class Diplomat(Unit):
    def __init__(self):
        super(Diplomat, self).__init__()
        self.set(Ability.bribe)
    name = "Diplomat"
    image = "Diplomat"
    base_attack = 0
    base_defence = 2
    base_movement = 1
    base_range = 3
    attack_bonuses = {}
    defence_bonuses = {}
    type = Type.Specialist
    #special_upgrades = [{Ability.bribe: 1}]
    final_upgrades = [{Trait.range_skill: 1}, {Trait.defence_skill: 1}]


class Weaponsmith(Unit):
    def __init__(self):
        super(Weaponsmith, self).__init__()
        self.set(Ability.improve_weapons, 1)

    name = "Weaponsmith"
    image = "Weaponsmith"
    base_attack = 0
    base_defence = 2
    base_movement = 1
    base_range = 4
    attack_bonuses = {}
    defence_bonuses = {}
    type = Type.Specialist
    #special_upgrades = [{Ability.improve_weapons: 1}]
    final_upgrades = [{Trait.range_skill: 1}, {Trait.defence_skill: 1}]
