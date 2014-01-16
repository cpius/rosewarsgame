from __future__ import division
import pygame
import interface_settings as settings
import viewlog
import viewgame
import viewinfo
from viewcommon import *


class View(object):
    def __init__(self):
        pygame.init()
        pygame.mixer.init()

        self.interface = settings.interface
        self.zoom = settings.zoom
        self.screen = pygame.display.set_mode(self.interface.board_size)
        self.logbook = []
        self.counter_size = self.interface.counter_size

        self.sounds = {
            "sword": "sword_sound.wav",
            "War_Elephant": "Elephant.wav",
            "Archer": "bow_fired.wav",
            "Fire_Archer": "bow_fired.wav",
            "Catapult": "catapult_attacksound.wav",
            "unit_defeated": "infantry_defeated_sound.wav",
            "your_turn": "fanfare.wav"
        }

    def get_position_from_mouse_click(self, coordinates):
        return get_position_from_mouseclick(self.interface, coordinates)

    def draw_ask_about_move_with_attack(self, position):
        viewgame.draw_ask_about_move_with_attack(self.screen, self.interface, position)
        write_message(self.screen, self.interface, "Click the tile you want to stand on.")
        self.refresh()

    def save_screenshot(self, name):
        pygame.image.save(self.screen, name)

    def draw_game_end(self, color):
        write_message(self.screen, self.interface, color + " Wins")
        self.refresh()

    def clear_right(self):
        pygame.draw.rect(self.screen, colors["light_grey"], self.interface.right_side_rectangle)

    def draw_game(self, game, start_at=None, actions=(), update_log=False):
        viewgame.draw_game(self.screen, self.interface, game, start_at, actions)
        if update_log:
            self.clear_right()
            self.logbook = viewlog.draw_log(self.logbook, self.screen, self.interface, game)
        self.refresh()

    def show_unit_zoomed(self, unit):
        self.clear_right()
        viewinfo.show_unit_zoomed(self.screen, self.interface, unit)
        self.refresh()

    @staticmethod
    def refresh():
        pygame.display.flip()

    def draw_upgrade_options(self, unit):
        viewinfo.draw_upgrade_options(self.screen, self.interface, unit)
        self.refresh()

    def draw_ask_about_ability(self, unit):
        viewinfo.draw_ask_about_ability(self.screen, self.interface, unit)
        self.refresh()

    def draw_action(self, action, outcome, game, flip=False):
        viewlog.draw_log(self.logbook, self.screen, self.interface, game, action, outcome)
        viewgame.draw_action(self.screen, self.interface, action, outcome, flip)
        self.refresh()

    def draw_post_movement(self, action):
        viewgame.draw_post_movement(self.screen, self.interface, action)
        self.refresh()

    def shade_positions(self, positions, color=None):
        viewgame.shade_positions(self.screen, self.interface, positions, color)
        self.refresh()

    def show_attack(self, gamestate, action, player_unit, opponent_unit):
        viewinfo.show_attack(self.screen, self.interface, action, player_unit, opponent_unit, gamestate)
        self.refresh()

    def draw_message(self, message):
        write_message(self.screen, self.interface, message)
        self.refresh()

    def draw_tutorial_message(self, message, horizontal_position=17):
        line_distances = self.interface.line_distances["small"]
        fonts = self.interface.fonts["small"]
        x_coordinate = 400 * settings.zoom
        y_coordinate = horizontal_position * settings.zoom
        show_lines(self.screen, message, 47 * settings.zoom, line_distances, fonts, x_coordinate, y_coordinate)
        self.refresh()

    def draw_game_tutorial(self, game):
        viewgame.draw_game(self.screen, self.interface, game)
        self.clear_right()
        self.refresh()

    def draw_action_tutorial(self, action, roll=None):
        viewgame.draw_action(self.screen, self.interface, action, False, roll)
        self.refresh()

    def play_sound(self, sound):
        sound = pygame.mixer.Sound("./../sounds/" + self.sounds[sound])
        sound.play()
