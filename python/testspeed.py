from __future__ import division
import gamestate_module as gamestate
import settings
import setup
from time import time
import copy
from player import Player


def make_gamestate():
    player1, player2 = Player("Green"), Player("Red")

    player1.ai_name, player2.ai_name = settings.player1_ai, settings.player2_ai

    player1_units, player2_units = setup.get_start_units()

    g = gamestate.Gamestate(player1, player1_units, player2, player2_units)

    g.initialize_turn()
    g.initialize_action()

    player1.actions_remaining = 2
    player2.actions_remaining = 0

    g.set_ais()

    return g


def timer(function, *args):

    t = time()
    for i in range(100):
        function(*args)
    return function.__name__, round((time() - t) * 10, 5)


def time_ai(ai_name, g):
    g.players[0].ai_name = ai_name
    g.players[1].ai_name = "Human"
    g.set_ais()

    t = time()
    for i in range(10):
        g.players[0].ai.select_action(g)
    return "Select action", ai_name, round((time() - t)*100, 5)


g = make_gamestate()
saved_g = gamestate.save_gamestate(g)


print timer(copy.deepcopy, g)
print timer(g.copy)
print timer(gamestate.load_gamestate, saved_g)
print timer(gamestate.save_gamestate, g)
print timer(g.get_actions)

g.players[0].ai.select_action(g)


print time_ai("Destroyer", g)

print time_ai("Advancer", g)

print time_ai("Evaluator", g)

