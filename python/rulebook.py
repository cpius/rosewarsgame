from common import *
import view as view_module
import json
from pygame.locals import *
from gamestate import Gamestate
from game import Game
from player import Player
import os
from action import Action
import units as units_module
import outcome
from glob import glob
from viewcommon import *
import sys


shading_blue = pygame.Color(*[0, 0, 100, 160])
shading_red = pygame.Color(*[100, 0, 0, 160])


def draw_gamestate(view, path):
    print path
    if os.path.exists(path + "Gamestate.json"):
        gamestate = Gamestate.from_file(path + "Gamestate.json")
    else:
        gamestate = Gamestate({}, {}, 2)

    players = [Player("Green", "Human"), Player("Red", "Human")]
    game = Game(players, gamestate)
    view.draw_game_tutorial(game)

    if os.path.exists(path + "Blue.marked"):
        marked_blue = [Position.from_string(position) for position in
                       json.loads(open(path + "Blue.marked").read())["tiles"]]
        view.shade_positions(marked_blue, shading_blue)

    if os.path.exists(path + "Red.marked"):
        marked_red = [Position.from_string(position) for position in
                      json.loads(open(path + "Red.marked").read())["tiles"]]
        view.shade_positions(marked_red, shading_red)

    if os.path.exists(path + "Unit.txt"):
        unit_name = open(path + "Unit.txt").readline()
        unit = getattr(units_module, unit_name.replace(" ", "_"))()
        view.show_unit_zoomed_tutorial(unit, None)
        draw_unit = True
    else:
        draw_unit = False

    if os.path.exists(path + "Description.txt"):
        description = open(path + "Description.txt").readlines()
        view.draw_tutorial_message(description, draw_unit)


def draw_action(view, path):

    rolls = outcome.Outcome()
    rolls.set_suboutcome(Position(3, 7), outcome.rolls(2, 1))

    gamestate = Gamestate.from_file(path + "Gamestate.json")
    units = gamestate.all_units()
    action = Action.from_document(units, json.loads(open(path + "Action.json").read()))
    view.draw_action_tutorial(action, rolls)


def menu_choice(view, menu):

    view.draw_help_menu(menu)

    while 1:
        event = pygame.event.wait()

        if quit_game_requested(event):
            sys.exit()

        if event.type == pygame.MOUSEBUTTONDOWN:
            if within(event.pos, view.interface.help_area):
                return "quit"

        if event.type == pygame.MOUSEBUTTONDOWN:
            for i in range(len(menu)):
                if within(event.pos, view.interface.help_menu[i]):
                    return i


def run_tutorial(view):

    menu = ["-General rules-", "Overview", "Movement", "Battle", "Basic Units", "",
            "-Examples and special cases-"]
    for path in glob("./../rulebook_1.0/*/*"):
        item = os.path.split(os.path.split(path)[0])[1]
        if item not in menu:
            menu.append(item)

    index = menu_choice(view, menu)

    if index != "quit":

        path = "./../rulebook_1.0/" + menu[index]
        scenarios = [walk[0] + "/" for walk in os.walk(path)][1:]
        index = 0
        draw_gamestate(view, scenarios[index])
        while 1:
            event = pygame.event.wait()

            if event.type == pygame.MOUSEBUTTONDOWN:
                if within(event.pos, view.interface.help_area):
                    break

            if event.type == pygame.MOUSEBUTTONDOWN:
                if within(event.pos, view.interface.to_help_menu_area):
                    run_tutorial(view)
                    break

            if quit_game_requested(event):
                sys.exit()

            if move_forward_requested(event) and len(scenarios) > index + 1:
                index += 1
                draw_gamestate(view, scenarios[index])

            if move_backward_requested(event) and index > 0:
                index -= 1
                draw_gamestate(view, scenarios[index])


def quit_game_requested(event):
    return event.type == QUIT or (event.type == KEYDOWN and command_q_down(event.key))


def command_q_down(key):
    return key == K_q and (pygame.key.get_mods() & KMOD_LMETA or pygame.key.get_mods() & KMOD_RMETA)


def move_forward_requested(event):
    return (event.type == pygame.MOUSEBUTTONDOWN and event.button == 1) or \
           (event.type == pygame.KEYDOWN and event.key == pygame.K_RIGHT)


def move_backward_requested(event):
    return (event.type == pygame.MOUSEBUTTONDOWN and event.button == 3) or \
           (event.type == pygame.KEYDOWN and event.key == pygame.K_LEFT)
