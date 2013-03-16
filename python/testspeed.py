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

    g = gamestate.Gamestate(player1, player1_units, player2, player2_units, 1, 2)

    g.initialize_turn()
    g.initialize_action()

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


def load_gamestates(saved_g):
    for i in range(10000):
        gamestate.load_gamestate(saved_g)


def get_many_actions():
    for i in range(1000):
        g.get_actions()


def profiling(function_string):

    cProfile.run(function_string, "./saves/foo")

    p = pstats.Stats('./saves/foo')
    p.strip_dirs()
    p.sort_stats("cumulative")
    p.print_stats()


g = make_gamestate()

g.set_ais()


profiling("g.players[0].ai.select_action(g)")

