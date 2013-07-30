from outcome import SubOutcome
from common import *


def attack_successful(action, rolls, gamestate):
    
    attack = get_attack_rating(action.unit, action.target_unit, action, gamestate)
    
    return rolls[0] <= attack


def defence_successful(action, rolls, gamestate):

    attack_rating = get_attack_rating(action.unit, action.target_unit, action, gamestate)
    defence_rating = get_defence_rating(action.unit, action.target_unit, attack_rating, action, gamestate)
    
    return rolls[1] <= defence_rating
    

def get_defence_rating(attacking_unit, defending_unit, attack_rating, action, gamestate):
    
    defence = defending_unit.defence
    enemy_units = gamestate.opponent_units()

    if attacking_unit.type in defending_unit.defence_bonuses:
        defence += defending_unit.defence_bonuses[attacking_unit.type]

    effects = {"improved_weapons": 1, "improved_weapons_II_A": 1, "improved_weapons_II_B": 2}
    for name, value in effects.items():
        if defending_unit.has(name):
            defence += value

    if attacking_unit.range > 1 and defending_unit.has("tall_shield"):
        defence += 1

    if attacking_unit.range == 1 and defending_unit.has("melee_expert"):
        defence += 1

    if attacking_unit.range == 1 and defending_unit.has("big_shield"):
        defence += 2

    if action.is_crusading_II_defence(enemy_units):
        defence += 1

    if attacking_unit.has("sharpshooting"):
        defence = 1

    for effect in ["sabotaged", "sabotaged_II"]:
        if defending_unit.has(effect):
            defence = 0

    if attack_rating > 6:
        defence += 6 - attack_rating

    return defence


def get_attack_rating(attacking_unit, defending_unit, action, gamestate):

    attack = attacking_unit.attack
    player_units = gamestate.player_units()

    effects = {"is_lancing": 2, "is_lancing_II": 3}
    for effect, value in effects.items():
        if getattr(action, effect)():
            attack += value

    effects = {"is_crusading": 1, "is_crusading_II_attack": 1, "has_high_morale": 2, "has_high_morale_II_A": 2,
               "has_high_morale_II_B": 3}
    for effect, value in effects.items():
        if getattr(action, effect)(player_units):
            attack += value

    if attacking_unit.get("bribed"):
        attack += 1

    if attacking_unit.get("bribed_II"):
        attack += 2

    effects = {"improved_weapons": 3, "improved_weapons_II_A": 2, "improved_weapons_II_B": 3}
    for name, value in effects.items():
        if attacking_unit.has(name):
            attack += value

    if defending_unit.type in attacking_unit.attack_bonuses:
        attack += attacking_unit.attack_bonuses[defending_unit.type]

    if defending_unit.range == 1 and attacking_unit.has("melee_expert"):
        attack += 1

    if attacking_unit.has("far_sighted") and distance(action.end_at, action.target_at) < 4:
        attack -= 1

    return attack


def get_outcome(action, outcome):
    sub_outcome = outcome.for_position(action.target_at)
    if sub_outcome == SubOutcome.MISS:
        return " Miss"
    elif sub_outcome == SubOutcome.DEFEND:
        return " Defend"
    elif sub_outcome == SubOutcome.WIN:
        return " Win"
