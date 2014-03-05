from __future__ import division
from common import *
from collections import namedtuple

Effect_tuple = namedtuple('Effect_tuple', ['level', 'duration'])


class Unit_class(object):
    def __init__(self):
        self.traits = {}
        self.states = {}
        self.abilities = {}
        self.effects = {}

    unit = 0
    zoc = []
    abilities = []
    experience_to_upgrade = 0
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
        return Unit.name[self.unit]

    def __eq__(self, other):
        return self.to_document() == other.to_document()

    def __ne__(self, other):
        return not self.__eq__(other)

    @property
    def name(self):
        return Unit.name[self.unit]

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


class Archer(Unit_class):

    unit = Unit.Archer
    type = Type.Infantry
    base_attack = 2
    base_defence = 2
    base_movement = 1
    base_range = 4
    attack_bonuses = {Type.Infantry: 1}
    upgrades = [{Trait.sharpshooting: 1}, {Trait.fire_arrows: 1}, {Trait.range_skill: 1}, {Trait.attack_skill: 1}]
    experience_to_upgrade = 4


class Pikeman(Unit_class):
    def __init__(self):
        super(Pikeman, self).__init__()
        self.set(Trait.cavalry_specialist, 1)
    unit = Unit.Pikeman
    type = Type.Infantry
    base_attack = 2
    base_defence = 2
    base_movement = 1
    base_range = 1
    zoc = [Type.Cavalry]
    upgrades = [Unit.Halberdier, Unit.Royal_Guard]
    experience_to_upgrade = 3


class Halberdier(Unit_class):
    def __init__(self):
        super(Halberdier, self).__init__()
        self.set(Trait.push, 1)
        self.set(Trait.cavalry_specialist, 1)
    unit = Unit.Halberdier
    type = Type.Infantry
    base_attack = 3
    base_defence = 2
    base_movement = 1
    base_range = 1
    zoc = [Type.Cavalry]
    upgrades = [{Trait.attack_skill: 1}, {Trait.defence_skill: 1}]
    experience_to_upgrade = 4


class Light_Cavalry(Unit_class):

    unit = Unit.Light_Cavalry
    type = Type.Cavalry
    base_attack = 2
    base_defence = 2
    base_movement = 4
    base_range = 1
    upgrades = [Unit.Flanking_Cavalry, Unit.Hussar]
    experience_to_upgrade = 3


class Flanking_Cavalry(Unit_class):
    def __init__(self):
        super(Flanking_Cavalry, self).__init__()
        self.set(Trait.flanking, 1)

    unit = Unit.Flanking_Cavalry
    type = Type.Cavalry
    base_attack = 2
    base_defence = 2
    base_movement = 4
    base_range = 1
    upgrades = [{Trait.flanking: 1}, {Trait.movement_skill: 1}, {Trait.attack_skill: 2}]
    experience_to_upgrade = 4


class Hussar(Unit_class):
    def __init__(self):
        super(Hussar, self).__init__()
        self.set(Trait.ride_through, 1)

    unit = Unit.Hussar
    type = Type.Cavalry
    base_attack = 2
    base_defence = 2
    base_movement = 4
    base_range = 1
    upgrades = [{Trait.attack_skill: 1}, {Trait.movement_skill: 1}]
    experience_to_upgrade = 4


class Knight(Unit_class):

    unit = Unit.Knight
    type = Type.Cavalry
    base_attack = 3
    base_defence = 3
    base_movement = 2
    base_range = 1
    upgrades = [Unit.Lancer, Unit.Hobelar]
    experience_to_upgrade = 4


class Lancer(Unit_class):
    def __init__(self):
        super(Lancer, self).__init__()
        self.set(Trait.lancing, 1)

    unit = Unit.Lancer
    type = Type.Cavalry
    base_attack = 2
    base_defence = 3
    base_movement = 3
    base_range = 1
    attack_bonuses = {Type.Cavalry: 1}
    upgrades = [{Trait.cavalry_specialist: 1}, {Trait.lancing: 1, Trait.movement_skill: 1}, {Trait.attack_skill: 1},
                {Trait.defence_skill: 1}]
    experience_to_upgrade = 4


class Hobelar(Unit_class):
    def __init__(self):
        super(Hobelar, self).__init__()
        self.set(Trait.swiftness, 1)

    unit = Unit.Hobelar
    type = Type.Cavalry
    base_attack = 3
    base_defence = 3
    base_movement = 3
    base_range = 1
    upgrades = [{Trait.attack_skill: 1}, {Trait.defence_skill: 1}]
    experience_to_upgrade = 4


class Ballista(Unit_class):
 
    unit = Unit.Ballista
    type = Type.War_Machine
    base_attack = 4
    base_defence = 1
    base_movement = 1
    base_range = 3
    upgrades = [{Trait.fire_arrows: 1}, {Trait.attack_skill: 1}, {Trait.range_skill: 1}]
    experience_to_upgrade = 4


class Catapult(Unit_class):
    def __init__(self):
        super(Catapult, self).__init__()
        self.set(Trait.double_attack_cost, 1)

    unit = Unit.Catapult
    type = Type.War_Machine
    base_attack = 6
    base_defence = 2
    base_movement = 1
    base_range = 3
    upgrades = [{Trait.attack_skill: 1}, {Trait.range_skill: 1, Trait.attack_skill: -1}]
    experience_to_upgrade = 3


class Royal_Guard(Unit_class):
    def __init__(self):
        super(Royal_Guard, self).__init__()
        self.set(Trait.defence_maneuverability, 1)
  
    unit = Unit.Royal_Guard
    type = Type.Infantry
    base_attack = 3
    base_defence = 3
    base_movement = 1
    base_range = 1
    zoc = [Type.Cavalry, Type.Infantry, Type.War_Machine, Type.Specialist]
    upgrades = [{Trait.melee_expert: 1}, {Trait.tall_shield: 1, Trait.melee_freeze: 1}, {Trait.attack_skill: 1},
                {Trait.defence_skill: 1}]
    experience_to_upgrade = 3


class Scout(Unit_class):
    def __init__(self):
        super(Scout, self).__init__()
        self.set(Trait.scouting, 1)
    
    unit = Unit.Scout
    type = Type.Cavalry
    base_attack = 0
    base_defence = 2
    base_movement = 4
    base_range = 1
    upgrades = [{Trait.tall_shield: 1}, {Trait.attack_skill: 2}, {Trait.movement_skill: 1}, {Trait.defence_skill: 1}]
    experience_to_upgrade = 1


class Viking(Unit_class):
    def __init__(self):
        super(Viking, self).__init__()
        self.set(Trait.rage, 1)
        self.set(Trait.extra_life, 1)

    unit = Unit.Viking
    type = Type.Infantry
    base_attack = 3
    base_defence = 2
    base_movement = 1
    base_range = 1
    defence_bonuses = {Type.War_Machine: 1}
    upgrades = [{Trait.war_machine_specialist: 1}, {Trait.attack_skill: 1}, {Trait.defence_skill: 1}]
    experience_to_upgrade = 4


class Javeliner(Unit_class):
    def __init__(self):
        super(Javeliner, self).__init__()
        self.set(Trait.javelin, 1)

    unit = Unit.Javeliner
    type = Type.Infantry
    base_attack = 4
    base_defence = 3
    base_movement = 1
    base_range = 1
    upgrades = [{Trait.attack_skill: 1}, {Trait.defence_skill: 1}]
    experience_to_upgrade = 4


class Cannon(Unit_class):
    def __init__(self):
        super(Cannon, self).__init__()
        self.set(Trait.attack_cooldown, 1)
    
    unit = Unit.Cannon
    base_attack = 5
    base_defence = 1
    base_movement = 1
    base_range = 4
    type = Type.War_Machine
    upgrades = [{Trait.attack_cooldown: 1, Trait.far_sighted: 1}, {Trait.attack_skill: 1}, {Trait.range_skill: 1}]
    experience_to_upgrade = 3


class Trebuchet(Unit_class):
    def __init__(self):
        super(Trebuchet, self).__init__()
        self.set(Trait.spread_attack, 1)

    unit = Unit.Trebuchet
    type = Type.War_Machine
    base_attack = 3
    base_defence = 1
    base_movement = 1
    base_range = 3
    upgrades = [{Trait.attack_skill: 1}, {Trait.range_skill: 1}]
    experience_to_upgrade = 4


class Flag_Bearer(Unit_class):
    def __init__(self):
        super(Flag_Bearer, self).__init__()
        self.set(Trait.flag_bearing, 1)
   
    unit = Unit.Flag_Bearer
    type = Type.Cavalry
    base_attack = 2
    base_defence = 3
    base_movement = 3
    base_range = 1
    upgrades = [{Trait.flag_bearing: 1}, {Trait.attack_skill: 1}, {Trait.defence_skill: 1}]
    experience_to_upgrade = 3


class Longswordsman(Unit_class):
    def __init__(self):
        super(Longswordsman, self).__init__()
        self.set(Trait.longsword, 1)

    unit = Unit.Longswordsman
    type = Type.Infantry
    base_attack = 3
    base_defence = 3
    base_movement = 1
    base_range = 1
    upgrades = [{Trait.rage: 1}, {Trait.attack_skill: 1}, {Trait.defence_skill: 1}]
    experience_to_upgrade = 4


class Crusader(Unit_class):
    def __init__(self):
        super(Crusader, self).__init__()
        self.set(Trait.crusading, 1)

    unit = Unit.Crusader
    type = Type.Cavalry
    base_attack = 3
    base_defence = 3
    base_movement = 3
    base_range = 1
    upgrades = [{Trait.crusading: 1}, {Trait.attack_skill: 1}, {Trait.defence_skill: 1}]
    experience_to_upgrade = 4


class Berserker(Unit_class):
    def __init__(self):
        super(Berserker, self).__init__()
        self.set(Trait.berserking, 1)

    unit = Unit.Berserker
    type = Type.Infantry
    base_attack = 5
    base_defence = 1
    base_movement = 1
    base_range = 1
    upgrades = [{Trait.big_shield: 1}, {Trait.attack_skill: 2}, {Trait.attack_skill: 1}, {Trait.defence_skill: 1}]
    experience_to_upgrade = 4


class War_Elephant(Unit_class):
    def __init__(self):
        super(War_Elephant, self).__init__()
        self.set(Trait.double_attack_cost, 1)
        self.set(Trait.triple_attack, 1)
        self.set(Trait.push, 1)

    unit = Unit.War_Elephant
    type = Type.Cavalry
    base_attack = 3
    base_defence = 3
    base_movement = 2
    base_range = 1
    upgrades = [{Trait.defence_skill: 1}, {Trait.attack_skill: 1}]
    experience_to_upgrade = 3


class Fencer(Unit_class):
    def __init__(self):
        super(Fencer, self).__init__()
        self.set(Trait.combat_agility, 1)

    unit = Unit.Fencer
    type = Type.Infantry
    base_attack = 3
    base_defence = 3
    base_movement = 1
    base_range = 1
    attack_bonuses = {Type.Infantry: 1}
    upgrades = [{Trait.attack_skill: 1}, {Trait.defence_skill: 1}]
    experience_to_upgrade = 4


class Saboteur(Unit_class):
    def __init__(self):
        super(Saboteur, self).__init__()
        self.set(Ability.sabotage, 1)
        self.set(Ability.poison, 1)
    unit = Unit.Saboteur
    type = Type.Specialist
    base_attack = 0
    base_defence = 2
    base_movement = 1
    base_range = 3
    upgrades = [{Ability.sabotage: 1}, {Ability.poison: 1}, {Trait.range_skill: 1}, {Trait.defence_skill: 1}]
    experience_to_upgrade = 4


class Diplomat(Unit_class):
    def __init__(self):
        super(Diplomat, self).__init__()
        self.set(Ability.bribe)
    unit = Unit.Diplomat
    type = Type.Specialist
    base_attack = 0
    base_defence = 2
    base_movement = 1
    base_range = 3
    upgrades = [{Ability.bribe: 1}, {Trait.range_skill: 1}, {Trait.defence_skill: 1}]
    experience_to_upgrade = 4


class Assassin(Unit_class):
    def __init__(self):
        super(Assassin, self).__init__()
        self.set(Ability.assassinate)
    unit = Unit.Assassin
    type = Type.Specialist
    base_attack = 0
    base_defence = 2
    base_movement = 1
    base_range = 11
    upgrades = [{Trait.defence_skill: 1}, {Trait.defence_skill: 1}]
    experience_to_upgrade = 4


class Weaponsmith(Unit_class):
    def __init__(self):
        super(Weaponsmith, self).__init__()
        self.set(Ability.improve_weapons, 1)

    unit = Unit.Weaponsmith
    type = Type.Specialist
    base_attack = 0
    base_defence = 2
    base_movement = 1
    base_range = 4
    upgrades = [{Ability.improve_weapons: 1}, {Trait.range_skill: 1}, {Trait.defence_skill: 1}]
    experience_to_upgrade = 4


base_units = {name: Unit.make(name) for name in all_units}
