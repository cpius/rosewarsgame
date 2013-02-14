from __future__ import division
import itertools
from operator import attrgetter
import ai_methods as m
import random as rnd




def get_action(p, actions, document_it = False):
            
    for action in actions:
        if action.is_attack:
                chance = m.chance_of_win(action.unit, action.enemy_unit, action)
                action.score = chance * 10
                if hasattr(action.unit, "double_attack_cost"):
                        action.score = action.score / 2
        else:
                action.score = 0
    
    rnd.shuffle(actions)
    actions.sort(key = attrgetter("score"), reverse= True)
    if document_it:
        m.document_actions("Destroyer", actions, p)  
    return actions[0]


def get_extra_action(p, actions, document_it = False):
    return get_action(p, actions, document_it)


def put_counter(p, unit):
        unit.acounters += 1