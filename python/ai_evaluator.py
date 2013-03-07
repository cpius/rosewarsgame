from operator import attrgetter
import ai_methods as m
import random as rnd
import settings
import gamestate
import mover
import copy
import setup
import numpy as np


def document_actions(actions, players):
    
    if players[0].actions_remaining == 2:
        taction = "1"
    else:
        taction = "2"
        
    if hasattr(players[0], "extra_action"):
        taction += ".2"
    
    out = open("./replay/" + players[0].color + " AI actions " + str(settings.turn) + "." + taction + ".txt", 'w')
    
    for action in actions:
        if players[0].color == "Red":
            action = gamestate.copy_action(action)
            get_transformed_action(action)
            
        out.write(" -- " + str(action) + " -- \n")
        
        out.write("\n")
        
        if action.is_attack:
            out.write("Chance of success: " + str(round(action.chance_of_win * 100)) + "%\n\n")
            out.write("Success\n")
            if action.values_success["player1"]["gained"]:
                out.write("Player 1 Gain: " + str(action.values_success["player1"]["gained"]) + "\n")
            if action.values_success["player1"]["lost"]:
                out.write("Player 1 Loss: " + str(action.values_success["player1"]["lost"]) + "\n")

            if action.values_success["player2"]["gained"]:
                out.write("Player 2 Gain: " + str(action.values_success["player2"]["gained"]) + "\n")
            if action.values_success["player2"]["lost"]:
                out.write("Player 2 Loss: " + str(action.values_success["player2"]["lost"]) + "\n")
            out.write("Overall: " + str(action.score_success) + "\n")
            out.write("\n")
            
            out.write("Failure\n")
            if action.values_failure["player1"]["gained"]:
                out.write("Playes 1 Gain: " + str(action.values_failure["player1"]["gained"]) + "\n")
            if action.values_failure["player1"]["lost"]:
                out.write("Player 1 Loss: " + str(action.values_failure["player1"]["lost"]) + "\n")
            out.write("Overall: " + str(action.score_failure) + "\n")
            out.write("\n")
        
        else:
            if action.values["player1"]["gained"]:
                out.write("Player 1 Gain: " + str(action.values["player1"]["gained"]) + "\n")
            if action.values["player1"]["lost"]:
                out.write("Player 1 Loss: " + str(action.values["player1"]["lost"]) + "\n")
            out.write("Overall: " + str(action.score) + "\n")
            out.write("\n")
      
        if hasattr(action, "score_success"):
            out.write("Score success: " + str(action.score_success)
                      + ", Score failure: " + str(action.score_failure) + "\n")
        out.write("Action Score: " + str(round(action.score, 2)) + "\n")

        out.write("\n")
        
        if hasattr(action, "next_action"):
            out.write("Next Action:\n")
            if action.next_action:
                out.write(str(action.next_action) + "\n")
                if hasattr(action.next_action, "chance_of_win"):
                    out.write("Chance of win: " + str(action.next_action.chance_of_win) + "\n")
                out.write("Action Score: " + str(round(action.next_action.score, 2)) + "\n")
            else:
                out.write("No next actions\n")
            out.write("\n")

        if hasattr(action, "combined_score"):
            out.write("Combined score: " + str(round(action.combined_score, 2)) + "\n")

        out.write("\n\n\n")         

        out.write("\n")
    out.close()


def perform_action(action, p):
    
    mover.do_action(action, p)
    if hasattr(p[0], "extra_action"):
        extra_action = p[0].ai.select_action(p)
        p = perform_action(extra_action, p)
    p[0].ai.add_counters(p)
    
    return p


def find_action_scores_one_action(saved_gamestate, actions):
    
    p_orig = gamestate.load_gamestate(saved_gamestate)
    
    for action in actions:
        
        p = gamestate.load_gamestate(saved_gamestate)
    
        unit = p[0].units[action.startpos]
        
        if action.is_attack:
    
            enemy_unit = action.target_unit
            
            action.chance_of_win = m.chance_of_win(unit, enemy_unit, action)
    
            action = get_action_success(action)
            
            p = perform_action(action, p)
            
            action.values_success, action.score_success = get_values_and_score(action, p, p_orig)
           
            p = gamestate.load_gamestate(saved_gamestate)
    
            action = get_action_failure(action)
                
            p = perform_action(action, p)
    
            action.values_failure, action.score_failure = get_values_and_score(action, p, p_orig)
    
            action.score = action.chance_of_win * action.score_success \
                + (1 - action.chance_of_win) * action.score_failure

        elif action.is_ability:
            
            p = perform_action(action, p)

            action.values, action.score = get_values_and_score(action, p, p_orig)

        else:
    
            p = perform_action(action, p)
            
            action.values, action.score = get_values_and_score(action, p, p_orig)
            
    return actions


def get_next_action(action, actions, p):

    saved_gamestate = gamestate.save_gamestate(p)
    
    if hasattr(action, "double_cost"):
        return []

    actions_copy = [copy.copy(action_c) for action_c in actions]
    
    actions_copy = [action_copy for action_copy in actions_copy if action_copy.startpos != action.startpos
                    and not hasattr(action_copy, "double_cost")]

    for action_copy in actions_copy:
        if hasattr(p[0].units[action_copy.startpos], "improved_weapons") and action_copy.is_attack:
            
            action_copy.chance_of_win =\
                m.chance_of_win(p[0].units[action_copy.startpos], p[1].units[action_copy.attackpos], action_copy)

            action_copy.chance_of_win = 1
        
            action_copy.score = action_copy.chance_of_win * action_copy.score_success\
                + (1 - action_copy.chance_of_win) * action_copy.score_failure

    actions_copy.sort(key=attrgetter("score"), reverse=True)

    return actions_copy[0]


def get_values_and_score(action, p, p_orig):

    totals = {}

    values = get_action_values(p, p_orig)
    player1_score = evaluate_action_values(values["player1"])
    player2_score = evaluate_action_values(values["player2"])
    score = player1_score - player2_score
    
    return values, score


def get_action_success(action):
    action.finalpos = action.endpos
    action.rolls = (6, 6)
    for sub_action in action.sub_actions:
        sub_action.rolls = (6, 6)
        
    return action


def get_action_failure(action):
    action.finalpos = action.endpos
    action.rolls = (1, 1)
    for sub_action in action.sub_actions:
        sub_action.rolls = (1, 1)
        
    return action
                
                
def find_action_scores_two_actions(saved_gamestate, actions_orig):

    p_orig = gamestate.load_gamestate(saved_gamestate)
    
    actions = copy.copy(actions_orig)

    for action in actions:
        p = gamestate.load_gamestate(saved_gamestate)
    
        unit = p[0].units[action.startpos]
        
        if action.is_attack:
    
            enemy_unit = action.target_unit
            
            action.chance_of_win = m.chance_of_win(unit, enemy_unit, action)
    
            action = get_action_success(action)

            p = perform_action(action, p)

            action.values_success, action.score_success = get_values_and_score(action, p, p_orig)
   
            p = gamestate.load_gamestate(saved_gamestate)
            
            action = get_action_failure(action)
            
            p = perform_action(action, p)
 
            action.values_failure, action.score_failure = get_values_and_score(action, p, p_orig)
    
            action.score = action.chance_of_win * action.score_success \
                + (1 - action.chance_of_win) * action.score_failure

            action.next_action = get_next_action(action, actions_orig, p)
            
            if action.next_action:
                action.combined_score = action.score + action.next_action.score
                if action.score < action.next_action.score:
                    action.combined_score -= 0.01
            else:
                action.combined_score = action.score

        elif action.is_ability:
            
            p = perform_action(action, p)

            action.values, action.score = get_values_and_score(action, p, p_orig)

            for action_copy in actions_orig:
                if action_copy.is_attack and action_copy.chance_of_win == 1:
                    print "before loop, chance of win 1"

            action.next_action = get_next_action(action, actions_orig, p)
     
            if action.next_action:
                action.combined_score = action.score + action.next_action.score
                if action.score < action.next_action.score:
                    action.combined_score -= 0.1
            else:
                action.combined_score = action.score
        
        else:
    
            p = perform_action(action, p)
            
            action.values, action.score = get_values_and_score(action, p, p_orig)

            action.next_action = get_next_action(action, actions_orig, p)
            
            if action.next_action:
                action.combined_score = action.score + action.next_action.score
                if action.score < action.next_action.score:
                    action.combined_score -= 0.1
            else:
                action.combined_score = action.score
            
    return actions


def get_action(p, actions):

    saved_gamestate = gamestate.save_gamestate(p)
    
    possible_actions = mover.get_actions(p)

    actions_orig = find_action_scores_one_action(saved_gamestate, possible_actions)
     
    actions_orig.sort(key = attrgetter("score"), reverse= True)

    print "actions orig score", actions_orig[0].score 
     
    if p[0].actions_remaining == 1:
                
        actions = actions_orig

        rnd.shuffle(actions)

        actions.sort(key = attrgetter("score"), reverse=True)

    else:
        actions = find_action_scores_two_actions(saved_gamestate, actions_orig)

        rnd.shuffle(actions)
        actions.sort(key = attrgetter("combined_score"), reverse=True)
    
    if settings.document_ai_actions:
        document_actions(actions, p)

    return actions[0]    


def put_counter(p, unit):
    unit.dcounters += 1


def evaluate_action_values(values):
    
    return sum(value for value in values["gained"].values()) - sum(value for value in values["lost"].values())


def get_action_values(p, p_orig):
    
    def get_values_unit(pos, unit, backline):

        values = {}

        if pos[1] == (9 - backline):
            values["line8"] = 1000
                 
        if pos[1] == (9 - backline) -1:
            values["line7"] = 4
    
        if pos[1] == (9 - backline) -2:
            values["line6"] = 2

        if pos[1] == (9 - backline) -3:
            values["line5"] = 0.5
            

        if unit.name == "Ballista":
            values["Ballista"] = 7
        
        elif unit.name == "Pikeman":
            values["Pikeman"] = 4
            
        elif unit.name in setup.special_unit_names:
            values["Special"] = 10
            
        else:
            values["otherunit"] = 2  
    
        return values

    values = {}
    values["player1"] = {}
    values["player1"]["gained"] = {}
    values["player1"]["lost"] = {}
    values["player2"] = {}
    values["player2"]["gained"] = {}
    values["player2"]["lost"] = {}
    
    for pos, unit in p[1].units.items():
        if hasattr(unit, "bribed"):
            p[0].units[pos] = p[1].units.pop(pos)

    for pos, unit in p[0].units.items():
        if hasattr(unit, "bribed"):
            p[1].units[pos] = p[0].units.pop(pos)
  
    new_p0 = set(p[0].units) - set(p_orig[0].units)
    old_p0 = set(p_orig[0].units) - set(p[0].units)

    new_p1 = set(p[1].units) - set(p_orig[1].units)
    old_p1 = set(p_orig[1].units) - set(p[1].units)
 
    for pos in new_p0:
        values["player1"]["gained"] = get_values_unit(pos, p[0].units[pos], p[0].backline)
    
    for pos in old_p0:
        values["player1"]["lost"] = get_values_unit(pos, p_orig[0].units[pos], p[0].backline)
    
    for key in values["player1"]["gained"].keys():
        if key in values["player1"]["lost"].keys():
            del values["player1"]["gained"][key]
            del values["player1"]["lost"][key]
    
    for pos in new_p1:
        values["player2"]["gained"] = get_values_unit(pos, p[1].units[pos], p[1].backline)
    
    for pos in old_p1:
        values["player2"]["lost"] = get_values_unit(pos, p_orig[1].units[pos], p[1].backline)

    return values
