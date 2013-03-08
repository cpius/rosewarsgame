from __future__ import division
import settings
import random as rnd
import battle
from action import Action


class Direction:
    """ An object direction is one move up, down, left or right.
    The class contains methods for returning the tile going one step in the direction will lead you to,
    and for returning the tiles you should check for zone of control.
    """
    def __init__(self, x, y):
        self.x = x
        self.y = y
        
    def move(self, pos):
        return pos[0] + self. x, pos[1] + self.y
    
    def perpendicular(self, pos):
        return (pos[0] + self.y, pos[1] + self.x), (pos[0] - self.y, pos[1] - self.x)

    def __repr__(self):

        if self.x == -1:
            return "Left"
    
        if self.x == 1:
            return "Right"
        
        if self.y == -1:
            return "Down"
        
        if self.y == 1:
            return "Up"


#global variables
_action = 0
board = set((i, j) for i in range(1, 6) for j in range(1, 9))
directions = [Direction(0, -1), Direction(0, +1), Direction(-1, 0), Direction(1, 0)]
eight_directions = [Direction(i, j) for i in[-1, 0, 1] for j in [-1, 0, 1] if not i == j == 0]

#####################
#####################
###Helper methods####
#####################
#####################


def any(iterable):  # For compatibility with older python versions.
    for element in iterable:
        if element:
            return True
    return False


def zoc(unit, pos, enemy_units):
    """ Returns whether an enemy unit can exert ZOC on a friendly unit """
    return pos in enemy_units and unit.type in enemy_units[pos].zoc


def surrounding_tiles(pos):
    """ Returns the 8 surrounding tiles"""
    return set(direction.move(pos) for direction in eight_directions)


def four_forward_tiles(pos, forward_pos):
    """ Returns the 4 other nearby tiles in the direction towards forward_pos. """
    return surrounding_tiles(pos) & surrounding_tiles(forward_pos)


def two_forward_tiles(pos, forward_pos):
    """ Returns the 2 other nearby tiles in the direction towards forward_pos. """
    return set(direction.move(pos) for direction in eight_directions) & \
        set(direction.move(forward_pos) for direction in directions)


def get_direction(pos, forward_pos):
    """ Returns the direction would take you from pos to forward_pos. """
    return Direction(-pos[0] + forward_pos[0], -pos[1] + forward_pos[1])


def distance(p1, p2):
    return abs(p1[0] - p2[0]) + abs(p1[1] - p2[1])


def find_all_friendly_units_except_current(current_unit_position, p):
    return dict((pos, p[0].units[pos]) for pos in p[0].units if pos != current_unit_position)


def out_of_board_vertical(pos):
    return pos[1] < 1 or pos[1] > 8


def out_of_board_horizontal(pos):
    return pos[0] < 1 or pos[0] > 5
    
    
def gain_xp(unit):
    if not unit.xp_gained_this_round:
        unit.xp += 1
        unit.xp_gained_this_round = True
    

def update_finalpos(action):
    if action.move_with_attack:
        action.finalpos = action.attackpos


###################
###################
###Do action##########
###################
###################


def do_action(action, p, unit=None):

    def player_has_won(action, unit, p):
        return (action.finalpos[1] == p[1].backline and not hasattr(unit, "bribed")) or \
               (not p[1].units and not action.ability == "bribe")

    def prepare_extra_actions(action, unit):
        
        def charioting():
            if not hasattr(unit, "extra_action"):
                unit.movement_remaining = unit.movement - distance(action.startpos, action.endpos)
                if action.is_attack and not (action.move_with_attack and action.outcome == "Success"):
                    unit.movement_remaining -= 1
                unit.extra_action = True
            else:
                del unit.extra_action
    
        def samuraiing():
            if not hasattr(unit, "extra_action"):
                unit.movement_remaining = unit.movement - distance(action.startpos, action.endpos)
                unit.extra_action = True
            else:
                del unit.extra_action
           
        for attribute in ["charioting", "samuraiing"]:
            if hasattr(unit, attribute):
                locals()[attribute]() 
   
    def update_player_actions_remaining(action, p):   

        if not hasattr(p[0], "extra_action") and not hasattr(p[0], "sub_action"):
            p[0].actions_remaining -= 1
            if hasattr(action, "double_cost"):
                p[0].actions_remaining -= 1

    def secondary_action_effects(action, unit):
        if hasattr(unit, "attack_cooldown") and action.is_attack:
            unit.attack_frozen = unit.attack_cooldown

    if not unit:
        unit = p[0].units[action.startpos]
  
    update_player_actions_remaining(action, p)

    unit.used = True

    secondary_action_effects(action, unit)

    if action.is_attack:
        if hasattr(action, "push"):
            settle_attack_push(action, p)
        else:    
            settle_attack(action, p)

    if action.is_ability:     
        settle_ability(action, p)
    
    prepare_extra_actions(action, unit)

    for sub_action in action.sub_actions:
        p[0].sub_action = True
        do_action(sub_action, p, unit)
        del p[0].sub_action

    if action.startpos in p[0].units:
        p[0].units[action.finalpos] = p[0].units.pop(action.startpos)

    if player_has_won(action, unit, p):
        p[0].won = True

    if hasattr(p[0], "extra_action"):
        del p[0].extra_action
    else:
        all_extra_actions = get_extra_actions(p)
        if len(all_extra_actions) > 1:
            p[0].extra_action = True


def initialize_action(p):

    def initialize_crusader():
        for pos, unit in p[0].units.items():
            if any(surrounding_pos in p[0].units and hasattr(p[0].units[surrounding_pos], "crusading") and
                    unit.range == 1 for surrounding_pos in surrounding_tiles(pos)):
                unit.is_crusading = True
            else:
                if hasattr(unit, "is_crusading"):
                    del unit.is_crusading

    initialize_crusader()
        

def initialize_turn(p):
    
    def initialize_abilities(unit, pos, p):
        
        def frozen():
            if unit.frozen == 1:
                del unit.frozen
            else:
                unit.frozen -= 1

        def attack_frozen():
            if unit.attack_frozen == 1:
                del unit.attack_frozen
            else:
                unit.attack_frozen -= 1

        def sabotaged():
            del unit.sabotaged
    
        def improved_weapons():
            del unit.improved_weapons
    
        def just_bribed():
            del unit.just_bribed
        
        for attribute in ["frozen", "attack_frozen", "sabotaged", "improved_weapons", "just_bribed"]:
            if hasattr(unit, attribute):
                locals()[attribute]() 

    def initialize_abilities_opponent(unit, p):
        if hasattr(unit, "bribed"):
            p[0].units[pos] = p[1].units.pop(pos)
            unit.just_bribed = True
            del p[0].units[pos].bribed   

    p[0].actions_remaining = 2
    
    for pos, unit in p[0].units.items():
        unit.used = False
        unit.xp_gained_this_round = False
        initialize_abilities(unit, pos, p)

    for pos, unit in p[1].units.items():
        unit.used = False
        initialize_abilities_opponent(unit, p)
        
    
def settle_attack_push(action, p):
    
    if not action.rolls:
        rolls = [rnd.randint(1, 6), rnd.randint(1, 6)]
        action.rolls = rolls

    if battle.attack_successful(action):

        pushpos = action.push_direction.move(action.attackpos)

        if not battle.defence_successful(action):
            action.outcome = "Success"

            gain_xp(action.unit)
            
            if hasattr(action.target_unit, "extra_life"):
                del p[1].units[action.attackpos].extra_life
                
                if not out_of_board_vertical(pushpos):
                    update_finalpos(action)
                    if pushpos in p[0].units or pushpos in p[1].units or out_of_board_horizontal(pushpos):
                        del p[1].units[action.attackpos]
                    else:       
                        p[1].units[pushpos] = p[1].units.pop(action.attackpos)
                
            else:
                update_finalpos(action)
                del p[1].units[action.attackpos]
           
        else:
            if not out_of_board_vertical(pushpos):
                action.outcome = "Push"
                update_finalpos(action)
                if pushpos in p[0].units or pushpos in p[1].units or out_of_board_horizontal(pushpos):
                    gain_xp(action.unit)
                    del p[1].units[action.attackpos]
     
                else:
                    p[1].units[pushpos] = p[1].units.pop(action.attackpos)
            
            else:
                action.outcome = "Failure"
    else:
        action.outcome = "Failure"


def settle_attack(action, p):
    
    if not action.rolls:
        rolls = [rnd.randint(1, 6), rnd.randint(1, 6)]
        action.rolls = rolls

    if battle.attack_successful(action) and not battle.defence_successful(action):

        action.outcome = "Success"

        gain_xp(action.unit)
        
        if hasattr(action.target_unit, "extra_life"):
            del p[1].units[action.attackpos].extra_life
        else:
            del p[1].units[action.attackpos]
            update_finalpos(action)
            
    else:
        action.outcome = "Failure"


def settle_ability(action, p):

    def sabotage(action, p):
        action.target_unit.sabotaged = True
    
    def poison(action, p):
        if not hasattr(action.target_unit, "frozen"):
            p[1].units[action.attackpos].frozen = 2
        else:
            p[1].units[action.attackpos].frozen = max(action.target_unit.frozen, 2)
    
    def improve_weapons(action, p):
        p[0].units[action.attackpos].improved_weapons = True
    
    def bribe(action, p):
        pos = action.attackpos
        p[0].units[pos] = p[1].units.pop(pos)
        p[0].units[pos].bribed = True

    locals()[action.ability](action, p)


###################
###################
###Get actions#####
###################
###################


def add_targets(actions, p):
    """ Adds an attribute target_unit to the actions, holding the target of the action"""
    for action in actions:
        if action.is_attack:
            action.target_unit = p[1].units[action.attackpos]
        elif action.is_ability:
            if action.attackpos in p[1].units:
                action.target_unit = p[1].units[action.attackpos]
            elif action.attackpos in p[0].units:
                action.target_unit = p[0].units[action.attackpos]
        
        add_targets(action.sub_actions, p)

        if hasattr(action.unit, "double_attack_cost") and action.is_attack:
            action.double_cost = True


def add_modifiers(moves, attacks, abilities, p):    
    def flag_bearing_bonus():
        for attack in attacks:
            if attack.unit.range == 1:
                friendly_units = find_all_friendly_units_except_current(attack.startpos, p)
                for direction in directions:
                    adjacent_pos = direction.move(attack.endpos)
                    if adjacent_pos in friendly_units and hasattr(friendly_units[adjacent_pos], "flag_bearing"):
                        attack.high_morale = True

    for modifier in [flag_bearing_bonus]:
        modifier()
            

def get_actions(p):

    def can_use_unit(unit):
        return not (unit.used or hasattr(unit, "frozen") or hasattr(unit, "just_bribed"))
    
    if hasattr(p[0], "extra_action"):
        return get_extra_actions(p)

    actions = []

    for pos, unit in p[0].units.items():
        if can_use_unit(unit):

            friendly_units = find_all_friendly_units_except_current(pos, p)
            units = dict(friendly_units.items() + p[1].units.items())
            
            moves, attacks, abilities = get_unit_actions(unit, pos, units, p)
            
            add_modifiers(moves, attacks, abilities, p)

            if p[0].actions_remaining == 1 and hasattr(unit, "double_attack_cost"):
                actions += moves + abilities
            else:
                actions += moves + attacks + abilities
           
            add_targets(actions, p)

    return actions
                

def get_unit_actions(unit, pos, units, p):
    
    if unit.name not in settings.special_units:
        if unit.range == 1:
            moves, attacks = melee_actions(unit, pos, units, p)
            return moves, attacks, []
        else:
            moves, attacks = ranged_actions(unit, pos, units, p)
            return moves, attacks, []
    
    else:
        return get_special_unit_actions(unit, pos, units, p)


def get_extra_actions(p):
    
    def charioting():
        moveset = moves_set(unit, pos, units, p[1].units, unit.movement_remaining)
        moves = move_actions(unit, pos, moveset | {pos})
        
        return moves, [], []
    
    def samuraiing():
        def melee_attacks_list_samurai_second(unit, startpos, moveset, enemy_units, movement_remaining):
            attacks = []
            for pos, newpos, move_with_attack in attack_generator(unit, moveset | {startpos}, enemy_units):
                if not move_with_attack:
                    attacks.append(Action(unit, startpos, pos, newpos, True, False))
                else:
                    if movement_remaining > 0:
                        attacks.append(Action(unit, startpos, pos, newpos, True, True))
            return attacks
        
        attacks = melee_attacks_list_samurai_second(unit, pos, {pos}, p[1].units, unit.movement_remaining)
        moves = move_actions(unit, pos, {pos})
        
        return moves, attacks, []
     
    extra_actions = []
    
    for pos, unit in p[0].units.items():
        if hasattr(unit, "extra_action"):
            friendly_units, enemy_units = find_all_friendly_units_except_current(pos, p), p[1].units
            units = dict(friendly_units.items() + enemy_units.items())

            moveset = moves_set(unit, pos, units, enemy_units, unit.movement_remaining)
        
            for attribute in ["charioting", "samuraiing"]:
                if hasattr(unit, attribute):
                    moves, attacks, abilities = locals()[attribute]()
            
            add_modifiers(moves, attacks, abilities, p)
            extra_actions = moves + attacks + abilities
            add_targets(extra_actions, p)

    return extra_actions  


############################
############################
###Basic actions methods####
############################
############################


def zoc_block(unit, pos, direction, enemy_units):
    """ Returns whether an enemy unit exerting ZOC prevents you from going in 'direction' from 'pos'. """
    return any(zoc(unit, perpendicular_pos, enemy_units) for perpendicular_pos in direction.perpendicular(pos))


def adjacent_tiles_the_unit_can_move_to(unit, pos, enemy_units, units):
    for direction in directions:
        newpos = direction.move(pos)
        if newpos in board and newpos not in units:
            if not zoc_block(unit, pos, direction, enemy_units):
                yield newpos


def adjacent_unoccupied_tiles(pos, units):
    for direction in directions:
        newpos = direction.move(pos)
        if newpos in board and newpos not in units:
            yield newpos


def adjacent_tiles(pos):
    for direction in directions:
        newpos = direction.move(pos)
        if newpos in board:
            yield newpos


def moves_sets(unit, pos, units, enemy_units, movement_remaining):
    """
    Returns all the tiles a unit can move to, in two sets.
    
    moveset_with_leftover: The tiles it can move to, and still have leftover movement to make an attack.
    moveset_no_leftover: The tiles it can move to, with no leftover movement to make an attack.
    """
    if movement_remaining > 0:
        if movement_remaining != unit.movement: moveset_with_leftover = {pos}
        else: moveset_with_leftover = set()
        moveset_no_leftover = set()
        
        for newpos in adjacent_tiles_the_unit_can_move_to(unit, pos, enemy_units, units):
            movesets = moves_sets(unit, newpos, units, enemy_units, movement_remaining - 1)
            moveset_with_leftover |= movesets[0]
            moveset_no_leftover |= movesets[1]

        return moveset_with_leftover, moveset_no_leftover
    
    else:
        return set(), {pos}


def moves_set(unit, pos, units, enemy_units, movement_remaining):
    """Returns all the tiles a unit can move to, in one set. """
                  
    if movement_remaining > 0:
        if movement_remaining != unit.movement: moveset = {pos}
        else: moveset = set()
        
        for newpos in adjacent_tiles_the_unit_can_move_to(unit, pos, enemy_units, units):
            moveset |= moves_set(unit, newpos, units, enemy_units, movement_remaining - 1)

        return moveset
    
    else:
        return {pos}


def ranged_attacks_set(unit, pos, units, enemy_units, range_remaining):
    """ Returns all the tiles a ranged unit can attack, in a set."""
    
    attackset = set()

    if pos in enemy_units:
        attackset.add(pos)

    if range_remaining > 0:
        for newpos in adjacent_tiles(pos):
            attackset |= ranged_attacks_set(unit, newpos, units, enemy_units, range_remaining - 1)

    return attackset


def abilities_set(unit, pos, units, target_units, range_remaining):
    """ Returns all the tiles an ability unit can target, in a set."""

    abilityset = set()

    if pos in target_units:
        abilityset.add(pos)

    if range_remaining > 0:
        for newpos in adjacent_tiles(pos):
            abilityset |= abilities_set(unit, newpos, units, target_units, range_remaining - 1)

    return abilityset


def move_actions(unit, startpos, moveset):
    return [Action(unit, startpos, pos, None, False, False) for pos in moveset]


def ranged_attack_actions(unit, startpos, attackset):
    return [Action(unit, startpos, startpos, pos, True, False) for pos in attackset]
  

def attack_generator(unit, moveset, enemy_units):
    """ Generates all the tiles a unit can attack based on the places it can move to. """
    for pos in moveset:
        for direction in directions:
            newpos = direction.move(pos)
            if newpos in enemy_units:
                if not zoc_block(unit, pos, direction, enemy_units):
                    yield pos, newpos, True 
                yield pos, newpos, False
                

def attack_generator_no_zoc_check(moveset, enemy_units):
    """ Generates all the tiles a unit can attack based on the places it can move to, with no accounting for ZOC """
    for pos in moveset:
        for direction in directions:
            newpos = direction.move(pos)
            if newpos in enemy_units:
                yield pos, newpos
                

def melee_attack_actions(unit, startpos, moveset, enemy_units):
    return [Action(unit, startpos, endpos, attackpos, True, move_with_attack) for endpos, attackpos,
            move_with_attack in attack_generator(unit, moveset, enemy_units)]


def melee_actions(unit, pos, units, p):
    moveset_with_leftover, moveset_no_leftover = moves_sets(unit, pos, units, p[1].units, unit.movement)
    attacks = melee_attack_actions(unit, pos, moveset_with_leftover | {pos}, p[1].units)
    moves = move_actions(unit, pos, moveset_with_leftover | moveset_no_leftover)
    
    return moves, attacks


def ranged_actions(unit, pos, units, p):
    attackset = ranged_attacks_set(unit, pos, units, p[1].units, unit.range)
    moveset = moves_set(unit, pos, units, p[1].units, unit.movement)
    attacks = ranged_attack_actions(unit, pos, attackset)
    moves = move_actions(unit, pos, moveset)
    
    return moves, attacks


def ability_actions(unit, startpos, abilityset, ability):
    return [Action(unit, startpos, startpos, pos, False, False, True, ability) for pos in abilityset]


##########################
##########################
###Special unit methods###
##########################
#########################


def get_special_unit_actions(unit, pos, units, p):  
    
    def melee_units(unit, pos, units, p):
        
        def rage(unit, pos, moveset_with_leftover, moveset_no_leftover, enemy_units):
            
            attacks = []
            for endpos, attackpos, move_with_attack in attack_generator(unit, moveset_with_leftover | set([pos]),
                                                                        enemy_units):
                attacks.append(Action(unit, pos, endpos, attackpos, True, move_with_attack))
            for endpos, attackpos in attack_generator_no_zoc_check(moveset_no_leftover, enemy_units):
                attacks.append(Action(unit, pos, endpos, attackpos, True, False))
        
            moves = move_actions(unit, pos, moveset_with_leftover | moveset_no_leftover)
            
            return moves, attacks

        def berserking(unit, pos, moveset_with_leftover, moveset_no_leftover, enemy_units):
            
            moveset_with_leftover_berserk, moveset_no_leftover_berserk = moves_sets(unit, pos, units, enemy_units, 5)
            # Det burde vaere 4, men virker med 5. :S

            attacks = melee_attack_actions(unit, pos, moveset_with_leftover_berserk | set([pos]), enemy_units)
        
            moves = move_actions(unit, pos, moveset_with_leftover | moveset_no_leftover)
            
            return moves, attacks

        def longsword(unit, pos, moveset_with_leftover, moveset_no_leftover, enemy_units):
            
            def get_attack(unit, pos, endpos, attackpos, move_with_attack):
                attack = Action(unit, pos, endpos, attackpos, True, move_with_attack)
                for fpos in four_forward_tiles(endpos, attackpos):
                    if fpos in enemy_units:
                        attack.sub_actions.append(Action(unit, pos, endpos, fpos, True, False))
                return attack
           
            attacks = [get_attack(unit, pos, endpos, attackpos, move_with_attack) for endpos, attackpos,
                       move_with_attack in attack_generator(unit, moveset_with_leftover | set([pos]), enemy_units)]

            moves = move_actions(unit, pos, moveset_with_leftover | moveset_no_leftover)
            
            return moves, attacks

        def triple_attack(unit, pos, moveset_with_leftover, moveset_no_leftover, enemy_units):
            
            def get_attack(unit, startpos, endpos, attackpos, move_with_attack):
                attack = Action(unit, startpos, endpos, attackpos, True, move_with_attack)
                for fpos in two_forward_tiles(endpos, attackpos):
                    if fpos in enemy_units:
                        attack.sub_actions.append(Action(unit, startpos, endpos, fpos, True, False))
                return attack
        
            attacks = [get_attack(unit, startpos, endpos, attackpos, move_with_attack) for endpos, attackpos,
                       move_with_attack in attack_generator(unit, moveset_with_leftover | {pos}, enemy_units)]

            moves = move_actions(unit, startpos, moveset_with_leftover | moveset_no_leftover)
            
            return moves, attacks

        def lancing(unit, pos, moveset_with_leftover, moveset_no_leftover, enemy_units):
            
            attacks = melee_attack_actions(unit, startpos, moveset_with_leftover | {startpos}, enemy_units)
            moves = move_actions(unit, startpos, moveset_with_leftover | moveset_no_leftover)

            for attack in attacks:
                if distance(attack.startpos, attack.attackpos) >= 3:
                    attack.lancing = True
            
            return moves, attacks

        def defence_maneuverability(unit, pos, moveset_with_leftover, moveset_no_leftover, enemy_units):
            extended_moveset_no_leftover = set()
            for pos in moveset_no_leftover:
                extended_moveset_no_leftover.add(pos)
                for direction in directions[2:]:
                    newpos = direction.move(pos)
                    if newpos in board and newpos not in units:
                        extended_moveset_no_leftover.add(newpos)
            
            attacks = melee_attack_actions(unit, startpos, moveset_with_leftover | {startpos}, enemy_units)
            moves = move_actions(unit, startpos, moveset_with_leftover | extended_moveset_no_leftover)
            
            return moves, attacks

        def get_attacks_push(attacks):
            for attack in attacks:
                push_direction = get_direction(attack.endpos, attack.attackpos)
                for sub_attack in attack.sub_actions:
                    sub_attack.push = True
                    sub_attack.push_direction = push_direction
                attack.push = True
                attack.push_direction = push_direction
            
            return attacks
        
        enemy_units = p[1].units
     
        moveset_with_leftover, moveset_no_leftover = moves_sets(unit, pos, units, enemy_units, unit.movement)
        attacks = melee_attack_actions(unit, pos, moveset_with_leftover | {pos}, enemy_units)
        moves = move_actions(unit, pos, moveset_with_leftover | moveset_no_leftover)
        
        for attribute in ["rage", "berserking", "longsword", "triple_attack", "defence_maneuverability", "lancing"]:
            if hasattr(unit, attribute):
                moves, attacks = locals()[attribute](unit, pos, moveset_with_leftover, moveset_no_leftover, enemy_units)
        
        if hasattr(unit, "push"):
            attacks = get_attacks_push(attacks)

        return moves, attacks

    def ranged_units(unit, pos, units, p):
        return ranged_actions(unit, pos, units, p)

    def ability_units(unit, pos, units, p):
        
        abilities = []
        
        for ability in unit.abilities:
        
            if ability in ["sabotage", "poison"]:
                target_units = p[1].units

            if ability == "improve_weapons":
                target_units = [tpos for tpos, target_unit in p[0].units.items()
                                if target_unit.attack and target_unit.range == 1]
                
            if ability == "bribe":
                target_units = [tpos for tpos, target_unit in p[1].units.items()
                                if not hasattr(target_unit, "bribed") and not hasattr(target_unit, "just_bribed")]

            abilityset = abilities_set(unit, pos, units, target_units, unit.range)
            abilities += ability_actions(unit, pos, abilityset, ability)

        return abilities

    def no_attack_units(unit, pos, units, p):
        
        def scouting():
            
            def moves_set_scouting(unit, pos, units, enemy_units, movement_remaining):
                
                if movement_remaining > 0:
                    if movement_remaining != unit.movement:
                        moveset = {pos}
                    else:
                        moveset = set()
                    
                    for newpos in adjacent_unoccupied_tiles(pos, units):
                        moveset |= moves_set_scouting(unit, newpos, units, enemy_units, movement_remaining - 1)
            
                    return moveset
                
                else:
                    return {pos}
                    
            moveset = moves_set_scouting(unit, pos, units, p[1].units, unit.movement)
            moves = move_actions(unit, pos, moveset)
            
            return moves

        moveset = moves_set(unit, pos, units, p[1].units, unit.movement)
        moves = move_actions(unit, pos, moveset)

        for attribute in ["scouting"]:
            if hasattr(unit, attribute):
                moves = locals()[attribute]()

        return moves

    if unit.abilities:
        abilities = ability_units(unit, pos, units, p)
    else:
        abilities = []
        
    if unit.attack:
        if unit.range == 1:
            moves, attacks = melee_units(unit, pos, units, p)
        else:
            moves, attacks = ranged_units(unit, pos, units, p)
    
    else: 
        moves = no_attack_units(unit, pos, units, p)
        attacks = []
        
    return moves, attacks, abilities