from __future__ import division
from player import Player
from gamestate_module import Gamestate
import setup
import sys
from time import time

_total_ai1_time = 0
_total_ai2_time = 0
_total_moves = 0


def perform_action(action, g):

    all_actions = g.get_actions()

    matchco = 0
    for possible_action in all_actions:
        if action == possible_action:
            matchco += 1
            action = possible_action

    if matchco == 1:

        g.do_action(action)

        g.players[0].ai.add_counters(g)

        g.initialize_action()

        if (g.get_actions_remaining() < 1 or len(all_actions) == 1) and not hasattr(g.players[0], "extra_action"):
            g.turn_shift()

    return g


def run_game(g):

    global _total_ai1_time
    global _total_ai2_time
    global _total_moves

    g.set_ais()

    while not hasattr(g.players[0], "won"):

        t = time()
        action = g.players[0].ai.select_action(g)

        if g.players[0].ai_name == ai1:
            _total_ai1_time += time() - t

        if g.players[0].ai_name == ai2:
            _total_ai2_time += time() - t

        _total_moves += 1

        if action:
            g = perform_action(action, g)
        else:
            g.turn_shift()

        if hasattr(g.players[0], "extra_action"):
            extra_action = g.players[0].ai.select_action(g)
            g = perform_action(extra_action, g)

    return g.players[0].ai_name


def new_game(player1_ai, player2_ai):

    player1, player2 = Player("Green"), Player("Red")

    player1.ai_name, player2.ai_name = player1_ai, player2_ai

    player1_units, player2_units = setup.get_start_units()

    gamestate = Gamestate(player1, player1_units, player2, player2_units)

    gamestate.initialize_turn()
    gamestate.initialize_action()

    gamestate.set_actions_remaining(1)

    return run_game(gamestate)


winners = []

ai1 = sys.argv[1]
ai2 = sys.argv[2]
matchco = int(sys.argv[3])

for match in range(matchco):
    print "Match", match + 1
    winners.append(new_game(ai1, ai2))
    winners.append(new_game(ai2, ai1))

print
print "Score:"
print ai1, winners.count(ai1)
print ai2, winners.count(ai2)
print
print "Average time per move:"
print ai1, round(_total_ai1_time * 2 / _total_moves, 3)
print ai2, round(_total_ai2_time * 2 / _total_moves, 3)

