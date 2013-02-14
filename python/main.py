from __future__ import division
import pygame, sys
from pygame.locals import *
import setup
import mover
import math
import os
import ai_module

pause_for_animation = 350

player1_ai = "Destroyer"
player2_ai = "Advancer"

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

_image_library = {}

def get_image(path, type = None):
        global _image_library
        image = _image_library.get(path)
        if image == None:
                image = pygame.image.load(path).convert()
                _image_library[path] = image
        return image    
    
def base_pos(pos):    
    if pos[1] < 5:
        return (22 + (pos[0] - 1) * unit_width, 22 + (pos[1] - 1) * unit_height)
    else:
        return (22 + (pos[0] - 1) * unit_width, 39 + (pos[1] - 1) * unit_height)

def center_pos(pos):
    return (int(base_pos(pos)[0] + unit_width / 2), int(base_pos(pos)[1] + unit_height / 2))

def symbol_pos(pos):
    return (base_pos(pos)[0] - 22 + unit_width / 2, base_pos(pos)[1] - 15 + unit_height / 2)
  
def acounter_pos(pos):
    return (int(base_pos(pos)[0] + 50), int(base_pos(pos)[1] + 78))

def dfont_pos(pos):
    return (int(base_pos(pos)[0] + 45), int(base_pos(pos)[1] + 48))

def dcounter_pos(pos):
    return (int(base_pos(pos)[0] + 50), int(base_pos(pos)[1] + 58))

def flag_pos(pos):
    return (int(base_pos(pos)[0] + 46), int(base_pos(pos)[1] + 10))

def ycounter_pos(pos):
    return (int(base_pos(pos)[0] + 50), int(base_pos(pos)[1] + 38))

def yfont_pos(pos):
    return (int(base_pos(pos)[0] + 45), int(base_pos(pos)[1] + 28))

def bcounter_pos(pos):
    return (int(base_pos(pos)[0] + 50), int(base_pos(pos)[1] + 18))

def bfont_pos(pos):
    return (int(base_pos(pos)[0] + 45), int(base_pos(pos)[1] + 8))

def star_pos(pos):
    return (int(base_pos(pos)[0]) + 8, int(base_pos(pos)[1] + 58))

def afont_pos(pos):
    return (int(base_pos(pos)[0] + 45), int(base_pos(pos)[1] + 68))

def draw_unit(screen, pos, unit):
    pic = get_image(unit.pic)
    screen.blit(pic, base_pos(pos))
    
    font = pygame.font.SysFont("arial", 18, True, False)

    if unit.acounters:
        pygame.draw.circle(screen, grey, acounter_pos(pos), 10, 0)
        pygame.draw.circle(screen, brown, acounter_pos(pos), 8, 0)
        if unit.acounters != 1:
            label = font.render(str(unit.acounters), 1, black)
            screen.blit(label, afont_pos(pos))
    
    if unit.dcounters:
        pygame.draw.circle(screen, grey, dcounter_pos(pos), 10, 0)
        pygame.draw.circle(screen, lightgrey, dcounter_pos(pos), 8, 0)

        if unit.dcounters > 1:
            label = font.render(str(unit.dcounters), 1, black)
            screen.blit(label, dfont_pos(pos))

        if unit.dcounters < 0:
            label = font.render("x", 1, black)
            screen.blit(label, dfont_pos(pos))       
            
    if unit.xp == 1:
        pic = get_image("./units/star.gif")
        screen.blit(pic, star_pos(pos))
    
    unit.ycounters = 0
    
    if hasattr(unit, "extra_life"):
        unit.ycounters = 1
    
    if unit.ycounters:
        pygame.draw.circle(screen, grey, ycounter_pos(pos), 10, 0)
        pygame.draw.circle(screen, yellow, ycounter_pos(pos), 8, 0)

        if unit.ycounters > 1:
            label = font.render(str(unit.ycounters), 1, black)
            screen.blit(label, yfont_pos(pos))     

    unit.bcounters = 0
    
    if hasattr(unit, "frozen"):
        unit.bcounters = unit.frozen

    if hasattr(unit, "just_bribed"):
        unit.bcounters = 1
  
    if unit.bcounters:
        pygame.draw.circle(screen, grey, bcounter_pos(pos), 10, 0)
        pygame.draw.circle(screen, blue, bcounter_pos(pos), 8, 0)

        if unit.bcounters > 1:
            label = font.render(str(unit.bcounters), 1, black)
            screen.blit(label, bfont_pos(pos))     
           
    if unit.is_crusading or unit.high_morale:
        pic = get_image("./units/flag.gif")
        screen.blit(pic, flag_pos(pos))        
    
    if hasattr(unit, "bribed"):
        pic = get_image("./units/ability.gif")
        screen.blit(pic, symbol_pos(pos))  

def draw_game(screen, p):
    pic = get_image("./units/board.gif")
    screen.blit(pic, (0,0))
 
    for pos in p[0].units:
        draw_unit(screen, pos, p[0].units[pos])

    for pos in p[1].units:
        draw_unit(screen, pos, p[1].units[pos])
        
    pygame.display.update()  

def draw_action(screen, action):
    pygame.draw.circle(screen, black, center_pos(action.startpos), 10)
    pygame.draw.line(screen, black, center_pos(action.startpos), center_pos(action.endpos), 5)
    
    if action.is_attack:

        pygame.draw.line(screen, black, center_pos(action.endpos), center_pos(action.attackpos), 5)

        if action.move_with_attack:
            pic = get_image("./units/moveattack.gif")
        else:
            pic = get_image("./units/attack.gif")

        screen.blit(pic, symbol_pos(action.attackpos))

    elif action.is_ability:

        pygame.draw.line(screen, black, center_pos(action.endpos), center_pos(action.attackpos), 5)

        pic = get_image("./units/ability.gif")

        screen.blit(pic, symbol_pos(action.attackpos))      

    else:
            pic = get_image("./units/move.gif")

            screen.blit(pic, symbol_pos(action.endpos))
    
    pygame.display.update()

def run_game():
    pygame.init()

    screen = pygame.display.set_mode(board_size)
    clock = pygame.time.Clock()
    
    p = setup.get_startunits()

    p[0].ai = ai_module.AI(player1_ai, p[0])
    p[1].ai = ai_module.AI(player2_ai, p[1])

    mover.initialize_turn([p[0], p[1]])
    mover.initialize_turn([p[1], p[0]])
    draw_game(screen, p)
   
    turn1 = True

    while True:
        time_passed = clock.tick(50)
        
        for event in pygame.event.get():

            if event.type == KEYDOWN:        

                if event.key == K_SPACE:
                    
                    print p[0].color
                    
                    mover.initialize_turn(p)

                    draw_game(screen, p)
                    
                    if turn1:
                        p[0].actions = 1
                        turn1 = False
                    
                    while p[0].actions > 0:
                        
                        p[0].extra_action = False
                        action = p[0].ai.select_action(p, False)
                        
                        if action:
                            draw_action(screen, action)
                            pygame.time.delay(pause_for_animation)

                            mover.do_first_action(action, p)
                            
                            if hasattr(p[0], "won"):
                                game_end(screen, p[0])                              
                            
                            p[0].ai.add_counters(p)

                            draw_game(screen, p)
                            
                            p[0].extra_action = True
                            extra_action = p[0].ai.select_extra_action(p, False)

                            if extra_action:
                                draw_action(screen, extra_action)
                                pygame.time.delay(pause_for_animation)
    
                                mover.do_extra_action(extra_action, p)
                                if hasattr(p[0], "won"):
                                    game_end(screen, p[0])
                                    
                                p[0].ai.add_counters(p)
    
                                draw_game(screen, p)         
                              
                        else:
                            p[0].actions -= 1
                                     
                    p = [p[1], p[0]]
                    print

                elif command_q_down(event.key):
                    exit_game();

            if event.type == QUIT:
                exit_game()
    
        pygame.display.flip()

def command_q_down(key):
    return key == K_q and (pygame.key.get_mods() & KMOD_LMETA or pygame.key.get_mods() & KMOD_RMETA)

def exit_game():
    sys.exit()

def game_end(screen, player):
    font = pygame.font.SysFont("monospace", 55, bold = True)
    label = font.render(player.color + "\nWins", 1, black)
    screen.blit(label, (40, 400))
    pygame.display.update()
    pygame.time.delay(40000)
    exit_game()

run_game()
