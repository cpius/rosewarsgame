from common import *
import random


class Outcome:
    def __init__(self, outcomes=None):
        if outcomes is None:
            self.outcomes = dict()
        else:
            self.outcomes = outcomes

    def set_suboutcome(self, position, sub_outcome):
        self.outcomes[position] = sub_outcome

    def for_position(self, position):
        if position in self.outcomes:
            return self.outcomes[position]

    def add_outcomes(self, other):
        self.outcomes.update(other.outcomes)

    def to_document(self):
        outcome_document = dict()
        for outcome in self.outcomes:
            outcome_document[Position.from_string(outcome)] = outcome
        return outcome_document

    @classmethod
    def determine_outcome(cls, action, gamestate):
        outcome = cls()
        if not action.is_attack():
            return outcome

        outcome.set_suboutcome(action.target_at, [random.randint(1, 6), random.randint(1, 6)])

        attack_direction = None
        if action.is_attack() and action.unit.is_melee():
            attack_direction = action.end_at.get_direction_to(action.target_at)

        if action.unit.has(Trait.triple_attack):
            for forward_position in action.end_at.two_forward_tiles(attack_direction):
                if forward_position in gamestate.enemy_units:
                    outcome.set_suboutcome(forward_position, [random.randint(1, 6), random.randint(1, 6)])

        if action.unit.has(Trait.longsword):
            for forward_position in action.end_at.four_forward_tiles(attack_direction):
                if forward_position in gamestate.enemy_units:
                    outcome.set_suboutcome(forward_position, [random.randint(1, 6), random.randint(1, 6)])

        return outcome


    @classmethod
    def from_document(cls, document):
        outcomes = dict()
        for outcome in document:
            outcomes[Position.from_string(outcome)] = document[outcome]

        return cls(outcomes)
