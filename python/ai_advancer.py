from operator import attrgetter
import ai_methods
import random
import interface_settings as settings


def get_action(actions, gamestate):
    
    for action in actions:
        action.score = action.end_at.row
        
        if action.end_at.row > action.start_at.row:
            action.score += 1
        
        if action.is_attack():
            action.score += 0.25
            if action.target_at.row > action.end_at.row and action.move_with_attack:
                action.score += 0.5
    
    random.shuffle(actions)
    actions.sort(key=attrgetter("score"), reverse=True)
    
    if settings.document_ai_actions:
        ai_methods.document_actions(actions, gamestate)

    return actions[0]
