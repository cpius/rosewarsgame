import random as rnd
import mover
import copy
import imp
from time import time
import gamestate


class AI(object):
    """
    Creates an AI of a certain type, which can make the two decisions a player has to make in a game:
    - Make an action
    - Make a second part of an action (with Samurai or Chariot)
    - Put a counter on a unit with two experience points
    
    The locations are transformed so that the player the AI is playing for has backline on row 1.
    """
    
    def __init__(self, type, player):

        ai_type = imp.load_source(type, "ai_" + type.lower() + ".py")
        self.get_action = ai_type.get_action
        self.put_counter = ai_type.put_counter
        self.name = type
            
    
    def select_action(self, p, turn = None):
                 
        p = gamestate.copy_p(p)
                    
        if p[0].backline == 8:
            p = get_transformed_p(p)
            transform_action = get_transformed_action
        else:
            transform_action = get_same_action
        
        actions = mover.get_actions(p)

        if actions:
            action = self.get_action(p, actions)
            return transform_action(action)     
        else:
            return None  

    
    def add_counters(self, p):
        
        for unit in p[0].units.values():
            if unit.xp == 2:
                if unit.defence + unit.dcounters == 4:
                    unit.acounters += 1
                else:
                    self.put_counter(p, unit)
                unit.xp = 0


class Direction:
    """ A object direction is one move up, down, left or right.
    The class contains methods for returning the tile you will go to after the move, and for returning the tiles you should check for zone of control.
    """
    def __init__(self, x, y):
        self.x = x
        self.y = y
        
    def move(self, pos):
        return (pos[0] + self. x, pos[1] + self.y)
    
    def perpendicular(self, pos):
        return ((pos[0] + self.y, pos[1] + self.x), (pos[0] - self.y, pos[1] - self.x))


def t(pos):
    if pos:
        return (pos[0], 9 - pos[1])     
    else:
        return None


def get_transformed_direction(direction):
    
    if direction.y == -1:
        return Direction(0,1)
 
    if direction.y == 1:
        return Direction(0,-1)

    return direction


def get_transformed_action(action):

    action.startpos = t(action.startpos)
    action.endpos = t(action.endpos)
    action.attackpos = t(action.attackpos)
    for sub_action in action.sub_actions:
        sub_action = get_transformed_action(sub_action)
    if hasattr(action, "push"):
        action.push_direction = get_transformed_direction(action.push_direction)
        
    return action


def get_same_action(action):

    return action

 

def get_transformed_p(p):

    newp = []
    
    for player in p:
        pc = copy.copy(player)
        pc.newunits = {}
        for pos, unit in pc.units.items():
            pc.newunits[t(pos)] = unit
        pc.units = pc.newunits
        pc.backline =  9 - player.backline
        newp.append(pc)
        
    return newp

