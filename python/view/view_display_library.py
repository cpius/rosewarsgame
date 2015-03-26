import pygame
import textwrap
import view.interface_settings as settings


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
