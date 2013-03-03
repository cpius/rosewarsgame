import itertools
from operator import attrgetter
import ai_methods as m
import random as rnd
import settings


def get_action(p, actions):
    
    for action in actions:
        action.score = action.endpos[1]
        
        if action.endpos[1] > action.startpos[1]:
            action.score += 1
        
        if action.is_attack:
            action.score += 0.25
            if action.attackpos[1] > action.endpos[1] and action.move_with_attack:
                action.score += 0.5
    
    rnd.shuffle(actions)
    actions.sort(key = attrgetter("score"), reverse= True)
    
    if settings.document_ai_actions:
        m.document_actions("Advancer", actions, p)
    return actions[0]
    

def put_counter(p, unit):
    unit.dcounters += 1