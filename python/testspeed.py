from __future__ import division
from gamestate_module import Gamestate
import settings
import setup
from time import time
from player import Player
import pstats
import cProfile
import saver


def make_gamestate():
    player1, player2 = Player("Green"), Player("Red")

    player1.ai_name = "Evaluator"
    player2.ai_name = "Human"

    player1_units, player2_units = setup.get_start_units()

    gamestate = Gamestate(player1, player1_units, player2, player2_units, 1, 2)

    gamestate.initialize_turn()
    gamestate.initialize_action()

    return gamestate


def timer(function, *args):

    t = time()
    for i in range(100):
        function(*args)
    return function.__name__, round((time() - t) * 10, 5)


def time_ai(ai_name, gamestate):
    gamestate.current_player().ai_name = ai_name
    gamestate.players[1].ai_name = "Human"
    gamestate.set_ais()

    t = time()
    for i in range(10):
        gamestate.current_player().ai.select_action(gamestate)
    return "Select action", ai_name, round((time() - t) * 100, 5)


def load_gamestates(saved_gamestate):
    for i in range(10000):
        saver.load_gamestate(saved_gamestate)


def get_many_actions():
    for i in range(1000):
        gamestate.get_actions()


def profiling(function_string):

    cProfile.run(function_string, "./saves/foo")

    p = pstats.Stats('./saves/foo')
    p.strip_dirs()
    p.sort_stats("cumulative")
    p.print_stats()


gamestate = make_gamestate()

gamestate.set_ais()


profiling("gamestate.current_player().ai.select_action(gamestate)")
