from __future__ import division
import pygame
import settings
from coordinates import Coordinates
import colors
import viewlog
import viewgame
import viewinfo
import viewmethods as m

_anti_alias = 1


class View(object):
    def __init__(self):
        pygame.init()

        self.interface = settings.interface
        self.zoom = settings.zoom
        self.screen = pygame.display.set_mode(self.interface.board_size)
        self.clear_right()

        self.logbook = []

        self.counter_size = self.interface.counter_size

    def clear_right(self):
        pygame.draw.rect(self.screen, colors.light_grey, self.interface.right_side_rectangle)

    def clear_info(self):
        pygame.draw.rect(self.screen, colors.light_grey, self.interface.lower_right_rectangle)

    def get_position_from_mouse_click(self, coordinates):
        x = int((coordinates[0] - self.interface.x_border) /
                (self.interface.unit_width + self.interface.unit_padding_width)) + 1
        if coordinates[1] > self.interface.board_size[1] / 2:
            y = 8 - int((coordinates[1] - self.interface.y_border_bottom) /
                        (self.interface.unit_height + self.interface.unit_padding_height))
        else:
            y = 8 - int((coordinates[1] - self.interface.y_border_top) /
                        (self.interface.unit_height + self.interface.unit_padding_height))
        return x, y

    def draw_ask_about_move_with_attack(self, position):

        base = self.interface.coordinates["base"].get(position)

        dimensions = (self.interface.unit_width, self.interface.unit_height)
        m.draw_rectangle(self.screen, dimensions, base, self.interface.selected_shading)

        m.write_message(self.screen, self.interface, "Click the tile you want to stand on.")
        pygame.display.update()

    def save_screenshot(self, name):
        pygame.image.save(self.screen, "./replay/" + name + ".jpeg")

    def draw_game_end(self, color):
        m.write_message(self.screen, self.interface, color + " Wins")
        pygame.display.update()

    def draw_game(self, game, start_position=None, actions=()):

        viewgame.draw_game(self.screen, self.interface, game, start_position, actions)
        self.draw_right()
        pygame.display.update()

    def show_unit_zoomed(self, unit):
        self.clear_right()
        viewinfo.show_unit_zoomed(self.screen, self.interface, unit)

    def refresh(self):
        pygame.display.flip()

    def draw_right(self):
        pygame.draw.rect(self.screen, colors.light_grey, self.interface.right_side_rectangle)
        self.logbook = viewlog.draw_log(self.logbook, self.screen, self.interface)

    def draw_log(self, action, gamestate):
        viewlog.draw_log(self, action, gamestate)

    def draw_upgrade_options(self, unit):
        self.clear_info()
        viewinfo.draw_upgrade_options(self.screen, self.interface, unit)

    def draw_ask_about_ability(self, unit):
        pass

    def draw_action(self, action, game, flip=False):

        viewlog.draw_log(self.logbook, self.screen, self.interface, action, game)
        viewgame.draw_action(self.screen, self.interface, action, flip)

    def draw_post_movement(self, action, gamestate):
        viewgame.draw_post_movement(self.screen, self.interface, action)

    def shade_positions(self, positions):
        viewgame.shade_positions(self.screen, self.interface, positions)

    def show_attack(self, action, player_unit, opponent_unit):
        pass

    def draw_message(self, message):
        m.write_message(self.screen, self.interface, message)
        pygame.display.update()

    def draw_tutorial(self, game):
        viewgame.draw_game(self.screen, self.interface, game)
        pygame.display.update()
