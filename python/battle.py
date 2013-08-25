from common import *


def attack_successful(action, rolls, gamestate):
    
    attack = get_attack_rating(action.unit, action.target_unit, action, gamestate.player_units)
    
    return rolls.attack <= attack


def defence_successful(action, rolls, gamestate):

    attack_rating = get_attack_rating(action.unit, action.target_unit, action, gamestate.player_units)
    defence_rating = get_defence_rating(action.unit, action.target_unit, attack_rating, action, gamestate.enemy_units)
    
    return rolls.defence <= defence_rating
    

def get_defence_adjusters(attacking_unit, defending_unit, action, enemy_units):

    defence_adjusters = {}

    if attacking_unit.is_melee() and defending_unit.has(Trait.big_shield):
        defence_adjusters["Big shield"] = 2

    if action.is_crusading_defense(enemy_units, level=2):
        defence_adjusters["Crusading, level 2"] = 1

    if attacking_unit.type in defending_unit.defence_bonuses:
        defence_adjusters["Defence bonus"] = defending_unit.defence_bonuses[attacking_unit.type]

    if defending_unit.has(Effect.improved_weapons):
        defence_adjusters["Improved weapons"] = 1

    if attacking_unit.is_melee() and defending_unit.has(Trait.melee_expert):
        defence_adjusters["Melee expert"] = 1

    if attacking_unit.has(Trait.pikeman_specialist) and defending_unit.name == "Pikeman":
        defence_adjusters["Pikeman specialist"] = 1

    if attacking_unit.is_ranged() and defending_unit.has(Trait.tall_shield):
        defence_adjusters["Tall shield"] = 1

    if defending_unit.has(Trait.cavalry_specialist) and attacking_unit.type == Type.Cavalry:
        defence_adjusters["Cavalry specialist"] = 1

    if defending_unit.has(Trait.siege_weapon_specialist) and attacking_unit.type == Type.Siege_Weapon:
        defence_adjusters["Siege weapon specialist"] = 1

    return defence_adjusters


def get_defence_setters(attacking_unit, defending_unit):

    defence_setters = {}
    if attacking_unit.has(Trait.sharpshooting):
        defence_setters["sharpshooting"] = 1

    if defending_unit.has(Effect.sabotaged):
        defence_setters["sabotaged"] = 0

    return defence_setters


def get_defence_rating(attacking_unit, defending_unit, attack_rating, action, enemy_units):

    defence_setters = get_defence_setters(attacking_unit, defending_unit)

    if defence_setters:
        defence = min(defence_setters.values())

    else:
        defence = defending_unit.defence

        defence_adjusters = get_defence_adjusters(attacking_unit, defending_unit, action, enemy_units)

        for value in defence_adjusters.values():
            defence += value

    if attack_rating > 6:
        defence = defence - attack_rating + 6

    return defence


def get_attack_adjusters(attacking_unit, defending_unit, action, player_units):

    attack_adjusters = {}

    if action.lancing():
        attack_adjusters["Lancing"] = action.lancing()

    if action.is_crusading_attack(player_units):
        attack_adjusters["Crusading"] = 1

    if action.has_high_morale(player_units):
        attack_adjusters["High morale"] = 2

    if attacking_unit.get(Effect.bribed):
        attack_adjusters["Bribed"] = attacking_unit.get(Effect.bribed)

    if attacking_unit.has(Effect.improved_weapons, level=1):
        attack_adjusters["Improved weapons, level 1"] = 3

    if attacking_unit.has(Effect.improved_weapons, level=2):
        attack_adjusters["Improved weapons, level 1"] = 2

    if defending_unit.type in attacking_unit.attack_bonuses:
        attack_adjusters["Attack bonus"] = attacking_unit.attack_bonuses[defending_unit.type]

    if defending_unit.has(Trait.pikeman_specialist) and attacking_unit.name == "Pikeman":
        attack_adjusters["Pikeman specialist"] = 1

    if defending_unit.is_melee() and attacking_unit.has(Trait.melee_expert):
        attack_adjusters["Melee expert"] = 1

    if attacking_unit.has(Trait.far_sighted) and distance(action.end_at, action.target_at) < 4:
        attack_adjusters["Far sighted"] = -1

    if attacking_unit.has(Trait.cavalry_specialist) and defending_unit.type == Type.Cavalry:
        attack_adjusters["Cavalry specialist"] = 1

    if attacking_unit.has(Trait.siege_weapon_specialist) and defending_unit.type == Type.Siege_Weapon:
        attack_adjusters["Siege weapon specialist"] = 1

    if attacking_unit.has(Trait.fire_arrows) and defending_unit.type == Type.Siege_Weapon:
        attack_adjusters["Fire arrows"] = 3

    if attacking_unit.has(Trait.flanking) and defending_unit.type == Type.Infantry:
        attack_adjusters["Flanking"] = 2

    return attack_adjusters


def get_attack_rating(attacking_unit, defending_unit, action, player_units):
    attack = attacking_unit.attack

    attack_adjusters = get_attack_adjusters(attacking_unit, defending_unit, action, player_units)
    for value in attack_adjusters.values():
        attack += value

    return attack
