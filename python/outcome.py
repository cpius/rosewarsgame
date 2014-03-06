from common import *


class Outcome:
    def __init__(self, outcomes=None):
        if outcomes is None:
            self.outcomes = dict()
        else:
            self.outcomes = outcomes

    def __repr__(self):
        representation = ""
        for position in self.outcomes:
            representation += str(position) + ": " + str(self.outcomes[position])

        return representation

    def set_suboutcome(self, position, sub_outcome):
        self.outcomes[position] = sub_outcome

    def for_position(self, position):
        if position in self.outcomes:
            return self.outcomes[position]

    def add_outcomes(self, other):
        self.outcomes.update(other.outcomes)

    def to_document(self):
        outcome_document = dict()
        for position, outcome in self.outcomes.items():
            outcome_document[str(position)] = outcome
        return outcome_document

    @classmethod
    def determine_outcome(cls, action, gamestate):
        outcome = cls()
        if not action.has_outcome():
            return outcome

        outcome.set_suboutcome(action.target_at, get_rolls())

        attack_direction = None
        if action.is_attack() and action.unit.is_melee() and not action.is_javelin_throw():
            attack_direction = action.end_at.get_direction_to(action.target_at)

        if action.unit.has(Trait.triple_attack):
            for position in action.end_at.two_forward_tiles(attack_direction) & set(gamestate.enemy_units):
                outcome.set_suboutcome(position, rolls(random.randint(1, 6), random.randint(1, 6)))

        if action.unit.has(Trait.spread_attack):
            for position in action.target_at.adjacent_tiles() & set(gamestate.enemy_units):
                outcome.set_suboutcome(position, rolls(random.randint(1, 6), random.randint(1, 6)))

        if action.unit.has(Trait.longsword):
            for position in action.end_at.four_forward_tiles(attack_direction) & set(gamestate.enemy_units):
                outcome.set_suboutcome(position, rolls(random.randint(1, 6), random.randint(1, 6)))

        return outcome


    @classmethod
    def from_document(cls, document):
        outcomes = dict()
        for outcome in [outcome for outcome in document if outcome[0] in "ABCDE" and outcome[1] in "12345678"]:
            outcomes[Position.from_string(outcome)] = rolls(*document[outcome])

        return cls(outcomes)
