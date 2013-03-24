import pygame
import settings
from coordinates import Coordinates


_image_library = {}


class View(object):
    def __init__(self):
        pygame.init()

        exec("import %s" % settings.interface)

        self.screen = pygame.display.set_mode(settings.board_size)

        self.font = pygame.font.SysFont(settings.normal_font_name, settings.normal_font_size, True, False)
        self.font_big = pygame.font.SysFont(settings.normal_font_name, settings.big_font_size, True, False)

        self.base_coordinates = Coordinates(settings.base_coordinates)
        self.center_coordinates = Coordinates(settings.center_coordinates)
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
        unit_pic = self.get_unit_pic(settings.interface, unit_name, color, True)
        pic = self.get_image(unit_pic)
        self.screen.blit(pic, (24, 49))
        pygame.display.flip()

    def save_screenshot(self, name):
        pygame.image.save(self.screen, "./replay/" + name + ".jpeg")

    def draw_game_end(self, color):
        font = pygame.font.SysFont("monospace", 55, bold=True)
        label = font.render(color + " Wins", 1, settings.black)
        self.screen.blit(label, (40, 300))
        pygame.display.update()

    def get_image(self, path):
        global _image_library
        image = _image_library.get(path)
        if not image:
            image = pygame.image.load(path).convert()
            _image_library[path] = image
        return image

    def draw_counters(self, unit, position):
        counters_drawn = 0

        if unit.attack_counters:
            counter_coordinates = self.get_counter_coordinates(counters_drawn)
            font_coordinates = self.get_font_coordinates(counters_drawn)
            self.draw_attack_counters(unit, position, counter_coordinates, font_coordinates)
            counters_drawn += 1
        if unit.defence_counters or hasattr(unit, "sabotaged"):
            counter_coordinates = self.get_counter_coordinates(counters_drawn)
            font_coordinates = self.get_font_coordinates(counters_drawn)
            self.draw_defence_counters(unit, position, counter_coordinates, font_coordinates)
            counters_drawn += 1
        if unit.blue_counters:
            counter_coordinates = self.get_counter_coordinates(counters_drawn)
            font_coordinates = self.get_font_coordinates(counters_drawn)
            self.draw_blue_counters(unit, position, counter_coordinates, font_coordinates)
            counters_drawn += 1
        if unit.yellow_counters:
            counter_coordinates = self.get_counter_coordinates(counters_drawn)
            self.draw_yellow_counters(unit, position, counter_coordinates)

    def get_counter_coordinates(self, counters_drawn):
        return {
            0: Coordinates(settings.first_counter_coordinates),
            1: Coordinates(settings.second_counter_coordinates),
            2: Coordinates(settings.third_counter_coordinates),
            3: Coordinates(settings.third_counter_coordinates)
        }[counters_drawn]

    def get_font_coordinates(self, counters_drawn):
        return {
            0: Coordinates(settings.first_font_coordinates),
            1: Coordinates(settings.second_font_coordinates),
            2: Coordinates(settings.third_font_coordinates),
            3: Coordinates(settings.third_counter_coordinates)
        }[counters_drawn]

    def draw_attack_counters(self, unit, position, counter_coordinates, font_coordinates):
        pygame.draw.circle(self.screen, settings.grey, counter_coordinates.get(position), 10, 0)
        pygame.draw.circle(self.screen, settings.brown, counter_coordinates.get(position), 8, 0)
        if unit.attack_counters != 1:
            label = self.font.render(str(unit.attack_counters), 1, settings.black)
            self.screen.blit(label, font_coordinates.get(position))

    def draw_defence_counters(self, unit, position, counter_coordinates, font_coordinates):
        if hasattr(unit, "sabotaged"):
            defence_counters = -1
        else:
            defence_counters = unit.defence_counters

        pygame.draw.circle(self.screen, settings.grey, counter_coordinates.get(position), 10, 0)
        pygame.draw.circle(self.screen, settings.light_grey, counter_coordinates.get(position), 8, 0)

        counter_text = None
        if defence_counters > 1:
            counter_text = str(defence_counters)
        elif defence_counters < 0:
            counter_text = "x"

        if counter_text:
            label = self.font.render(counter_text, 1, settings.black)
            self.screen.blit(label, font_coordinates.get(position))

    def draw_yellow_counters(self, unit, position, counter_coordinates):
        if unit.yellow_counters:
            pygame.draw.circle(self.screen, settings.grey, counter_coordinates.get(position), 10, 0)
            pygame.draw.circle(self.screen, settings.yellow, counter_coordinates.get(position), 8, 0)

    def draw_blue_counters(self, unit, position, counter_coordinates, font_coordinates):
        if unit.blue_counters:
            pygame.draw.circle(self.screen, settings.grey, counter_coordinates.get(position), 10, 0)
            pygame.draw.circle(self.screen, settings.blue, counter_coordinates.get(position), 8, 0)

            if unit.blue_counters > 1:
                label = self.font.render(str(unit.blue_counters), 1, settings.black)
                self.screen.blit(label, font_coordinates.get(position))

    def draw_symbols(self, unit, position):
        coordinates = Coordinates(settings.first_symbol_coordinates)
        if unit.xp == 1:
            self.draw_xp(position, coordinates)
            coordinates = Coordinates(settings.second_symbol_coordinates)
        if hasattr(unit, "bribed"):
            self.draw_bribed(position, coordinates)
            coordinates = Coordinates(settings.second_symbol_coordinates)
        if hasattr(unit, "is_crusading"):
            self.draw_crusading(position, coordinates)

    def draw_xp(self, position, coordinates):
        pic = self.get_image(settings.star_icon)
        self.screen.blit(pic, coordinates.get(position))

    def draw_bribed(self, position, coordinates):
        pic = self.get_image(settings.ability_icon)
        self.screen.blit(pic, coordinates.get(position))

    def draw_crusading(self, position, coordinates):
        pic = self.get_image(settings.crusading_icon)
        self.screen.blit(pic, coordinates.get(position))

    def draw_unit(self, unit, position, color):
        unit_pic = self.get_unit_pic(settings.interface, unit.name, color)
        pic = self.get_image(unit_pic)
        self.screen.blit(pic, self.base_coordinates.get(position))

        base = self.base_coordinates.get(position)
        position_and_size = (base[0], base[1], settings.unit_width, settings.unit_height)

        if settings.interface in ["square", "rectangles"]:
            if color == "Red":
                rectangle_color = settings.dark_red
            else:
                rectangle_color = settings.dark_green
            pygame.draw.rect(self.screen, rectangle_color, position_and_size, 3)

        self.draw_counters(unit, position)
        self.draw_symbols(unit, position)

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
                coordinates = Coordinates(settings.first_symbol_coordinates)
                self.screen.blit(pic, coordinates.get(action.end_position))

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

    def get_unit_pic(self, interface, name, color=None, zoomed=False):
        if zoomed:
            return "./zoomed/" + name.replace(" ", "-") + ",-" + color + ".jpg"
        elif interface == "original":
            return "./" + interface + "/" + name.replace(" ", "-") + ",-" + color + ".jpg"
        else:
            return "./" + interface + "/" + name.replace(" ", "-") + ".jpg"

    def refresh(self):
        pygame.display.flip()
