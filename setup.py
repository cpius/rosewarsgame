# Sample Python/Pygame Programs
# Simpson College Computer Science
# http://programarcadegames.com/
# http://simpson.edu/computer-science/

from __future__ import division
from numpy import random as rnd
import itertools as it
   

class Unit:
    def __init__(self, name, col, row, color):
        self.name = name
        self.pic = "./units/" + name + color + ".jpg"
        self.row = row
        self.col = col
        self.color = color
        self.acounter = 0
        self.dcounter = 0
        
    def __repr__(self):
        return self.name + ", " + self.color + "\n"
      

def get_backline(color):

    if color == "green":
        return 8
    else:
        return 1

def get_frontline(color):

    if color == "green":
        return 5
    else:
        return 4


def test_coloumn_blocks(units, color):

    backline = get_backline(color)
    
    colcos = [0 for i in range(6)]
    for unit in units:
        colcos[unit.col] += 1
        if unit.name == "pikeman" and unit.row != backline:
            if unit.col > 1:
                colcos[unit.col -1] += 1
            if unit.col < 5:
                colcos[unit.col +1] += 1
    
    return not any(co < 2 for co in colcos[1:])


def test_backlineco(units, color):
    
    backline = get_backline(color)
    
    return sum(1 for unit in units if unit.row == backline) < 2
   
    
def test_samekind(units, unit_names):
    
    names = [unit.name for unit in units]
    
    return not any(names.count(name) > 3 for name in set(names))
    

def test_onepikeman(units):
    
    return any(unit.name == "pikeman" for unit in units)
        

def test_pikemanline(units):
    
    colcos = [0 for i in range(6)]
    for unit in units:
        if unit.name == "pikeman":
            colcos[unit.col] += 1
    
    return not any(co > 1 for co in colcos[1:])


def test_frontline(units, color, nonfrontunit_names):

    frontline = get_frontline(color)
    
    return not any((unit.row == frontline and unit.name in nonfrontunit_names) for unit in units)


def test_backline(units, color, nonbackunit_names):

    frontline = get_backline(color)
    
    return not any((unit.row == frontline and unit.name in nonbackunit_names) for unit in units)


def get_startunits():
    
    unit_names = ["archer", "ballista", "catapult", "lightcavalry", "heavycavalry", "pikeman"]
    specialunit_names = ["berserker", "cannon", "chariot", "crusader", "diplomat", "flagbearer", "lancer", "longswordsman", "royalguard", "saboteur", "samurai", "scout", "viking", "warelephant", "weaponsmith"]  
    nonfrontunit_names = ["lightcavalry", "ballista", "catapult", "archer", "scout", "saboteur", "diplomat", "berserker", "cannon", "weaponsmith", "royalguard"]
    nonbackunit_names = ["Pikeman", "Berserker", "longswordsman", "royalguard", "samurai", "viking", "warelephant"]
    
    def get_units(color):
        
        counter = it.count(1)
        for co in counter:

            units = [] 
            unit_bag = [name for name in unit_names for i in range(4)]
            specialunit_bag = [name for name in specialunit_names]
            occupied = [[False for i in range(9)] for j in range(6)]
            
            while len(units) <= 6: 
                name = unit_bag[rnd.randint(len(unit_bag))]
                col = rnd.randint(1,6)
                if color == "green":
                    row = rnd.randint(5,9)
                else:
                    row = rnd.randint(1,5)
                
                if not occupied[col][row]:
                    unit = Unit(name, col, row, color)
                    if len(units) == 0:
                        unit.acounter = 1
                    if len(units) == 1:
                        unit.dcounter = 1
                    units.append(unit)
                    occupied[col][row] = True
                    unit_bag.remove(name)
    
            while len(units) <= 9:   
                name = specialunit_bag[rnd.randint(len(specialunit_bag))]      
                col = rnd.randint(1,6)
                if color == "green":
                    row = rnd.randint(5,9)
                else:
                    row = rnd.randint(1,5)
                
                if not occupied[col][row]:
                    unit = Unit(name, col, row, color)
                    units.append(unit)
                    occupied[col][row] = True
                    specialunit_bag.remove(name)
    
            
            if not test_coloumn_blocks(units, color):
                continue
            
            if not test_samekind(units, unit_names):
                continue
            
            if not test_onepikeman(units):
                continue
            
            if not test_pikemanline(units):
                continue
    
            if not test_frontline(units, color, nonfrontunit_names):
                continue

            if not test_backlineco(units, color):
                continue

            if not test_backline(units, color, nonbackunit_names):
                continue         
            
            print color, co
            
            return units


    green_units = get_units("green")
    red_units = get_units("red")
                


    return green_units, red_units

















        
def getpos(col, row):
    
    if row < 5:
        return (22 + (unit.col -1) * width,  22 + (unit.row -1) * height)
    else:
        return (22 + (unit.col -1) * width, 39 + (unit.row -1) * height)

def draw_unit(unit):
    pic = pygame.image.load(unit.pic)
    pic = pygame.transform.smoothscale(pic, (65, 100))
    pos = getpos(unit.col, unit.row)
    
    screen.blit(pic, pos)

    cpos = (int(pos[0]) + 45, int(pos[1]) + 58)

    if unit.acounter:
        pygame.draw.circle(screen, grey, cpos, 10, 0)
        pygame.draw.circle(screen, brown, cpos, 8, 0)
    if unit.dcounter:
        pygame.draw.circle(screen, grey, cpos, 10, 0)
        pygame.draw.circle(screen, lightgrey, cpos, 8, 0)




green_units, red_units = get_startunits()


import pygame
 
# Define some colors
black    = (   0,   0,   0)
white    = ( 255, 255, 255)
green    = (   0, 255,   0)
red      = ( 255,   0,   0)
brown = (128, 64, 0)
grey = ( 48,48,48)
lightgrey = (223,223, 223)
 
# This sets the width and height of each grid location
width=70
height=106.5

#set the dimensions
rowco = 8
colco = 5

 # Initialize pygame
pygame.init()
  
# Set the height and width of the screen
size=[391, 908]
screen=pygame.display.set_mode(size)

# Set title of screen
pygame.display.set_caption("War of the Roses")
 
#Loop until the user clicks the close button.
done=False
 
# Used to manage how fast the screen updates
clock=pygame.time.Clock()
 
# -------- Main Program Loop -----------
while done==False:
    for event in pygame.event.get(): # User did something
        if event.type == pygame.QUIT: # If user clicked close
            done=True # Flag that we are done so we exit this loop
        if event.type == pygame.MOUSEBUTTONDOWN:
            # User clicks the mouse. Get the position
            pos = pygame.mouse.get_pos()
        
    # Limit to 20 frames per second
    clock.tick(40)
 
    # Draw board
    pic = pygame.image.load("./units/board.jpg")
    pic = pygame.transform.smoothscale(pic, size)
    screen.blit(pic, (0,0))
 
    #Draw the units

    for unit in green_units:
        draw_unit(unit)
    
    for unit in red_units:
        draw_unit(unit)

    # Go ahead and update the screen with what we've drawn.
    pygame.display.flip()

    
# Be IDLE friendly. If you forget this line, the program will 'hang'
# on exit.
pygame.quit ()
