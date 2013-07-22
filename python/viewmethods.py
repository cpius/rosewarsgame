from __future__ import division
import pygame
import textwrap
import colors
import settings


zoom = settings.zoom
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
        image = pygame.transform.scale(image, (int(image.get_size()[0] * zoom),
                                               int(image.get_size()[1] * zoom)))
        _image_library[path] = image
    return image


def write(screen, message, location, font, color=colors.black):
    label = font.render(message, _anti_alias, color)
    screen.blit(label, location)


def write_message(screen, interface, message):
    write(screen, message, interface.message_location, interface.fonts["normal"])


def split_lines(lines, line_length):
    new_lines = []
    for line in lines:
        if line:
            split_lines = textwrap.wrap(line, line_length)
        else:
            split_lines = [""]
        for split_line in split_lines:
            new_lines.append(split_line)
    return new_lines


def get_unit_pic(interface, name):
    return "./" + interface.unit_folder + "/" + name.replace(" ", "_") + ".jpg"


def draw_rectangle(screen, dimensions, location, color):
    rectangle = pygame.Surface(dimensions, pygame.SRCALPHA, 32)
    rectangle.fill(color)
    screen.blit(rectangle, location)


def draw_unit_box(screen, interface, base, color, resize=1):

    def scale_rectangle(corners, pixels):

        corner1 = (corners[0][0] - pixels, corners[0][1] - pixels)
        corner2 = (corners[1][0] + pixels, corners[1][1] - pixels)
        corner3 = (corners[2][0] + pixels, corners[2][1] + pixels)
        corner4 = (corners[3][0] - pixels, corners[3][1] + pixels)

        return [corner1, corner2, corner3, corner4]

    height = interface.unit_height * resize
    width = interface.unit_width * resize

    if color == "Red":
        border_color = interface.red_player_color
    else:
        border_color = interface.green_player_color

    corner1 = (base[0], base[1])
    corner2 = (base[0] + width, base[1])
    corner3 = (base[0] + width, base[1] + height)
    corner4 = (base[0], base[1] + height)

    base_corners = [corner1, corner2, corner3, corner4]

    inner_corners = scale_rectangle(base_corners, -1)

    pygame.draw.lines(screen, colors.black, True, inner_corners)

    thickness = int(5 * zoom * resize)

    for i in range(thickness):
        middle_corners = scale_rectangle(base_corners, i)
        pygame.draw.lines(screen, border_color, True, middle_corners)

    outer_corners = scale_rectangle(base_corners, thickness)
    pygame.draw.lines(screen, colors.black, True, outer_corners)


