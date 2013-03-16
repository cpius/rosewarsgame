import battle


class Action(object):
    def __init__(self,
                 start_position,
                 end_position,
                 attack_position,
                 is_attack,
                 move_with_attack,
                 is_ability=False,
                 ability=""):
        self.start_position = start_position  # The tile the unit starts it's action on
        self.end_position = end_position  # If the action is a movement, the tile the unit ends it movement on.
                                          # If the action is an attack, tile the unit stops at while attacking
                                          # an adjacent tile.
        self.attack_position = attack_position  # The tile a unit attacks
        self.is_attack = is_attack
        self.move_with_attack = move_with_attack
        self.is_ability = is_ability
        self.ability = ability
        self.sub_actions = []
        self.final_position = end_position  # The tile a unit ends up at after attacks are resolved

        self.unit = None
        self.target = None
        self.unit_reference = None
        self.target_reference = None
        self.rolls = None
        self.outcome = None

    def attribute_representation(self):
        return str(self.__dict__)

    def get_basic_string(self):
        representation = self.unit_reference.name

        if self.start_position != self.end_position:
            representation += " move from " + coordinates(self.start_position)
            representation += " to " + coordinates(self.end_position)
            if self.is_attack:
                representation += " and"
        else:
            representation += " at " + coordinates(self.start_position)

        if self.is_attack and not self.move_with_attack:
            representation += " attack " + self.target_reference.name + " " + coordinates(self.attack_position)

        if self.is_attack and self.move_with_attack:
            representation += " attack-move " + self.target_reference.name + " " + coordinates(self.attack_position)

        if self.is_ability:
            representation += " use "\
                              + self.ability\
                              + " on "\
                              + self.target_reference.name\
                              + " "\
                              + coordinates(self.attack_position)

        return representation

    def get_battle_outcome_string(self):
        if self.outcome:
            return self.outcome
        else:
            return ""

    def get_full_battle_outcome_string(self):
        representation = ""
        if self.rolls:
            attack = battle.get_attack_rating(self.unit_reference, self.target_reference, self)
            defence = battle.get_defence_rating(self.unit_reference, self.target_reference, attack)

            representation += "Stats A: " + str(attack) + ", D: " + str(defence)
            representation += " Rolls A: " + str(self.rolls[0]) + " D: " + str(self.rolls[1])
            representation += ", " + self.outcome

        for sub_action in self.sub_actions:
            representation += "\n"
            representation += "and attack " + coordinates(sub_action.attack_position)
            if sub_action.rolls:
                attack = battle.get_attack_rating(self.unit_reference, self.target_reference, self)
                defence = battle.get_defence_rating(self.unit_reference, self.target_reference, attack)

                representation += ", Stats A: " + str(attack) + ", D: " + str(defence)
                representation += " Rolls A: " + str(self.rolls[0]) + " D: " + str(self.rolls[1])
                representation += ", " + self.outcome

        return representation

    def __repr__(self):
        return self.get_basic_string()

    def full_string(self):
        return self.get_basic_string() + ", " + self.get_battle_outcome_string() + "\n" \
               + self.get_full_battle_outcome_string()

    def string_with_outcome(self):
        return self.get_basic_string() + ", " + self.get_battle_outcome_string()

    def __eq__(self, other):
        basic_attributes = ["start_position",
                            "end_position",
                            "attack_position",
                            "is_attack",
                            "move_with_attack",
                            "is_ability",
                            "ability"]
        original = dict((attribute, self.__dict__[attribute]) for attribute in basic_attributes)
        other = dict((attribute, other.__dict__[attribute]) for attribute in basic_attributes)

        return original == other


def coordinates(position):
    columns = list(" ABCDE")
    return columns[position[0]] + str(position[1])