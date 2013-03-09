from operator import attrgetter
import ai_methods as m
import random as rnd
import settings
import gamestate_module
import copy
import ai_module


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
            ai_module.get_transformed_action(action)
            
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


def perform_action(action, g):

    g.do_action(action)
    if hasattr(g.players[0], "extra_action"):
        extra_action = g.players[0].ai.select_action(g)
        perform_action(extra_action, g)
    g.players[0].ai.add_counters(g)


def get_values_and_score(g, g_orig):

    values = get_action_values(g, g_orig)
    player1_score = evaluate_action_values(values["player1"])
    player2_score = evaluate_action_values(values["player2"])
    score = player1_score - player2_score
    
    return values, score


def get_action_success(action):
    action.finalpos = action.endpos
    action.rolls = (1, 6)
    for sub_action in action.sub_actions:
        sub_action.rolls = (1, 6)
        
    return action


def get_action_failure(action):
    action.finalpos = action.endpos
    action.rolls = (6, 1)
    for sub_action in action.sub_actions:
        sub_action.rolls = (6, 1)
        
    return action


def find_action_scores_one_action(actions, g_orig):

    gamestate = gamestate_module.save_gamestate(g_orig)

    for action in actions:

        g = gamestate_module.load_gamestate(gamestate)

        if action.is_attack:

            action.chance_of_win = m.chance_of_win(action.unit_ref, action.target_ref, action)

            action = get_action_success(action)

            perform_action(action, g)

            action.values_success, action.score_success = get_values_and_score(g, g_orig)

            g = gamestate_module.load_gamestate(gamestate)

            action = get_action_failure(action)

            perform_action(action, g)

            action.values_failure, action.score_failure = get_values_and_score(g, g_orig)

            action.score = action.chance_of_win * action.score_success +\
                (1 - action.chance_of_win) * action.score_failure

        elif action.is_ability:

            perform_action(action, g)

            action.values, action.score = get_values_and_score(g, g_orig)

        else:

            perform_action(action, g)

            action.values, action.score = get_values_and_score(g, g_orig)

    return actions


def get_action(actions, g):

    gc = g.copy()

    actions = gc.get_actions()

    actions = find_action_scores_one_action(actions, gc)

    rnd.shuffle(actions)
    actions.sort(key=attrgetter("score"), reverse=True)
    
    if settings.document_ai_actions:
        document_actions(actions, gc)

    return actions[0]    


def put_counter(unit):

    if unit.name in ["Pikeman", "Heavy Cavalry", "Royal Guard", "Viking"]:
        unit.defence_counters += 1
    else:
        unit.attack_counters += 1


def evaluate_action_values(values):
    
    return sum(value for value in values["gained"].values()) - sum(value for value in values["lost"].values())


def get_action_values(g, g_orig):
    
    def get_values_unit(pos, unit, backline):

        values = {}

        if pos[1] == (9 - backline):
            values["line 8"] = 1000
                 
        if pos[1] == (9 - backline) - 1:
            values["line 7"] = 4
    
        if pos[1] == (9 - backline) - 2:
            values["line 6"] = 2

        if pos[1] == (9 - backline) - 3:
            values["line 5"] = 0.5
            
        if unit.name in settings.special_units:
            values["Special unit"] = 8
        else:
            values["Basic unit"] = 4
    
        return values

    def give_back_bribed_units():
        for pos, unit in g.units[1].items():
            if hasattr(unit, "bribed"):
                g.units[0][pos] = g.units[1].pop(pos)

        for pos, unit in g.units[0].items():
            if hasattr(unit, "bribed"):
                g.units[1][pos] = g.units[0].pop(pos)

    def fill_values():

        new_player1 = set(g.units[0]) - set(g_orig.units[0])
        old_player1 = set(g_orig.units[0]) - set(g.units[0])

        new_player2 = set(g.units[1]) - set(g_orig.units[1])
        old_player2 = set(g_orig.units[1]) - set(g.units[1])

        for pos in new_player1:
            values["player1"]["gained"] = get_values_unit(pos, g.units[0][pos], g.players[0].backline)

        for pos in old_player1:
            values["player1"]["lost"] = get_values_unit(pos, g_orig.units[0][pos], g.players[0].backline)

        for key in values["player1"]["gained"].keys():
            if key in values["player1"]["lost"].keys():
                del values["player1"]["gained"][key]
                del values["player1"]["lost"][key]

        for pos in new_player2:
            values["player2"]["gained"] = get_values_unit(pos, g.units[1][pos], g.players[1].backline)

        for pos in old_player2:
            values["player2"]["lost"] = get_values_unit(pos, g_orig.units[1][pos], g.players[1].backline)

    values = {"player1": {"gained": {}, "lost": {}}, "player2": {"gained": {}, "lost": {}}}

    give_back_bribed_units()

    fill_values()

    return values
