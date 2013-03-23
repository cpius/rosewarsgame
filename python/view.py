import pygame
import settings
from coordinates import Coordinates


_image_library = {}


class View(object):
    def __init__(self):
        pygame.init()

        self.screen = pygame.display.set_mode(settings.board_size)

        self.font = pygame.font.SysFont(settings.normal_font_name, settings.normal_font_size, True, False)
        self.font_big = pygame.font.SysFont(settings.normal_font_name, settings.big_font_size, True, False)

        self.base_coordinates = Coordinates(settings.base_coordinates)
        self.center_coordinates = Coordinates(settings.center_coordinates)
        self.attack_counter_coordinates = Coordinates(settings.attack_counter_coordinates)
        self.defence_counter_coordinates = Coordinates(settings.defence_counter_coordinates)
        self.defence_font_coordinates = Coordinates(settings.defence_font_coordinates)
        self.flag_coordinates = Coordinates(settings.flag_coordinates)
        self.yellow_counter_coordinates = Coordinates(settings.yellow_counter_coordinates)
        self.blue_counter_coordinates = Coordinates(settings.blue_counter_coordinates)
        self.star_coordinates = Coordinates(settings.star_coordinates)
        self.blue_font_coordinates = Coordinates(settings.blue_font_coordinates)
        self.attack_font_coordinates = Coordinates(settings.attack_font_coordinates)
        self.symbol_coordinates = Coordinates(settings.symbol_coordinates)

    def get_position_from_mouse_click(self, coordinates):
        x = int((coordinates[0] - settings.x_border) / settings.unit_width) + 1
        if coordinates[1] > 454:
            y = 8 - int((coordinates[1] - settings.y_border_bottom) / settings.unit_height)
        else:
            y = 8 - int((coordinates[1] - settings.y_border_top) / settings.unit_height)
        return x, y

    def draw_ask_about_counter(self, unit_name):
        label = self.font_big.render("Select counter for " + unit_name, 1, settings.black)
        self.screen.blit(label, (20, 400))
        label = self.font_big.render("'a' for attack, 'd' for defence", 1, settings.black)
        self.screen.blit(label, (20, 435))
        pygame.display.update()

    def draw_ask_about_ability(self, ability1, ability2):
        label = self.font_big.render("Select ability:", 1, settings.black)
        self.screen.blit(label, (130, 400))
        label = self.font_big.render("1 for " + ability1, 1, settings.black)
        self.screen.blit(label, (130, 435))
        label = self.font_big.render("2 for " + ability2, 1, settings.black)
        self.screen.blit(label, (130, 470))
        pygame.display.update()

    def show_unit_zoomed(self, unit_name, color):
        pic = self.get_image("./units_big/" + self.get_unit_pic(unit_name, color))
        self.screen.blit(pic, (40, 40))
        pygame.display.flip()

    def save_screenshot(self, name):
        pygame.image.save(self.screen, "./replay/" + name + ".jpeg")

    def draw_game_end(self, color):
        font = pygame.font.SysFont("monospace", 55, bold=True)
        label = font.render(color + " Wins", 1, settings.black)
        self.screen.blit(label, (40, 400))
        pygame.display.update()

    def get_image(self, path):
        global _image_library
        image = _image_library.get(path)
        if not image:
            image = pygame.image.load(path).convert()
            _image_library[path] = image
        return image

    def draw_attack_counters(self, unit, position):
        if unit.attack_counters:
            pygame.draw.circle(self.screen, settings.grey, self.attack_counter_coordinates.get(position), 10, 0)
            pygame.draw.circle(self.screen, settings.brown, self.attack_counter_coordinates.get(position), 8, 0)
            if unit.attack_counters != 1:
                label = self.font.render(str(unit.attack_counters), 1, settings.black)
                self.screen.blit(label, self.attack_font_coordinates.get(position))

    def draw_defence_counters(self, unit, position):

        if hasattr(unit, "sabotaged"):
            defence_counters = -1
        else:
            defence_counters = unit.defence_counters

        if defence_counters:
            pygame.draw.circle(self.screen, settings.grey, self.defence_counter_coordinates.get(position), 10, 0)
            pygame.draw.circle(self.screen, settings.light_grey, self.defence_counter_coordinates.get(position), 8, 0)

            if defence_counters > 1:
                label = self.font.render(str(defence_counters), 1, settings.black)
                self.screen.blit(label, self.defence_font_coordinates.get(position))

            if defence_counters < 0:
                label = self.font.render("x", 1, settings.black)
                self.screen.blit(label, self.defence_font_coordinates.get(position))

    def draw_xp(self, unit, position):
        if unit.xp == 1:
            pic = self.get_image(settings.star_icon)
            self.screen.blit(pic, self.star_coordinates.get(position))

    def draw_yellow_counters(self, unit, position):
        if unit.yellow_counters:
            pygame.draw.circle(self.screen, settings.grey, self.yellow_counter_coordinates.get(position), 10, 0)
            pygame.draw.circle(self.screen, settings.yellow, self.yellow_counter_coordinates.get(position), 8, 0)

    def draw_blue_counters(self, unit, position):
        if unit.blue_counters:
            pygame.draw.circle(self.screen, settings.grey, self.blue_counter_coordinates.get(position), 10, 0)
            pygame.draw.circle(self.screen, settings.blue, self.blue_counter_coordinates.get(position), 8, 0)

            if unit.blue_counters > 1:
                label = self.font.render(str(unit.blue_counters), 1, settings.black)
                self.screen.blit(label, self.blue_font_coordinates.get(position))

    def draw_bribed(self, unit, position):
        if hasattr(unit, "bribed"):
            pic = self.get_image(settings.ability_icon)
            self.screen.blit(pic, self.symbol_coordinates.get(position))

    def draw_crusading(self, unit, position):
        if hasattr(unit, "is_crusading"):
            pic = self.get_image(settings.crusading_icon)
            self.screen.blit(pic, self.flag_coordinates.get(position))

    def draw_unit(self, unit, position, color):
        pic = self.get_image("./units_small/" + self.get_unit_pic(unit.name, color))
        self.screen.blit(pic, self.base_coordinates.get(position))

        self.draw_attack_counters(unit, position)
        self.draw_defence_counters(unit, position)
        self.draw_xp(unit, position)

        self.draw_yellow_counters(unit, position)
        self.draw_blue_counters(unit, position)

        self.draw_crusading(unit, position)
        self.draw_bribed(unit, position)

    def draw_game(self, gamestate):

        pic = self.get_image(settings.board_image)
        self.screen.blit(pic, (0, 0))

        for position, unit in gamestate.units[0].items():
            self.draw_unit(unit, position, gamestate.current_player().color)

        for position, unit in gamestate.units[1].items():
            self.draw_unit(unit, position, gamestate.players[1].color)

        pygame.display.update()

    def draw_action(self, action):
        pygame.draw.circle(self.screen, settings.black, self.center_coordinates.get(action.start_position), 10)
        pygame.draw.line(self.screen,
                         settings.black,
                         self.center_coordinates.get(action.start_position),
                         self.center_coordinates.get(action.end_position),
                         5)

        if action.is_attack:
            pygame.draw.line(self.screen,
                             settings.black,
                             self.center_coordinates.get(action.end_position),
                             self.center_coordinates.get(action.attack_position),
                             5)
            if action.move_with_attack:
                pic = self.get_image(settings.move_attack_icon)
            else:
                pic = self.get_image(settings.attack_icon)

            if hasattr(action, "high_morale"):
                pic = self.get_image(settings.high_morale_icon)
                self.screen.blit(pic, self.flag_coordinates.get(action.end_position))

            self.screen.blit(pic, self.symbol_coordinates.get(action.attack_position))

        elif action.is_ability:
            pygame.draw.line(self.screen,
                             settings.black,
                             self.center_coordinates.get(action.end_position),
                             self.center_coordinates.get(action.attack_position), 5)
            pic = self.get_image(settings.ability_icon)
            self.screen.blit(pic, self.symbol_coordinates.get(action.attack_position))

        else:
            pic = self.get_image(settings.move_icon)
            self.screen.blit(pic, self.symbol_coordinates.get(action.end_position))

        pygame.display.update()

    def get_unit_pic(self, name, color):
        return name.replace(" ", "-") + ",-" + color.lower() + ".jpg"

    def refresh(self):
        pygame.display.flip()
