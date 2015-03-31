from gamestate.gamestate_library import *
from game.game_library import *
from gamestate.enums import *
from game.settings import beginner_mode


class Unit_class():
    def __init__(self):
        self.attributes = {}

    unit = None
    type = None
    experience_to_upgrade = 0
    base_attack = 0
    base_defence = 0
    base_range = 0
    base_movement = 0
    level = 0
    upgrades = {}

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
    def states(self):
        return [attribute for attribute in self.attributes if attribute in State]

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
        """
        :param attribute: A Trait, Effect, Ability or State
        :param number: A level or value depending on the attribute type
        :return: If a number is not given, returns whether the unit has the attribute.
                 If a number is given, returns whether the unit has the attribute at that specific level / value.
        """
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
        if not self.has(State.used) and not beginner_mode:
            if State.experience in self.attributes:
                self.attributes[State.experience].value += 1
            else:
                self.attributes[State.experience] = AttributeValues(value=1)
            self.remove(State.recently_upgraded)

    def remove_states_with_value_zero(self):
        removestates = [state for state in self.states if self.get_state(state) == 0]
        for state in removestates:
            self.remove(state)

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
        if upgrade in Unit:
            upgraded_unit = base_units[upgrade]()
            for attribute in self.attributes:
                if attribute in State or attribute in Effect:
                    upgraded_unit.attributes[attribute] = self.attributes[attribute]
            upgraded_unit.set(State.recently_upgraded)
            upgraded_unit.remove(State.experience)
            return upgraded_unit
        else:
            upgraded_unit = base_units[self.unit]()
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
        if version == 1.0:
            if choice == 1:
                return {Trait.attack_skill: AttributeValues(level=1)}
            else:
                return {Trait.defence_skill: AttributeValues(level=1)}

        def has_upgrade(upgrade):
            if upgrade in Unit:
                return False
            for attribute, attribute_values in upgrade.items():
                level = attribute_values.level
                return self.has(attribute, level) and not base_units[self.unit]().has(attribute, level)


        def translate_to_enum_format(upgrade):
            if upgrade in Unit:
                return upgrade
            else:
                upgrade_enum_format = {}
                for attribute_enum, number in upgrade.items():
                    upgrade_enum_format[get_enum_attributes(attribute_enum)] = AttributeValues(level=number)
                return upgrade_enum_format

        possible_upgrade_choices = []
        if "unit_1" in self.upgrades:
            possible_upgrade_choices.append(Unit[self.upgrades["unit_1"]])
        if "unit_2" in self.upgrades:
            possible_upgrade_choices.append(Unit[self.upgrades["unit_2"]])
        if "once_1" in self.upgrades:
            upgrade = translate_to_enum_format(self.upgrades["once_1"])
            if not has_upgrade(upgrade):
                possible_upgrade_choices.append(upgrade)
        if "once_2" in self.upgrades:
            upgrade = translate_to_enum_format(self.upgrades["once_2"])
            if not has_upgrade(upgrade):
                possible_upgrade_choices.append(upgrade)
        if "repeat_1" in self.upgrades:
            possible_upgrade_choices.append(translate_to_enum_format(self.upgrades["repeat_1"]))
        if "repeat_2" in self.upgrades:
            possible_upgrade_choices.append(translate_to_enum_format(self.upgrades["repeat_2"]))

        return possible_upgrade_choices[choice]



    @property
    def unit_level(self):
        return self.get_state(State.experience) // self.experience_to_upgrade

    def should_be_upgraded(self):
        experience = self.get_state(State.experience)
        return experience and experience % self.experience_to_upgrade == 0 and not self.has(State.recently_upgraded)

    def to_document(self):
        write_attributes = {attribute: attribute_values for attribute, attribute_values in self.attributes.items() if
                            not base_units[self.unit]().has(attribute)}

        if write_attributes:
            unit_dict = get_string_attributes(write_attributes)
            unit_dict["name"] = self.name
            return unit_dict
        else:
            return self.name

    @classmethod
    def make(cls, unit):
        return globals()[unit.name]()


attributes_units = {}


def make_unit_subclasses_from_document(document):
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
                self.set(attribute, level=level)

        del unit_class_content["attributes"]
        unit_class_content["__init__"] = init
        unit_class_content["type"] = Type[unit_class_content["type"]]
        unit_class = type(name, (Unit_class,), unit_class_content)

        unit_class_dictionary[Unit[name]] = unit_class

    return unit_class_dictionary


unit_document = read_json("./../Version_1.1/Units.json")


base_units = make_unit_subclasses_from_document(unit_document)
