import itertools
from operator import attrgetter
import ai_methods as m
import random as rnd
import settings


def get_action(actions, g):
    
    for action in actions:
        action.score = action.end_position[1]
        
        if action.end_position[1] > action.start_position[1]:
            action.score += 1
        
        if action.is_attack():
            action.score += 0.25
            if action.attack_position[1] > action.end_position[1] and action.is_move_with_attack():
                action.score += 0.5
    
    rnd.shuffle(actions)
    actions.sort(key=attrgetter("score"), reverse=True)
    
    if settings.document_ai_actions:
        m.document_actions(actions, g)
    return actions[0]
    

def put_counter(g):
    def decide_counter(unit):
        unit.defence_counters += 1

    for unit in g.units[0].values():
        if unit.xp == 2:
            if unit.defence + unit.defence_counters == 4:
                unit.attack_counters += 1
            else:
                if not unit.attack:
                    unit.defence_counters += 1
                else:
                    decide_counter(unit)
            unit.xp = 0
