from common import *
import view as view_module
import json
import pygame
from pygame.locals import *
from gamestate import Gamestate
from game import Game
from player import Player
import os
import viewinfo

shading_blue = pygame.Color(0, 0, 100, 160)
shading_red = pygame.Color(100, 0, 0, 160)


def run_tutorial():
    with open("./tutorial/list.txt") as file:
        scenarios = [line.split(": ") for line in file]

    for scenario in scenarios:
        if scenario[1].strip() == "Move":
            path = "./tutorial/" + scenario[0] + "/"

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
            print "de", description
            view.draw_tutorial_message(description)

            cont = True
            while cont:
                for event in pygame.event.get():
                    if event.type == pygame.MOUSEBUTTONDOWN:
                        cont = False
                        break

if __name__ == "__main__":
    run_tutorial()