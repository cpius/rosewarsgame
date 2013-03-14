from __future__ import division
from player import Player
from gamestate_module import Gamestate
import setup
import settings


def perform_action(action, g):

    all_actions = g.get_actions()

    matchco = 0
    for possible_action in all_actions:
        if action == possible_action:
            matchco += 1
            action = possible_action

    if matchco == 1:

        g.do_action(action)

        if settings.show_full_battle_result:
            print action.full_string()
        else:
            print action.string_with_outcome()
        print

        g.players[0].ai.add_counters(g)

        g.initialize_action()

        if (g.players[0].actions_remaining < 1 or len(all_actions) == 1) and not hasattr(g.players[0], "extra_action"):
            g.turn_shift()

    return g


def run_game(g):

    g.set_ais()

    while not hasattr(g.players[0], "won"):

        print g.turn, 3 - g.players[0].actions_remaining
        print g.players[0].color

        action = g.players[0].ai.select_action(g)
        if action:
            g = perform_action(action, g)
        else:
            g.turn_shift()

        if hasattr(g.players[0], "extra_action"):
            extra_action = g.players[0].ai.select_action(g)
            g = perform_action(extra_action, g)

    print g.players[0].color, "won in turn", g.turn


def new_game():

    player1, player2 = Player("Green"), Player("Red")

    player1.ai_name, player2.ai_name = "Advancer", "Advancer"

    player1_units, player2_units = setup.get_start_units()

    gamestate = Gamestate(player1, player1_units, player2, player2_units)

    gamestate.initialize_turn()
    gamestate.initialize_action()

    player1.actions_remaining = 1
    player2.actions_remaining = 0

    run_game(gamestate)


new_game()