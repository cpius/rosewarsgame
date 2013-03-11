from __future__ import division
import pygame, sys
from pygame.locals import *
import setup
import mover
import math
import os
import ai_module
import settings
import units



def perform_action(action, p):

    if hasattr(p[0], "extra_action"):
        all_actions = mover.get_extra_actions(p)
    else:
        all_actions = mover.get_actions(p)

    mover.do_action(action, p)

    if hasattr(p[0], "won"):
        print p[0].color, "won"
        return p, True
    else:
        game_ended = False

    p[0].ai.add_counters(p)
        
    
    if hasattr(p[0], "extra_action"):
        del p[0].extra_action
    else:
        all_extra_actions = mover.get_extra_actions(p)
        if len(all_extra_actions) > 1:
            p[0].extra_action = True
    
    mover.initialize_action(p)
    
    if (p[0].actions_remaining < 1 or len(all_actions) == 1) and not hasattr(p[0], "extra_action"):
        p = [p[1], p[0]]
        mover.initialize_turn(p)

    if hasattr(p[0], "extra_action"):
        print p[0].color, "extra action"
    else:
        print p[0].color  

    return p, game_ended


def game_end(player):
    print "game ended"
    

def run_game():
    
    p = setup.get_start_units()
    
    p[0].ai = ai_module.AI(settings.player1_ai)
    p[1].ai = ai_module.AI(settings.player2_ai)
    
    mover.initialize_turn([p[0], p[1]])
    mover.initialize_turn([p[1], p[0]])
    mover.initialize_action(p)

   
    p[0].actions_remaining = 1
    print p[0].color
    startpos, endpos = None, None
    game_ended = False

    while not game_ended:
        
        action = p[0].ai.select_action(p)
        if action:
            p, game_ended = perform_action(action, p)
            
        if hasattr(p[0], "extra_action"):
            extra_action = p[0].ai.select_action(p)
            p, game_ended = perform_action(extra_action, p)
                           
                           
run_game() 