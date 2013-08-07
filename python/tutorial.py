from common import *
import view as view_module
import json
import pygame
from pygame.locals import *
from gamestate import Gamestate
from game import Game
from player import Player
import os
import units as units_module

shading_blue = pygame.Color(*[0, 0, 100, 160])
shading_red = pygame.Color(*[100, 0, 0, 160])
view = view_module.View()


def draw_gamestate(path):
    gamestate = Gamestate.from_file(path + "Gamestate.json")
    players = [Player("Green", "Human"), Player("Red", "Human")]
    game = Game(players, gamestate)
    view.draw_tutorial(game)


def draw_marked(path):
    marked_blue = [Position.from_string(position) for position in
                   json.loads(open(path + "Marked_blue.marked").read())["tiles"]]
    view.shade_positions(marked_blue, shading_blue)

    if os.path.exists(path + "Marked_red.marked"):
        marked_red = [Position.from_string(position) for position in
                      json.loads(open(path + "Marked_red.marked").read())["tiles"]]
        view.shade_positions(marked_red, shading_red)


def draw_description(path):
    description = open(path + "Description.txt").readlines()
    view.draw_tutorial_message(description)


def draw_empty_gamestate():
    gamestate = Gamestate({}, {}, 2)
    players = [Player("Green", "Human"), Player("Red", "Human")]
    game = Game(players, gamestate)
    view.draw_tutorial(game)


def draw_unit(path):
    unit_name = open(path + "Unit.txt").readline()
    unit = getattr(units_module, unit_name.replace(" ", "_"))()
    view.show_unit_zoomed(unit)
    description = open(path + "Description.txt").readlines()
    view.draw_tutorial_message(description, 550)


def run_tutorial():
    if use_list:
        with open("./tutorial/list.txt") as file:
            scenarios = [line.split(": ") for line in file]
    else:
        scenarios = [["Unit_1", "Unit"]]

    exit = False
    index = 0

    while index < len(scenarios) and not exit:
        if scenarios[index][1].strip() == "Move":
            path = "./tutorial/" + scenarios[index][0] + "/"

            draw_gamestate(path)
            draw_marked(path)
            draw_description(path)

        elif scenarios[index][1].strip() == "Unit":
            path = "./tutorial/" + scenarios[index][0] + "/"

            draw_empty_gamestate()
            draw_unit(path)

        while True:
            event = pygame.event.wait()

            if move_forward_requested(event):
                break
            elif move_backward_requested(event):
                index -= 2
                break
            elif quit_game_requested(event):
                exit = True
                break

        index += 1


def quit_game_requested(event):
    return event.type == QUIT or (event.type == KEYDOWN and command_q_down(event.key))


def command_q_down(key):
    return key == K_q and (pygame.key.get_mods() & KMOD_LMETA or pygame.key.get_mods() & KMOD_RMETA)


def move_forward_requested(event):
    return (event.type == pygame.MOUSEBUTTONDOWN and event.button == 1) or \
           (event.type == pygame.KEYDOWN and event.key == pygame.K_RIGHT)


def move_backward_requested(event):
    return (event.type == pygame.MOUSEBUTTONDOWN and event.button == 6) or \
           (event.type == pygame.KEYDOWN and event.key == pygame.K_LEFT)

if __name__ == "__main__":
    use_list = True
    run_tutorial()
