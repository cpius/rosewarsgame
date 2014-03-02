from common import *


def get_defence_adjusters(attacking_unit, defending_unit, action, gamestate):

    defence_adjusters = 0

    if attacking_unit.is_melee() and defending_unit.has(Trait.big_shield):
        defence_adjusters += 2

    if "No_Crusader" not in gamestate.ai_factors and action.is_crusading_defense(gamestate.enemy_units, level=2):
        defence_adjusters += 1

    if attacking_unit.type in defending_unit.defence_bonuses:
        defence_adjusters += defending_unit.defence_bonuses[attacking_unit.type]

    if defending_unit.has(Effect.improved_weapons):
        defence_adjusters += 1

    if attacking_unit.is_melee() and defending_unit.has(Trait.melee_expert):
        defence_adjusters += 1

    if attacking_unit.has(Trait.pikeman_specialist) and defending_unit.name == "Pikeman":
        defence_adjusters += 1

    if attacking_unit.is_ranged() and defending_unit.has(Trait.tall_shield):
        defence_adjusters += 1

    if defending_unit.has(Trait.cavalry_specialist) and attacking_unit.type == Type.Cavalry:
        defence_adjusters += 1

    if defending_unit.has(Trait.siege_weapon_specialist) and attacking_unit.type == Type.Siege_Weapon:
        defence_adjusters += 1

    return defence_adjusters


def get_defence_setters(attacking_unit, defending_unit):

    defence_setters = []
    if attacking_unit.has(Trait.sharpshooting):
        defence_setters.append(1)

    if defending_unit.has(Effect.sabotaged):
        defence_setters.append(0)

    return defence_setters


def get_defence(action, attack, gamestate):

    attacking_unit = action.unit
    defending_unit = action.target_unit

    defence_setters = get_defence_setters(attacking_unit, defending_unit)

    if defence_setters:
        defence = min(defence_setters)
    else:
        defence = defending_unit.defence + get_defence_adjusters(attacking_unit, defending_unit, action, gamestate)

    if attack > 6:
        defence = defence - attack + 6

    return defence


def get_attack(action, gamestate):

    attacking_unit = action.unit
    defending_unit = action.target_unit

    attack = attacking_unit.attack

    if action.lancing():
        attack += action.lancing()

    if action.flanking():
        attack += attacking_unit.get(Trait.flanking)

    if "No_player_Crusader" not in gamestate.ai_factors and action.is_crusading_attack(gamestate.player_units):
        attack += 1

    if "No_FlagBearer" not in gamestate.ai_factors and action.has_high_morale(gamestate.player_units):
        attack += 2

    if attacking_unit.has(Effect.bribed):
        attack += attacking_unit.get(Effect.bribed)

    if attacking_unit.has(Effect.improved_weapons, level=1):
        attack += 3

    if attacking_unit.has(Effect.improved_weapons, level=2):
        attack += 2

    if defending_unit.type in attacking_unit.attack_bonuses:
        attack += attacking_unit.attack_bonuses[defending_unit.type]

    if defending_unit.has(Trait.pikeman_specialist) and attacking_unit.name == "Pikeman":
        attack += 1

    if defending_unit.is_melee() and attacking_unit.has(Trait.melee_expert):
        attack += 1

    if attacking_unit.has(Trait.far_sighted) and distance(action.end_at, action.target_at) < 4:
        attack -= 1

    if attacking_unit.has(Trait.cavalry_specialist) and defending_unit.type == Type.Cavalry:
        attack += 1

    if attacking_unit.has(Trait.siege_weapon_specialist) and defending_unit.type == Type.Siege_Weapon:
        attack += 1

    if attacking_unit.has(Trait.fire_arrows) and defending_unit.type == Type.Siege_Weapon:
        attack += 3

    return attack
