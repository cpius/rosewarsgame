from __future__ import division
import itertools
from operator import attrgetter
import ai_methods as m
import random as rnd




def get_action(p, actions, document_it = False):
    
    
    for action in actions:
        unit = action.unit
        action.score = 0
        if action.is_attack:
                action.score += 0.5
                
                if unit.name == "Catapult":
                        action.score += 6
                
                if unit.name == "Ballista":
                        action.score += 3

                action.score += unit.acounters / 2
    
        else:

                if unit.name == "Catapult" and action.endpos[1] > action.startpos[1]:
                        action.score += 2
                
                if unit.name == "Ballista" and action.endpos[1] > action.startpos[1]:
                        action.score += 1              
    
    
    rnd.shuffle(actions)  
    actions.sort(key = attrgetter("score"), reverse= True)
    if document_it:
        m.document_actions("Catapulter", actions, p)  
    return actions[0]
    

def get_second_action(p, actions, document_it = False):
    return get_action(p, actions, document_it)


def put_counter(p, unit):
        unit.acounters += 1