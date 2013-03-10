from __future__ import division
import gamestate_module as gamestate
import settings
import setup
from time import time
import copy
from player import Player
import pickle
import pstats
import cProfile


def make_gamestate():
    player1, player2 = Player("Green"), Player("Red")

    player1.ai_name, player2.ai_name = settings.player1_ai, settings.player2_ai

    player1_units, player2_units = setup.get_start_units()

    g = gamestate.Gamestate(player1, player1_units, player2, player2_units)

    g.initialize_turn()
    g.initialize_action()

    player1.actions_remaining = 2
    player2.actions_remaining = 0

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
    return "Select action", ai_name, round((time() - t) * 100, 5)


def run_five_saves():
    for i in range(5):
        g = pickle.load(open("./saves/save" + str(i) + ".pickle", 'rb'))
        g.players[0].ai_name = "Evaluator"
        g.players[1].ai_name = "Human"
        g.set_ais()

        g.players[0].ai.select_action(g)


def load_gamestates():
    for i in range(10000):
        gamestate.load_gamestate(saved_g)


def profiling(function_string):

    cProfile.run(function_string, "foo")

    p = pstats.Stats('foo')
    p.strip_dirs()
    p.sort_stats("cumulative")
    p.print_stats()


g = make_gamestate()
saved_g = gamestate.save_gamestate(g)

profiling("gamestate.load_gamestate(saved_g)")


