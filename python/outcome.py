from common import *


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
    def from_document(cls, document):
        outcomes = dict()
        for outcome in document:
            outcomes[Position.from_string(outcome)] = document[outcome]

        return cls(outcomes)
