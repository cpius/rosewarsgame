from __future__ import division
from operator import attrgetter
import ai_methods as m
import random as rnd
import settings


def get_action(actions, g):

    for action in actions:
        if action.is_attack:
            enemy_unit = g.units[1][action.attackpos]
            unit = g.units[0][action.startpos]
            chance = m.chance_of_win(unit, enemy_unit, action)
            action.score = chance * 10
            if hasattr(action.unit, "double_attack_cost"):
                action.score /= 2
        else:
            action.score = 0

    rnd.shuffle(actions)
    actions.sort(key=attrgetter("score"), reverse=True)
    if settings.document_ai_actions:
        m.document_actions(actions, g)
    return actions[0]


def put_counter(unit):
    unit.attack_counters += 1

