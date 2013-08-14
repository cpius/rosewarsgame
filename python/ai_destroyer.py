from __future__ import division
from operator import attrgetter
import ai_methods as m
import random as rnd
import interface_settings as settings


def get_action(actions, gamestate):

    for action in actions:
        if action.is_attack():
            enemy_unit = gamestate.enemy_units()[action.target_at]
            unit = gamestate.player_units()[action.start_at]
            chance = m.chance_of_win(unit, enemy_unit, action)
            action.score = chance * 10
            if hasattr(action.unit, "double_attack_cost"):
                action.score /= 2
        else:
            action.score = 0

    rnd.shuffle(actions)
    actions.sort(key=attrgetter("score"), reverse=True)
    if settings.document_ai_actions:
        m.document_actions(actions, gamestate)
    return actions[0]


def put_counter(g):
    def decide_counter(unit):
        unit.attack_counters += 1

    for unit in g.player_units().values():
        if unit.xp == 2:
            if unit.defence + unit.defence_counters == 4:
                unit.attack_counters += 1
            else:
                if not unit.attack:
                    unit.defence_counters += 1
                else:
                    decide_counter(unit)
            unit.xp = 0

