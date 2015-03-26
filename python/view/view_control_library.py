import pygame
from gamestate.gamestate_library import *


def get_position_from_mouseclick(interface, coordinates):
    x = int((coordinates[0] - interface.x_border) /
           (interface.unit_width + interface.unit_padding_width)) + 1
    if coordinates[1] > interface.board_size[1] / 2:
        y = 8 - int((coordinates[1] - interface.y_border_bottom) /
                    (interface.unit_height + interface.unit_padding_height))
    else:
        y = 8 - int((coordinates[1] - interface.y_border_top) /
                    (interface.unit_height + interface.unit_padding_height))
    return Position(x, y)


def within(point, area):
    return area[0].y <= point[1] <= area[1].y and area[0].x <= point[0] <= area[1].x


def quit_game_requested(event):
    return event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and command_q_down(event.key))


def command_q_down(key):
    return key == pygame.K_q and (pygame.key.get_mods() & pygame.KMOD_LMETA or pygame.key.get_mods() & pygame.KMOD_RMETA)

