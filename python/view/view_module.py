from view.viewlog import Viewlog
from view.viewgame import Viewgame
from view.viewinfo import Viewinfo
from view.view_control_library import *
from view.view_display_library import *
import game.settings as settings
import view.interfaces as interfaces
from game.enums import Intelligence


class View():
    def __init__(self):
        pygame.init()
        pygame.mixer.init()

        self.zoom = settings.zoom
        self.interface = getattr(interfaces, settings.interface_name)(settings.zoom)
        self.interface.load_fonts(self.zoom)
        self.screen = pygame.display.set_mode(self.interface.board_size)
        self.viewlog = Viewlog(self.zoom, self.interface, self.screen)
        self.viewgame = Viewgame(self.interface, self.screen)
        self.viewinfo = Viewinfo(self.interface, self.screen, self.zoom)

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

    def draw_ask_about_move_with_attack(self, game, end_at, target_at):
        self.draw_game(game, None, None, False)
        self.viewgame.draw_ask_about_move_with_attack(end_at, target_at)
        write_message(self.screen, self.interface, "Click the tile you want to stand on.")
        self.refresh()

    def save_screenshot(self, name):
        pygame.image.save(self.screen, name)

    def draw_game_end(self, color, game):
        self.draw_game(game, actions=None, shade_positions=None, redraw_log=True)
        write_message(self.screen, self.interface, color + " Wins")
        self.refresh()

    def clear_right(self):
        pygame.draw.rect(self.screen, Color.Light_grey, self.interface.right_side_rectangle)
        write(self.screen, "Help", self.interface.help_area[0], self.interface.fonts["normal"])

    def clear_left(self):
        pygame.draw.rect(self.screen, Color.Light_grey, self.interface.left_side_rectangle)

    def draw_game(self, game, actions, shade_positions, redraw_log):
        self.viewgame.draw_game(game, actions, shade_positions)
        if redraw_log:
            self.clear_right()
            self.viewlog.draw_logbook(game)
        if game.gamestate.is_extra_action() and game.current_player().intelligence == Intelligence.Human:
            self.viewinfo.draw_pass_action_button()
        self.refresh()

    @staticmethod
    def refresh():
        pygame.display.flip()

    def draw_upgrade_options(self, upgrade_choices, unit):
        self.viewinfo.draw_upgrade_options(upgrade_choices, unit)
        self.refresh()

    def draw_ask_about_ability(self, unit):
        self.viewinfo.draw_ask_about_ability(unit)
        self.refresh()

    def draw_action(self, action, game):
        self.viewlog.draw_logbook(game)
        flip = not game.is_player_human()
        self.viewgame.draw_action(action, flip)
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

    def shade_actions(self, actions):
        self.viewgame.shade_actions(actions)
        self.refresh()

    def show_battle_hint(self, gamestate, start_at, target_at):
        self.viewinfo.show_battle_hint(gamestate, start_at, target_at)
        self.refresh()

    def show_unit_zoomed(self, unit):
        self.clear_right()
        self.viewinfo.show_unit_zoomed(unit)
        self.refresh()

    def click_is_on_board(self, coordinates):
        return click_is_on_board(self.interface, coordinates)

    def get_item_from_mouse_click(self, coordinates):
        return get_item_from_mouse_click(self.interface, coordinates)

    def draw_pass_action_button(self):
        self.viewinfo.draw_pass_action_button()
        self.refresh()

