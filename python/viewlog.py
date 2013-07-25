from __future__ import division
from viewmethods import colors
import pygame
import battle
import settings
import viewmethods as m

zoom = settings.zoom
maximum_logs = 5
base_height = 48


class Log():
    def __init__(self, action, outcome, turn, action_number, player_color):
        self.action = action
        self.outcome = outcome
        self.turn = turn
        self.action_number = action_number
        self.player_color = player_color

    def get_next(self):
        if self.action_number == 1:
            return self.player_color, 1
        else:
            if self.player_color == "Red":
                player_color = "Green"
            else:
                player_color = "Red"
            return player_color, 2


def draw_log(logbook, screen, interface, action=None, outcome=None, game=None):

    if action:
        log = Log(action, outcome, game.turn, game.gamestate.get_actions_remaining(), game.current_player().color)
        logbook.append(log)

    if len(logbook) > maximum_logs:
        logbook.pop(0)

    log_heights = base_height * zoom

    pygame.draw.rect(screen, colors["light_grey"], interface.right_side_rectangle)

    for index, log in enumerate(logbook):

        action = log.action
        outcome = log.outcome
        base_x = int(391 * zoom)
        base_y = int(index * log_heights)
        base = (base_x, base_y)

        draw_turn_box(screen, interface, log.player_color, log.action_number, *base)

        line_thickness = int(3 * zoom)
        line_start = (base_x, base_y + log_heights - line_thickness / 2)
        line_end = (int(interface.board_size[1] * zoom), base_y + log_heights - line_thickness / 2)
        pygame.draw.line(screen, colors["black"], line_start, line_end, line_thickness)

        symbol_location = (base_x + 118 * zoom, base_y + 10 * zoom)

        if action.is_attack():
            draw_attack(screen, interface, action, outcome, base, symbol_location, log)

        elif action.is_ability():

            pic = m.get_image(interface.ability_icon)
            screen.blit(pic, symbol_location)

            if log.player_color == "Green":
                draw_unit_right(screen, interface, action, "Green", 0, *base)
                draw_unit_right(screen, interface, action, "Red", 1, *base)
            elif log.player_color == "Red":
                draw_unit_right(screen, interface, action, "Red", 0, *base)
                draw_unit_right(screen, interface, action, "Green", 1, *base)

        else:
            pic = m.get_image(interface.move_icon)
            screen.blit(pic, symbol_location)

            if log.player_color == "Green":
                draw_unit_right(screen, interface, action, "Green", 0, *base)
            elif log.player_color == "Red":
                draw_unit_right(screen, interface, action, "Red", 0, *base)

    base_x = int(391 * zoom)
    base_y = int(len(logbook) * log_heights)
    base = (base_x, base_y)

    if logbook:
        color, action_number = logbook[-1].get_next()
    else:
        color, action_number = "Green", 1
    draw_turn_box(screen, interface, color, action_number - 1, *base)

    base_x = int(391 * zoom)
    base_y = int(len(logbook) * log_heights)
    base = (base_x, base_y)

    if logbook:
        color, action_number = logbook[-1].get_next()
    else:
        color, action_number = "Green", 1
    draw_turn_box(screen, interface, color, action_number - 1, *base)

    return logbook


def draw_attack(screen, interface, action, outcome, base, symbol_location, log):

    outcome_string = battle.get_outcome(action, outcome)

    draw_outcome(screen, interface, outcome_string, *base)

    pic = m.get_image(interface.attack_icon)
    screen.blit(pic, symbol_location)

    if log.player_color == "Green":
        draw_unit_right(screen, interface, action, "Green", 0, *base)
        draw_unit_right(screen, interface, action, "Red", 1, *base)
    elif log.player_color == "Red":
        draw_unit_right(screen, interface, action,  "Red", 0, *base)
        draw_unit_right(screen, interface, action, "Green", 1, *base)


def draw_unit_right(screen, interface, action, color, index, base_x, base_y):

    if not action.is_attack():
        unit = action.unit_reference
    elif index == 0:
        unit = action.unit_reference
    else:
        unit = action.target_reference

    unit_height = int((base_height - 10) * zoom)
    unit_width = int((interface.unit_width / interface.unit_height) * unit_height)

    location = (base_x + (65 + index * 100) * zoom, base_y + 4 * zoom)
    unit_pic = m.get_unit_pic(interface, unit.image)
    unit_image = m.get_image(unit_pic, (unit_width, unit_height))

    screen.blit(unit_image, location)

    draw_unit_box(screen, interface, location, color, unit_height, unit_width)


def draw_turn_box(screen, interface, color, action_number, base_x, base_y):
    box_width, box_height = 40 * zoom, (base_height - 2) * zoom
    position_and_size = (base_x, base_y, box_width, box_height)

    if color == "Green":
        border_color = interface.green_player_color
    else:
        border_color = interface.red_player_color

    pygame.draw.rect(screen, border_color, position_and_size)

    current_action = 2 - action_number
    location = (base_x + 7 * zoom, base_y)
    m.write(screen, str(current_action), location, interface.fonts["big"])


def draw_unit_box(screen, interface, base, color, height, width):

    def scale_rectangle(corners, pixels):

        corner1 = (corners[0][0] - pixels, corners[0][1] - pixels)
        corner2 = (corners[1][0] + pixels, corners[1][1] - pixels)
        corner3 = (corners[2][0] + pixels, corners[2][1] + pixels)
        corner4 = (corners[3][0] - pixels, corners[3][1] + pixels)

        return [corner1, corner2, corner3, corner4]

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

    pygame.draw.lines(screen, colors["black"], True, inner_corners)

    resize = height / (interface.unit_height * zoom)
    thickness = int(5 * zoom * resize)

    for i in range(thickness):
        middle_corners = scale_rectangle(base_corners, i)
        pygame.draw.lines(screen, border_color, True, middle_corners)

    outer_corners = scale_rectangle(base_corners, thickness)
    pygame.draw.lines(screen, colors["black"], True, outer_corners)


def draw_outcome(screen, interface, outcome, base_x, base_y):
    location = (base_x + 230 * zoom, base_y + 5 * zoom)
    m.write(screen, outcome, location, interface.fonts["big"])

