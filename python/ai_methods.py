from __future__ import division
import battle
import copy


def document_actions(actions, gamestate):
    
    if gamestate.get_actions_remaining() == 1:
        current_action = "1"
    else:
        current_action = "2"
        
    if gamestate.is_extra_action():
        current_action += ".extra"
    
    out = open("./replay/AI actions " + str(gamestate.action_number) + "." + current_action + ".txt", 'w')
    
    for action in actions:
        action = copy.copy(action)

        out.write(str(action) + "\n")
        out.write("Score: " + str(round(action.score, 2)) + "\n")
        if hasattr(action, "score_success"):
            out.write("Score success: " + str(round(action.score_success)) + " Score failure: " +
                      str(round(action.score_failure)) + "\n")
        out.write("\n")
    out.close()


def chance_of_win(gamestate, attacking_unit, defending_unit, action):

    attack_rating = battle.get_attack_rating(attacking_unit, defending_unit, action, gamestate.player_units)
    defence_rating = battle.get_defence_rating(attacking_unit, defending_unit, attack_rating, action, gamestate.enemy_units)

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
