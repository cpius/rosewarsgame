from __future__ import division
from viewcommon import *
import pygame
import action_doer


class ActionType:
    Attack, Ability, Move = range(3)


class Viewlog:

    def __init__(self, zoom, interface, screen):
        self.logbook = []
        self.zoom = zoom
        self.interface = interface
        self.screen = screen
        self.maximum_logs = 5
        self.base_height = 48

        unit_height = int((self.base_height - 14) * self.zoom)
        unit_width = int((self.interface.unit_width * unit_height / self.interface.unit_height))
        self.unit_dimensions = (unit_width, unit_height)

        self.box_dimensions = 40 * self.zoom, (self.base_height - 2) * self.zoom
        self.line_thickness = int(3 * self.zoom)

        self.locations = {}
        for i in range(self.maximum_logs):
            base = Location(391, i * self.base_height, self.zoom)
            self.locations[i] = {"unit1": base.adjust(65, 5),
                                 "unit2": base.adjust(165, 5),
                                 "symbol": base.adjust(118, 8),
                                 "outcome": base.adjust(230, 5),
                                 "box": base.adjust(0, 0),
                                 "box_text": base.adjust(7, 0),
                                 "line": base.adjust(0, self.base_height - self.line_thickness / 2)}

    class Log():
        def __init__(self, action_type, unit, target_unit, action_number, colors, outcome_string=None):
            self.action_type = action_type
            self.unit = unit
            self.target_unit = target_unit
            self.outcome_string = outcome_string
            self.action_number = action_number
            self.colors = colors

    def draw_logbook(self):

        def clear_log():
            pygame.draw.rect(self.screen, Color.Light_grey, self.interface.right_side_rectangle)

        clear_log()

        if len(self.logbook) > self.maximum_logs:
            self.logbook.pop(0)

        for lognumber, log in enumerate(self.logbook):

            locations = self.locations[lognumber]

            self.draw_turn_box(log.colors[0], log.action_number, locations)
            self.draw_unit(log.unit, locations["unit1"], log.colors[0])

            if log.action_type == ActionType.Attack:
                symbol = self.interface.attack_icon
                self.draw_outcome(log.outcome_string, locations["outcome"])
                self.draw_unit(log.target_unit, locations["unit2"], log.colors[1])

            elif log.action_type == ActionType.Ability:
                symbol = self.interface.ability_icon
                self.draw_unit(log.target_unit, locations["unit2"], log.colors[1])

            else:
                symbol = self.interface.move_icon

            self.draw_symbol(symbol, locations["symbol"])

        write(self.screen, "Help", self.interface.help_area[0], self.interface.fonts["normal"])

    @staticmethod
    def get_outcome_string(action, rolls, gamestate, is_sub_action):
        if action_doer.is_win(action, rolls, gamestate, is_sub_action):
            return "WIN"
        elif not action_doer.attack_successful(action, rolls, gamestate, is_sub_action):
            return "MISS"
        else:
            return "DEFEND"

    def add_log(self, action, outcome, game):

        action_number = 3 - game.gamestate.get_actions_remaining()
        colors = game.current_player().color, game.opponent_player().color

        if action.is_attack():
            for position in outcome.outcomes:
                is_sub_action = action.target_at == position
                outcome_string = self.get_outcome_string(action, outcome.outcomes[position], game.gamestate, is_sub_action)
                target_unit = game.gamestate.all_units()[position]
                self.logbook.append(self.Log(ActionType.Attack, action.unit, target_unit, action_number, colors, outcome_string))
        elif action.is_ability():
            target_unit = game.gamestate.all_units()[action.target_at]
            self.logbook.append(self.Log(ActionType.Ability, action.unit, target_unit, action_number, colors))
        else:
            self.logbook.append(self.Log(ActionType.Move, action.unit, None, action_number, colors))

    def draw_unit(self, unit, location, color):
        unit_pic = get_unit_pic(self.interface, unit)
        unit_image = get_image(unit_pic, self.unit_dimensions)
        self.draw_unit_box(location, color)
        self.screen.blit(unit_image, location.tuple)

    def draw_symbol(self, symbol, location):
        image = get_image(symbol)
        self.screen.blit(image, location.tuple)

    def draw_turn_box(self, color, action_number, locations):
        border_color = self.interface.green_player_color if color == "Green" else self.interface.red_player_color

        pygame.draw.rect(self.screen, border_color, (locations["box"].tuple, self.box_dimensions))
        write(self.screen, str(action_number), locations["box_text"].tuple, self.interface.fonts["big"])

        line_start = locations["line"]
        line_end = line_start.adjust(600, 0)
        pygame.draw.line(self.screen, Color.Black, line_start.tuple, line_end.tuple, self.line_thickness)

    def draw_unit_box(self, base, color):

        border_color = self.interface.green_player_color if color == "Green" else self.interface.red_player_color
        thickness = int(3 * self.zoom)

        rectangle = pygame.Rect(base.tuple, self.unit_dimensions)
        pygame.draw.rect(self.screen, Color.Black, rectangle, 1)
        for i in range(1, thickness):
            pygame.draw.rect(self.screen, border_color, rectangle.inflate(2*i, 2*i), 1)
        pygame.draw.rect(self.screen, Color.Black, rectangle.inflate(2*thickness, 2*thickness), 1)

    def draw_outcome(self, outcome_string, location):
        write(self.screen, outcome_string, location.tuple, self.interface.fonts["larger"])
