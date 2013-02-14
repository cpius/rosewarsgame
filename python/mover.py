from __future__ import division
import itertools as it
import setup
import copy
import random as rnd
import battle
from time import time


class Action:
    def __init__(self, unit, startpos, endpos, attackpos, is_attack, move_with_attack, is_ability = False, ability = ""):
        self.unit = unit
        self.startpos = startpos
        self.endpos = endpos
        self.attackpos = attackpos
        self.is_attack = is_attack
        self.move_with_attack = move_with_attack
        self.is_ability = is_ability
        self.ability = ability
        self.sub_actions = []
        self.abonus = 0
        self.finalpos = ()
        
    def __repr__(self):
        representation = self.unit.name

        if self.startpos != self.endpos:
            representation += " move from " + coordinates(self.startpos)
            representation += " to " + coordinates(self.endpos)
            if self.is_attack:
                representation += " and"
        else:
            representation += " at " + coordinates(self.startpos)

        if self.is_attack:
            representation += " attack " + coordinates(self.attackpos)

        if self.is_ability:
            representation += " ability " + self.ability + " " + coordinates(self.attackpos)
        
        if hasattr(self, "outcome"):
            representation += ", " + self.outcome
         
        return representation


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



#global variables
_action = 0
board = set((i,j) for i in range(1,6) for j in range(1, 9))
directions = [Direction(0, -1), Direction(0, +1), Direction(-1, 0), Direction(1, 0)]
eight_directions = [Direction(i, j) for i in[-1,0,1] for j in [-1,0,1] if not i == j == 0]





###################
###################
###Helper methods######
###################
###################

def coordinates(position):
    columns = list(" ABCDE")
    return columns[position[0]] + str(position[1])

def any(iterable):
    for element in iterable:
        if element:
            return True
    return False


def zoc(pos, unit, enemy_units):
    return pos in enemy_units and unit.type in enemy_units[pos].zoc


def surrounding_tiles(pos):
    return set(direction.move(pos) for direction in eight_directions)


def four_forward_tiles(pos, fpos):
    """ Returns the 4 other nearby tiles in the direction towards fpos"""
    
    return surrounding_tiles(pos) & surrounding_tiles(fpos) 


def two_forward_tiles(pos, fpos):
    """ Returns the 2 other nearby tiles in the direction towards fpos"""
    
    return set(direction.move(pos) for direction in eight_directions) & set(direction.move(fpos) for direction in directions)

"""
def get_direction(pos, apos):
    for direction in directions:
        if direction.move(pos) == apos:
            return direction
"""
def get_direction(pos, apos):
    return Direction(-pos[0] + apos[0], -pos[1] + apos[1])


def distance(p1, p2):
    return abs(p1[0] - p2[0]) + abs(p1[1] - p2[1])


def find_all_units_except_current(pos, p):
    all_units = dict((upos, p[0].units[upos]) for upos in p[0].units if upos != pos)
    for upos in p[1].units:
        all_units[upos] = p[1].units[upos]
        
    return all_units



def out_of_board_vertical(pos):
    return (pos[1] < 1 or pos[1] > 8)


def out_of_board_horizontal(pos):
    return (pos[0] < 1 or pos[0] > 5)

###################
###################
###Major methods######
###################
###################



def get_all_actions(p):
    """
    Gets all possible actions for the player whose turn it is.
    
    Adds them as attributes to the unit which can do the actions.
    """
    
    for pos, unit in p[0].units.items():
        
        if unit.used or hasattr(unit, "frozen") or hasattr(unit, "just_bribed"):
            unit.actions = []
        
        else:
            all_units = find_all_units_except_current(pos, p)
            
            if unit.name in setup.specialunit_names:
                moves, attacks, abilities = get_special_unit_actions(pos, unit, all_units, p)
            else:
                moves, attacks = get_basic_unit_actions(pos, unit, all_units, p)
                abilities = []
            
            flag_bearing_bonus(attacks, all_units)
      
            if hasattr(unit, "double_attack_cost") and p[0].actions == 1:
                unit.actions = moves
            else:
                unit.actions = moves + attacks + abilities
                

def get_extra_actions(p):
    """
    Gets all possible second actions for the player whose turn it is.
    
    Adds them as attributes to the unit which can do the actions.
    """
    
    for pos, unit in p[0].units.items():
        
        if hasattr(unit, "extra_action"):
      
            all_units = find_all_units_except_current(pos, p)
                
            if hasattr(unit, "charioting"):
                moveset_w_leftover, moveset_wo_leftover = moves_set(all_units, p[1].units, unit, pos, unit.movement_remaining)
                moves = moves_list(unit, pos, moveset_w_leftover | moveset_wo_leftover | set([(pos)]))
                attacks, abilities = [],[]
            
            if hasattr(unit, "samuraiing"):
                attacks = melee_attacks_list_samurai_second(p[1].units, unit, pos, set([(pos)]), unit.movement_remaining)
                moves = moves_list(unit, pos, set([(pos)]))
                abilities = []
            
            flag_bearing_bonus(attacks, all_units)
            
            unit.actions = moves + attacks + abilities
            
        else:
            
            unit.actions = []
            


def settle_attack_push(action, unit, enemy_unit, p, pos):

    rolls = [rnd.randint(1, 6), rnd.randint(1, 6)]

    if battle.attack_successful(unit, enemy_unit, action, rolls):

        pushpos = action.push_direction.move(action.attackpos)

        if not battle.defence_successful(unit, enemy_unit, action, rolls):
            action.outcome = "Success"

            if not unit.xp_gained_this_round:
                unit.xp += 1
                unit.xp_gained_this_round = True
            
            if hasattr(enemy_unit, "extra_life"):
                del enemy_unit.extra_life
                
                if not out_of_board_vertical(pushpos):
                    if action.move_with_attack and not action.finalpos:
                        action.finalpos = pos
                    if pushpos in p[0].units or pushpos in p[1].units or out_of_board_horizontal(pushpos):
                        del p[1].units[pos]
                    else:       
                        p[1].units[pushpos] = p[1].units.pop(action.attackpos)
                
            else:
                if action.move_with_attack and not action.finalpos:
                    action.finalpos = pos
                del p[1].units[pos]
           
        else:
            if not out_of_board_vertical(pushpos):
                action.outcome =  "Push"
                if action.move_with_attack and not action.finalpos:
                    action.finalpos = pos
                if pushpos in p[0].units or pushpos in p[1].units or out_of_board_horizontal(pushpos):
    
                    if not unit.xp_gained_this_round:
                        unit.xp += 1
                        unit.xp_gained_this_round = True
                    del p[1].units[pos]
     
                else:
                    p[1].units[pushpos] = p[1].units.pop(pos)
            
            else:
                action.outcome = "Failure"
    else:
        action.outcome = "Failure"


def settle_attack(action, unit, enemy_unit, p, pos):
    rolls = [rnd.randint(1, 6), rnd.randint(1, 6)]

    if battle.attack_successful(unit, enemy_unit, action, rolls) and not battle.defence_successful(unit, enemy_unit, action, rolls):

        action.outcome = "Success"

        if not unit.xp_gained_this_round:
            unit.xp += 1
            unit.xp_gained_this_round = True
        if hasattr(enemy_unit, "extra_life"):
            del enemy_unit.extra_life
        else:
            del p[1].units[pos]
            
            if action.move_with_attack and not action.finalpos:
                action.finalpos = pos
    else:
        action.outcome = "Failure"


def settle_ability(action, friendly_unit, enemy_unit, pos, p):
    if action.ability == "sabotage":
        enemy_unit.dcounters = -10
        enemy_unit.sabotaged = True

    elif action.ability == "poison":
        if not hasattr(enemy_unit, "frozen"):
            enemy_unit.frozen = 2
        else:
            enemy_unit.frozen = max(enemy_unit.frozen, 2)

    elif action.ability == "improve weapons":
        friendly_unit.acounters += 3
        friendly_unit.dcounters += 1
        friendly_unit.improved_weapons = True

    elif action.ability == "bribe":
        p[0].units[pos] = p[1].units.pop(pos)
        p[0].units[pos].bribed = True


def do_extra_action(action, p):
    
    unit = p[0].units[action.startpos]
    do_action(action, p, unit)
    del unit.extra_action



def do_action(action, p, unit = None):
    """ Carries out an action in the game."""
    
    print action
    
    if not unit:
        unit = p[0].units[action.startpos]
        
    unit.used = True
    
    if not hasattr(unit, "extra_action"):
        p[0].actions -= 1
        if hasattr(unit, "double_attack_cost") and action.is_attack:
            p[0].actions -= 1
    
    pos = action.attackpos
    enemy_unit = p[1].units.get(pos)
    friendly_unit = p[0].units.get(pos)

    if hasattr(unit, "cooldown"):
        unit.frozen = unit.cooldown
        
    if action.is_attack and hasattr(action, "push"):
        settle_attack_push(action, unit, enemy_unit, p, pos)
    
    if action.is_attack and not hasattr(action, "push"):
        settle_attack(action, unit, enemy_unit, p, pos)
    
    if action.is_ability:     
        settle_ability(action, enemy_unit, friendly_unit, pos, p)
    
    if hasattr(unit, "charioting"):
        if not hasattr(unit, "extra_action"):
            unit.movement_remaining = unit.movement - distance(action.startpos, action.endpos)
            if action.is_attack and not action.move_with_attack:
                unit.movement_remaining -= 1
            if action.move_with_attack and action.endpos != action.attackpos:
                unit.movement_remaining -= 1 
            unit.extra_action = True

        
    if hasattr(unit, "samuraiing"):
        if not hasattr(unit, "extra_action"):
            unit.movement_remaining = unit.movement - distance(action.startpos, action.endpos)
            unit.extra_action = True


    if not action.finalpos:
        action.finalpos = action.endpos

    for sub_action in action.sub_actions:
        do_action(sub_action, p, unit)
    
    if action.startpos in p[0].units:
        p[0].units[action.finalpos] = p[0].units.pop(action.startpos)

    if action.finalpos[1] == p[1].backline or not p[1].units:
        p[0].won = True

    print action

def initialize_turn(p):
    
    p[0].actions = 2
    
    for pos, unit in p[0].units.items():
        unit.used = False
        unit.xp_gained_this_round = False
        
        if hasattr(unit, "frozen"):
            if unit.frozen == 1: del unit.frozen
            else: unit.frozen -= 1
        
        if hasattr(unit, "sabotaged"):
            unit.dcounters += 10
            del unit.sabotaged

        if hasattr(unit, "improved_weapons"):
            unit.acounters -= 3
            unit.dcounters -= 1
            del unit.improved_weapons

        if hasattr(unit, "just_bribed"):
            del unit.just_bribed
        
        unit.crusading = (unit.range == 1 and any(spos in p[0].units and hasattr(p[0].units[spos], "crusading") for spos in surrounding_tiles(pos)))


    for pos, unit in p[1].units.items():
   
        if hasattr(unit, "bribed"):
            p[0].units[pos] = p[1].units.pop(pos)
            unit.just_bribed = True
            del p[0].units[pos].bribed
        
    



###################
###################
###Basic unit actions######
###################
###################


def moves_set(units, enemy_units, unit, pos, tiles):
    """
    Returns all the tiles a unit can move to in two sets.
    
    moveset_w_leftover: The tiles it can move to, and still have leftover movement to make an attack.
    moveset_wo_leftover: The tiles it can move to, with no leftover movement to make an attack.
    """
    
    if tiles > 0:
        if tiles != unit.movement:
            moveset_w_leftover = set([(pos)])
        else:
            moveset_w_leftover = set()
        moveset_wo_leftover = set()
    else:
        moveset_w_leftover = set()
        moveset_wo_leftover = set([(pos)])
              
    if tiles > 0:       
        for direction in directions:
            npos = direction.move(pos)
            if npos in board and npos not in units:
                if not any(zoc(ppos, unit, enemy_units) for ppos in direction.perpendicular(pos)):
                    movesets = moves_set(units, enemy_units, unit, npos, tiles -1)
                    moveset_w_leftover |= movesets[0]
                    moveset_wo_leftover |= movesets[1]
     
    return moveset_w_leftover, moveset_wo_leftover


def ranged_attacks_set(units, enemy_units, unit, pos, tiles):
    """ Returns all the tiles a ranged unit can attack in a set."""
    
    attackset = set()

    if pos in enemy_units:
        attackset.add(pos)

    if tiles > 0:
        for direction in directions:
            npos = direction.move(pos)
            if npos in board:
                attackset |= ranged_attacks_set(units, enemy_units, unit, npos, tiles -1)

    return attackset


def moves_list(unit, startpos, moveset):
    """ Generates the actions a unit can do which are moves."""
    
    return [Action(unit, startpos, pos, None, False, False) for pos in moveset]


def ranged_attacks_list(unit, startpos, attackset):
    """Generates the actions a unit can do which are ranged attacks."""
    
    return [Action(unit, startpos, startpos, pos, True, False) for pos in attackset]
  
  
def melee_attacks_list_samurai_second(enemy_units, unit, startpos, moveset, movement_remaining):
    """ Generates actions a unit can do which are melee attacks."""
    
    actions = []
    
    for move in moveset:
        for direction in directions:
            npos = direction.move(move)
            if npos in enemy_units:
                if not any(zoc(ppos, unit, enemy_units) for ppos in direction.perpendicular(move)) and movement_remaining == 1:
                    actions.append(Action(unit, startpos, move, npos, True, True))
                actions.append(Action(unit, startpos, move, npos, True, False))
    
    return actions



def melee_attacks_list(enemy_units, unit, startpos, moveset):
    """ Generates actions a unit can do which are melee attacks."""
    
    actions = []
    
    for move in moveset:
        for direction in directions:
            npos = direction.move(move)
            if npos in enemy_units:
                if not any(zoc(ppos, unit, enemy_units) for ppos in direction.perpendicular(move)):
                    actions.append(Action(unit, startpos, move, npos, True, True))
                actions.append(Action(unit, startpos, move, npos, True, False))
    
    return actions


def melee_actions(pos, unit, all_units, p):
    moveset_w_leftover, moveset_wo_leftover = moves_set(all_units, p[1].units, unit, pos, unit.movement)
    attacks = melee_attacks_list(p[1].units, unit, pos, moveset_w_leftover | set([(pos)]))
    moves = moves_list(unit, pos, moveset_w_leftover | moveset_wo_leftover)
    
    return moves, attacks


def ranged_actions(pos, unit, all_units, p):
    attackset = ranged_attacks_set(all_units, p[1].units, unit, pos, unit.range)
    moveset_w_leftover, moveset_wo_leftover = moves_set(all_units, p[1].units, unit, pos, unit.movement)
    attacks = ranged_attacks_list(unit, pos, attackset)
    moves = moves_list(unit, pos, moveset_w_leftover | moveset_wo_leftover)
    
    return moves, attacks


def get_basic_unit_actions(pos, unit, all_units, p):
    """ Returns all possible actions for a basic units.
    
    Returns two lists, one of all moves and one of all attacks.
    """
    
    if unit.range == 1:
        return melee_actions(pos, unit, all_units, p)
    else:
        return ranged_actions(pos, unit, all_units, p)





###################
###################
###Special unit methods###
###################
###################




def get_special_unit_actions(pos, unit, all_units, p):
    """ Returns all possible actions for a special units.
    
    Returns three lists, one of all moves, one of all attacks, and one of all abilities.
    """
    
    def melee_units():
        
        moveset_w_leftover, moveset_wo_leftover = moves_set(all_units, p[1].units, unit, pos, unit.movement)
        attacks = melee_attacks_list(p[1].units, unit, pos, moveset_w_leftover | set([(pos)]))
        moves = moves_list(unit, pos, moveset_w_leftover | moveset_wo_leftover)
        

        if hasattr(unit, "rage"):
            attacks = melee_attacks_rage(p[1].units, unit, pos, moveset_w_leftover, moveset_wo_leftover)
            

        if hasattr(unit, "berserking"):
            moveset_w_leftover_berserk, moveset_wo_leftover_berserk = moves_set(all_units, p[1].units, unit, pos, 4)
            attacks = melee_attacks_list(p[1].units, unit, pos, moveset_w_leftover_berserk | set([(pos)]))


        if hasattr(unit, "longsword"):
            attacks = melee_attacks_longsword(p[1].units, unit, pos, moveset_w_leftover | set([(pos)]))
    

        if hasattr(unit, "triple_attack"):
            attacks = melee_attacks_triple(p[1].units, unit, pos, moveset_w_leftover | set([(pos)])) 


        if hasattr(unit, "defence_maneuverability"):
            moveset_wo_leftover = extra_moveset_defence_maneuverability(all_units, moveset_wo_leftover)
            moves = moves_list(unit, pos, moveset_w_leftover | moveset_wo_leftover) 


        if hasattr(unit, "lancing"):   
            for attack in attacks:
                if distance(attack.startpos, attack.attackpos) >= 3:
                    attack.abonus = 2 
     
        if hasattr(unit, "push"):
            for attack in attacks:
                push_direction = get_direction(attack.endpos, attack.attackpos)
                for sub_attack in attack.sub_actions:
                    sub_attack.push = True
                    sub_attack.push_direction = push_direction
                attack.push = True
                attack.push_direction = push_direction

        return moves, attacks


    def ranged_units():
        return ranged_actions(pos, unit, all_units, p)
    
    
    def get_abilities(unit, pos):
        
        abilities = []
        
        for ability in unit.abilities:
        
            if ability in ["sabotage", "poison"]:
                target_units = p[1].units


            if ability == "improve weapons":
                target_units = [unit for unit in p[1].units.values() if unit.has_attack]
                
    
            if ability == "bribe":
                target_units = [tpos for tpos, unit in p[1].units.items() if not hasattr(unit, "bribed") and not hasattr(unit, "just_bribed")]


            abilityset = abilities_set(all_units, target_units, unit, pos, unit.range)
            abilities += abilities_list(unit, pos, abilityset, ability)

        return abilities
            
    
    def no_attack_units():
             
        if hasattr(unit, "scouting"):
            moveset_w_leftover, moveset_wo_leftover = moves_set_scouting(all_units, p[1].units, unit, pos, unit.movement)
            moves = moves_list(unit, pos, moveset_w_leftover | moveset_wo_leftover)
            return moves
            
        moveset_w_leftover, moveset_wo_leftover = moves_set(all_units, p[1].units, unit, pos, unit.movement)
        moves = moves_list(unit, pos, moveset_w_leftover | moveset_wo_leftover)
        
        return moves

    if unit.has_ability:
        abilities = get_abilities(unit, pos)
    else:
        abilities = []
        
    if unit.has_attack:
        if unit.range == 1:
            moves, attacks = melee_units()
        else:
            moves, attacks = ranged_units()
    
    else: 
        moves = no_attack_units()
        attacks = []
        
    return moves, attacks, abilities
    

def moves_set_scouting(units, enemy_units, unit, pos, tiles):

    if tiles > 0:
        if tiles != unit.movement:
            moveset_w_leftover = set([(pos)])
        else:
            moveset_w_leftover = set()
        moveset_wo_leftover = set()
    else:
        moveset_w_leftover = set()
        moveset_wo_leftover = set([(pos)])
              
    if tiles > 0:       
        for direction in directions:
            npos = direction.move(pos)
            if npos in board and npos not in units:
                movesets = moves_set_scouting(units, enemy_units, unit, npos, tiles -1)
                moveset_w_leftover |= movesets[0]
                moveset_wo_leftover |= movesets[1]
     
    return moveset_w_leftover, moveset_wo_leftover


def abilities_list(unit, startpos, moveset, ability):
    """ Generates the actions a unit can do which are abilities."""
    
    return [Action(unit, startpos, startpos, pos, False, False, True, ability) for pos in moveset]


def abilities_set(units, target_units, unit, pos, tiles):
    """ Returns all the tiles a ranged unit can attack in a set."""
    
    abilityset = set()

    if pos in target_units:
        abilityset.add(pos)

    if tiles > 0:
        for direction in directions:
            npos = direction.move(pos)
            if npos in board:
                abilityset |= abilities_set(units, target_units, unit, npos, tiles -1)

    return abilityset


def melee_attacks_rage(enemy_units, unit, startpos, moveset_w_leftover, moveset_wo_leftover):
    """ Generates actions a unit can do which are melee attacks."""
    
    actions = []
    
    for move in moveset_w_leftover:
        for direction in directions:
            npos = direction.move(move)
            if npos in enemy_units:
                if not any(zoc(ppos, unit, enemy_units) for ppos in direction.perpendicular(move)):
                    actions.append(Action(unit, startpos, move, npos, True, True))
                actions.append(Action(unit, startpos, move, npos, True, False))

    for move in moveset_wo_leftover:
        for direction in directions:
            npos = direction.move(move)
            if npos in enemy_units:
                actions.append(Action(unit, startpos, move, npos, True, False))

  
    return actions


def melee_attacks_longsword(enemy_units, unit, startpos, moveset):
    
    actions = []
    
    for move in moveset:
        for direction in directions:
            npos = direction.move(move)
            if npos in enemy_units:
                if not any(zoc(ppos, unit, enemy_units) for ppos in direction.perpendicular(move)):
                    actions.append(Action(unit, startpos, move, npos, True, True))
                    for fpos in four_forward_tiles(move, npos):
                        if fpos in enemy_units:
                            actions[-1].sub_actions.append(Action(unit, startpos, move, fpos, True, False))
                actions.append(Action(unit, startpos, move, npos, True, False))
                for fpos in four_forward_tiles(move, npos):
                    if fpos in enemy_units:
                        actions[-1].sub_actions.append(Action(unit, startpos, move, fpos, True, False))          
    
    return actions


def melee_attacks_triple(enemy_units, unit, startpos, moveset):
    """ Generates actions a unit can do which are melee attacks."""
    
    actions = []
    
    for move in moveset:
        for direction in directions:
            npos = direction.move(move)
            if npos in enemy_units:
                if not any(zoc(ppos, unit, enemy_units) for ppos in direction.perpendicular(move)):
                    actions.append(Action(unit, startpos, move, npos, True, True))
                    for fpos in two_forward_tiles(move, npos):
                        if fpos in enemy_units:
                            actions[-1].sub_actions.append(Action(unit, startpos, move, fpos, True, False))
                actions.append(Action(unit, startpos, move, npos, True, False))
                for fpos in two_forward_tiles(move, npos):
                    if fpos in enemy_units:
                        actions[-1].sub_actions.append(Action(unit, startpos, move, fpos, True, False))          
    
    return actions


def extra_moveset_defence_maneuverability(units, moveset_wo_leftover):
    
    new_moveset = copy.copy(moveset_wo_leftover)
    for pos in moveset_wo_leftover:
        new_moveset.add(pos)
        for direction in directions[2:]:
            npos = direction.move(pos)
            if npos in board and npos not in units:
                new_moveset.add(npos)
    
    return new_moveset
        

def flag_bearing_bonus(actions, all_units):
    for attack in actions:
        for direction in directions:
            cpos = direction.move(attack.endpos)
            if cpos in board and cpos in all_units and hasattr(all_units[cpos], "flag_bearing"):
                attack.abonus += 2