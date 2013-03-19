import pygame


black = (0, 0, 0)
white = (255, 255, 255)
green = (0, 255, 0)
red = (255, 0, 0)
brown = (128, 64, 0)
grey = (48, 48, 48)
yellow = (200, 200, 0)
light_grey = (223, 223, 223)
blue = (0, 102, 204)

unit_width = 70
unit_height = 106.5
board_size = [391, 908]
x_border = 22
y_border_top = 22
y_border_bottom = 39


class Coordinates(object):
    def __init__(self, x, y):
        self.add_x = x
        self.add_y = y

    def get(self, position):
        if position[1] >= 5:
            y_border = y_border_top
        else:
            y_border = y_border_bottom

        return int((position[0] - 1) * unit_width + x_border + self.add_x), \
            int((8 - position[1]) * unit_height + y_border + self.add_y)

base_coords = Coordinates(0, 0)
center_coords = Coordinates(35, 53.2)
symbol_coords = Coordinates(13, 38.2)
attack_counter_coords = Coordinates(50, 78)
defence_counter_coords = Coordinates(50, 58)
defence_font_coords = Coordinates(45, 48)
flag_coords = Coordinates(46, 10)
yellow_counter_coords = Coordinates(50, 38)
blue_counter_coords = Coordinates(50, 18)
star_coords = Coordinates(8, 58)
blue_font_coords = Coordinates(45, 8)
attack_font_coords = Coordinates(45, 68)

_image_library = {}


class View(object):
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode(board_size)
        self.font = pygame.font.SysFont("arial", 18, True, False)
        self.font_big = pygame.font.SysFont("arial", 28, True, False)

    def get_position_from_mouse_click(self, coordinates):
        x = int((coordinates[0] - x_border) / unit_width) + 1
        if coordinates[1] > 454:
            y = 8 - int((coordinates[1] - y_border_bottom) / unit_height)
        else:
            y = 8 - int((coordinates[1] - y_border_top) / unit_height)
        return x, y

    def draw_ask_about_counter(self, unit_name):
        label = self.font_big.render("Select counter for " + unit_name, 1, black)
        self.screen.blit(label, (20, 400))
        label = self.font_big.render("'a' for attack, 'd' for defence", 1, black)
        self.screen.blit(label, (20, 435))
        pygame.display.update()

    def draw_ask_about_ability(self, ability1, ability2):
        label = self.font_big.render("Select ability:", 1, black)
        self.screen.blit(label, (130, 400))
        label = self.font_big.render("1 for " + ability1, 1, black)
        self.screen.blit(label, (130, 435))
        label = self.font_big.render("2 for " + ability2, 1, black)
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
        label = font.render(color + " Wins", 1, black)
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
            pygame.draw.circle(self.screen, grey, attack_counter_coords.get(position), 10, 0)
            pygame.draw.circle(self.screen, brown, attack_counter_coords.get(position), 8, 0)
            if unit.attack_counters != 1:
                label = self.font.render(str(unit.attack_counters), 1, black)
                self.screen.blit(label, attack_font_coords.get(position))

    def draw_defence_counters(self, unit, position):

        if hasattr(unit, "sabotaged"):
            defence_counters = -1
        else:
            defence_counters = unit.defence_counters

        if defence_counters:
            pygame.draw.circle(self.screen, grey, defence_counter_coords.get(position), 10, 0)
            pygame.draw.circle(self.screen, light_grey, defence_counter_coords.get(position), 8, 0)

            if defence_counters > 1:
                label = self.font.render(str(defence_counters), 1, black)
                self.screen.blit(label, defence_font_coords.get(position))

            if defence_counters < 0:
                label = self.font.render("x", 1, black)
                self.screen.blit(label, defence_font_coords.get(position))

    def draw_xp(self, unit, position):
        if unit.xp == 1:
            pic = self.get_image("./other/star.gif")
            self.screen.blit(pic, star_coords.get(position))

    def draw_yellow_counters(self, unit, position):
        if unit.yellow_counters:
            pygame.draw.circle(self.screen, grey, yellow_counter_coords.get(position), 10, 0)
            pygame.draw.circle(self.screen, yellow, yellow_counter_coords.get(position), 8, 0)

    def draw_blue_counters(self, unit, position):
        if unit.blue_counters:
            pygame.draw.circle(self.screen, grey, blue_counter_coords.get(position), 10, 0)
            pygame.draw.circle(self.screen, blue, blue_counter_coords.get(position), 8, 0)

            if unit.blue_counters > 1:
                label = self.font.render(str(unit.blue_counters), 1, black)
                self.screen.blit(label, blue_font_coords.get(position))

    def draw_bribed(self, unit, position):
        if hasattr(unit, "bribed"):
            pic = self.get_image("./other/ability.gif")
            self.screen.blit(pic, symbol_coords.get(position))

    def draw_crusading(self, unit, position):
        if hasattr(unit, "is_crusading"):
            pic = self.get_image("./other/flag.gif")
            self.screen.blit(pic, flag_coords.get(position))

    def draw_unit(self, unit, position, color):
        pic = self.get_image("./units_small/" + self.get_unit_pic(unit.name, color))
        self.screen.blit(pic, base_coords.get(position))

        self.draw_attack_counters(unit, position)
        self.draw_defence_counters(unit, position)
        self.draw_xp(unit, position)

        self.draw_yellow_counters(unit, position)
        self.draw_blue_counters(unit, position)

        self.draw_crusading(unit, position)
        self.draw_bribed(unit, position)

    def draw_game(self, gamestate):

        pic = self.get_image("./other/board.gif")
        self.screen.blit(pic, (0, 0))

        for position, unit in gamestate.units[0].items():
            self.draw_unit(unit, position, gamestate.current_player().color)

        for position, unit in gamestate.units[1].items():
            self.draw_unit(unit, position, gamestate.players[1].color)

        pygame.display.update()

    def draw_action(self, action):
        pygame.draw.circle(self.screen, black, center_coords.get(action.start_position), 10)
        pygame.draw.line(self.screen,
                         black,
                         center_coords.get(action.start_position),
                         center_coords.get(action.end_position),
                         5)

        if action.is_attack:
            pygame.draw.line(self.screen,
                             black,
                             center_coords.get(action.end_position),
                             center_coords.get(action.attack_position),
                             5)
            if action.move_with_attack:
                pic = self.get_image("./other/moveattack.gif")
            else:
                pic = self.get_image("./other/attack.gif")

            if hasattr(action, "high_morale"):
                pic = self.get_image("./other/flag.gif")
                self.screen.blit(pic, flag_coords.get(action.end_position))

            self.screen.blit(pic, symbol_coords.get(action.attack_position))

        elif action.is_ability:
            pygame.draw.line(self.screen,
                             black,
                             center_coords.get(action.end_position),
                             center_coords.get(action.attack_position), 5)
            pic = self.get_image("./other/ability.gif")
            self.screen.blit(pic, symbol_coords.get(action.attack_position))

        else:
            pic = self.get_image("./other/move.gif")
            self.screen.blit(pic, symbol_coords.get(action.end_position))

        pygame.display.update()

    def get_unit_pic(self, name, color):
        return name.replace(" ", "-") + ",-" + color.lower() + ".jpg"

    def refresh(self):
        pygame.display.flip()
