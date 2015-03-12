from __future__ import division
from viewlog import Viewlog
from viewgame import Viewgame
from viewinfo import Viewinfo
from viewcommon import *


class View(object):
    def __init__(self):
        pygame.init()
        pygame.mixer.init()

        self.zoom = settings.zoom
        self.interface = settings.interface
        self.interface.load_fonts(self.zoom)
        self.screen = pygame.display.set_mode(self.interface.board_size)
        self.viewlog = Viewlog(self.zoom, self.interface, self.screen)
        self.viewgame = Viewgame(self.interface, self.screen)
        self.viewinfo = Viewinfo(self.interface, self.screen, self.zoom)
        self.counter_size = self.interface.counter_size
        self.showing_unit_info = False

        self.sounds = {
            "sword": "sword_sound.wav",
            "War_Elephant": "Elephant.wav",
            "Archer": "bow_fired.wav",
            "Catapult": "catapult_attacksound.wav",
            "unit_defeated": "infantry_defeated_sound.wav",
            "your_turn": "fanfare.wav"
        }

    def get_position_from_mouse_click(self, coordinates):
        return get_position_from_mouseclick(self.interface, coordinates)

    def draw_ask_about_move_with_attack(self, position):
        self.viewgame.draw_ask_about_move_with_attack(position)
        write_message(self.screen, self.interface, "Click the tile you want to stand on.")
        self.refresh()

    def save_screenshot(self, name):
        pygame.image.save(self.screen, name)

    def draw_game_end(self, color):
        self.clear_right()
        self.viewlog.draw_logbook()
        write_message(self.screen, self.interface, color + " Wins")
        self.refresh()

    def clear_right(self):
        pygame.draw.rect(self.screen, Color.Light_grey, self.interface.right_side_rectangle)
        write(self.screen, "Help", self.interface.help_area[0], self.interface.fonts["normal"])
        self.showing_unit_info = False

    def clear_left(self):
        pygame.draw.rect(self.screen, Color.Light_grey, self.interface.left_side_rectangle)

    def draw_game(self, game, start_at=None, actions=(), redraw_log=False):
        self.viewgame.draw_game(game, start_at, actions)
        if redraw_log:
            self.clear_right()
            self.viewlog.draw_logbook()
        self.refresh()

    def show_unit_zoomed(self, unit, attack_hint):
        self.clear_right()
        self.viewinfo.show_unit_zoomed(unit, attack_hint)
        self.showing_unit_info = True
        self.refresh()

    def show_unit_zoomed_tutorial(self, unit, attack_hint):
        self.clear_right_tutorial()
        self.viewinfo.show_unit_zoomed(unit, attack_hint)
        self.showing_unit_info = True
        write(self.screen, "To Game", self.interface.help_area[0], self.interface.fonts["normal"])
        self.refresh()

    def hide_unit_zoomed(self):
        if self.showing_unit_info:
            self.clear_right()
            self.viewlog.draw_logbook()

    @staticmethod
    def refresh():
        pygame.display.flip()

    def draw_upgrade_options(self, unit):
        self.viewinfo.draw_upgrade_options(unit)
        self.refresh()

    def draw_ask_about_ability(self, unit):
        self.viewinfo.draw_ask_about_ability(unit)
        self.refresh()

    def draw_action(self, action, outcome, game, flip=False):
        self.viewlog.add_log(action, outcome, game)
        self.viewlog.draw_logbook()
        self.viewgame.draw_action(action, outcome, flip)
        self.refresh()

    def draw_post_movement(self, action):
        self.viewgame.draw_post_movement(action)
        self.refresh()

    def shade_positions(self, positions, color=None):
        self.viewgame.shade_positions(positions, color)
        self.refresh()

    def draw_message(self, message):
        write_message(self.screen, self.interface, message)
        self.refresh()

    def play_sound(self, sound):
        sound = pygame.mixer.Sound("./../sounds/" + self.sounds[sound])
        sound.play()

    def draw_help_menu(self, menu):
        self.screen.fill(Color.Light_grey)
        for i, item in enumerate(menu):
            write(self.screen, item, self.interface.help_menu[i], self.interface.fonts["normal"])
        write(self.screen, "To game", self.interface.help_area[0], self.interface.fonts["normal"])
        self.refresh()
