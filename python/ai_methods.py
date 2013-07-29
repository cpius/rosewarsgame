from __future__ import division
import battle
import copy


def document_actions(actions, g):
    
    if g.get_actions_remaining() == 1:
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


def chance_of_win(gamestate, attacking_unit, defending_unit, action):

    attack_rating = battle.get_attack_rating(attacking_unit, defending_unit, action, gamestate)
    defence_rating = battle.get_defence_rating(attacking_unit, defending_unit, attack_rating, action, gamestate)

    if attack_rating < 0:
        attack_rating = 0
    
    if attack_rating > 6:
        attack_rating = 6
        
    if defence_rating < 0:
        defence_rating = 0
    
    if defence_rating > 6:
        defence_rating = 6
    
    chance_of_attack_successful = attack_rating / 6
    
    chance_of_defence_unsuccessful = (6 - defence_rating) / 6

    return chance_of_attack_successful * chance_of_defence_unsuccessful
