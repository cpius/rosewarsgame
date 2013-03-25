import pygame
import settings
from coordinates import Coordinates
import battle


_image_library = {}


class View(object):
    def __init__(self):
        pygame.init()

        exec("import %s" % settings.interface)

        self.screen = pygame.display.set_mode(settings.board_size)

        pic = self.get_image("./other/wood.jpg")
        self.screen.blit(pic, (391, 0))

        self.font = pygame.font.SysFont(settings.normal_font_name, settings.normal_font_size, True, False)
        self.font_big = pygame.font.SysFont(settings.normal_font_name, settings.big_font_size, True, False)
        self.font_bigger = pygame.font.SysFont(settings.normal_font_name, settings.bigger_font_size, True, False)
        self.font_dice = pygame.font.SysFont(settings.normal_font_name, settings.dice_font_size, True, False)

        self.base_coordinates = Coordinates(settings.base_coordinates)
        self.center_coordinates = Coordinates(settings.center_coordinates)
        self.symbol_coordinates = Coordinates(settings.symbol_coordinates)

    def get_position_from_mouse_click(self, coordinates):
        x = int((coordinates[0] - settings.x_border) / (settings.unit_width + settings.unit_padding_width)) + 1
        if coordinates[1] > settings.board_size[1] / 2:
            y = 8 - int((coordinates[1] - settings.y_border_bottom) / (settings.unit_height + settings.unit_padding_height))
        else:
            y = 8 - int((coordinates[1] - settings.y_border_top) / (settings.unit_height + settings.unit_padding_height))
        return x, y

    def draw_ask_about_counter(self, unit_name):
        label = self.font_big.render("Select counter for", 1, settings.black)
        self.screen.blit(label, (410, 490))
        label = self.font_big.render(unit_name, 1, settings.black)
        self.screen.blit(label, (410, 515))
        label = self.font_big.render("'a' for attack", 1, settings.black)
        self.screen.blit(label, (410, 540))
        label = self.font_big.render("'d' for defence", 1, settings.black)
        self.screen.blit(label, (410, 565))
        pygame.display.update()

    def draw_ask_about_ability(self, ability1, ability2):
        label = self.font_big.render("Select ability:", 1, settings.black)
        self.screen.blit(label, (460, 330))
        label = self.font_big.render("1 for " + ability1, 1, settings.black)
        self.screen.blit(label, (460, 365))
        label = self.font_big.render("2 for " + ability2, 1, settings.black)
        self.screen.blit(label, (460, 400))
        pygame.display.update()

    def show_unit_zoomed(self, unit_name, color):
        unit_pic = self.get_unit_pic(unit_name, color, True)
        pic = self.get_image(unit_pic)
        self.screen.blit(pic, (24, 49))
        pygame.display.flip()

    def save_screenshot(self, name):
        pygame.image.save(self.screen, "./replay/" + name + ".jpeg")

    def draw_game_end(self, color):
        pic = self.get_image("./other/wood.jpg")
        self.screen.blit(pic, (391, 0))
        font = pygame.font.SysFont("monospace", 55, bold=True)
        label = font.render(color + " Wins", 1, settings.black)
        self.screen.blit(label, (440, 300))
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
        pygame.draw.circle(self.screen, settings.counter_circle_color, counter_coordinates.get(position), 10, 0)
        pygame.draw.circle(self.screen, settings.brown, counter_coordinates.get(position), 8, 0)
        if unit.attack_counters != 1:
            label = self.font.render(str(unit.attack_counters), 1, settings.black)
            self.screen.blit(label, font_coordinates.get(position))

    def draw_defence_counters(self, unit, position, counter_coordinates, font_coordinates):
        if hasattr(unit, "sabotaged"):
            defence_counters = -1
        else:
            defence_counters = unit.defence_counters

        pygame.draw.circle(self.screen, settings.counter_circle_color, counter_coordinates.get(position), 10, 0)
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
            pygame.draw.circle(self.screen, settings.counter_circle_color, counter_coordinates.get(position), 10, 0)
            pygame.draw.circle(self.screen, settings.yellow, counter_coordinates.get(position), 8, 0)

    def draw_blue_counters(self, unit, position, counter_coordinates, font_coordinates):
        if unit.blue_counters:
            pygame.draw.circle(self.screen, settings.counter_circle_color, counter_coordinates.get(position), 10, 0)
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

    def draw_message(self, string):
        label = self.font_big.render(string, 1, settings.black)
        self.screen.blit(label, (440, 350))

    def draw_unit(self, unit, position, color, selected=False):
        unit_pic = self.get_unit_pic(unit.name, color)
        pic = self.get_image(unit_pic)
        self.screen.blit(pic, self.base_coordinates.get(position))

        base = self.base_coordinates.get(position)
        position_and_size = (base[0], base[1], settings.unit_width, settings.unit_height)

        if selected:
            rect = pygame.Surface((settings.unit_width, settings.unit_height), pygame.SRCALPHA, 32)
            rect.fill((0, 0, 0, 160))
            self.screen.blit(rect, (base[0], base[1]))

        if settings.interface in ["rectangles", "rectangles2"]:

            position_and_size_fill = (base[0] - 2, base[1] - 2, settings.unit_width + 4, settings.unit_height + 4)
            position_and_size_outer = (base[0] - 4, base[1] - 4, settings.unit_width + 8, settings.unit_height + 8)

            if color == "Red":
                rectangle_color = settings.red_player_color
            else:
                rectangle_color = settings.green_player_color
            pygame.draw.rect(self.screen, rectangle_color, position_and_size_fill, 4)
            pygame.draw.rect(self.screen, settings.black, position_and_size, 1)
            pygame.draw.rect(self.screen, settings.black, position_and_size_outer, 1)

        if settings.interface == "square":
            if color == "Red":
                rectangle_color = settings.dark_red
            else:
                rectangle_color = settings.dark_green
            pygame.draw.rect(self.screen, rectangle_color, position_and_size, 3)

        self.draw_counters(unit, position)
        self.draw_symbols(unit, position)

    def draw_game(self, gamestate, selected_position=None, attack_positions=set(), ability_positions=set(), move_positions=set()):

        pic = self.get_image(settings.board_image)
        self.screen.blit(pic, (0, 0))

        pic = self.get_image("./other/wood.jpg")
        self.screen.blit(pic, (391, 0))

        for position, unit in gamestate.units[0].items():
            if position == selected_position:
                self.draw_unit(unit, position, gamestate.current_player().color, True)
            else:
                self.draw_unit(unit, position, gamestate.current_player().color)

        for position, unit in gamestate.units[1].items():
            self.draw_unit(unit, position, gamestate.players[1].color)

        coordinates = Coordinates((0, 0))

        for move_position in move_positions:
            rect = pygame.Surface((settings.unit_width, settings.unit_height), pygame.SRCALPHA, 32)
            rect.fill((0, 0, 0, 160))
            self.screen.blit(rect, coordinates.get((move_position[0], move_position[1])))

        for attack_position in attack_positions:
            rect = pygame.Surface((settings.unit_width, settings.unit_height), pygame.SRCALPHA, 32)
            rect.fill((130, 0, 0, 170))
            self.screen.blit(rect, coordinates.get((attack_position[0], attack_position[1])))

        for ability_position in ability_positions:
            rect = pygame.Surface((settings.unit_width, settings.unit_height), pygame.SRCALPHA, 32)
            rect.fill((0, 0, 150, 130))
            self.screen.blit(rect, coordinates.get((ability_position[0], ability_position[1])))

        pygame.display.update()

    def draw_action(self, action, gamestate):
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

        if action.is_attack and settings.interface == "rectangles2":

            attacking_unit = action.unit_reference
            defending_unit = action.target_reference

            attack = battle.get_attack_rating(attacking_unit, defending_unit, action)
            defence = battle.get_defence_rating(attacking_unit, defending_unit, attack)

            if action.rolls[0] <= attack:
                if action.rolls[1] <= defence:
                    outcome = "Defended"
                else:
                    outcome = "Success"
            else:
                outcome = "Missed"

            label = self.font_bigger.render(str(outcome), 1, settings.black)
            self.screen.blit(label, (440, 350))

            if gamestate.current_player().color == "Red":

                unit_pic = self.get_unit_pic(attacking_unit.name, "Red")
                pic = self.get_image(unit_pic)
                self.screen.blit(pic, (440, 120))

                label = self.font_big.render("Attack: " + str(attack), 1, settings.black)
                self.screen.blit(label, (510, 140))

                if outcome != "Missed":
                    label = self.font_dice.render(str(action.rolls[1]), 1, settings.green_player_color)
                    self.screen.blit(label, (590, 370))

                label = self.font_dice.render(str(action.rolls[0]), 1, settings.red_player_color)
                self.screen.blit(label, (590, 300))

                unit_pic = self.get_unit_pic(defending_unit.name, "Green")
                pic = self.get_image(unit_pic)
                self.screen.blit(pic, (440, 550))

                label = self.font_big.render("Defence: " + str(defence), 1, settings.black)
                self.screen.blit(label, (510, 570))

            else:

                unit_pic = self.get_unit_pic(attacking_unit.name, "Green")
                pic = self.get_image(unit_pic)
                self.screen.blit(pic, (440, 550))

                label = self.font_big.render("Attack: " + str(attack), 1, settings.black)
                self.screen.blit(label, (510, 570))

                if outcome != "Missed":
                    label = self.font_dice.render(str(action.rolls[1]), 4, settings.red_player_color)
                    self.screen.blit(label, (590, 300))

                label = self.font_dice.render(str(action.rolls[0]), 4, settings.green_player_color)
                self.screen.blit(label, (590, 370))

                unit_pic = self.get_unit_pic(defending_unit.name, "Red")
                pic = self.get_image(unit_pic)
                self.screen.blit(pic, (440, 120))

                label = self.font_big.render("Defence: " + str(defence), 1, settings.black)
                self.screen.blit(label, (510, 140))

        pygame.display.update()

    def get_unit_pic(self, name, color=None, zoomed=False):
        if zoomed:
            return "./zoomed/" + name.replace(" ", "-") + ",-" + color + ".jpg"
        elif settings.interface == "original":
            return "./" + settings.unit_folder + "/" + name.replace(" ", "-") + ",-" + color + ".jpg"
        else:
            return "./" + settings.unit_folder + "/" + name.replace(" ", "-") + ".jpg"

    def refresh(self):
        pygame.display.flip()
