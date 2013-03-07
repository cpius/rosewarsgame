import setup
import mover
from time import time
import gamestate as g
import cProfile
import main


def get_p():

    p = setup.get_start_units()
    p[0].ai_name = "Advancer"
    p[1].ai_name = "Destroyer"
    p[0].actions_remaining = 1
    p[1].actions_remaining = 2
    
    return p


def time_get_actions(p):

    t = time()
    for i in range(10):
        mover.get_actions(p)
        
    return (time() - t) * 100


def time_do_action(action, p):

    t = time()
    for i in range(1000):
        p_copy = g.copy_p(p)
        mover.do_action(action, p_copy)
    t = time() - t

    t_copy = time()
    for i in range(1000):
        p_copy = g.copy_p(p)
    t_copy = time() - t_copy

    t -= t_copy

    return t


def time_copy_p(p):
    t = time()
    for i in range(1000):
        g.copy_p(p)

    return time() - t

def time_save_gamestate(p):
    t = time()
    for i in range(1000):
        g.save_gamestate(p)

    return time() - t


def time_load_gamestate(gamestate):
    t = time()
    for i in range(1000):
        g.load_gamestate(gamestate)

    return time() - t


def time_copy_action(action):
    t = time()
    for i in range(1000):
        g.copy_action(action)

    return time() - t




p = get_p()

#game_state = g.save_game_state(p)

#p = g.load_game_state(game_state)

g.write_gamestate(p, "./replay/save1.txt")

p = g.read_gamestate("./replay/save1.txt")

for pos, unit in p[0].units.items():
    print pos, unit, p[0].color

print
for pos, unit in p[1].units.items():
    print pos, unit, p[1].color

print p[0].backline
print p[1].backline

main.run_game(p)








"""

p_copy = g.copy_p(p)

actions = mover.get_actions(p)

gamestate = g.save_gamestate(p)

print time_get_actions(p)

print actions[3].__dict__

print time_copy_action(actions[0])

"""
