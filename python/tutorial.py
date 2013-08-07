from common import *
import view as view_module
import json
import pygame
from pygame.locals import *
from gamestate import Gamestate
from game import Game
from player import Player
import os

shading_blue = pygame.Color(0, 0, 100, 160)
shading_red = pygame.Color(100, 0, 0, 160)


def run_tutorial():
    if use_list:
        with open("./tutorial/list.txt") as file:
            scenarios = [line.split(": ") for line in file]
    else:
        scenarios = [["Moves_3", "Move"]]

    exit = False
    index = 0
    while index < len(scenarios) and not exit:
        if scenarios[index][1].strip() == "Move":
            path = "./tutorial/" + scenarios[index][0] + "/"

            gamestate = Gamestate.from_file(path + "Gamestate.json")
            players = [Player("Green", "Human"), Player("Red", "Human")]
            game = Game(players, gamestate)
            view = view_module.View()
            view.draw_tutorial(game)

            marked_blue = [Position.from_string(position) for position in
                           json.loads(open(path + "Marked_blue.marked").read())["tiles"]]
            view.shade_positions(marked_blue, shading_blue)

            if os.path.exists(path + "Marked_red.marked"):
                marked_red = [Position.from_string(position) for position in
                              json.loads(open(path + "Marked_red.marked").read())["tiles"]]
                view.shade_positions(marked_red, shading_red)

            description = open(path + "Description.txt").readlines()
            view.draw_tutorial_message(description)

            while True:
                event = pygame.event.wait()

                if event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 1:
                        break
                    elif event.button == 3:
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


if __name__ == "__main__":
    use_list = True
    run_tutorial()
