import methods
import view as view_module
import json
import pygame
from pygame.locals import *
from gamestate_module import Gamestate
from game import Game
from player import Player

gamestate = Gamestate.from_file("./tutorial/tutorial_1.gamestate")

marked_tiles = [methods.position_to_tuple(position) for position in
                json.loads(open("./tutorial/tutorial_1.marked").read())["tiles"]]

text = open("./tutorial/tutorial_1.txt").readline()

print text

players = [Player("Green", "Human"), Player("Red", "Human")]

game = Game(players, gamestate)

view = view_module.View()

view.draw_tutorial(game)

view.shade_positions(marked_tiles)

view.draw_message(text)


cont = True
while cont:
    for event in pygame.event.get():
        if event.type == QUIT:
            cont = False
            break
