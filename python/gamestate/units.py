from gamestate.gamestate_library import *
from game.game_library import *
from gamestate.enums import *
from game.settings import beginner_mode


class UnitClass():
    def __init__(self):
        self.attributes = {}

    unit = None
    type = None
    experience_to_upgrade = 0
    base_attack = 0
    base_defence = 0
    base_range = 0
    base_movement = 0
    upgrades = {}


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
    def states(self):
        return [attribute for attribute in self.attributes if attribute in State]

    @property
    def effects(self):
        return [attribute for attribute in self.attributes if attribute in Effect]

    @property
    def abilities(self):
        return [attribute for attribute in self.attributes if attribute in Ability]

    def set(self, attribute, value=1, duration=None, level=1):
        """
        :param attribute: A state or effect.
        :param value: A value for states. Default 1.
        :param duration: A duration for effects.
        :param level: A level for effects. Default 1.
        """
        if attribute in State:
            self.attributes[attribute] = AttributeValues(value=value)
        elif attribute in Effect:
            self.attributes[attribute] = AttributeValues(duration=duration, level=level)

    def decrease(self, attribute):
        """
        :param attribute: A state or effect.
        :return: If the attribute is a state, decrease the value by 1. If the attribute is an effect, decrease the
        duration by 1. If the value or duration is set to 0, remove the attribute.
        """
        if attribute in self.states:
            self.attributes[attribute].value -= 1
            if self.get(attribute) == 0:
                self.remove(attribute)

        if attribute in self.effects:
            self.attributes[attribute].duration -= 1
            if self.attributes[attribute].duration == 0:
                self.remove(attribute)

    def has(self, attribute, number=None):
        """
        :param attribute: An attribute
        :param number: A level or value depending on the attribute type
        :return: If a number is not given, returns whether the unit has the attribute.
                 If a number is given, returns whether the unit has the attribute at that specific level / value.
        """
        if attribute not in self.attributes:
            return False
        elif number is None:
            return True
        if attribute in State:
            return self.attributes[attribute].value == number
        else:
            return self.attributes[attribute].level == number

    def get(self, attribute):
        """
        :param attribute: An attribute
        :return: If the attribute is a state, returns the state value. Otherwise returns the state level.
        """
        if attribute in State:
            return self.attributes[attribute].value if attribute in self.attributes else 0
        else:
            return self.attributes[attribute].level if attribute in self.attributes else 0

    def remove(self, attribute):
        if attribute in self.attributes:
            del self.attributes[attribute]

    def increase(self, attribute, n=1):
        """
        :param attribute: An attribute
        :return: If the attribute is a state, increase the value by n. Otherwise increase the level by n.
        """
        if attribute in State:
            if self.has(attribute):
                self.attributes[attribute].value += n
            else:
                self.attributes[attribute] = AttributeValues(value=n)
        else:
            if self.has(attribute):
                self.attributes[attribute].level += n
            else:
                self.attributes[attribute] = AttributeValues(level=n)

    def gain_experience(self):
        if not self.has(State.used) and not beginner_mode:
            self.increase(State.experience)

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
        :return: A new UnitClass object, based on the unit and with the upgrade.
        """
        if upgrade in Unit:
            upgraded_unit = base_units[upgrade]()
            for attribute in self.states + self.effects:
                upgraded_unit.attributes[attribute] = self.attributes[attribute]
            upgraded_unit.remove(State.experience)
        else:
            upgraded_unit = base_units[self.unit]()
            upgraded_unit.attributes = dict(self.attributes)
            upgraded_unit.increase(State.rank, 1)
            upgraded_unit.remove(State.experience)
            for attribute, attribute_values in upgrade.items():
                upgraded_unit.increase(attribute, attribute_values.level)

        return upgraded_unit

    def get_upgraded_unit_from_choice(self, choice):
        """
        :param choice: upgrade choice 0 or 1.
        :return: A new UnitClass object, based on the unit and with the upgrade.
        """
        upgrade = self.get_upgrade_choices()[choice]
        return self.get_upgraded_unit_from_upgrade(upgrade)

    def get_upgrade_choices(self):
        """
        :param choice: upgrade choice 0 or 1.
        :return: The chosen unit upgrade in enum upgrade format. (Dictionary with enums as keys and AttributeValues as
        values.)
        """
        if version == 1.0:
            return [{Trait.attack_skill: AttributeValues(level=1)}, {Trait.defence_skill: AttributeValues(level=1)}]

        def has_upgrade(check_upgrade):
            if check_upgrade in Unit:
                return False
            for attribute, attribute_values in check_upgrade.items():
                level = attribute_values.level
                return self.has(attribute, level) and not base_units[self.unit]().has(attribute, level)

        possible_upgrade_choices = []
        for upgrade_category in ["once_1", "once_2", "unit_1", "unit_2", "repeat_1", "repeat_2"]:
            if upgrade_category in self.upgrades:
                upgrade = get_enum_attributes(self.upgrades[upgrade_category])
                if not (upgrade_category in ["once_1", "once_2"] and has_upgrade(upgrade)):
                    possible_upgrade_choices.append(upgrade)

        return possible_upgrade_choices

    def should_be_upgraded(self):
        return self.has(State.experience) and self.get(State.experience) % self.experience_to_upgrade == 0

    def to_document(self):
        write_attributes = {attribute: attribute_values for attribute, attribute_values in self.attributes.items() if
                            not base_units[self.unit]().has(attribute)}

        if write_attributes:
            unit_dict = get_string_attributes(write_attributes)
            unit_dict["name"] = self.name
            return unit_dict
        else:
            return self.name

attributes_units = {}


def make_unit_subclasses_from_document(document):
    """
    :param document: A document containing the specifications for units.
    :return: A dictionary of unit objects.
    """
    unit_class_dictionary = {}
    for name, unit_class_content in document.items():

        unit_class_content["unit"] = Unit[name]
        for key, value in unit_class_content.items():
            if key in ["attack", "defence", "movement", "range"]:
                unit_class_content["base_" + key] = value
                del unit_class_content[key]
        attributes_units[name] = {get_enum_attributes(key): value for key, value in unit_class_content["attributes"].items()}

        def init(self):
            super(type(self), self).__init__()
            for attribute, level in attributes_units[self.name].items():
                self.attributes[attribute] = AttributeValues(level=level)

        del unit_class_content["attributes"]
        unit_class_content["__init__"] = init
        unit_class_content["type"] = Type[unit_class_content["type"]]
        unit_class = type(name, (UnitClass,), unit_class_content)

        unit_class_dictionary[Unit[name]] = unit_class

    return unit_class_dictionary


unit_document = read_json("./../Version_1.1/Units.json")


base_units = make_unit_subclasses_from_document(unit_document)
