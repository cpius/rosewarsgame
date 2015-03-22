from common import *


class Unit_class():
    def __init__(self):
        self.attributes = {}

    unit = None
    zoc = []
    abilities = []
    experience_to_upgrade = 0
    attack_bonuses = {}
    defence_bonuses = {}
    attributes = {}
    base_attack = 0
    base_defence = 0
    base_range = 0
    base_movement = 0
    type = None
    level = 0
    upgrades = []

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
        return self.unit.name

    def __eq__(self, other):
        return self.to_document() == other.to_document()

    def __ne__(self, other):
        return not self.__eq__(other)

    @property
    def name(self):
        return self.unit.name

    @property
    def pretty_name(self):
        return prettify(self.unit.name)

    @property
    def effects(self):
        return [attribute for attribute in self.attributes if attribute in Effect]

    @property
    def abilities(self):
        return [attribute for attribute in self.attributes if attribute in Ability]

    def get_traits(self):
        return [attribute for attribute in self.attributes if attribute in Trait]

    def get_states(self):
        return [attribute for attribute in self.attributes if attribute in State]

    def set(self, attribute, value=None, duration=None, level=1):
        if attribute in State:
            if value is None:
                value = 1
            if value is not 0:
                self.attributes[attribute] = AttributeValues(value=value)
        else:
            self.attributes[attribute] = AttributeValues(value=value, duration=duration, level=level)

    def decrease_duration(self, attribute):
        if attribute in self.attributes:
            duration = self.attributes[attribute].duration - 1
            if duration == 0:
                del self.attributes[attribute]
            else:
                self.attributes[attribute].duration = duration

    def has(self, attribute, number=None):
        if attribute not in self.attributes:
            return False
        if number is None:
            return True
        if attribute in Trait or attribute in Effect or attribute in Ability:
            return self.attributes[attribute].level == number
        elif attribute in State:
            return self.attributes[attribute].value == number

    def get_duration(self, attribute):
        return self.attributes[attribute].duration

    def get_level(self, attribute):
        return self.attributes[attribute].level if attribute in self.attributes else 0

    def get_state(self, attribute):
        return self.attributes[attribute].value if attribute in self.attributes else 0

    def remove(self, attribute):
        if attribute in self.attributes:
            del self.attributes[attribute]

    def gain_experience(self):
        if not self.has(State.used) and not get_setting("Beginner_mode"):
            if State.experience in self.attributes:
                self.attributes[State.experience].value += 1
            else:
                self.attributes[State.experience] = AttributeValues(value=1)
            self.remove(State.recently_upgraded)

    @property
    def has_extra_life(self):
        return self.has(Trait.extra_life) and not self.has(State.lost_extra_life)

    @property
    def has_javelin(self):
        return self.has(Trait.javelin) and not self.has(State.javelin_thrown)

    @property
    def is_melee(self):
        return self.range == 1

    @property
    def is_ranged(self):
        return self.range > 1

    def get_upgraded_unit_from_upgrade(self, upgrade):
        """
        :param upgrade: A unit enum or a dictionary with enums as keys and AttributeValues as values.
        :return: An instance of a Unit_class object, based on the unit and with the upgrade.
        """
        if type(upgrade) is Unit:
            upgraded_unit = self.make(upgrade)
            for attribute in self.attributes:
                if attribute in State or attribute in Effect:
                    upgraded_unit.attributes[attribute] = self.attributes[attribute]
            upgraded_unit.set(State.recently_upgraded)
            upgraded_unit.remove(State.experience)
            return upgraded_unit
        else:
            upgraded_unit = Unit_class.make(self.unit)
            upgraded_unit.attributes = dict(self.attributes)
            for key, attributes in upgrade.items():
                if key in upgraded_unit.attributes:
                    level = attributes.level + upgraded_unit.attributes[key].level
                    if level == 0:
                        del upgraded_unit.attributes[key]
                    else:
                        upgraded_unit.attributes[key] = AttributeValues(level=attributes.level + upgraded_unit.attributes[key].level)
                else:
                    upgraded_unit.attributes[key] = attributes
            upgraded_unit.set(State.recently_upgraded, value=1)

            return upgraded_unit

    def get_upgraded_unit_from_choice(self, choice):
        """
        :param choice: upgrade choice 0 or 1.
        :return: An instance of a Unit_class object, based on the unit and with the upgrade.
        """
        upgrade = self.get_upgrade(choice)
        return self.get_upgraded_unit_from_upgrade(upgrade)

    def get_upgrade(self, choice):
        """
        :param choice: upgrade choice 0 or 1.
        :return: The chosen unit upgrade in enum upgrade format. (Dictionary with enums as keys and AttributeValues as
        values.)
        """
        if get_setting("version") == "1.0":
            if choice == 1:
                return {Trait.attack_skill: AttributeValues(level=1)}
            else:
                return {Trait.defence_skill: AttributeValues(level=1)}

        def has_upgrade(upgrade):
            if upgrade in Unit:
                return False
            for attribute, level in upgrade.items():
                return self.has(attribute, level) and not base_units[self.unit].has(attribute, level)

        possible_upgrade_choices = [get_enum_upgrade(upgrade) for upgrade in self.upgrades if not has_upgrade(upgrade)]
        return possible_upgrade_choices[choice]

    @property
    def unit_level(self):
        return self.get_state(State.experience) // self.experience_to_upgrade

    def should_be_upgraded(self):
        experience = self.get_state(State.experience)
        return experience and experience % self.experience_to_upgrade == 0 and not self.has(State.recently_upgraded)

    def to_document(self):
        write_attributes = [(attribute, attribute_values) for attribute, attribute_values in self.attributes.items() if
                            not base_units[self.unit].has(attribute)]

        if write_attributes:
            unit_dict = readable(write_attributes)
            unit_dict["name"] = self.name
            return unit_dict
        else:
            return self.name

    @classmethod
    def make(cls, unit):
        return globals()[unit.name]()


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
        self.set(Trait.cavalry_specialist, level=1)
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
        self.set(Trait.push, level=1)
        self.set(Trait.cavalry_specialist, level=1)
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
        self.set(Trait.flanking, level=1)

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
        self.set(Trait.ride_through, level=1)

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
        self.set(Trait.lancing, level=1)

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
        self.set(Trait.swiftness, level=1)

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
        self.set(Trait.double_attack_cost, level=1)

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
        self.set(Trait.defence_maneuverability, level=1)
  
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
        self.set(Trait.scouting, level=1)
    
    unit = Unit.Scout
    type = Type.Cavalry
    base_attack = 0
    base_defence = 2
    base_movement = 4
    base_range = 1
    upgrades = [{Trait.tall_shield: 1}, {Trait.attack_skill: 2}, {Trait.movement_skill: 1}, {Trait.defence_skill: 1}]
    experience_to_upgrade = 2


class Viking(Unit_class):
    def __init__(self):
        super(Viking, self).__init__()
        self.set(Trait.rage, level=1)
        self.set(Trait.extra_life, level=1)

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
        self.set(Trait.javelin, level=1)

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
        self.set(Trait.attack_cooldown, level=1)
    
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
        self.set(Trait.spread_attack, level=1)

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
        self.set(Trait.flag_bearing, level=1)
   
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
        self.set(Trait.longsword, level=1)

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
        self.set(Trait.crusading, level=1)

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
        self.set(Trait.berserking, level=1)

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
        self.set(Trait.double_attack_cost, level=1)
        self.set(Trait.triple_attack, level=1)
        self.set(Trait.push, level=1)

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
        self.set(Trait.combat_agility, level=1)

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
        self.set(Ability.sabotage, level=1)
        self.set(Ability.poison, level=1)
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
        self.set(Ability.bribe, level=1)
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
        self.set(Ability.assassinate, level=1)
    unit = Unit.Assassin
    type = Type.Specialist
    base_attack = 0
    base_defence = 2
    base_movement = 1
    base_range = 11
    upgrades = [{Ability.assassinate: 1}, {Trait.defence_skill: 1}, {Trait.defence_skill: 1}]
    experience_to_upgrade = 2


class Weaponsmith(Unit_class):
    def __init__(self):
        super(Weaponsmith, self).__init__()
        self.set(Ability.improve_weapons, level=1)

    unit = Unit.Weaponsmith
    type = Type.Specialist
    base_attack = 0
    base_defence = 2
    base_movement = 1
    base_range = 4
    upgrades = [{Ability.improve_weapons: 1}, {Trait.range_skill: 1}, {Trait.defence_skill: 1}]
    experience_to_upgrade = 4


base_units = {unit: Unit_class.make(unit) for unit in list(Unit)}
