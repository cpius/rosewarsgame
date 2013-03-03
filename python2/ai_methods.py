from __future__ import division
import battle
from ai_module import get_transformed_action
import copy
import gamestate
import settings



def document_actions(ai_type, actions, p):
    
    if p[0].actions_remaining == 1:
        taction = "1"
    else:
        taction = "2"
        
    if hasattr(p[0], "extra_action"):
        taction += ".2"
    
    out = open("./replay/" + p[0].color + " AI actions " + str(settings.turn) + "." + taction + ".txt", 'w')
    
    for action in actions:
        if p[0].color == "Red":
            #action = copy.deepcopy(action)
            action = gamestate.copy_action(action)
            get_transformed_action(action)
            
        out.write(str(action) + "\n")
        out.write("Score: " + str(round(action.score,2)) + "\n")
        if hasattr(action, "score_success"):
            out.write("Score sucess: " + str(round(action.score_success)) + " Score failure: " + str(round(action.score_failure)) + "\n")
        out.write("\n")
    out.close()


def chance_of_win(a, d, action):

    attack = battle.get_attack(a, d, action)
    defence = battle.get_defence(a, d, attack, action)

    if attack < 0:
        attack = 0
    
    if attack > 6:
        attack = 6
        
    if defence < 0:
        defence = 0
    
    if defence > 6:
        defence = 6

    return ((7 - attack) / 6) * ((6 - defence) / 6)