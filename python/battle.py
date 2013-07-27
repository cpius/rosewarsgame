from outcome import Outcome, SubOutcome
import common


def attack_successful(action, rolls, gamestate):
    
    attack = get_attack_rating(action.unit, action.target_unit, action, gamestate)
    
    return rolls[0] <= attack


def defence_successful(action, rolls, gamestate):

    attack_rating = get_attack_rating(action.unit, action.target_unit, action, gamestate)
    defence_rating = get_defence_rating(action.unit, action.target_unit, attack_rating, gamestate)
    
    return rolls[1] <= defence_rating
    

def get_defence_rating(attacking_unit, defending_unit, attack_rating, gamestate):
    
    defence_rating = defending_unit.defence

    if attacking_unit.type in defending_unit.dbonus:
        defence_rating += defending_unit.dbonus[attacking_unit.type]

    if hasattr(defending_unit, "improved_weapons"):
        defence_rating += 1

    if hasattr(defending_unit, "shield") and attacking_unit.range == 1:
        defence_rating += 1

    if hasattr(attacking_unit, "sharpshooting"):
        defence_rating = 1

    if attacking_unit.range > 1 and hasattr(defending_unit, "tall_shield"):
        defence_rating += 1

    if attacking_unit.range == 1 and hasattr(defending_unit, "melee_expert"):
        defence_rating += 1

    if attack_rating > 6:
        defence_rating = defending_unit.defence - attack_rating + 6
    
    if defending_unit.get_sabotaged_II():
        defence_rating = 0

    if defending_unit.get_sabotaged_II():
        defence_rating = -1

    return defence_rating


def get_attack_rating(attacking_unit, defending_unit, action, gamestate):
    
    attack = attacking_unit.attack

    if action.is_lancing():
        attack += 2

    if action.is_lancing_II():
        attack += 3

    if action.is_crusading(gamestate):
        attack += 1
    
    if attacking_unit.get_bribed():
        attack += 1

    if action.has_high_morale(gamestate):
        attack += 2

    if action.has_high_morale_II_A(gamestate):
        attack += 2

    if action.has_high_morale_II_B(gamestate):
            attack += 3

    if hasattr(attacking_unit, "improved_weapons"):
        attack += 3
 
    if defending_unit.type in attacking_unit.abonus:
        attack += attacking_unit.abonus[defending_unit.type]

    if defending_unit.range == 1 and hasattr(attacking_unit, "melee_expert"):
        attack += 1

    if hasattr(attacking_unit, "far_sighted") and common.distance(action.end_position, action.attack_position) < 4:
        attack -= 1

    return attack


def get_outcome(action, outcome):
    sub_outcome = outcome.for_position(action.attack_position)
    if sub_outcome == SubOutcome.MISS:
        return " Miss"
    elif sub_outcome == SubOutcome.DEFEND:
        return " Defend"
    elif sub_outcome == SubOutcome.WIN:
        return " Win"
