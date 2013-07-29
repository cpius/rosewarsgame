from outcome import Outcome, SubOutcome
from common import *


def attack_successful(action, rolls, gamestate):
    
    attack = get_attack_rating(action.unit, action.target_unit, action, gamestate)
    
    return rolls[0] <= attack


def defence_successful(action, rolls, gamestate):

    attack_rating = get_attack_rating(action.unit, action.target_unit, action, gamestate)
    defence_rating = get_defence_rating(action.unit, action.target_unit, attack_rating, action, gamestate)
    
    return rolls[1] <= defence_rating
    

def get_defence_rating(attacking_unit, defending_unit, attack_rating, action, gamestate):
    
    defence_rating = defending_unit.defence
    enemy_units = gamestate.opponent_units()

    if attacking_unit.type in defending_unit.defence_bonuses:
        defence_rating += defending_unit.defence_bonuses[attacking_unit.type]

    if defending_unit.has("improved_weapons"):
        defence_rating += 1

    if defending_unit.has("improved_weapons_II_A"):
            defence_rating += 1

    if defending_unit.has("improved_weapons_II_B"):
            defence_rating += 2

    if attacking_unit.has("sharpshooting"):
        defence_rating = 1

    if attacking_unit.range > 1 and defending_unit.has("tall_shield"):
        defence_rating += 1

    if attacking_unit.range == 1 and defending_unit.has("melee_expert"):
        defence_rating += 1

    if attack_rating > 6:
        defence_rating = defending_unit.defence - attack_rating + 6
    
    if defending_unit.is_sabotaged_II():
        defence_rating = 0

    if defending_unit.is_sabotaged_II():
        defence_rating = -1

    if attacking_unit.range == 1 and defending_unit.has("big_shield"):
        defence_rating += 2

    if action.is_crusading_II_defence(enemy_units):
        defence_rating += 1

    return defence_rating


def get_attack_rating(attacking_unit, defending_unit, action, gamestate):

    attack = attacking_unit.attack
    action.add_references(gamestate)
    player_units = gamestate.player_units()

    if action.is_lancing():
        attack += 2

    if action.is_lancing_II():
        attack += 3

    if action.is_crusading(player_units):
        attack += 1

    if action.is_crusading_II_attack(player_units):
        attack += 1
    
    if attacking_unit.get_bribed():
        attack += 1

    if action.has_high_morale(player_units):
        attack += 2

    if action.has_high_morale_II_A(player_units):
        attack += 2

    if action.has_high_morale_II_B(player_units):
            attack += 3

    if attacking_unit.has_improved_weapons():
        attack += 3

    if attacking_unit.has_improved_weapons_II_A():
        attack += 2

    if attacking_unit.has_improved_weapons_II_B():
        attack += 3

    if defending_unit.type in attacking_unit.attack_bonuses:
        attack += attacking_unit.attack_bonuses[defending_unit.type]

    if defending_unit.range == 1 and attacking_unit.has("melee_expert"):
        attack += 1

    if attacking_unit.has("far_sighted") and distance(action.end_position, action.attack_position) < 4:
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
