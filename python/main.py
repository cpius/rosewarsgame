from __future__ import division
import pygame
import sys
from pygame.locals import *
import setup
from gamestate_module import Gamestate
import os
import settings
import shutil
import ai_methods
from player import Player
from action import Action

pause_for_animation = settings.pause_for_animation

action_index = 1

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


def get_pixel_position(coordinates):
    x = int((coordinates[0] - x_border) / unit_width) + 1
    if coordinates[1] > 454:
        y = 8 - int((coordinates[1] - y_border_bottom) / unit_height)
    else:
        y = 8 - int((coordinates[1] - y_border_top) / unit_height)
    return x, y


class Coordinates(object):
    def __init__(self, x, y):
        self.add_x = x
        self.add_y = y
    
    def get(self, position):
        if position[1] >= 5:
            y_border = y_border_top
        else:
            y_border = y_border_bottom
            
        return int((position[0] - 1) * unit_width + x_border + self.add_x), int((8 - position[1]) * unit_height + y_border + self.add_y)

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


def get_image(path):
        global _image_library
        image = _image_library.get(path)
        if not image:
                image = pygame.image.load(path).convert()
                _image_library[path] = image
        return image    


def draw_attack_counters(unit, position):
    if unit.attack_counters:
        pygame.draw.circle(screen, grey, attack_counter_coords.get(position), 10, 0)
        pygame.draw.circle(screen, brown, attack_counter_coords.get(position), 8, 0)
        if unit.attack_counters != 1:
            label = font.render(str(unit.attack_counters), 1, black)
            screen.blit(label, attack_font_coords.get(position))


def draw_defence_counters(unit, position):
    
    if hasattr(unit, "sabotaged"):
        defence_counters = -1
    else:
        defence_counters = unit.defence_counters
    
    if defence_counters:
        pygame.draw.circle(screen, grey, defence_counter_coords.get(position), 10, 0)
        pygame.draw.circle(screen, light_grey, defence_counter_coords.get(position), 8, 0)
        
        if defence_counters > 1:
            label = font.render(str(defence_counters), 1, black)
            screen.blit(label, defence_font_coords.get(position))

        if defence_counters < 0:
            label = font.render("x", 1, black)
            screen.blit(label, defence_font_coords.get(position))


def draw_xp(unit, position):
    if unit.xp == 1:
        pic = get_image("./other/star.gif")
        screen.blit(pic, star_coords.get(position))


def draw_yellow_counters(unit, position):
    
    if unit.yellow_counters:
        pygame.draw.circle(screen, grey, yellow_counter_coords.get(position), 10, 0)
        pygame.draw.circle(screen, yellow, yellow_counter_coords.get(position), 8, 0)


def draw_blue_counters(unit, position):
    if unit.blue_counters:
        pygame.draw.circle(screen, grey, blue_counter_coords.get(position), 10, 0)
        pygame.draw.circle(screen, blue, blue_counter_coords.get(position), 8, 0)

        if unit.blue_counters > 1:
            label = font.render(str(unit.blue_counters), 1, black)
            screen.blit(label, blue_font_coords.get(position))


def draw_bribed(unit, position):
    if hasattr(unit, "bribed"):
        pic = get_image("./other/ability.gif")
        screen.blit(pic, symbol_coords.get(position))


def draw_crusading(unit, position):
    if hasattr(unit, "is_crusading"):
        pic = get_image("./other/flag.gif")
        screen.blit(pic, flag_coords.get(position))


def add_yellow_counters(unit):
    if hasattr(unit, "extra_life"):
        unit.yellow_counters = 1
    else:
        unit.yellow_counters = 0


def add_blue_counters(unit):
    unit.blue_counters = 0
    if hasattr(unit, "frozen"):
        unit.blue_counters = unit.frozen
    if hasattr(unit, "attack_frozen"):
        unit.blue_counters = unit.attack_frozen
    if hasattr(unit, "just_bribed"):
        unit.blue_counters = 1


def get_unit_pic(name, color):
    return name.replace(" ", "-") + ",-" + color.lower() + ".jpg"


def draw_unit(unit, position, color):
    pic = get_image("./units_small/" + get_unit_pic(unit.name, color))
    screen.blit(pic, base_coords.get(position))

    draw_attack_counters(unit, position)
    draw_defence_counters(unit, position)
    draw_xp(unit, position)
 
    add_yellow_counters(unit)
    draw_yellow_counters(unit, position)
    
    add_blue_counters(unit)
    draw_blue_counters(unit, position)
  
    draw_crusading(unit, position)
    draw_bribed(unit, position)


def draw_game(gamestate):
    
    pic = get_image("./other/board.gif")
    screen.blit(pic, (0, 0))
 
    for position, unit in gamestate.units[0].items():
        draw_unit(unit, position, gamestate.players[0].color)

    for position, unit in gamestate.units[1].items():
        draw_unit(unit, position, gamestate.players[1].color)

    pygame.display.update()  


def draw_action(action):
    pygame.draw.circle(screen, black, center_coords.get(action.start_position), 10)
    pygame.draw.line(screen,
                     black,
                     center_coords.get(action.start_position),
                     center_coords.get(action.end_position),
                     5)
    
    if action.is_attack:
        pygame.draw.line(screen,
                         black,
                         center_coords.get(action.end_position),
                         center_coords.get(action.attack_position),
                         5)
        if action.move_with_attack:
            pic = get_image("./other/moveattack.gif")
        else:
            pic = get_image("./other/attack.gif")

        if hasattr(action, "high_morale"):
            pic = get_image("./other/flag.gif")
            screen.blit(pic, flag_coords.get(action.end_position))

        screen.blit(pic, symbol_coords.get(action.attack_position))

    elif action.is_ability:
        pygame.draw.line(screen,
                         black,
                         center_coords.get(action.end_position),
                         center_coords.get(action.attack_position), 5)
        pic = get_image("./other/ability.gif")
        screen.blit(pic, symbol_coords.get(action.attack_position))

    else:
            pic = get_image("./other/move.gif")
            screen.blit(pic, symbol_coords.get(action.end_position))
    
    pygame.display.update()


def get_input_counter(unit):
    label = font_big.render("Select counter for " + unit.name, 1, black)
    screen.blit(label, (20, 400))
    label = font_big.render("'a' for attack, 'd' for defence", 1, black)
    screen.blit(label, (20, 435))
    pygame.display.update()

    while True:
        for event in pygame.event.get():
            if event.type == KEYDOWN and event.key == K_a:
                unit.attack_counters += 1
                return

            if event.type == KEYDOWN and event.key == K_d:
                unit.defence_counters += 1
                return


def get_input_abilities(unit):
    label = font_big.render("Select ability:", 1, black)
    screen.blit(label, (130, 400))
    label = font_big.render("1 for " + unit.abilities[0], 1, black)
    screen.blit(label, (130, 435))
    label = font_big.render("2 for " + unit.abilities[1], 1, black)
    screen.blit(label, (130, 470))
    pygame.display.update()
    while True:
        for event in pygame.event.get():
            if event.type == KEYDOWN and event.key == K_1:
                return 0

            if event.type == KEYDOWN and event.key == K_2:
                return 1


def pause():
    while True:
        for event in pygame.event.get():
            if event.type == QUIT:
                exit_game()
            elif event.type == KEYDOWN or event.type == pygame.MOUSEBUTTONDOWN:
                return


def add_counters(units):
    for unit in units.values():
        if unit.xp == 2:
            if unit.defence + unit.defence_counters == 4:
                unit.attack_counters += 1
            else:
                get_input_counter(unit)
               
            unit.xp = 0
            

def perform_action(action, g):
    
    if hasattr(g.players[0], "extra_action"):
        all_actions = g.get_actions()
    else:
        all_actions = g.get_actions()
    
    matchco = 0
    for possible_action in all_actions:
        if action == possible_action:
            matchco += 1
            action = possible_action

    if matchco == 0:
        print "Action not allowed"
    
    elif matchco > 1:
        print "Action ambiguous"
    
    else:
        
        draw_action(action)
        pygame.time.delay(pause_for_animation)

        g.do_action(action)

        save_game(g)

        if settings.show_full_battle_result:
            print action.full_string()
        else:    
            print action.string_with_outcome()
        print

        if hasattr(g.players[0], "won"):
            game_end(g.players[0])

        draw_game(g)

        if g.players[0].ai_name == "Human":
            add_counters(g.units[0])
        else:
            g.players[0].ai.add_counters(g)
            
        draw_game(g)

        g.initialize_action()
        
        if (g.get_actions_remaining() < 1 or len(all_actions) == 1) and not hasattr(g.players[0], "extra_action"):
            g.turn_shift()
          
        draw_game(g)
        
        if hasattr(g.players[0], "extra_action"):
            print g.players[0].color, "extra action"
        else:
            print g.players[0].color

    return g


def show_unit(position, gamestate):
    
    unit = color = None
    if position in gamestate.units[0]:
        unit = gamestate.units[0][position]
        color = gamestate.players[0].color
    if position in gamestate.units[1]:
        unit = gamestate.units[1][position]
        color = gamestate.players[1].color
        
    if unit:
        print
        print unit
        for attribute, value in unit.__dict__.items():
            if attribute not in ["name", "yellow_counters", "blue_counters", "pic",
                                 "color", "range", "movement"]:
                if value:
                    print attribute, value
        pic = get_image("./units_big/" + get_unit_pic(unit.name, color))
        screen.blit(pic, (40, 40))
        pygame.display.flip()
        
        while 1:
            for event in pygame.event.get():
                if event.type == pygame.MOUSEBUTTONDOWN or event.type == KEYDOWN:
                    draw_game(gamestate)
                    return


def save_game(gamestate):
    global action_index

    name = str(action_index) + ". "\
                             + gamestate.players[0].color\
                             + ", "\
                             + str(gamestate.turn)\
                             + "."\
                             + str(2 - gamestate.get_actions_remaining())
    pygame.image.save(screen, "./replay/" + name + ".jpeg")

    action_index += 1


def run_game(gamestate):

    gamestate.set_ais()

    pygame.time.set_timer(USEREVENT + 1, 1000)
    start_position, end_position = None, None

    draw_game(gamestate)

    while True:
        for event in pygame.event.get():

            if event.type == USEREVENT + 1:

                if gamestate.players[0].ai_name != "Human":

                    print "turn", gamestate.turn
                    print "action", 3 - gamestate.get_actions_remaining()
                    print

                    action = gamestate.players[0].ai.select_action(gamestate)
                    if action:
                        gamestate = perform_action(action, gamestate)
                    else:
                        gamestate.turn_shift()
                        draw_game(gamestate)

                    if hasattr(gamestate.players[0], "extra_action"):
                        extra_action = gamestate.players[0].ai.select_action(gamestate)
                        gamestate = perform_action(extra_action, gamestate)

            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                x, y = get_pixel_position(event.pos)

                if not start_position and (x, y) in gamestate.units[0]:
                    print "Start at", (x, y)
                    start_position = (x, y)
                    selected_unit = gamestate.units[0][start_position]

                elif start_position and not end_position and ((x, y) in gamestate.units[1] or (x, y) in gamestate.units[0]) and \
                        selected_unit.abilities:
                    print "Ability", (x, y)
                    if len(selected_unit.abilities) > 1:
                        index = get_input_abilities(selected_unit)
                        action = Action(start_position, start_position, (x, y), False, False, True, selected_unit.abilities[index])
                    else:
                        action = Action(start_position, start_position, (x, y), False, False, True, selected_unit.abilities[0])
                    gamestate, start_position, end_position = perform_action(action, gamestate), None, None

                elif start_position and not end_position and (x, y) in gamestate.units[1] and selected_unit.range > 1:
                    print "Attack", (x, y)
                    action = Action(start_position, start_position, (x, y), True, False)
                    gamestate, start_position, end_position = perform_action(action, gamestate), None, None

                elif start_position and not end_position and (x, y) in gamestate.units[1]:
                    print "Attack-Move", (x, y)

                    if hasattr(gamestate.players[0], "extra_action"):
                        all_actions = gamestate.get_actions()
                    else:
                        all_actions = gamestate.get_actions()

                    action = None

                    for possible_action in all_actions:
                        if possible_action.start_position == start_position and possible_action.attack_position == (x, y) and \
                                possible_action.move_with_attack:
                            if possible_action.end_position == start_position:
                                action = possible_action
                                break
                            action = possible_action

                    if not action:
                        print "Action not possible"
                        start_position, end_position = None, None
                    else:
                        gamestate, start_position, end_position = perform_action(action, gamestate), None, None

                elif start_position and not end_position:
                    print "Stop at", (x, y)
                    end_position = (x, y)

                elif start_position and end_position and (x, y) in gamestate.units[1]:
                    print "Attack-Move", (x, y)
                    action = Action(start_position, end_position, (x, y), True, False)

                    gamestate, start_position, end_position = perform_action(action, gamestate), None, None

                elif start_position and end_position and (x, y) not in gamestate.units[1]:
                    print "Move to", (x, y)
                    action = Action(start_position, (x, y), None, False, False)
                    gamestate, start_position, end_position = perform_action(action, gamestate), None, None

            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 2:
                x, y = get_pixel_position(event.pos)

                if start_position and (x, y) not in gamestate.units[1]:
                    print "Move to", (x, y)
                    action = Action(start_position, (x, y), None, False, False)
                    gamestate, start_position, end_position = perform_action(action, gamestate), None, None

                if start_position and (x, y) in gamestate.units[1]:
                    action = Action(start_position, (x, y), (x, y), True, False)
                    chance_of_win = ai_methods.chance_of_win(selected_unit, gamestate.units[1][(x, y)], action)
                    print "Chance of win", round(chance_of_win * 100), "%"
                    start_position = None

            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 3:
                x, y = get_pixel_position(event.pos)

                if not start_position:
                    show_unit((x, y), gamestate)

                elif start_position and not end_position and (x, y) in gamestate.units[1]:
                    print "Attack", (x, y)

                    if hasattr(gamestate.players[0], "extra_action"):
                        all_actions = gamestate.get_actions()
                    else:
                        all_actions = gamestate.get_actions()

                    action = None

                    for possible_action in all_actions:
                        if possible_action.start_position == start_position \
                                and possible_action.attack_position == (x, y) \
                                and not possible_action.move_with_attack:

                            if possible_action.end_position == start_position:
                                action = possible_action
                                break
                            action = possible_action

                    if not action:
                        print "Action not possible"
                        start_position, end_position = None, None
                    else:
                        gamestate, start_position, end_position = perform_action(action, gamestate), None, None

                elif start_position and end_position and (x, y) in gamestate.units[1]:
                    print "Attack", (x, y)
                    action = Action(start_position, end_position, (x, y), True, False)
                    gamestate, start_position, end_position = perform_action(action, gamestate), None, None

            if event.type == KEYDOWN and event.key == K_p:
                print "paused"
                pause()

            if event.type == KEYDOWN and event.key == K_a:
                print
                print "Possible actions:"
                if hasattr(gamestate.players[0], "extra_action"):
                    actions = gamestate.get_actions()
                    for action in actions:
                        print action
                else:
                    actions = gamestate.get_actions()
                    for action in actions:
                        print action
                print

            if event.type == KEYDOWN and event.key == K_ESCAPE:
                print "move cleared"
                start_position, end_position, selected_unit = None, None, None

            elif event.type == KEYDOWN and command_q_down(event.key):
                exit_game()

            elif event.type == QUIT:
                exit_game()

            pygame.display.flip()


def new_game():

    player1 = Player("Green")
    player2 = Player("Red")

    player1.ai_name = settings.player1_ai
    player2.ai_name = settings.player2_ai

    player1_units, player2_units = setup.get_start_units()

    gamestate = Gamestate(player1, player1_units, player2, player2_units)

    gamestate.initialize_turn()
    gamestate.initialize_action()

    gamestate.set_actions_remaining(1)

    if  os.path.exists("./replay"):
        shutil.rmtree('./replay')
    
    os.makedirs("./replay")

    run_game(gamestate)


def command_q_down(key):
    return key == K_q and (pygame.key.get_mods() & KMOD_LMETA or pygame.key.get_mods() & KMOD_RMETA)


def exit_game():
    sys.exit()


def game_end(player):
    font = pygame.font.SysFont("monospace", 55, bold=True)
    label = font.render(player.color + "\nWins", 1, black)
    screen.blit(label, (40, 400))
    pygame.display.update()
    pause()
    exit_game()


pygame.init()
screen = pygame.display.set_mode(board_size)
font = pygame.font.SysFont("arial", 18, True, False)
font_big = pygame.font.SysFont("arial", 28, True, False)


if __name__ == '__main__':

    new_game()
