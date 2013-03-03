from __future__ import division
import pygame, sys
from pygame.locals import *
import setup
import mover
import math
import os
import ai_module
import settings
import shutil
import os
import ai_methods


pause_for_animation = settings.pause_for_animation

black = (0, 0, 0)
white = (255, 255, 255)
green = (0, 255, 0)
red = (255, 0, 0)
brown = (128, 64, 0)
grey = (48, 48, 48)
yellow = (200, 200, 0)
lightgrey = (223, 223, 223)
blue = (0, 102, 204)

unit_width = 70
unit_height = 106.5
board_size = [391, 908]
x_border = 22
y_border_top = 22
y_border_bottom = 39



def get_position(coords):
    x = int((coords[0] - x_border) / unit_width) +1
    if coords[1] > 454:
        y = 8 - int((coords[1] - y_border_bottom) / unit_height)
    else:
        y = 8 - int((coords[1] - y_border_top) / unit_height)
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
            
        return ( int((pos[0] -1) * unit_width + x_border + self.add_x), int(( 8 - pos[1]) * unit_height + + y_border + self.add_y))

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
def get_image(path, type = None):
        global _image_library
        image = _image_library.get(path)
        if image == None:
                image = pygame.image.load(path).convert()
                _image_library[path] = image
        return image    



def draw_acounters(unit, pos):
    
    if unit.acounters:
        pygame.draw.circle(screen, grey, acounter_coords.get(pos), 10, 0)
        pygame.draw.circle(screen, brown, acounter_coords.get(pos), 8, 0)
        if unit.acounters != 1:
            label = font.render(str(unit.acounters), 1, black)
            screen.blit(label, afont_coords.get(pos)) 


def draw_dcounters(unit, pos):
    
    if hasattr(unit, "sabotaged"):
        dcounters = -1
    else:
        dcounters = unit.dcounters
    
    if dcounters:
        pygame.draw.circle(screen, grey, dcounter_coords.get(pos), 10, 0)
        pygame.draw.circle(screen, lightgrey, dcounter_coords.get(pos), 8, 0)
        
        if dcounters > 1:
            label = font.render(str(dcounters), 1, black)
            screen.blit(label, dfont_coords.get(pos))

        if dcounters < 0:
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
    if hasattr(unit, "just_bribed"):
        unit.bcounters = 1
        
        
def draw_unit(unit, pos):
    pic = get_image("./units_small/" + unit.pic.replace(" ", "-"))
    screen.blit(pic, base_coords.get(pos))

    draw_acounters(unit, pos)
    draw_dcounters(unit, pos)
    draw_xp(unit, pos)
 
    add_ycounters(unit)
    draw_ycounters(unit, pos)
    
    add_bcounters(unit)
    draw_bcounters(unit, pos)
  
    draw_crusading(unit, pos)
    draw_bribed(unit, pos)
           
  


def draw_game(p):
    
    pic = get_image("./other/board.gif")
    screen.blit(pic, (0,0))
 
    for pos, unit in p[0].units.items() + p[1].units.items():
        draw_unit(unit, pos)

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
                unit.acounters += 1
                return

            if event.type == KEYDOWN and event.key == K_d:
                unit.dcounters += 1
                return


def get_input_abilities(unit, p):
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
                draw_game(p)
                return 0

            if event.type == KEYDOWN and event.key == K_2:
                draw_game(p)
                return 1



def pause():
    while True:
        for event in pygame.event.get():
            if event.type == KEYDOWN:
                return

def add_counters(p):
    for unit in p[0].units.values():
        if unit.xp == 2:
            if unit.defence + unit.dcounters == 4:
                unit.acounters += 1
            else:
                get_input_counter(unit)
               
            unit.xp = 0
            

def perform_action(action, p):
    
    if hasattr(p[0], "extra_action"):
        all_actions = mover.get_extra_actions(p)
    else:
        all_actions = mover.get_actions(p)
    
    matchco = 0
    for possible_action in all_actions:
        if action == possible_action:
            matchco += 1
            action = possible_action
 

    if matchco == 0:
        print "Action not allowed"
    
    elif matchco > 1:
        print "Action ambigious"
    
    else:
        
        draw_action(action)
        pygame.time.delay(pause_for_animation)
        
        mover.do_action(action, p)

        if settings.show_full_battle_result:
            print action.full_string()
        else:    
            print action.string_with_outcome()                 
        print

        if hasattr(p[0], "won"):
            game_end(p[0])

        draw_game(p)

        if p[0].ai == "Human":
            add_counters(p)
        else:
            p[0].ai.add_counters(p)
            
        draw_game(p)

        
        mover.initialize_action(p)
        
        if (p[0].actions_remaining < 1 or len(all_actions) == 1) and not hasattr(p[0], "extra_action"):
            p = [p[1], p[0]]
            if p[0].color == "Green":
                settings.turn += 1
            mover.initialize_turn(p)
          
        draw_game(p)
        
        if hasattr(p[0], "extra_action"):
            print p[0].color, "extra action"
        else:
            print p[0].color

    return p


def show_unit(p, pos):
    
    unit = None
    if pos in p[0].units:
        unit = p[0].units[pos]
    if pos in p[1].units:
        unit = p[1].units[pos]
        
    if unit:
        print
        print unit
        for attribute, value in unit.__dict__.items():
            if attribute not in ["has_ability", "has_attack", "name", "ycounters", "bcounters", "pic", "xp_gained_this_round", "color", "attack", "defence", "range", "movement"]:
                if value:
                    print attribute, value
        pic = get_image("./units_big/" + unit.pic.replace(" ", "-"))
        screen.blit(pic, (40,40))
        pygame.display.flip()
        
        while 1:
            for event in pygame.event.get():
                if event.type == pygame.MOUSEBUTTONDOWN or event.type == KEYDOWN:
                    draw_game(p)
                    return
    

def run_game():

    clock = pygame.time.Clock()
    
    p = setup.get_startunits()
    

    if settings.player1_ai != "Human":
        p[0].ai = ai_module.AI(settings.player1_ai, p[0])
    else:
        p[0].ai = "Human"
        
    if settings.player2_ai != "Human":
        p[1].ai = ai_module.AI(settings.player2_ai, p[1])
    else:
        p[1].ai = "Human"

    mover.initialize_turn([p[0], p[1]])
    mover.initialize_turn([p[1], p[0]])
    mover.initialize_action(p)
    draw_game(p)
   
    p[0].actions_remaining = 1
    print p[0].color
    startpos, endpos = None, None

    pygame.time.set_timer(USEREVENT + 1, 1000)

    if  os.path.exists("./replay"):
        shutil.rmtree('./replay')
    
    os.makedirs("./replay")
    
    while True:
        time_passed = clock.tick(50)
    
        for event in pygame.event.get():  
            
            if event.type == USEREVENT + 1:

                
                if p[0].ai != "Human":            
                    
                    pygame.image.save(screen, "./replay/" + p[0].color + " " + str(settings.turn) + "." + str(3 - p[0].actions_remaining) + ".jpeg")
                    action = p[0].ai.select_action(p)
                    if action:
                        p = perform_action(action, p)
                    else:
                        p = [p[1], p[0]]
                        if p[0].color == "Green":
                            settings.turn += 1
                        mover.initialize_turn(p)
                        
                    if hasattr(p[0], "extra_action"):
                        extra_action = p[0].ai.select_action(p)
                        p = perform_action(extra_action, p)
                            
    
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                x, y = get_position(event.pos)
                
                if not startpos and (x,y) in p[0].units:
                    print "Start at", (x,y)
                    startpos = (x,y)
                    p[0].unit = p[0].units[startpos]
                 
                elif startpos and not endpos and p[0].unit.has_ability:          
                    print "Ability", (x,y)
                    if len(p[0].unit.abilities) > 1:
                        index = get_input_abilities(p[0].unit, p)
                        action = mover.Action(p[0].unit, startpos, startpos, (x,y), False, False, True, p[0].unit.abilities[index])
                        p, startpos, endpos = perform_action(action, p), None, None
                    else:   
                        action = mover.Action(p[0].unit, startpos, startpos, (x,y), False, False, True, p[0].unit.abilities[0])
                        p, startpos, endpos = perform_action(action, p), None, None

                elif startpos and not endpos and (x,y) in p[1].units and p[0].unit.range > 1:
                    print "Attack", (x,y)

                    action = mover.Action(p[0].unit, startpos, startpos, (x,y), True, False)
                    p, startpos, endpos = perform_action(action, p), None, None            
                    
         
                elif startpos and not endpos and (x,y) in p[1].units and not p[0].unit.has_ability:
                    print "Attack-Move", (x,y)
                    
                    if hasattr(p[0], "extra_action"):
                        all_actions = mover.get_extra_actions(p)
                    else:
                        all_actions = mover.get_actions(p)
                    
                    action = None
                         
                    for possible_action in all_actions:
                        if possible_action.startpos == startpos and possible_action.attackpos == (x,y) and possible_action.move_with_attack:
                            if possible_action.endpos == startpos:
                                action = possible_action
                                break
                            action = possible_action

                    if not action:
                        print "Action not possible"
                        startpos, endpos = None, None
                    else:
                        p, startpos, endpos = perform_action(action, p), None, None
                
                elif startpos and not endpos:
                    print "Stop at", (x,y)
                    endpos = (x,y)
                   
                elif startpos and endpos and (x,y) in p[1].units:
                    print "Attack-Move", (x,y)
                    action = mover.Action(p[0].unit, startpos, endpos, (x,y), True, False)
                    p, startpos, endpos = perform_action(action, p), None, None
                    

                elif startpos and endpos and (x,y) not in p[1].units:
                    print "Move to", (x,y)
                    action = mover.Action(p[0].unit, startpos, (x,y), None, False, False)
                    p, startpos, endpos = perform_action(action, p), None, None
                    
       
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 2:
                x, y = get_position(event.pos)
                
                if startpos and (x,y) not in p[1].units:
                    print "Move to", (x,y)
                    action = mover.Action(p[0].unit, startpos, (x,y), None, False, False)
                    p, startpos, endpos = perform_action(action, p), None, None


                if startpos and (x,y) in p[1].units:
                    action = mover.Action(p[0].unit, startpos, (x,y), (x,y), True, False)
                    chance_of_win = ai_methods.chance_of_win(p[0].unit, p[1].units[(x,y)], action)
                    print "Chance of win", round(chance_of_win *100), "%"
                    startpos = None
                    


            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 3:   
                x, y = get_position(event.pos)
                
                if not startpos:
                    show_unit(p, (x,y))  
                
                elif startpos and not endpos and (x,y) in p[1].units:
                    print "Attack", (x,y)
                    
                    if hasattr(p[0], "extra_action"):
                        all_actions = mover.get_extra_actions(p)
                    else:
                        all_actions = mover.get_actions(p)
                    
                    action = None
                         
                    for possible_action in all_actions:
                        if possible_action.startpos == startpos and possible_action.attackpos == (x,y) and not possible_action.move_with_attack:
                            if possible_action.endpos == startpos:
                                action = possible_action
                                break
                            action = possible_action
                    
                    if not action:
                        print "Action not possible"
                        startpos, endpos = None, None
                    else:
                        p, startpos, endpos = perform_action(action, p), None, None

            if event.type == KEYDOWN and event.key == K_p:
                print "paused"
                pause()
                
  
            if event.type == KEYDOWN and event.key == K_a:
                print
                print "Possible actions:"
                if hasattr(p[0], "extra_action"):
                    actions = mover.get_extra_actions(p)
                    for action in actions:
                        print action
                else:
                    p[0].actions = mover.get_actions(p)
                    for action in p[0].actions:
                        print action
                print
                        
            if event.type == KEYDOWN and event.key == K_ESCAPE:
                print "move cleared"
                startpos, endpos = None, None

            elif event.type == KEYDOWN and command_q_down(event.key):
                exit_game();
    
            elif event.type == QUIT:
                exit_game()

            
            pygame.display.flip()


def command_q_down(key):
    return key == K_q and (pygame.key.get_mods() & KMOD_LMETA or pygame.key.get_mods() & KMOD_RMETA)

def exit_game():
    sys.exit()

def game_end(player):
    font = pygame.font.SysFont("monospace", 55, bold = True)
    label = font.render(player.color + "\nWins", 1, black)
    screen.blit(label, (40, 400))
    pygame.display.update()
    pygame.time.delay(400000)
    exit_game()


if __name__ == '__main__':
    pygame.init()
    screen = pygame.display.set_mode(board_size)
    font = pygame.font.SysFont("arial", 18, True, False)
    font_big = pygame.font.SysFont("arial", 28, True, False)
    
    run_game()
