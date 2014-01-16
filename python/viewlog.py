from __future__ import division
from viewcommon import *
import pygame
import interface_settings as settings


zoom = settings.zoom
maximum_logs = 5
base_height = 48


class Log():
    def __init__(self, action, outcome_string, action_number, player_color):
        self.action = action
        self.outcome_string = outcome_string
        self.action_number = action_number
        self.player_color = player_color

    def get_next(self):
        if self.action_number == 1:
            return self.player_color, 2
        else:
            if self.player_color == "Red":
                player_color = "Green"
            else:
                player_color = "Red"
            return player_color, 1


def draw_log(logbook, screen, interface, game, action=None, outcome=None):
    player_color = game.current_player().color
    action_number = 3 - game.gamestate.get_actions_remaining()
    if action:
        if game.gamestate.action_count == 0:
            action_number -= 1

        if action.is_attack():
            for position in outcome.outcomes:
                outcome_string = action.outcome_string(outcome.for_position(position), game.gamestate)
                modified_action = action.copy()
                modified_action.target_at = position
                modified_action.target_unit = game.gamestate.enemy_units[position]
                log = Log(modified_action, outcome_string, action_number, player_color)
                logbook.append(log)
        else:
            log = Log(action, None, action_number, player_color)
            logbook.append(log)

    if len(logbook) > maximum_logs:
        logbook.pop(0)

    log_heights = base_height * zoom

    pygame.draw.rect(screen, colors["light_grey"], interface.right_side_rectangle)

    for index, log in enumerate(logbook):

        base_x = int(391 * zoom)
        base_y = int(index * log_heights)
        base = (base_x, base_y)

        draw_turn_box(screen, interface, log.player_color, log.action_number, *base)

        line_thickness = int(3 * zoom)
        line_start = (base_x, base_y + log_heights - line_thickness / 2)
        line_end = (int(interface.board_size[1] * zoom), base_y + log_heights - line_thickness / 2)
        pygame.draw.line(screen, colors["black"], line_start, line_end, line_thickness)

        symbol_location = (base_x + 118 * zoom, base_y + 8 * zoom)

        if log.action.is_attack():
            draw_attack(screen, interface, log.action, log.outcome_string, base, symbol_location, log)

        elif log.action.is_ability():
            pic = get_image(interface.ability_icon)
            screen.blit(pic, symbol_location)

            if log.player_color == "Green":
                draw_unit_right(screen, interface, log.action, "Green", 0, *base)
                draw_unit_right(screen, interface, log.action, "Red", 1, *base)
            elif log.player_color == "Red":
                draw_unit_right(screen, interface, log.action, "Red", 0, *base)
                draw_unit_right(screen, interface, log.action, "Green", 1, *base)

        else:
            pic = get_image(interface.move_icon)
            screen.blit(pic, symbol_location)

            if log.player_color == "Green":
                draw_unit_right(screen, interface, log.action, "Green", 0, *base)
            elif log.player_color == "Red":
                draw_unit_right(screen, interface, log.action, "Red", 0, *base)

    base_x = int(391 * zoom)
    base_y = int(len(logbook) * log_heights)
    base = (base_x, base_y)

    if not action:
        draw_turn_box(screen, interface, player_color, action_number, *base)

    return logbook


def draw_attack(screen, interface, action, outcome_string, base, symbol_location, log):
    draw_outcome(screen, interface, outcome_string, *base)

    pic = get_image(interface.attack_icon)
    screen.blit(pic, symbol_location)

    if log.player_color == "Green":
        draw_unit_right(screen, interface, action, "Green", 0, *base)
        draw_unit_right(screen, interface, action, "Red", 1, *base)
    elif log.player_color == "Red":
        draw_unit_right(screen, interface, action,  "Red", 0, *base)
        draw_unit_right(screen, interface, action, "Green", 1, *base)


def draw_unit_right(screen, interface, action, color, index, base_x, base_y):

    if not action.target_at:
        unit = action.unit
    elif index == 0:
        unit = action.unit
    else:
        unit = action.target_unit

    unit_height = int((base_height - 10) * zoom)
    unit_width = int((interface.unit_width / interface.unit_height) * unit_height)

    location = (base_x + (65 + index * 100) * zoom, base_y + 3 * zoom)
    unit_pic = get_unit_pic(interface, unit.image)
    unit_image = get_image(unit_pic, (unit_width, unit_height))

    screen.blit(unit_image, location)

    draw_unit_box_right(screen, interface, location, color, unit_height, unit_width)


def draw_turn_box(screen, interface, color, action_number, base_x, base_y):
    box_width, box_height = 40 * zoom, (base_height - 2) * zoom
    position_and_size = (base_x, base_y, box_width, box_height)

    if color == "Green":
        border_color = interface.green_player_color
    else:
        border_color = interface.red_player_color

    pygame.draw.rect(screen, border_color, position_and_size)

    location = (base_x + 7 * zoom, base_y)
    write(screen, str(action_number), location, interface.fonts["big"])


def draw_unit_box_right(screen, interface, base, color, height, width):

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
    write(screen, outcome, location, interface.fonts["big"])
