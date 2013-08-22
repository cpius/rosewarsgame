from __future__ import division
import setup_settings as settings
from common import *


class Unit(object):
    def __init__(self):
        self.traits = {}
        self.states = {}
        self.abilities = {}
        self.effects = {}

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
        return self.base_attack + self.get_level(Trait.attack_skill)

    @property
    def defence(self):
        return self.base_defence + self.get_level(Trait.defence_skill)

    @property
    def range(self):
        return self.base_range + self.get_level(Trait.range_skill)

    @property
    def movement(self):
        return self.base_movement + self.get_level(Trait.movement_skill)

    def __repr__(self):
        return self.name

    def get_dict(self, attribute):
        if attribute in Trait.name:
            return self.traits
        elif attribute in Ability.name:
            return self.abilities
        elif attribute in Effect.name:
            return self.effects
        elif attribute in State.name:
            return self.states

    def set(self, attribute, value=1, level=1):
        self.get_dict(attribute)[attribute] = [value, level]

    def add(self, attribute, value, level=1):
        assert isinstance(value, int)
        dict = self.get_dict(attribute)
        if attribute in dict:
            dict[attribute][0] += value
        else:
            dict[attribute] = [value, level]

    def add_levels(self, attribute, levels=1):
        dict = self.get_dict(attribute)
        if attribute in dict:
            dict[attribute][1] += levels
        else:
            dict[attribute] = [1, levels]

    def has(self, attribute, value=None, level=None):
        if value:
            return self.get_value(attribute) == value
        elif level:
            return self.get_level(attribute) == level
        else:
            return self.get_value(attribute)

    def get(self, attribute):
        return self.get_value(attribute)

    def get_value(self, attribute):
        dict = self.get_dict(attribute)
        if attribute in dict:
            return dict[attribute][0]
        else:
            return 0

    def get_level(self, attribute):
        dict = self.get_dict(attribute)
        if attribute in dict:
            return dict[attribute][1]
        else:
            return 0

    def set_value(self, attribute, value, level=1):
        self.get_dict(attribute)[attribute] = [value, level]

    def remove(self, attribute):
        dict = self.get_dict(attribute)
        if attribute in dict:
            del dict[attribute]

    def decrement(self, attribute):
        dict = self.get_dict(attribute)
        if attribute in dict:
            dict[attribute][0] = max(0, dict[attribute][0] - 1)
            if dict[attribute][0] == 0:
                del dict[attribute]

    def increment(self, attribute):
        self.add(attribute, 1)

    def do(self, ability, level):
        if ability == Ability.poison:
            self.set(Effect.poisoned, level + 1)

        if ability == Ability.sabotage:
            self.set(Effect.sabotaged, level)

        if ability == Ability.improve_weapons:
            if level == 2:
                self.set(Effect.improved_weapons, 2, 2)
            else:
                self.set(Effect.improved_weapons)

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

    def get_upgrade_choice(self, choice_index):
        if getattr(self, "upgrades"):
            return self.upgrades[choice_index].replace(" ", "_")

        upgrades = []
        if getattr(self, "special_upgrades"):
            for upgrade in self.special_upgrades:
                if not self.has_upgrade(upgrade):
                    upgrades.append(upgrade)

        while len(upgrades) < 2:
            upgrades.append(self.final_upgrades[1 - len(upgrades)])

        return dict((key, [1, level]) for key, level in upgrades[choice_index].items())

    def has_upgrade(self, upgrade):
        attribute = upgrade.keys()[0]
        base_unit_attributes = self.make(self.name).get_dict(attribute)
        self_attributes = self.get_dict(attribute)

        if attribute not in self_attributes:
            return False
        elif attribute not in base_unit_attributes and attribute in self_attributes:
            return True
        else:
            return base_unit_attributes[attribute] != self_attributes[attribute]

    def get_upgraded_unit(self, choice):

        if isinstance(choice, basestring):
            upgraded_unit = self.make(choice)

        else:
            upgraded_unit = self.make(self.name)

            for trait, info in self.traits.items():
                upgraded_unit.set(trait, *info)

            for ability, info in self.abilities.items():
                upgraded_unit.set(ability, *info)

            for attribute, info in choice.items():
                upgraded_unit.add_levels(attribute, info[1])

        for state, info in self.states.items():
            upgraded_unit.set(state, *info)

        upgraded_unit.set(State.recently_upgraded)

        return upgraded_unit

    def is_allowed_upgrade_choice(self, upgrade_choice):
        if not self.is_milf():
            return False

        return upgrade_choice in [self.get_upgrade_choice(0), self.get_upgrade_choice(1)]

    def get_abilities_not_in_base(self):
        base_unit = self.make(self.name)
        return dict((ability, info) for ability, info in self.abilities.items() if info[1] != base_unit.get_level(ability))

    def get_traits_not_in_base(self):
        base_unit = self.make(self.name)
        return dict((trait, info) for trait, info in self.traits.items() if info[1] != base_unit.get_level(trait))

    def get_unit_level(self):
        experience = self.get(State.experience)
        to_upgrade = self.experience_to_upgrade
        return experience // to_upgrade

    def is_milf(self):
        experience = self.get(State.experience)
        to_upgrade = self.experience_to_upgrade
        return experience and experience % to_upgrade == 0 and not self.get(State.recently_upgraded)

    def to_document(self):
        attributes = merge(self.states, self.effects, self.get_traits_not_in_base(), self.get_abilities_not_in_base())

        if attributes:
            unit_dict = readable(attributes)
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
    zoc = [Type.Cavalry]
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
    special_upgrades = [{Trait.cavalry_specialist: 1}, {Trait.lancing: 1, Trait.movement_skill: 1}]
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
    experience_to_upgrade = 2
    special_upgrades = [{Trait.tall_shield: 1}, {Trait.attack_skill: 2}]
    final_upgrades = [{Trait.movement_skill: 2}, {Trait.defence_skill: 1}]


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
    special_upgrades = [{Trait.siege_weapon_specialist: 1}]
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
    special_upgrades = [{Trait.attack_cooldown: 1, Trait.far_sighted: 1}]
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
    special_upgrades = [{Trait.flag_bearing: 1}]
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
    special_upgrades = [{Ability.bribe: 1}]
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
    special_upgrades = [{Ability.improve_weapons: 1}]
    final_upgrades = [{Trait.range_skill: 1}, {Trait.defence_skill: 1}]
