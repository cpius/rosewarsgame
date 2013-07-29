import itertools
from operator import attrgetter
import ai_methods as m
import random as rnd
import settings


def get_action(actions, g):
    
    for action in actions:
        action.score = action.end_position.row
        
        if action.end_position.row > action.start_position.row:
            action.score += 1
        
        if action.is_attack():
            action.score += 0.25
            if action.attack_position.row > action.end_position.row and action.is_move_with_attack():
                action.score += 0.5
    
    rnd.shuffle(actions)
    actions.sort(key=attrgetter("score"), reverse=True)
    
    if settings.document_ai_actions:
        m.document_actions(actions, g)
    return actions[0]
