from __future__ import division
import battle
from ai_module import get_transformed_action
import copy


def document_actions(actions, g):
    
    if g.players[0].actions_remaining == 1:
        current_action = "1"
    else:
        current_action = "2"
        
    if hasattr(g.players[0], "extra_action"):
        current_action += ".2"
    
    out = open("./replay/" + g.players[0].color + " AI actions " + str(g.turn) + "." + current_action + ".txt", 'w')
    
    for action in actions:
        if g.players[0].color == "Red":
            action = copy.copy(action)
            action = get_transformed_action(action)
            
        out.write(str(action) + "\n")
        out.write("Score: " + str(round(action.score, 2)) + "\n")
        if hasattr(action, "score_success"):
            out.write("Score success: " + str(round(action.score_success)) + " Score failure: " +
                      str(round(action.score_failure)) + "\n")
        out.write("\n")
    out.close()


def chance_of_win(attacking_unit, defending_unit, action):

    attack = battle.get_attack(attacking_unit, defending_unit, action)
    defence = battle.get_defence(attacking_unit, defending_unit, attack, action)

    if attack < 0:
        attack = 0
    
    if attack > 6:
        attack = 6
        
    if defence < 0:
        defence = 0
    
    if defence > 6:
        defence = 6
    
    chance_of_attack_successful = attack / 6
    
    chance_of_defence_unsuccessful = (6 - defence) / 6

    return chance_of_attack_successful * chance_of_defence_unsuccessful
