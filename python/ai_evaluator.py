from __future__ import division
from operator import attrgetter
import ai_methods as m
import random as rnd
import settings
import gamestate_module
import copy
import ai_module
import action_getter
import math

board = set((i, j) for i in range(1, 6) for j in range(1, 9))


def document_actions(actions, g):

    if g.players[0].actions_remaining == 1:
        current_action = "2"
    else:
        current_action = "1"

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
                out.write("Player 1 Gain: " + str(action.values_failure["player1"]["gained"]) + "\n")
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

        if hasattr(action, "score_with_next"):
            out.write("Score with next: " + str(round(action.score_with_next, 2)) + "\n")

        out.write("\n")

        try:
            if hasattr(action, "next_action_if_success"):
                if hasattr(action, "next_action_if_failure") and action.next_action_if_success.score != \
                        action.next_action_if_failure.score:
                    out.write("Next Action If Success:\n")
                    if action.next_action_if_success:
                        out.write(str(action.next_action_if_success) + "\n")
                        out.write("Action Score: " + str(round(action.next_action_if_success.score, 2)) + "\n")
                    else:
                        out.write("No next actions\n")
                    out.write("\n")

                    if hasattr(action, "next_action_if_failure"):
                        out.write("Next Action If Failure:\n")
                        if action.next_action_if_failure:
                            out.write(str(action.next_action_if_failure) + "\n")
                            out.write("Action Score: " + str(round(action.next_action_if_failure.score, 2)) + "\n")
                        else:
                            out.write("No next actions\n")
                        out.write("\n")

                else:
                    out.write("Next Action:\n")
                    if action.next_action_if_success:
                        out.write(str(action.next_action_if_success) + "\n")
                        out.write("Action Score: " + str(round(action.next_action_if_success.score, 2)) + "\n")
                    else:
                        out.write("No next actions\n")
                    out.write("\n")

            if hasattr(action, "next_action"):
                out.write("Next Action:\n")
                if action.next_action:
                    out.write(str(action.next_action) + "\n")
                    out.write("Action Score: " + str(round(action.next_action.score, 2)) + "\n")
                else:
                    out.write("No next actions\n")
                out.write("\n")

        except AttributeError:
            print "attribute error"


        if hasattr(action, "combined_score"):
            out.write("Combined score: " + str(round(action.combined_score, 2)) + "\n")

        out.write("\n\n\n")         

        out.write("\n")
    out.close()


def get_chariot_pos(units):
    for pos, unit in units.items():
        if unit.name == "Chariot":
            return pos


def perform_action(action, g):

    g.do_action(action)
    #if hasattr(g.players[0], "extra_action"):
    #    g_copy = g.copy()
    #    extra_action = g.players[0].ai.select_action(g_copy)
    #    perform_action(extra_action, g)
    put_counter(g)


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


def find_action_scores_two_actions(actions, g_orig):

    gamestate = gamestate_module.save_gamestate(g_orig)

    for action in actions:

        g = gamestate_module.load_gamestate(gamestate)

        if action.is_attack:

            action.chance_of_win = m.chance_of_win(action.unit_ref, action.target_ref, action)

            action = get_action_success(action)

            perform_action(action, g)

            action.next_action_if_success = get_next_action(g)

            action.values_success, action.score_success = get_values_and_score(g, g_orig)

            g = gamestate_module.load_gamestate(gamestate)

            action = get_action_failure(action)

            perform_action(action, g)

            action.next_action_if_failure = get_next_action(g)

            action.values_failure, action.score_failure = get_values_and_score(g, g_orig)

            action.score = action.chance_of_win * action.score_success + \
                (1 - action.chance_of_win) * action.score_failure

            if action.next_action_if_success:
                action.score_with_next = action.chance_of_win * (action.score_success + action.next_action_if_success.score) +\
                    (1 - action.chance_of_win) * (action.score_failure + action.next_action_if_failure.score)
            else:
                action.score_with_next = action.score

        elif action.is_ability:

            perform_action(action, g)

            action.next_action = get_next_action(g)

            action.values, action.score = get_values_and_score(g, g_orig)

            action.score_with_next = action.score + action.next_action.score

        else:

            perform_action(action, g)

            action.next_action = get_next_action(g)

            action.values, action.score = get_values_and_score(g, g_orig)

            action.score_with_next = action.score + action.next_action.score

    return actions


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


def get_next_action(g):

    if g.players[0].actions_remaining == 0:
        return None

    gc = g.copy()

    actions = gc.get_actions()

    if gc.players[0].actions_remaining == 2:
        actions = find_action_scores_two_actions(actions, gc)
        rnd.shuffle(actions)
        actions.sort(key=attrgetter("score"), reverse=True)
    else:
        actions = find_action_scores_one_action(actions, gc)
        rnd.shuffle(actions)
        actions.sort(key=attrgetter("score"), reverse=True)

    return actions[0]


def get_action(actions, g):

    gc = g.copy()

    if gc.players[0].actions_remaining == 2:
        actions = find_action_scores_two_actions(actions, gc)
        rnd.shuffle(actions)
        actions.sort(key=attrgetter("score_with_next"), reverse=True)
    else:
        actions = find_action_scores_one_action(actions, gc)
        rnd.shuffle(actions)
        actions.sort(key=attrgetter("score"), reverse=True)

    if settings.document_ai_actions:
        document_actions(actions, gc)

    return actions[0]    


def put_counter(g):

    def decide_counter(unit):
        if unit.name in ["Pikeman", "Heavy Cavalry", "Royal Guard", "Viking"]:
            unit.defence_counters += 1
        else:
            unit.attack_counters += 1

    for unit in g.units[0].values():
        if unit.xp == 2:
            if unit.defence + unit.defence_counters == 4:
                unit.attack_counters += 1
            else:
                if not unit.attack:
                    unit.defence_counters += 1
                else:
                    decide_counter(unit)
            unit.xp = 0


def evaluate_action_values(values):
    
    return sum(value for value in values["gained"].values()) - sum(value for value in values["lost"].values())


def get_action_values(g, g_orig):

    def get_values_unit_player(unit, pos, g):

        friendly_units = action_getter.find_all_friendly_units_except_current(pos, g.units[0])
        all_units = dict(friendly_units.items() + g.units[1].items())

        def get_backline_value(unit, pos, g):

            def get_coloumn_blocks(unit, pos, g):
                cols = [pos[0] + i for i in [-1, 0, 1] if pos[0] + i in [1, 2, 3, 4, 5]]

                coloumn_blocks = []
                for col in cols:
                    blocks = 0
                    for enemy_pos, enemy_unit in g.units[1].items():
                        if enemy_pos[0] == col and enemy_pos[1] > pos[1]:
                            blocks += 1
                        if (enemy_pos[0] == col - 1 or enemy_pos[0] == col - 1) and enemy_pos[1] >= pos[1]:
                            if enemy_unit.zoc:
                                if unit.type in enemy_unit.zoc:
                                    blocks += 1
                    coloumn_blocks.append(blocks)

                return coloumn_blocks

            def get_moves_to_backline(unit, pos):
                return math.ceil((8 - pos[1]) / unit.movement)

            moves_to_backline = get_moves_to_backline(unit, pos)
            coloumn_blocks = get_coloumn_blocks(unit, pos, g)

            if moves_to_backline == 0:
                return "backline", 1000

            if unit.name == "Berserker":
                if math.ceil((8 - pos[1]) / 4) == 1:
                    actions = action_getter.get_unit_actions(unit, pos, all_units, g.units[1], friendly_units)[0]
                    if any(action.endpos[1] == 8 for action in actions):
                        return "One action from backline", 20
                    elif any(action.is_attack and action.attackpos[1] == 8 and action.move_with_attack for
                             action in actions):
                        return "One attack from backline", 10
                    else:
                        if coloumn_blocks[1] < 2:
                            return "Berserking distance", 5

            if moves_to_backline == 1:
                actions = action_getter.get_unit_actions(unit, pos, all_units, g.units[1], friendly_units)[0]
                if any(action.endpos[1] == 8 for action in actions):
                    return "One action from backline", 20
                elif any(action.is_attack and action.attackpos[1] == 8 and action.move_with_attack
                         for action in actions):
                    return "One attack from backline", 10

            if unit == "Viking" and hasattr(unit, "extra_life"):
                if moves_to_backline == 1:
                    return "One move from backline, viking", 6

                elif moves_to_backline == 2:
                    return "Two moves from backline, viking", 4

                elif moves_to_backline == 3:
                    return "Three moves from backline, viking", 1

            if moves_to_backline == 1 and coloumn_blocks[1] <= 1 and unit.defence < 3:
                return "One move from backline, Light Cavalry", 4

            if moves_to_backline == 1 and coloumn_blocks[1] <= 1 and unit.defence >= 3:
                return "One move from backline, Heavy Cavalry", 6

            if moves_to_backline == 2 and unit.defence >= 3:
                return "Two moves from backline, Heavy Cavalry", 2

            if moves_to_backline == 2 and unit.movement < 3:
                return "Two moves from backline, Light Cavalry", 1

            return None, None

        values = {}

        value_title, value = get_backline_value(unit, pos, g)
        if value:
            values[value_title] = value

        if unit.name == "Longswordsman":
            attacks = action_getter.get_unit_actions(unit, pos, all_units, g.units[1], friendly_units)[1]
            maxscore = 0
            for attack in attacks:
                if attack.sub_actions:
                    score = len(attack.sub_actions)
                    maxscore = max(maxscore, score)

            if maxscore > 0:
                values["Longsword multiple hit possible"] = maxscore + 1

        if unit.name == "Samurai":
            pass

        if unit.name == "Flag Bearer":
            pass

        if unit.name == "Crusader":
            pass

        if unit.range > 1:
            for enemy_pos in g.units[1]:
                if action_getter.distance(pos, enemy_pos) <= unit.range:
                    values["Within range"] = 1

        if hasattr(unit, "improved_weapons"):
            values["improved_weapons"] = 0.5

        if unit.attack_counters or unit.defence_counters:
            values["counter"] = 1

        return values

    def get_values_unit_opponent(unit, pos, g):

        friendly_units = action_getter.find_all_friendly_units_except_current(pos, g.units[0])
        all_units = dict(friendly_units.items() + g.units[1].items())

        def get_backline_value(unit, pos, g):

            def get_moves_to_backline(unit, pos):
                return math.ceil((pos[1] - 1) / unit.movement)

            moves_to_backline = get_moves_to_backline(unit, pos)

            if moves_to_backline == 0:
                return "backline", 1000

            if unit.name == "Berserker":
                if math.ceil((pos[1] - 1) / 4):
                    actions = action_getter.get_unit_actions(unit, pos, all_units, g.units[1], friendly_units)[0]
                    if any(action.endpos[1] == 1 for action in actions):
                        return "One action from backline", 200
                    elif any(action.is_attack and action.attackpos[1] == 1 and action.move_with_attack for
                             action in actions):
                        return "One attack from backline", 40
                    else:
                        return "Berserking distance", 4

            if moves_to_backline == 1:
                actions = action_getter.get_unit_actions(unit, pos, all_units, g.units[1], friendly_units)[0]
                if any(action.endpos[1] == 1 for action in actions):
                    return "One action from backline", 200
                elif any(action.is_attack and action.attackpos[1] == 1 and action.move_with_attack
                         for action in actions):
                    return "One attack from backline", 40

            if unit == "Viking" and hasattr(unit, "extra_life"):
                if moves_to_backline == 1:
                    return "One move from backline, viking", 6

                elif moves_to_backline == 2:
                    return "Two moves from backline, viking", 4

            if moves_to_backline == 1:
                return "One move from backline", 4

            if moves_to_backline == 2 and unit.movement < 3:
                return "Two moves from backline", 3

            if moves_to_backline == 2 and unit.movement >= 3:
                return "Two moves from backline, Light Cavalry", 1

            return None, None

        values = {}

        value_title, value = get_backline_value(unit, pos, g)
        if value:
            values[value_title] = value

        if unit.name == "Viking":
            if hasattr(unit, "extra_lives"):
                values["extra life"] = 5

        if unit.name == "Longswordsman":
            pass
            """
            unit_actions = action_getter.get_unit_actions(unit, pos, all_units, g.units[1], g.units[1])

            if unit_action.sub_actions:
                values["Potential longsword attack"] = unit_action.sub_actions
            """

        if unit.name == "Samurai":
            pass

        if unit.name == "Flag Bearer":
            pass

        if unit.name == "Crusader":
            pass

        if unit.name in ["Chariot", "Samurai", "War Elephant", "Scout", "Lancer", "Royal Guard", "Berserker",
                         "Crusader", "Longswordsman", "Flag Bearer", "Cannon", "Weaponsmith"]:
            values["Special unit"] = 8
        else:
            values["Basic unit"] = 4

        if unit.attack_counters or unit.defence_counters:
            values["counter"] = 1

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
            values["player1"]["gained"] = get_values_unit_player(g.units[0][pos], pos, g)

        for pos in old_player1:
            values["player1"]["lost"] = get_values_unit_player(g_orig.units[0][pos], pos, g)

        for key in values["player1"]["gained"].keys():
            if key in values["player1"]["lost"].keys():
                del values["player1"]["gained"][key]
                del values["player1"]["lost"][key]

        for pos in new_player2:
            values["player2"]["gained"] = get_values_unit_opponent(g.units[1][pos], pos, g)

        for pos in old_player2:
            values["player2"]["lost"] = get_values_unit_opponent(g_orig.units[1][pos], pos, g)

    values = {"player1": {"gained": {}, "lost": {}}, "player2": {"gained": {}, "lost": {}}}

    give_back_bribed_units()

    fill_values()

    return values
