from common import *
import json
from pygame.locals import *
from gamestate import Gamestate
from game import Game
from player import Player
import os
from action import Action
import units as units_module
import outcome
from viewcommon import *
import sys


shading_blue = pygame.Color(*[0, 0, 100, 160])
shading_red = pygame.Color(*[100, 0, 0, 160])


def draw_scenario(view, path, number, total):
    if os.path.exists(path + "Gamestate.json"):
        gamestate = Gamestate.from_file(path + "Gamestate.json")
    else:
        gamestate = Gamestate({}, {}, 2)

    players = [Player("Green", "Human"), Player("Red", "Human")]
    game = Game(players, gamestate)
    view.draw_game_tutorial(game)
    view.draw_tutorial_page_number(number, total)

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
                    return menu[i]


def get_menu_choice(view, folder):

    menu = [x[1] for x in os.walk(folder)][0]
    return menu_choice(view, menu)


def show_scenarios(view, folder):
    scenarios = [walk[0] + "/" for walk in os.walk(folder)][1:]
    index = 0
    draw_scenario(view, scenarios[index], index + 1, len(scenarios))
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
            draw_scenario(view, scenarios[index], index + 1, len(scenarios))

        if move_backward_requested(event) and index > 0:
            index -= 1
            draw_scenario(view, scenarios[index], index + 1, len(scenarios))


def run_tutorial_10(view):
    base_folder = "./../rulebook_1.0/"
    choice = get_menu_choice(view, base_folder)
    if choice != "quit":
        folder = base_folder + choice + "/"
        show_scenarios(view, folder)


def show_upgrade_list(view, unit):
    view.show_upgrades_tutorial(unit.upgrades)


def show_upgrades(view, folder):
    unit = menu_choice(view, sorted([unit for unit in Unit.name.values()]))
    gamestate = Gamestate.from_file(folder + "/Gamestate.json")
    gamestate.player_units["C2"] = unit
    unit = getattr(units_module, unit.replace(" ", "_"))()
    view.show_unit_zoomed_tutorial(unit, None)
    show_upgrade_list(view, unit)

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


def run_tutorial_11(view):
    base_folder = "./../rulebook_1.1/"
    choice = get_menu_choice(view, base_folder)

    if choice != "quit":
        folder = base_folder + choice + "/"
        if choice == "6. Special Rules":
            choice = get_menu_choice(view, folder)
            folder += choice + "/"
            show_scenarios(view, folder)
        elif choice == "5. Upgrades":
            show_upgrades(view, folder)
        else:
            show_scenarios(view, folder)


def run_tutorial(view):

    if get_setting("version") == "1.0":
        run_tutorial_10(view)
    else:
        run_tutorial_11(view)


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
