from __future__ import division
import pygame, sys
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
    
    def get(self, pos):
        if pos[1] >= 5:
            y_border = y_border_top
        else:
            y_border = y_border_bottom
            
        return int((pos[0] - 1) * unit_width + x_border + self.add_x), int((8 - pos[1]) * unit_height + y_border + self.add_y)

base_coords = Coordinates(0, 0)
center_coords = Coordinates(35, 53.2)
symbol_coords = Coordinates(13, 38.2)
acounter_coords = Coordinates(50, 78)
dcounter_coords = Coordinates(50, 58)
dfont_coords = Coordinates(45, 48)
flag_coords = Coordinates(46, 10)
ycounter_coords = Coordinates(50, 38)
bcounter_coords = Coordinates(50, 18)
star_coords = Coordinates(8, 58)
bfont_coords = Coordinates(45, 8)
afont_coords = Coordinates(45, 68)


_image_library = {}


def get_image(path):
        global _image_library
        image = _image_library.get(path)
        if not image:
                image = pygame.image.load(path).convert()
                _image_library[path] = image
        return image    


def draw_attack_counters(unit, pos):
    if unit.attack_counters:
        pygame.draw.circle(screen, grey, acounter_coords.get(pos), 10, 0)
        pygame.draw.circle(screen, brown, acounter_coords.get(pos), 8, 0)
        if unit.attack_counters != 1:
            label = font.render(str(unit.attack_counters), 1, black)
            screen.blit(label, afont_coords.get(pos)) 


def draw_defence_counters(unit, pos):
    
    if hasattr(unit, "sabotaged"):
        defence_counters = -1
    else:
        defence_counters = unit.defence_counters
    
    if defence_counters:
        pygame.draw.circle(screen, grey, dcounter_coords.get(pos), 10, 0)
        pygame.draw.circle(screen, light_grey, dcounter_coords.get(pos), 8, 0)
        
        if defence_counters > 1:
            label = font.render(str(defence_counters), 1, black)
            screen.blit(label, dfont_coords.get(pos))

        if defence_counters < 0:
            label = font.render("x", 1, black)
            screen.blit(label, dfont_coords.get(pos))    


def draw_xp(unit, pos):           
    if unit.xp == 1:
        pic = get_image("./other/star.gif")
        screen.blit(pic, star_coords.get(pos))


def draw_ycounters(unit, pos):
    
    if unit.ycounters:
        pygame.draw.circle(screen, grey, ycounter_coords.get(pos), 10, 0)
        pygame.draw.circle(screen, yellow, ycounter_coords.get(pos), 8, 0)   


def draw_bcounters(unit, pos):
    if unit.bcounters:
        pygame.draw.circle(screen, grey, bcounter_coords.get(pos), 10, 0)
        pygame.draw.circle(screen, blue, bcounter_coords.get(pos), 8, 0)

        if unit.bcounters > 1:
            label = font.render(str(unit.bcounters), 1, black)
            screen.blit(label, bfont_coords.get(pos))     


def draw_bribed(unit, pos):                 
    if hasattr(unit, "bribed"):
        pic = get_image("./other/ability.gif")
        screen.blit(pic, symbol_coords.get(pos))  


def draw_crusading(unit, pos):           
    if hasattr(unit, "is_crusading"):
        pic = get_image("./other/flag.gif")
        screen.blit(pic, flag_coords.get(pos))      


def add_ycounters(unit):
    if hasattr(unit, "extra_life"): unit.ycounters = 1
    else: unit.ycounters = 0


def add_bcounters(unit):
    unit.bcounters = 0
    if hasattr(unit, "frozen"):
        unit.bcounters = unit.frozen
    if hasattr(unit, "attack_frozen"):
        unit.bcounters = unit.attack_frozen
    if hasattr(unit, "just_bribed"):
        unit.bcounters = 1


def get_unit_pic(name, color):
    return name.replace(" ", "-") + ",-" + color.lower() + ".jpg"


def draw_unit(unit, pos, color):
    pic = get_image("./units_small/" + get_unit_pic(unit.name, color))
    screen.blit(pic, base_coords.get(pos))

    draw_attack_counters(unit, pos)
    draw_defence_counters(unit, pos)
    draw_xp(unit, pos)
 
    add_ycounters(unit)
    draw_ycounters(unit, pos)
    
    add_bcounters(unit)
    draw_bcounters(unit, pos)
  
    draw_crusading(unit, pos)
    draw_bribed(unit, pos)


def draw_game(g):
    
    pic = get_image("./other/board.gif")
    screen.blit(pic, (0, 0))
 
    for pos, unit in g.units[0].items():
        draw_unit(unit, pos, g.players[0].color)

    for pos, unit in g.units[1].items():
        draw_unit(unit, pos, g.players[1].color)

    pygame.display.update()  


def draw_action(action):
    pygame.draw.circle(screen, black, center_coords.get(action.startpos), 10)
    pygame.draw.line(screen, black, center_coords.get(action.startpos), center_coords.get(action.endpos), 5)
    
    if action.is_attack:
        pygame.draw.line(screen, black, center_coords.get(action.endpos), center_coords.get(action.attackpos), 5)
        if action.move_with_attack:
            pic = get_image("./other/moveattack.gif")
        else:
            pic = get_image("./other/attack.gif")

        if hasattr(action, "high_morale"):
            pic = get_image("./other/flag.gif")
            screen.blit(pic, flag_coords.get(action.endpos))    

        screen.blit(pic, symbol_coords.get(action.attackpos))

    elif action.is_ability:
        pygame.draw.line(screen, black, center_coords.get(action.endpos), center_coords.get(action.attackpos), 5)
        pic = get_image("./other/ability.gif")
        screen.blit(pic, symbol_coords.get(action.attackpos))      

    else:
            pic = get_image("./other/move.gif")
            screen.blit(pic, symbol_coords.get(action.endpos))
    
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
        
        if (g.players[0].actions_remaining < 1 or len(all_actions) == 1) and not hasattr(g.players[0], "extra_action"):
            g.turn_shift()
          
        draw_game(g)
        
        if hasattr(g.players[0], "extra_action"):
            print g.players[0].color, "extra action"
        else:
            print g.players[0].color

    return g


def show_unit(pos, g):
    
    unit = color = None
    if pos in g.units[0]:
        unit = g.units[0][pos]
        color = g.players[0].color
    if pos in g.units[1]:
        unit = g.units[1][pos]
        color = g.players[1].color
        
    if unit:
        print
        print unit
        for attribute, value in unit.__dict__.items():
            if attribute not in ["name", "ycounters", "bcounters", "pic",
                                 "color", "range", "movement"]:
                if value:
                    print attribute, value
        pic = get_image("./units_big/" + get_unit_pic(unit.name, color))
        screen.blit(pic, (40, 40))
        pygame.display.flip()
        
        while 1:
            for event in pygame.event.get():
                if event.type == pygame.MOUSEBUTTONDOWN or event.type == KEYDOWN:
                    draw_game(g)
                    return


def run_game(g):

    g.set_ais()

    pygame.time.set_timer(USEREVENT + 1, 1000)
    startpos, endpos = None, None

    draw_game(g)

    while True:
        for event in pygame.event.get():

            if event.type == USEREVENT + 1:

                if g.players[0].ai_name != "Human":

                    print "turn", g.turn
                    print "action", 3 - g.players[0].actions_remaining
                    print

                    pygame.image.save(screen, "./replay/" + g.players[0].color + " " + str(settings.turn) + "." +
                                              str(3 - g.players[0].actions_remaining) + ".jpeg")
                    action = g.players[0].ai.select_action(g)
                    if action:
                        g = perform_action(action, g)
                    else:
                        g.next_turn()
                        draw_game(g)

                    if hasattr(g.players[0], "extra_action"):
                        extra_action = g.players[0].ai.select_action(g)
                        g = perform_action(extra_action, g)

            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                x, y = get_pixel_position(event.pos)

                if not startpos and (x, y) in g.units[0]:
                    print "Start at", (x, y)
                    startpos = (x, y)
                    selected_unit = g.units[0][startpos]

                elif startpos and not endpos and ((x, y) in g.units[1] or (x, y) in g.units[0]) and \
                        selected_unit.abilities:
                    print "Ability", (x, y)
                    if len(selected_unit.abilities) > 1:
                        index = get_input_abilities(g.selected_unit)
                        action = Action(startpos, startpos, (x, y), False, False, True, selected_unit.abilities[index])
                    else:
                        action = Action(startpos, startpos, (x, y), False, False, True, selected_unit.abilities[0])
                    g, startpos, endpos = perform_action(action, g), None, None

                elif startpos and not endpos and (x, y) in g.units[1] and selected_unit.range > 1:
                    print "Attack", (x, y)
                    action = Action(startpos, startpos, (x, y), True, False)
                    g, startpos, endpos = perform_action(action, g), None, None

                elif startpos and not endpos and (x, y) in g.units[1]:
                    print "Attack-Move", (x, y)

                    if hasattr(g.players[0], "extra_action"):
                        all_actions = g.get_actions()
                    else:
                        all_actions = g.get_actions()

                    action = None

                    for possible_action in all_actions:
                        if possible_action.startpos == startpos and possible_action.attackpos == (x, y) and \
                                possible_action.move_with_attack:
                            if possible_action.endpos == startpos:
                                action = possible_action
                                break
                            action = possible_action

                    if not action:
                        print "Action not possible"
                        startpos, endpos = None, None
                    else:
                        g, startpos, endpos = perform_action(action, g), None, None

                elif startpos and not endpos:
                    print "Stop at", (x, y)
                    endpos = (x, y)

                elif startpos and endpos and (x, y) in g.units[1]:
                    print "Attack-Move", (x, y)
                    action = Action(startpos, endpos, (x, y), True, False)

                    g, startpos, endpos = perform_action(action, g), None, None

                elif startpos and endpos and (x, y) not in g.units[1]:
                    print "Move to", (x, y)
                    action = Action(startpos, (x, y), None, False, False)
                    g, startpos, endpos = perform_action(action, g), None, None

            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 2:
                x, y = get_pixel_position(event.pos)

                if startpos and (x, y) not in g.units[1]:
                    print "Move to", (x, y)
                    action = Action(startpos, (x, y), None, False, False)
                    g, startpos, endpos = perform_action(action, g), None, None

                if startpos and (x, y) in g.units[1]:
                    action = Action(startpos, (x, y), (x, y), True, False)
                    chance_of_win = ai_methods.chance_of_win(selected_unit, g.units[1][(x, y)], action)
                    print "Chance of win", round(chance_of_win * 100), "%"
                    startpos = None

            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 3:
                x, y = get_pixel_position(event.pos)

                if not startpos:
                    show_unit((x, y), g)

                elif startpos and not endpos and (x, y) in g.units[1]:
                    print "Attack", (x, y)

                    if hasattr(g.players[0], "extra_action"):
                        all_actions = g.get_actions()
                    else:
                        all_actions = g.get_actions()

                    action = None

                    for possible_action in all_actions:
                        if possible_action.startpos == startpos and possible_action.attackpos == (x, y) and not possible_action.move_with_attack:

                            if possible_action.endpos == startpos:
                                action = possible_action
                                break
                            action = possible_action

                    if not action:
                        print "Action not possible"
                        startpos, endpos = None, None
                    else:
                        g, startpos, endpos = perform_action(action, g), None, None

                elif startpos and endpos and (x, y) in g.units[1]:
                    print "Attack", (x, y)
                    action = Action(startpos, endpos, (x, y), True, False)
                    g, startpos, endpos = perform_action(action, g), None, None

            if event.type == KEYDOWN and event.key == K_p:
                print "paused"
                pause()

            if event.type == KEYDOWN and event.key == K_a:
                print
                print "Possible actions:"
                if hasattr(g.players[0], "extra_action"):
                    actions = g.get_actions()
                    for action in actions:
                        print action
                else:
                    actions = g.get_actions()
                    for action in actions:
                        print action
                print

            if event.type == KEYDOWN and event.key == K_ESCAPE:
                print "move cleared"
                startpos, endpos, selected_unit = None, None, None

            elif event.type == KEYDOWN and command_q_down(event.key):
                exit_game()

            elif event.type == QUIT:
                exit_game()

            pygame.display.flip()


def new_game():

    player1, player2 = Player("Green"), Player("Red")

    player1.ai_name, player2.ai_name = settings.player1_ai, settings.player2_ai

    player1_units, player2_units = setup.get_start_units()

    gamestate = Gamestate(player1, player1_units, player2, player2_units)

    gamestate.initialize_turn()
    gamestate.initialize_action()

    player1.actions_remaining = 1
    player2.actions_remaining = 0

    if  os.path.exists("./replay"):
        shutil.rmtree('./replay')
    
    os.makedirs("./replay")

    run_game(gamestate)


def command_q_down(key):
    return key == K_q and (pygame.key.get_mods() & KMOD_LMETA or pygame.key.get_mods() & KMOD_RMETA)


def exit_game():
    sys.exit()


def game_end(player):
    font = pygame.font.SysFont("monospace", 55, bold = True)
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

