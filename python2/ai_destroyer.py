from __future__ import division
import itertools
from operator import attrgetter
import ai_methods as m
import random as rnd
import settings



def get_action(p, actions):
            
    for action in actions:
        if action.is_attack:
            enemy_unit = p[1].units[action.attackpos]
            chance = m.chance_of_win(action.unit, enemy_unit, action)
            action.score = chance * 10
            if hasattr(action.unit, "double_attack_cost"):
                    action.score = action.score / 2
        else:
            action.score = 0
    
    
    if hasattr(action, "push"):
        print "push"
        action.score = 30
    
    rnd.shuffle(actions)
    actions.sort(key = attrgetter("score"), reverse= True)
    if settings.document_ai_actions:
        m.document_actions("Destroyer", actions, p)  
    return actions[0]


def put_counter(p, unit):
        unit.acounters += 1