from __future__ import division
import pygame
import textwrap
import interface_settings as settings
from common import *
from pygame.locals import *


class Location(object):
    def __init__(self, x, y, zoom):
        self.x = x
        self.y = y
        self.zoom = zoom

    def adjust(self, x, y):
        return Location(self.x + x * self.zoom, self.y + y * self.zoom, self.zoom)

    @property
    def tuple(self):
        return self.x, self.y


class Color:
    Black = (0, 0, 0)
    White = (255, 255, 255)
    Green = (0, 255, 0)
    Red = (255, 0, 0)
    Blue = (0, 0, 255)
    Light_blue = (20, 70, 255)
    Brown = (128, 64, 0)
    Grey = (48, 48, 48)
    Yellow = (200, 200, 0)
    Light_grey = (240, 240, 240)
    Medium_grey = (150, 150, 150)
    Dark_grey = (60, 60, 60)
    Dark_green = (60, 113, 50)
    Dark_red = (204, 0, 16)
    Gold = (150, 130, 15)
    Dull_red = (190, 55, 55)
    Dodger_blue = (30, 144, 255)


_anti_alias = True
_image_library = {}


def show_lines(screen, lines, line_length, line_distance, font, x, y):

    lines = split_lines(lines, line_length)

    i = 0
    for line in lines:
        i += 1
        line_y = y + i * line_distance
        write(screen, line, (x, line_y), font)


def get_image(path, dimensions=None):
    global _image_library

    if dimensions:
        image = pygame.image.load(path).convert()
        return pygame.transform.scale(image, dimensions)

    image = _image_library.get(path)
    if not image:
        image = pygame.image.load(path).convert()
        image = pygame.transform.scale(image, (int(image.get_size()[0] * settings.zoom),
                                               int(image.get_size()[1] * settings.zoom)))
        _image_library[path] = image
    return image


def write(screen, message, location, font, color=Color.Black):
    label = font.render(message, _anti_alias, color)
    screen.blit(label, location)


def write_message(screen, interface, message):
    write(screen, message, interface.message_location, interface.fonts["normal"])


def split_lines(lines, line_length):
    new_lines = []
    for line in lines:
        if line == "" or line == "\n":
            split_lines = [""]
        else:
            split_lines = textwrap.wrap(line, line_length)
        for split_line in split_lines:
            new_lines.append(split_line)

    return new_lines


def get_unit_pic(interface, unit):
    return "./" + interface.unit_folder + "/" + unit.name.replace(" ", "_") + ".jpg"


def draw_rectangle(screen, dimensions, location, color):
    rectangle = pygame.Surface(dimensions, pygame.SRCALPHA, 32)
    rectangle.fill(color)
    screen.blit(rectangle, location)


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
    return event.type == QUIT or (event.type == KEYDOWN and command_q_down(event.key))


def command_q_down(key):
    return key == K_q and (pygame.key.get_mods() & KMOD_LMETA or pygame.key.get_mods() & KMOD_RMETA)

