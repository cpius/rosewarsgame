from __future__ import division
from common import *
from collections import namedtuple

Effect_tuple = namedtuple('Effect_tuple', ['level', 'duration'])


class Unit(object):
    def __init__(self):
        self.traits = {}
        self.states = {}
        self.abilities = {}
        self.effects = {}

    name = ""
    zoc = []
    abilities = []
    experience_to_upgrade = 4
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

    def __eq__(self, other):
        return self.to_document() == other.to_document()

    def __ne__(self, other):
        return not self.__eq__(other)

    def get_dict(self, attribute):
        if attribute in Trait.name:
            return self.traits
        elif attribute in Ability.name:
            return self.abilities
        elif attribute in Effect.name:
            return self.effects
        elif attribute in State.name:
            return self.states

    def set(self, attribute, value=1, duration=None):
        if attribute in Effect.name:
            self.set_effect(attribute, value, duration)
        else:
            self.get_dict(attribute)[attribute] = value

    def upgrade_attribute(self, attribute, amount):
        dictionary = self.get_dict(attribute)
        if attribute in dictionary:
            dictionary[attribute] += amount
        else:
            dictionary[attribute] = amount

    def increment_trait(self, trait):
        if trait in self.traits:
            self.traits[trait] += 1
        else:
            self.traits[trait] = 1

    def has(self, attribute, value=None, level=None):
        if attribute in Effect.name:
            return self.has_effect(attribute, level)

        if value:
            return self.get(attribute) == value
        else:
            return self.get(attribute)

    def has_effect(self, effect, level=None):
        if not effect in self.effects:
            return False

        if not level:
            return True

        return self.effects[effect].level == level

    def get(self, attribute):
        if attribute in Effect.name:
            return self.get_effect_level(attribute)
        else:
            dictionary = self.get_dict(attribute)
            if attribute in dictionary:
                return self.get_dict(attribute)[attribute]
            else:
                return 0

    def remove_state(self, state):
        if state in self.states:
            del self.states[state]

    def decrement(self, attribute):
        dictionary = self.get_dict(attribute)
        if attribute in dictionary:
            dictionary[attribute][0] = max(0, dictionary[attribute][0] - 1)
            if dictionary[attribute][0] == 0:
                del dictionary[attribute]

    def increment_state(self, state):
        if state in self.states:
            self.states[state] += 1
        else:
            self.states[state] = 1

    def do(self, ability, level):
        if ability == Ability.poison:
            self.set(Effect.poisoned, duration=level)

        if ability == Ability.sabotage:
            self.set_effect(Effect.sabotaged, duration=level)

        if ability == Ability.improve_weapons:
            if level == 2:
                self.set_effect(Effect.improved_weapons, 2, 2)
            else:
                self.set_effect(Effect.improved_weapons)

    def set_effect(self, effect, level=1, duration=1):
        self.effects[effect] = Effect_tuple(level, duration)

    def get_effect_level(self, effect):
        if not effect in self.effects:
            return 0
        else:
            return self.effects[effect].level

    def gain_experience(self):
        if not self.has(State.used) and not get_setting("Beginner_mode"):
            self.increment_state(State.experience)
            self.remove_state(State.recently_upgraded)

    def reduce_effect(self, effect):
        if self.effects[effect].duration <= 1:
            del self.effects[effect]
        else:
            self.effects[effect] = Effect_tuple(self.effects[effect].level, self.effects[effect].duration - 1)

    def has_extra_life(self):
        return self.has(Trait.extra_life) and not self.has(State.lost_extra_life)

    def has_javelin(self):
        return self.has(Trait.javelin) and not self.has(State.javelin_thrown)

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

        return upgrades[choice_index]

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

        if get_setting("version") == "1.0":
            if int(choice.keys()[0]) == Trait.attack_skill:
                self.increment_trait(Trait.attack_skill)
            elif int(choice.keys()[0]) == Trait.defence_skill:
                self.increment_trait(Trait.defence_skill)
            self.set(State.recently_upgraded)
            return self

        if isinstance(choice, basestring):
            self.remove_state(State.experience)
            upgraded_unit = self.make(choice)

        else:
            upgraded_unit = self.make(self.name)
            for trait, level in self.traits.items():
                upgraded_unit.set(trait, level)

            for ability, level in self.abilities.items():
                upgraded_unit.set(ability, level)

            for attribute, amount in choice.items():
                upgraded_unit.upgrade_attribute(attribute, amount)

        for state, level in self.states.items():
            upgraded_unit.set(state, level)

        for effect, info in self.effects.items():
            upgraded_unit.set(effect, info[0], info[1])

        upgraded_unit.set(State.recently_upgraded)

        return upgraded_unit

    def is_allowed_upgrade_choice(self, upgrade_choice):
        if not self.should_be_upgraded():
            return False

        if get_setting("version") == "1.0":
            return True

        return upgrade_choice in [self.get_upgrade_choice(0), self.get_upgrade_choice(1)]

    def get_abilities_not_in_base(self):
        return dict((ability, level) for ability, level in self.abilities.items() if
                    level != base_units[self.name].get(ability))

    def get_traits_not_in_base(self):
        return dict((trait, level) for trait, level in self.traits.items() if
                    level != base_units[self.name].get(trait))

    def get_unit_level(self):
        experience = self.get(State.experience)
        to_upgrade = self.experience_to_upgrade
        return experience // to_upgrade

    def should_be_upgraded(self):
        experience = self.get(State.experience)
        to_upgrade = self.experience_to_upgrade
        return experience and experience % to_upgrade == 0 and not self.has(State.recently_upgraded)

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
    experience_to_upgrade = 4


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
    experience_to_upgrade = 4


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
    experience_to_upgrade = 4


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
    experience_to_upgrade = 4


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
    upgrades = ["Flanking_Cavalry", "Hussar"]
    experience_to_upgrade = 3


class Flanking_Cavalry(Unit):
    def __init__(self):
        super(Flanking_Cavalry, self).__init__()
        self.set(Trait.flanking, 2)

    name = "Flanking Cavalry"
    image = "Light Cavalry"
    base_attack = 2
    base_defence = 2
    base_movement = 4
    base_range = 1
    attack_bonuses = {}
    defence_bonuses = {}
    zoc = []
    type = Type.Cavalry
    final_upgrades = [{Trait.flanking: 1}, {Trait.movement_skill: 1}]
    experience_to_upgrade = 4


class Hussar(Unit):
    def __init__(self):
        super(Hussar, self).__init__()
        self.set(Trait.ride_through, 1)

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
    experience_to_upgrade = 4


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
    experience_to_upgrade = 4


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
    experience_to_upgrade = 4


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
    experience_to_upgrade = 4


class Ballista(Unit):
 
    name = "Ballista"
    image = "Ballista"
    base_attack = 4
    base_defence = 1
    base_movement = 1
    base_range = 3
    attack_bonuses = {}
    defence_bonuses = {}
    type = Type.War_Machine
    special_upgrades = [{Trait.fire_arrows: 1}]
    final_upgrades = [{Trait.attack_skill: 1}, {Trait.range_skill: 1}]
    experience_to_upgrade = 4


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
    type = Type.War_Machine
    final_upgrades = [{Trait.attack_skill: 1}, {Trait.range_skill: 1, Trait.attack_skill: -1}]
    experience_to_upgrade = 3


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
    zoc = [Type.Cavalry, Type.Infantry, Type.War_Machine, Type.Specialist]
    special_upgrades = [{Trait.melee_expert: 1}, {Trait.tall_shield: 1, Trait.melee_freeze: 1}]
    final_upgrades = [{Trait.attack_skill: 1}, {Trait.defence_skill: 1}]
    experience_to_upgrade = 3


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
    special_upgrades = [{Trait.tall_shield: 1}, {Trait.attack_skill: 2}]
    final_upgrades = [{Trait.movement_skill: 1}, {Trait.defence_skill: 1}]
    experience_to_upgrade = 2


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
    defence_bonuses = {Type.War_Machine: 1}
    zoc = []
    type = Type.Infantry
    special_upgrades = [{Trait.war_machine_specialist: 1}]
    final_upgrades = [{Trait.attack_skill: 1}, {Trait.defence_skill: 1}]
    experience_to_upgrade = 4

    traits = {Trait.rage: 1, Trait.extra_life: 1}


class Javeliner(Unit):
    def __init__(self):
        super(Javeliner, self).__init__()
        self.set(Trait.javelin, 1)

    name = "Javeliner"
    image = "Javeliner"
    base_attack = 4
    base_defence = 3
    base_movement = 1
    base_range = 1
    attack_bonuses = {}
    defence_bonuses = {}
    zoc = []
    type = Type.Infantry
    final_upgrades = [{Trait.attack_skill: 1}, {Trait.defence_skill: 1}]
    experience_to_upgrade = 4

    traits = {Trait.javelin: 1}



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
    type = Type.War_Machine
    special_upgrades = [{Trait.attack_cooldown: 1, Trait.far_sighted: 1}]
    final_upgrades = [{Trait.attack_skill: 1}, {Trait.range_skill: 1}]
    experience_to_upgrade = 3


class Trebuchet(Unit):
    def __init__(self):
        super(Trebuchet, self).__init__()
        self.set(Trait.spread_attack, 1)

    name = "Trebuchet"
    image = "Trebuchet"
    base_attack = 3
    base_defence = 1
    base_movement = 1
    base_range = 3
    attack_bonuses = {}
    defence_bonuses = {}
    zoc = []
    type = Type.War_Machine
    final_upgrades = [{Trait.attack_skill: 1}, {Trait.range_skill: 1}]
    experience_to_upgrade = 4


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
    experience_to_upgrade = 3


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
    experience_to_upgrade = 4


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
    special_upgrades = [{Trait.crusading: 1}]
    final_upgrades = [{Trait.attack_skill: 1}, {Trait.defence_skill: 1}]
    experience_to_upgrade = 4


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
    experience_to_upgrade = 4


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
    experience_to_upgrade = 4

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
    special_upgrades = [{Ability.sabotage: 1}, {Ability.poison: 1}]
    final_upgrades = [{Trait.range_skill: 1}, {Trait.defence_skill: 1}]
    experience_to_upgrade = 4


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
    experience_to_upgrade = 4


class Assassin(Unit):
    def __init__(self):
        super(Assassin, self).__init__()
        self.set(Ability.assassinate)
    name = "Assassin"
    image = "Assassin"
    base_attack = 0
    base_defence = 2
    base_movement = 1
    base_range = 11
    attack_bonuses = {}
    defence_bonuses = {}
    type = Type.Specialist
    special_upgrades = [{Ability.assassinate: 1}]
    final_upgrades = [{Trait.range_skill: 1}, {Trait.defence_skill: 1}]
    experience_to_upgrade = 4


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
    experience_to_upgrade = 4


base_units = {name: Unit.make(name) for name in all_units}
