import itertools
from operator import attrgetter
import ai_methods as m
import random as rnd
import settings


def get_action(actions, g):
    
    for action in actions:
        action.score = action.end_at.row
        
        if action.end_at.row > action.start_at.row:
            action.score += 1
        
        if action.is_attack():
            action.score += 0.25
            if action.target_at.row > action.end_at.row and action.move_with_attack:
                action.score += 0.5
    
    rnd.shuffle(actions)
    actions.sort(key=attrgetter("score"), reverse=True)
    
    if settings.document_ai_actions:
        m.document_actions(actions, g)
    return actions[0]
